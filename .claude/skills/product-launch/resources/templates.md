# Blog Post Templates

## Product Launch Post Template

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

HOOK_PARAGRAPH — What problem does this solve? Why should the reader care? Make it compelling and specific. Lead with the user's pain point, not the product name.

<!-- truncate -->

## What is PRODUCT?

2-3 paragraphs explaining the product. Focus on value and outcomes, not implementation details. Answer: what does it do, who is it for, why does it matter?

## Key Features

- **Feature 1** — Brief explanation of why it matters to the user
- **Feature 2** — Brief explanation with a concrete benefit
- **Feature 3** — Brief explanation

:::tip
Include a callout for the most compelling feature or use case.
:::

## Getting Started

Practical steps: installation, first use, or where to go next. Include a brief code snippet or command if appropriate.

```bash
# Example installation or first-use command
```

## What's New in VERSION

(Include this section only for version-specific announcements)

Highlight the most impactful changes from the changelog. Focus on what users can now do that they couldn't before.

## Learn More

- [Documentation](DOCS_URL)
- [GitHub](GITHUB_URL)
- [Website](https://sunholo.com)
```

### Product Launch Sections Guide

| Section | Required? | Notes |
|---------|-----------|-------|
| Hook paragraph | Yes | Before truncate. 2-3 sentences max. |
| What is PRODUCT? | Yes | Core explanation |
| Key Features | Yes | 3-5 bullets |
| Getting Started | Yes | At least a link; ideally a code snippet |
| What's New | Only for version-specific | Skip for general product introductions |
| Learn More | Yes | Always include links |

---

## Press Release Template

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

**COPENHAGEN, Denmark — Month Day, Year —** Sunholo today announced WHAT, enabling WHO to DO_WHAT. The PRODUCT delivers CORE_BENEFIT, addressing MARKET_NEED.

<!-- truncate -->

PARAGRAPH_2 — Expand on the announcement. What does it do? How does it work at a high level? Include a concrete metric if available.

PARAGRAPH_3 — Business context. What market need does this address? What pain point does it solve? Scale or competitive positioning.

> "Quote about why this matters and what it means for customers. Should sound like a real person speaking, not marketing copy."
> — Mark Edmondson, Founder, Sunholo

## Key Highlights

- **Highlight 1** — concrete metric or capability (e.g., "96.6% accuracy across 10+ document formats")
- **Highlight 2** — business benefit (e.g., "Reduces processing time from 16 hours to 20 minutes")
- **Highlight 3** — availability or differentiation

## Availability

Describe how to get started: licensing model (Apache 2.0, commercial, etc.), pricing if applicable, where to download or sign up.

## About Sunholo

Sunholo (Holosun ApS) builds production AI systems for enterprises. Products include AILANG, a deterministic language for AI code synthesis; Multivac, an enterprise AI platform; and DocParse, universal document parsing. Based in Copenhagen, Denmark. Learn more at [sunholo.com](https://sunholo.com).

## Links

- [Product page](PRODUCT_URL)
- [Documentation](DOCS_URL)
- [GitHub](GITHUB_URL)
```

### Press Release Structure Guide

| Section | Required? | Notes |
|---------|-----------|-------|
| Dateline | Yes | Always "COPENHAGEN, Denmark — Month Day, Year —" |
| Lead paragraph | Yes | Who, what, when, where, why in one paragraph |
| Supporting paragraphs | Yes | 2-3 paragraphs of detail |
| Quote | Yes | Attributed to Mark Edmondson. Natural tone. |
| Key Highlights | Yes | 3-5 bullets with metrics |
| Availability | Yes | How to get started |
| About Sunholo | Yes | Standard boilerplate (copy verbatim) |
| Links | Yes | Product, docs, GitHub |

---

## Retroactive Post Additions

For posts covering past releases, add this admonition immediately after the AI disclosure:

```markdown
:::note[Retroactive Announcement]
This announcement was prepared in March 2026 to document the original release from [DATE].
:::
```

Use the original release date in the filename (e.g., `2025-09-26-ailang-launch.md`).
