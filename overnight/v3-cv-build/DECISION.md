# v3 computer vision: not shipping — decision record

**Date:** 2026-07-15
**Status:** closed. Manual entry remains the only path for building info and
damage severity. The `v3-computer-vision` branch (GitHub) is parked, unmerged.

## What was planned

Two photo-based suggestion features for the homeowner wizard: a facade photo
suggesting building type/materials/age, and a damage photo suggesting
per-category severity (9 categories). Built on `v3-computer-vision`:
`api/vision-assess.py`, a server-side Vercel proxy calling Claude's vision API,
plus client UI with confidence badges and a critic pass. Full build history:
`overnight/v3-cv-build/` on that branch; plan doc `V3_CV_PLAN.md`.

That work was structurally complete and verified (request validation, payload
sizing, offline degradation), but never tested for real — it needed an
`ANTHROPIC_API_KEY` in Vercel that was never provisioned.

## Why it changed direction

Before deploying, Becca asked to drop the LLM call entirely and use her own
Python CV instead, branched from the sibling research repo
`~/Code/compvision/llmDamagev3`. Investigation found that repo's own damage
assessment is *also* LLM-based (`assess.py` via Claude on Vertex) — no
non-LLM implementation of damage severity existed anywhere to port. Its
`facade_cv/` directory does have real non-LLM CV (story counting, fenestration
%, roof shape), but tuned only on 5 downtown Montpelier commercial buildings
via satellite imagery and address lookups, not owner phone photos.

## What was actually tried

New branch `residential-facade-cv` in `~/Code/compvision/llmDamagev3`,
redesigned to take 1-10 arbitrary owner-submitted photos per building. Full
methodology and scoreboard: `facade_cv_residential/VALIDATION.md` on that
branch (pushed to `github.com/rkn2/llmDamagev3`).

Tested against 6 real buildings with documented ground-truth story counts
(Wikipedia/NRHP text + one real homeowner photo). The original script,
unmodified, overcounted every pitched-roof building by 1-2 stories (roofline
read as extra floors) — 1/6 correct. After redesigning the facade-top
detection (eave-crop) and switching to window-blob row counting instead of
edge detection: **4/6 correct or close.** A real, evidenced improvement over
baseline, honestly reported including a regression that was caught and
reverted mid-round (documented in that file, not swept under the rug).

## Why 4/6 isn't good enough to ship

Two reasons, not one:

1. **The remaining failure modes aren't edge cases for this app's users.**
   Full-width front porches — extremely common on historic American houses
   (Colonial Revival, Victorian, Craftsman, Greek Revival) — produce false
   extra floors every time, because the porch roof creates the same kind of
   false signal the main roof did before the fix. Photos that are angled or
   partly obstructed (branches, cars, fences) are the realistic default for a
   homeowner's phone photo, not a rare edge case, and those also degrade
   accuracy. Real-world accuracy on floodAPp's actual user base is likely
   well below the 4/6 measured on a curated validation set.

2. **Story count isn't a valuable thing to automate even at 100% accuracy.**
   A homeowner already knows how many floors their house has — it's a
   one-tap manual field, not a task worth a CV pipeline. The fields that
   would genuinely save a homeowner effort — materials, age, damage severity
   — have no non-LLM path in this codebase at all; only geometric
   measurements (story count, fenestration %) are CV-derivable from a photo
   this way. Automating the easy, low-value field while the hard, high-value
   fields stay manual isn't worth the added failure surface and maintenance
   burden.

## Decision

- floodAPp's wizard stays manual-entry-only for building info and damage
  assessment. No CV or LLM suggestion feature ships in v3.
- `v3-computer-vision` branch is left unmerged on GitHub as a reference (the
  vision-assess.py proxy and client UI are real, working code if this is
  revisited later with a validated accuracy source).
- The one unrelated fix on that branch (chat FAB overlap / severity button
  mobile clipping) was cherry-picked to `main` separately — it was never
  CV-specific.
- `residential-facade-cv` in the sibling `llmDamagev3` repo is left as a
  research checkpoint, not deleted — the eave-detection/window-blob approach
  may be useful for that repo's own Montpelier pipeline even though it isn't
  going into floodAPp.
