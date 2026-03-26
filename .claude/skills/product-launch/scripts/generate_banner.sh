#!/bin/bash
# Generate banner images for blog posts using Gemini image generation
# via the voyage CLI (from stapledons_voyage)
#
# Usage:
#   scripts/generate_banner.sh SLUG "prompt describing the image"
#   scripts/generate_banner.sh docparse-launch "Abstract visualization of documents flowing through a parser"
#
# Requirements:
#   - voyage CLI installed (from stapledons_voyage)
#   - GOOGLE_API_KEY or gcloud auth configured
#
# Output:
#   blog/img/SLUG.webp (converted from PNG)

set -euo pipefail

SLUG="${1:?Usage: generate_banner.sh SLUG \"prompt\"}"
PROMPT="${2:?Usage: generate_banner.sh SLUG \"prompt\"}"

BLOG_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
IMG_DIR="${BLOG_DIR}/blog/img"
OUTPUT_PNG="${IMG_DIR}/${SLUG}.png"
OUTPUT_WEBP="${IMG_DIR}/${SLUG}.webp"

# Ensure img directory exists
mkdir -p "${IMG_DIR}"

# Check for voyage CLI
if ! command -v voyage &>/dev/null; then
    echo "Error: voyage CLI not found. Install from stapledons_voyage:"
    echo "  cd /Users/mark/dev/sunholo/stapledons_voyage && make install"
    exit 1
fi

# Banner style prefix for consistent blog aesthetics
STYLE_PREFIX="Modern, clean tech illustration for a blog banner. Wide aspect ratio, suitable for social sharing. No text overlays. "

echo "Generating banner image for: ${SLUG}"
echo "Prompt: ${STYLE_PREFIX}${PROMPT}"

# Generate image with voyage CLI (uses Gemini gemini-2.5-flash-image)
voyage ai -generate-image -aspect 16:9 -size 2K \
    -prompt "${STYLE_PREFIX}${PROMPT}"

# Find the most recently generated image
GENERATED=$(ls -t /Users/mark/dev/sunholo/stapledons_voyage/assets/generated/response_*.png 2>/dev/null | head -1)

if [ -z "${GENERATED}" ]; then
    echo "Error: No generated image found in assets/generated/"
    exit 1
fi

echo "Generated: ${GENERATED}"

# Convert to webp for blog (smaller file size, better for web)
if command -v cwebp &>/dev/null; then
    cwebp -q 85 "${GENERATED}" -o "${OUTPUT_WEBP}"
    echo "Saved: ${OUTPUT_WEBP}"
elif command -v sips &>/dev/null; then
    # macOS fallback: copy as PNG
    cp "${GENERATED}" "${OUTPUT_PNG}"
    echo "Saved: ${OUTPUT_PNG} (install cwebp for webp conversion: brew install webp)"
else
    cp "${GENERATED}" "${OUTPUT_PNG}"
    echo "Saved: ${OUTPUT_PNG}"
fi

echo ""
echo "Add to frontmatter:"
if [ -f "${OUTPUT_WEBP}" ]; then
    echo "  image: ./img/${SLUG}.webp"
else
    echo "  image: ./img/${SLUG}.png"
fi
