#!/usr/bin/env bash
# fetch_next_image.sh — Download the oldest unposted image for a brand from GitHub
#
# Usage: bash scripts/fetch_next_image.sh <brand-name>
# Example: bash scripts/fetch_next_image.sh TableClay
#
# Requires: GITHUB_TOKEN and GITHUB_REPO env vars
# Downloads to: /tmp/organic-poster/<brand>/

set -euo pipefail

BRAND="${1:?Usage: fetch_next_image.sh <brand-name>}"
REPO="${GITHUB_REPO:-Nsf34/claude-skills}"
TOKEN="${GITHUB_TOKEN:?GITHUB_TOKEN environment variable is required}"

# Try new structure first, fall back to old
IMAGE_PATH="Brands/${BRAND}/organic-images"
FALLBACK_PATH="Business Research/${BRAND}/organic-images"

DOWNLOAD_DIR="/tmp/organic-poster/${BRAND}"
mkdir -p "$DOWNLOAD_DIR"

echo "Checking for unposted images for ${BRAND}..."

# Try primary path
RESPONSE=$(curl -sf \
  -H "Authorization: token ${TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${REPO}/contents/${IMAGE_PATH}" 2>/dev/null || true)

# If primary path fails, try fallback
if [ -z "$RESPONSE" ] || echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if isinstance(d,list) else 1)" 2>/dev/null; then
  : # primary path worked (or is empty list)
else
  echo "Primary path not found, trying fallback path..."
  IMAGE_PATH="$FALLBACK_PATH"
  RESPONSE=$(curl -sf \
    -H "Authorization: token ${TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${REPO}/contents/${IMAGE_PATH}" 2>/dev/null || true)
fi

if [ -z "$RESPONSE" ]; then
  echo "ERROR: Could not find organic-images folder for ${BRAND}"
  echo "Checked: Brands/${BRAND}/organic-images and Business Research/${BRAND}/organic-images"
  exit 1
fi

# Parse response — get list of image files sorted by name (FIFO approximation)
# For true FIFO by commit date, we'd need to check git log for each file
FIRST_IMAGE=$(echo "$RESPONSE" | python3 -c "
import sys, json
items = json.load(sys.stdin)
if not isinstance(items, list) or len(items) == 0:
    print('EMPTY')
    sys.exit(0)
# Filter for image files
images = [f for f in items if f['name'].lower().endswith(('.jpg','.jpeg','.png','.webp','.gif'))]
if not images:
    print('EMPTY')
    sys.exit(0)
# Sort by name (oldest first assuming sequential naming)
images.sort(key=lambda x: x['name'])
print(images[0]['name'])
print(images[0]['download_url'])
print(images[0]['sha'])
print(len(images))
")

if [ "$FIRST_IMAGE" = "EMPTY" ]; then
  echo "No unposted images for ${BRAND}. Add images to the organic-images folder."
  exit 0
fi

# Parse output
IMAGE_NAME=$(echo "$FIRST_IMAGE" | sed -n '1p')
DOWNLOAD_URL=$(echo "$FIRST_IMAGE" | sed -n '2p')
FILE_SHA=$(echo "$FIRST_IMAGE" | sed -n '3p')
TOTAL_COUNT=$(echo "$FIRST_IMAGE" | sed -n '4p')

echo "Found ${TOTAL_COUNT} unposted image(s). Next up: ${IMAGE_NAME}"

# Download the image
curl -sL \
  -H "Authorization: token ${TOKEN}" \
  -o "${DOWNLOAD_DIR}/${IMAGE_NAME}" \
  "$DOWNLOAD_URL"

echo "Downloaded: ${DOWNLOAD_DIR}/${IMAGE_NAME}"
echo "SHA: ${FILE_SHA}"
echo "Remaining after this: $((TOTAL_COUNT - 1))"

# Output JSON summary for script consumption
cat <<EOF > "${DOWNLOAD_DIR}/fetch_result.json"
{
  "brand": "${BRAND}",
  "filename": "${IMAGE_NAME}",
  "local_path": "${DOWNLOAD_DIR}/${IMAGE_NAME}",
  "github_path": "${IMAGE_PATH}/${IMAGE_NAME}",
  "sha": "${FILE_SHA}",
  "remaining": $((TOTAL_COUNT - 1))
}
EOF

echo "Fetch result saved to ${DOWNLOAD_DIR}/fetch_result.json"
