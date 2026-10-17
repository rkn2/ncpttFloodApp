#!/usr/bin/env python3
"""
build_events.py — build events.json (declared disasters + their counties) for the field app.

Which disasters: the ones listed in events-sources.json. Each entry records the HENTF notice that
put it there (pipeline/hentf_inbox.py adds them from FEMA-HENTF emails Trish forwards).
What counties: FEMA's OpenFEMA DisasterDeclarationsSummaries v2 (the authoritative designations;
it matched the DR-4933-IN HENTF email exactly). County shapes: Census cartographic boundary file
(cb_<year>_us_county_5m), simplified, so the app can match a GPS point to a county offline.

Validation (an email can contain a typo, e.g. "DR-4391-MP" for 4931): a DR number is kept only if
OpenFEMA knows it, its state is one the notice names, and it was declared within MAX_AGE_DAYS before
the notice. Anything dropped is printed with the reason, never guessed.

Usage:
    uv run --with pyshp python3 pipeline/build_events.py            # writes events.json + deploy/events.json
    uv run --with pyshp python3 pipeline/build_events.py --check    # validate only, write nothing
"""

import json
import math
import sys
import urllib.parse
import urllib.request
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / 'events-sources.json'
OUTPUTS = [ROOT / 'events.json', ROOT / 'deploy' / 'events.json']
CACHE = Path.home() / '.cache' / 'floodapp'
CENSUS_YEAR = 2024
CENSUS_URL = f'https://www2.census.gov/geo/tiger/GENZ{CENSUS_YEAR}/shp/cb_{CENSUS_YEAR}_us_county_5m.zip'
OPENFEMA = 'https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries'
MAX_AGE_DAYS = 400          # a notice about a declaration older than this is treated as a typo
SIMPLIFY_DEG = 0.002        # ~200 m; plenty to tell counties apart, keeps the file small

STATE_NAMES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois',
    'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
    'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
    'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia',
    'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
    'PR': 'Puerto Rico', 'VI': 'Virgin Islands', 'GU': 'Guam', 'AS': 'American Samoa',
    'MP': 'Northern Mariana Islands',
}


def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'ncpttFloodApp build_events.py'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def openfema_rows(dr):
    """All designation rows for one disaster, paged (a statewide declaration can exceed one page)."""
    rows, skip, top = [], 0, 1000
    while True:
        q = urllib.parse.urlencode({'$filter': f'disasterNumber eq {dr}', '$top': top, '$skip': skip,
                                    '$inlinecount': 'allpages'})
        d = fetch_json(f'{OPENFEMA}?{q}')
        page = d.get('DisasterDeclarationsSummaries', [])
        rows += page
        total = d.get('metadata', {}).get('count')
        if len(page) < top:
            break
        skip += top
    if total is not None and total != len(rows):
        raise RuntimeError(f'DR-{dr}: OpenFEMA said {total} rows, got {len(rows)}')
    return rows


def day(s):
    return s[:10] if s else None


def validate(dr, rows, notice):
    """Return None if the DR number is consistent with its HENTF notice, else the reason it isn't."""
    if not rows:
        return 'not in OpenFEMA'
    st = rows[0]['state']
    named = notice.get('states_named') or []
    if named and st not in named:
        return f'OpenFEMA state {st} is not one the notice names ({", ".join(named)})'
    declared = date.fromisoformat(day(rows[0]['declarationDate']))
    noticed = date.fromisoformat(notice['email_date'])
    age = (noticed - declared).days
    if age < -7 or age > MAX_AGE_DAYS:
        return f'declared {declared}, {age} days before the {noticed} notice'
    return None


# ── county shapes ──────────────────────────────────────────────────────────
def census_shapes():
    CACHE.mkdir(parents=True, exist_ok=True)
    z = CACHE / Path(CENSUS_URL).name
    if not z.exists():
        print(f'  downloading {CENSUS_URL}')
        urllib.request.urlretrieve(CENSUS_URL, z)
    out = CACHE / z.stem
    if not out.exists():
        zipfile.ZipFile(z).extractall(out)
    import shapefile  # pyshp
    sf = shapefile.Reader(str(next(out.glob('*.shp'))))
    fields = [f[0] for f in sf.fields[1:]]
    shapes = {}
    for sr in sf.iterShapeRecords():
        rec = dict(zip(fields, sr.record))
        shapes[rec['GEOID']] = sr.shape
    return shapes


def _perp(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return math.hypot(x - x1, y - y1)
    return abs(dy * x - dx * y + x2 * y1 - y2 * x1) / math.hypot(dx, dy)


def simplify(pts, tol):
    """Douglas-Peucker (iterative)."""
    if len(pts) < 4:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        dmax, idx = 0, None
        for k in range(i + 1, j):
            d = _perp(pts[k], pts[i], pts[j])
            if d > dmax:
                dmax, idx = d, k
        if idx is not None and dmax > tol:
            keep[idx] = True
            stack += [(i, idx), (idx, j)]
    return [p for p, k in zip(pts, keep) if k]


def rings(shape):
    """Shapefile parts -> list of simplified rings [[lon, lat], ...] rounded to 4 decimals."""
    parts = list(shape.parts) + [len(shape.points)]
    out = []
    for a, b in zip(parts, parts[1:]):
        r = simplify(shape.points[a:b], SIMPLIFY_DEG)
        if len(r) >= 4:
            out.append([[round(x, 4), round(y, 4)] for x, y in r])
    return out


# ── main ───────────────────────────────────────────────────────────────────
def main():
    check_only = '--check' in sys.argv
    sources = json.loads(SOURCES.read_text())
    shapes = None if check_only else census_shapes()
    events, county_shapes, dropped, unmatched = [], {}, [], []

    for src in sources['disasters']:
        dr = int(src['disasterNumber'])
        rows = openfema_rows(dr)
        why = validate(dr, rows, src['notice'])
        if why:
            dropped.append(f'DR-{dr}: {why} (notice "{src["notice"]["subject"]}")')
            continue
        r0 = rows[0]
        kind = r0.get('declarationType', 'DR')
        counties = []
        for r in sorted(rows, key=lambda r: r['designatedArea']):
            fips = r['fipsStateCode'] + r['fipsCountyCode']
            c = {'name': r['designatedArea'], 'fips': fips,
                 'pa': bool(r.get('paProgramDeclared')), 'ia': bool(r.get('ihProgramDeclared'))}
            if r['fipsCountyCode'] == '000':
                c['statewide'] = True          # statewide or tribal designation: match by state
            counties.append(c)
            if shapes is not None and r['fipsCountyCode'] != '000' and fips not in county_shapes:
                if fips in shapes:
                    county_shapes[fips] = rings(shapes[fips])
                else:
                    unmatched.append(f'{kind}-{dr}-{r0["state"]} {r["designatedArea"]} ({fips})')
        events.append({
            'id': f'{kind}-{dr}-{r0["state"]}',
            'disasterNumber': dr,
            'type': kind,
            'state': r0['state'],
            'stateName': STATE_NAMES.get(r0['state'], r0['state']),
            'title': r0['declarationTitle'].title(),
            'incidentType': r0.get('incidentType'),
            'declarationDate': day(r0['declarationDate']),
            'incidentBegin': day(r0.get('incidentBeginDate')),
            'incidentEnd': day(r0.get('incidentEndDate')),
            'femaUrl': f'https://www.fema.gov/disaster/{dr}',
            'openfemaRefresh': day(max(r['lastRefresh'] for r in rows)),
            'hentfNotice': src['notice']['email_date'],
            'counties': counties,
        })
        print(f'  {events[-1]["id"]}: {len(counties)} areas, declared {events[-1]["declarationDate"]}')

    for d in dropped:
        print(f'  DROPPED {d}')
    for u in unmatched:
        print(f'  NO SHAPE {u} (app falls back to state-level matching)')
    if check_only:
        return
    events.sort(key=lambda e: e['declarationDate'], reverse=True)
    doc = {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'note': 'Declared disasters the app can tag entries with. Designations from OpenFEMA '
                'DisasterDeclarationsSummaries v2; county shapes from the Census '
                f'cb_{CENSUS_YEAR}_us_county_5m file, simplified. Built by pipeline/build_events.py '
                'from events-sources.json. Used for tagging and routing only, not shown as guidance.',
        'events': events,
        'county_shapes': county_shapes,
        'dropped': dropped,
    }
    text = json.dumps(doc, separators=(',', ':'), ensure_ascii=False)
    for out in OUTPUTS:
        old = out.read_text() if out.exists() else None
        # Only generated_at changed -> leave the file alone so the daily job doesn't commit noise.
        if old and json.loads(old) | {'generated_at': ''} == doc | {'generated_at': ''}:
            continue
        out.write_text(text)
        print(f'  wrote {out.relative_to(ROOT)} ({len(text) // 1024} KB)')


if __name__ == '__main__':
    main()
