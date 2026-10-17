# SHPO sync: one private map per disaster

```
FEMA-HENTF email (forwarded by DRI colleagues)
  └─ pipeline/hentf_inbox.py (daily, launchd)  → events-sources.json
       └─ pipeline/build_events.py (OpenFEMA counties + Census shapes) → events.json (published with the app)
Field app entry (assessor, or homeowner who checked "share")
  └─ tagged with its disaster (GPS county match, assessor confirms)
       └─ sync/intake.gs  (Apps Script, runs as Becca, anonymous POST)
            └─ "Flood app entries: DR-4933-IN" Google Sheet  (created on first entry, never auto-shared)
                 └─ sync/shpo-map.gs + shpo-map.html  (Apps Script, runs as the viewer)
                      └─ map page: only people the Sheet is shared with can open it
```

Why two Apps Script projects: the intake has to accept entries from phones with no login, so it runs
as Becca. If the map page ran there too, it would show every disaster to anyone with the link. The
map runs as the person viewing it, so Google's own Sheet sharing decides who sees what.

## Step 0: check Penn State allows it (10 minutes, do this first)

ArcGIS was ruled out because pages couldn't be shared. Google Workspace at Penn State may have similar
limits ("Anyone" web-app access, or sharing outside psu.edu). Before anything else:

1. Do step 1 below, then open the intake URL in a private browser window that is **not** signed in.
   You should see `{"status":"ok","message":"Flood app intake is live..."}`. A Google sign-in page
   instead means Penn State blocks anonymous web apps; use a personal Google account for both projects.
2. After step 2, share any test Sheet with a non-PSU address you control and open
   `<map URL>?sheet=<that Sheet's ID>` from that account. If sharing outside psu.edu is blocked,
   SHPO staff can't get in from a Penn State account either.
3. The first time any account opens the map, Google asks it to allow the script to *view* Sheets
   (read-only, plus the viewer's email address; the manifest in step 2 pins these),
   probably with a **"Google hasn't verified this app"** warning (Advanced → Go to Flood app SHPO map).
   The outside-account test must get past that screen. Warn SHPO staff to expect it once.

## Step 1: intake (once)

1. Create a Google Sheet named **Flood app intake (registry)**. It will hold the *Disasters* tab
   listing every disaster Sheet.
2. Extensions → Apps Script. Replace the default code with `sync/intake.gs`.
3. Optional: Project Settings → Script properties → `FOLDER_ID` = the ID of a Drive folder for the
   disaster Sheets (otherwise they land in My Drive). **Every disaster Sheet inherits that folder's
   sharing**, so use a folder shared with no one. If the folder is shared with a collaborator, or by
   link, every state's damaged buildings are shared with them too.
4. Deploy → New deployment → type **Web app**. Execute as: **Me**. Who has access: **Anyone**.
   Authorize it (it asks for Sheets, Drive and external requests: it reads the published events.json).
5. Copy the web app URL. Claude puts it in `SYNC_ENDPOINT` in `floodapp.html` and republishes the app.

## Step 2: SHPO map (once)

1. At script.google.com create a **new, separate** project named **Flood app SHPO map**.
2. Replace `Code.gs` with `sync/shpo-map.gs`. Add an HTML file named exactly `shpo-map` and paste
   `sync/shpo-map.html` into it.
   Then Project Settings → tick **Show "appsscript.json" manifest file in editor**, open
   `appsscript.json` and replace it with `sync/shpo-map.appsscript.json`. This limits the map to
   *reading* Sheets. Without it, Google infers full read/write access to all of each SHPO viewer's
   Sheets, because the map runs as them.
3. Deploy → New deployment → **Web app**. Execute as: **User accessing the web app**. Who has access:
   **Anyone with a Google account**.
4. Copy the URL. In the *intake* project: Script properties → `MAP_URL` = that URL. From then on the
   registry's *Map link* column has a ready link for each disaster.

## Each disaster

- The first entry tagged with a disaster creates its Sheet (*Flood app entries: DR-4933-IN*, with an
  *About* tab) and a row in the registry. Entries with no listed disaster go to *Unassigned*.
- When the daily job adds a new disaster it leaves a task in the vault. To give a SHPO access:
  open that disaster's Sheet → **Share** → add the SHPO/THPO staff as **Viewer** → send them the
  *Map link* from the registry. Note who in the registry's last column.
- SHPO staff need a Google account to open the map. A free one made with their work email is fine.
- A multi-state disaster has one Sheet per FEMA declaration (each DR number is one state), so each
  SHPO only ever sees its own state.

## Never

- **Never "Publish to web"** a disaster Sheet or the registry. It makes the data public to anyone with
  the link: a map of damaged historic buildings and archaeological material (NHPA §304 confidentiality).
- Never share the registry Sheet with a SHPO; it lists every disaster.
- Never share the *Unassigned* Sheet with a SHPO. It holds entries from every state that had no
  listed disaster. Move each entry to its disaster instead: the assessor picks the disaster on the
  phone and syncs again, and the intake moves the row (see below).

## What the intake accepts

| Entry | Stored when | Tab |
|---|---|---|
| Rapid triage | always | Rapid Triage |
| Full assessment | always | Full Assessment |
| Homeowner | only with a consent record (`shareConsent`: time, wording version `shpo-share-v1-2026-10-17`, language) | Homeowner |

A re-sent entry (edited on the phone and synced again) replaces its earlier row, matched on Entry ID.
If its disaster changed since the last sync (for example *Unassigned* → DR-4933-IN), the intake also
deletes its old row from the previous disaster's Sheet.
The intake replies `{"status":"ok","routedTo":"DR-4933-IN"}`; the app marks an entry synced only on
that reply and otherwise keeps it queued with the error.

## What an anonymous endpoint allows

Phones send entries with no login, so the intake can't tell who sent what. Accept these limits, or put
a sign-in in front of it later:

- **Anyone can add rows.** The disaster IDs are public in `events.json`, so a script could fill a real
  disaster's Sheet with fake buildings. Spot-check new rows before relying on a count, and watch for
  bursts in the *Submitted* column.
- **Anyone who sees an Entry ID can overwrite or move that row.** IDs are in column A of each Sheet and
  in every CSV export from the map, so a SHPO viewer, or anyone a CSV is forwarded to, can replace an
  assessment. Sheets keeps edit history (File → Version history), so a changed row can be restored.
- Formulas can't be planted: any cell starting with `=`, `+`, `-` or `@` is stored as text.
