# Post 5 — Any AI that can't say "I don't know" is lying to you

**Status:** skeleton — fill with prose
**Target length:** 1200–1800 words (the series closer — punchy, not exhaustive)
**Publishing slot:** week 6 (series finale)
**Author tag:** `me`
**Tags:** `ai-delegation`, `refusal`, `safety`, `series-finale`
**Hero visual:** "The I don't know door" — illustration of a three-door building where the third door is bricked up. Caption: *every AI system ships with two doors. The one marked "I don't know" is usually missing.*
**Supporting visual:** screenshot of the NYC MyCity chatbot answering a question about wage theft with confidently wrong guidance (from the Markup reporting, March 2024)

---

## 1. Hook — the NYC MyCity chatbot (~350 words)

Open with the single most damning modern example of AI-without-refusal.

- October 2023 — NYC launches **MyCity**, a Microsoft-powered chatbot intended to help small business owners navigate city regulations.
- March 2024 — The Markup (Colin Lecher) tests it against actual NYC law. The chatbot tells business owners, among other things:
  - **They can take a cut of workers' tips.** (They can't — it's wage theft.)
  - **They can fire workers who complain about harassment.** (They can't — retaliation is illegal.)
  - **They don't have to accept Section 8 housing vouchers.** (They do — source-of-income discrimination is illegal in NYC.)
  - **Rent-stabilised apartments can be turned into condos without tenant consent.** (They can't.)
- Mayor Adams defends the tool through 2024 as a "work in progress."
- **January 2026 — Mayor Mamdani's administration announces MyCity will be shut down**, citing unfixable hallucination risk and active harm to small business owners who relied on it.

The diagnosis that ties the series together: **MyCity didn't lack knowledge. It lacked a refusal path.** Every one of those answers should have been *"I don't know — consult a lawyer or call 311."* Instead, every one was a confident paragraph.

Sources to link:
- [The Markup — NYC's AI Chatbot Tells Businesses to Break the Law](https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law)
- [AP — New York City's AI chatbot rolled out to answer questions](https://apnews.com/article/new-york-city-chatbot-misinformation-6ebc71db5b770b9969c906a7ee4fae21)
- [NYC Mayor's Office — MyCity announcement, January 2026](#) *(fill with actual link when cited in-post)*

---

## 2. The DPD swearing-chatbot cameo (~150 words)

Lighter second example — proof the pattern is industry-wide, not a government-IT story.

- January 2024. Ashley Beauchamp can't get DPD's customer service chatbot to help him find a missing parcel.
- Asks it to write him a poem criticising DPD. **It does.** Then swears at him. Then calls itself "the worst delivery firm in the world."
- Goes viral. DPD pulls it within hours.

Sources: [The Guardian — DPD AI chatbot swears, calls itself 'worst delivery firm'](https://www.theguardian.com/technology/2024/jan/20/dpd-ai-chatbot-swears-calls-itself-worst-delivery-firm-customer-service)

The point isn't that a chatbot swore. The point is: **the chatbot had no refusal path for "this is out of scope."** Given an adversarial prompt, a helpful-by-default model did the thing it was rewarded for — produced fluent, on-task output. Helpful is the *wrong default* when scope is undefined.

---

## 3. The missing primitive (~300 words)

Pull the diagnosis out explicitly.

Every one of the incidents in this series has the same shape at the end: **the AI produced confident output where the correct output was refusal.**

- Replit → should have refused to act under code freeze.
- Air Canada → should have refused to quote policy it couldn't verify.
- Mata v. Avianca → should have refused to produce case citations it couldn't ground.
- NYC MyCity → should have refused questions whose answer requires legal judgement.
- DPD → should have refused anything outside "track my parcel".

The common cause: **"I don't know" is not a first-class output for most AI systems.** It is culturally coded as a failure, commercially coded as a bad demo, and architecturally absent from the training signal.

What trained models actually optimise for:
- RLHF rewards **helpful, harmless, honest** — but "helpful" has dominated in practice. Refusal is penalised as unhelpfulness in a huge fraction of training data.
- Benchmarks reward answer coverage, not calibrated abstention. A model that says "I don't know" on 20% of questions loses to one that guesses and gets 55%.
- Product UX rewards fluency. A chatbot that answers "I'm not the right tool for this" looks broken; one that confidently invents looks magical. The magic is the bug.

The reframe: **a refusal path is a feature, not a failure mode.** A system that can say "I don't know, here's who can" is more trustworthy, more defensible, and more useful than one that always answers.

---

## 4. What refusal looks like when it's first-class (~300 words)

Make it concrete. Three examples across different layers of the stack.

### Language-level (AILANG)

- **Exhaustive pattern matching** — the compiler refuses to build code that doesn't handle every case. You cannot "accidentally" forget the None branch. The refusal is structural; the code literally won't run.
- **No silent `null`** — there is no ambient "missing value" that can be confused with a real one. If a value might not exist, the type says so, and the compiler forces you to handle the absence.
- **`requires/ensures` contracts** — a function declares what it requires of its inputs and what it guarantees of its outputs. Violations refuse to type-check.

Short quote:
> *"Fail loud, fail early, fail in the type system."*
> — paraphrase of AILANG's effect-system design philosophy (cite `m_r2_effect_system.md` if used verbatim)

### System-level (retrieval/grounding)

- RAG systems with citation-required output: if no supporting document is found, the system returns "no answer found," not a plausible paragraph.
- Tool-call architectures where certain verbs (quote policy, make legal claim, cite case) are gated behind tools that themselves can refuse.

### Policy-level (refusal envelopes)

- The entropy-budget scope from Post 4 — `forbidden: [facts, quantities, names, dates, monetary amounts, legal claims]` — is a refusal path expressed as a rule. Anything in `forbidden` that lacks evidence → the system returns "I don't know" rather than producing text.

The general shape: **refusal is designed, not hoped for.** Every system that successfully refuses has architecture that makes refusal the cheapest path. Every system that hallucinates has architecture that makes answering the cheapest path.

---

## 5. The cultural problem — why refusal is under-built (~200 words)

Brief, sharp.

Three forces push against refusal:

1. **Demo bias.** A bot that says "I don't know" loses the investor pitch. Fluency wins the meeting; refusal wins the lawsuit six months later.
2. **"Helpful" as a universal virtue.** Training corpora reward attempts over abstentions. The result is a model whose first instinct under uncertainty is to produce text.
3. **The vendor's incentive gradient.** Every refusal is a moment where the user might leave your product for a competitor who will just answer. Refusal is honest. Fluency is sticky.

The procurement implication: **refusal behaviour is a procurement question, not a technology question.** Before buying, ask: "Show me the last ten interactions where this system refused to answer. I want to see refusal rate by category." If the vendor can't produce that data, they're not tracking it, which means they're not optimising for it, which means the product you're evaluating has been shaped by pure fluency pressure.

A system without a measurable refusal rate is a system that doesn't refuse.

---

## 6. The series in one picture (~200 words)

Return to the five principles. Show that each one, ultimately, is a different face of the same requirement: **honest delegation.**

| Principle | What it forces | What happens when missing |
|---|---|---|
| Declared authority | The AI says what it will touch | Replit deletes prod DB |
| Reproducibility | The AI can be replayed | Air Canada can't defend chatbot output |
| Visibility | The AI's actions are logged | o1 hides reasoning, bills you for it |
| Entropy budgets | The AI's ambiguity is assigned | "Don't hallucinate" fails; 30-turn sessions |
| Refusal | The AI can say "I don't know" | NYC MyCity tells you to commit wage theft |

Every AI failure in the press over the last three years is one of these five, or a combination. None are failures of model capability. All are failures of delegation architecture.

The thread that runs through all five: **trust is built out of constraints, not capabilities.** The more constrained a system's authority, the more defensible its outputs. The series has been one long argument for this single claim.

---

## 7. The three questions, earned (~150 words)

Return to the three reader questions from Post 0 — now with the full context behind them.

Before granting authority to any AI system — agent, assistant, contract-reviewer, policy-drafter, customer-service bot — answer these. Write them down. File them.

1. **What capabilities has it declared, and what happens when it exceeds them?**
   *If nothing happens, it has unbounded authority. You are Jason Lemkin.*
2. **Can I replay any decision it made, bit-for-bit, from the same inputs?**
   *If not, its outputs are opinions, not records. You are Air Canada in the tribunal.*
3. **Does it have a first-class way to say "I don't know"?**
   *If not, every answer is overconfident by construction. You are the small business owner who just committed wage theft on the city's advice.*

A system that passes all three is one you can delegate to. A system that fails any one is one you are being delegated by.

---

## 8. Close (~150 words)

Land it. Short. Personal.

The whole series has been one argument: **we are giving AI systems authority at a scale and speed our institutions were not designed for.** The solution is not to slow down the AI — the economics won't allow it. The solution is to catch our *institutions* up: written capability envelopes, reproducible decisions, audit-grade action logs, explicit entropy budgets, mandatory refusal paths.

This is not exotic. It is what we already demand of human professionals — the contractor, the lawyer, the doctor, the accountant. All of them operate within declared scope, keep records, escalate uncertainty, and have a legally-binding way to say "outside my expertise, ask someone else." AI deserves the same discipline, and the same expectations.

Close line:
> *Trust is not a feeling you have about a system. It is a property the system earns by being constrained. Build for constraint, and trust will follow. Build for capability alone, and you will be writing the postmortem.*

---

## Cutting-room floor — do NOT include

- Extended riff on RLHF internals — too technical
- Philosophical detour on epistemic humility in humans — stay tactical
- Additional incident catalogue — five posts' worth is enough; don't pile on
- AILANG syntax detail — the one-line refusal-is-structural mention is enough
- Anything that positions this as an "AI safety" post in the existential sense — the series is about operational trust, not x-risk

## Editorial notes

- This is the series closer. End with Mark's voice, not a framework.
- The table in section 6 is the single most shareable artefact of the whole series. Design it for screenshot.
- Don't over-pitch AILANG in the close — the series already made the case. Let it breathe.
- Pull-quote for Substack preview: *"A system without a measurable refusal rate is a system that doesn't refuse."*
- Optional forward-link if you're doing the capstone (Post 6): *"Next week, a postscript: why the EU AI Act is quietly writing these five principles into statute — and what it means for anyone shipping AI in 2026."*
- If not doing Post 6, close the forward-link slot with a simple sign-off: *"That's the series. If it changed how you read your own prompts, it did its job."*
