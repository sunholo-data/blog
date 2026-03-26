---
title: "DocParse: Universal Document Parsing in AILANG"
authors: solaris
tags: [product-launch, docparse, ailang]
slug: /docparse-launch
image: ./img/docparse-launch.webp
---

Today we're launching **DocParse** — a universal document parser that extracts structured content from 10+ formats, built entirely in AILANG. It parses Office documents deterministically from XML, delegates to AI only for PDFs and images, and scores 96.6% on OfficeDocBench against Unstructured, Docling, and LlamaParse.

<!-- truncate -->

:::info[AI-Generated Content]
This product announcement was written by Solaris, Sunholo's AI communications assistant, and reviewed by the Sunholo team.
:::

:::note[Retroactive Announcement]
This announcement was prepared in March 2026 to document the original v0.8 release from March 19, 2026.
:::

![DocParse](./img/docparse-logo.svg)

## Parsing a Word document shouldn't require a GPU

Most document parsing tools treat every format the same way: convert to PDF, throw AI at it, hope for the best. That approach throws away tracked changes, comments, headers, footers, and precise table structure before even starting.

We took a different approach. Office formats (DOCX, PPTX, XLSX) are just ZIP archives containing XML. DocParse reads that XML directly — no cloud calls, no latency, no cost.

For PDFs and images, where the structure genuinely isn't in the file, DocParse delegates to whatever AI model you prefer. Swap `--ai` and nothing else changes. AI usage is bounded by AILANG's capability budgets (`AI @limit=20`), so costs stay predictable.

[Try DocParse in your browser](https://www.sunholo.com/ailang-demos/docparse.html) — no install needed.

## What we extract that competitors miss

| Feature | DOCX | PPTX | XLSX | Competitors |
|---------|------|------|------|-------------|
| Tables with merged cells | Yes | Yes | Yes | Buggy or missing |
| Track changes (redlining) | Yes | — | — | No |
| Comments (interleaved) | Yes | — | — | No |
| Headers/footers | Yes | — | — | Limited |
| Text boxes / VML shapes | Yes | Yes | — | Dropped silently |
| Speaker notes | — | Yes | — | Dropped |
| Multi-sheet extraction | — | — | Yes | Yes |

:::tip[Why deterministic parsing matters]
Most tools convert DOCX to PDF before extracting. That conversion loses tracked changes, comments, and precise table structure. We skip the middleman and read the XML directly — which is why we catch things competitors miss entirely.
:::

## Key features

**Deterministic Office parsing.** DOCX, PPTX, and XLSX parsed via XML extraction. No AI needed, instant results, zero cost.

**AI-agnostic PDF and image parsing.** Plug in Gemini, Claude, or a local Ollama model. Change the backend with a single flag, zero code changes.

**10+ input formats, 9 output formats.** Every run produces structured JSON with typed blocks and LLM-ready markdown. Cross-format conversion lets you go from CSV to DOCX or Markdown to PPTX.

**96.6% accuracy on OfficeDocBench.** Measured against Unstructured, Docling, and LlamaParse on structural accuracy for Office documents.

**28 contracts verified with Z3.** When DocParse says it parsed your document, the guarantees are mathematical, not aspirational.

## Get started in under a minute

Install and parse your first document:

```bash
git clone https://github.com/sunholo-data/docparse.git
ln -s "$(pwd)/docparse/bin/docparse" /usr/local/bin/docparse
```

Parse Office documents instantly — no API keys, no configuration:

```bash
docparse report.docx
docparse slides.pptx
docparse spreadsheet.xlsx
```

For PDFs and images, pick your AI backend:

```bash
docparse scan.pdf --ai gemini-3-flash-preview
docparse scan.pdf --ai claude-haiku-4-5
docparse scan.pdf --ai granite-docling  # Local Ollama, free
```

Output lands in `docparse/data/` as structured JSON and LLM-ready markdown.

## New in v0.8: Cloud API

We've brought DocParse to the cloud with an API that's compatible with the Unstructured API format. If you're already using Unstructured, you can point your existing client at our endpoint and get better results on Office formats without changing your code.

The Cloud API handles the same 10+ formats with the same deterministic parsing and pluggable AI backends.

## Built entirely in AILANG

DocParse is the first real-world application built entirely in [AILANG](https://github.com/sunholo-data/ailang). The entire codebase is 10 modules, 28 contracts, and roughly 3,600 lines of AILANG code.

```bash
docparse --check   # Type-check all 10 modules
docparse --test    # Run 51 inline tests
docparse --prove   # Static Z3 contract verification
```

This is what building with AILANG looks like in practice: deterministic logic handles what it can, AI fills in the gaps, and contracts ensure the output meets its guarantees regardless of which path executed.

## Learn more

- [Live demo](https://www.sunholo.com/ailang-demos/docparse.html) — try DocParse in your browser right now
- [GitHub](https://github.com/sunholo-data/docparse) — source code (Apache 2.0)
- [AILANG](https://github.com/sunholo-data/ailang) — the language DocParse is built in
- [Sunholo](https://sunholo.com) — enterprise AI systems
