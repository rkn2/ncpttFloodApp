# Flood app vs FEMA PAPPG v4 (June 2020): review, 2026-10-02

Source: https://www.fema.gov/sites/default/files/documents/fema_pappg-v4-updated-links_policy_6-1-2020.pdf (read from a Wayback copy; FEMA blocked direct download). Page numbers are **printed** page numbers (PDF page = printed + 1). **v4 is superseded by PAPPG v5 (Jan 2025): re-verify every cite against v5 before shipping it** (see `pappg-v5-cite-map.md` when it exists).

## Headline
The app treats every user as a private homeowner. Homeowners fall under Individual Assistance (IA), not Public Assistance (PA). PA covers PNPs (houses of worship, museums, libraries, community centers; p.43-46) and governments owning historic buildings (p.56). Assessor mode already lists Museum / Religious / Government occupancy (`floodapp.html:2274`) but gives no PA guidance.

## Where the app aligns
| App | PAPPG v4 |
|---|---|
| Start cleanup promptly (`content-bundle.json:683`, `:750`) | Damage/mold from failure to protect in reasonable time is ineligible (p.52, 137, 172) |
| Photograph before repairs (`:750`, `floodapp.html:1117`) | Documentation requirements (p.63); EHP review wants photos (p.143) |
| Mold PPE, containment, HVAC cleaning (`:683-750`) | Eligible mold work (p.136); EPA methods (App. I p.240) |
| Repair windows/roofs vs replace | 50% rule n/a to components; repairable component = repair only (p.159) |
| Contact SHPO/FEMA early (`floodapp.html:1101`, `programs.json:31`) | Allow EHP review before work (p.141-142) |
| Elevate utilities | 406 mitigation (p.155); App. J measures (p.242) |

## Conflicts / bugs
1. **Section 106 trigger too narrow** (`floodapp.html:2039-2042`, messages `:1101` / `:1102`). Only "NR listed" gets the Section 106 message. PAPPG covers listed **or eligible** properties (App. A p.221; p.149; p.159).
2. **Fiberglass insulation inconsistent**: `content-bundle.json:70`, `:356` say case by case; `:320`, `:728`, `floodapp.html:3176` say remove all wet insulation. PAPPG App. I p.241 (advisory EPA summary, p.136) says discard.
3. **Bug**: `content-bundle.json:770` "Remove all flooded carpeting" sits in the mold `dont` list.
4. **Unverifiable against PAPPG** (IA claims): `programs.json:9`, `:20`. Check against the IAPPG.

## Gaps, ranked for historic building owners
1. No permanent work, demolition, or historic fabric removal before EHP/Section 106 review (p.141-142); emergency work must avoid historic impacts (p.110); muck-out is emergency only if prompt for immediate threat (p.111).
2. Document pre-disaster condition: photos, maintenance records (p.52, 172); FEMA screens mold for pre-existing leaks, gutters, ceilings (p.137).
3. Houses of worship / museums must apply for an SBA loan first; missing the deadline makes permanent work ineligible (p.57-58; App. B p.229).
4. Flood insurance: uninsured in SFHA = reduction by max NFIP payout (p.162); obtain-and-maintain requirement (p.144-145). App never mentions NFIP.
5. Deadlines: RPA 30 days (p.36); damage list 60 days after scoping meeting (p.60); replacement request 1 yr (p.158); emergency work 6 mo / permanent 18 mo (p.196).
6. Collections: stabilization eligible, replacement not; qualified conservator, AIC Code, accession records (p.175-176); moving contents = emergency work (p.111). Do **not** adopt App. I's "photocopy and discard valuable papers" (p.240).
7. Historic exception to 50% rule for listed/eligible buildings (p.149, 159); most state historic building codes don't qualify (p.149).
8. Smaller: vacant/inactive buildings ineligible (p.58); museum grounds ineligible (p.46); mold sampling by independent professional (p.136-137); mixed use needs >50% eligible use (p.56).

## Recommendation
Add a nonprofit/public-owner PA path triggered by building type; keep homeowner path on IA, SBA, NFIP; add PAPPG v5 to `docs/`.
