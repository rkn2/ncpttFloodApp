// SHPO map — one private map page per disaster.
//
// Deploy as a web app that runs AS THE PERSON VIEWING IT (Execute as: User accessing the web app).
// The page opens the disaster's Sheet with the viewer's own Google permissions, so only people
// that Sheet is shared with can see anything. This must stay a separate Apps Script project from
// sync/intake.gs (which runs as Becca and accepts anonymous entries). Setup: sync/README.md.
//
// Link for a disaster: <map web app URL>?sheet=<that disaster's Sheet ID> (the intake registry
// tab lists it once MAP_URL is set).

const TABS = { rapid: 'Rapid Triage', full: 'Full Assessment', homeowner: 'Homeowner' };

function doGet(e) {
  const id = (e && e.parameter && e.parameter.sheet) || '';
  const viewer = Session.getActiveUser().getEmail();
  if (!id) return message('No disaster selected', 'This link is missing its ?sheet= part. Ask for the full link.');
  let ss;
  try {
    ss = SpreadsheetApp.openById(id);
  } catch (err) {
    return message('No access',
      'This disaster map is shared only with the State Historic Preservation Office staff working on it. ' +
      (viewer ? 'You are signed in as ' + viewer + ', which does not have access. ' : '') +
      'Ask the person who sent the link to share the Sheet with this account.');
  }
  const about = {};
  const aboutSheet = ss.getSheetByName('About');
  if (aboutSheet) aboutSheet.getDataRange().getDisplayValues().forEach(r => { about[r[0]] = r[1]; });
  const tabs = {};
  Object.keys(TABS).forEach(k => { tabs[k] = rows(ss.getSheetByName(TABS[k])); });
  const t = HtmlService.createTemplateFromFile('shpo-map');
  // '<' escaped so no cell value can close the <script> block the data is embedded in.
  t.data = JSON.stringify({ about: about, tabs: tabs, sheetUrl: ss.getUrl(), viewer: viewer }).replace(/</g, '\\u003c');
  return t.evaluate()
    .setTitle('Disaster map: ' + (about['Event ID'] || ss.getName()))
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function rows(sheet) {
  if (!sheet || sheet.getLastRow() < 2) return [];
  const v = sheet.getDataRange().getDisplayValues();
  const h = v[0];
  return v.slice(1).map(r => { const o = {}; h.forEach((k, i) => { o[k] = r[i]; }); return o; });
}

function message(title, text) {
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  return HtmlService.createHtmlOutput(
    '<div style="font-family:-apple-system,Segoe UI,sans-serif;max-width:560px;margin:48px auto;padding:0 16px;color:#1B3A5C">' +
    '<h1 style="font-size:1.3rem">' + esc(title) + '</h1><p style="line-height:1.5">' + esc(text) + '</p></div>')
    .setTitle(title).addMetaTag('viewport', 'width=device-width, initial-scale=1');
}
