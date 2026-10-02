# FloodApp — Remaining TODO

## Becca's Actions (not code)

- [ ] **Set up Google Sheets sync** — Create a Google Sheet, paste `sync/google-apps-script.js` into Extensions → Apps Script, deploy as web app (Execute as: Me, Who has access: Anyone), paste the deployment URL into `SYNC_ENDPOINT` in floodapp.html (~line 3316), commit + push
- [ ] **Publish Sheet for dashboard** — In that Sheet: File → Share → Publish to web → select "Rapid Triage" tab → CSV → Publish. Open https://rkn2.github.io/ncpttFloodApp/dashboard.html and paste the CSV URL
- [ ] **Get PR SHPO/ICP review of Spanish translation** — `content-bundle.es.json` is marked `entailment_audited: false`. Spanish guidance text needs SHPO sign-off before reporting as authoritative
- [ ] **Native-speaker/SHPO review of changed Spanish strings (2026-10-02)**: `floodapp.html` I18N.es `results_district`, `results_local`, `results_eligible` (new Section 106 messages, replacing `results_unlisted`); `content-bundle.es.json` siding `do` item on removing flooded insulation (closed-cell board exception) and insulation `do` item on fiberglass batts (now remove-by-default); mold carpeting item moved from `dont` to `do` (text unchanged)
- [ ] **Native-speaker/SHPO review of new Spanish file `pa-guidance.es.json` (2026-10-02, nonprofit/public-owner Public Assistance path)**: `panel_title`, `panel_intro`, `label_do`/`label_dont`/`label_source`/`label_page`, the three `sources` names, all 10 record `label`/`summary` strings, all 44 `do`/`dont` item texts, and `notes.age45_pa` / `notes.age45_private`. Quotes stay in English (verified verbatim). Both files are `entailment_audited: false`
- [ ] **Review `pa-guidance.json` item wording against its quotes (entailment)** — `python3 pipeline/verify_pa_guidance.py pa-guidance.json --es pa-guidance.es.json` checks all 73 quotes are verbatim and on the cited printed page, but nobody has yet checked that each plain-language item says only what its quotes support
- [ ] **Native-speaker/SHPO review of new Spanish UI strings (2026-10-02, PA path)**: `floodapp.html` I18N.es `owner_legend`, `owner_hint`, `owner_private`, `owner_nonprofit`, `owner_government` (new "Who owns this building?" question), `results_pa`, `results_pa_assist_note`, `pa_unavailable`, `as_pa_intro`
- [ ] **Native-speaker/SHPO review of new/changed Spanish UI strings (2026-10-02, building age and Section 106)**: `floodapp.html` I18N.es `age_legend`, `age_hint`, `age_old`, `age_new`, `age_unsure`, `age45_lead_yes`, `age45_lead_maybe` (new), and `results_listed` (reworded to "exige revisar cómo les afectan los trabajos" wording)
- [ ] **Decide on the private-owner 45-year note** — for private homeowners the app now says FEMA's *Public Assistance* rules send work on 45+-year-old buildings to more detailed historic review (PAPPG p.237) and that household grants are also covered by historic preservation law (IAPPG p.14). The IAPPG has no 45-year rule, so the note doesn't claim household-grant repairs will get that review. Keep, soften or drop for homeowners
- [ ] **Confirm the National Heritage Responders contact is current** — `pa-guidance.json` `help` gives institutions (202) 661-8068 and individuals NHRpublichelpline@culturalheritage.org, cited to the 2023 Texas Historical Commission handbook p.19 (the PAPPG doesn't list it)
- [ ] **Native-speaker/SHPO review of new Spanish strings (2026-10-02, homeowner aid)**: `programs.json` national `desc_es`/`note_es` for FEMA IA (historic-home note, safe/sanitary/functional framing, $44,800 cap), SBA (loan limits; apply even if you don't want a loan) and NPS/SHPO (Section 106 listed-or-eligible wording); `content-bundle.es.json` structural `do` item on FEMA basement repair limits; new `recovery_aid` record (label "Seguro, FEMA y SBA", summary, 7 `do` and 3 `dont` items on flood insurance, claims, documenting damage, the SFHA flood insurance requirement and SBA)
- [ ] **Decide on the IHP cap in `programs.json`** — FEMA IA desc says $44,800 for disasters declared on or after 2025-10-01 (Federal Register 2026-19854). A notice for disasters declared from 2026-10-01 could appear any time; update or drop the figure then
- [ ] **Frame CV decision in next progress report** — Decided against with evidence (see `overnight/v3-cv-build/DECISION.md`). Explain as a reasoned scope decision, not a silent omission
- [ ] **Design evaluation plan** — What should the PR PhD fieldwork measure? What feedback to capture? Once decided, telemetry can be wired into the app

## Code TODO (ask Claude)

- [ ] Fix 8 moderate/minor WCAG items (touch targets, fieldset/legend, autocomplete attrs, citation accessibility)
- [ ] Add evaluation telemetry (after Becca decides what to capture)
- [ ] Add more states/territories to `programs.json`
- [x] Render the `recovery_aid` bundle record (2026-10-02: insurance panel + "Common mistakes to avoid"); service worker cache bumped to v11
- [x] `results_listed` (EN/ES) aligned with the Section 106 "review of effects" wording (2026-10-02)
- [ ] EN bundle `provenance_note` says every item passed the entailment audit; no longer true for hand-edited items (`entailment_audited: false`). Re-run the audit or reword the note

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
