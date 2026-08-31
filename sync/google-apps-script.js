// Google Apps Script — paste this into your Google Sheet's script editor.
//
// SETUP:
// 1. Create a new Google Sheet
// 2. Extensions → Apps Script
// 3. Paste this entire file, replacing the default code
// 4. Click Deploy → New deployment
//    - Type: Web app
//    - Execute as: Me
//    - Who has access: Anyone
// 5. Copy the deployment URL
// 6. Paste it into SYNC_ENDPOINT in floodapp.html (search for SYNC_ENDPOINT)
//
// The sheet auto-creates two tabs: "Rapid Triage" and "Full Assessment"
// with headers on first POST. Each new assessment appends a row.

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const data = payload.data || {};
    const as = data.as || {};
    const hw = data.hw || {};
    const mode = data.mode;
    const submode = as.submode;

    if (mode === 'assessor' && submode === 'rapid') {
      appendRapid(ss, payload, as);
    } else if (mode === 'assessor' && submode === 'full') {
      appendFull(ss, payload, as);
    } else if (mode === 'homeowner') {
      appendHomeowner(ss, payload, hw);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok', message: 'SHPO sync endpoint is live.' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function getOrCreateSheet(ss, name, headers) {
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function appendRapid(ss, payload, as) {
  const headers = [
    'Submitted', 'Synced From', 'Inspector', 'Date', 'Area/Event',
    'Building Name', 'Address', 'GPS',
    'Stories', 'Footprint', 'Units', 'Age', 'Construction Type', 'Occupancy',
    'Foundation', 'Roof Shape', 'Roof Covering', 'Wall Finish',
    'Historic Status',
    'Water Nature', 'Water Depth', 'Sediment', 'Erosion',
    'Structural', 'Roof Dmg', 'Siding', 'Windows', 'Chimney',
    'Electrical', 'Insulation', 'Interior', 'Mold',
    'Overall Damage', 'Posting', 'Recommend Full?', 'Trigger Reasons', 'Notes'
  ];
  const sheet = getOrCreateSheet(ss, 'Rapid Triage', headers);

  const rd = as.rapidDamage || {};
  sheet.appendRow([
    payload.queuedAt || new Date().toISOString(),
    payload.name || '',
    as.inspector, as.date, as.area,
    as.buildingName, as.address, (as.gps || []).filter(Boolean).join('; '),
    as.stories, as.footprint, as.units, as.age, as.constructionType, as.occupancy,
    as.foundation, as.roof, as.roofCovering, as.wallFinish,
    (as.historicStatus || []).join(', '),
    (as.waterNature || []).join(', '), (as.waterDepth || []).join(', '), as.sediment, as.erosion,
    rd.structural || '', rd.roof || '', rd.siding || '', rd.windows || '', rd.chimney || '',
    rd.electrical || '', rd.insulation || '', rd.interior || '', rd.mold || '',
    as.overallDamage, as.posting, as.recommendFull ? 'Yes' : 'No',
    (as.triggerReasons || []).join(', '), as.notes
  ]);
}

function appendFull(ss, payload, as) {
  const headers = [
    'Submitted', 'Synced From', 'Inspector', 'Building Name', 'Address', 'GPS',
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
  ];
  const sheet = getOrCreateSheet(ss, 'Full Assessment', headers);

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

  sheet.appendRow([
    payload.queuedAt || new Date().toISOString(),
    payload.name || '',
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
  ]);
}

function appendHomeowner(ss, payload, hw) {
  const headers = [
    'Submitted', 'Address', 'State', 'GPS',
    'Materials', 'Designations',
    'Water Level', 'Exterior', 'Foundation', 'Roof', 'Windows',
    'Interior', 'Mold', 'Chimney',
    'Damage: Structural', 'Damage: Roof', 'Damage: Siding', 'Damage: Windows',
    'Damage: Chimney', 'Damage: Electrical', 'Damage: Insulation',
    'Damage: Interior', 'Damage: Mold'
  ];
  const sheet = getOrCreateSheet(ss, 'Homeowner', headers);

  const wa = hw.walkAnswers || {};
  const d = hw.damage || {};
  sheet.appendRow([
    payload.queuedAt || new Date().toISOString(),
    hw.address, hw.state, (hw.gps || []).join(', '),
    (hw.materials || []).join(', '), (hw.designations || []).join(', '),
    wa.water_level || '', wa.exterior_damage || '', wa.foundation_visible || '',
    wa.roof_damage || '', wa.windows_doors || '',
    wa.interior_condition || '', wa.mold_visible || '', wa.chimney || '',
    d.structural || '', d.roof || '', d.siding || '', d.windows || '',
    d.chimney || '', d.electrical || '', d.insulation || '',
    d.interior || '', d.mold || ''
  ]);
}
