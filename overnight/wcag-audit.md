# WCAG / Section 508 Accessibility Audit — Historic Flood Recovery Tool

*Audited 2026-08-31 against floodapp.html (deployed at rkn2.github.io/ncpttFloodApp). Manual code review — axe-cli could not run due to ChromeDriver version mismatch. Covers WCAG 2.1 AA (the standard for federally funded, citizen-facing web applications under Section 508).*

---

## Critical (blocks access for some users)

### 1. Interactive `<div>` elements not keyboard accessible
**WCAG 2.1.1 (A) — Keyboard**, **4.1.2 (A) — Name, Role, Value**

Multiple interactive `<div>` elements use `onclick` but have no `role="button"`, `tabindex="0"`, or `onkeydown` handler. Keyboard-only and screen reader users cannot activate them.

| Element | Location | Fix |
|---|---|---|
| Mode selector buttons (Homeowner/Assessor) | `showModeSelect()`, `showAssessorSubmode()` | Change to `<button>` or add `role="button" tabindex="0"` + Enter/Space keydown |
| Result panel expand headers (Assistance, Insurance, Repair) | `showHwResults()` | Same |
| Guidance card expand headers | `showHwResults()` guidance cards | Same |

### 2. Dynamic content not announced to screen readers
**WCAG 4.1.3 (AA) — Status Messages**

The `#screens` container is replaced entirely on each step transition. There is no `aria-live` region, so screen readers don't announce when the page content changes (e.g., moving from Safety to Building Info). Users hear nothing when clicking "Next."

**Fix:** Add `aria-live="polite"` to `#screens`, or manage focus to the new heading after each screen change (call `.focus()` on the new `<h2>` with `tabindex="-1"`).

### 3. Focus outline suppressed
**WCAG 2.4.7 (AA) — Focus Visible**

`outline: none` on `select:focus, input:focus, textarea:focus` (line 167) and `#saves-name-input` (line 658). Keyboard users lose track of which element is focused.

**Fix:** Replace `outline: none` with a custom focus style: `outline: 2px solid var(--hw-accent); outline-offset: 2px;` or use `:focus-visible` to only hide outlines for mouse users.

### 4. Severity modal not focus-trapped
**WCAG 2.4.3 (A) — Focus Order**

The severity info modal (`.sev-modal-overlay`) can be opened but Tab will move focus to elements behind the overlay. No focus trap, no Escape key handler, and focus is not moved into the modal on open.

**Fix:** On open, move focus to the modal. Trap Tab within the modal (first/last focusable element wraps). Close on Escape. Return focus to trigger on close.

---

## Serious (significant barrier)

### 5. Color contrast failures (WCAG 1.4.3 AA — 4.5:1 for normal text)

| Element | Foreground | Background | Ratio | Required | Fix |
|---|---|---|---|---|---|
| **Homeowner primary button** | #FFF | #C4884A | 3.0:1 | 4.5:1 | Darken to #9A6930 or similar |
| **Field hint text** | #888 | #FFF | 3.5:1 | 4.5:1 | Darken to #767676 |
| **Severity "moderate"** | #E65100 | #FFF3E0 | 3.5:1 | 4.5:1 | Darken to #BF4400 |
| **Step dot inactive** | #AAA | #FFF | 2.3:1 | 4.5:1 | Darken to #767676 |
| **Progress bar track** | #DDD | #FFF | 1.4:1 | 3:1 (UI) | Darken to #949494 (or accept as decorative) |

### 6. No landmark roles
**WCAG 1.3.1 (A) — Info and Relationships**, **2.4.1 (A) — Bypass Blocks**

No `<main>`, `<nav>`, `<header>`, `<footer>`, or `<aside>` elements. No skip-to-content link. Screen reader users have no way to orient or skip past the header/progress bar.

**Fix:**
- Wrap `#app-header` in a `<header>` (or add `role="banner"`)
- Wrap `#screens` in `<main>` (or add `role="main"`)
- Add a skip link: `<a href="#screens" class="sr-only focus-visible">Skip to content</a>` as the first element in `<body>`

### 7. Language attribute not switching for full-page content
**WCAG 3.1.2 (AA) — Language of Parts**

`setLang()` correctly sets `document.documentElement.lang = l`, which is good. However, the assessor mode always renders in English even when `lang="es"` is set. This could confuse screen readers that would switch to Spanish pronunciation.

**Fix:** Either set `lang` only for the homeowner content region, or translate assessor chrome minimally (button labels, headers).

### 8. External links open in new tabs without warning
**WCAG 3.2.5 (AAA, but good practice) / usability**

Three `target="_blank"` links open in new windows with no screen reader warning.

**Fix:** Add `<span class="sr-only">(opens in new tab)</span>` after link text, or add `aria-label` that includes the warning.

---

## Moderate

### 9. Touch target sizes below WCAG 2.5.8 (AA) minimum of 24×24px
**WCAG 2.5.5 (AAA) recommends 44×44px; 2.5.8 (AA) requires 24×24px**

| Element | Approx size | Fix |
|---|---|---|
| Severity buttons (desktop) | ~24px tall | Increase padding to 6px 10px (min 32px) |
| Save item Load/Delete buttons | ~22px tall | Increase padding to 6px 12px |
| Language switcher EN/ES | ~20px tall | Increase padding to 6px 10px |
| Export/Share buttons | OK at 28px | Near minimum but acceptable |

Post-disaster users on phones with wet/gloved hands — larger targets help everyone.

### 10. Form inputs lack explicit `<label>` associations
**WCAG 1.3.1 (A) — Info and Relationships**

Form inputs use a preceding `<label class="field-label">` but the `<label>` elements don't have a `for` attribute matching the input's `id`. Screen readers may not associate the label with the input.

**Fix:** Add `for="hw-address"` to the label, matching the input's `id`. All dynamically-generated inputs need this treatment.

The `#saves-name-input` has no associated label at all (just a placeholder).

### 11. Checkbox/radio groups lack `<fieldset>` + `<legend>`
**WCAG 1.3.1 (A)**

Groups of checkboxes (materials, designations, historic status, hazards) and radio buttons (posting, sediment, erosion) are not wrapped in `<fieldset>` with a `<legend>`. Screen reader users hear each individual option but not the group question.

**Fix:** Wrap each group in `<fieldset>` with a `<legend>` containing the question text. Hide the `<legend>` visually if the `field-label` is preferred.

### 12. Emoji used as the sole content indicator
**WCAG 1.1.1 (A) — Non-text Content**

Several UI elements rely on emoji as the primary or sole indicator:
- `📍` on the locate button (has text label — OK)
- `💾` Saves, `❓` Quick Answers, `📄` citation tooltips
- Walkthrough option icons (✅, 🚨, ⚠️, 🦠) — these supplement text labels (OK)
- `📚` source note prefix — decorative (OK)

The `📄` citation hover markers are emoji-only with no text label. A screen reader user would hear "page facing up" or nothing, not "citation."

**Fix:** Add `aria-label="Citation"` or `aria-hidden="true"` with a text alternative on citation spans.

---

## Minor

### 13. `confirm()` and `alert()` are not accessible dialogs
Calls to `confirm()` and `alert()` (safety step, state validation) use native browser dialogs which are technically accessible but jarring and cannot be styled. Not a WCAG violation but a usability concern — consider inline validation messages instead.

### 14. Print stylesheet doesn't show collapsed sections
The print stylesheet forces `.guidance-card-body` and `.result-panel-body` to display, which is correct. But the `#step-indicator` and `#app-header` are hidden in print, which removes context about which assessment this is. Consider keeping the building name and address visible in print.

### 15. `title` attribute on citation tooltips
Citations use `title` attributes for hover quotes. These are not accessible on touch devices (no hover) and are not announced by most screen readers. The information is secondary (the recommendation itself is visible), so this is low-impact, but consider a tap-to-reveal pattern for mobile.

### 16. `autocomplete` attributes missing
**WCAG 1.3.5 (AA) — Identify Input Purpose**

Text fields for name, address, and date lack `autocomplete` attributes. Adding them helps browsers auto-fill and benefits users with cognitive disabilities.

**Fix:** Add `autocomplete="name"` to inspector name, `autocomplete="street-address"` to address fields, etc.

---

## Summary

| Severity | Count | WCAG Level |
|---|---|---|
| Critical | 4 | A, AA |
| Serious | 4 | A, AA, AAA |
| Moderate | 4 | A, AA |
| Minor | 4 | AA, best practice |

**Top 3 fixes by impact:**
1. Make interactive `<div>` elements keyboard-accessible (change to `<button>` or add role+tabindex+keydown)
2. Add `aria-live` or focus management to `#screens` so screen transitions are announced
3. Fix the 5 color contrast failures (especially the homeowner primary button at 3.0:1)
