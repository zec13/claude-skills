#!/usr/bin/env bash
# move_to_posted.sh — Move an image from organic-images/ to already-posted/ in GitHub
#
# Usage: bash scripts/move_to_posted.sh <brand-name> <filename>
# Example: bash scripts/move_to_posted.sh TableClay blue-glaze-mug.jpg
#
# This creates two commits: one to add the file to already-posted/, one to delete from organic-images/
# The git history serves as an audit trail of what was posted and when.

set -euo pipefail

BRAND="${1:?Usage: move_to_posted.sh <brand-name> <filename>}"
FILENAME="${2:?Usage: move_to_posted.sh <brand-name> <filename>}"
REPO="${GITHUB_REPO:-Nsf34/claude-skills}"
TOKEN="${GITHUB_TOKEN:?GITHUB_TOKEN environment variable is required}"

# Determine paths (try new structure first)
SRC_PATH="Brands/${BRAND}/organic-images/${FILENAME}"
DST_PATH="Brands/${BRAND}/already-posted/${FILENAME}"

echo "Moving ${FILENAME} to already-posted for ${BRAND}..."

# Step 1: Get the file content and SHA from the source
echo "Fetching file from ${SRC_PATH}..."
FILE_INFO=$(curl -sf \
  -H "Authorization: token ${TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${REPO}/contents/${SRC_PATH}")

if [ -z "$FILE_INFO" ]; then
  # Try fallback path
  SRC_PATH="Business Research/${BRAND}/organic-images/${FILENAME}"
  DST_PATH="Business Research/${BRAND}/already-posted/${FILENAME}"
  FILE_INFO=$(curl -sf \
    -H "Authorization: token ${TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${REPO}/contents/${SRC_PATH}")
fi

FILE_CONTENT=$(echo "$FILE_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin)['content'])" | tr -d '\n')
FILE_SHA=$(echo "$FILE_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])")

DATE=$(date +%Y-%m-%d)

# Step 2: Create file at destination (already-posted/)
echo "Creating ${DST_PATH}..."
curl -sf -X PUT \
  -H "Authorization: token ${TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${REPO}/contents/${DST_PATH}" \
  -d "{
    \"message\": \"[${BRAND}] Posted: ${FILENAME} on ${DATE}\",
    \"content\": \"${FILE_CONTENT}\",
    \"branch\": \"main\"
  }" > /dev/null

echo "Created in already-posted/"

# Step 3: Delete file from source (organic-images/)
echo "Removing from ${SRC_PATH}..."
curl -sf -X DELETE \
  -H "Authorization: token ${TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${REPO}/contents/${SRC_PATH}" \
  -d "{
    \"message\": \"[${BRAND}] Moved to already-posted: ${FILENAME}\",
    \"sha\": \"${FILE_SHA}\",
    \"branch\": \"main\"
  }" > /dev/null

echo "Removed from organic-images/"
echo "Done! ${FILENAME} moved to already-posted/ for ${BRAND}"

# Step 4: Log the posting
LOG_FILE="/tmp/organic-poster/posting-log.csv"
if [ ! -f "$LOG_FILE" ]; then
  echo "date,brand,filename,platforms,notes" > "$LOG_FILE"
fi
echo "${DATE},${BRAND},${FILENAME},\"ig+fb+threads+tiktok\",\"\"" >> "$LOG_FILE"
echo "Logged to ${LOG_FILE}"
