#!/usr/bin/env bash
# Create the GitHub repo, labels, issues (one per docs/tasks/*.md) and a Project board.
# Usage: scripts/bootstrap.sh <owner>/<repo> [--private]
# Needs: gh auth with repo + project scopes (gh auth refresh -s project).
set -euo pipefail

REPO="${1:?usage: bootstrap.sh <owner>/<repo> [--private]}"
VIS="${2:---private}"
OWNER="${REPO%%/*}"
cd "$(dirname "$0")/.."

if ! gh repo view "$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" "$VIS" --source=. --remote=origin --push
fi

for l in learning bug feature skills fusion automation merge stacked-prs capstone agent-ready \
         phase-1 phase-2 phase-3 phase-4 phase-5; do
  gh label create "$l" --repo "$REPO" --force >/dev/null
done

PROJECT_URL=$(gh project create --owner "$OWNER" --title "Copilot Lab" --format json --jq .url 2>/dev/null || true)

for f in docs/tasks/*.md; do
  title=$(sed -n '1s/^# //p' "$f")
  labels=$(sed -n '2s/^labels: //p' "$f")
  body=$(sed '1,2d' "$f")
  # agent-ready on creation would trigger automation; hold it back until task 08 is done.
  labels_no_trigger=$(echo "$labels" | sed 's/agent-ready,\?//; s/,$//')
  url=$(gh issue create --repo "$REPO" --title "$title" --label "$labels_no_trigger" --body "$body")
  echo "created $url"
  [ -n "$PROJECT_URL" ] && gh project item-add "$(basename "$PROJECT_URL")" --owner "$OWNER" --url "$url" >/dev/null || true
done

echo "Done. Project: ${PROJECT_URL:-<not created, run: gh auth refresh -s project>}"
