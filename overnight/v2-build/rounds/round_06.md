# Round 06 — offline PWA (D2.1)

## MEASURE
Start 7/11. Frontier [H6,H7]. Gate ran (P2 has real design choices).

## HYPOTHESIZE (Opus gate)
- H6 (PWA) before H7 (i18n): the offline shell must exist before it's worth translating.
- PRECACHE the 3.2MB KB (fail-closed), don't lazy-load — the flood use case needs full offline.
- **Versioned cache name + activate cleanup** is the #1 hand-written-SW failure mode (stale cache
  strands every future deploy) — bake a version constant in tonight.
- start_url './' consistently; navigation fallback to cached index.html.
- Groq is cross-origin → SW must exclude it (network-only, never cached); offline degrades to KB.
- Icons: SVG maskable data-URI acceptable given no PNG tooling.
- i18n: SCAFFOLD only (t()+table+switcher+Spanish homeowner flow), gate switcher behind 100%
  coverage + English fallback + untranslated-string lint. (→ next round.)

## SELECT / EXECUTE (all gate points adopted)
- `deploy/manifest.webmanifest` — name/start_url './'/display standalone/theme/SVG maskable icon.
- `deploy/icon.svg` — house + floodwater mark.
- `deploy/sw.js` — CACHE_VERSION constant (bump-per-deploy, commented), precache SHELL
  [./ , index.html, content-bundle.json, knowledge-base.json, manifest, icon] via addAll
  (fail-closed), activate deletes old caches, cache-first fetch, cross-origin (Groq) passthrough
  never cached, navigation fallback to cached index.html.
- floodapp.html: `<link rel=manifest>` + theme-color + apple-touch-icon; guarded SW registration on
  load (silent no-op in dev). Synced deploy/index.html.

## VERIFY (re-run, captured)
- manifest valid JSON w/ required fields; sw.js `node --check` OK; versioned cache + activate cleanup
  present.
- **Coverage test (node):** every same-origin fetch the app makes (knowledge-base.json,
  content-bundle.json) is in SHELL; Groq is the only cross-origin fetch and is excluded. PASS.
- **HTTP test (serve deploy/):** all 7 shell resources return 200 (install would succeed); app
  registers sw.js + links manifest.
- **NOT runnable here:** the actual airplane-mode reload (no headless browser in this env). Every
  mechanical precondition passes; this needs ONE manual browser confirmation (documented in handoff).

## Metric delta
7/11 → 8/11 (D2.1 DONE*, * = 1 manual browser offline-check pending; all preconditions validated).

## CRITIQUE / carry-forward
- Honest limit: I validated the offline machinery, not the browser behavior. Handoff step for Becca:
  open the deployed site once online, then DevTools→Network→Offline (or airplane mode) and reload —
  it should load fully. If not, the usual cause is start_url/scope mismatch on the host.
- CACHE_VERSION must be bumped every deploy — called out in sw.js and the handoff.
- Next R7: H7 i18n scaffold + Spanish homeowner flow (final build deliverable), then FINAL_REPORT.
