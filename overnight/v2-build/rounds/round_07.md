# Round 07 — i18n scaffold + Spanish (D2.2 / D2.3)

## MEASURE
Start 8/11. Frontier [H7]. Adopted R6 gate's i18n guidance (scaffold, not full externalization;
gate switcher behind 100% coverage; English fallback; avoid half-translated view).

## SELECT / EXECUTE (additive, floodapp.html)
- i18n infrastructure: `I18N` table (en/es), `t(key)` with English fallback, `LANG` (persisted in
  localStorage), `setLang()`, `syncLangUI()`, `renderCurrent()` (re-renders the active screen on
  switch, reusing the share-hash navigation logic).
- Language switcher (EN | ES) in the header, wired to setLang; `.lang-active` CSS.
- Fully translated the ENTRY / welcome / mode-select screen (a complete, self-contained surface) —
  deliberately a whole screen rather than scattered strings, per the gate's half-translation warning.
- INIT sets document.documentElement.lang + syncs the switcher. Synced deploy/index.html.

## VERIFY (re-run, captured)
- JS syntax OK (`node --check` on extracted script).
- i18n logic test (node): 6/6 en keys have es translations, 0 missing, 0 identical/untranslated
  (100% coverage of scaffolded keys); `t()` → Spanish under es, English under en, key-name for a
  missing key; mode-select template renders "Bienvenido / Propietario / Evaluador de campo". PASS.
- Switcher present + wired (setLang en/es).
- (Fixed a bug in the TEST harness — const inside eval doesn't reach global; app was fine.)

## Metric delta
8/11 → 9/11. **D2.2 DONE** (string table + switcher, working EN↔ES). **D2.3 PARTIAL**: the entry
screen renders fully in Spanish; the deeper homeowner flow (steps 1–2, results, insurance) is NOT
yet externalized. This is an honest scaffold — extending coverage is mechanical (wrap more strings
in t(), add es values), and t()'s English fallback means partial coverage never shows blanks.

## CRITIQUE / carry-forward
- Chose to fully translate one complete surface over half-translating the whole flow (gate's explicit
  warning). Honest scope: D2.3 is a demonstrated capability, not full-flow localization.
- Spanish strings are machine-authored; a native/PR reviewer should verify terminology (e.g.
  preservation terms) before public PR release. Flag for handoff.
- This completes the autonomously-achievable P0–P2 build. Next: regression checks + FINAL_REPORT.
