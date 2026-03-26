# Product Repository Map

## Repo Paths and Key Files

| Product | Repo Path | Key Files | Website |
|---------|-----------|-----------|---------|
| AILANG | `/Users/mark/dev/sunholo/ailang` | README.md, CHANGELOG.md, go.mod | [ailang.sunholo.com](https://ailang.sunholo.com) |
| AILANG Docs Site | `/Users/mark/dev/sunholo/ailang/docs` | docs/, guides/, static/img/ | [ailang.sunholo.com](https://ailang.sunholo.com) |
| Multivac | `/Users/mark/dev/sunholo/multivac` | README.md | [sunholo.com](https://sunholo.com) |
| AILANG Cloud | `/Users/mark/dev/sunholo/ailang-multivac` | README.md, terraform/ | — |
| DocParse | `/Users/mark/dev/sunholo/docparse` | README.md, CHANGELOG.md | [sunholo.com/docparse](https://sunholo.com/docparse) |
| sunholo-py | `/Users/mark/dev/sunholo/sunholo-py` | README.md, CHANGELOG.md, pyproject.toml | [PyPI](https://pypi.org/project/sunholo/) |
| Website | `/Users/mark/dev/sunholo/website` | README.md, src/ | [sunholo.com](https://sunholo.com) |
| AILANG Demos | `/Users/mark/dev/sunholo/demos` | README.md, site/index.html | [sunholo.com/ailang-demos](https://www.sunholo.com/ailang-demos/) |
| Stapledons Voyage | `/Users/mark/dev/sunholo/stapledons_voyage` | README.md, engine/handlers/ai_gemini*.go | — |
| Presentations | `/Users/mark/dev/sunholo/presentations` | Various .html files, images/ | [sunholo.com/presentations](https://www.sunholo.com/presentations/) |

## Product Tag Names

Use these as the product-specific tag in frontmatter:

| Product | Tag |
|---------|-----|
| AILANG | `ailang` |
| Multivac | `multivac` |
| AILANG Cloud | `ailang-cloud` |
| DocParse | `docparse` |
| sunholo-py | `sunholo-py` |
| AILANG Demos | `ailang-demos` |

## Product Descriptions (for reference)

### AILANG
A deterministic, purely functional language designed as an execution substrate for AI-generated code. Features: Hindley-Milner type inference, effect system with capability-based security, pattern matching, SMT-based contract verification. Apache 2.0 licensed. Current version: v0.9.x (March 2026).

**AILANG Documentation Site** (`ailang/docs/`): Full Docusaurus site at ailang.sunholo.com with 40+ pages covering guides (getting-started, contracts, streaming, serve-api, packages, agent-integration, WASM, telemetry, etc.), language reference (syntax, effects, modules, capability budgets, arrays), architecture docs, examples, benchmarks, roadmap, and playground. This is a major research source for any AILANG-related blog post — check here first for feature details, code examples, and screenshots.

### Multivac
Enterprise AI platform that takes GenAI from prototype to production in weeks instead of months. Claims: 3 weeks to production (vs 6-12 months), save €500K+ in development costs. Includes security (SSO, RBAC, encryption), auto-scaling, model versioning, A/B testing. Deployed on GCP.

### DocParse
Universal document parsing that extracts structured content from 10+ formats. Key differentiator: uses deterministic XML parsing for Office formats (DOCX, PPTX, XLSX) — no AI needed, instant results. AI-powered for PDFs and images. Built in AILANG. 96.6% accuracy benchmark vs competitors. Cloud API available.

### sunholo-py
AI DevOps framework for building GenAI applications on Google Cloud Platform. VAC (Virtual Agent Computer) concept — configuration-driven agents. Supports Vertex AI, OpenAI, Anthropic, Ollama. Deploys to Cloud Run. v0.146 includes ADK, multi-channel messaging, MCP discovery.

### AILANG Demos
Live interactive demo suite showcasing AILANG's capabilities. 15+ demos across document intelligence (DocParse browser, Document Extractor), streaming/voice (Ambient Assistant, Voice DocParse, Claude Chat, Gemini Live, Safe Agent), website builder (first AILANG Cloud use case), ecommerce vertical (6 demos including REST API + MCP + A2A), Z3 verification showcase, GA4 analytics, and LinkedIn marketing automation. Deployed at sunholo.com/ailang-demos via GitHub Pages. 100% AI-coded.

### AILANG Cloud
Cloud coordinator infrastructure for autonomous agent orchestration. Built on GCP: Pub/Sub messaging, Firestore state, Cloud Run services, OpenTelemetry tracing. Package registry for AILANG ecosystem. Multi-environment (dev/test/prod) with Terraform.

## GitHub Organization

- **Organization:** [sunholo-data](https://github.com/sunholo-data)
- **Bot account:** sunholo-voight-kampff
- **Blog repo:** sunholo-data/blog

## External Links

### Presentations
Conference slide decks with high-quality AILANG visuals. Key content:
- **"Building AI with AI"** (Oct 2025) — Procurement intelligence, Aitana dashboard screenshot.
- **"Multivac Platform"** (Apr 2024) — Platform overview, roadblocks visual, 4-icon design system.
- Unpublished decks also contain useful visuals (LoCoBench heatmap, "Boring Task" illustration, entropy visualizations) — use content but don't reference the presentation titles.
- Images at: `presentations/images/` (logos, case studies, talks).

- Main website: https://sunholo.com
- AILANG docs: https://ailang.sunholo.com
- Dev portal: https://dev.sunholo.com
- Discord: https://discord.gg/RANn65Rh9a
- GitHub: https://github.com/sunholo-data
