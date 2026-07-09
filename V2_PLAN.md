# Historic Flood Recovery Tool — Critical Review & v2 Roadmap

*Prepared for internal review before sharing with program partners. Written in a deliberately skeptical, reviewer's voice — the goal is to surface every objection a grants panel or SHPO could raise **before** they do.*

---

## 1. Executive summary

The v1 prototype works and demonstrates the concept. But if a grants reviewer opens it next to the funded proposal, they will find one structural contradiction and several gaps that need to be closed — or knowingly re-scoped — before the tool can be defended as *the* innovation the grant describes.

The single most important thing in this document is a **reframe**, not a rebuild:

> The innovation is **not a runtime AI chatbot.** It is an **NLP knowledge-compilation pipeline** that turns a dozen-plus authoritative preservation and disaster documents into structured, *cited*, offline decision guidance — plus computer-vision-assisted building capture. The AI does the hard synthesis *at authoring time*, so the field user gets instant, trustworthy, connectivity-independent guidance.

This reframe matters because Becca's own instinct — *use the LLM heavily to build the app, but keep the runtime rule-based and offline* — is architecturally correct, yet on the surface it reads as **retreating from the grant's headline AI claim.** Framed as an authoring pipeline, it is actually *more* sophisticated than a chatbot, and it is fundable. This document makes that case and gives a phased plan to realize it.

**One flag for Becca to decide, not me:** if the grant's *written deliverables* promise a runtime AI assistant (a live chatbot the citizen talks to in the field), that language may need re-scoping before this plan goes out. That is a program-management call — but you need to see it now.

---

## 2. What v1 actually is today (accurate current state)

Being precise here matters, because it means **you are closer to your stated goal than it feels.**

| Component | Reality |
|---|---|
| **Delivery** | One self-contained `floodapp.html` (~2,500 lines) + a ~3 MB `knowledge-base.json`. No backend, no build step for the app itself. |
| **Two modes** | *Homeowner* (3 steps) and *Assessor* (Rapid Triage + Full Assessment). Both are structured questionnaires. |
| **Guidance engine** | **Already ~90% rule-based and deterministic.** `REPAIR_GUIDANCE`, `STATE_PROGRAMS`, `NATIONAL_PROGRAMS` are hardcoded JS objects keyed by damage category and state. No LLM involved in producing guidance. |
| **The *only* runtime LLM dependency** | The floating chat widget. It runs BM25 keyword search over the KB, then calls the Groq API for a chat completion. |
| **Knowledge base** | 14 authoritative PDFs in `docs/` — 13 unique (FEMA, NPS, THC, Historic England, NPS Preservation Brief 39, SOI Standards, etc.; two files are duplicate copies of the NTHP treatment guide) → `build-kb.py` → ~3,400 clean chunks with an IDF table for BM25. |
| **Persistence** | localStorage saves, JSON export, shareable base64 link. No server, no database, no audit trail. Forms output to Print. |
| **Coverage** | 3 states (VT, NC, PR). English only. |

**Takeaway:** v2 is *not* "convert the app to rule-based." It already is. v2 is: (a) formalize the rule content and give every recommendation a citation; (b) build the LLM authoring pipeline that *generates* that content from the corpus; (c) make the whole thing genuinely offline; (d) add computer vision. That's a much more credible story than "rewrite."

---

## 3. The central tension (the spine of everything below)

There are **two audiences**, and the design serves them in opposite directions:

- **The grants reviewer** — the proposal sells "NLP-driven, dynamic, real-time personalized guidance" as the innovation. They will look for AI.
- **The post-flood field user** — needs dead-simple, offline, trustworthy, low-effort guidance. A live chatbot is the *last* thing they can rely on with no cell signal and a flooded house.

The correct architecture optimizes for the field user (deterministic runtime, LLM at authoring time). The job of this document — and of the proposal language going forward — is to show that this **is** the NLP innovation, rigorously realized, not a walk-back from it.

---

## 4. Critical review — how a grants reviewer will read v1

These are ordered by how hard they are to wave away. The first five are anchored directly in your own requirement documents, so a reviewer cannot dismiss them as scope creep — they come from the grant.

### 4.1 🔴 The offline contradiction *(lead with this — it's the strongest)*
Your 6/24 notes state the app **must work offline** — "sometimes you don't have internet or cell in these areas after a flood." The one feature branded as "AI" is the chat widget, and here's the precise problem: the widget already *detects* offline and degrades gracefully (`sendChat` checks `navigator.onLine` and, when offline, shows the top matching source passages instead of calling the API — that fallback is already built). But what it falls back to is **raw, unsynthesized passage dumps** — snippets of dense preservation PDFs. The *LLM synthesis* — the part that turns those snippets into a plain-language, actionable answer — is **online-only.** So the headline "AI" capability is exactly the capability that disappears when the user has no signal, leaving a stressed homeowner with a flooded house to read raw document excerpts. State it that precisely — "synthesis is online-only, offline degrades to passage retrieval" — not "it fails offline," because a technical reviewer who knows the fallback exists would discount an overstated claim. This is still the critique that most cleanly motivates the whole v2 architecture, so it doubles as your thesis.

### 4.2 🔴 Provenance & liability
This is government-funded guidance about **structural repair of irreplaceable historic fabric.** The hand-authored do/don't lists are good, but most have **no traceable citation** — and the chatbot can *hallucinate* repair advice (e.g., inventing a mortar spec or a grant deadline). For a SHPO to point constituents at this (the stated Vermont use case), every recommendation needs a source cite to an authoritative document. Right now it's "trust us." That's a credibility and liability exposure.

### 4.3 🔴 The "NLP" gap — and an exposed API key
Today, "NLP" = BM25 keyword search + a Groq call whose **API key is embedded in client-side JavaScript** (anyone can view-source and steal it). That is not "extract and synthesize knowledge from documents to create personalized guidance," which is what the proposal claims. Name the gap honestly, then close it with the authoring pipeline (§5). The exposed key is also a concrete, cheap, do-it-now security fix (§6, P0).

### 4.4 🟠 Transferability is claimed but not built
The proposal claims adaptability "to diverse regional contexts, architectural styles, and regulations." In reality: **3 hardcoded states, English only, adding a region = hand-editing a JavaScript file.** Puerto Rico — an active partnership — needs Spanish. Where is the modularity that makes the transferability claim true? This becomes a v2 requirement: content as data, not code; i18n from the start.

### 4.5 🟠 The SHPO value proposition is unbuilt
The proposal says the tool helps SHPOs "more effectively allocate their limited resources." That requires **aggregating assessments** — a backend and a database so a SHPO can see, across a disaster, which historic buildings were hit and how badly. Today every assessment is trapped on one device and prints to paper. The SHPO-facing half of the value prop does not exist yet.

### 4.6 Reviewer must-haves you haven't addressed (they *will* ask)
- **Evaluation / validation plan.** How do you know the guidance is correct and that users succeed? The two PhD structural engineers + PR fieldwork are the obvious validation vehicle, but they are **not wired to the app** — there's no feedback capture, no telemetry, no field-test instrument. Reviewers *always* ask "how will you measure success?"
- **Novelty / anti-duplication.** The grant itself promises "not duplicating efforts," and your notes have **Esri** already doing damage classification. Pre-empt "why not just use Esri's or FEMA's app?" — the answer is: *historic-fabric-specific, offline, cited, and citizen-facing.* Say it explicitly.
- **Sustainability after the grant.** Who maintains the content when funding ends? The authoring pipeline **is** the answer: re-run it, don't hand-edit. Sell that as a feature.
- **Accessibility (Section 508 / WCAG).** Federally funded and citizen-facing → almost certainly required. Needs an explicit line and an audit. Post-disaster users skew older, stressed, on old phones and slow connections.

---

## 5. Target architecture for v2

The whole design is one idea: **push all the intelligence to authoring time; keep the runtime dumb, fast, offline, and cited.**

```
  ┌───────────────────────  AUTHORING TIME (online, LLM-heavy, you)  ───────────────────────┐
  │                                                                                          │
  │   docs/ (15+ authoritative PDFs)                                                          │
  │        │                                                                                  │
  │        ▼                                                                                  │
  │   NLP KNOWLEDGE-COMPILATION PIPELINE  (Python + LLM)                                       │
  │     • extract & clean text (existing build-kb.py, extended)                               │
  │     • LLM synthesizes structured, DECISION-READY guidance                                 │
  │     • every claim carries a CITATION back to source doc + page                            │
  │     • human-in-the-loop review/sign-off before publish                                    │
  │     • i18n: emit English + Spanish                                                         │
  │        │                                                                                  │
  │        ▼                                                                                  │
  │   content-bundle.json   (versioned, vetted, cited — the "compiled" knowledge)             │
  └────────────────────────────────────────┬─────────────────────────────────────────────────┘
                                            │  ships inside the app
  ┌─────────────────────────────────────────▼────────────────  RUN TIME (offline-first, no LLM)  ─┐
  │                                                                                                │
  │   PWA (installable, works with no signal)                                                       │
  │     • deterministic RULE ENGINE evaluates user answers → guidance (with citations)              │
  │     • CV-assisted capture: photo → typology / materials / damage suggestion (see §5.3)          │
  │     • forms + local save + export                                                               │
  │     • OPTIONAL "ask a question" — online: LLM over the bundle; offline: graceful cited-passage   │
  │        fallback (already exists)                                                                 │
  └─────────────────────────────────────────┬──────────────────────────────────────────────────────┘
                                            │  syncs when connectivity returns
  ┌─────────────────────────────────────────▼───────────────  SHPO BACKEND (online, aggregate)  ───┐
  │   assessments DB • dashboard • CV enrichment • evaluation telemetry • field-validation capture   │
  └──────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.1 The authoring pipeline — *this is the fundable innovation*
Extend `build-kb.py` into a real pipeline that doesn't just chunk text for search — it **compiles decision-ready guidance.** For each building system / damage type / scenario, an LLM reads the relevant source passages and emits a structured record: the recommendation, the do/don't, the "call a pro" trigger, the SOI-standard tie-in — **each with a citation to the source document and page.** A human reviewer (Simeon / APTI DRI) signs off before publish. Output is a versioned `content-bundle.json`.

This is what makes the "NLP" claim real *and* solves sustainability (re-run to update) *and* solves provenance (citations are first-class) *and* feeds transferability (regional bundles).

### 5.2 The runtime rule engine — "Python rules, compiled to the client"
You said "rule-based in Python." A Python *backend* contradicts the offline requirement. Resolve it this way: **author and test the rule engine in Python** (readable, testable, version-controlled decision logic), then **compile it to a client-side bundle** (data + a small JS evaluator) that ships inside the PWA and runs with no network. Python runs server-side **only** for CV and SHPO aggregation, which are inherently online. This gives you the developer experience you want *and* keeps the field app offline.

### 5.3 Computer vision — capture on device, enrich when online
Scope it concretely so it's fundable and not open-ended:
- **Building typology / architectural style / primary materials** from a façade photo (helps a stressed homeowner who doesn't know their building is "Italianate, brick, load-bearing masonry").
- **Damage classification & severity** from photos of affected areas → **auto-fills the assessment form** you already have.
- **Offline reconciliation:** the phone *captures* photos with GPS/time on device (works with no signal); CV *processing* happens on the server when connectivity returns, or via an on-device model for the high-value cases.
- **Tie it to the existing Esri thread** in your notes (Esri is already doing "automatic detection"). Framing CV as *partnership work with Esri* makes it fundable collaboration, not net-new technical risk you're carrying alone. This also directly answers the anti-duplication question.

### 5.4 SHPO aggregation backend
A lightweight server + database that receives synced assessments, dashboards them for a SHPO during a disaster, runs CV enrichment, and captures **evaluation telemetry + field-validation notes** (the PhD students in PR are the data source). This builds the second half of the value proposition and the evaluation plan at the same time.

---

## 6. Phased roadmap

Each phase ends in a milestone you can *demo or report* to the funder. Ordered by dependency: authoring pipeline before CV; offline before field deployment. Relative sizes below are rough and meant only to help slot phases into budget periods — not commitments.

### P0 — Credibility fixes *(days — do now)*
- **Kill the exposed API key.** Move the Groq call behind a tiny backend proxy (or disable the online chat until it exists). No secrets in client JS.
- **Add citations to the *existing* hardcoded guidance** by hand — even before the pipeline exists. Instantly upgrades trustworthiness.
- *Milestone:* a version you can safely deploy publicly and defend on provenance.

### P1 — The NLP authoring pipeline *(the headline deliverable — small-to-medium; fits grant year 1)*
- Extend `build-kb.py` → compile structured, cited guidance from the documents already in `docs/`.
- Human review/sign-off step. Versioned `content-bundle.json`. Runtime reads the bundle instead of hardcoded objects.
- *Milestone:* "Our NLP pipeline synthesized N authoritative documents into M cited guidance records, reviewed and signed off by APTI DRI." **This is the sentence that makes the grant's innovation real.**

### P2 — True offline + internationalization *(medium; year 1–2)*
- Convert to an installable **PWA** (service worker, cached bundle, works with zero signal).
- i18n scaffold; produce **Spanish** for Puerto Rico via the pipeline.
- Content-as-data so a new region is a bundle, not a code edit (delivers the transferability claim).
- *Milestone:* installable app that runs fully offline in English and Spanish — demoable to PR SHPO.

### P3 — Computer vision *(medium-to-large; year 2, Esri-dependent)*
- Typology/materials from façade photos; damage classification → form auto-fill; capture-now/process-later.
- Esri collaboration for detection/classification.
- *Milestone:* photograph a building → draft assessment pre-filled. Strong live demo + partnership deliverable.

### P4 — SHPO backend + evaluation *(large; year 2, runs alongside PR fieldwork)*
- Assessment sync, DB, SHPO dashboard, CV enrichment.
- Evaluation telemetry + field-validation instrument; validate with the PhD students in PR.
- *Milestone:* a SHPO sees aggregated post-disaster assessments; you have quantitative evidence the tool works (your evaluation plan, executed).

---

## 7. Decisions needed (my recommendations, your call)

| Decision | Recommendation | Why / tradeoff |
|---|---|---|
| **Platform: PWA vs native iOS vs both** | **PWA-first** | One codebase, installable, offline-capable, works on any phone, and it's the cheapest path to the transferability the grant promises. Native iOS costs a second codebase + App Store friction for marginal gain. Your 6/24 notes explicitly left this open ("we can talk through that") — worth a real conversation, but PWA is the defensible default. |
| **"Rule-based in Python" vs offline** | Author/test rules in Python; **compile to a client bundle** for the PWA | Gives you the Python DX you want without breaking offline. Python stays server-side for CV + aggregation only. |
| **CV scope** | Typology + damage-to-form-autofill, framed as **Esri partnership** | Concrete, demoable, and reframes technical risk as funded collaboration + anti-duplication answer. |
| **Runtime chatbot** | Keep as *optional*, online-only, cited; offline falls back to passage retrieval (already built) | Preserves the "ask a question" affordance without making it the critical path — and forces the proposal-language check in §1. |

---

## 8. Crosswalk — v2 vs the grant's promises

Hand this to a reviewer to show every proposal claim has a home in the plan.

| Proposal language | v1 today | v2 plan |
|---|---|---|
| "Leverages NLP to extract & synthesize knowledge from documents" | BM25 search + chatbot | **Authoring pipeline** compiles cited guidance from the corpus (P1) |
| "Real-time, personalized guidance based on user inputs" | Rule-based guidance by damage/state | Same, expanded + cited; CV personalizes capture (P1, P3) |
| "Works offline after a flood" | ⚠️ forms work; AI *synthesis* is online-only (offline = raw passage dumps) | **PWA, fully offline** (P2) |
| "Adaptable to diverse regional contexts / architectural styles / regulations" | 3 hardcoded states, English | Content-as-data, regional bundles, **Spanish** (P2) |
| "Helps SHPOs allocate limited resources" | ❌ prints to paper | **Aggregation backend + dashboard** (P4) |
| "Not duplicating efforts" | — | **Esri partnership** for CV; historic-specific niche (P3) |
| *(implicit reviewer demand)* Evaluation | ❌ none | **Telemetry + PR field validation** (P4) |
| *(implicit)* Sustainability | ❌ hand-edited | **Re-runnable pipeline** (P1) |
| *(implicit)* Accessibility / 508 | not audited | WCAG audit in P2 |

---

*Prepared 2026-07-08. Current state verified against `floodapp.html`, `build-kb.py`, `docs/`, and the 5/1 and 6/24 vision notes.*
