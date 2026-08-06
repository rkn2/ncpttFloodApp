---
name: feedback-verify-platform-before-committing
description: "When a user names a specific language/runtime for a piece of infra, verify the chosen host actually supports it before building — don't assume compatibility"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 068ccfb5-c8ea-4e77-9996-ba29d67774ce
---

When a plan has already committed to a hosting platform (e.g. Netlify Functions) and
the user later specifies a language/runtime for that piece ("just use python for the
computer vision"), verify the platform actually supports that runtime before writing
any code — don't assume it does and don't silently try to force it. In the floodApp v3
CV build, Netlify Functions turned out to only support JavaScript/TypeScript/Go, no
Python, which wasn't discovered until directly WebFetching Netlify's own docs after
the instruction was given.

**Why:** Silently building on an incompatible platform wastes the whole session's work
once the mismatch surfaces at deploy time — much more costly than a two-minute doc
check up front. This is the same "gather evidence before building" discipline as
hypothesis-driven debugging, applied to infra choices rather than bug fixes.

**How to apply:** Whenever a request pins BOTH a platform and a language/runtime,
verify compatibility explicitly (WebFetch the platform's docs) before writing code.
If they conflict, pick a platform that supports what was asked rather than trying to
route around the constraint — in this case, moving the function from Netlify to Vercel
(which has first-class Python support and links to the same GitHub repo) was cleaner
than trying to shoehorn Python onto a JS-only host. Flag the pivot and the reasoning
clearly in whatever plan/handoff doc exists, since it changes deployment instructions
downstream (env var dashboard, deploy command, etc.).
