"""Server-side proxy for photo-based building/damage suggestions.

The browser never holds an Anthropic API key. It POSTs a downscaled photo
plus a fixed `task` name; all prompts and JSON schemas live here, so this
endpoint cannot be repurposed as a general-purpose Claude proxy. Stateless:
image in, JSON out, nothing logged or persisted.

Enum strings below (buildingType, materials, age, DAMAGE_CATEGORIES,
affectedAreas, ARCH_STYLES) must stay byte-identical to floodapp.html --
they are what "Apply suggestion" writes into the existing form state.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from anthropic import Anthropic

MODEL = "claude-sonnet-5"
MAX_IMAGE_BYTES_B64 = 2_000_000  # ~1.5MB raw image, base64-inflated; see H0c
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")

BUILDING_TYPES = [
    "Single-family residential", "Multi-family residential",
    "Commercial / mixed-use", "Civic / institutional",
]
MATERIALS = ["Wood frame", "Masonry (brick / stone)", "Concrete", "Mixed"]
AGE_BANDS = ["Pre-1870", "1870–1940", "1940–1970", "Post-1970"]
ARCH_STYLES = [
    "Federal / Early Republic (pre-1830)", "Greek Revival (1825–1860)",
    "Italianate (1840–1885)", "Gothic Revival (1840–1880)",
    "Second Empire (1855–1885)", "Queen Anne (1880–1910)",
    "Romanesque Revival (1880–1900)", "Colonial Revival (1880–1955)",
    "Craftsman / Bungalow (1905–1930)", "Tudor Revival (1890–1940)",
    "Spanish Colonial Revival (1915–1940)", "Art Deco (1925–1940)",
    "Mid-Century Modern (1940–1970)", "Vernacular / Folk (no specific style)",
    "Other / Unknown",
]
AFFECTED_AREAS = ["Basement / crawl space", "First floor", "Upper floors", "Exterior / site"]
DAMAGE_CATEGORIES = [
    ("structural", "Structural / Foundation"), ("roof", "Roof"),
    ("siding", "Exterior Walls / Siding"), ("windows", "Windows and Doors"),
    ("chimney", "Chimney"), ("electrical", "Electrical / Mechanical / HVAC"),
    ("insulation", "Insulation"), ("interior", "Interior Finishes"),
    ("mold", "Mold / Contamination"),
]
SEVERITY_LEVELS = ["none", "minor", "moderate", "severe", "not_assessable"]

WATER_LINE_RUBRIC = """Severity anchors, by how high floodwater visibly reached on this category:
- none: no visible water line, staining, or damage on this element
- minor: water reached below floor-joist height (crawlspace/basement contact only);
  cosmetic staining, no structural or functional damage
- moderate: water reached partway up the element (joist to mid-wall height);
  material replacement needed but framing/structure intact
- severe: water covered the full element or higher; structural/functional
  compromise, or total loss of the material
- not_assessable: this category is not visible in the photo (e.g. interior
  finishes from an exterior shot) -- do NOT guess"""


def _facade_schema() -> dict:
    def field(enum, extra_null=True):
        value_schema = {"type": "string", "enum": enum}
        return {
            "anyOf": [
                {
                    "type": "object",
                    "properties": {
                        "value": value_schema,
                        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                        "reasoning": {"type": "string"},
                    },
                    "required": ["value", "confidence", "reasoning"],
                    "additionalProperties": False,
                },
                {"type": "null"},
            ]
        } if extra_null else value_schema

    return {
        "type": "object",
        "properties": {
            "buildingType": field(BUILDING_TYPES),
            "materials": {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "values": {"type": "array", "items": {"type": "string", "enum": MATERIALS}},
                            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                            "reasoning": {"type": "string"},
                        },
                        "required": ["values", "confidence", "reasoning"],
                        "additionalProperties": False,
                    },
                    {"type": "null"},
                ]
            },
            "age": field(AGE_BANDS),
            "archStyle": field(ARCH_STYLES),
            "limitations": {"type": "string"},
        },
        "required": ["buildingType", "materials", "age", "archStyle", "limitations"],
        "additionalProperties": False,
    }


def _damage_schema() -> dict:
    cat_props = {}
    for key, _label in DAMAGE_CATEGORIES:
        cat_props[key] = {
            "type": "object",
            "properties": {
                "severity": {"type": "string", "enum": SEVERITY_LEVELS},
                "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                "reasoning": {"type": "string"},
            },
            "required": ["severity", "confidence", "reasoning"],
            "additionalProperties": False,
        }
    return {
        "type": "object",
        "properties": {
            "categories": {
                "type": "object",
                "properties": cat_props,
                "required": [k for k, _ in DAMAGE_CATEGORIES],
                "additionalProperties": False,
            },
            "affectedAreas": {"type": "array", "items": {"type": "string", "enum": AFFECTED_AREAS}},
            "limitations": {"type": "string"},
        },
        "required": ["categories", "affectedAreas", "limitations"],
        "additionalProperties": False,
    }


def _critic_schema() -> dict:
    return {
        "type": "object",
        "properties": {
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "field": {"type": "string"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                        "issue": {"type": "string"},
                    },
                    "required": ["field", "severity", "issue"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["findings"],
        "additionalProperties": False,
    }


FACADE_SYSTEM = f"""You are assisting a homeowner filling out a historic-building flood
recovery form. Look at ONE facade photo and suggest values for these fields, using ONLY
what is visibly evident in the photo -- never guess or infer from context you cannot see.

Building type options: {BUILDING_TYPES}
Construction material options (select all visibly evident): {MATERIALS}
Approximate age band options: {AGE_BANDS}
Architectural style options: {ARCH_STYLES}

For each field, return null for the whole field if you cannot make a reasonable visual
judgment -- do not force a guess. National Register / historic designation status is
NEVER inferable from a photo and is not part of this task."""

DAMAGE_SYSTEM = f"""You are assisting with a flood damage assessment for a historic
building. Look at ONE photo taken after a flood and suggest a severity for whichever of
these 9 categories are actually visible in the photo. Mark categories not visible in
frame as "not_assessable" -- do not guess at damage you cannot see.

Categories: {[label for _, label in DAMAGE_CATEGORIES]}

{WATER_LINE_RUBRIC}

Also suggest which general areas of the building show flood impact, from:
{AFFECTED_AREAS}"""

CRITIC_SYSTEM = """You are an adversarial reviewer. You will see one photo and a set of
field values someone (or an earlier AI pass) proposed for that photo. Check ONLY
whether each given value is directly contradicted by what is visible in the photo --
flag CONTRADICTS-PHOTO issues only. Do not flag a value merely because you are
uncertain or would have chosen differently; only flag clear, defensible
contradictions. If a value looks fine, do not include it in the findings list at all."""


def _image_block(image_b64: str, media_type: str) -> dict:
    return {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_b64}}


def _run_task(client: Anthropic, task: str, image_b64: str, media_type: str, fields: dict | None) -> dict:
    img = _image_block(image_b64, media_type)
    if task == "facade":
        system, schema, max_tokens = FACADE_SYSTEM, _facade_schema(), 1200
        content = [img, {"type": "text", "text": "Suggest building attributes for this facade."}]
    elif task == "damage":
        system, schema, max_tokens = DAMAGE_SYSTEM, _damage_schema(), 1500
        content = [img, {"type": "text", "text": "Suggest flood damage severity per category for this photo."}]
    elif task == "critic":
        system, schema, max_tokens = CRITIC_SYSTEM, _critic_schema(), 800
        proposed = json.dumps(fields or {}, indent=2)
        content = [img, {"type": "text", "text": f"Proposed field values to check against this photo:\n{proposed}"}]
    else:
        raise ValueError(f"unknown task {task!r}")

    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        thinking={"type": "disabled"},
        output_config={"format": {"type": "json_schema", "schema": schema}},
        messages=[{"role": "user", "content": content}],
    )
    text = next(b.text for b in response.content if b.type == "text")
    result = json.loads(text)
    result["_usage"] = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
    return result


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self) -> None:
        # Soft abuse deterrent only -- Origin/Referer are trivially spoofable outside a
        # browser. The real backstop is the Anthropic workspace spend cap (see
        # overnight/v3-cv-build/PROTOCOL.md PENDING-HUMAN). Skipped entirely when
        # ALLOWED_ORIGIN is left at its "*" default, so a fresh deploy isn't locked out
        # before Becca configures it.
        if ALLOWED_ORIGIN != "*":
            origin = self.headers.get("Origin", "")
            if origin and urlparse(origin).netloc != urlparse(ALLOWED_ORIGIN).netloc:
                self._send_json(403, {"error": "origin not allowed"})
                return

        length = int(self.headers.get("Content-Length", 0))
        if length <= 0 or length > MAX_IMAGE_BYTES_B64 + 10_000:
            self._send_json(413, {"error": "request body too large or empty"})
            return

        raw = self.rfile.read(length)
        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid JSON body"})
            return

        task = body.get("task")
        image_b64 = body.get("imageBase64")
        media_type = body.get("mediaType", "image/jpeg")
        fields = body.get("fields")

        if task not in ("facade", "damage", "critic"):
            self._send_json(400, {"error": f"unknown task {task!r}; must be facade, damage, or critic"})
            return
        if not image_b64 or not isinstance(image_b64, str):
            self._send_json(400, {"error": "imageBase64 is required"})
            return
        if len(image_b64) > MAX_IMAGE_BYTES_B64:
            self._send_json(413, {"error": "image too large; downscale before uploading"})
            return
        if media_type not in ("image/jpeg", "image/png", "image/webp"):
            self._send_json(400, {"error": f"unsupported mediaType {media_type!r}"})
            return
        if task == "critic" and not fields:
            self._send_json(400, {"error": "critic task requires fields to check"})
            return

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            self._send_json(500, {"error": "server misconfigured: no API key set"})
            return

        try:
            client = Anthropic(api_key=api_key)
            result = _run_task(client, task, image_b64, media_type, fields)
        except Exception as e:  # noqa: BLE001 -- surface to caller, never a silent 500
            self._send_json(502, {"error": f"vision call failed: {e}"})
            return

        self._send_json(200, result)
