#!/usr/bin/env bash
# Scaffold a new blog post file from template.
# Creates the file with frontmatter and placeholder content.

set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <format> <slug> [date]" >&2
    echo "" >&2
    echo "  format: 'launch' or 'press'" >&2
    echo "  slug:   URL slug (e.g., 'ailang-v09-cloud')" >&2
    echo "  date:   optional YYYY-MM-DD (defaults to today)" >&2
    echo "" >&2
    echo "Examples:" >&2
    echo "  $0 launch ailang-v09-cloud" >&2
    echo "  $0 press docparse-cloud-api 2026-03-15" >&2
    exit 1
fi

FORMAT="$1"
SLUG="$2"
DATE="${3:-$(date +%Y-%m-%d)}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLOG_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
BLOG_DIR="$BLOG_ROOT/blog"
FILEPATH="$BLOG_DIR/$DATE-$SLUG.md"

if [[ -f "$FILEPATH" ]]; then
    echo "ERROR: File already exists: $FILEPATH" >&2
    exit 1
fi

case "$FORMAT" in
    launch)
        TAG="product-launch"
        SLUG_PREFIX=""
        cat > "$FILEPATH" << 'TEMPLATE'
---
title: "PRODUCT: Compelling Headline Here"
authors: solaris
tags: [product-launch, PRODUCT_TAG]
slug: /SLUG
---

:::info[AI-Generated Content]
This product announcement was written by Solaris, Sunholo's AI communications assistant, and reviewed by the Sunholo team.
:::

HOOK_PARAGRAPH — What problem does this solve? Why should the reader care?

<!-- truncate -->

## What is PRODUCT?

2-3 paragraphs explaining the product. Focus on value, not implementation details.

## Key Features

- **Feature 1** — Brief explanation of why it matters
- **Feature 2** — Brief explanation
- **Feature 3** — Brief explanation

## Getting Started

Practical steps: installation, first use, or where to go next.

## What's New in VERSION

Highlight the most impactful changes from the changelog.

## Learn More

- [Documentation](DOCS_URL)
- [GitHub](GITHUB_URL)
- [Website](https://sunholo.com)
TEMPLATE
        ;;
    press)
        TAG="press-release"
        SLUG_PREFIX="press-"
        cat > "$FILEPATH" << 'TEMPLATE'
---
title: "Sunholo Launches PRODUCT for TARGET_AUDIENCE"
authors: solaris
tags: [press-release, PRODUCT_TAG]
slug: /press-SLUG
---

:::info[AI-Generated Content]
This press release was prepared by Solaris, Sunholo's AI communications assistant, and reviewed by the Sunholo team.
:::

**COPENHAGEN, Denmark — MONTH DAY, YEAR —** Sunholo today announced WHAT, enabling WHO to DO_WHAT.

<!-- truncate -->

SUPPORTING_PARAGRAPH_1 — Expand on the announcement with specifics.

SUPPORTING_PARAGRAPH_2 — Business context: market need, metrics.

> "QUOTE_ABOUT_WHY_THIS_MATTERS"
> — Mark Edmondson, Founder, Sunholo

## Key Highlights

- HIGHLIGHT_1 with concrete metric or capability
- HIGHLIGHT_2
- HIGHLIGHT_3

## Availability

PRICING_AND_ACCESS_INFO — how to get started, licensing, links.

## About Sunholo

Sunholo (Holosun ApS) builds production AI systems for enterprises. Products include AILANG, a deterministic language for AI code synthesis; Multivac, an enterprise AI platform; and DocParse, universal document parsing. Based in Copenhagen, Denmark. Learn more at [sunholo.com](https://sunholo.com).

## Links

- [Product page](PRODUCT_URL)
- [Documentation](DOCS_URL)
- [GitHub](GITHUB_URL)
TEMPLATE
        ;;
    *)
        echo "ERROR: Unknown format '$FORMAT'. Use 'launch' or 'press'." >&2
        exit 1
        ;;
esac

echo "Created: $FILEPATH"
echo "Format: $FORMAT"
echo "Date: $DATE"
echo "Slug: /${SLUG_PREFIX}${SLUG}"
echo ""
echo "Next: Fill in the template placeholders, then run validate_post.sh"
