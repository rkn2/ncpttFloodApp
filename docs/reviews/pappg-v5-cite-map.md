# PAPPG v4 to v5 cite map, plus IAPPG check (2026-10-02)

Maps every claim in `2026-10-02-pappg-v4-review.md` (Headline, Aligns, Conflicts and Gaps sections) from PAPPG v4 (June 2020) to PAPPG v5.0 Amended. Every row was checked against the extracted text (`pdftotext -layout`, with tables re-extracted without `-layout`). None of it comes from memory. **Later agents writing app content may cite only the v5 and IAPPG locations in this file.**

## Sources (pin cites to these exact files)

| Doc | File in repo | Source URL | Retrieved | Notes |
|---|---|---|---|---|
| PAPPG v5.0 **Amended** (FP 104-009-2) | `docs/fema-pappg-v5.0-amended-2025.pdf` (4.2 MB, 329 pp, SHA-256 `0d3999c4…5606`) | https://www.fema.gov/sites/default/files/documents/fema_pa_pappg-5.0-amended.pdf (FEMA returned 403 to curl, so the copy came from Wayback snapshot `20260611042933`) | 2026-10-02 | Cover: "Version 5.0 Amended, Effective January 6, 2025". Foreword: "applies to incidents declared on or after January 6, 2025 and supersedes Version 4". The amendment covers Executive Orders issued on and after 2025-01-20 and changed Ch. 4, 6, 8, 10 and App. A, B, C, D, G. PDF metadata says Aug 2025; the FEMA PA library lists it as Aug 8, 2025. **The un-amended Jan 2025 v5.0 (`fema_pa_pappg-v5.0_012025.pdf`, also mirrored on state sites) has different text in those chapters. Don't cite it.** |
| IAPPG v1.1 **Amended** (FP 104-009-03) | `docs/fema-iappg-v1.1-amended-2025.pdf` (7.9 MB, 283 pp, SHA-256 `bd2f2eb0…702e`) | https://www.fema.gov/sites/default/files/documents/fema_iappg-1.1_amended_july2025.pdf (via Wayback snapshot `20250804165300`) | 2026-10-02 | The FEMA IA library page (fetched 2026-10-02) says this version "supersedes the IAPPG Version 1.1 dated May 2021". The amendment covers Executive Orders on and after 2025-01-20 and changed Ch. 1, 2, 5, 8 and App. G. |
| PAPPG v4 (comparison only, not committed) | none | https://www.fema.gov/sites/default/files/documents/fema_pappg-v4-updated-links_policy_6-1-2020.pdf (via Wayback) | 2026-10-02 | Used to confirm what v4 actually said |

**Newer-version check (2026-10-02).**
- **PAPPG:** the FEMA PA policy library lists v5.0 Amended as current, and no v5.1 is listed. Industry sources (ICF) say a v5.1 is planned. A Wayback CDX listing of `fema.gov/sites/default/files/documents/*pappg*` shows nothing newer.
- **IAPPG:** the FEMA IA library page shows v1.1 Amended (July 2025) as current, with no v2.

**Page numbers.**
- All v5 pages below are **printed** page numbers (footer). In this file, printed page = PDF page − 4.
- IAPPG pages are also **printed**. The offset varies, so there is no fixed formula: for example p.86 = PDF 98 and p.266 = PDF 263.
- v4 pages are printed (v4 printed = PDF − 1).

**Status definitions.**
- **unchanged**: same substance, same page.
- **renumbered**: same substance, new page or section.
- **changed**: substance differs, even in part.
- **dropped**: no v5 equivalent.
- **not found**: couldn't locate.
- **new in v5**: no v4 counterpart in the review, listed because it matters.
- **n/a**: the review row has no PAPPG cite.

## Counts (45 rows in the Headline, Aligns, Conflicts and Gaps tables)

| Status | Count | Rows |
|---|---|---|
| unchanged (same page) | 0 | none |
| renumbered (substance unchanged) | 34 | all rows not listed below |
| changed | 9 | A2a, A5, A6a, G1a, G1b, G2a, G2c, G4b, G6b |
| dropped | 0 | none. One v4 *sentence* is gone ("jeopardizes PA funding", see A5/G1a); the requirement itself survives |
| not found | 0 | none |
| n/a | 2 | C3 (app bug), C4 (IAPPG, handled below) |
| new in v5 | C1d + N1-N9 | C1d is the same item as N2 |

The review's compound bullets are split into one row per cite. A single review bullet can therefore produce several rows.

## Headline

| # | Claim | v4 page | v5 section / printed page | Status | v5 quote (≤30 words) | Notes |
|---|---|---|---|---|---|---|
| H1 | PA covers PNPs: houses of worship, museums, libraries, community centers | 43-46 | Ch.3 III-V, pp.45, 55-56 (Table 4) | renumbered | "Private nonprofit (PNP) organizations, including houses of worship and other faith-based organizations." (p.45) Table 4 lists "Houses of worship and faith-based organizations… Libraries; Museums" (p.56) | v5 makes the HOW = PNP point explicit (Summary of Changes p.22). Community centers are in Table 4, p.55 |
| H2 | Governments owning historic buildings are PA applicants (public facility) | 56 | Ch.4 I.A, p.60 | renumbered | "Public buildings, structure, or system, including those used for educational, recreational, or cultural purposes" (p.60) | |

## Where the app aligns

| # | Claim | v4 page | v5 section / printed page | Status | v5 quote (≤30 words) | Notes |
|---|---|---|---|---|---|---|
| A1a | Damage from failure to protect in a reasonable time is ineligible | 52 | Ch.4 II.B.1, p.63 | renumbered | "Impacts or damage due to failure to take measures to protect a facility from further damage in a timely manner" (p.63) | Listed as "not caused by the declared incident" |
| A1b | Same, for mold | 137 | Ch.7 XIII.W.3, p.163 | renumbered | "mold must not be a result of poor facility maintenance or failure to take protective measures to prevent the spread of mold in a reasonable time after the incident." (p.163) | Extenuating circumstances (power out, facility underwater, etc.) are kept on p.163 |
| A1c | Same, for buildings | 172 | Ch.8 V.C.1, p.196 | renumbered | "Whether the applicant took prudent actions to prevent additional damage." (p.196) | |
| A2a | Documentation requirements (photograph before repairs) | 63 | Ch.4 II.B.1.i Table 7, p.64 | **changed** | Small projects: "Applicants must certify, in lieu of providing documentation"; large: "If necessary… Pre-incident photographs and/or video of the impacted site or facility" (p.64) | v5 cut documentation for small projects (Summary p.22). Photos are still good practice and still feed EHP review (A2b) |
| A2b | EHP review wants photos | 143 | Ch.10 I.A.1, p.236; I.D, p.240 | renumbered | "Maps or photographs to support the SOW" (p.236); "Provide maps or sketches of work details, photographs, site plans, and area descriptions of pre-disaster conditions" (p.240) | |
| A3a | Eligible mold work (PPE, containment, HVAC cleaning) | 136 | Ch.7 XIII.W.3, p.163 | renumbered | "Cleaning of contaminated heating and ventilation (including ductwork), plumbing, and air conditioning systems or other mechanical equipment." (p.163) | v4 said these "may be eligible"; v5 says they "are eligible" |
| A3b | EPA mold methods appendix | App. I p.240 | **App. H** p.297 | renumbered | "Seal contents in two bags using 6-mil polyethylene sheeting" and "Sealing of materials must be within containment area to limit further contamination." (p.297) | The appendix letter changed from I to H. Still "Summarized from… EPA" (fn 514) |
| A4 | 50% rule doesn't apply to components; a repairable component gets repair only | 159 | Ch.8 VI.D, p.211 | renumbered | "FEMA does not apply the 50 percent rule to a facility's structural or mechanical components (e.g., windows; roofs; heating, ventilation, and air conditioning (HVAC); electrical; plumbing)." (p.211) | Repair-only: "If the HVAC system is repairable… FEMA limits its funding to the repair of the system." (p.211) |
| A5 | Allow EHP review before work | 141-142 | Ch.8 VIII, p.214; Ch.10, pp.234-240 | **changed** | "Applicants need to make every effort to afford FEMA the opportunity to perform environmental and historic preservation (EHP) reviews prior to starting any work" (p.214) | v4 p.141 said early work "jeopardizes PA funding for the entire project", and v4 p.142 said it "jeopardizes PA funding for that project". **v5 has no EHP-specific "jeopardizes" sentence.** The consequence now sits in general text: p.62 "FEMA may take one of several actions including disallowing all or part of the cost of the project not in compliance" and p.41 "Non-compliance… could jeopardize an applicant's PA funding". **App copy must not quote the v4 wording.** |
| A6a | Section 406 hazard mitigation | 155 | Ch.8 III, pp.178-179 | **changed** | "FEMA evaluates proposed measures to determine feasibility and the capability of the mitigation measure to protect against disaster damages, regardless of hazard type." (p.179) | v5 allows mitigation against all hazards, not only the one that caused the damage, and against hazards beyond code (p.178; Summary p.21). It also adds mitigation on replacement projects (p.210) |
| A6b | Elevate utilities (App. J measures) | App. J p.242 (measure on p.244) | App. J III.C, p.314; VIII.B, p.315 | renumbered | "Elevate or dry floodproof components or systems vulnerable to flood damage" (p.314); "Elevate, wet floodproof, or dry floodproof buildings." (p.315) | v5 App. J is expanded (Summary p.21) |

## Conflicts / bugs

| # | Claim | v4 page | v5 section / printed page | Status | v5 quote (≤30 words) | Notes |
|---|---|---|---|---|---|---|
| C1a | Section 106 covers listed **or eligible** properties | App. A p.221 | **App. D** II, p.275 | renumbered | "Historic properties include buildings, structures, sites, including archaeological resources, objects, and districts included in, or eligible for inclusion in, the National Register of Historic Places." (p.275) | The EHP appendix moved from A to D |
| C1b | Same (historic preservation compliance) | 149 | Ch.8 III.C.1, p.182 | renumbered | "If the facility is listed in, or meets the criteria to be listed in, the National Register of Historic Places" (p.182) | |
| C1c | Same (repair vs. replacement) | 159 | Ch.8 VI.C, p.211 | renumbered | "A historic facility is defined as one listed in, or eligible for listing in, the National Register of Historic Places." (p.211) | |
| C1d | (new trigger to add to the app) | none | Ch.10 I.B-C, pp.236-237 | new in v5 | "Work affecting buildings, structures, sites, objects, or districts that are 45 years or older, historic landmarks of any age" (p.237) | Streamlined review is limited to buildings "less than 45 years old and that are not listed or eligible for listing" (p.236). v4 used 45 years only for scope changes to Alternative Procedures projects (v4 p.195, kept in v5 App. G p.294). **Recommended app trigger for the Section 106/EHP message: 45+ years old, OR NR listed, OR NR eligible, OR a local landmark.** |
| C2 | Wet fiberglass insulation: discard | App. I p.241 (and p.136) | **App. H** Table 38, p.298 (and p.163) | renumbered | "Fiberglass Insulation: Discard and replace. (Replacement is only eligible as permanent work.)" (p.298) | Still advisory. p.163 says App. H "provides information for consideration when developing a SOW"; footnote 515 cites EPA. v5 adds for wallboard: "(May include removal of wallboard up to 12-16 inches above the waterline.)" (p.298) |
| C3 | Carpet line in the mold `dont` list | none | none | n/a | none | App bug, no PAPPG cite |
| C4 | `programs.json:9`, `:20` can't be checked against PAPPG | none | IAPPG, see below | n/a | none | Checked against the IAPPG in the section below |

## Gaps

| # | Claim | v4 page | v5 section / printed page | Status | v5 quote (≤30 words) | Notes |
|---|---|---|---|---|---|---|
| G1a | No permanent work, demolition or removal of historic fabric before EHP/Section 106 review | 141-142 | Ch.8 VIII, p.214; Ch.10 E.2, p.242 | **changed** | "This includes, but is not limited to, demolition work, site preparation, and ground disturbing activities." (p.214) | Same change as A5: the "jeopardizes" sentence is gone. Section 106 consultation with SHPO/THPO is on p.242. v5 lists "Modifying to the interior or exterior of a historic building" as a permanent-work example with potential EHP impacts (p.239) |
| G1b | Emergency work must avoid historic impacts | 110 | Ch.10 I.C.3, p.238 | **changed** | "FEMA must ensure that the applicant's emergency protective measures, where possible: 1) avoid impacts to resources such as… historic properties" (p.238) | v4 had a flat "must ensure… avoid", and v5 adds "where possible". Debris removal (p.238) keeps the stronger "must ensure that the applicant's debris removal operations avoid impacts to… historic properties". v5 p.238 also encourages coordinating before emergency work and says after-the-fact EHP documentation is still needed |
| G1c | Muck-out counts as emergency work only if done promptly for an immediate threat | 111 | Ch.7 XIII.B, p.132 | renumbered | "Extracting water and clearing mud, silt, or other accumulated debris from eligible facilities if the work is conducted expeditiously for the purpose of addressing an immediate threat" (p.132) | fn 275: work needed only to restore the facility is permanent work |
| G2a | Document pre-disaster condition (photos, maintenance records) | 52 | Ch.4 II.B.1.i, p.64 | **changed** | "the applicant is not required to furnish pre-incident images, records of maintenance, or reports on inspections and safety measures." (p.64) | That applies when the damage is evident. Large projects may still need "Pre-incident photographs and/or video" (Table 7, p.64). Summary p.22: "maintenance records are not always required." The kept sentence "pre-disaster condition was not a significant contributing factor" is on p.64. **Keep the advice to document; drop any claim that FEMA requires it.** |
| G2b | Buildings: FEMA weighs maintenance and pre-disaster condition | 172 | Ch.8 V.C.1, pp.195-196 | renumbered | "Evidence of pre-disaster condition, such as interior water stains from a leaky roof" (p.196) | |
| G2c | Mold: FEMA screens for pre-existing leaks, gutters, ceilings | 137 | Ch.7 XIII.W.3, p.164 | **changed** | "Poorly maintained drains or gutters with rust or vegetative growth; and, Leaking and or water-stained ceiling tiles." (p.164) | v5 drops v4's "Absence of rain gutters". It adds "pre-existing damage or deferred maintenance" and "water-stained" tiles |
| G3a | Houses of worship and museums must apply for an SBA loan (noncritical PNPs) | 57-58 | Ch.3 V.J, pp.51-52 (Table 2) | renumbered | "PNPs that do not provide any critical services must also apply for a disaster loan from the SBA and receive a determination for permanent work" (p.51) | The rule covers **permanent work only**. Table 2 (p.52): emergency work needs no SBA application. v5 does not say "first"; it says "Applying to both agencies as soon as possible ensures meeting both application deadlines" (p.52) |
| G3b | Missing the SBA deadline makes permanent work ineligible | 58 | Ch.3 V.J.1, p.52 | renumbered | "If the PNP misses the SBA application deadline, including any SBA approved extension, permanent work is ineligible for PA funding." (p.52) | Declining the loan, or being unable to meet its terms, limits PA to costs the loan would not have covered (p.52) |
| G3c | Worked example: a chapel must apply to SBA | App. B p.229 | **App. E** VII, p.285 | renumbered | "Houses of worship provide noncritical services, so Community Church is required to apply for an SBA loan for the chapel." (p.285) | The PNP examples appendix moved from B to E |
| G4a | Uninsured building in an SFHA: PA cut by the maximum NFIP payout | 162 | Ch.8 IX.C.1, p.219 | renumbered | "FEMA reduces eligible project costs by the lesser of: The maximum amount of insurance proceeds that could have been obtained from an NFIP standard flood insurance policy" (p.219) | The cut applies only when the area has been mapped SFHA for over a year, the building was flood-damaged, and it was uninsured (p.219). The alternative cap is the value of the building and contents. PNPs in communities outside the NFIP: the community must join within 6 months (p.220) |
| G4b | Obtain-and-maintain insurance requirement | 144-145 | Ch.8 X, pp.220-221 | **changed** | "Applicants that receive PA funding for permanent work to replace, repair, reconstruct, or construct a facility must obtain and maintain insurance to protect the facility against future loss." (p.220) | Core rule unchanged. Differences: (1) the modification basis is narrower. v4 listed three alternative grounds; v5 requires "not reasonably available; and, … not necessary" (p.220) and drops "an alternative… provides adequate protection". (2) v4 p.145 §A on subsequent-disaster reductions is not repeated; v5 points to FP 206-086-1. (3) It adds a letter of commitment (LOC) for facilities not yet insurable (p.221). (4) The waiver at ≤$5,000 is kept |
| G5a | RPA deadline 30 days | 36 | Ch.3 III, p.45 | renumbered | "it must submit an RPA to FEMA via PA Grants Portal within 30 days after the respective area is designated." (p.45) | **No change found** in substance. Extension grounds are on p.46 |
| G5b | Damage list due 60 days after the scoping meeting | 60 | Ch.5 I.A, p.70 | renumbered | "Applicants are required to identify and report all incident-related impacts and damage to FEMA within 60 days of attending a recovery scoping meeting." (p.70) | **No change found** in the deadline. The term is now "Impact List" (p.70) |
| G5c | Replacement request within 1 year | 158 | Ch.8 VI.B, p.209 | renumbered | "Applicants should submit their requests for replacement within one year of the declaration." (p.209) | **No change found** |
| G5d | Emergency work 6 months, permanent 18 months | 196 | Ch.11 II, pp.247-248; also p.116 | renumbered | "For emergency work, the deadline is six months from the disaster declaration date. For most permanent work, the deadline is 18 months" (p.247) | **No change found.** Recipients can still extend by 6 months (emergency) and 30 months (permanent) (p.248). The only new deadline is Category I at 180 days (p.247), which doesn't apply to owners |
| G6a | Collections: stabilization eligible, replacement not | 175-176 | Ch.8 V.C.2.iii, pp.197-198 | renumbered | "Stabilization of damaged collections or individual objects is eligible." (p.197); "Replacement of destroyed irreplaceable collections or objects is ineligible." (p.198) | Special library collections: "only eligible for treatment, not replacement" (p.197) |
| G6b | Qualified conservator, AIC Code, accession records | 175-176 | Ch.8 V.C.2.iii, pp.197-198 | **changed** (minor) | "Treatment needs to be conducted by a qualified conservation professional with the appropriate specialty and in accordance with the American Institute for Conservation Code of Ethics and Guidelines for Practice." (p.198) | Accession, catalog and inventories are on p.197. v4's "submit all associated documentation along with a clear title" is **not carried over**. New on p.196: "Contents damaged as a result of the disaster are eligible even if the building housing the contents is not damaged" |
| G6c | Moving contents counts as emergency work | 111 | Ch.7 XIII.B, p.132 | renumbered | "Removal and storage of contents from eligible facilities for the purpose of minimizing additional damage" (p.132) | |
| G6d | Do NOT adopt "photocopy and discard valuable papers" | App. I p.240 | **App. H** Table 38, p.298 | renumbered | "Valuable/important: photocopy and discard originals" (p.298) | Still in v5, still an EPA summary. Keep the review's advice: don't put it in the app for historic papers. See also files recovery on pp.196-197 (freeze-drying is eligible) |
| G7a | Historic exception to the 50% rule (listed/eligible) | 149 | Ch.8 III.C.1, p.182 | renumbered | "costs associated with work to comply with that code or standard are eligible, even if repair costs exceed replacement costs." (p.182) | Applies only if a code or standard "requires repair in a certain manner" |
| G7b | Same | 159 | Ch.8 VI.C, p.211 | renumbered | "the cost to restore the facility in accordance with the code or standard is eligible and may exceed the estimated replacement cost." (p.211) | p.211 says "As discussed in Chapter 10", but Ch.10 doesn't actually discuss it. Cite p.182/211 |
| G7c | Most state historic building codes don't qualify | 149 | Ch.8 III.C.2, p.182 | renumbered | "Most state historic building codes and standards encourage code officials to allow less intrusive alternatives… As a result, the codes and standards usually fail to meet the eligibility criteria." (p.182) | |
| G8a | Vacant/inactive buildings ineligible | 58 | Ch.4 I.B, p.61 | renumbered | "To be eligible, a facility must have been in active use at the start of the incident period." (p.61) | The three exceptions (temporary repairs, budgeted future use, demonstrated intent) are kept |
| G8b | Museum grounds ineligible | 46 | Ch.3 V.K Table 5, p.57 | renumbered | "Grounds at museums and historic sites" (Table 5, PNP Ineligible Services, p.57) | Moved from a footnote-style note to the ineligible-services table |
| G8c | Mold sampling by an independent professional | 136-137 | Ch.7 XIII.W.3, p.163 | renumbered | "The indoor environmental professional should not be employed by the remediation company to avoid a conflict of interest." (p.163) | |
| G8d | Mixed use needs >50% eligible use | 56 | Ch.3 V.E, p.50; Ch.4 I.B, p.61 | renumbered | "Primary use is the use for which more than 50 percent of the physical space in the facility is dedicated." (p.50) | Active-use rule: "more than 50 percent of the facility had to be in active use for an eligible purpose" (p.61) |

## v5 changes that matter for historic buildings (new-in-v5 rows)

| # | Topic | v5 printed page | Status | v5 quote (≤30 words) | Why it matters |
|---|---|---|---|---|---|
| N1 | Heritage Emergency National Task Force section | 245 | new in v5 | "HENTF can serve as a technical assistance resource for field staff… advising on conservators and allied professionals, and evaluating scopes of work for treatment of objects." | v4 never mentions HENTF (0 hits). It is a citable referral for cultural PNPs, and DRI liaises with HENTF |
| N2 | 45-year / landmark trigger for complex EHP review | 236-237 | new in v5 | See C1d | This is the basis for widening the app's Section 106 trigger |
| N3 | Historic building alterations named as EHP-impact work | 239 | new in v5 | "Modifying to the interior or exterior of a historic building" | Supports gap G1 |
| N4 | Waiver from FEMA consensus-based codes for historic facilities | 169 | new in v5 | "It would otherwise be inappropriate for the facility (such as adversely affecting a facility that is listed or is eligible to be listed on the National Register of Historic Places)." | v4 only pointed to the separate interim policy. The waiver requires Regional Administrator approval |
| N5 | Floodplain-ordinance upgrades: historic exception to the replacement-cost cap | 217 | new in v5 | "There is an exception for facilities eligible for or on the National Register of Historic Places." | v4 p.151 had the replacement-cost cap with no historic exception |
| N6 | SBA loan terms for PNPs | 52 | new in v5 | "SBA disaster loans are available up to $2 million to qualified businesses and most private nonprofit organizations." | v4 has no "2 million" hit. Mitigation can add up to 20% of the loan (p.52) |
| N7 | Contents eligible even if the building is undamaged | 196 | new in v5 | "Contents damaged as a result of the disaster are eligible even if the building housing the contents is not damaged" | Museums and archives with basement flooding |
| N8 | Houses of worship explicitly PNPs | 22, 45 | changed (clarified) | "Clarified that Houses of Worship and faith-based organizations are considered private nonprofit organizations." (p.22) | Supports the PA path for churches |
| N9 | NEPA regulations removed (amendment) | 275 | new in v5 Amended | "Effective April 11, 2025, interim final rule removed the implementation of NEPA regulations." | NEPA changed; **Section 106/NHPA did not** (p.275). Don't tell owners EHP review went away |

Also unchanged and still useful:
- ADA exceptions for historic buildings (p.176; v4 p.152).
- Category I training "on unique considerations for repair of disaster-damaged historic buildings" (p.223).
- The deadlines, which did **not** change in v5 (see G5a-d). The brief expected changes to RPA, damage reporting and work completion; none were found.

## IAPPG claims (`programs.json`)

Source: IAPPG v1.1 Amended (July 2025), printed pages.

### `programs.json:9` (FEMA IA note)

> "Historic property owners: notify FEMA that your building is historically significant. FEMA must consider historic character in repair requirements."

**Verdict: not supported. Rewrite it.**

| Point | IAPPG location | Quote (≤30 words) |
|---|---|---|
| IHP Home Repair Assistance is for basic habitability, not restoration | Ch.3 IV.E, p.86 | "Home Repair Assistance is intended to make the damaged home safe, sanitary, or functional. It is not intended to return the home to its pre-disaster condition." |
| Awards are priced at average quality | Ch.3 IV.E.2, p.89 | "Home Repair Assistance award amounts are based on repair or replacement of components that are of average quality, size, or capacity." |
| No upgrades beyond pre-disaster condition, except for code, unavailable products or mitigation | p.89 | "will not be provided to make improvements to a component's pre-disaster condition unless required by current SLTT government building codes or ordinances" |
| Section 106 is FEMA's duty for a federally funded "project", not a repair standard placed on the owner | Ch.1 D, p.14; App. G, p.266 | "Section 106 of the National Historic Preservation Act requires FEMA to consider the effects a project will have on historic properties" (p.266) |
| Where EHP review explicitly applies in IHP | p.91 (private access routes), p.95 (direct housing), p.118 (TTHU sites) | "Eligible activities for the repair of privately-owned access routes are subject to Federal Environmental Planning and Historic Preservation (EHP) compliance review requirements." (p.91) |

A search of the whole IAPPG text for "historic" found no provision telling owners to notify FEMA of historic significance. It also found nothing requiring FEMA to factor historic character into IHP repair amounts or methods. Every hit is the generic EHP/Section 106 description (pp.14, 266) or a FEMA-built or FEMA-funded site (pp.91, 95, 118-119).

**Suggested replacement (verified wording):**
- FEMA home repair grants cover only making the home "safe, sanitary, or functional" at "average quality".
- They will not pay for historic-quality materials.
- Talk to your SHPO before repairs.
- If you use other federal money (SBA, HUD, FEMA mitigation), that agency's Section 106 review may apply.

The "other federal money" point is an inference for Becca to confirm. The IAPPG doesn't say it.

### `programs.json:20` (SBA note)

> "SBA loan approval is often required before FEMA can provide certain types of additional assistance."

**Verdict: inaccurate (reversed). Rewrite it.**

| Point | IAPPG location | Quote (≤30 words) |
|---|---|---|
| SBA-dependent help follows an SBA *denial or shortfall*, not approval | Ch.3 I.C.2, p.46 | "Only applicants who do not qualify for a loan from the SBA may be eligible for assistance for the SBA-dependent category." |
| Which types are SBA-dependent | p.46; Fig. 28, p.146 | "SBA-dependent ONA includes Personal Property Assistance, Transportation Assistance, and Group Flood Insurance Policy (GFIP)." (p.46) |
| You must *apply* to SBA first | Fig. 28, p.146 | "The applicant must first apply to the SBA for a loan for these expenses or serious needs." |
| Declining or withdrawing ends the path | Ch.3 VI.C, p.166 | "Applicants who withdraw from the process or decline a loan from the SBA will not be referred back to FEMA for assistance with SBA-Dependent ONA." |
| Referral depends on income | p.145 | "FEMA refers the applicant's information to SBA if the applicant's income meets SBA minimum guidelines." |
| Home Repair Assistance is **not** SBA-dependent | p.44 (Housing Assistance) vs p.46 (ONA list) | Home Repair is Housing Assistance; the SBA-dependent list is ONA only |

**Suggested replacement:** "If FEMA refers you to SBA, complete the SBA application. FEMA can only help with personal property, vehicles and group flood insurance if SBA turns you down or lends too little. If you decline or withdraw, you lose that help. FEMA home repair grants don't depend on SBA."

**`programs.json:18` ($500,000):**
- The IAPPG doesn't state SBA loan limits.
- sba.gov (physical-damage-loans page, fetched 2026-10-02): "Homeowners may apply for up to $500,000 to replace or repair their primary residence." and "up to $100,000 to replace or repair personal property".
- Mitigation: "up to a 20% loan amount increase above the real estate damage".
- **Line 18 is accurate. Cite sba.gov, not the IAPPG.**

### IAPPG facts for historic homeowners (citable)

| Topic | IAPPG location | Quote / fact |
|---|---|---|
| IHP housing maximum | p.42-43 | The cap is set annually by notice: "FEMA adjusts these maximum awards each fiscal year based on the Department of Labor Consumer Price Index." (p.42). Separate, equal caps for Housing Assistance and ONA. Current figure: **$44,800 housing / $44,800 ONA** for disasters declared on or after 2025-10-01 (Federal Register 2026-19854, 91 FR 61429, published 2026-09-29). This figure is not in the IAPPG. |
| What home repair covers | p.87 | Structural components (foundation, exterior walls, roof); windows, doors, floors, walls, ceilings, cabinetry; HVAC; utilities; private access. Not covered: garage, pool, fences, landscaping (Fig. 21, p.87) |
| Conditions | p.88 | Component was "functional immediately before the declared disaster", the disaster caused the damage, and it "is not covered by insurance". Maintenance need alone doesn't disqualify (sidebar p.88) |
| Must file insurance first | p.88 | "An applicant with insurance for a covered peril will be ineligible for Home Repair Assistance for insured real property components when the applicant fails to file a claim" |
| Basements (common in historic homes) | p.88-89 | Flood repair in basements is limited to structural, critical utilities (furnace, water heater), and rooms needed for occupancy. Wet or moldy materials in non-essential areas are paid "for removal only" (p.89) |
| Mitigation in home repair | p.87-88 | "Hazard mitigation may be awarded as part of Home Repair Assistance for real property components that existed, and were functional, prior to the disaster." (p.88) |
| Home replacement | p.92 | For destroyed homes, capped at the Housing Assistance maximum. "Destroyed" includes "Flood waters have reached the roof" |
| NFIP purchase requirement (SFHA) | Ch.3 II.B.11, p.64 | Owners in an SFHA who get Home Repair, Home Replacement, PHC or Personal Property help "must obtain and maintain flood insurance coverage for at least the amount of disaster assistance they receive". If they don't, they're ineligible for flood-damage IHP in future disasters (p.64) |
| The requirement runs with the property | Fig. 14, p.66 | "If the home is sold or otherwise becomes owned by someone else, the requirement to purchase and maintain flood insurance carries over to any subsequent owner." |
| 30 days to decline | p.67 | Applicants can decline (return) the assistance within 30 days to avoid the flood-insurance requirement |
| Sanctioned (non-NFIP) communities | p.65 | No IHP for flood-damaged NFIP-insurable items, unless the community joins NFIP within 6 months of the declaration |
| Clean and Removal Assistance | p.165-166 | Flood disasters only, state-requested. For flood contamination where the home is still habitable. $550 award mentioned (p.166) |
| SBA referral | p.145-146, 166 | See line 20 above |
| Period of assistance | p.42 | "IHP assistance is limited to 18 months following the date of the disaster declaration." |

## Next steps
- **Rebuild the knowledge base.** `knowledge-base.json` (gitignored) doesn't yet include `docs/fema-pappg-v5.0-amended-2025.pdf` or `docs/fema-iappg-v1.1-amended-2025.pdf`. Becca should rerun `build-kb.py`; it was deliberately not run here. If the extractor doesn't normalize ligatures (ﬂ/ﬁ) and private-use bullet glyphs, add that, or searches for "flood" will miss hits.
- The v4 review (`2026-10-02-pappg-v4-review.md`) should now cite this file. Its v4 page numbers are superseded for any shipped content.
