"""H0a/H1/H0b test harness for api/vision-assess.py.

Loads the handler by file path (the deployed filename has a hyphen, which
isn't a valid Python module name for a normal import) and drives it as a
BaseHTTPRequestHandler would be driven by Vercel's runtime: a fake request
with headers + a body stream, then inspect what got written to the response.

Usage:
    python3 test_function_local.py --mock   # H0a + H1, no network, no key needed
    python3 test_function_local.py --live   # H0b, needs ANTHROPIC_API_KEY in env
"""
from __future__ import annotations

import argparse
import base64
import importlib.util
import io
import json
import sys
import time
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
FUNC_PATH = ROOT / "api" / "vision-assess.py"


def load_module():
    spec = importlib.util.spec_from_file_location("vision_assess", FUNC_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class FakeRequest:
    """Enough of a socket-like object for BaseHTTPRequestHandler.__init__."""
    def makefile(self, *args, **kwargs):
        return io.BytesIO()


def invoke(mod, body_dict: dict) -> tuple[int, dict]:
    """Drive handler.do_POST() directly, bypassing the socket layer."""
    body_bytes = json.dumps(body_dict).encode("utf-8")
    h = mod.handler.__new__(mod.handler)
    h.rfile = io.BytesIO(body_bytes)
    h.wfile = io.BytesIO()
    h.headers = {"Content-Length": str(len(body_bytes))}
    h.client_address = ("127.0.0.1", 0)

    captured = {"status": None, "headers": []}

    def fake_send_response(status, *_):
        captured["status"] = status

    def fake_send_header(k, v):
        captured["headers"].append((k, v))

    def fake_end_headers():
        pass

    h.send_response = fake_send_response
    h.send_header = fake_send_header
    h.end_headers = fake_end_headers

    h.do_POST()

    raw_out = h.wfile.getvalue()
    parsed = json.loads(raw_out) if raw_out else {}
    return captured["status"], parsed


def tiny_jpeg_b64() -> str:
    # 1x1 white JPEG, valid image bytes so mediaType/size checks pass in mock mode.
    b64 = (
        "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkI"
        "CQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD/2wBDAQMDAwQDBAgEBAgQCwkLEBAQEBAQ"
        "EBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBD/wAARCAABAAEDASIA"
        "AhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAf/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEB"
        "AQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX"
        "/9k="
    )
    return b64


def run_mock_tests():
    mod = load_module()
    good_img = tiny_jpeg_b64()
    results = []

    def check(name, ok, detail=""):
        results.append((name, ok, detail))
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""))

    # --- H0a: happy path, Anthropic call stubbed ---
    fake_response = mock.Mock()
    fake_response.content = [mock.Mock(type="text", text=json.dumps({
        "buildingType": {"value": "Single-family residential", "confidence": "high", "reasoning": "test"},
        "materials": {"values": ["Wood frame"], "confidence": "high", "reasoning": "test"},
        "age": None, "archStyle": None, "limitations": "test",
    }))]
    fake_response.usage = mock.Mock(input_tokens=100, output_tokens=50)

    with mock.patch.object(mod, "Anthropic") as MockClient, \
         mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-test-fake"}):
        MockClient.return_value.messages.create.return_value = fake_response
        status, body = invoke(mod, {"task": "facade", "imageBase64": good_img, "mediaType": "image/jpeg"})
        check("H0a happy path -> 200", status == 200, f"status={status}")
        check("H0a happy path returns parsed JSON with buildingType", "buildingType" in body, str(body)[:200])
        check("H0a happy path calls Anthropic exactly once",
              MockClient.return_value.messages.create.call_count == 1)

    # --- H1: rejection paths, Anthropic must NEVER be called ---
    reject_cases = [
        ("unknown task", {"task": "bogus", "imageBase64": good_img, "mediaType": "image/jpeg"}, 400),
        ("missing image", {"task": "facade", "mediaType": "image/jpeg"}, 400),
        ("bad media type", {"task": "facade", "imageBase64": good_img, "mediaType": "image/gif"}, 400),
        ("oversized image", {"task": "facade", "imageBase64": "A" * (mod.MAX_IMAGE_BYTES_B64 + 1),
                              "mediaType": "image/jpeg"}, 413),
        ("critic without fields", {"task": "critic", "imageBase64": good_img, "mediaType": "image/jpeg"}, 400),
    ]
    for name, payload, expected_status in reject_cases:
        with mock.patch.object(mod, "Anthropic") as MockClient, \
             mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-test-fake"}):
            status, body = invoke(mod, payload)
            check(f"H1 reject: {name} -> {expected_status}", status == expected_status,
                  f"got status={status} body={body}")
            check(f"H1 reject: {name} never calls Anthropic",
                  MockClient.return_value.messages.create.call_count == 0)

    # --- H1: missing API key -> clean 500, not a crash ---
    with mock.patch.dict("os.environ", {}, clear=True):
        import os as _os
        _os.environ.pop("ANTHROPIC_API_KEY", None)
        status, body = invoke(mod, {"task": "facade", "imageBase64": good_img, "mediaType": "image/jpeg"})
        check("H1 missing API key -> 500 (not a crash)", status == 500, f"status={status} body={body}")

    passed = sum(1 for _, ok, _ in results if ok)
    print(f"\n{passed}/{len(results)} assertions passed")
    return passed == len(results)


def run_live_tests():
    import os
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("PENDING-KEY: no ANTHROPIC_API_KEY in environment; H0b/H2/H3/H4/H6 cannot run live.")
        return None

    mod = load_module()
    ref_dir = ROOT.parent / "068ccfb5-c8ea-4e77-9996-ba29d67774ce" / "scratchpad" / "llmDamagev3" / "ref_photos" / "after"
    photos = list(ref_dir.rglob("*.jpg"))[:2] + list(ref_dir.rglob("*.png"))[:1]
    if not photos:
        print(f"No reference photos found under {ref_dir}; cannot run H0b live test.")
        return False

    results = []
    for photo in photos[:3]:
        media_type = "image/png" if photo.suffix.lower() == ".png" else "image/jpeg"
        b64 = base64.standard_b64encode(photo.read_bytes()).decode()
        t0 = time.monotonic()
        try:
            status, body = invoke(mod, {"task": "damage", "imageBase64": b64, "mediaType": media_type})
        except Exception as e:
            print(f"  FAIL  {photo.name}: exception {e}")
            results.append(False)
            continue
        latency = time.monotonic() - t0
        ok = status == 200 and "categories" in body
        under_budget = latency < 8.0
        usage = body.get("_usage", {})
        print(f"  {'PASS' if ok and under_budget else 'FAIL'}  {photo.name}  "
              f"status={status} latency={latency:.1f}s usage={usage}")
        results.append(ok and under_budget)

    passed = sum(results)
    print(f"\n{passed}/{len(results)} live calls passed (status 200, valid schema, <8s)")
    return passed == len(results) and len(results) > 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    if not args.mock and not args.live:
        args.mock = True

    ok = True
    if args.mock:
        print("=== H0a/H1: mock tests ===")
        ok = run_mock_tests() and ok
    if args.live:
        print("\n=== H0b: live tests ===")
        result = run_live_tests()
        if result is not None:
            ok = result and ok

    sys.exit(0 if ok else 1)
