# Writing Guidelines

## Brand Voice

**Sunholo** (brand name) / **Holosun ApS** (legal entity)
Based in Copenhagen, Denmark.

### Products
- **AILANG** — deterministic language for AI code synthesis (Apache 2.0)
- **Multivac** — enterprise AI platform, prototype to production
- **DocParse** — universal document parsing (10+ formats)
- **sunholo-py** — AI DevOps framework for GCP (PyPI package)
- **AILANG Cloud** — managed cloud coordinator infrastructure

### Key People
- **Mark Edmondson** — Founder. Use for attributed quotes in press releases.

## Style Model: Google's "The Keyword" Blog

Our product launch style is modeled on Google's official blog ("The Keyword"). Key principles:

### Voice & Perspective
- **First-person plural ("we")** — "Today we're introducing..." / "We built this because..."
- **Directly address the reader ("you")** — "You can try it now" / "Here's what this means for you"
- **Conversational but confident** — Not stiff corporate prose, not breathless hype. The tone of an engineer explaining something they built and are proud of.
- **Inclusive, not exclusive** — Explain jargon when first used. Write so a technical PM understands, not just a compiler engineer.

### Opening Pattern
Google product posts almost always open with one of these patterns:

1. **The "Today we're" lead** — Direct announcement, benefit in the first sentence.
   > "Today we're making Gemini 2.5 Flash available to all developers — our fastest model yet, with improved reasoning across code, math, and multimodal tasks."

2. **The problem-then-solution lead** — One sentence of context, then the announcement.
   > "Developers have told us that switching between models for speed and quality is a constant tradeoff. Starting today, Gemini 2.5 Flash eliminates that choice."

3. **The user-benefit lead** — Start with what the reader can now do.
   > "You can now talk to your documents. Voice DocParse lets you upload a file and ask questions about it conversationally."

**Avoid:**
- "We're excited to announce..." (overused, Google themselves have moved away from this)
- Opening with the company name ("Sunholo today released...") — save this for press releases only
- Opening with history or background — lead with the news

### Feature Presentation
Google presents features as **benefit → evidence → try-it**:

1. **State what it does for the user** (one sentence, plain language)
2. **Back it up** with a number, benchmark, or concrete example
3. **Show how to use it** (link, CLI command, or code snippet)

**Example:**
> **Deterministic Office parsing** — DOCX, PPTX, and XLSX parsed via XML extraction. No AI needed, instant results, zero cost.
>
> On the OfficeDocBench benchmark, DocParse scores 96.6% — ahead of Unstructured, Docling, and LlamaParse on structural accuracy.
>
> ```bash
> docparse report.docx
> ```

Features should be grouped under clear section headers. Use short paragraphs (2-3 sentences max) — not walls of text.

### Numbers & Metrics
Google always includes concrete numbers. Follow these rules:
- **Prefer specific over vague** — "53 golden benchmarks" not "extensive testing"
- **Use comparisons** — "5x faster than..." / "96.6% vs competitors' 81%"
- **Include unit context** — "5 concurrent DOCX files in 26ms on Apple M2"
- **Don't overload** — 2-3 key metrics per section, not a data dump

### Tone Calibration

| Too cold (press release) | Right (Google blog) | Too hot (hype) |
|--------------------------|---------------------|----------------|
| "Sunholo announced availability of..." | "Today we're launching..." | "We're thrilled to unveil our revolutionary..." |
| "The solution addresses enterprise needs" | "This means you can now..." | "This changes everything about..." |
| "Performance improvements were observed" | "It's 3x faster on our benchmarks" | "Blazing fast, best-in-class performance" |

### Structure Flow
Google product launches follow this arc:

```
1. HOOK (1-2 sentences)
   What's new + why it matters to you

2. <!-- truncate -->

3. WHAT IT IS (1 paragraph)
   Plain-language explanation of the product/feature

4. KEY FEATURES (3-5 sections)
   Each: benefit statement → evidence → example/code
   Use section headers (##)

5. HOW TO GET STARTED
   Concrete steps: install, configure, first command
   Code snippets, links to docs

6. LEARN MORE
   Links to docs, GitHub, demos, community
```

### Paragraph & Sentence Style
- **Short paragraphs** — 2-3 sentences max. Blog posts are scanned, not read linearly.
- **Short sentences** — Break complex ideas into multiple sentences. "AILANG's effect system tracks every side effect in the type system. A function typed `-> string ! {IO, Net}` can't touch the filesystem. A function typed `-> int` is guaranteed pure."
- **Bold key terms** on first use — helps scanners find what matters.
- **Active voice** — "DocParse extracts tables" not "Tables are extracted by DocParse"
- **Present tense** — "AILANG verifies contracts at compile time" not "AILANG will verify..."

### Call-to-Action Style
Google always gives the reader something to do next:
- **Try it now:** "Install and start parsing in under a minute"
- **See it live:** "Try the [live demo](https://www.sunholo.com/ailang-demos/docparse.html) in your browser"
- **Go deeper:** "Read the [full documentation](https://ailang.sunholo.com)"
- Multiple CTAs throughout the post, not just at the end

## Tone by Format

### Product Launch Posts
- **Conversational "we/you" voice** — Google-style, as described above
- **Developer-friendly** — Include code snippets, CLI commands, practical steps
- **Specific** — "Parses 10+ document formats with 96.6% accuracy" not "industry-leading accuracy"
- **Problem-first hook** — Lead with the pain point or what's now possible, then the solution

### Press Releases
- **Formal third-person** — "Sunholo today announced..." (this is the one format where formal tone is correct)
- **Dense and factual** — Every sentence carries information
- **Metrics-forward** — Lead with numbers: speed, accuracy, cost savings
- **Quotable** — Write quotes that sound natural, not corporate

## Words to Avoid

| Avoid | Use Instead |
|-------|-------------|
| Revolutionary | Specific description of what changed |
| Game-changing | Concrete metric or comparison |
| Cutting-edge | Describe the actual technology |
| Leverage | Use |
| Synergy | Integration, combination |
| Best-in-class | Specific benchmark result |
| Seamless | Describe how the integration works |
| State-of-the-art | Current approach, latest method |
| We're excited to announce | Today we're launching / introducing / making available |
| Pleased to | Just state the fact |
| Proud to | Just state the fact |
| World-class | Specific evidence |

## Words to Use

- **Deterministic** — core AILANG value prop
- **Production-ready** — Multivac's positioning
- **Enterprise** — target market
- **Open source** — where applicable (Apache 2.0)
- **Prototype to production** — Multivac tagline
- **Today** — for announcements ("Today we're launching...")
- **You can now** — for user-facing features
- **Here's how** — to introduce getting started sections

## Structure Guidelines

### Hooks (opening paragraph)
- Lead with what's new and why it matters to the reader
- Use "Today we're..." or problem-then-solution pattern
- Keep to 2-3 sentences before the truncate marker
- Be specific: "Parsing a Word document shouldn't require a GPU" not "Document processing is hard"

### Code Snippets (product launches only)
- Keep to 5-10 lines maximum
- Show the simplest meaningful example
- Include comments only where the code isn't self-explanatory
- Use bash for CLI, the product's language for code

### Links
- Always link to official docs when mentioning a feature
- Link to GitHub repos for open source products
- Link to live demos when available
- Link to sunholo.com for commercial/enterprise info
- Never use bare URLs — always markdown links
- Scatter CTAs throughout, not just at the end

### Images
- Banner images go in `blog/img/`
- Use `.webp` format when possible (smaller files)
- Include product logos/icons inline where appropriate (from branding.md)
- If no image available, omit the `image:` frontmatter field (don't leave a broken reference)

### Screenshots & Product Examples
- **Prefer real product screenshots over generated images** — actual UI screenshots and demo outputs are more credible and useful than AI-generated illustrations
- Copy screenshots from product/demo repos into `blog/img/` (convert to `.webp` where possible)
- Include at least one real screenshot or product output per product launch post
- Show the product doing something real: a parsed document, a running demo, a dashboard view, a CLI output
- Available screenshot sources:
  - Demo thumbnails: `demos/site/thumbnails/` (docparse, extractor, ecommerce, streaming demos)
  - Website builder: `demos/website_builder/docs/screenshots/` (dashboard, upload, builder selection, cloud build)
  - DocParse demo: `demos/invoice_processor_wasm/assets/doc_parse_demo_screenshot.png`
  - Ecommerce dashboard: `demos/ecommerce/img/ecommerce-dashboard-ui.png`
  - Ambient assistant: `demos/streaming/ambient_assistant/ambient-demo.png`
- AILANG docs site: `ailang/docs/static/img/` (logo, social card, dashboard screenshots, cloud trace)
- Also check ailang.sunholo.com docs pages for any new images added over time
- When writing about a demo or feature, check the product repo for existing screenshots before generating new images

## Docusaurus Features

### Admonitions
```markdown
:::tip[Optional Title]
Helpful tip content — use for "try this first" recommendations
:::

:::info[Optional Title]
Informational content — use for AI disclosure
:::

:::note[Optional Title]
Noteworthy content — use for retroactive announcement notes
:::

:::warning[Optional Title]
Warning content — use sparingly
:::
```

### Truncate Marker
Always include `<!-- truncate -->` after the hook paragraph. This controls the excerpt shown on the blog index page.

## Quality Checklist

Before submitting for review:
- [ ] Opens with "Today we're..." or problem-then-solution hook (not "We're excited to...")
- [ ] Uses "we/you" voice throughout (not third-person, except press releases)
- [ ] Short paragraphs (2-3 sentences max)
- [ ] Every feature claim backed by a number, benchmark, or concrete example
- [ ] At least one code snippet or CLI command (product launches)
- [ ] At least one CTA in the middle of the post, not just at the end
- [ ] No placeholder text remaining
- [ ] All links are real URLs (not DOCS_URL etc.)
- [ ] AI disclosure admonition is first content after frontmatter
- [ ] Truncate marker is after the hook paragraph
- [ ] Word count is in target range (800-1500 launch, 400-800 press)
- [ ] Slug is set and meaningful
- [ ] Tags include the format tag + product tag
- [ ] Product logo/icon included where appropriate
- [ ] At least one real product screenshot or demo output included (not just AI-generated banners)
