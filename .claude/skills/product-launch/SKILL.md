---
name: product-launch
description: Write product launch posts or press releases for Sunholo products. Use when user asks to write a product announcement, launch post, press release, product update, or says "announce PRODUCT". Handles research, writing, and PR creation. Posts are authored by Solaris (AI).
user-invokable: true
---

# Product Launch & Press Release

**Research a Sunholo product, write a blog post or press release as Solaris (AI), and create a PR for human review.**

## Quick Start

```
/product-launch announce AILANG v0.7 - focus on cloud coordinator features
/product-launch press-release DocParse Cloud API launch
/product-launch write about Multivac platform - prototype to production
/product-launch retroactive AILANG v0.8 2026-02-13 - formal verification with Z3
```

## Content Formats

This skill supports two formats. Detect from the user's prompt, or ask if ambiguous.

| | Product Launch Post | Press Release |
|---|---|---|
| **Trigger words** | "announce", "write about", "product launch" | "press release", "PR for" |
| **Tag** | `product-launch` | `press-release` |
| **Slug** | `/slug` | `/press-slug` |
| **Tone** | Enthusiastic, hands-on, developer-friendly | Formal third-person, business audience |
| **Length** | 800-1500 words | 400-800 words |
| **Content** | Features, code snippets, getting started | Business significance, metrics, quotes |

**Major releases** (new products, x.0 versions) may warrant both formats as separate posts.

## Workflow

### Phase 1: Understand the Request

Parse the user's message to determine:
- **Which format** — product launch post or press release (see Content Formats above)
- **Which product** is being announced (see Product Repo Map below)
- **What to focus on** — specific version, feature, or general overview
- **Target audience** — developers, decision-makers, or both
- **Is this retroactive?** — if "retroactive" or a past date is mentioned, use that date instead of today

If the message is ambiguous, ask the user for clarification before proceeding.

### Phase 2: Research

1. **Read the product repo** for current state:
   - README.md (product description, features, getting started)
   - CHANGELOG.md (what's new, recent versions)
   - package.json / pyproject.toml / go.mod (current version)

2. **Check existing blog posts** in `blog/` to avoid duplicating recent content.

3. **Extract key information:**
   - Product name and current version
   - Core value proposition (1 sentence)
   - Key features (3-5 bullets)
   - What's new or noteworthy
   - Getting started steps
   - Links to docs, GitHub, website

### Product Repo Map

| Product | Repo Path | Key Files |
|---------|-----------|-----------|
| AILANG | `/Users/mark/dev/sunholo/ailang` | README.md, CHANGELOG.md |
| Multivac | `/Users/mark/dev/sunholo/multivac` | README.md |
| AILANG Cloud | `/Users/mark/dev/sunholo/ailang-multivac` | README.md |
| DocParse | `/Users/mark/dev/sunholo/docparse` | README.md, CHANGELOG.md |
| sunholo-py | `/Users/mark/dev/sunholo/sunholo-py` | README.md, CHANGELOG.md |
| Website / General | `/Users/mark/dev/sunholo/website` | README.md |
| Presentations | `/Users/mark/dev/sunholo/presentations` | Various .qmd files |

If a product is not in the table above, ask the user where to find information.

### Phase 3: Write the Content

Create the file at `blog/YYYY-MM-DD-SLUG.md`. Use today's date unless this is a retroactive post (use the original release date).

**For retroactive posts**, add this admonition immediately after the AI disclosure:
```markdown
:::note[Retroactive Announcement]
This announcement was prepared in March 2026 to document the original release from [ORIGINAL_DATE].
:::
```

---

#### Format A: Product Launch Post

**Use this template:**

```markdown
---
title: "PRODUCT: Compelling Headline Here"
authors: solaris
tags: [product-launch, PRODUCT_TAG]
image: ./img/SLUG-banner.webp
slug: /SLUG
---

:::info[AI-Generated Content]
This product announcement was written by Solaris, Sunholo's AI communications assistant, and reviewed by the Sunholo team.
:::

HOOK_PARAGRAPH — What problem does this solve? Why should the reader care? Make it compelling and specific.

<!-- truncate -->

## What is PRODUCT?

2-3 paragraphs explaining the product. Focus on value, not implementation details.

## Key Features

- **Feature 1** — Brief explanation of why it matters
- **Feature 2** — Brief explanation
- **Feature 3** — Brief explanation

## Getting Started

Practical steps: installation, first use, or where to go next. Include a brief code snippet or command if appropriate.

## What's New in VERSION

(Include this section only for version-specific announcements)

Highlight the most impactful changes from the changelog.

## Learn More

- Documentation: DOCS_URL
- GitHub: GITHUB_URL
- Website: WEBSITE_URL
```

---

#### Format B: Press Release

**Use this template:**

```markdown
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

SUPPORTING_PARAGRAPH_1 — Expand on the announcement with specifics: what it does, how it works at a high level.

SUPPORTING_PARAGRAPH_2 — Business context: market need, customer pain point addressed, scale or metrics.

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

- Product page: PRODUCT_URL
- Documentation: DOCS_URL
- GitHub: GITHUB_URL
```

**Press release guidelines:**
- **Tone:** Formal third-person. "Sunholo today announced..." not "We're excited to..."
- **Length:** 400-800 words. Dense and factual.
- **Quotes:** Include one attributed quote from Mark Edmondson. Make it sound natural, not corporate.
- **Metrics:** Lead with concrete numbers where available (96.6% accuracy, 48x speed, etc.).
- **No code snippets.** Link to docs for technical details.
- **Dateline:** Always "COPENHAGEN, Denmark" (company headquarters).

---

### Writing Guidelines (both formats)

- **Tone:** Enthusiastic but grounded. No hype words ("revolutionary", "game-changing"). Be specific about what the product does.
- **Audience:** Technical decision-makers and developers. Accessible but not dumbed down.
- **Length:** 800-1500 words.
- **Examples:** Include at least one concrete example, code snippet, or use case.
- **Admonitions:** Use `:::tip`, `:::info`, `:::note` for callouts where helpful.
- **Components:** Do NOT use custom React components (AudioPlayer, CogFlow, etc.) — keep it simple markdown.
- **Images:** If no banner image exists, add a comment in the PR body noting that a banner image is needed before merge. Do not leave a broken image reference — comment it out or omit the `image:` frontmatter field.
- **Links:** Always link to official docs, GitHub repos, and the Sunholo website where relevant.
- **Sunholo brand:** The company is Holosun ApS, brand name Sunholo. Products: AILANG, Multivac, DocParse, sunholo-py.

### Phase 4: Validate

Run `yarn build` to verify the post compiles without errors (broken links, bad frontmatter, etc.). Fix any issues before proceeding.

### Phase 5: Publish (Create PR)

Use `product-launch` or `press-release` in the branch name to match the format.

```bash
# Create branch (use press-release/ prefix for press releases)
git checkout -b blog/FORMAT-SLUG
# e.g., blog/product-launch-ailang-v08  or  blog/press-release-docparse-cloud

# Stage the post (and any images)
git add blog/YYYY-MM-DD-SLUG.md
# git add blog/img/SLUG-banner.webp  # if image was added

# Commit
git commit -m "Add FORMAT: TITLE"

# Push
git push -u origin blog/FORMAT-SLUG

# Create PR
gh pr create \
  --title "Blog: TITLE" \
  --body "## FORMAT_TYPE

- **Product:** PRODUCT_NAME
- **Author:** Solaris (AI)
- **Format:** Product Launch / Press Release
- **Post:** blog/YYYY-MM-DD-SLUG.md

### Summary
BRIEF_DESCRIPTION_OF_POST

### Pre-merge checklist
- [ ] Content reviewed by human editor
- [ ] Banner image added (if missing)
- [ ] Links verified
- [ ] Tone and accuracy checked
- [ ] Quote attributed correctly (press releases)

---
Generated by the product-launch skill."
```

### Output Markers

After completing the workflow, output these markers for AILANG agent integration:

```
POST_PATH: blog/YYYY-MM-DD-SLUG.md
PR_URL: https://github.com/sunholo-data/blog/pull/N
BRANCH_NAME: blog/product-launch-SLUG
```
