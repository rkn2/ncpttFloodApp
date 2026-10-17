#!/usr/bin/env python3
"""
hentf_inbox.py — add disasters to events-sources.json from FEMA-HENTF declaration emails.

FEMA-HENTF emails ("ACTION REQUESTED: Major Disaster Declaration ...", "UPDATE: Additional Counties
Added for DR-####-XX") reach Becca forwarded by Trish or Adam. Each new DR number found in one becomes
an entry in events-sources.json with the notice it came from; build_events.py then pulls the
counties from OpenFEMA and validates the number (typos such as "DR-4391-MP" are dropped there).

Reads mail through Becca's Graph app ("E5-Nap API", see ~/.claude/skills/outlook) with a SILENT
token only: if the cached sign-in can't supply one, it stops with the full error instead of
starting a device-code login (this runs unattended from launchd).

Usage (run from the bot clone, see pipeline/hentf-events-job.sh):
    uv run --with requests --with msal python3 pipeline/hentf_inbox.py [--dry-run]
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / 'events-sources.json'
API_ACCESS = '/Users/becca/Code/admin/general/api-access'
GRAPH = 'https://graph.microsoft.com/v1.0'
HENTF_ADDR = 'fema-hentf@fema.dhs.gov'
SUBJECT_RE = re.compile(r'declaration|DR-\d{4}|additional counties', re.I)
DR_RE = re.compile(r'\b(?:DR|EM)-(\d{4})\b')

ABBR = {'CNMI': 'MP'}
NAMES = {
    'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR', 'california': 'CA',
    'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE', 'florida': 'FL', 'georgia': 'GA',
    'hawaii': 'HI', 'idaho': 'ID', 'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS',
    'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD', 'massachusetts': 'MA',
    'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS', 'missouri': 'MO', 'montana': 'MT',
    'nebraska': 'NE', 'nevada': 'NV', 'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM',
    'new york': 'NY', 'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK',
    'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
    'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT', 'vermont': 'VT',
    'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV', 'wisconsin': 'WI', 'wyoming': 'WY',
    'puerto rico': 'PR', 'virgin islands': 'VI', 'guam': 'GU', 'american samoa': 'AS',
    'northern mariana islands': 'MP',
}
CODES = set(NAMES.values())


def token():
    sys.path.insert(0, API_ACCESS)
    import msal
    import test_graph_login as t
    cache = t.load_cache()
    app = msal.PublicClientApplication(
        t.CLIENT_ID, authority=f'https://login.microsoftonline.com/{t.TENANT_ID}', token_cache=cache)
    accounts = app.get_accounts()
    if not accounts:
        sys.exit('No cached Graph account. Sign in once interactively (see ~/.claude/skills/outlook).')
    r = app.acquire_token_silent_with_error(['Mail.ReadWrite'], account=accounts[0])
    t.save_cache(cache)
    if not r or 'access_token' not in r:
        sys.exit(f'Silent Graph token failed: {json.dumps(r)}')
    return r['access_token']


def states_named(subject, body):
    """State codes a notice names: DR-####-XX suffixes, plus state names/codes in the subject."""
    found = set(re.findall(r'\b(?:DR|EM)-\d{4}-([A-Z]{2,4})\b', subject + ' ' + body))
    found = {ABBR.get(s, s) for s in found}
    low = subject.lower()
    found |= {code for name, code in NAMES.items() if re.search(rf'\b{name}\b', low)}
    found |= {ABBR.get(w, w) for w in re.findall(r'\b([A-Z]{2,4})\b', subject) if ABBR.get(w, w) in CODES}
    return sorted(found & CODES)


def hentf_notices(tok):
    """FEMA-HENTF declaration emails in the mailbox, oldest first."""
    h = {'Authorization': f'Bearer {tok}', 'ConsistencyLevel': 'eventual',
         'Prefer': 'outlook.body-content-type="text"'}
    url = f'{GRAPH}/me/messages'
    params = {'$search': '"fema-hentf"', '$top': 50, '$select': 'subject,receivedDateTime,body,from'}
    out = []
    while url:
        r = requests.get(url, headers=h, params=params, timeout=60)
        if r.status_code != 200:
            sys.exit(f'Graph search failed: {r.status_code} {r.text}')
        d = r.json()
        for m in d['value']:
            body = m['body']['content']
            if HENTF_ADDR in body.lower() and SUBJECT_RE.search(m['subject']):
                out.append({'subject': m['subject'], 'date': m['receivedDateTime'][:10], 'body': body,
                            'from': m['from']['emailAddress']['name']})
        url, params = d.get('@odata.nextLink'), None
    return sorted(out, key=lambda m: m['date'])


def main():
    dry = '--dry-run' in sys.argv
    doc = json.loads(SOURCES.read_text()) if SOURCES.exists() else {'disasters': []}
    known = {int(d['disasterNumber']) for d in doc['disasters']}
    added = []
    for n in hentf_notices(token()):
        # Subject first: forwards carry long quoted threads that mention older disasters.
        nums = DR_RE.findall(n['subject']) or DR_RE.findall(n['body'])
        for num in dict.fromkeys(int(x) for x in nums):
            if num in known:
                continue
            known.add(num)
            entry = {'disasterNumber': num, 'notice': {
                'subject': re.sub(r'^(?:(?:re|fw|fwd)\s*:\s*)+', '', n['subject'], flags=re.I).strip(),
                'email_date': n['date'], 'forwarded_by': n['from'],
                'states_named': states_named(n['subject'], n['body'])}}
            doc['disasters'].append(entry)
            added.append(entry)
            print(f'  new: DR-{num} from "{entry["notice"]["subject"]}" ({n["date"]}, '
                  f'states named: {entry["notice"]["states_named"] or "none"})')
    if not added:
        print('  no new disasters in HENTF notices')
    elif not dry:
        doc['disasters'].sort(key=lambda d: d['notice']['email_date'])
        SOURCES.write_text(json.dumps(doc, indent=2) + '\n')
        print(f'  wrote {SOURCES.name} (+{len(added)})')
    # The job script reads this line to decide whether to rebuild and which task to file.
    print('ADDED ' + ' '.join(str(e['disasterNumber']) for e in added))


if __name__ == '__main__':
    main()
