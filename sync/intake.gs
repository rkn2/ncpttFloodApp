// Intake — receives entries from the field app and files each into its disaster's own Sheet.
//
// This is the ANONYMOUS endpoint (the field app has no login), so it only ever writes:
//   - doPost appends/updates rows; doGet returns a status line, never data.
//   - A new disaster Sheet is created only for an event id listed in the published events.json
//     (anything else goes to the "Unassigned" Sheet), so nobody can create Sheets at will.
//   - Homeowner entries without a consent record are rejected (the app only sends them when the
//     owner checks "share with the SHPO").
//   - Nothing is ever shared automatically. Sharing a disaster's Sheet with the SHPO is Becca's step.
// The SHPO-facing map is a SEPARATE Apps Script project (sync/shpo-map.gs) that runs as the person
// viewing it, so Sheet sharing is the access control. Setup: sync/README.md.

const EVENTS_URL = 'https://rkn2.github.io/ncpttFloodApp/events.json';
const UNASSIGNED = 'UNASSIGNED';
const REGISTRY_TAB = 'Disasters';
const REGISTRY_HEADERS = ['Event ID', 'Title', 'State', 'Declared', 'Sheet URL', 'Sheet ID', 'Created',
                          'Map link (share with SHPO staff)', 'Shared with (fill in by hand)'];

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents);
    const data = payload.data || {};
    const as = data.as || {}, hw = data.hw || {};
    let kind;
    if (data.mode === 'assessor' && as.submode === 'rapid') kind = 'rapid';
    else if (data.mode === 'assessor' && as.submode === 'full') kind = 'full';
    else if (data.mode === 'homeowner') kind = 'homeowner';
    else return reply({ status: 'error', message: 'unknown entry type' });
    if (kind === 'homeowner' && !(hw.shareConsent && hw.shareConsent.version && hw.shareConsent.at)) {
      return reply({ status: 'error', message: 'homeowner entry without share consent' });
    }

    const wanted = (kind === 'homeowner' ? hw.event : as.event) || '';
    const ev = listedEvents()[wanted];
    const lock = LockService.getScriptLock();
    lock.waitLock(20000);   // find-or-create + upsert must not interleave
    try {
      const ss = eventSpreadsheet(ev ? wanted : UNASSIGNED, ev);
      const row = kind === 'rapid' ? rapidRow(payload, as) : kind === 'full' ? fullRow(payload, as) : homeownerRow(payload, hw);
      upsert(ss, row.tab, row.headers, row.values, payload.id || '');
      return reply({ status: 'ok', routedTo: ev ? wanted : UNASSIGNED });
    } finally {
      lock.releaseLock();
    }
  } catch (err) {
    console.error(err && err.stack || err);
    return reply({ status: 'error', message: String(err && err.message || err) });
  }
}

function doGet() {
  return reply({ status: 'ok', message: 'Flood app intake is live. This endpoint only accepts entries.' });
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// Event ids from the published events.json, cached for an hour.
function listedEvents() {
  const cache = CacheService.getScriptCache();
  const hit = cache.get('events');
  if (hit) return JSON.parse(hit);
  const res = UrlFetchApp.fetch(EVENTS_URL, { muteHttpExceptions: true });
  if (res.getResponseCode() !== 200) throw new Error('events.json fetch failed: HTTP ' + res.getResponseCode());
  const out = {};
  JSON.parse(res.getContentText()).events.forEach(ev => {
    out[ev.id] = { title: ev.title, state: ev.state, declared: ev.declarationDate };
  });
  cache.put('events', JSON.stringify(out), 3600);
  return out;
}

// The registry lives in the Sheet this script is bound to: one row per disaster Sheet.
function eventSpreadsheet(eventId, ev) {
  const master = SpreadsheetApp.getActiveSpreadsheet();
  let reg = master.getSheetByName(REGISTRY_TAB);
  if (!reg) {
    reg = master.insertSheet(REGISTRY_TAB);
    reg.appendRow(REGISTRY_HEADERS);
    reg.getRange(1, 1, 1, REGISTRY_HEADERS.length).setFontWeight('bold');
    reg.setFrozenRows(1);
  }
  const rows = reg.getDataRange().getValues();
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] === eventId) return SpreadsheetApp.openById(rows[i][5]);
  }
  const title = eventId === UNASSIGNED ? 'Flood app entries: Unassigned' : 'Flood app entries: ' + eventId;
  const ss = SpreadsheetApp.create(title);
  const folderId = PropertiesService.getScriptProperties().getProperty('FOLDER_ID');
  if (folderId) DriveApp.getFileById(ss.getId()).moveTo(DriveApp.getFolderById(folderId));
  const about = ss.getSheets()[0].setName('About');
  about.getRange(1, 1, 6, 2).setValues([
    ['Event ID', eventId],
    ['Title', ev ? ev.title : 'Entries with no listed disaster'],
    ['State', ev ? ev.state : ''],
    ['Declared', ev ? ev.declared : ''],
    ['Created', new Date().toISOString()],
    ['Confidential', 'Locations of damaged historic buildings and archaeological material. Share only with the SHPO/THPO staff who need it (NHPA §304). Do not publish to the web.'],
  ]);
  const mapBase = PropertiesService.getScriptProperties().getProperty('MAP_URL') || '';
  reg.appendRow([eventId, ev ? ev.title : '', ev ? ev.state : '', ev ? ev.declared : '',
                 ss.getUrl(), ss.getId(), new Date().toISOString(),
                 mapBase ? mapBase + '?sheet=' + ss.getId() : '(set MAP_URL script property)', '']);
  return ss;
}

// One row per field entry: a re-sent (edited) entry replaces its earlier row, matched on Entry ID.
function upsert(ss, tab, headers, values, entryId) {
  headers = ['Entry ID'].concat(headers);
  values = [entryId].concat(values);
  let sheet = ss.getSheetByName(tab);
  if (!sheet) {
    sheet = ss.insertSheet(tab);
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  if (entryId && sheet.getLastRow() > 1) {
    const ids = sheet.getRange(2, 1, sheet.getLastRow() - 1, 1).getValues();
    for (let i = 0; i < ids.length; i++) {
      if (ids[i][0] === entryId) { sheet.getRange(i + 2, 1, 1, values.length).setValues([values]); return; }
    }
  }
  sheet.appendRow(values);
}

function rapidRow(payload, as) {
  const rd = as.rapidDamage || {};
  return { tab: 'Rapid Triage', headers: [
    'Submitted', 'Synced From', 'Event', 'Inspector', 'Affiliation', 'Date', 'Area Inspected', 'Area/Event',
    'Building Name', 'Address', 'GPS',
    'Stories', 'Footprint', 'Units', 'Age', 'Construction Type', 'Occupancy',
    'Foundation', 'Roof Shape', 'Roof Covering', 'Wall Finish',
    'Historic Status',
    'Water Nature', 'Water Depth', 'Sediment', 'Erosion',
    'Collapsed/Off Foundation', 'Structural', 'Roof Dmg', 'Siding', 'Windows', 'Chimney',
    'Electrical', 'Insulation', 'Interior', 'Mold',
    'Overall Damage', 'Occupied', 'Repairs Begun', 'Posting', 'Recommend Full?', 'Trigger Reasons', 'Notes'
  ], values: [
    payload.queuedAt || new Date().toISOString(),
    payload.name || '', as.event || '',
    as.inspector, as.affiliation, as.date, as.areaInspected, as.area,
    as.buildingName, as.address, (as.gps || []).filter(Boolean).join('; '),
    as.stories, as.footprint, as.units, as.age, as.constructionType, as.occupancy,
    as.foundation, as.roof, as.roofCovering, as.wallFinish,
    (as.historicStatus || []).join(', '),
    (as.waterNature || []).join(', '), (as.waterDepth || []).join(', '), as.sediment, as.erosion,
    rd.collapsed || '', rd.structural || '', rd.roof || '', rd.siding || '', rd.windows || '', rd.chimney || '',
    rd.electrical || '', rd.insulation || '', rd.interior || '', rd.mold || '',
    as.overallDamage, as.occupied, as.repairsBegun, as.posting, as.recommendFull ? 'Yes' : 'No',
    (as.triggerReasons || []).join(', '), as.notes
  ] };
}

function fullRow(payload, as) {
  const ed = as.exteriorDamage || {};
  const id = as.interiorDamage || {};
  const extCats = [
    'Foundation', 'Basement walls', 'Exterior walls', 'Roof structure',
    'Roofing material', 'Chimneys', 'Porches / balconies', 'Windows',
    'Doors', 'Exterior trim', 'Siding / cladding', 'Paint / coatings',
    'Drainage / gutters', 'Steps / walkways', 'Fencing',
    'Site features (walls, fountains, pools)'
  ];
  const intCats = [
    'Ceiling structure / finish', 'Floor structure', 'Floor covering',
    'Interior walls / plaster', 'Stairways', 'Upper floor structure'
  ];
  return { tab: 'Full Assessment', headers: [
    'Submitted', 'Synced From', 'Event', 'Inspector', 'Building Name', 'Address', 'GPS',
    'Stories', 'Age', 'Construction Type', 'Occupancy', 'Foundation', 'Roof Shape', 'Roof Covering', 'Wall Finish',
    'Water Nature', 'Water Depth', 'Sediment', 'Erosion',
    'Arch Style', 'Hazards',
    'Significance: Older', 'Significance: Craftsman', 'Significance: Style',
    'Significance: Setting', 'Significance: Rare', 'Significance: Persons',
    'Site: Topo', 'Site: Retaining', 'Site: Vegetation', 'Site: Small Structures',
    'Site: Archaeology', 'Site: Collections', 'Site: Collections Condition',
    'Ext: Foundation', 'Ext: Basement walls', 'Ext: Exterior walls', 'Ext: Roof structure',
    'Ext: Roofing material', 'Ext: Chimneys', 'Ext: Porches/balconies', 'Ext: Windows',
    'Ext: Doors', 'Ext: Exterior trim', 'Ext: Siding/cladding', 'Ext: Paint/coatings',
    'Ext: Drainage/gutters', 'Ext: Steps/walkways', 'Ext: Fencing', 'Ext: Site features',
    'Int: Ceiling', 'Int: Floor structure', 'Int: Floor covering',
    'Int: Walls/plaster', 'Int: Stairways', 'Int: Upper floor',
    'Contents Type', 'Contents Condition',
    'Final Posting', 'Further Eval?', 'Recommendations'
  ], values: [
    payload.queuedAt || new Date().toISOString(),
    payload.name || '', as.event || '',
    as.inspector, as.buildingName, as.address, (as.gps || []).filter(Boolean).join('; '),
    as.stories, as.age, as.constructionType, as.occupancy, as.foundation, as.roof, as.roofCovering, as.wallFinish,
    (as.waterNature || []).join(', '), (as.waterDepth || []).join(', '), as.sediment, as.erosion,
    as.archStyle, (as.hazards || []).join(', '),
    as.sigOlder, as.sigCraftsman, as.sigStyle,
    as.sigSetting, as.sigRare, as.sigPersons,
    as.siteTopo, as.siteRetaining, as.siteVeg, as.siteSmall,
    as.siteArchaeo, as.siteCollections, as.siteCollCond,
    ...extCats.map(c => ed[c] || ''),
    ...intCats.map(c => id[c] || ''),
    (as.contentsType || []).join(', '), as.contentsCond,
    as.finalPosting, as.furtherEval ? 'Yes' : 'No', as.recommendations
  ] };
}

function homeownerRow(payload, hw) {
  const wa = hw.walkAnswers || {};
  const d = hw.damage || {};
  const c = hw.shareConsent || {};
  return { tab: 'Homeowner', headers: [
    'Submitted', 'Event', 'Consent At', 'Consent Version', 'Language',
    'Address', 'State', 'GPS', 'Owner Type', 'Age',
    'Materials', 'Designations',
    'Water Level', 'Exterior', 'Foundation', 'Roof', 'Windows',
    'Interior', 'Mold', 'Chimney',
    'Damage: Structural', 'Damage: Roof', 'Damage: Siding', 'Damage: Windows',
    'Damage: Chimney', 'Damage: Electrical', 'Damage: Insulation',
    'Damage: Interior', 'Damage: Mold'
  ], values: [
    payload.queuedAt || new Date().toISOString(),
    hw.event || '', c.at, c.version, c.lang || '',
    hw.address, hw.state, (hw.gps || []).filter(Boolean).join(', '), hw.owner || '', hw.age || '',
    (hw.materials || []).join(', '), (hw.designations || []).join(', '),
    wa.water_level || '', wa.exterior_damage || '', wa.foundation_visible || '',
    wa.roof_damage || '', wa.windows_doors || '',
    wa.interior_condition || '', wa.mold_visible || '', wa.chimney || '',
    d.structural || '', d.roof || '', d.siding || '', d.windows || '',
    d.chimney || '', d.electrical || '', d.insulation || '',
    d.interior || '', d.mold || ''
  ] };
}
