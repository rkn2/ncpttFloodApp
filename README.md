# Historic Flood Recovery Tool

A web-based prototype to guide homeowners, renters, and preservation professionals through post-flood assessment and recovery for historic buildings. Built on the Secretary of the Interior's Standards for Rehabilitation and APTI Disaster Response Initiative expertise.

## Running the app

The app is a single HTML file. Because it fetches a local JSON file, you must serve it over HTTP rather than opening it directly in a browser:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/floodapp.html`.

## Building the knowledge base (required for the chat widget)

The RAG chat widget needs a `knowledge-base.json` built from the source documents in `docs/`. This file is not committed to the repo — you must generate it locally.

**1. Install dependencies**

```bash
brew install poppler        # provides pdftotext
pip install -r requirements.txt
```

**2. Add source documents**

Drop any `.pdf`, `.txt`, `.docx`, or `.md` files into the `docs/` folder. The two reference documents are already there.

**3. Build**

```bash
python3 build-kb.py
```

Re-run this any time you add or update files in `docs/`.

## Chat widget

The chat widget uses [Groq](https://console.groq.com) to generate responses. To enable it, replace the placeholder API key in `floodapp.html`:

```js
const GROQ_API_KEY = 'gsk_PASTE_YOUR_KEY_HERE';  // line ~1955
```

> **Note:** Storing an API key directly in client-side JavaScript is insecure and should only be used for local development/prototyping. A backend proxy is needed before any public deployment.
