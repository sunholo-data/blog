# Post 2 — If you can't replay it, you can't ship it

**Status:** skeleton — fill with prose
**Target length:** 1500–2000 words
**Publishing slot:** week 3
**Author tag:** `me`
**Tags:** `ai-delegation`, `reproducibility`, `determinism`, `code-quality`, `ailang`
**Hero visual:** side-by-side: Python's 5 ways to transform a list vs AILANG's 1. Or: same prompt, two different code outputs.
**Supporting visual:** the arXiv 68.3% reproducibility chart; AILANG benchmark comparison

---

## 1. Hook — Code is deterministic. AI-generated code isn't. (~300 words)

Open with the counterintuitive observation. No dramatic incident — the insight *is* the hook.

**The assumption everyone makes:**
- Code is deterministic. You run it, it does the same thing every time. That's the whole point of code — it's a recipe, not a conversation.
- So when an AI writes code for you, the output should be deterministic too, right? Same prompt, same code, same result.
- **Wrong.** The code is deterministic once it exists. The act of *generating* it is not.

**Why — and this is the part that surprises people:**
- Human programming languages were designed for human expressiveness. Python has at least five idiomatic ways to transform a list: list comprehension, `map()`, for-loop with append, generator expression, `filter()` + lambda. All correct. All different.
- A human developer picks one style and stays consistent (usually). They have preferences, team conventions, muscle memory.
- An AI has none of these. Each generation is a fresh sample from a probability distribution. It picks whichever form emerges from the dice roll *that particular run*. Next run, it picks differently. Both are correct Python. Neither is reproducible.

**What this actually means in practice:**
- You ask an AI to write a data-processing function on Monday. It gives you a list comprehension. Tests pass. You ship.
- On Tuesday, a colleague asks for the same function. The AI gives them a for-loop with append. Functionally identical. Structurally different. Their tests pass too.
- Now you have two implementations of the same logic in the same codebase, written by the same "developer," and neither of you knows why they're different. Try merging those branches.

**The frame for the post:** this is the second question you need to ask of any AI system: *can I replay what it did?* And for AI-generated code, the answer is almost always no — not because the AI is broken, but because the *language* gives it too many degrees of freedom.

---

## 2. The recipe vs improvisation frame (~150 words)

Brief universalisation — don't belabour, the hook already did the work:

- You can trust a recipe because it doesn't depend on the chef's mood. You can *love* improvisation but you can't certify it.
- The framing flip: **reproducibility isn't a nice-to-have — it's the precondition of every other property we want from AI-generated code. Testing. Caching. Auditing. Code review. Merging. All downstream of being able to replay the same generation twice.**
- And the reason we don't have it isn't that AI models are bad. It's that the languages they write in were designed for a different author.

---

## 3. The evidence: 68.3% and the dependency gap (~250 words)

Now bring in the data. The hook was conceptual; this section proves it empirically.

**The arXiv study (2512.22387) — "AI-Generated Code Is Not Reproducible (Yet)":**
- Researchers tested three leading AI coding agents — Claude Code, OpenAI Codex, and Gemini — across 300 projects generated from 100 standardised prompts in Python, JavaScript, and Java.
- Each project was tested in a clean environment using only the dependencies the model explicitly declared.
- Result: only **68.3% executed out-of-the-box**. Java was worst at **44%**.
- The killer finding: a **13.5x average expansion** from declared to actual runtime dependencies. The AI said it needed X; it actually needed 13.5 times X.

**What this tells us about reproducibility:**
- The AI doesn't just generate structurally different code each run — it generates code that *doesn't even know what it depends on*. The dependency gap isn't a minor bookkeeping error; it's a 13.5x chasm between what the model thinks it wrote and what the code actually requires.
- You can't reproduce what you can't even fully describe. If the AI can't declare its own dependencies correctly, how can you replay the build? How can you audit the supply chain? How can you trust that staging and production are running the same thing?

**Supporting industry data (one paragraph, don't dwell):**
- CodeRabbit: AI PRs have 1.7x more major issues, incidents per PR up 23.5%
- Veracode: AI code has 2.74x more vulnerabilities
- These are symptoms. The disease is non-reproducible generation.

Sources:
- [arXiv 2512.22387](https://arxiv.org/abs/2512.22387)
- [CodeRabbit report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)

---

## 4. Temperature=0 doesn't fix this (~200 words)

Brief technical sidebar — debunk the obvious objection.

- The first response from technical readers will be: "just set temperature to zero."
- Temperature controls randomness in token selection. At temperature=0, the model picks the single most probable next token every time. Sounds deterministic.
- It isn't, for several reasons:
  - Non-deterministic GPU math (floating-point reduction order varies between runs)
  - Silent model-version upgrades by the provider
  - Prompt-cache behaviour and context-window drift
  - System-prompt changes you don't see
- But even if temperature=0 *were* perfectly deterministic, **it wouldn't solve the structural problem.** The model would deterministically pick *one* of Python's five ways to transform a list. Change the prompt slightly — add a comment, reorder a paragraph — and it deterministically picks a *different* one. The language still has five doors; you're just fixing which door the AI walks through for that exact input.
- **The problem isn't randomness. The problem is optionality.** A language with five ways to do the same thing gives the AI five chances to be inconsistent — whether or not the token selection is stochastic.

---

## 5. What a language designed for AI does differently (~350 words)

This is the AILANG section. Lead with the design principle, then show the mechanics.

**The insight:**
- Every programming language makes a trade-off between expressiveness and consistency. Human languages (Python, JavaScript) maximise expressiveness: many ways to say the same thing, because human creativity thrives on choice.
- But AI doesn't need creative freedom in syntax. It needs a narrow, predictable target. Fewer ways to express the same logic = less entropy per generation = more reproducible output.
- This is the design thesis behind [AILANG](https://ailang.sunholo.com/): a programming language built for AI as the primary author, where reproducibility is a first-class design goal.

**How it works (keep it plain, three beats):**

1. **One canonical form per operation.** In Python, list transformation has 5+ idiomatic forms. In AILANG: `result = map(f, items)`. That's it. One way. The AI doesn't choose between forms because there's nothing to choose between. Same prompt → same structure → reproducible generation.

2. **Declared effects in the type signature.** Every function says what it touches: `func fetchData() -> string ! {Net}` means "this function uses the network and nothing else." No hidden side effects. No dependencies the AI forgot to mention. The type signature *is* the dependency declaration — and the compiler enforces it. (Compare: the arXiv study found a 13.5x gap between declared and actual dependencies. In AILANG, the compiler won't let that gap exist.)

3. **Environment pinning for deterministic execution.** `AILANG_SEED=42` pins the random-number generator. `TZ` pins the timezone. `AILANG_FS_SANDBOX` restricts filesystem access to a declared directory. Same inputs + same seed + same environment = identical output. Not approximately. Exactly.

**The benchmarks bear this out:**
- On IO tasks: AILANG-generated code is **+20 percentage points** more correct than Python-generated code from the same models.
- On contract/type-safety tasks: **+27.8 percentage points**.
- The better the model, the bigger the advantage — because structure gives capable models more to work with, not less.

**The trade-off, stated honestly:** AILANG is less expressive than Python for humans. That's by design. It trades human creative freedom for machine reproducibility. If a human is writing the code, you want Python. If an AI is writing the code, you want the narrowest target you can give it.

---

## 6. The sectors that already know this (~200 words)

Brief tour — regulated industries where reproducibility of generated code isn't theoretical.

- **Aviation (DO-178C):** AI-generated code is treated identically to human code for certification. Same verification, traceability, and audit requirements. You must be able to reproduce any build from source. The FAA doesn't care who wrote it — human or AI.
- **Medical devices (FDA):** January 2025 draft guidance requires Total Product Life Cycle documentation for AI-enabled software. If an AI generates code for a pacemaker, every line needs provenance.
- **Financial services:** SEC and FINRA are watching AI-generated trading algorithms. Regulators want reproducible builds and auditable logic. Non-deterministic code generation is a compliance gap.

One-line synthesis: *these sectors already require what most AI coding tools can't provide. The question isn't whether reproducibility will be required — it's whether your tools are ready when it is.*

Sources:
- [DO-178C and AI — Aerospace Global News](https://aerospaceglobalnews.com/opinion/ai-aerospace-software-do-178c-certification/)
- [FDA AI/ML guidance](https://www.fda.gov/media/184856/download)

---

## 7. Close (~150 words)

Return to the opening observation. Code is deterministic. AI-generated code isn't. Not because AI is broken, but because the languages AI writes in were designed for a different kind of author — one with preferences, conventions, and consistency. AI has none of these. It needs them supplied by the language.

The five-ways-to-transform-a-list problem isn't a Python bug. It's a design feature that becomes a liability when the author changes from human to machine. Reproducibility for AI-generated code starts with giving the AI fewer degrees of freedom — not fewer capabilities, but fewer ways to express the same capability.

Land the takeaway:
> *A language designed for human creativity gives AI five doors and no memory of which one it opened last. A language designed for AI gives it one door and a receipt.*

Forward link:
> *Next week: why "just ask the AI to explain itself" is fantasy — and why the strongest evidence comes from Anthropic's own researchers.*

---

## Cutting-room floor — do NOT include

- Amazon outage — dramatic but it's a code quality / review story, not a reproducibility story. Save for a sidebar or social post.
- Cigna/UnitedHealth health insurance denials — post 3 (visibility/opacity)
- Mata v. Avianca — post 3 (hallucination, not code reproducibility)
- EU AI Act — post 3 (transparency/audit trail)
- 57% legal consistency study — post 3 sidebar
- `requires`/`ensures` contract system deep dive — post 5
- Anthropic "chain of thought isn't faithful" — post 3
- Air Canada / Moffatt — already in post 1

## Editorial notes

- The hook is conceptual, not a news story. This is deliberate — the counterintuitive observation ("code is deterministic, AI-generated code isn't") is stronger than any single incident because it applies to everyone using AI coding tools.
- The "five ways to transform a list" example is the spine of the post. It appears in the hook, returns in the temperature section, and resolves in the AILANG section. Keep it consistent.
- The arXiv paper (2512.22387) is the empirical anchor. The 68.3% and 13.5x stats are strong. Visualise if possible.
- Section 5 (AILANG) is the longest section deliberately — this is where the post's unique contribution lives.
- The pull-quote ("one door and a receipt") is the Substack preview line.
- Tone: technical but accessible. The reader is a developer or technical decision-maker who uses AI coding tools daily and hasn't thought about why the output varies.
- The "trade-off stated honestly" paragraph in section 5 is important — don't oversell AILANG. Acknowledge the trade-off and let the reader decide.
