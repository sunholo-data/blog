# Sunholo Blog

Docusaurus 3.9.2 blog-only site deployed at `https://www.sunholo.com/blog/`.

## Blog Posts

- Location: `blog/YYYY-MM-DD-slug.md` (or `.mdx` for React components)
- Images: `blog/img/`
- Static assets: `static/img/`
- Excerpt cutoff: `<!-- truncate -->`

### Frontmatter

```yaml
---
title: "Post Title"
authors: me                    # or solaris for AI product launches
tags: [tag1, tag2]
image: ./img/filename.webp     # social sharing image
slug: /custom-slug             # optional
---
```

### Authors

Defined in `blog/authors.yml`:
- `me` — Mark Edmondson (Founder, human-authored posts)
- `solaris` — Solaris (AI), product announcements and launch posts

### Available Components (MDX only)

- `<AudioPlayer src="url" />` — podcast/audio player
- `<MultivacChatMessage />` — chat interface
- `<CogFlow nodes={} edges={} />` — flow diagrams
- `<ProtocolComparison />` — protocol timeline
- `<CustomPlot />` / `<Highlight />` — charts and highlights

## Solaris (AI) Content Types

All AI-generated content uses author `solaris` and must include an AI disclosure admonition. Two formats:

### Product Launch Posts
- Tag: `product-launch` (plus product-specific tags)
- Slug: `/slug-name`
- Tone: forward-thinking, ambitious, developer-friendly
- Length: 800-1500 words
- Includes code snippets, getting started steps

### Press Releases
- Tag: `press-release` (plus product-specific tags)
- Slug: `/press-slug-name` (note the `press-` prefix)
- Tone: formal third-person ("Sunholo today announced...")
- Length: 400-800 words
- Dateline: "COPENHAGEN, Denmark"
- Includes attributed quote from Mark Edmondson
- No code snippets; link to docs for technical details

### Retroactive Posts
Posts covering past releases use the original release date in the filename and include:
```
:::note[Retroactive Announcement]
This announcement was prepared in March 2026 to document the original release from [DATE].
:::
```

### Common Rules
- Must include AI disclosure admonition at the top
- Use simple markdown (no custom React components)
- Major releases may get both a press release AND a product launch post
- **Use real product screenshots and examples** — prefer actual UI screenshots, demo outputs, and CLI results over AI-generated illustrations. Check product and demo repos for existing screenshots before generating new images. Copy into `blog/img/` and convert to `.webp` where possible.

## Substack

Two directions, do not confuse them:

- **Blog → Substack** (normal): write here first, then adapt into `substack/` for
  pasting into Substack's rich-text editor. See `substack/SUBSTACK-GUIDE.md` (local, gitignored).
- **Substack → Blog** (catching up): a weekly post went out on Substack first and
  needs mirroring here for SEO. See `scripts/MIRRORING-GUIDE.md`.

The Substack RSS feed (`markedmondson.substack.com/feed`) carries **full post
content** for the last ~19 posts, so mirroring needs no pasted URLs:

```bash
python3 scripts/mirror_substack.py --refresh list   # what is not mirrored yet
python3 scripts/mirror_substack.py fetch <fragment> <slug>
python3 scripts/mirror_substack.py assemble <config.json>
```

Mirrors are **verbatim** (fix conversion artifacts only, no re-editing) with **no**
"originally published on Substack" note. Writing real alt text requires actually
looking at each image — the fetch step leaves alt empty on purpose.

After merging a mirror, set the canonical URL on the **Substack** post to the
`sunholo.com/blog/...` equivalent. Without that, Substack keeps the ranking.

## Product Repos (for research)

| Product | Repo Path |
|---------|-----------|
| AILANG | `/Users/mark/dev/sunholo/ailang` |
| Multivac | `/Users/mark/dev/sunholo/multivac` |
| AILANG Cloud | `/Users/mark/dev/sunholo/ailang-multivac` |
| DocParse | `/Users/mark/dev/sunholo/docparse` |
| sunholo-py | `/Users/mark/dev/sunholo/sunholo-py` |
| Website | `/Users/mark/dev/sunholo/website` |

## Build & Dev

```bash
yarn start    # dev server
yarn build    # production build (validates links)
yarn serve    # serve production build locally
```

Requires Node >= 20.

## Git Workflow

- Use feature branches: `blog/product-launch-SLUG` or `blog/press-release-SLUG`
- Create PRs and merge to main to trigger deploy
- Deploy is automatic via GitHub Pages on push to `main` (`.github/workflows/deploy.yml`)
