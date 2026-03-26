# Product Branding & Assets

## Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Sunholo Red (Primary) | `#e73c17` | Buttons, links, accents |
| Sunholo Red Dark | `#c42f0f` | Hover states |
| Sunholo Red Light | `#ff5a3c` | Dark mode primary |
| Charcoal | `#314352` | Secondary, body text |
| Teal | `#2c7a7b` | Accent, success states |
| Purple | `#6b46c1` | Feature highlights |
| Blog Primary | `#c94435` | Blog theme accent |

## Typography

- **Headings:** Montserrat (400-800)
- **Body:** Inter / Segoe UI fallback
- **Code:** JetBrains Mono / Fira Code fallback

## Product Logos

| Product | Logo Path | Format |
|---------|-----------|--------|
| AILANG | `/Users/mark/dev/sunholo/ailang/docs/static/img/ailang-logo.svg` | SVG |
| DocParse | `/Users/mark/dev/sunholo/docparse/docs/img/docparse-logo.svg` | SVG |
| DocParse Hero | `/Users/mark/dev/sunholo/docparse/docs/img/docparse-hero.svg` | SVG |
| Sunholo Corporate | `/Users/mark/dev/sunholo/demos/site/sunholo-logo.svg` | SVG |
| Blog Navbar | `/Users/mark/dev/sunholo/blog/static/img/eclipse1.png` | PNG |
| AILANG Social Card | `/Users/mark/dev/sunholo/ailang/docs/static/img/ailang-social-card.jpg` | JPG |
| Solaris Avatar | `/Users/mark/dev/sunholo/blog/static/img/solaris-avatar.svg` | SVG |

## Demo Category Icons

| Category | Icon Path |
|----------|-----------|
| Contract Verification | `/Users/mark/dev/sunholo/demos/site/demo-contract-verified.svg` |
| Document Intelligence | `/Users/mark/dev/sunholo/demos/site/demo-document-intelligence.svg` |
| Streaming & Voice | `/Users/mark/dev/sunholo/demos/site/demo-streaming-voice.svg` |
| AILANG Logo (demos) | `/Users/mark/dev/sunholo/demos/site/ailang-logo.svg` |
| Sunholo Logo (demos) | `/Users/mark/dev/sunholo/demos/site/sunholo-logo.svg` |

## Architecture Diagrams

| Diagram | Path |
|---------|------|
| Multivac Venn Diagram | `/Users/mark/dev/sunholo/website/landingpage/public/multivac-venn-diagram.svg` |
| Multivac Deployments | `/Users/mark/dev/sunholo/website/landingpage/public/images/multivac-deployments.svg` |
| Cloud Architecture | `/Users/mark/dev/sunholo/website/landingpage/public/images/multivac-cloud-architecture.svg` |

## Design System Files

| File | Location | Notes |
|------|----------|-------|
| Blog CSS | `/Users/mark/dev/sunholo/blog/src/css/custom.css` | Blog theme variables |
| AILANG Docs CSS | `/Users/mark/dev/sunholo/ailang/docs/src/css/custom.css` | Full design system (914 lines) |
| Website CSS | `/Users/mark/dev/sunholo/website/src/styles.css` | Marketing site styles |
| Demos Design System | `/Users/mark/dev/sunholo/demos/site/shared/design-system.css` | Shared design system (662 lines, 30+ CSS vars) |

## Banner Image Generation

Use the `generate_banner.sh` script with brand-consistent prompts:
```bash
.claude/skills/product-launch/scripts/generate_banner.sh SLUG "prompt"
```

**Style guidelines for AI-generated banners:**
- Use the Sunholo color palette (blue/red/teal/orange accents)
- Clean, modern tech illustration style
- 16:9 aspect ratio, no text overlays
- Consistent with the minimalist + gradient glow aesthetic used across products
