---
name: product-launch
description: Write product launch posts or press releases for Sunholo products. Use when user asks to write a product announcement, launch post, press release, product update, or says "announce PRODUCT". Also use when user says "retroactive post", "write about release", "blog about DocParse/AILANG/Multivac/sunholo-py", or wants marketing content for a product. Handles research, writing, validation, and PR creation. Posts are authored by Solaris (AI).
user-invokable: true
---

# Product Launch & Press Release

Research a Sunholo product, write a blog post or press release as Solaris (AI), and create a PR for human review.

## Quick Start

```
/product-launch announce AILANG v0.9 - focus on cloud packages
/product-launch press-release DocParse Cloud API launch
/product-launch retroactive AILANG v0.8 2026-02-13 - formal verification
```

## When to Use This Skill

- User asks to announce, write about, or promote a Sunholo product
- User wants a press release for a product milestone
- User says "retroactive post" for a past release
- User asks to blog about AILANG, DocParse, Multivac, sunholo-py, or AILANG Cloud
- User asks for marketing content or a product update post

## Content Formats

Two formats — detect from the user's prompt, or ask if ambiguous.

| | Product Launch Post | Press Release |
|---|---|---|
| **Trigger words** | "announce", "write about", "product launch" | "press release", "PR for" |
| **Tag** | `product-launch` | `press-release` |
| **Slug** | `/slug` | `/press-slug` |
| **Tone** | Enthusiastic, hands-on, developer-friendly | Formal third-person, business audience |
| **Length** | 800-1500 words | 400-800 words |
| **Content** | Features, code, getting started | Business significance, metrics, quotes |

Major releases (new products, x.0 versions) may warrant both formats.

## Workflow

### 1. Understand the Request

Parse the user's message for:
- **Format** — product launch or press release
- **Product** — see [resources/product_repos.md](resources/product_repos.md) for repo map
- **Focus** — specific version, feature, or general overview
- **Retroactive?** — if past date mentioned, use that date instead of today

### 2. Research

Run the research script to gather product info:
```bash
.claude/skills/product-launch/scripts/research_product.sh PRODUCT_NAME
```

Then manually read the key files it identifies. Extract:
- Product name and current version
- Core value proposition (1 sentence)
- Key features (3-5 bullets)
- What's new or noteworthy
- Getting started steps
- Links to docs, GitHub, website

Also check existing blog posts in `blog/` to avoid duplicating recent content.

### 3. Write the Content

Create the file using the scaffold script:
```bash
.claude/skills/product-launch/scripts/create_post.sh FORMAT SLUG [DATE]
# FORMAT: "launch" or "press"
# DATE: optional, defaults to today (use YYYY-MM-DD for retroactive)
```

Then fill in the content following the appropriate template.
See [resources/templates.md](resources/templates.md) for full templates.
See [resources/writing_guidelines.md](resources/writing_guidelines.md) for tone and style.

For retroactive posts, add after the AI disclosure:
```markdown
:::note[Retroactive Announcement]
This announcement was prepared in March 2026 to document the original release.
:::
```

### 4. Generate Banner Image

Generate a social sharing banner image using Gemini AI (via the `voyage` CLI from stapledons_voyage):
```bash
.claude/skills/product-launch/scripts/generate_banner.sh SLUG "prompt describing the image"
```

This generates a 16:9 2K image and saves it to `blog/img/SLUG.webp`. Then add the `image:` field to frontmatter:
```yaml
image: ./img/SLUG.webp
```

### 5. Validate

```bash
.claude/skills/product-launch/scripts/validate_post.sh blog/YYYY-MM-DD-SLUG.md
```

Checks frontmatter, AI disclosure, truncate marker, links, and runs `yarn build`.

### 5. Publish

```bash
.claude/skills/product-launch/scripts/publish_post.sh blog/YYYY-MM-DD-SLUG.md "Post Title"
```

Creates branch, commits, pushes, and opens a PR for human review.

### Output Markers

After completing the workflow, output these for AILANG agent integration:
```
POST_PATH: blog/YYYY-MM-DD-SLUG.md
PR_URL: https://github.com/sunholo-data/blog/pull/N
BRANCH_NAME: blog/FORMAT-SLUG
```

## Available Scripts

| Script | Purpose |
|--------|---------|
| `scripts/research_product.sh` | Gather product info from repo (README, CHANGELOG, version) |
| `scripts/create_post.sh` | Scaffold a new post file from template |
| `scripts/validate_post.sh` | Validate frontmatter, structure, and build |
| `scripts/generate_banner.sh` | Generate AI banner image via Gemini (voyage CLI) |
| `scripts/publish_post.sh` | Create branch, commit, push, and open PR |

## Resources

| Resource | Content |
|----------|---------|
| [branding.md](resources/branding.md) | Product logos, brand colors, design system files, demo icons |
| [templates.md](resources/templates.md) | Full templates for both content formats |
| [writing_guidelines.md](resources/writing_guidelines.md) | Tone, style, brand voice, common mistakes |
| [product_repos.md](resources/product_repos.md) | Product repo map with paths and key files |

## Progressive Disclosure

1. **Always loaded**: This SKILL.md (overview + workflow)
2. **Execute as needed**: Scripts in `scripts/` (research, scaffold, validate, publish)
3. **Load on demand**: Resources in `resources/` (templates, guidelines, repo map)

## Self-Improvement

This skill is self-improving. When you discover issues during execution:
1. Identify the issue (e.g., missing product in repo map, template needs adjustment)
2. Inform the user
3. Propose and implement the fix
4. Log the improvement in CHANGELOG.md
