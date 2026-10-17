# FloodApp — Remaining TODO

## Done 2026-10-17 (commits `90ff453` → this one)
- [x] Source labels: card footers and quote markers show publication titles (`SOURCE_TITLES` in `floodapp.html`), not file names
- [x] Vermont `programs.json` entry reworded to the listed-or-eligible Section 106 wording
- [x] EN bundle `provenance_note` no longer claims hand-edited items passed the entailment audit
- [x] Install banner (Install button on Chrome/Android, Share → Add to Home Screen steps on iPhone), PNG home-screen icons, and a printable EN/ES QR flyer at https://rkn2.github.io/ncpttFloodApp/flyer.html
- [x] WCAG audit items 9–16 fixed; axe-core over every screen reports 0 violations (see `overnight/wcag-audit.md`). A VoiceOver pass is still worth doing
- [x] Chat KB rebuilt with PAPPG v5 + IAPPG v1.1, ligatures folded, duplicate PDFs skipped (5,771 chunks, 5.3 MB, still gitignored and not deployed)
- [x] 18-month deadline verified: 44 CFR 206.204(c)(1) sets all completion deadlines "from the date that a major disaster or emergency is declared". Figure 21 (PAPPG p.247) is only a table (Emergency 6 months; Permanent C–G 18 months; Category I 180 days). The app's wording is correct; no change
- [x] Entailment review written: `docs/reviews/2026-10-17-entailment-review.md` (decisions below)

## Decisions from the 2026-10-17 entailment review (Becca)
Source: `docs/reviews/2026-10-17-entailment-review.md`, which has the item, quote, problem and a suggested rewording for each. `pa-guidance.json`: 29 of 56 items fully supported; `content-bundle.json` unaudited items: 9 of 11. Any rewording must be mirrored in the `.es.json` file with identical citations.
- [ ] **SHPO advice** in `ehp_first.summary`, `ehp_first.do[0]`, `notes.age45_pa`, `notes.age45_private`: no cited quote tells owners to contact the SHPO (FEMA consults the SHPO). Also `age45_pa` "need" → "may need" (in-kind repair gets streamlined review regardless of age)
- [ ] **Extensions** (`deadlines.do[0..1]`): "a good reason" → FEMA's "extenuating circumstances beyond your control"
- [ ] **Flood insurance** (`dont[0]`, `dont[1]`): restore "NFIP-insurable", the non-participating-community PNP exception, and the $5,000 waiver
- [ ] **Vacant buildings** (`other_rules.dont[0]`): add the third exception (intent to begin use within a reasonable time)
- [ ] **Mixed use** (`other_rules.do[1]`): add "must restore the entire facility"
- [ ] **Mold** (`document.do[3]`): add "document and justify"
- [ ] **SBA** (`sba.summary`, `sba.do[0]`): "community centers" / "most other nonprofits" unsupported; the rule is per facility
- [ ] **Photos** (`document.do[0]`): first sentence (photograph damage before cleanup) needs its own citation
- [ ] **Bundle `recovery_aid` do[5]**: "can't get FEMA help in a future flood" → household aid for NFIP-insurable items only
- [x] **Household-program items hidden from nonprofit/government owners** (2026-10-17): the 7 bundle items citing the IAPPG (structural basement limits; 5 `recovery_aid` do + 2 dont on FEMA home repair, SFHA insurance, SBA) carry `owners: ["private"]` and are hidden on the homeowner path when the owner is nonprofit or government. General claims/documentation items still show
- [ ] 7 items are true but cite nearby text; add the citations the report lists (all pre-checked with the verifier)

## NEXT UP: from the FEMA PAPPG review (2026-10-02)

Source: `docs/reviews/2026-10-02-pappg-v4-review.md` and `docs/reviews/pappg-v5-cite-map.md`. The detailed items are under Becca's Actions and Code TODO below; this is the short list, in priority order.

**Decisions for Becca**
- [ ] **Fiberglass batts.** The app now says remove wet insulation by default (closed-cell foam board is the only exception), citing NTHP. NTHP's technical section also has one sentence saying fiberglass batts "must be evaluated on a case-by-case basis", which the app no longer shows. Confirm with Simeon, or bring it back (`content-bundle.json` ~:73, ~:367; commit `bfefccc`)
- [ ] **45-year note for private homeowners.** Keep the softer version, change it, or drop it (see the item below)
- [ ] **30-day decline item** in `recovery_aid`. It's accurate, but it tells owners how to opt out of the flood-insurance requirement (IAPPG pp.66-67). Keep or cut
- [ ] **NHR hotline and email.** The phone number (202) 661-8068 matches HENTF's 2026-09-29 DR-4933-IN email. The email addresses come from a 2023 source; confirm them (see the item below)
- [x] **Vermont entry in `programs.json`.** (Done 2026-10-17.) It still says listed and contributing structures "may qualify for additional review support", which wrongly implies designation is required. Reword to the listed-or-eligible Section 106 wording
- [ ] **$44,800 IHP cap.** Not covered by any citation check. Update it when FEMA publishes the next annual notice, or drop it (see the item below)
- [ ] **Assessor occupancy mapping.** "Museum / gallery" gets the nonprofit Public Assistance guidance, so a for-profit gallery gets it too. "Post-1970" and "Unknown" ages get the "if built in…" note. OK as is?
- [ ] **Entry card hint.** Nonprofit and public staff still start from the "Homeowner / Property Owner" card. Add a hint like "also for churches, museums, local governments"?
- [ ] **Cutoff year edge case.** "Built in 1981 or earlier" is only 45+ years old for part of the cutoff year. Fine for guidance?

**Verification still open**
- [x] **18-month permanent-work deadline.** (Resolved 2026-10-17, see above.) No text in PAPPG v5 says when this clock starts; only emergency work is tied to the declaration date (p.247). Figure 21 may say, but it's an image. Check it by hand, then fix the wording in `pa-guidance.json` if needed
- [x] **Entailment review.** (Report done 2026-10-17; decisions above.) Check that every plain-language item in `pa-guidance.json` and the hand-edited bundle items says only what its quotes support. Then re-run the audit or reword the EN bundle's `provenance_note` (see Code TODO)
- [ ] **Spanish review.** All new or changed ES strings from 2026-10-02 need native-speaker or SHPO review (four items below)

**Code / build**
- [x] **Rebuild the chat knowledge base** (done 2026-10-17) with `python3 build-kb.py` so the chat can draw on `docs/fema-pappg-v5.0-amended-2025.pdf` and `docs/fema-iappg-v1.1-amended-2025.pdf`. Make the extractor normalize the ligatures ﬂ and ﬁ, or searches for "flood" will miss text. `knowledge-base.json` is gitignored and about 3 MB; check its size afterward
- [ ] **Keep App. H out.** Never add PAPPG App. H's "photocopy and discard valuable papers" to the collections guidance; it contradicts conservation practice
- [ ] **Watch for PAPPG v5.1.** FEMA has announced it. When it comes out, re-run the cite map and `pipeline/verify_pa_guidance.py`

**Done 2026-10-02** (commits `45ecada` → `b61c3ac`)
- [x] Section 106 messages split into listed, contributing, local and not-sure/eligible, with the age note at 45+ years (PAPPG v5 p.237)
- [x] Wet insulation made consistent; flooded carpeting moved to "Do this"
- [x] `programs.json`: FEMA IA note (safe, sanitary and functional repairs only), SBA note (no longer backwards), NPS/SHPO listed-or-eligible wording
- [x] New `recovery_aid` homeowner guidance (NFIP, documentation, SBA) and basement repair limits
- [x] Nonprofit/public owner Public Assistance path (`pa-guidance.json`/`.es.json`; checked by `pipeline/verify_pa_guidance.py`)
- [x] PAPPG v5.0 Amended and IAPPG v1.1 added to `docs/`, plus the v4-to-v5 cite map
- [x] Service worker cache bumped to v12

## Becca's Actions (not code)

- [ ] **Set up Google Sheets sync** — Create a Google Sheet, paste `sync/google-apps-script.js` into Extensions → Apps Script, deploy as web app (Execute as: Me, Who has access: Anyone), paste the deployment URL into `SYNC_ENDPOINT` in floodapp.html (~line 3316), commit + push
- [ ] **Publish Sheet for dashboard** — In that Sheet: File → Share → Publish to web → select "Rapid Triage" tab → CSV → Publish. Open https://rkn2.github.io/ncpttFloodApp/dashboard.html and paste the CSV URL
- [ ] **Get PR SHPO/ICP review of Spanish translation** — `content-bundle.es.json` is marked `entailment_audited: false`. Spanish guidance text needs SHPO sign-off before reporting as authoritative
- [ ] **Native-speaker/SHPO review of changed Spanish strings (2026-10-02)**: `floodapp.html` I18N.es `results_district`, `results_local`, `results_eligible` (new Section 106 messages, replacing `results_unlisted`); `content-bundle.es.json` siding `do` item on removing flooded insulation (closed-cell board exception) and insulation `do` item on fiberglass batts (now remove-by-default); mold carpeting item moved from `dont` to `do` (text unchanged)
- [ ] **Native-speaker/SHPO review of new Spanish file `pa-guidance.es.json` (2026-10-02, nonprofit/public-owner Public Assistance path)**: `panel_title`, `panel_intro`, `label_do`/`label_dont`/`label_source`/`label_page`, the three `sources` names, all 10 record `label`/`summary` strings, all 44 `do`/`dont` item texts, and `notes.age45_pa` / `notes.age45_private`. Quotes stay in English (verified verbatim). Both files are `entailment_audited: false`
- [ ] **Review `pa-guidance.json` item wording against its quotes (entailment)** — `python3 pipeline/verify_pa_guidance.py pa-guidance.json --es pa-guidance.es.json` checks all 75 quotes are verbatim and on the cited printed page, but nobody has yet checked that each plain-language item says only what its quotes support
- [ ] **Native-speaker/SHPO review of new Spanish strings (2026-10-17)**: `floodapp.html` I18N.es `install_android`, `install_ios`, `install_btn`, `install_dismiss`, `cite_show`, `print_assessed`, and the reworded `guidance_sources` ("toque 📄 para ver la cita exacta"); the Spanish half of `deploy/flyer.html`
- [ ] **Native-speaker/SHPO review of new Spanish UI strings (2026-10-02, PA path)**: `floodapp.html` I18N.es `owner_legend`, `owner_hint`, `owner_private`, `owner_nonprofit`, `owner_government` (new "Who owns this building?" question), `results_pa`, `results_pa_assist_note`, `pa_unavailable`, `as_pa_intro`
- [ ] **Native-speaker/SHPO review of new/changed Spanish UI strings (2026-10-02, building age and Section 106)**: `floodapp.html` I18N.es `age_legend`, `age_hint`, `age_old`, `age_new`, `age_unsure`, `age45_lead_yes`, `age45_lead_maybe` (new), and `results_listed` (reworded to "exige revisar cómo les afectan los trabajos" wording)
- [ ] **Decide on the private-owner 45-year note** — for private homeowners the app now says FEMA's *Public Assistance* rules send work on 45+-year-old buildings to more detailed historic review (PAPPG p.237) and that household grants are also covered by historic preservation law (IAPPG p.14). The IAPPG has no 45-year rule, so the note doesn't claim household-grant repairs will get that review. Keep, soften or drop for homeowners
- [ ] **Confirm the National Heritage Responders contact is current** — `pa-guidance.json` `help` gives institutions (202) 661-8068 and individuals NHRpublichelpline@culturalheritage.org, plus the HENTF email culturalrescue@si.edu, cited to the 2023 Texas Historical Commission handbook p.19 (the PAPPG doesn't list it)
- [ ] **Native-speaker/SHPO review of new Spanish strings (2026-10-02, homeowner aid)**: `programs.json` national `desc_es`/`note_es` for FEMA IA (historic-home note, safe/sanitary/functional framing, $44,800 cap), SBA (loan limits; apply even if you don't want a loan) and NPS/SHPO (Section 106 listed-or-eligible wording); `content-bundle.es.json` structural `do` item on FEMA basement repair limits; new `recovery_aid` record (label "Seguro, FEMA y SBA", summary, 7 `do` and 3 `dont` items on flood insurance, claims, documenting damage, the SFHA flood insurance requirement and SBA)
- [ ] **Decide on the IHP cap in `programs.json`** — FEMA IA desc says $44,800 for disasters declared on or after 2025-10-01 (Federal Register 2026-19854). A notice for disasters declared from 2026-10-01 could appear any time; update or drop the figure then
- [ ] **Frame CV decision in next progress report** — Decided against with evidence (see `overnight/v3-cv-build/DECISION.md`). Explain as a reasoned scope decision, not a silent omission
- [ ] **Design evaluation plan** — What should the PR PhD fieldwork measure? What feedback to capture? Once decided, telemetry can be wired into the app

## Code TODO (ask Claude)

- [x] **Install prompt + QR code.** (Done 2026-10-17; still ask field testers about a store version.) Decided 2026-10-16 to stay a web app (PWA), not an app-store app, at least through field testing. Add an "Install this app" banner with iPhone steps (Share → Add to Home Screen) and Android install, plus a printable QR code for SHPO flyers. Ask field testers whether they'd want a store version

- [ ] **Header attribution (wait for Simeon's answer).** The header reads "National Park Service • Preservation Assistance", which presents the tool as an NPS product. Default fix: "Developed by Penn State with support from the National Park Service's National Center for Preservation Technology and Training". Change the EN and ES strings in `floodapp.html` and `deploy/index.html`, using whatever wording/logo/disclaimer NCPTT prefers (asked 2026-10-16)
- [x] **Source labels on repair cards.** (Done 2026-10-17.) The footer of each guidance card builds titles from file names ("Nthp Treatment Flood Damaged Historic Buildings; Fema Iappg V1.1 Amended 2025"). Map each `docs/` source to its proper title (e.g. National Trust, *Treatment of Flood-Damaged Older and Historic Buildings*; FEMA *Individual Assistance Program and Policy Guide* v1.1). The flaw shows in the Oct 2026 PPR Figure 2a. Do it in the next website update

- [x] Fix 8 moderate/minor WCAG items (2026-10-17) (touch targets, fieldset/legend, autocomplete attrs, citation accessibility)
- [ ] Add evaluation telemetry (after Becca decides what to capture)
- [ ] Add more states/territories to `programs.json`
- [x] Render the `recovery_aid` bundle record (2026-10-02: insurance panel + "Common mistakes to avoid"); service worker cache bumped to v11
- [x] `results_listed` (EN/ES) aligned with the Section 106 "review of effects" wording (2026-10-02)
- [x] (Reworded 2026-10-17; the re-audit itself is the entailment-review decisions above.) EN bundle `provenance_note` says every item passed the entailment audit; no longer true for hand-edited items (`entailment_audited: false`). Re-run the audit or reword the note

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
