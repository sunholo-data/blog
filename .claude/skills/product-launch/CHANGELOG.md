# Changelog - product-launch

Track improvements and evolution of this skill.

## 2026-03-26 - Rebuild with skill-builder conventions

**Change:**
- Rewrote SKILL.md for progressive disclosure (<130 lines, down from 268)
- Created 4 scripts: research_product.sh, create_post.sh, validate_post.sh, publish_post.sh
- Created 3 resources: templates.md, writing_guidelines.md, product_repos.md
- Added self-improvement section

**Impact:**
- Templates and guidelines no longer bloat the always-loaded SKILL.md
- Scripts automate research, scaffolding, validation, and publishing
- validate_post.sh catches common errors before human review

---

## 2026-03-26 - Initial Creation

- Created product-launch skill with two content formats (product launch + press release)
- Added Solaris (AI) author persona
- Integrated with AILANG coordinator as blog-launcher agent
- Support for retroactive posts with original release dates
