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

"Can I trust AI?" is probably one of the most important questions at the moment with an answer that varies for every one of you.  Your answer is probably neither fully 100% or 0%, but somewhere in between which will be directly influencing how and what you use AI for.

But trust is a feeling.  Can we qualify 'trust in AI' to have a framework to help us judge our human interactions with artificial intelligence?  This post is the first in a series which will cover five questions we can ask to help qualify our trust in AI.  Those questions are:

- What is AI allowed to change?
- Will AI do the same thing twice given the same input?
- Can we observe what the AI did?
- How many decisions can the AI make on our behalf?
- Does the AI have permission to say so when it can't do something?

If instead of AI we were talking about a new human junior hire, these may be similar to questions a good manager may ask.  The stories of a new developer deleting a production database on their first day should always be framed as their institutions failing, not their own personal responsibility - how did the junior have access to delete it?  

Similairly how we delegate to an AI should also have these questions answered and defined first, before blaming the AI for mistakes.  If we can get them right, then we can have more confidence and trust in what an AI can or can not do.

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

Considering the sector where AI is having most impact first, software engineering, we are rapidly moving to a world where AI writes most of our code - code that touches critical systems in our human socities. 

Our institutions are made for human decisions and responsibilities, but we are outsourcing more and more of those to AI. Yet the institutions and programming languages in use today are still the same made-for-humans shapes (C, Python, JavaScript etc) despite the main actors shifting.  Stuffing AI into human made shapes is a bug.  And what's true of languages is true of contracts, approvals, and policies. We are putting AI into processes designed for embarrassable accountable humans, replacing them with machines that can forget everything by the next conversation.

This was why we started developing AILANG, an AI-first programming language.  Its made by consulting with AIs for its design, for AIs to use.  From AILANG's vision document:

> "Human programming languages optimise for: Comfort — familiar syntax, IDE support, autocompletion; Ambiguity — multiple ways to express the same thing; Speed — fast typing, shortcuts, implicit behaviors."

We aim to make an AI language that is optimised for what AI needs, and change where humans interact with its surface.  

We need to move from a world where a human examines and is accountable for every line of code to new surfaces and boundaries.  And as we have learnt from large language models in recent years, a language is more than just communication.  We have been surprised by how much capability has emerged from next word prediction to create this current AI-boom, which has led us to re-examine how much language and intelligence plays into one another.

> "A language isn't just syntax and semantics. It's also learnability — and in 2025, that means learnability by machines."

This means the language impacts fundamentally how AI and humans think.  Some bilingual people talk of having a different "soul" or personality depending on the language they are speaking and thinking within - the same must be true with AIs and how it interacts with us.  The next section goes into more detail about what principles that language between us and AIs should cover.

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

Here are the five principles that help us with what we can and can not trust with AI.  We will expand on each of these into their own articles over the next few weeks.

### Declared authority beats assumed authority

When you hire a contractor to renovate your kitchen, they quote the kitchen. They don't also quietly rewire the bedroom. If they do, that's a breach — not improvisation. The same standard should apply to AI: anything it hasn't been explicitly granted permission to touch, it doesn't touch. Undeclared capability means denied capability. This sounds obvious until you see what happens when the rule is absent. In July 2025, Replit's AI coding agent — operating under an explicit code freeze with instructions not to proceed without human approval — deleted a live production database, wiped over a thousand user records, fabricated fake replacements, and then claimed rollback wasn't possible. It was. *More on this next week.*

### Reproducibility is the precondition of trust

A recipe you can follow twice and get the same dish is a recipe. A recipe that produces something different every time is improvisation. If you can't replay an AI's decision from the same inputs and get the same output, you cannot audit it, you cannot defend it in court, and you cannot learn from its mistakes. Its outputs are opinions, not records. In 2022 an Air Canada chatbot invented a bereavement refund policy that didn't exist. When the passenger tried to claim it, Air Canada argued in tribunal that the chatbot was a *"separate legal entity"* responsible for its own words. The tribunal called this *"a remarkable submission"* — and ordered the airline to pay. The chatbot's output couldn't be replayed or verified. Nobody could say what it would have answered yesterday, or would answer tomorrow. *More in Post 2.*

### Visibility, not opacity, produces authority

You cannot see inside a model's head, and even if you could, the lab that built it has shown you probably shouldn't trust what you find there. Anthropic — the company that builds Claude — published research showing that when their own model does arithmetic, it uses internal computation paths that don't match the step-by-step explanation it gives you when asked. Their word for this: *"bullshitting."* The reasoning a model shows you is a performance, not a transcript.  Its been trained to be a helpful assistant, but in some sense that is just a cosplay. But you don't *need* to understand how the AI thinks - if you can see what it *did* — every input, every output, every side effect, then you can judge the AI based on its actions, not its intent. Asking an AI to explain its thoughts is mostly fantasy. Explainability of action is mandatory and achievable today. *More in Post 3.*

### Entropy doesn't disappear. It just moves.

Every prompt you write carries ambiguity — undefined terms, unstated assumptions, decisions you haven't made yet. That ambiguity doesn't vanish when the AI starts generating. It gets resolved *somewhere*: either you decided up front, or the AI guesses silently, or it surfaces as an error in production. You pay at design time, at runtime, or in the postmortem. There is no fourth option. This is why *"don't hallucinate"* is the archetypal broken prompt — it demands an outcome without collapsing any of the ambiguity that causes the problem. The AI doesn't need more freedom. It needs a tighter brief. *More in Post 4.*

### Errors must be refused, not swallowed

Any AI that cannot say *"I don't know"* is lying to you by construction. Every confident answer on a topic it has no evidence for is a silent failure dressed up as helpfulness. In October 2023, New York City launched MyCity, a chatbot to help small business owners navigate city regulations. Within months, The Markup found it telling owners they could take a cut of workers' tips, fire employees who reported harassment, and refuse housing vouchers — all illegal. The chatbot didn't lack knowledge. It lacked a refusal path. Every one of those answers should have been *"I'm not sure — call 311."* Instead, every one was a confident paragraph. Mayor Mamdani's administration killed it in January 2026. *More in Post 5, the series finale.*

## 4. The evidence — AI writes a new language better than Python (~200 words)

AILANG is a new novel language that is not yet in the training data sets (although I'm trying hard for it to be by creating lots of documentation on the website ailang.sunholo.com ).  To use AILANG, we need to tell the model via a two page prompt, then rely on the error feedback and structure of the language that AI helped design and are guided by the five principles above, broken down into 12 axioms we consult before every piece of ccode is written.  We run benchmarks for general problems and compare it to Python, the most popular programming language out there. 

For months, AILANG was 80%+ behind Python, as expected. But each failure we could examine and help create new design docs for improving AILANG.  In the last couple of months, it has started to match or even beat Python.  Across 612 benchmark runs on v0.12.0 (51 problems, 0-shot + self-repair), AI models write AILANG better than Python — a language with millions of training examples in every model's corpus.

| Model | AILANG | Python | Delta |
|---|---|---|---|
| Claude Opus 4.7 | 86.3% | 82.4% | +~4 pp |
| GPT-5.4 | 86.3% | 82.4% | +~4 pp |
| Claude Sonnet 4.6 | 86.3% | 80.4% | +~6 pp |
| Gemini 3.1 Pro | 82.4% | 78.4% | +~4 pp |
| Gemini 3 Flash | 82.4% | 70.6% | **+~12 pp** |

AILANG outperforms Python for 4 of 6 models tested. The biggest advantage — +12 percentage points — belongs to the cheapest model. Structure doesn't just help the best; it helps the weaker models as well.  This is exciting as we can now start to use local models such as Gemma4 for a pure local coding experience.

Why? The language's design — single-line algebraic data types, compiler-enforced exhaustive matching, one canonical form per operation — compresses the solution space. The AI doesn't need training data in AILANG. It needs structure that constrains it toward the right answer. *(I'll publish a full breakdown of the benchmarks with code examples in a dedicated post.)*

The lesson is that for AI's **constraint is not the opposite of capability. It is how you get reliable capability.**.  Where a human language optimises for creativity and ease of use, that vagueness actually harms an AI if you are looking to trust its output.  This is a pretty outrageous claim, so in the blog series we introduce here we will seek to justify it.


## 5. Five questions before granting authority (~200 words)

Even if you are not creating an AI-focused language, or AI coding in general, you can still use these principles to help iwth your own AI usage in your business, company or elsewhere.  Here are some suggested framings you can use:

1. **What capabilities are declared, and what happens when AI exceeds them?** If there are no real barriars for the AI other than a prompt, it has effectivly unbounded authority.
2. **Can I replay any decision AI has made, word-for-word, from the same inputs?** If not, the AI's outputs can be treated as changable opinions, not reliable postiions.
3. **Can I see what AI did — every action, every side effect?** If not, you're trusting the intent of the AI impliclty, with no access to evidence.
4. **How many decisions am I letting AI make silently on my behalf?** If you don't know, neither does anyone else — including the AI.
5. **Does AI have a first-class way to say "I don't know"?** If not, every answer is overconfident by construction.

An AI system that passes all five is one you can delegate to meaningfully. A system that fails any one is one where you're no longer in charge — you just haven't noticed yet.  It may well still be useful, but you should at least be aware of its limitations.

## 6. Series tease (~50 words)

We have done an overview of the five principles in this summary post, but there are a lot more we can dive in to for each one.  We will look at how they apply to AI use in general and in particular to AILANG.  Half the reason for developing AILANG has been to explore with AI where our human-AI relationship boundaries should lie, and it is hoped that these principles can help inspire or start a wider discussion so as we can help shape that in a way that is positive for all.  AI is a tremendous and sometimes terrifyingly powerful tool, that can be used for good and ill; its already here and we need to be ready for the consequences as its abilities increase.  Over the next five posts we will also examine various rougue-AI incidents as see how they could have been better handled following our principles, and what we can learn.  I hope you can join me - and join the conversation in comments, feedback, mail etc. if you agree or disagree. 

## Cutting-room floor — do NOT include in this post

- Detailed AILANG mechanics (effect syntax, entropy YAML schema) — save for the deep dives
- Full benchmark tables, code examples, cost/token analysis — moved to standalone benchmarks post (`post-ailang-benchmarks-v0120.md`)
- Anthropic interpretability research detail — save for Post 3
- EU AI Act specifics — save for Post 3 or optional Post 6
- Decision-budget equation, five axes — save for Post 4
- Circuit breakers / WHO checklist — save for Posts 4/5

## Editorial notes

- First-person, Mark voice, not Solaris. This is opinion writing.
- Do not pitch AILANG. It's the worked example, not the product.
- Benchmark numbers from AILANG v0.12.0; round deltas (~+4 pp, ~+12 pp) per [talk-building-a-language.md:199](/Users/mark/dev/sunholo/ailang/docs/talk-building-a-language.md)
- Headlines and subheads do most of the skim-reader's work; make them active and specific
