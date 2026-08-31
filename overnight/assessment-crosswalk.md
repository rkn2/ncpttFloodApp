# Assessment Crosswalk: App vs. NCPTT Source Forms vs. Guidance Engine

*Generated 2026-08-31. Compared against the three NCPTT forms in `simeonResources/` and the 9-category guidance engine in `content-bundle.json`.*

---

## Source Documents Used

| Abbreviation | Full Name | Date |
|---|---|---|
| **RBSCA** | Rapid Building and Site Condition Assessment | FEMA/NPS/NCPTT, 9/2005 |
| **DBSCA** | Detailed Building and Site Condition Assessment | FEMA/NPS/NCPTT, Updated 7/2011 |
| **Combined** | Combined Building and Site Condition Assessment | FEMA/NPS/NCPTT, Updated 7/2011 |
| **Definitions** | RBSCA Definitions | 7/2011 |

The Combined form merges Rapid + Detailed into one 3-page instrument. The Detailed form is a superset of the Rapid. The app models this as two separate modes (Rapid Triage → Full Assessment), matching the NCPTT intent of a quick screen that can escalate.

---

## 1. Rapid Triage: App vs. RBSCA

### Fields in the app that ARE in the RBSCA (justified)

| App Field | RBSCA Field | Match Quality |
|---|---|---|
| Inspector name | Inspector | Exact |
| Date | Inspection date/time | App drops time — minor |
| Area / Neighborhood | *(not on RBSCA)* | See "not in source" below |
| Building Name | Building name | Exact |
| Address | Address | Exact |
| Number of Stories | Number of stories above ground / below ground | App omits "below ground" — minor gap |
| Est. Footprint (sq ft) | Approx footprint area (square feet) | App uses ranges; RBSCA is free text |
| Number of Units | Number of residential units | Exact |
| Approx. Age | Building age (0–25, 25–50, 50–100, 100+) | App uses different bins (Pre-1870, 1870–1940, 1940–1970, Post-1970) — **mismatch** (see §5) |
| Foundation Type | Foundation (Pier, Slab, Chain Wall, Basement) | App adds Stone/rubble, Brick, Poured concrete, Concrete block, Crawl space — reasonable expansion |
| Roof Type | Roof type (Hipped, Gable, Mansard, Pyramid, Flat) | App matches + adds Gambrel, Shed — reasonable |
| Wall Finish / Siding | Wall finish (Stucco, Wood, Vinyl, Masonry, Asbestos) | App matches + adds Wood shingle, Concrete block |
| Historic Status | Historic designation (NHL, NR/District, State/Local, Eligible) | App omits "Eligible" and "NHL" as separate — minor |
| Nature of Water | Nature of water (Standing, Flowing, Seepage, Water Marks) | App has Standing, Flowing/moving, Seepage/groundwater, Combined sewage. RBSCA has "Water Marks" and "Other"; app has "Combined sewage" — different but valid |
| Water Depth/Location | Space where water entered + Depth from main floor | App combines into checkboxes (Basement only, <1ft, 1–4ft, >4ft, Second floor). RBSCA separates location from depth measurement. App is less precise but more usable on a phone |
| Sediment | Sediment deposited (On Site, In Structure) | App simplifies to Yes/No/Unknown; RBSCA distinguishes on-site vs. in-structure — **gap** |
| Erosion | Site erosion (Yes, No, Don't know) | Exact match |
| Damage categories (10 cats, None/Minor/Moderate/Severe) | Evaluation section (9 rows, Minor/None – Moderate – Severe) | See detailed comparison in §4 |
| Overall Damage Estimate | Estimated Building Damage (None, 1–10%, 10–30%, 30–60%, 60–90%, 90–100%) | App uses 0–10%, 10–30%, etc. — matches with slightly different labels |
| Posting (Inspected / Restricted Use / Unsafe) | Posting (Inspected, Restricted Use, Unsafe, Historic Designation, Detailed Evaluation Needed) | App omits "Historic Designation" as a posting option — see §3 |
| Recommend Full Assessment (with trigger reasons) | Detailed evaluation recommended (Structural, Environmental, Archaeological, Historic Significance, Collections) | Good match; app adds "Other" |
| Notes | Other recommendations | Exact |

### Fields in the app NOT in the RBSCA (possibly unnecessary)

| App Field | Assessment |
|---|---|
| **Area / Neighborhood** | Not on any NCPTT form. Useful for SHPO aggregation ("show me all buildings in Ward 3") — **keep, it's an app-specific improvement** |
| **Footprint as ranges** | RBSCA uses free text. Ranges are a mobile UX choice — fine |

### Fields in the RBSCA NOT in the app (gaps)

| RBSCA Field | Impact | Priority |
|---|---|---|
| **Affiliation** (inspector's org) | Important for SHPO — who sent this person? | Medium — add next to inspector name |
| **Area Inspected** (Exterior Only / Exterior and Interior) | Documents scope of assessment. A rapid triage done exterior-only has different weight than one with interior access | High — add as radio |
| **Type of Construction** (Wood Frame, Steel Frame, Concrete, Brick, Stone, Manufactured, Boat) | RBSCA captures structural system, not just wall finish. App has wall finish but NOT structural framing type. These are different things | **High** — the guidance engine's structural/foundation advice depends on whether it's wood frame vs masonry bearing wall |
| **Primary Occupancy** (Dwelling, Commercial, Museum, School, Religious, etc.) | Missing entirely from app. Affects which programs apply (residential vs. commercial disaster assistance) and risk profile (museum = collections) | **High** — add as select |
| **Occupied?** | Whether someone is currently living in the damaged building — safety/urgency signal | Medium |
| **Repairs begun?** | Whether unauthorized repairs may already be changing historic fabric | Medium |
| **Owner/Contact Info** | SHPO needs to reach the owner. App has no contact capture at all | Medium for SHPO sync use case |
| **Roof Covering** (Slate, Metal, Tile, Asphalt, Asbestos) | Distinct from roof type (shape). App has roof shape but not covering material. **The guidance engine's roof advice specifically discusses slate vs. tile vs. asphalt** | **High** — the guidance literally says "Do NOT replace historic slate, clay tile, or other character-defining roofing materials with modern substitutes" but never asks what the roof is made of |
| **Landscape Features** (Walkway, Driveway, Fences, Sculpture/Fountains, Structures) | Checklist of site features present. App has landscape as a rapid damage category but doesn't inventory what features exist | Low |
| **Visible Artifacts** (Bone, Pottery, Metal, Stone, Glass) | Archaeological material inventory | Low — niche |
| **Interior Condition** summary checkboxes (Structural Damage, Mold/Mildew, Falling Plaster) | Quick interior condition flags separate from the per-category damage ratings | Low — app's damage categories cover this |
| **Interior Contents** (Antiques, Archives, Art Work) | What's inside — collections triage. App captures this in Full but not Rapid | Low for rapid |
| **Appears Historic?** / **Sign or plaque?** | Quick historic-significance screen. App has "Historic Status" checkboxes which partially covers this | Low — covered differently |
| **Historic District Name** | Free text field for the district name | Low — nice to have |
| **Potential Hazards** (Electrical, Lead, Asbestos, Mold) as separate checkboxes | RBSCA has this as a distinct section. App captures this in Full Assessment but not Rapid | Medium — hazards affect safety posting |
| **Recommendations** (Add Temporary Roof Covering, Board, Shore, Other) | Specific actionable checklist. App has free-text notes only | Medium |
| **Barricades needed** | Safety action item | Low |
| **Attachments** checkboxes (Sketches, Photographs, Documents) | Document what was collected | Low |
| **Depth of water measured from main floor** (numeric +/-) | RBSCA asks for an actual measurement. App uses ranges. The measurement is more useful for engineering | Medium — keep ranges for usability, but consider adding optional numeric field |

---

## 2. Full Assessment: App vs. DBSCA

### Key differences

The DBSCA (Detailed form) is a 3-page instrument. The app's Full Assessment covers most of it but with notable differences:

**What the app has that matches well:**
- Inspector, Date, Building Name, Address, GPS (5 points → now 1 auto-populated)
- Hazards section (Electrical, Chemical, Mold, Asbestos, Lead)
- Significance questions (6 yes/no/don't know questions) — exact match to DBSCA
- Architectural styles checklist — matches DBSCA closely
- Site Evaluation (Topographic, Retaining Walls, Vegetation, Small Structures) — matches
- Archaeological Material — matches
- Exterior Damage ratings — see §4
- Interior Damage ratings — see §4
- Contents/Collections — matches
- Final Posting — matches (app adds "Further Evaluation" which DBSCA also has)

**What the DBSCA has that the app's Full Assessment is missing:**

| DBSCA Field | Impact |
|---|---|
| **Affiliation** | Same gap as Rapid |
| **Area Inspected** (Exterior Only / Ext+Int) | Same gap |
| **Type of Construction** | Same gap — **high priority** |
| **Primary Occupancy** | Same gap — **high priority** |
| **Occupied? / Repairs begun?** | Same gap |
| **Owner/Contact Info** | Same gap |
| **Roof Covering** (material, not shape) | Same gap — **high priority for guidance** |
| **Building Age** | Rapid has it; Full Assessment form doesn't re-ask it (carries from Rapid on escalation) but Full-from-scratch doesn't capture it |
| **Stories / Footprint / Units** | Same — Full form doesn't ask these (Rapid does). Full-from-scratch loses them |
| **Foundation type / Roof shape / Wall finish** | Same — captured in Rapid but not re-asked in Full |
| **Flood Data** (water nature, depth, sediment) | DBSCA and Combined both include Flood Data. App's Full Assessment has NO flood data section — it's only in Rapid. **Major gap if Full is entered directly** |
| **"Is it possible to enter?"** / **"Is it Safe to enter?"** | DBSCA asks these explicitly as yes/no before the interior section | Medium |
| **Estimated Building Damage** percentage | On DBSCA page 3. App's Full Assessment doesn't have this (Rapid does) | Medium |
| **Sketch page** | DBSCA page 3 is a grid for sketching damage. App has no sketch/photo capture | Medium — phone camera partially replaces this |
| **Interior: Missing architectural features** | DBSCA exterior eval row. App's `FULL_DAMAGE_INTERIOR` doesn't have this | Medium |
| **Interior: Graffiti, vandalism, evidence of looting** | DBSCA has this as an eval row | Low-Medium |
| **Interior: Standing water** | DBSCA has this as an eval row (separate from flood data) | Medium |
| **Exterior: Standing water** | DBSCA exterior eval has this | Medium |
| **Exterior: Shutter damage** | DBSCA has it; app doesn't | Low |
| **Exterior: Cornice damage** | DBSCA has it; app doesn't | Low |
| **Exterior: Balcony damage** | DBSCA has it; app doesn't | Low |
| **Exterior: Missing architectural features** | DBSCA has it; app doesn't | Medium |
| **Exterior: Porch damage** | DBSCA has it; app has "Porches / balconies" — partial match |

---

## 3. Posting Classification Mismatch

| Source (RBSCA) | App Rapid | App Full | Notes |
|---|---|---|---|
| Inspected | ✅ | ✅ | |
| Restricted Use | ✅ | ✅ | |
| Unsafe | ✅ | ✅ | |
| **Historic Designation** | ❌ | ❌ | RBSCA has this as a posting option. It's not a safety classification — it's a flag that the building has been identified as historic during the assessment. This is useful for SHPO triage and probably should be a separate checkbox rather than a posting option, which the app handles via "Historic Status" checkboxes |
| **Detailed Evaluation Needed** | ✅ (as "Recommend Full") | ✅ (as "Further Evaluation") | Same intent, different label |

---

## 4. Damage Category Comparison

### Rapid Triage Damage Categories

| App Category | RBSCA Equivalent | Match |
|---|---|---|
| Structural | Collapsed or off foundation + Leaning, other structural damage | App merges two rows into one — **loses distinction** between "off foundation" and "leaning" |
| Roof | Roof damage | Exact |
| Foundation | Foundation damage | Exact |
| Siding / Cladding | Siding damage | Exact |
| Windows / Doors | Damage to windows, doors | Exact |
| Chimney | Chimney, parapet, or other falling hazard | App narrows to chimney; RBSCA includes parapets and other falling hazards |
| Electrical / Mechanical | Damage to electrical, mechanical, AC systems | Exact |
| Landscape / Site | Landscape damage | Exact |
| Interior Finishes | *(not on RBSCA rapid)* | **App addition** — RBSCA rapid doesn't have a separate interior damage row (it's in the Detailed form). Reasonable addition |
| Mold / Contamination | *(not on RBSCA rapid)* | **App addition** — RBSCA has mold only as a Potential Hazard checkbox, not a damage severity. App treats it as a damage category with its own severity — reasonable given guidance engine needs |

**Severity scale:** Both use Minor/None – Moderate – Severe. The app adds an explicit "None" button separate from Minor, which the RBSCA combines as "Minor/None." This is arguably better — it distinguishes "I looked and it's fine" from "minor damage."

### Full Assessment Exterior Damage Categories

| App Category | DBSCA Equivalent | Match |
|---|---|---|
| Foundation | Foundation Damage | ✅ |
| Basement walls | *(not in DBSCA)* | **App addition** |
| Exterior walls | Building leaning, other structural damage (partial) | Loose |
| Roof structure | Roof Damage (partial) | DBSCA doesn't split roof structure from covering |
| Roofing material | Roof Damage (partial) | Same — app splits what DBSCA keeps together |
| Chimneys | Chimney, Parapet, or Other Falling Hazard | App narrows scope |
| Porches / balconies | Porch damage + Balcony damage | DBSCA has these separate; app merges |
| Windows | Damage to windows, doors (partial) | App splits what DBSCA combines |
| Doors | Damage to windows, doors (partial) | Same |
| Exterior trim | *(not in DBSCA as separate)* | **App addition** |
| Siding / cladding | Siding Damage | ✅ |
| Paint / coatings | *(not in DBSCA)* | **App addition** |
| Drainage / gutters | *(not in DBSCA)* | **App addition** |
| Steps / walkways | *(partially in Site Evaluation)* | Different section in DBSCA |
| Fencing | *(in Site Evaluation)* | Different section |
| Site features | *(in Site Evaluation)* | Different section |

**DBSCA exterior rows the app is missing:**
- Standing water (exterior)
- Collapsed or off foundation (as separate from foundation damage)
- Missing architectural features
- Shutter damage
- Cornice damage
- Balcony damage (separate from porches)
- Graffiti, vandalism, evidence of looting

### Full Assessment Interior Damage Categories

| App Category | DBSCA Equivalent | Match |
|---|---|---|
| Ceiling structure / finish | Ceilings | ✅ |
| Floor structure | First Floor structure | ✅ |
| Floor covering | First Floor flooring | ✅ |
| Interior walls / plaster | First floor walls | ✅ |
| Stairways | *(not in DBSCA)* | **App addition** |
| Upper floor structure | Damage to upper floors | ✅ |

**DBSCA interior rows the app is missing:**
- Missing architectural features
- Graffiti, vandalism, evidence of looting
- Standing water (interior)

---

## 5. Age Bins Mismatch

| RBSCA / DBSCA | App |
|---|---|
| 0–25 yr | Post-1970 |
| 25–50 yr | 1940–1970 |
| 50–100 yr | 1870–1940 |
| 100+ yr | Pre-1870 |

The NCPTT bins are relative to assessment date (e.g. "50–100 yr" = eligible for NR consideration). The app's bins are absolute date ranges. The app's approach is **better for data consistency** (a 2005 assessment and a 2026 assessment categorize the same building identically) but **doesn't match the source form** and loses the "50 year" NR-eligibility signal that the NCPTT bins are designed to capture.

**Recommendation:** Keep the app's absolute bins but add the DBSCA's significance question "Does this property appear to be older than 50 years?" (already present in Full Assessment, missing from Rapid).

---

## 6. What the Guidance Engine Needs but Neither Form Collects Well

The 9-category content-bundle.json produces guidance keyed by damage category. Here's what it assumes the user knows:

| Guidance Category | Key Assumptions in the Guidance Text | What the Form Collects | Gap |
|---|---|---|---|
| **Structural / Foundation** | Mortar type (lime vs. Portland), masonry type | Nothing about mortar or masonry type | Guidance says "repoint with lime-based mortar" but doesn't know if the building HAS masonry |
| **Roof** | Roof covering material (slate, clay tile, wood shingle vs. asphalt) | Roof shape only. **No covering material.** | **Critical gap** — the guidance's most important advice ("don't replace historic slate with asphalt") requires knowing the covering material |
| **Siding** | Wall material (wood, masonry) | Wall finish in Rapid; not in Full | Partial — Rapid has it but guidance is served to homeowners who don't go through Rapid |
| **Windows** | Whether windows are historic wood | Nothing | Moderate gap — guidance says "historic windows can often be restored" but doesn't know if they're historic |
| **Insulation** | Whether insulation is present and what type | Nothing | The guidance discusses fiberglass batts, spray foam, etc. but doesn't know what's installed |
| **Electrical** | Whether systems were submerged | Water depth (in Rapid) | Inferred from water level — adequate |
| **Mold** | Area of contamination (10 sq ft threshold for professional remediation) | Severity rating only | Moderate gap — can't distinguish "3 sq ft in a closet" from "entire basement" |

---

## 7. Rapid vs. Full: Does the Split Match the Source Forms' Intent?

The NCPTT designed the Rapid form as a **one-page field screen** that a trained assessor fills out building-by-building during the first pass through a disaster area. The Detailed form is a **3-page deep-dive** for buildings flagged during rapid triage.

**The app's split generally matches this intent, with two structural problems:**

1. **Full Assessment entered directly (not via escalation from Rapid) loses critical data.** The Full form doesn't re-ask: building age, stories, footprint, units, foundation type, roof type/shape, wall finish, flood data (nature of water, depth, sediment, erosion), or overall damage percentage. These are all captured in Rapid but not in Full. If an assessor starts directly in Full Assessment, they skip all of it.

2. **The homeowner walkthrough and the assessor rapid triage ask about the same building differently and can't be cross-referenced.** A homeowner reports "ankle to knee height on the first floor" and gets mapped to `electrical: moderate`. An assessor doing rapid triage on the same building rates `electrical: minor/moderate/severe` independently. Neither knows about the other. This is fine for v1 but becomes a problem when the SHPO backend aggregates both.

---

## 8. Priority Recommendations

### Must-fix (fields that affect guidance accuracy or match source form requirements)

1. **Add Roof Covering Material** — slate, metal, tile, asphalt, wood shingle. The guidance engine's roof advice is keyed to this and currently can't distinguish a building with historic slate from one with modern asphalt. Add to both Rapid and Full.
2. **Add Type of Construction** — wood frame, steel frame, concrete, brick, stone, manufactured. Different from wall finish. Affects structural guidance.
3. **Add Primary Occupancy** — dwelling, commercial, museum, school, religious, etc. Affects which assistance programs apply and whether collections guidance is relevant.
4. **Add Flood Data to Full Assessment** — nature of water, depth, sediment. Currently only in Rapid; a direct-entry Full assessment has no flood data at all.

### Should-fix (NCPTT form compliance, SHPO utility)

5. **Add Affiliation** (inspector's organization) — one text field, standard on all NCPTT forms.
6. **Add Area Inspected** (Exterior Only / Exterior and Interior) — one radio, documents assessment scope.
7. **Carry Rapid fields into Full on escalation** — when "escalate to Full" is clicked, ensure building age, stories, wall finish, flood data, etc. are preserved and visible.
8. **Add Occupied? / Repairs begun?** — two yes/no radios, both on all NCPTT forms.
9. **Add "Collapsed or off foundation"** as a distinct damage row, separate from general structural damage — this is the most severe structural condition and RBSCA calls it out specifically.
10. **Split Sediment** into On Site / In Structure (matches RBSCA).

### Nice-to-have (completeness, lower priority)

11. Add Potential Hazards to Rapid (currently only in Full).
12. Add missing DBSCA exterior rows: standing water, missing architectural features, shutters, cornices, balconies, graffiti/vandalism.
13. Add missing DBSCA interior rows: missing architectural features, standing water, graffiti/vandalism.
14. Add sketch/photo annotation capability.
15. Add Owner/Contact Info fields.
16. Add Historic District Name free text.
