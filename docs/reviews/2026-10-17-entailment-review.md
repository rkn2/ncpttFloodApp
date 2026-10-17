# Entailment review: pa-guidance.json and hand-authored content-bundle items

**Date:** 2026-10-17
**Scope:**
- `pa-guidance.json`: all 10 `guidance` records (summary plus every `do`/`dont` item) and both `notes.*` entries. `help` is a guidance record id, so it is covered. 56 items in total.
- `content-bundle.json`: the 11 items carrying `"entailment_audited": false`.
- `deploy/pa-guidance.json` and `deploy/content-bundle.json` are byte-identical to the root copies (`cmp`), so every finding applies to them too.

**Method:**
- Quotes are already verified verbatim and on-page by `pipeline/verify_pa_guidance.py`, so this review does not re-check them.
- For each citation, I located the quote in the source PDF and read about 1,000 characters on each side of it. Tables were re-read with `pdftotext -layout` to confirm which column a quote sits in.
- Summaries carry no citations of their own. Each one is judged against the quotes cited in its own record.
- **The rule applied is the strict one: an item may say only what its cited quote(s) say.** When a claim is true in the surrounding source text but not in the quote, it is marked NOT-SUPPORTED and tagged *(context)*. Those are listed separately because the fix is to extend or add a quote, not to change the meaning.

**Verdicts:** SUPPORTED · OVERSTATED (claim stronger or broader than the quote) · MISSING-CONDITION (drops a condition the quote or its sentence carries) · NOT-SUPPORTED (part of the claim is in no cited quote) · JUDGMENT (a defensible paraphrase a reviewer might object to).

## Summary

| File | Items | SUPPORTED | OVERSTATED | MISSING-CONDITION | NOT-SUPPORTED (substantive) | NOT-SUPPORTED (context: extend quote) | JUDGMENT |
|---|---|---|---|---|---|---|---|
| pa-guidance.json | 56 | 29 | 1 | 8 | 5 | 7 | 6 |
| content-bundle.json (`entailment_audited: false`) | 11 | 9 | 1 | 0 | 0 | 0 | 1 |

**Most important fixes (the meaning a reader takes away is wrong or incomplete):**
1. **"Contact your SHPO" (4 items).** No cited quote supports telling a PA applicant, or a homeowner, to contact the SHPO. The PAPPG says FEMA consults the SHPO. Affected: `ehp_first.summary`, `ehp_first.do[0]`, `notes.age45_pa`, `notes.age45_private`.
2. **Extension deadlines.** "Good reason" replaces FEMA's much narrower "extenuating circumstances beyond [the] applicant's or recipient's control". Affected: `deadlines.do[0]`, `deadlines.do[1]`.
3. **Flood insurance.** Two conditions are dropped:
   - the PNP exception for communities that don't participate in the NFIP, plus "NFIP-insurable" (`flood_insurance.dont[0]`);
   - the $5,000 waiver of the obtain-and-maintain requirement (`flood_insurance.dont[1]`).
4. **Inactive buildings (`other_rules.dont[0]`).** One of the three exceptions is dropped ("intent to begin use within a reasonable amount of time"), so the rule reads stricter than FEMA's.
5. **Mixed-use buildings (`other_rules.do[1]`).** The text drops "must restore the entire facility to receive funding for repairs to the eligible use portions".
6. **Mold (`document.do[3]`).** The extenuating-circumstance exception requires the applicant to "document and justify" it. The text drops that.
7. **SBA (`sba.summary`, `sba.do[0]`).** "Community centers" and "most other nonprofits" are in no cited quote. The SBA rule also applies facility by facility (a nonprofit's critical-service buildings are exempt), which the text frames as a rule about the whole organization.
8. **Bundle `guidance[9]/do[5]`.** "Can't get FEMA help for flood damage in a future flood" is broader than the source: ineligible for *IHP assistance for flood-damaged real or personal property*.

**Spanish mirror.** Any rewording below needs a matching edit in `pa-guidance.es.json` (and `content-bundle.es.json`). Any added or changed citation must be copied there identically, because the mirror check requires identical citations per item.

---

## pa-guidance.json: substantive findings

### ehp_first.summary: NOT-SUPPORTED
- **Text:** "If you want FEMA to help pay, let FEMA and your State Historic Preservation Office (SHPO) review permanent repairs, demolition, or removal of historic material before the work starts."
- **Quotes (record):** PAPPG p214: "Applicants need to make every effort to afford FEMA the opportunity to perform environmental and historic preservation (EHP) reviews prior to starting any work that has the potential to impact the environment or historic properties." PAPPG p239: "Modifying to the interior or exterior of a historic building".
- **Problem:** The quotes give FEMA, not the applicant-plus-SHPO, the review role. The PAPPG describes FEMA consulting the SHPO (p242, Section 106), not the applicant going to the SHPO.
- **Suggested:** "If you want FEMA to help pay, give FEMA the chance to do its environmental and historic review before permanent repairs, demolition, or removal of historic material. FEMA consults your State Historic Preservation Office (SHPO) as part of that review." For the second sentence, add the citation PAPPG p242: "requires FEMA to assess if PA-eligible work will affect such properties and consult with the state historic preservation officer (SHPO)" (verifier: PASS). Don't start the quote at "Section 106 of the National Historic Preservation Act (NHPA)": footnote marker 443 sits in that span, and that version FAILS.

### ehp_first.do[0]: NOT-SUPPORTED
- **Text:** "Before permanent repairs, demolition, or removing historic material (plaster, trim, windows, floors), contact FEMA and your State Historic Preservation Office (SHPO). Give FEMA the chance to do its environmental and historic review first."
- **Quotes:** p214 "Applicants need to make every effort to afford FEMA the opportunity to perform … (EHP) reviews prior to starting any work …". p239 "Modifying to the interior or exterior of a historic building".
- **Problem:** "Contact … your SHPO" is in neither quote. The rest is supported.
- **Suggested:** "Before permanent repairs, demolition, or removing historic material (plaster, trim, windows, floors), contact FEMA and give it the chance to do its environmental and historic review first. FEMA brings in your State Historic Preservation Office (SHPO)." Add the p242 Section 106 citation, or drop the SHPO sentence.

### document.do[0]: NOT-SUPPORTED
- **Text:** "Before cleanup and repairs, photograph or video the whole building and the damage. For larger projects FEMA may ask for photos from before the flood, so gather any you have."
- **Quotes:** p64 Table 7, large-project column (confirmed with `-layout`): "If necessary to validate that the impacts or damage was caused by the declared event, applicants will be required to provide" plus "Pre-incident photographs and/or video of the impacted site or facility".
- **Problem:** The first sentence (document the *post-flood* damage before cleanup) is good practice, but both quotes concern *pre-incident* photos only. Sentence 2 is supported.
- **Suggested:** Keep sentence 2. Either drop sentence 1 or support it with a separate quote, for example PAPPG p240, which is already used in `document.do[2]`: "Provide maps or sketches of work details, photographs, site plans, and area descriptions of pre-disaster conditions and proposed or completed work". Reworded: "For larger projects, FEMA may ask for photos or video from before the flood to show the flood caused the damage, so gather any you have."

### document.do[3]: MISSING-CONDITION
- **Text:** "… FEMA won't pay to fix mold caused by not acting in a reasonable time, unless there was a good reason, like no power or the building was still underwater."
- **Quotes:** p163 "mold must not be a result of poor facility maintenance or failure to take protective measures to prevent the spread of mold in a reasonable time after the incident." p163 "Examples of extenuating circumstances include: Disruption of power; Facility is underwater;"
- **Problem:** The sentence between the two quotes makes the exception conditional: "If an applicant can **document and justify** why it did not take measures …, mold remediation is eligible." "Unless there was a good reason" drops the documentation burden.
- **Suggested:** "… unless you can document and justify why you couldn't act, for example no power or the building was still underwater. Write down the dates and the reason as they happen." To be strictly entailed, add the p163 citation "If an applicant can document and justify why it did not take measures to prevent further contamination" (verifier: PASS).

### sba.summary: OVERSTATED
- **Text:** "Houses of worship, museums, libraries, community centers, and most other nonprofits must apply for a Small Business Administration (SBA) disaster loan to get FEMA help with permanent repairs."
- **Quotes (record):** p51 "PNPs that do not provide any critical services must also apply …". p56 "Houses of worship …; Libraries; Museums;". p285 example (house of worship).
- **Problem:** "Community centers" is in no cited quote (it is in PAPPG Table 4, p55). "Most other nonprofits" is an unsupported quantity claim. The rule is "nonprofits that don't provide critical services".
- **Suggested:** "Houses of worship, museums, libraries, and other nonprofits that don't provide critical services must apply for a Small Business Administration (SBA) disaster loan before FEMA will help with permanent repairs." If community centers are wanted, cite p55 Table 4 ("Community centers or other facilities established and primarily used for similar services"; verify the exact string, since it is a table cell).

### sba.do[0]: MISSING-CONDITION
- **Text:** "If your nonprofit doesn't provide critical services (like a school or a hospital does), you must apply for an SBA disaster loan and get SBA's answer before FEMA will pay for permanent repairs. Houses of worship, museums, and libraries are in this group."
- **Quotes:** p51 "PNPs that do not provide any critical services must also apply for a disaster loan from the SBA" plus "and receive a determination for permanent work on facilities that". p56 list. p285 example.
- **Problem:** The second quote is cut at "on facilities that". The sentence continues on p52: "Provide noncritical services; or Are mixed-use facilities and the damaged portion … provides services that are entirely noncritical. PNPs do not need to apply for an SBA loan for any facilities that provide critical services." The rule therefore applies building by building (p285 evaluates a church's school buildings and chapel separately). The text frames it as a rule about the whole organization.
- **Suggested:** "For each building used for services that aren't critical (critical means things like education or medical care), your nonprofit must apply for an SBA disaster loan and get SBA's answer before FEMA will pay for permanent repairs. Houses of worship, museums, and libraries are in this group. Buildings that provide critical services don't need the SBA step." A quote can't span the page break, so add separate printed-p52 citations: "PNPs do not need to apply for an SBA loan for any facilities that provide critical services" and "Are mixed-use facilities and the damaged portion of the facility provides services that are entirely noncritical" (verifier: both PASS).

### flood_insurance.dont[0]: MISSING-CONDITION
- **Text:** "If the building has been in a mapped high-risk flood zone (Special Flood Hazard Area) for more than a year and had no flood insurance, FEMA cuts its funding. The cut is the most a standard flood insurance (NFIP) policy would have paid, or the value of the building and contents if that is less."
- **Quotes:** p219 "Located in an area that FEMA has identified as an SFHA for more than 1 year;". p219 "FEMA reduces eligible project costs by the lesser of: The maximum amount of insurance proceeds that could have been obtained from an NFIP standard flood insurance policy for the building and its contents".
- **Problems:**
  - The quoted list applies "for a National Flood Insurance Program (NFIP) insurable facility" and also requires "damaged by flooding". The text drops "NFIP-insurable".
  - p220 adds an exception that matters to nonprofit users: "FEMA does not apply this reduction to PNP facilities in communities that do not participate in the NFIP." (That exception has its own conditions: the community must agree to join within 6 months and the PNP must buy flood insurance.)
  - The clause "or the value of the building and contents if that is less" is only in the surrounding text, not the quote.
- **Suggested:** "If an insurable building has been in a mapped high-risk flood zone (Special Flood Hazard Area) for more than a year, was damaged by flooding, and had no flood insurance, FEMA reduces its funding by the most a standard NFIP policy would have paid (or by the value of the building and contents, if that is less). Nonprofits in communities that don't take part in the NFIP may be treated differently; ask FEMA." Don't extend the second quote across footnote marker 402. Add separate citations instead: p219 "or the value of the building and its contents at the time of the incident", and p220 "FEMA does not apply this reduction to PNP facilities in communities that do not participate in the NFIP" (verifier: both PASS).

### flood_insurance.dont[1]: MISSING-CONDITION
- **Text:** "If FEMA pays for permanent repairs, you must buy and keep insurance on the building. If you don't, FEMA can take back the money, and the building can't get FEMA Public Assistance in future disasters."
- **Quotes:** p220 "Applicants that receive PA funding for permanent work … must obtain and maintain insurance …". p221 "… FEMA will deny or deobligate PA funds … the facilities … are ineligible for future PA funding."
- **Problem:** Two lines below the p220 quote: "The requirements of Stafford Act section 311 are waived when eligible costs for an insurable facility do not exceed $5,000." The requirement also applies to insurable facilities only. The text states it unconditionally. (`flood_insurance.summary` carries the same simplification; it is counted under JUDGMENT below.)
- **Suggested:** "If FEMA pays more than $5,000 for permanent repairs to an insurable building, you must buy and keep insurance on it. If you don't, …". Add the p220 citation "The requirements of Stafford Act section 311 are waived when eligible costs for an insurable facility do not exceed $5,000." (verifier: PASS).

### deadlines.do[0]: MISSING-CONDITION
- **Text:** "Request for Public Assistance (RPA): due within 30 days after FEMA designates your area. FEMA can extend it if your state asks in writing and gives a good reason."
- **Quotes:** p45 "… within 30 days after the respective area is designated." p46 "FEMA extends the deadline for submitting an RPA if a recipient submits a request in writing with justification based on extenuating circumstances".
- **Problem:** "A good reason" is much looser than "extenuating circumstances". The quote's own sentence continues "beyond an applicant's or recipient's control", and FEMA's examples are narrow: FEMA delays, Grants Portal down on deadline day, communications down. Users could wrongly expect routine extensions.
- **Suggested:** "… FEMA can extend it only if your state asks in writing and shows extenuating circumstances beyond your or the state's control (for example, FEMA's portal was down on the deadline)." Add the p46 citation "beyond an applicant's or recipient's control" (verifier: PASS), or extend the existing quote through it.

### deadlines.do[1]: MISSING-CONDITION
- **Text:** "Impact List …: due within 60 days after you attend your recovery scoping meeting with FEMA. FEMA may extend it if you ask with a good reason."
- **Quote:** p70 "FEMA may extend the deadline to identify and report the impacts if an applicant submits a request with justification based on extenuating circumstances".
- **Problem:** The same softening. The quote requires "extenuating circumstances", and the sentence continues across the page break onto printed p71: "beyond the recipient's or applicant's control." FEMA's examples there are narrow: "For example, FEMA extends the deadline for an inaccessible site or when an applicant is in an area where FEMA approved additional categories of work after the recovery scoping meeting."
- **Suggested:** "FEMA may extend it if you ask and justify it with extenuating circumstances beyond your control (for example, the site was inaccessible)." A quote can't span the page break, so add a separate printed-p71 citation: "For example, FEMA extends the deadline for an inaccessible site or when an applicant is in an area where FEMA approved additional categories of work after the recovery scoping meeting." (Verifier: PASS.)

### other_rules.do[1]: MISSING-CONDITION
- **Text:** "Mixed-use buildings: more than half of the space has to be used for eligible services, like worship, a museum, or a library. FEMA then pays only for the eligible share."
- **Quotes:** p50 "Primary use is the use for which more than 50 percent of the physical space in the facility is dedicated." p50 "If the facility is eligible, FEMA prorates funding based on the percentage of physical space dedicated to eligible services."
- **Problems:**
  - Two sentences after the second quote: "The applicant is responsible for the balance of restoration costs and **must restore the entire facility** to receive funding for repairs to the eligible use portions." That condition is dropped.
  - Common space (halls, bathrooms, stairs) is excluded from the calculation.
  - The examples "worship, a museum, or a library" are not in these quotes (they are in p56).
- **Suggested:** "Mixed-use buildings: more than half of the space (not counting halls, bathrooms, and stairs) has to be used for eligible services. FEMA then pays only the eligible share, and you must restore the whole building, paying the rest yourself, to get it." Add the p50 citation "must restore the entire facility to receive funding for repairs to the eligible use portions of the facility" (verifier: PASS).

### other_rules.dont[0]: MISSING-CONDITION
- **Text:** "Vacant or unused buildings usually aren't eligible. The building must have been in active use when the disaster started, unless it was closed only for repairs, or you had approved plans or a budget to use it."
- **Quotes:** p61 "To be eligible, a facility must have been in active use at the start of the incident period." p61 "The facility was only temporarily inactive for repairs or remodeling". p61 "The applicant established future active use in an approved budget or plans".
- **Problems:**
  - The source lists three exceptions. The text omits the third, "or the applicant can clearly demonstrate its intent to begin use within a reasonable amount of time". That makes the rule stricter than FEMA's, which matters for historic buildings awaiting reuse.
  - It also drops the proviso on the repair exception: "provided a contractor is not responsible for the repair of disaster-related damage".
- **Suggested:** "… unless it was only temporarily closed for repairs or remodeling, you had approved plans or a budget to use it, or you can clearly show you intended to start using it within a reasonable time." Add the p61 citation "the applicant can clearly demonstrate its intent to begin use within a reasonable amount of time" (verifier: PASS).

### notes.age45_pa: NOT-SUPPORTED (also partly OVERSTATED)
- **Text:** "In FEMA's Public Assistance program, work on buildings 45 years or older is on FEMA's list of work that may affect historic resources and needs a more detailed review. That is true even if the building isn't listed as historic. Plan for this review before permanent repairs, and talk to FEMA and your SHPO early."
- **Quote:** p237 "Work affecting buildings, structures, sites, objects, or districts that are 45 years or older, historic landmarks of any age".
- **Problems:**
  - "Talk to … your SHPO" is not in the quote (see `ehp_first.summary`).
  - "Needs a more detailed review" is stronger than the source. The list is "examples of projects with the potential to impact natural and cultural resources" under "Projects Requiring Complex EHP Review" (p236), and the streamlined-review list just above (p236) includes "Projects intended to restore the facility back to pre-disaster condition using in-kind or like materials" with no age limit.
- **Suggested:** "In FEMA's Public Assistance program, work on buildings 45 years or older is on FEMA's list of work that may affect historic resources, even if the building isn't listed, and it may need a longer, more detailed review. Plan for this before permanent repairs and talk to FEMA early."

### notes.age45_private: NOT-SUPPORTED
- **Text:** "Buildings this old may be historic even if they aren't listed. FEMA's Public Assistance rules (for nonprofits and governments) send work on buildings 45 years or older for a more detailed historic review. FEMA's household grants have their own rules, but they are also covered by historic preservation law. Ask your SHPO before removing historic material."
- **Quotes:** PAPPG p237 (45 years). IAPPG p14 "Federally-funded IA grants and programs are subject to compliance with EHP compliance requirements, including … the National Historic Preservation Act."
- **Problems:**
  - "Ask your SHPO before removing historic material" is in neither quote. Neither guide places a SHPO-contact duty on a homeowner.
  - "Send … for a more detailed historic review" carries the same overstatement as `notes.age45_pa`.
  - "May be historic even if they aren't listed" is an inference from the 45-year threshold; acceptable as a JUDGMENT on its own.
- **Suggested:** Drop the SHPO sentence or reframe it as general advice with a supporting source (for example a THC handbook quote recommending SHPO contact, if one exists on a cited page). Change "send … for a more detailed historic review" to "flag … as work that may affect historic resources".

## pa-guidance.json: NOT-SUPPORTED *(context)*: true in the source, but not in the cited quote

All of these are accurate. The fix is to add a citation for the adjacent text. Every suggested quote below passes `verify_citation` and `page_check` as written.

| Item | Cited quote(s) | What's wrong | Source text to add (verifier PASS) |
|---|---|---|---|
| `pa_start.do[2]` "Nonprofits: have your IRS tax-exemption ruling letter ready, or your state's nonprofit documentation." | p57 "A ruling letter from the Internal Revenue Service that was in effect on the declaration date and granted tax exemption" | The state-documentation alternative is not in the quote, and the quote's condition "in effect on the declaration date" is dropped. | p57 "documentation from the State substantiating it is a non-revenue producing nonprofit entity". Optionally say "(in effect on the declaration date)". |
| `ehp_first.dont[0]` "Don't start permanent work that changes historic features before FEMA's review. If work doesn't follow the rules, FEMA may refuse to pay for all or part of it." | p62 "FEMA may take one of several actions including disallowing all or part of the cost of the project not in compliance." | Sentence 1 has no supporting quote; the p62 quote is about general noncompliance only. | The p214 quote already used in `ehp_first.do[0]` ("Applicants need to make every effort to afford FEMA the opportunity to perform … EHP reviews prior to starting any work …"). |
| `document.do[4]` "FEMA checks mold claims for signs of leaks from before the flood, like poorly sealed windows, rusty or clogged gutters, and water-stained ceiling tiles. Photograph these areas and keep your repair records." | p164 "FEMA evaluates whether the facility had pre-existing water infiltration conditions when determining whether mold remediation is eligible." p164 "Poorly maintained drains or gutters with rust or vegetative growth; and, Leaking and or water-stained ceiling tiles." | "Poorly sealed windows" comes from the list item the quote skips. (The advice to photograph is the app's own, which is fine.) | p164 "For this evaluation, FEMA considers whether there is evidence of pre-existing damage or deferred maintenance, such as improperly sealed windows or exterior vents" |
| `sba.dont[0]` "…If you decline it, FEMA only pays the costs the loan would not have covered. The same is true if SBA denies the loan because you can't meet its terms." | p52 "If the PNP declines an SBA loan, PA funding is limited to the costs that the loan would not have otherwise covered. This applies even when the PNP cannot accept the terms of the loan" | "SBA denies the loan" is in the next clause, not the quote. | p52 "by, for example, not meeting a collateral requirement and the SBA therefore denies the loan" |
| `collections.do[1]` "FEMA can pay to stabilize damaged collections and objects, for example by controlling temperature and humidity, and by cleaning them to stop further damage." | p197 "Stabilization of damaged collections or individual objects is eligible." p197 "Treating damaged items utilizing environmental controls to achieve proper temperature and humidity" | "Cleaning" is not in either quote. | p197 "and chemical or mechanical cleaning to stabilize items to prolong their existence" |
| `historic_exceptions.do[1]` "Normally, when repair would cost more than replacement, FEMA pays only the replacement cost. For a historic building, …" | p182 "If the facility is listed in, or meets the criteria to be listed in, the National Register … costs … are eligible, even if repair costs exceed replacement costs." p211 "A historic facility is defined as one listed in, or eligible for listing in, the National Register of Historic Places." | Sentence 1 has no supporting quote. It also drops the source's condition that the cap applies "when a facility is eligible for replacement". | p182 "This is an exception to the regulatory requirement that when a facility is eligible for replacement, FEMA limits eligible costs to the less expensive of repairs or replacement". Reword: "Normally, when a building qualifies for replacement, FEMA pays the lesser of repair or replacement." |
| `help.do[0]` "Ask your FEMA contact about the Heritage Emergency National Task Force (HENTF), a FEMA and Smithsonian partnership…" | p245 "HENTF can serve as a technical assistance resource for field staff … evaluating scopes of work for treatment of objects." THC p19 "and address their aftermath; they can be contacted by email at culturalrescue@si.edu." | "A FEMA and Smithsonian partnership" is in neither quote. | p245 "a partnership between FEMA's Office of Environmental Planning and Historic Preservation (OEHP) and the Smithsonian Cultural Rescue Initiative" |

## pa-guidance.json: JUDGMENT

| Item | Cited quote(s) | Issue | Suggested |
|---|---|---|---|
| `ehp_first.do[1]` "Emergency work … counts as emergency work if you do it promptly… it encourages you to coordinate before you start." | p132 "Extracting water and clearing mud, silt, or other accumulated debris from eligible facilities if the work is conducted expeditiously for the purpose of addressing an immediate threat". p238 "FEMA must ensure that the applicant's emergency protective measures, where possible: 1) avoid impacts to … historic properties". p238 "FEMA encourages applicants to coordinate prior to conducting work to front-load any applicable EHP considerations in a timely manner." | Drops "from eligible facilities" and "for the purpose of addressing an immediate threat" from the first quote (partly restated as "to deal with an immediate threat"). The encouragement to coordinate is scoped in the source to "emergency work that occurs in or near impacted areas that have natural and cultural resources". A historic building plausibly is one, so this is low risk. | "…can be eligible emergency work if it is done promptly to address an immediate threat. … Where historic or natural resources are involved, FEMA encourages you to coordinate before you start." |
| `ehp_first.dont[1]` "Don't let debris crews haul away historic material…" | p238 "FEMA must ensure that the applicant's debris removal operations avoid impacts to such resources as floodplains, wetlands, … and historic properties" | The quote says debris removal must avoid impacts to "historic properties" (a legal term for buildings, sites, and so on), not loose "historic material". The advice is a reasonable application, but not what the quote literally says. | "Don't let debris crews haul away material from a historic building without checking first. FEMA must make sure debris removal avoids harm to historic properties." |
| `flood_insurance.summary` "…FEMA requires insurance after it pays for permanent repairs." | (record) p220 "Applicants that receive PA funding for permanent work … must obtain and maintain insurance to protect the facility against future loss." | Same $5,000 waiver omission as `dont[1]`. Acceptable at summary level if `dont[1]` is fixed. | "…FEMA usually requires insurance after it pays for permanent repairs." |
| `deadlines.summary` "Most can be extended, but you have to ask in writing and give a reason." | (record) p46 "…if a recipient submits a request in writing with justification based on extenuating circumstances". p70 "…if an applicant submits a request with justification based on extenuating circumstances". p248 "Recipients may extend emergency work…". p209 replacement request (no extension stated). | The RPA extension is requested by the *recipient* (state), not the applicant. The Impact List extension needs "a request with justification" but "in writing" isn't stated. The replacement-request deadline has no stated extension. The bar is "extenuating circumstances", not "a reason". | "…Some can be extended, but only with a written justification based on circumstances beyond your control." |
| `deadlines.do[3]` "…Your state can extend emergency work by up to 6 more months and permanent work up to 30 months, one project at a time." | p247 "For emergency work, the deadline is six months from the disaster declaration date." p247 "For most permanent work, the deadline is 18 months, except for category I projects". p248 "Recipients may extend emergency work up to an additional six months and permanent work up to 30 months on a project-by-project basis" | p248's quote is preceded by "Recipients have authority to grant time extensions **due to extenuating circumstances**". That basis is dropped. The 30-month figure reproduces the source's own ambiguity (additional, or total?); that's acceptable because it mirrors the source. | "…If there are extenuating circumstances, your state can extend…" (add p248 "Recipients have authority to grant time extensions due to extenuating circumstances", verifier PASS) |
| `collections.do[5]` "Wet paper records can often be saved. Freeze-drying is one way FEMA can pay to stabilize them." | p197 "Recovery of damaged hard copies includes labor and materials, such as bags, boxes, and containers. Stabilizing damaged hard copies includes freeze-drying." | "Can often be saved" is not in the quote, which only lists freeze-drying as part of stabilizing hard copies. | "Wet paper records may be saved. Freeze-drying is one stabilization step FEMA can pay for." |

## pa-guidance.json: SUPPORTED (29)

`pa_start.summary`, `pa_start.do[0]`, `pa_start.do[1]`, `pa_start.do[3]`, `ehp_first.do[2]`, `document.summary`, `document.do[1]`, `document.do[2]`, `sba.do[1]`, `sba.do[2]`, `sba.do[3]`, `flood_insurance.do[0]`, `flood_insurance.do[1]`, `deadlines.do[2]`, `collections.summary`, `collections.do[0]`, `collections.do[2]`, `collections.do[3]`, `collections.do[4]`, `collections.dont[0]`, `historic_exceptions.summary`, `historic_exceptions.do[0]`, `historic_exceptions.do[2]`, `historic_exceptions.dont[0]`, `other_rules.summary`, `other_rules.do[0]`, `other_rules.dont[1]`, `help.summary`, `help.do[1]`.

---

## content-bundle.json (`entailment_audited: false` items)

Item paths are JSON paths. `guidance[5]` is `structural` and `guidance[9]` is `recovery_aid`; both have audience `homeowner`.

### guidance[9]/do[5]: OVERSTATED
- **Text:** "If your home is in a FEMA Special Flood Hazard Area … and FEMA pays for home repair, home replacement, or personal property, you must buy and keep flood insurance (NFIP or private) for at least the amount of that aid. If you don't, you can't get FEMA help for flood damage in a future flood."
- **Quotes:** IAPPG p64: "…must obtain and maintain flood insurance coverage for at least the amount of disaster assistance they receive" / "Applicants may satisfy the insurance requirement by purchasing private insurance or a policy through the NFIP." / "Applicants who do not obtain and maintain flood insurance will be ineligible for IHP assistance for flood-damaged real or personal property in future disasters with flood-related damage."
- **Problems:**
  - "Can't get FEMA help for flood damage" is broader than "ineligible for IHP assistance for flood-damaged real or personal property". Other household help, such as rental or non-SBA-dependent other-needs assistance, is not barred by this sentence.
  - The requirement also covers only aid "for NFIP-insurable items", which the text drops.
- **Suggested:** "…you must buy and keep flood insurance (NFIP or private) for at least the amount of that aid for flood-insurable items. If you don't, FEMA won't help repair or replace flood-damaged home or belongings in a future flood."

### guidance[9]/dont[1]: JUDGMENT
- **Text:** "Don't count on FEMA home repair money to restore historic materials. It is meant to make the home safe, sanitary, or functional, and it is priced at average quality."
- **Quotes:** IAPPG p86 "Home Repair Assistance is intended to make the damaged home safe, sanitary, or functional." IAPPG p89 "…based on repair or replacement of components that are of average quality, size, or capacity."
- **Problem:** "Restore historic materials" is an inference. Neither quote mentions historic material, though the inference is strong. The sentence right after the p86 quote states it more directly.
- **Suggested:** Keep the text and add the IAPPG p86 citation "It is not intended to return the home to its predisaster condition." (verifier: PASS).

### SUPPORTED (9)
`guidance[5]/do[6]` (basement), `guidance[9]/do[0]`, `do[1]`, `do[2]`, `do[3]`, `do[4]`, `do[6]`, `dont[0]`, `dont[2]`.

---

## Notes outside the strict scope (no verdict)
- `guidance[5]` (`structural`) carries no `owners` filter. If the app shows that record to nonprofit or government owners, `do[6]` (FEMA household-program basement limits) would appear for buildings that go through Public Assistance instead. Worth a check in `floodapp.html` (`paOwnerMatch` only filters the PA panel).
- `pa-guidance.json` `verification.entailment_audited` should stay `false` until the fixes above are applied and Becca or APTI DRI signs off.
