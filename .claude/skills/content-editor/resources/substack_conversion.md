# Docusaurus → Substack Conversion

Substack's editor is WYSIWYG, not markdown. Pasting markdown like `**bold**` or `[text](url)` leaves the syntax *literal* in the published post — you see the asterisks and brackets, not the formatting. This has bitten us. Generate a plain-text version, not a markdown version.

## Output location

Write to `blog/substack/<slug>.md` (create the `substack/` folder if needed). Never overwrite the canonical `.md`/`.mdx` source. The `substack/` folder may be gitignored — confirm before assuming it commits.

## The core rule: no markdown syntax survives the paste

Substack's editor:
- ✅ **Auto-hyperlinks bare URLs** on paste — so put URLs on their own lines (or inline as plain URLs)
- ✅ **Auto-linkifies URLs pasted on a new line after the anchor text** — text immediately above a bare URL gets linked if they're adjacent
- ❌ Does NOT parse `[text](url)` — it becomes literal `[text](url)` in the post
- ❌ Does NOT parse `**bold**` — it becomes literal `**bold**`
- ❌ Does NOT parse `*italic*` — becomes literal asterisks
- ❌ Does NOT parse `> blockquote` reliably — sometimes, sometimes not
- ❌ Does NOT parse `##` headings — becomes literal hash marks
- ❌ Does NOT parse image syntax `![alt](path)`

**Approach:** output plain prose. Leave formatting instructions as `[square-bracket notes]` for the author to apply manually in the Substack editor, and tell them to delete the brackets before publishing.

## Conversions

### Links
- Remove all `[text](url)` syntax.
- Two workable patterns:
  1. **Inline**: put the bare URL in the sentence. E.g. "Details at https://ida.dk/driving-ai where I'll talk about..." — Substack will auto-link the URL.
  2. **Break-line**: write the anchor-phrase sentence, then put the URL on its own line below. Easier for the author to then select the phrase and attach the URL via the editor's link tool.

### Bold / emphasis
- Remove all `**` and `*`. Express emphasis through prose: short punchy sentence, or put the claim on its own one-sentence paragraph.
- For a sentence the author definitely wants bold/pull-quoted, put it on its own line and add `[Format this line as a pull quote / blockquote in Substack.]` underneath.

### Headings
- Write the heading text on its own line with no `#` marks.
- Add `[Heading 2]` (or H3) on the next line so the author can apply the style in Substack.

### Images
- Remove `![alt](path)` syntax.
- Replace with `[IMAGE: <alt text> — upload <source path>]` on its own line where the image should go.
- Do NOT try to construct absolute URLs to the Docusaurus-deployed image — the site's asset-URL format is unstable (hashed filenames on build), so link-based images often 404 in the Substack post. Manual upload is more reliable.

### Admonitions
Flatten `:::note`, `:::tip`, etc. to a plain paragraph with a bold-marker prefix in prose, like `Note — Retroactive Announcement:` at the start of the paragraph. No markdown bold.

### Frontmatter
Strip. Put title/subtitle/tags/canonical at the very top of the file as plain labelled lines (not YAML, not HTML comments) so the author can eyeball and paste individually into Substack's editor fields.

### `<!-- truncate -->`
Remove entirely.

### MDX components
Strip. Replace each with `[IMAGE: screenshot of <component> — upload blog/img/<file>]` or plain text.

### Code blocks
Keep triple-backtick fenced blocks if the post is code-heavy — Substack DOES support pasted code blocks from some source formats, but test it. When in doubt, indent with 4 spaces and note `[Format as code block]`.

### Internal links
Rewrite relative links (`/blog/foo`, `/docs/bar`) to bare absolute URLs (`https://www.sunholo.com/blog/foo`) on their own lines.

## Editorial tweaks for Substack

- **Subtitle**: Substack has a dedicated subtitle field. Suggest one pulled from an early strong sentence — not a rephrasing of the title.
- **Hook**: Substack readers arrive via email. The first two sentences matter more. Consider a tighter opener than the Docusaurus version.
- **Pull quotes**: identify 1-2 tweetable lines and put them on their own line with `[Format as pull quote]` underneath.
- **Footer**: append a canonical-link footer as plain text:
  ```
  Originally published on the Sunholo blog: https://www.sunholo.com/blog/<slug>
  Subscribe there for more on [topic area].
  ```

## Header instructions for the author

Add a preamble at the top of the generated file:

```
(Paste-into-Substack notes: URLs below are bare so Substack auto-hyperlinks them on paste. No markdown syntax — select text in the Substack editor and apply bold/italic/link manually where you want emphasis. Suggested formatting is noted in [square brackets] — delete these before publishing.)
```

## Things to flag to the author

- Any component that couldn't be cleanly converted
- Any image needing manual upload (which is most of them)
- Whether the opening paragraph should be rewritten for email-reader context
- Any code block whose formatting may not survive the paste
