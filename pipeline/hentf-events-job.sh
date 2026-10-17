#!/bin/bash
# Daily HENTF -> events.json job (launchd: com.becca.floodapp-hentf-events, 07:15).
#
# Runs in its OWN clone (never Becca's working copy) so it can't commit her in-progress work:
#   ~/.local/share/floodapp-bot/ncpttFloodApp
# 1. pull; 2. look for new DR numbers in FEMA-HENTF emails (silent Graph token only);
# 3. rebuild events.json from OpenFEMA (also picks up counties added to known disasters);
# 4. commit + push ONLY events-sources.json / events.json / deploy/events.json;
# 5. leave Becca a vault task for each disaster that newly appears in events.json (sharing its
#    Sheet with the SHPO is hers). Compared before/after the build, so a DR number OpenFEMA hadn't
#    loaded yet on the day of the notice still gets its task on the day it validates.
# The service worker serves events.json network-first, so no cache bump is needed.
set -uo pipefail
CLONE="$HOME/.local/share/floodapp-bot/ncpttFloodApp"
UV=/opt/homebrew/bin/uv
TASKS="/Users/becca/Library/Mobile Documents/iCloud~md~obsidian/Documents/BeccaNap/tasks"
FILES=(events-sources.json events.json deploy/events.json)
LOG_DIR="$HOME/Library/Logs/floodapp-hentf"; mkdir -p "$LOG_DIR"
exec >>"$LOG_DIR/$(date +%F).log" 2>&1
echo "== $(date) start"
notify() { osascript -e "display notification \"$1\" with title \"Flood app HENTF job\" sound name \"Basso\"" || true; }
fail() { echo "FAILED: $1"; notify "Failed: $1. See ~/Library/Logs/floodapp-hentf"; exit 1; }

[ -d "$CLONE/.git" ] || git clone -q https://github.com/rkn2/ncpttFloodApp.git "$CLONE" || fail "clone"
cd "$CLONE" || fail "cd clone"
[ -z "$(git status --porcelain)" ] || fail "bot clone has uncommitted changes: $(git status --porcelain | tr '\n' ' ')"
git pull -q --rebase || fail "git pull"

out=$("$UV" run -q --with requests --with msal python3 pipeline/hentf_inbox.py) || { echo "$out"; fail "inbox check"; }
echo "$out"

ids() { python3 -c 'import json; print(" ".join(str(e["disasterNumber"]) for e in json.load(open("events.json"))["events"]))'; }
before=" $(ids) "
"$UV" run -q --with pyshp python3 pipeline/build_events.py || fail "build_events"
new_events=""
for n in $(ids); do case "$before" in *" $n "*) ;; *) new_events="$new_events $n" ;; esac; done
new_events="${new_events# }"

other=$(git status --porcelain | cut -c4- | grep -v -x -E "events-sources\.json|events\.json|deploy/events\.json" || true)
[ -z "$other" ] || fail "unexpected changes, not committing: $other"
if [ -n "$(git status --porcelain -- "${FILES[@]}")" ]; then
  msg="events: update declared disasters from HENTF notices and OpenFEMA"
  [ -n "$new_events" ] && msg="events: add DR-${new_events// /, DR-} from HENTF notices"
  git add -- "${FILES[@]}" && git commit -q -m "$msg

Automated by pipeline/hentf-events-job.sh (launchd com.becca.floodapp-hentf-events)." || fail "commit"
  git push -q || { git pull -q --rebase && git push -q; } || fail "push"
  echo "pushed: $msg"
else
  echo "no changes"
fi

# A task for each disaster new to events.json (validated by build_events.py).
for dr in $new_events; do
  line=$(python3 - "$dr" <<'EOF'
import json, sys
d = json.load(open('events.json'))
ev = next((e for e in d['events'] if e['disasterNumber'] == int(sys.argv[1])), None)
print(f"{ev['id']}\t{ev['stateName']}\t{ev['title']}\t{ev['hentfNotice']}" if ev else '')
EOF
)
  [ -n "$line" ] || { echo "DR-$dr dropped by validation, no task"; continue; }
  IFS=$'\t' read -r id state title notice <<<"$line"
  f="$TASKS/$(date +%F)-floodapp-$(echo "$id" | tr '[:upper:]' '[:lower:]')-shpo-map.md"
  [ -e "$f" ] && continue
  cat >"$f" <<EOF
---
completed_date: ''
created: '$(date +%F)'
dismissed_reason: ''
domain: research
done: false
due_date: '$(date -v+7d +%F)'
due_type: soft
estimated_minutes: 15
origin: claude
priority: medium
source: 'floodapp HENTF job, notice of ${notice}'
title: "Flood app: ${id} (${state}) added; share its map with the ${state} SHPO once entries arrive"
---

HENTF's notice put ${id} (${title}) in the flood app's disaster list, so field entries in its declared counties are now tagged with it. When the first entry arrives, its Sheet "Flood app entries: ${id}" and a map link appear in the intake registry. Share that Sheet (Viewer) with the ${state} SHPO staff and send them the map link. Steps: [setup guide](https://github.com/rkn2/ncpttFloodApp/blob/main/sync/README.md#each-disaster). Disaster page: https://www.fema.gov/disaster/${id:3:4}
EOF
  echo "task: $f"
done
echo "== $(date) done"
