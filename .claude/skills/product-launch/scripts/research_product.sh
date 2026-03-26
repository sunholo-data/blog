#!/usr/bin/env bash
# Gather product information from a Sunholo product repo.
# Outputs: version, key files found, recent changelog entries.

set -euo pipefail

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <product-name>" >&2
    echo "" >&2
    echo "Products: ailang, multivac, ailang-cloud, docparse, sunholo-py, website, presentations" >&2
    echo "" >&2
    echo "Example: $0 ailang" >&2
    exit 1
fi

PRODUCT="$1"
BASE="/Users/mark/dev/sunholo"

# Map product name to repo path
case "$PRODUCT" in
    ailang)          REPO="$BASE/ailang" ;;
    multivac)        REPO="$BASE/multivac" ;;
    ailang-cloud)    REPO="$BASE/ailang-multivac" ;;
    docparse)        REPO="$BASE/docparse" ;;
    sunholo-py)      REPO="$BASE/sunholo-py" ;;
    website)         REPO="$BASE/website" ;;
    presentations)   REPO="$BASE/presentations" ;;
    *)
        echo "Unknown product: $PRODUCT" >&2
        echo "Known products: ailang, multivac, ailang-cloud, docparse, sunholo-py, website, presentations" >&2
        exit 1
        ;;
esac

if [[ ! -d "$REPO" ]]; then
    echo "ERROR: Repo not found at $REPO" >&2
    exit 1
fi

echo "=== Product Research: $PRODUCT ==="
echo "Repo: $REPO"
echo ""

# 1. Check for key files
echo "--- Key Files ---"
FOUND=0
for f in README.md CHANGELOG.md package.json pyproject.toml go.mod Cargo.toml; do
    if [[ -f "$REPO/$f" ]]; then
        SIZE=$(wc -l < "$REPO/$f" | tr -d ' ')
        echo "  $f ($SIZE lines)"
        FOUND=$((FOUND + 1))
    fi
done
if [[ $FOUND -eq 0 ]]; then
    echo "  (no standard files found)"
fi
echo ""

# 2. Extract version if possible
echo "--- Version ---"
if [[ -f "$REPO/package.json" ]]; then
    grep -o '"version": "[^"]*"' "$REPO/package.json" 2>/dev/null || echo "  (no version in package.json)"
elif [[ -f "$REPO/pyproject.toml" ]]; then
    grep -i "^version" "$REPO/pyproject.toml" 2>/dev/null || echo "  (no version in pyproject.toml)"
elif [[ -f "$REPO/go.mod" ]]; then
    head -1 "$REPO/go.mod" 2>/dev/null
fi
echo ""

# 3. Git tags (recent versions)
echo "--- Recent Tags ---"
if cd "$REPO" && git rev-parse --git-dir > /dev/null 2>&1; then
    TAGS=$(git tag --sort=-version:refname 2>/dev/null | head -10)
    if [[ -n "$TAGS" ]]; then
        echo "$TAGS" | sed 's/^/  /'
    else
        echo "  (no tags)"
    fi
else
    echo "  (not a git repo)"
fi
echo ""

# 4. Recent changelog entries (first 30 lines)
echo "--- Changelog (first 30 lines) ---"
if [[ -f "$REPO/CHANGELOG.md" ]]; then
    head -30 "$REPO/CHANGELOG.md" | sed 's/^/  /'
else
    echo "  (no CHANGELOG.md)"
fi
echo ""

# 5. README first 20 lines (description/overview)
echo "--- README Overview (first 20 lines) ---"
if [[ -f "$REPO/README.md" ]]; then
    head -20 "$REPO/README.md" | sed 's/^/  /'
else
    echo "  (no README.md)"
fi
echo ""

# 6. Recent commits (last 10)
echo "--- Recent Commits ---"
if cd "$REPO" && git rev-parse --git-dir > /dev/null 2>&1; then
    git log --oneline -10 2>/dev/null | sed 's/^/  /'
else
    echo "  (not a git repo)"
fi
echo ""

echo "=== Research complete. Read the key files above for full details. ==="
