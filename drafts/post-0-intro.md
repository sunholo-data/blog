# Post 0 — The wrong question about AI trust

**Status:** skeleton — fill with prose
**Target length:** 1200–1500 words
**Publishing slot:** series opener (week 1)
**Primary venue:** Substack, cross-post to Sunholo blog
**Author tag:** `me`
**Tags:** `ai-delegation`, `trust`, `authority`
**Hero visual:** [programming-language-performance-heatmap.png](/Users/mark/dev/sunholo/ailang/docs/static/img/programming-language-performance-heatmap.png) — the counterintuitive "better models benefit more from structure" chart

---

## 1. Hook (~150 words)

**Lead with the reframe.** "Do I trust this AI?" is a feeling, not a question. Replace it with five concrete ones a manager would ask of any delegate — human or artificial.

Points to hit:
- The five questions (what is it allowed to touch / will it do the same thing twice / can I see what it did / are there fewer ways for it to go wrong / does it say when it doesn't know)
- One-line frame: *these are the questions a good manager asks of a junior hire — and, it turns out, the questions AILANG answers at the language level*
- Don't explain AILANG yet — just the claim that the questions generalise

---

## 2. The shift that makes this urgent (~200 words)

**One central point:** the code-writer changed; the language didn't. Our *institutions* were built for humans. Stuffing AI into them unchanged is the bug.

Mandatory quote (keep verbatim):
> "Human programming languages optimize for: Comfort — familiar syntax, IDE support, autocompletion; Ambiguity — multiple ways to express the same thing; Speed — fast typing, shortcuts, implicit behaviors."
> — [VISION.md:8-11](/Users/mark/dev/sunholo/ailang/docs/VISION.md)

And:
> "A language isn't just syntax and semantics. It's also learnability — and in 2025, that means learnability by machines."
> — [talk-building-a-language.md:66](/Users/mark/dev/sunholo/ailang/docs/talk-building-a-language.md)

Bridge line: *what's true of languages is true of contracts, approvals, policies. We are putting AI into processes designed for embarrassable humans, and wondering why it goes wrong.*

---

## 3. The five principles (~600 words — ~120 per principle)

One paragraph each. Each ends with the anchor incident that will open the dedicated post.

### Principle 1 — Declared authority beats assumed authority
- Contractor scope metaphor (one sentence)
- Anything undeclared = denied
- Anchor: **Replit AI deletes SaaStr's production database during a code freeze, July 2025** → *more on this next week*

### Principle 2 — Reproducibility is the precondition of trust
- Recipe vs improvisation (one sentence)
- If you can't replay it, you can't audit it
- Anchor: ***Moffatt v. Air Canada* — the chatbot that invented a refund policy and the tribunal that called the airline's defence "remarkable"** → *more in Post 2*

### Principle 3 — Visibility, not opacity, produces authority
- You can't see inside the model's head. You can see everything around it.
- Most honest framing: explainability-of-thought is fantasy; explainability-of-action is mandatory
- Anchor: **Anthropic's own research showing Claude's stated reasoning isn't faithful** → *Post 3*

### Principle 4 — Entropy doesn't disappear. It just moves.
- Ambiguity is a conserved quantity — pay at design time, runtime, or postmortem
- Power-relationship inversion: AI *demands* upstream decisiveness from you
- Anchor: **why "don't hallucinate" is the archetypal broken prompt** → *Post 4*

### Principle 5 — Errors must be refused, not swallowed
- Silent failure is how trust collapses all at once
- Any AI that can't say "I don't know" is lying to you
- Anchor: **NYC's MyCity chatbot told business owners wage theft and housing discrimination are fine; Mayor Mamdani killed it January 2026** → *Post 5 (series finale)*

---

## 4. The counterintuitive finding (~150 words)

**Make this a pull-out, with the heatmap image.** Strong shareable hook:

From AILANG's benchmarks:

| Model | AILANG | Python | Delta |
|---|---|---|---|
| Sonnet 4.6 | 82.0% | 72.0% | +10.0 pp |
| Opus 4.6 | 84.3% | 74.5% | +9.8 pp |
| GPT-5 | 82.4% | 80.4% | +2.0 pp |

Punchline: **the better the model, the bigger the advantage from structure and constraint.** This is the opposite of the "AI needs freedom to be creative" narrative. For any task where trust matters, constraint compounds with capability.

General-audience analogy: give a senior employee a loose mandate and they do something impressive — but unaccountable. Give them a tight mandate with clear scope and they do their best work, auditably.

---

## 5. Three questions before granting authority (~150 words)

Reader-portable checklist. The closing payoff — they can use this before reading any other post.

1. **What capabilities has it declared, and what happens when it exceeds them?** If nothing, it has unbounded authority.
2. **Can I replay any decision it made, bit-for-bit, from the same inputs?** If not, its outputs are opinions, not records.
3. **Does it have a first-class way to say "I don't know"?** If not, every answer is overconfident by construction.

Closing line options (pick one or combine):
- *"A system that answers yes to all three is one you can delegate to. A system that answers no is one you're being delegated by."*
- *"Every widely-reported AI failure of the past three years is a failure of one of these five principles. None are failures of model capability."*

---

## 6. Series tease (~50 words)

Sign off: *"Over the next five weeks I'll take each of these apart with the specific cases that prove it. Next week: the Replit incident, iOS permissions, and what your AI agent is quietly allowed to touch."*

---

## Cutting-room floor — do NOT include in this post

- Detailed AILANG mechanics (effect syntax, entropy YAML schema) — save for the deep dives
- The Python/AILANG toy code contrasts — rhetorically weak, hold back
- Anthropic interpretability research detail — save for Post 3
- EU AI Act specifics — save for Post 3 or optional Post 6
- Entropy-budget equation, five axes — save for Post 4
- Circuit breakers / WHO checklist — save for Posts 4/5

## Editorial notes

- First-person, Mark voice, not Solaris. This is opinion writing.
- Do not pitch AILANG. It's the worked example, not the product.
- Round benchmark numbers (~+10 pp, not 10.0%) per [talk-building-a-language.md:199](/Users/mark/dev/sunholo/ailang/docs/talk-building-a-language.md)
- Headlines and subheads do most of the skim-reader's work; make them active and specific
