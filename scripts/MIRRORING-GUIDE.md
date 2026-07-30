# Substack → Blog Mirroring Guide

How to mirror posts published on Substack **back** into this blog.

This is the reverse of `substack/SUBSTACK-GUIDE.md` (untracked, local only), which covers the
normal blog-first flow (write here, adapt for Substack). Use this guide when a post
went out on Substack first and the blog needs to catch up.

Tool: [`mirror_substack.py`](./mirror_substack.py) (stdlib only,
needs `cwebp` — `brew install webp`).

## Why bother

Substack pages rank worse for us than `sunholo.com/blog`, and posts that only exist
on Substack are invisible to the blog's tag pages, search and internal linking.

## The key fact

`https://markedmondson.substack.com/feed` returns the **last ~19 posts with full
content** in `<content:encoded>` — not excerpts. So mirroring needs no pasted URLs,
no login and no scraping.

Caveat: only ~19 posts. Anything older has aged out of the feed and would need
another source.

## Workflow

### 1. Find the gap

```bash
python3 scripts/mirror_substack.py --refresh list
```

Prints every feed post against the blog, marking each `yes` / `?` / `NO`. Matching
is fuzzy on the title because mirrored posts are sometimes retitled for the blog
(e.g. Substack's *"Can I trust AI?" is the wrong question* is
`2026-04-19-wrong-question-ai-trust.mdx` here). Confirmed pairs whose titles diverge
go in [`mirrored-overrides.json`](./mirrored-overrides.json) so they stop showing up
as ambiguous.

### 2. Fetch each missing post

```bash
python3 scripts/mirror_substack.py fetch <url-fragment> <blog-slug>
```

`<url-fragment>` is any distinctive part of the Substack URL (`using-ai-to-buy`).
This writes `.substack-staging/<slug>.body.md` plus `<slug>.meta.json`, and downloads
images to `.substack-staging/img/<slug>/`. Staging is gitignored.

Image alt text is deliberately left **empty** at this stage.

### 3. Look at every image

Actually open them. This is where the judgement is:

- write real alt text describing what the image *shows* (SEO + accessibility)
- pick a descriptive filename
- choose which image is the hero (the social card)
- confirm orientation is right

### 4. Write the config

One JSON array covering every post — see
[`mirror-config.example.json`](./mirror-config.example.json). Per post: `date`,
`slug`, `title`, `tags`, `hero`, `description`, and an `images` map of
`"<n>": ["<filename-stem>", "<alt text>"]` keyed by the image's order in the post.

Tags should reuse the existing vocabulary (`ailang`, `ai-delegation`, `agents`,
`ai-coding`, `ai-protocols`, `mcp`, `conferences`…) — check with:

```bash
grep -h "^tags:" blog/*.md blog/*.mdx | tr -d '[]' | sed 's/tags: //' \
  | tr ',' '\n' | tr -d ' ' | sort | uniq -c | sort -rn
```

### 5. Assemble and build

```bash
python3 scripts/mirror_substack.py assemble scripts/my-config.json
yarn build
```

### 6. Check fidelity

Word-count the result against the source to prove nothing was dropped. Expect a
diff of only the stripped `[Subscribe now]` CTAs.

### 7. Ship

Feature branch `blog/mirror-...`, PR, merge. Deploy runs on push to `main`.

### 8. Set the canonical URLs (do not skip)

**This is the step that actually fixes the SEO.** Mirroring alone leaves the blog
looking like the duplicate, because Substack published first. For each mirrored post,
open its Substack settings and set the canonical URL to the
`https://www.sunholo.com/blog/<slug>` equivalent. Manual, per post, in Substack.

## Conversion gotchas

These are all handled by the script; listed so they are not re-discovered.

| Problem | Why | Handling |
|---|---|---|
| iPhone photos upside down | The raw S3 original in `data-attrs` carries EXIF orientation and `cwebp` ignores EXIF | Download the rendered `substackcdn` `<img src>` instead, which has orientation baked in |
| Image counts look ~6x too high | `srcset` variants are all distinct URLs | Count `<figure>` elements |
| Extension lies | The CDN URL ends `.png` but serves `f_auto` | Sniff format from magic bytes |
| `**Read - **naively` | Substack writes `<strong>Read - </strong>`; `** x **` is not bold in markdown | Move padding whitespace outside the markers, at parse time |
| `](url)word` run together | Substack writes `<a>Fable 5.0 </a>` — the trailing space inside the anchor is the only word separator | Same padding fix; never strip spaces inside `[ ... ]` |
| MDX build fails | MDX reads `<1s` as JSX and evaluates `{verdict, proposed_fix}` as JavaScript | Escape `<`, `{`, `}` in prose |
| Nested lists flattened, numbering restarts | A blank line before a nested list closes the parent item; and stripping leading spaces destroys nesting | Indent past the parent marker (`- ` = 2 cols, `1. ` = 3), no blank line, never strip list indentation |
| Bullets split across lines | Substack nests `<p>` inside `<li>` | Suppress paragraph breaks inside list items |
| Stray `Subscribe now` link | Some CTAs sit outside a widget div and survive as bare links | Regex-stripped in `tidy()` |
| Heading levels collide | Substack's biggest header is `h1`, but the post title is already the page `h1` | Shift so the top level used lands on `h2`, preserving relative structure |
| `an .ail` becomes `an.ail` | Over-eager "space before punctuation" cleanup | Only strip before punctuation followed by whitespace |

## Editorial defaults

Confirmed with Mark for the June–July 2026 backlog:

- **Verbatim** mirror — fix conversion artifacts only, do not re-edit the prose
- **No** "originally published on Substack" note or footer link
- Images self-hosted under `blog/img/<slug>/`, webp where smaller
