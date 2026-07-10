# Round 01 — Phase 0/1: proxy viability + architecture pivot

## MEASURE
Starting state: plan reviewed and corrected (git remote discrepancy fixed). No
`ANTHROPIC_API_KEY`, no `ant` CLI locally (confirmed directly via `env | grep -i
anthropic` and `command -v ant`, not assumed). Netlify was the planned host.

## ARCHITECTURE PIVOT (before any code was written)
Becca said "you should just be using python for the computer vision." Verified via
WebFetch that Netlify Functions supports only JavaScript/TypeScript and Go (checked
both the Functions overview page and the Lambda-compatibility page — Python is not
mentioned as a runtime on either). Verified via WebFetch that Vercel Python Functions
are a first-class, documented runtime: `api/*.py` files defining a `handler`
(`BaseHTTPRequestHandler` subclass) become serverless functions automatically,
dependencies via `requirements.txt`, git-linked deploy to the same GitHub repo works
identically to how Netlify would have.

**Decision: move the proxy to Vercel, implemented in Python.** The core architecture
(server-side proxy holding the real key, task-enum contract, fixed server-side
prompts, structured JSON output, progressive enhancement, critic pass) is unchanged —
only the host and language changed. Updated `HYPOTHESES.json` and `PROTOCOL.md`
accordingly (see `architecture_pivot` key in HYPOTHESES.json for full reasoning).

## HYPOTHESIZE
Cheapest-to-falsify next: H0a (can the handler even be invoked locally as a plain
Python script, no Vercel CLI) and H1 (does request validation actually block bad
requests before they'd reach the API) — both fully testable without a key. H0c
(payload size) is also key-independent. H0b/H2/H3/H4/H6 all require a live key and
were expected to land as pending-key going in.

**Critique asked:** are we building the right thing before validating it works? Per
advisor guidance received before this round started: don't gold-plate the Phase 2/3/4
UIs on an unvalidated accuracy foundation. Decision: build full structural scaffolding
(the function, the client wiring, the degradation paths) since all of that is
independently testable and valuable regardless of accuracy — but do NOT claim or imply
the suggestions are validated anywhere in code comments, UI copy, or this log.

## EXECUTE
- `requirements.txt` collision check: root `requirements.txt` already exists for
  `python-docx` (used elsewhere, e.g. docx-reading scripts) — did NOT overwrite it.
  Created `api/requirements.txt` scoped to just the function's own dependency
  (`anthropic`), which is the documented Vercel convention for per-function deps.
- Wrote `api/vision-assess.py`: task-enum routing (facade|damage|critic), fixed
  server-side system prompts + JSON schemas per task (enums pulled verbatim from
  `floodapp.html` — BUILDING_TYPES, MATERIALS, AGE_BANDS with en-dashes, ARCH_STYLES,
  AFFECTED_AREAS, DAMAGE_CATEGORIES with the app's exact 9 keys), request validation
  (task/size/media-type/missing-fields checks + soft Origin check), uses the official
  `anthropic` Python SDK per the claude-api skill's guidance (not raw HTTP — this is a
  correction from the original Netlify-era plan which had assumed no-SDK raw fetch;
  Python + pip makes the SDK free to use, unlike the zero-build-step JS constraint that
  motivated avoiding it on Netlify).
- Wrote `overnight/v3-cv-build/artifacts/test_function_local.py`: loads the handler by
  file path (the deployed filename has a hyphen, not valid as a Python module name for
  normal `import`), drives `do_POST()` directly against a fake request/response pair.
  `--mock` mode stubs the Anthropic client; `--live` mode (needs a real key) hits
  reference photos from the local llmDamagev3 clone.

## VERIFY
```
$ python3 -m venv overnight/v3-cv-build/artifacts/venv && pip install -q anthropic
$ python3 overnight/v3-cv-build/artifacts/test_function_local.py --mock
=== H0a/H1: mock tests ===
  PASS  H0a happy path -> 200
  PASS  H0a happy path returns parsed JSON with buildingType
  PASS  H0a happy path calls Anthropic exactly once
  PASS  H1 reject: unknown task -> 400            (+ never calls Anthropic)
  PASS  H1 reject: missing image -> 400            (+ never calls Anthropic)
  PASS  H1 reject: bad media type -> 400           (+ never calls Anthropic)
  PASS  H1 reject: oversized image -> 413          (+ never calls Anthropic)
  PASS  H1 reject: critic without fields -> 400    (+ never calls Anthropic)
  PASS  H1 missing API key -> 500 (not a crash)
14/14 assertions passed
```

```
$ python3 overnight/v3-cv-build/artifacts/test_function_local.py --live
=== H0b: live tests ===
PENDING-KEY: no ANTHROPIC_API_KEY in environment; H0b/H2/H3/H4/H6 cannot run live.
```

H0c (payload size, no key needed): generated a synthetic oversized source photo
(sips-upscaled an llmDamagev3 reference photo to 8471×3549px / 3.75MB JPEG q95 — larger
than a typical phone photo, a deliberate stress case), then downscaled it via `sips` to
the exact client-side canvas target (long edge 1568px, JPEG q85):
```
$ sips -Z 1568 -s format jpeg -s formatOptions 85 synthetic_phone_photo.jpg --out downscaled.jpg
$ sips -g pixelWidth -g pixelHeight downscaled.jpg
  pixelWidth: 1568 / pixelHeight: 657
$ ls -la downscaled.jpg           # 251,578 bytes raw
$ base64 -i downscaled.jpg | wc -c  # 335,441 bytes base64
```
335KB ≪ 1.5MB target, ≪ the function's own 2,000,000-byte cap. **H0c: PASS.**

## LOG+PERSIST
- `HYPOTHESES.json` updated: H0a=pass, H1=pass, H0c=pass, H0b/H2/H3/H4/H6=pending-key
  (each with evidence or the reason it can't run yet).
- No git commit yet this round (batching Phase 0/1 + Phase 2/3 client wiring into one
  commit once the client side exists, per "additive & reversible" safety rail — the
  function alone isn't independently useful without the UI that calls it).

## Next round
Build Phase 2 (facade UI wiring) and Phase 3 (damage UI wiring) client-side in
`floodapp.html`, then Phase 4 (critic wiring), then Phase 5 (offline degradation
walkthrough — H5, fully testable without a key) and `deploy/` sync.
