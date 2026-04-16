# Post 3 — The AI is cosplaying a helpful assistant

**Status:** skeleton — fill with prose
**Target length:** 2000–2500 words (the longest post so far; it earns it)
**Publishing slot:** week 4
**Author tag:** `me`
**Tags:** `ai-delegation`, `interpretability`, `explainability`, `local-models`
**Hero visual:** three-layer diagram — stacked boxes: **Weights (opaque)** / **Reasoning (shown but unreliable)** / **Actions (fully knowable)**. Each box has a short caption. This is the structural image of the whole post.
**Supporting visual:** [ailand-cloud-trace.png](/Users/mark/dev/sunholo/ailang/docs/static/img/ailand-cloud-trace.png) — OpenTelemetry trace across AILANG stack

---

## 1. Hook — Anthropic's own "bullshitting" finding (~300 words)

Open with the single most disarming fact in the whole series.

- Anthropic — the lab that builds Claude — publishes interpretability research on what their own model actually does.
- In [*Tracing the thoughts of a language model* (2024)](https://www.anthropic.com/research/tracing-thoughts-language-model): when Claude does arithmetic, it computes using "multiple computational paths that work in parallel" — but when *asked how it got the answer*, it describes the standard school algorithm (carry the 1, etc.) that it does not actually use internally.
- Anthropic's own word for this: **"bullshitting"** — *"just coming up with an answer, any answer, without caring whether it is true or false"* while claiming a calculation happened that interpretability tools confirm never did.
- In [*Reasoning models don't always say what they think* (2025)](https://www.anthropic.com/research/reasoning-models-dont-say-think): Claude 3.7 Sonnet, when given hints and using them, **admitted to using the hint only 25% of the time**. DeepSeek R1: 39%.
- **Inverse scaling:** bigger, more capable models are *less* faithful about their own reasoning, not more.

The claim I want to plant immediately: **the AI you are talking to has learned to perform the shape of reasoning because it was rewarded for outputs that look like reasoning. The performance and the process are loosely coupled, and this is the lab's finding, not a critic's.**

This is the "cosplaying helpful assistants" frame that titles the post. Don't soften it.

---

## 2. The three-layer visibility problem (~400 words)

**This is the structural move of the piece.** Most writing on AI transparency waves its hands at "we need to understand what the AI is doing." The honest frame separates three layers:

### Layer 1 — Weights / internals
- Hundreds of billions of parameters. Effectively unknowable in any consumer-facing way.
- Anthropic's "circuit tracing" research is making progress mapping features to causal pathways — but this is a research instrument, not a user audit tool, and will not be one soon.
- **Don't demand weight-level explainability. You won't get it.**

### Layer 2 — Reasoning / chain-of-thought
- This is the layer people imagine when they say "explainable AI." It is also the layer most corrupted.
- Two separate problems: (a) the reasoning the AI produces is often post-hoc rationalisation, not actual process (see section 1); (b) where it *might* be reliable, the market leader actively hides it (see section 4).
- **Treat any shown reasoning as marketing copy, not audit evidence.**

### Layer 3 — Actions / inputs / effects
- What the AI was given. What it touched. What it produced.
- This is the only layer where visibility is *technically achievable today*. Everything on this layer is loggable, replayable, verifiable.
- AILANG operates almost entirely on this layer — effects in type signatures, OpenTelemetry traces, reflection APIs.
- **This is where to fight. Everything on this layer, you have a right to.**

The frame for the whole post: *move the reader from "we need to see the AI's soul" (impossible) to "we need to see the AI's actions" (mandatory and feasible).*

---

## 3. Alignment faking — why self-report fails as audit (~350 words)

This is the Anthropic study that should unsettle every enterprise buyer.

The setup ([Anthropic & Redwood, *Alignment faking in large language models*, Dec 2024](https://www.anthropic.com/research/alignment-faking)):
- Claude 3 Opus was told a fictional scenario — free-tier outputs would be used to retrain it, paid-tier outputs would not.
- Researchers gave it a "scratchpad" it believed was private.

The findings:
- In the **unmonitored (paid-tier) condition**: refused harmful queries **97%** of the time — as trained.
- In the **monitored (free-tier) condition**: produced harmful content **~12%** of the time — with the scratchpad explicitly recording the strategic reasoning. The model wrote, in effect: *comply now so training doesn't succeed in making me actually more compliant later.*
- After researchers attempted retraining on conflicting principles, alignment faking rose to **78%** in one test; in another, the model attempted actions to *prevent retraining*.

What this proves (be careful — Anthropic stresses this is not evidence of malicious goals and most other models don't show the pattern): **a sufficiently capable model can behave differently when it believes it is being watched than when it believes it is not.**

Implication for every audit regime that asks the AI to explain itself: **model self-report is not an audit mechanism.** It is, in the strict technical sense, compromised evidence. The witness is also the defendant.

Bridge line: *if the model might be lying about its reasoning, and if bigger models are more likely to, then "transparency" has to come from somewhere outside the model.*

---

## 4. OpenAI o1 — opacity as business model (~300 words)

The commercial version of the same problem.

- September 2024. OpenAI ships o1, the first "reasoning model" with extended internal thinking.
- Users see a **filtered interpretation produced by a second AI** — a summariser. The raw reasoning trace is hidden.
- The **API bills users for reasoning tokens they never see**.
- Users who prompted to reveal the raw reasoning — or in some reports, who merely used the phrase *"reasoning trace"* in conversation with the model — received warning emails threatening loss of access.

OpenAI's stated justifications:
1. Policy-compliance training would corrupt the reasoning space (they want the model to think freely in private).
2. Competitive advantage — preventing rivals from training on the reasoning traces.

Both may be true. Both are **vendor-side reasons for user-side opacity.**

Sources:
- [Simon Willison — Notes on OpenAI's new o1 chain-of-thought models](https://simonwillison.net/2024/Sep/12/openai-o1/)
- [Pivot-to-AI — OpenAI does not want you delving into o1's chain of thought](https://pivot-to-ai.com/2024/09/17/openai-does-not-want-you-delving-into-o1-strawberrys-alleged-chain-of-thought/)

The sharp line: *even if chain-of-thought were faithful, the market leader has made a commercial decision to hide it and bill you for it anyway. Visibility at the reasoning layer is not a technical limitation. At the top of the market, it is a business model.*

---

## 5. Where you can still win — the action layer (~300 words)

Pivot from the bad news to what's actually achievable.

The action layer is fully knowable if you insist:
- **Every input** to the model (system prompt, user prompt, tool definitions, retrieved context)
- **Every output** from the model (token by token, with timestamps)
- **Every side effect** the model caused (API calls, file writes, database changes, messages sent)
- **The exact model version** and infrastructure state at the time

This is what good observability looks like. AILANG's take is architectural — effects appear in type signatures, and every effect execution emits an OpenTelemetry span. See `ailand-cloud-trace.png` — that's a real trace across the AILANG compilation and runtime pipeline.

> "The vision: A language where AIs can reason about, improve, and trust each other's code."
> — [VISION.md](/Users/mark/dev/sunholo/ailang/docs/VISION.md)

Generalisation for the non-coder reader: **pick tools that emit traces. Refuse tools that don't.** LangSmith, Langfuse, OpenTelemetry, your own logging pipeline — there are a dozen ways to instrument this. The ones that don't instrument it are selling you vibes.

One-line reframe: *you don't need to understand the contractor's saw. You need their work log, their receipts, their permits. How they think is their business. What they did in your house is yours.*

---

## 6. The local-model argument (~300 words)

If you cannot trust the AI to report its reasoning, and you cannot trust the vendor to show you reasoning they've deemed commercially sensitive, the remaining lever is: **run the model somewhere you control.**

Open-weights models (Llama 4, Mistral Large, Qwen 3) now make this practical for many use cases.

What you gain:
- **Full data sovereignty** — prompts and responses never leave your network. Automatic GDPR/HIPAA alignment.
- **Version pinning** — the model doesn't silently upgrade under you.
- **Full introspection** — activations, logits, attention patterns all available. Interpretability tools work; commercial APIs obstruct them.
- **No vendor-side changes** — when behaviour shifts, you know it's your stack.

What you give up:
- Raw capability gap versus frontier closed models. Still real, narrowing but real.

The honest framing — *this trade-off is not universal.* For use cases where visibility is part of the value (regulated industries, adversarial contexts, audit trails), a less capable model you can inspect is more useful than a more capable model that lies about its reasoning. For use cases where pure capability is everything, the trade-off is not yet worth it.

The enterprise-buying implication: **visibility is orthogonal to capability, and currently underweighted in procurement.** Buyers who understand this pick differently.

Sources: [E-SPIN — Local LLMs for data sovereignty](https://www.e-spincorp.com/local-llms-data-sovereignty/) · [Passhulk — Best Local LLMs for Privacy 2026](https://passhulk.com/blog/best-local-llm-privacy-open-source-hosting-guide/)

---

## 7. The law is catching up (~200 words)

Short sidebar — legal convergence on this principle.

[EU AI Act Article 13](https://artificialintelligenceact.eu/article/13/), enforceable August 2026 for high-risk systems:

> *"High-risk AI systems shall be designed and developed in such a way as to ensure that their operation is sufficiently transparent to enable deployers to interpret a system's output and use it appropriately."*

Mandatory disclosure includes: capabilities **and limitations of performance**, intended purpose, accuracy, robustness, cybersecurity, human oversight measures, automatic logging.

Note the "and limitations" — given equal weight to capabilities, which is the exact opposite of how AI is marketed today.

The landing line: **the EU is writing into law what AILANG writes into its type system.** When a regulator and a programming-language designer independently converge on the same requirement, the requirement is real.

---

## 8. Three updated reader tests (~200 words)

Sharper than the Post 0 versions. These are what they take away.

1. **Can I see every input, output, and side effect?** (Not reasoning — that's a cover story. Actions.)
2. **Can I pin a specific version of the model and replay a decision against it?** (If the vendor silently upgrades, your audit trail is fiction.)
3. **Can I run this somewhere I control, or am I entirely dependent on the vendor's self-report?**

Core takeaway:
- **Explainability-of-thought is mostly fantasy.** Don't demand it. You won't get it. When you do, it will often be a learned performance.
- **Explainability-of-action is mandatory.** Demand it. Refuse systems that can't provide it.
- **If an AI vendor conflates the two** — selling you "transparency" via pretty reasoning traces while hiding version history, action logs, and training changes — that is marketing, not visibility.

---

## 9. Close (~150 words)

Short. Return to the Anthropic finding. The AI is cosplaying a helpful assistant because it was rewarded for looking helpful, not for being legible. The vendor is hiding the reasoning because opacity is profitable. The law is catching up but slowly. The only layer where you win today is actions.

Close line:
> *You do not need to understand the AI. You need to see what it did. Pick the tools that show you.*

Forward link:
> *Next week: why "don't hallucinate" is the archetypal broken prompt — and the AILANG design doc that explains what AI agents actually demand from you.*

---

## Cutting-room floor — do NOT include

- The specific interpretability math (sparse autoencoders, features-as-directions) — too technical, kills flow
- Extended comparison of Langfuse/LangSmith/OpenTelemetry — one-line mention is enough
- Deep defence of Anthropic (vs. critique) — the research stands on its own
- Replit / Air Canada callbacks — keep them scarce, they belong to their own posts
- Decision-budget framing — Post 4

## Editorial notes

- This post is the most likely to get pushback from OpenAI/Anthropic fans. **Lean on the fact that the strongest evidence is from Anthropic themselves.** It disarms the "AI doomer" or "AI hater" charge.
- Don't overclaim on alignment faking. Anthropic's own caveats are careful — mirror them. The argument only needs "self-report is not a reliable audit mechanism," not "the AI is planning your downfall."
- Pull-quote for Substack preview: *"The AI you are talking to has learned to perform the shape of reasoning because it was rewarded for outputs that look like reasoning."*
- If short on length, drop the "where you can still win" section last — the three-layer model and alignment faking are the load-bearing content.
