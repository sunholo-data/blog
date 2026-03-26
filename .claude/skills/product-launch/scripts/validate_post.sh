#!/usr/bin/env bash
# Validate a product launch or press release blog post.
# Checks: frontmatter, AI disclosure, truncate marker, structure, and build.

set -euo pipefail

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <post-file>" >&2
    echo "" >&2
    echo "Example: $0 blog/2026-03-15-docparse-cloud-api.md" >&2
    exit 1
fi

POST="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLOG_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

if [[ ! -f "$BLOG_ROOT/$POST" ]] && [[ ! -f "$POST" ]]; then
    echo "ERROR: File not found: $POST" >&2
    exit 1
fi

# Resolve to absolute path
if [[ -f "$BLOG_ROOT/$POST" ]]; then
    POST_PATH="$BLOG_ROOT/$POST"
else
    POST_PATH="$POST"
fi

FAILURES=0
WARNINGS=0

echo "=== Validating: $POST ==="
echo ""

# 1. Check frontmatter exists
echo "1/7 Checking frontmatter..."
if head -1 "$POST_PATH" | grep -q "^---$"; then
    # Check required fields
    FRONTMATTER=$(sed -n '/^---$/,/^---$/p' "$POST_PATH")

    if echo "$FRONTMATTER" | grep -q "^title:"; then
        echo "  ✓ title present"
    else
        echo "  ✗ title missing"
        FAILURES=$((FAILURES + 1))
    fi

    if echo "$FRONTMATTER" | grep -q "^authors: solaris"; then
        echo "  ✓ authors: solaris"
    else
        echo "  ✗ authors should be 'solaris'"
        FAILURES=$((FAILURES + 1))
    fi

    if echo "$FRONTMATTER" | grep -q "^tags:"; then
        if echo "$FRONTMATTER" | grep -q "product-launch\|press-release"; then
            echo "  ✓ tags include product-launch or press-release"
        else
            echo "  ✗ tags must include 'product-launch' or 'press-release'"
            FAILURES=$((FAILURES + 1))
        fi
    else
        echo "  ✗ tags missing"
        FAILURES=$((FAILURES + 1))
    fi

    if echo "$FRONTMATTER" | grep -q "^slug:"; then
        echo "  ✓ slug present"
    else
        echo "  ! slug missing (optional but recommended)"
        WARNINGS=$((WARNINGS + 1))
    fi

    if echo "$FRONTMATTER" | grep -q "^image:"; then
        # Check if image file exists
        IMAGE_REF=$(echo "$FRONTMATTER" | grep "^image:" | sed 's/image: *//' | tr -d '"' | tr -d "'")
        IMAGE_DIR=$(dirname "$POST_PATH")
        if [[ -f "$IMAGE_DIR/$IMAGE_REF" ]]; then
            echo "  ✓ image exists: $IMAGE_REF"
        else
            echo "  ! image referenced but not found: $IMAGE_REF"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        echo "  ! no image field (add before merge or omit)"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ✗ no frontmatter found (must start with ---)"
    FAILURES=$((FAILURES + 1))
fi

# 2. Check AI disclosure admonition
echo ""
echo "2/7 Checking AI disclosure..."
if grep -q ":::info\[AI-Generated Content\]" "$POST_PATH"; then
    echo "  ✓ AI disclosure admonition present"
else
    echo "  ✗ Missing AI disclosure admonition"
    FAILURES=$((FAILURES + 1))
fi

# 3. Check truncate marker
echo ""
echo "3/7 Checking truncate marker..."
if grep -q "<!-- truncate -->" "$POST_PATH"; then
    echo "  ✓ truncate marker present"
else
    echo "  ✗ Missing <!-- truncate --> marker"
    FAILURES=$((FAILURES + 1))
fi

# 4. Check for placeholder text
echo ""
echo "4/7 Checking for unfilled placeholders..."
PLACEHOLDERS=$(grep -c "PRODUCT_TAG\|DOCS_URL\|GITHUB_URL\|PRODUCT_URL\|HOOK_PARAGRAPH\|SUPPORTING_PARAGRAPH\|HIGHLIGHT_1\|DO_WHAT\|TARGET_AUDIENCE" "$POST_PATH" 2>/dev/null || true)
if [[ "$PLACEHOLDERS" -gt 0 ]]; then
    echo "  ✗ Found $PLACEHOLDERS unfilled placeholder(s):"
    grep -n "PRODUCT_TAG\|DOCS_URL\|GITHUB_URL\|PRODUCT_URL\|HOOK_PARAGRAPH\|SUPPORTING_PARAGRAPH\|HIGHLIGHT_1\|DO_WHAT\|TARGET_AUDIENCE" "$POST_PATH" | sed 's/^/    /'
    FAILURES=$((FAILURES + 1))
else
    echo "  ✓ No unfilled placeholders"
fi

# 5. Check word count
echo ""
echo "5/7 Checking word count..."
# Strip frontmatter and count words
BODY=$(sed '1,/^---$/d' "$POST_PATH" | sed '/^---$/d')
WORD_COUNT=$(echo "$BODY" | wc -w | tr -d ' ')

IS_PRESS=$(grep -c "press-release" "$POST_PATH" 2>/dev/null || true)
if [[ "$IS_PRESS" -gt 0 ]]; then
    if [[ "$WORD_COUNT" -lt 200 ]]; then
        echo "  ! Press release is very short ($WORD_COUNT words, target 400-800)"
        WARNINGS=$((WARNINGS + 1))
    elif [[ "$WORD_COUNT" -gt 1000 ]]; then
        echo "  ! Press release is long ($WORD_COUNT words, target 400-800)"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "  ✓ Word count: $WORD_COUNT (target: 400-800 for press release)"
    fi
else
    if [[ "$WORD_COUNT" -lt 400 ]]; then
        echo "  ! Product launch post is very short ($WORD_COUNT words, target 800-1500)"
        WARNINGS=$((WARNINGS + 1))
    elif [[ "$WORD_COUNT" -gt 2000 ]]; then
        echo "  ! Product launch post is long ($WORD_COUNT words, target 800-1500)"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "  ✓ Word count: $WORD_COUNT (target: 800-1500 for product launch)"
    fi
fi

# 6. Check for press release specific elements
echo ""
echo "6/7 Checking format-specific elements..."
if [[ "$IS_PRESS" -gt 0 ]]; then
    if grep -q "COPENHAGEN, Denmark" "$POST_PATH"; then
        echo "  ✓ Dateline present"
    else
        echo "  ✗ Press release missing dateline (COPENHAGEN, Denmark)"
        FAILURES=$((FAILURES + 1))
    fi
    if grep -q "About Sunholo" "$POST_PATH"; then
        echo "  ✓ About Sunholo boilerplate present"
    else
        echo "  ✗ Press release missing 'About Sunholo' section"
        FAILURES=$((FAILURES + 1))
    fi
    if grep -q "Mark Edmondson" "$POST_PATH"; then
        echo "  ✓ Quote attribution present"
    else
        echo "  ! Press release should include a quote from Mark Edmondson"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    if grep -q "## Getting Started\|## Key Features\|## What is\|## Learn More" "$POST_PATH"; then
        echo "  ✓ Product launch structure looks good"
    else
        echo "  ! Product launch post may be missing standard sections"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# 7. Build check
echo ""
echo "7/7 Running yarn build..."
if cd "$BLOG_ROOT" && yarn build > /dev/null 2>&1; then
    echo "  ✓ Build passed"
else
    echo "  ✗ Build failed — run 'yarn build' manually to see errors"
    FAILURES=$((FAILURES + 1))
fi

# Summary
echo ""
echo "=== Validation Summary ==="
if [[ $FAILURES -eq 0 ]] && [[ $WARNINGS -eq 0 ]]; then
    echo "✓ All checks passed!"
    exit 0
elif [[ $FAILURES -eq 0 ]]; then
    echo "✓ Passed with $WARNINGS warning(s)"
    exit 0
else
    echo "✗ $FAILURES failure(s), $WARNINGS warning(s)"
    exit 1
fi
