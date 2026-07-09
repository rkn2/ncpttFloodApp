# Round 05 — wire the app to the cited bundle (D1.4)

## MEASURE
Start 6/11. Frontier [H5,H6,H7]. Move: D1.4 (connect content-bundle.json to floodapp.html).

## SELECT (gate note)
No separate Opus gate — D1.4 is a contained integration with an objective acceptance test; I
front-loaded gate budget onto R4 (synthesis) and will run the gate before P2's PWA/i18n (R6),
which carries real design choices. Documented deviation.

## EXECUTE (additive, floodapp.html)
- `loadContentBundle()` + `contentBundle` map; called at INIT alongside loadKB(). Silent fallback
  if content-bundle.json is absent.
- `guidanceBodyHtml(catKey)` — prefers the compiled cited record; falls back to built-in
  REPAIR_GUIDANCE. `citedItemHtml()` renders each do/dont with a 📄 whose TOOLTIP is the verbatim
  source quote + source label — provenance visible at point of use. Added a sources summary line
  and a `.cite` CSS style.
- Rewired the homeowner results guidance card to call guidanceBodyHtml (icon/label fall back too).
- Synced deploy/: index.html, content-bundle.json, knowledge-base.json.

## VERIFY (re-run, captured)
- **JS syntax**: extracted <script> (89KB) → `node --check` → OK.
- **Logic test (node)**: roof (in bundle) → cited tooltips + sources line + 11 cited items;
  mold (not in bundle) → falls back to hardcoded, no cite tooltips. PASS.
- **HTTP test**: served repo root — content-bundle.json 200, floodapp.html 200, app references
  loadContentBundle(), bundle delivers 6 records over HTTP. **D1.4 PASS.**

## Metric delta
6/11 → 7/11 (D1.4 DONE). D0.4 now PARTIAL: the 6 auto-synth categories render verified citations in
the app; the 3 safety-critical categories stay on built-in (uncited) text pending human authoring —
intentional, not a shortfall.

## CRITIQUE / carry-forward
- The app now shows source-cited guidance with the exact quote on hover — the grant's provenance
  claim is live in the UI, not just in a file.
- deploy/ is a full copy of floodapp.html (renamed index.html). Kept in sync by copy; noted for
  handoff that the app is single-source (floodapp.html) and deploy/ is generated.
- Next: R6 = P2. Opus gate first (PWA architecture + i18n approach are design decisions). H6 offline
  PWA (service worker + manifest, cache app shell + bundle + KB), H7 i18n + Spanish for PR.
