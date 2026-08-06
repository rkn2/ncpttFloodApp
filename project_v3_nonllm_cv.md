---
name: project-v3-nonllm-cv
description: "floodApp v3 CV pivot to non-LLM Python CV, branched in ~/Code/compvision/llmDamagev3 (branch residential-facade-cv) — research checkpoint, 4/6 validated, not wired into floodAPp yet"
metadata:
  type: project
  originSessionId: 751392c7-33da-4686-8075-a6d68d43eb3c
---

Becca rejected the LLM vision proxy for floodAPp's v3 CV feature (facade/damage
photo suggestions) — wanted her own non-LLM Python CV instead, sourced from the
sibling research repo `~/Code/compvision/llmDamagev3`. That repo's own damage
assessment (`assess.py`) is itself LLM-based (Claude via AnthropicVertex) —
that part had no non-LLM equivalent to port. Its `facade_cv/` directory does
have real non-LLM CV (story counting, fenestration %, roof shape from aerial
tiles) but tuned only on 5 downtown Montpelier commercial buildings via
satellite imagery + address lookups, not owner phone photos.

Becca's direction: rebuild this to take 1-10 arbitrary owner-submitted photos
per building instead of aerial imagery/address lookups — "I guess it will be a
branch of that code." Work is happening on branch `residential-facade-cv` in
that repo, not in floodAPp itself.

## Status as of 2026-07-10 (one research round complete)

New module: `facade_cv_residential/analyze_stories_residential.py`. Validated
against a 6-building set (Wikipedia/NRHP-documented story counts + one real
homeowner photo) — **4/6 correct or close, vs 1/6 for the original H7 script
run unmodified on residential photos.** Full scoreboard, methodology, and a
caught-and-reverted regression (an eave-crop + edge-valley attempt that broke
a case the baseline got right) are in `facade_cv_residential/VALIDATION.md`.

Root cause of the original failure: H7's facade-top-boundary detection finds
the top of the ROOF (sky-texture detection), not the top of the WALL — fine
for flat/parapet-roofed commercial buildings, badly wrong for pitched
residential roofs (roofline read as extra floors, e.g. a real 2-story house
scored as 4 stories). Fix: detect the actual eave line, then count via
window-blob rows (not edge-valleys — edge signals are correlated and fail
together under the same roofline confound; window-blob detection is a
structurally independent signal). Fenestration % comes free from the same
blob pass.

## Known open gaps (not fixed yet)
- Full-width porches/entry roofs still produce false extra rows (their own
  mini-roofline confound, not yet masked).
- Tree-obstructed/angled photos are genuinely hard (foliage reads as windows).
- Eave detection itself has only one confirmed failure case caught (indirectly,
  by breaking a different signal) — not independently validated as reliable.
- **Building type/materials/age and damage severity have NO non-LLM
  implementation anywhere in this codebase.** Only geometric measurements
  (story count, fenestration %) are CV-derivable from a photo this way. Wiring
  this into floodAPp will cover fewer fields than the original LLM proxy did,
  not the same fields via a different method — do not imply parity to Becca.

## CLOSED (2026-07-15): not shipping into floodAPp
Decision: manual entry stays the only path in floodAPp for building info and
damage severity. Reasoning (full writeup: `overnight/v3-cv-build/DECISION.md`
on floodAPp main): the two remaining failure modes (porches, imperfect owner
photos) are common cases for floodAPp's actual users, not edge cases: real
accuracy on the live user base is likely well below 4/6. Also, story count
isn't valuable to automate even at high accuracy (homeowner already knows it
trivially) while the fields worth automating (materials/age/damage) have no
non-LLM path at all.

`residential-facade-cv` branch pushed to `github.com/rkn2/llmDamagev3`,
left as a research checkpoint (not deleted, not merged to that repo's main) —
may still be useful for the Montpelier pipeline itself. floodAPp's
`v3-computer-vision` branch also left unmerged/parked on GitHub as reference
code; only the one unrelated bugfix on it (chat FAB/severity button mobile
clipping) was cherry-picked to floodAPp main.

See also [[project-v3-cv-build]] (superseded LLM-proxy plan) [[project-structure]].
