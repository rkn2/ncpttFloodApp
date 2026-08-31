# FloodApp — Remaining TODO

## Becca's Actions (not code)

- [ ] **Set up Google Sheets sync** — Create a Google Sheet, paste `sync/google-apps-script.js` into Extensions → Apps Script, deploy as web app (Execute as: Me, Who has access: Anyone), paste the deployment URL into `SYNC_ENDPOINT` in floodapp.html (~line 3316), commit + push
- [ ] **Publish Sheet for dashboard** — In that Sheet: File → Share → Publish to web → select "Rapid Triage" tab → CSV → Publish. Open https://rkn2.github.io/ncpttFloodApp/dashboard.html and paste the CSV URL
- [ ] **Get PR SHPO/ICP review of Spanish translation** — `content-bundle.es.json` is marked `entailment_audited: false`. Spanish guidance text needs SHPO sign-off before reporting as authoritative
- [ ] **Frame CV decision in next progress report** — Decided against with evidence (see `overnight/v3-cv-build/DECISION.md`). Explain as a reasoned scope decision, not a silent omission
- [ ] **Design evaluation plan** — What should the PR PhD fieldwork measure? What feedback to capture? Once decided, telemetry can be wired into the app

## Code TODO (ask Claude)

- [ ] Fix 8 moderate/minor WCAG items (touch targets, fieldset/legend, autocomplete attrs, citation accessibility)
- [ ] Add evaluation telemetry (after Becca decides what to capture)
- [ ] Add more states/territories to `programs.json`

## Done This Session (2026-08-31)

- [x] Full Spanish i18n — homeowner path complete (130+ UI strings + 76 guidance items)
- [x] content-bundle.es.json with verified citation preservation
- [x] SHPO sync client — offline-first queue with Google Sheets backend
- [x] Geolocation + address auto-populate (homeowner + assessor)
- [x] Assessment form alignment with NCPTT source forms (roof covering, construction type, occupancy, flood data in Full)
- [x] 6 crosswalk should-fixes (affiliation, area inspected, occupied/repairs begun, sediment split, collapsed/off-foundation, escalation carry-forward)
- [x] STATE_PROGRAMS extracted to programs.json (transferability)
- [x] SHPO dashboard with map, filtering, stats
- [x] WCAG/508 audit + all critical/serious fixes (8 of 16)
- [x] GitHub Pages deployment (replacing Netlify)
- [x] "Not sure" options + interior question split
- [x] Standing water safety tip
