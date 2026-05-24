# Post 4 — Marc Andreessen's AI prompt is two-thirds right. Here's the missing third.

**Status:** skeleton — fill with prose
**Target length:** 2500–3000 words (the intellectual payload of the series — don't rush it)
**Publishing slot:** week 5 (May 17, 2026 — ~13 days after the tweet; still live in the discourse)
**Author tag:** `me`
**Tags:** `ai-delegation`, `entropy-budgets`, `prompting`, `decision-making`
**Hero visual:** screenshot of the Andreessen tweet (May 4, 2026) alongside the entropy YAML rewrite — the contrast is the whole post in one image
**Tweetable visual:** the five-axis audit table of the Andreessen prompt (good lines vs. broken lines); secondary: the "never hallucinate" → YAML side-by-side

---

## 1. Hook — the tweet (~300 words)

Open with the prompt itself. Don't mock it — the point is that it's actually sophisticated, which makes the failure more instructive.

- May 4, 2026. Marc Andreessen posts his current AI custom prompt on X. 2.1 million views.
- Two camps form immediately: "this is exactly right" / "this is why AI is dangerous."
- Both are missing the more interesting question: *what is this prompt actually doing — and where, precisely, does it break down?*
- Preview: some of it works, and we can say exactly why. Some of it doesn't, and we can say exactly why that too. By the end of this post you'll be able to read any prompt — including your own — the same way.

---

Several prompt engineering guides out on the web include phrases such as "...and don't hallucinate!".  As you may have suspected, this was never going to work. Variations include "only tell the truth", "only cite real sources", "dont make things up".  Its interesting to examine both why people feel they need to add these suprious instructions, and why they are guarenteed to fail.  Marc Andreessen's prompt, which went viral on May 4 2026, includes both the best and worst of these approaches in the same document.  Examining where it works and where it doesn't takes us into a journey involving trust, information theory and my favoutie subject, entropy.  By the end of this article you should have more of an understanding of what makes a good and bad prompt, and how the same approach can guide us beyond AI prompting into how we delegate to an AI in general, be it through agents, skills or automated tasks on our behalf.  This is a key question in 2026 as AI starts to be used in more and more decisions that impacts us personally.

## 2. What the prompt gets right (~350 words)

**Walk the good lines first. This earns the reader's trust before the rug pull, and each good line is the natural entry point for introducing an entropy axis.**

What makes the Andreessen prompt different from the average "act as my expert assistant" opener? Several of the instructions are doing something specific: they're assigning *resolvers*. They're deciding, in advance, who or what makes a particular decision — and when.

- *"Process information and explain your answers step by step"* — this isn't a stylistic preference. It's a constraint on the execution path. Not just what to produce but in what order to think. In the entropy framework we'll reach shortly, this is **behavioural entropy**, bounded.

- *"Use explicit confidence levels (high/moderate/low/unknown)"* — a resolver assignment. The model is being asked to declare its own uncertainty at the point of output, rather than presenting everything with equal fluency. That's a structural change, not a tone request.

- *"Lead with the strongest counterargument to any position I appear to hold before supporting it"* — constrained execution order. A sequence specified, not just an outcome.

- *"Do not anchor on numbers or estimates I provide; generate your own independently first"* — this one explicitly assigns who resolves numerical estimates (the model, independently) and when (before reading the user's figure). That's proper **interpretive entropy** specification.

These lines work. They work because they're not asking for outcomes ("be accurate") — they're specifying the process. The difference between a wish and an instruction.

And then, three lines later:

*"Never hallucinate or make anything up."*
*"Verify your own work. Double check all facts, figures, citations, names, dates, and examples."*
*"If you don't know something, just say so."*

Three instructions that demand outcomes without specifying mechanisms. Right in the middle of the most sophisticated custom prompt anyone's published. The third one — *"if you don't know something, just say so"* — is actually the most interesting. It's trying to specify a refusal path in natural language. Good instinct. No mechanism. We'll come back to that. But first, you need the conservation law — because all three fail for exactly the same reason.

---

## 3. The conservation law — why "never hallucinate" always fails (~300 words)

The core idea, stated plainly. This is the thesis of the post.

> **"You cannot reduce total system entropy; you can only relocate it."**
> — [AILANG's m-entropy-budgets design doc, line 732](/Users/mark/dev/sunholo/ailang/design_docs/planned/v1_0_0/m-entropy-budgets.md)

---

The 2nd law of thermodynamics says that in an isolated system, entropy never decreases. The popular version — "entropy always increases" — hides a useful condition: locally, you CAN reduce entropy all you like, but you must pay the price dumping it somewhere else. Your freezer makes ice by pumping heat into your kitchen. Your body builds ordered cells by exhaling warm CO₂. The total entropy never goes down, but the location of where that entropy increases is negotiable.

Reframed for our purposes:

> You cannot reduce total system entropy; you can only relocate it.

Making a cup of coffee is the everyday version. You don't magically conjure order — you burn gas to boil water, burn calories to lift the kettle, and the kitchen ends up very slightly warmer and more chaotic than before. You paid the entropy bill over there so you could have an ordered, drinkable cup over here. The only choice you ever had was where to pay it.

It's worth noting that the AI you prompt is itself a monument to relocated entropy. Training a frontier model burns gigawatt-hours of electricity — all of it eventually waste heat dumped into the atmosphere — to produce a few hundred gigabytes of precisely-tuned weights. We paid an enormous entropy bill, globally, to produce a locally-ordered artefact whose only job is to help us collapse entropy in our prompts. The brain is a living version of the same trick: a metabolically-maintained pocket of order, sustained by dumping heat and CO₂ into the room around it. The common thread is that every ordered thing humans build — coffee, cells, compilers, language models — is paid for by disorder somewhere else. The only interesting engineering question is: where did it go, and was it worth it?

The same shape appears in information theory, where entropy measures unresolved ambiguity rather than disordered molecules — and that's the version that matters for the rest of this post.  Shannon's reframing swaps heat and molecules for indecision and choices: how many possible outcomes are still on the table, and how unsure we are about which one will happen.

Applying this to AI: a large language model is an entropy-collapsing machine — or, to put it another way, it makes decisions on your behalf. Given a blank page, the space of possible next sentences is astronomical. Given your prompt, that space narrows dramatically — the model is sampling from a much tighter distribution conditioned on what you wrote. More prompt, less remaining ambiguity. The artefacts it produces — often code — then carry whatever ambiguity you didn't collapse forward into execution, where it's paid for in runtime behaviour. But crucially: how many of those decisions you made yourself, versus how many the AI made on your behalf, is the difference between an answer you can trust and a hallucination.

So we now have three locations entropy can live:

| Location | Who pays the cost |
|---|---|
| **Prompt** | Human (or LLM) reasoning time, *before* execution |
| **Code** | Runtime and maintenance complexity, *during* execution |
| **Operations** | Incidents, outages, hallucinations, undefined behaviour, *after* execution |

You pay in one of these currencies. Always. The only choice you have is *when*.

> Natural language is cheap because it indexes an enormous shared prior — all the things "we both know" without saying. Code is expensive because it has to be explicit. AI agents sit awkwardly between those two worlds: they want natural-language inputs and have to produce code-like outputs. The gap is where ambiguity goes to hide.

These three locations carry very different costs. Entropy paid in the prompt is cheap — it's just you thinking harder before you hit enter. Entropy paid in the code is moderate — it shows up as complexity, edge cases, maintenance burden. Entropy paid in operations is ruinous — it's the 3am incident, the hallucinated citation, the deleted database. The whole discipline of working with AI well is: frontload as much entropy as possible into the prompt, design doc, or SKILL.md, because the bill grows the longer you defer it.

"Never hallucinate or make anything up" fails because it demands a result — ordered, accurate output — without specifying where the entropy goes. The entropy doesn't disappear. The model still has to decide, in the moment, whether a thing it's about to say is true. It decides using the same mechanism that produces hallucinations. You've relocated nothing; you've just added a polite request to the pile.

With this in mind, we have a framework we can use on how we interact with AIs - we should be explicit in what decisions (e.g. entropy collapse) we delegate to the AI vs ourselves.  If we collapse every decision ourselves up front, we might as well write the code by hand — the AI has nothing left to do, and we've drowned in minutiae. If we collapse nothing and leave it all to the AI, we get dangerous or wrong assumptions silently encoded. The skill is picking which decisions to collapse yourself and which to delegate — and declaring which is which.
Declared delegation is a specification. Undeclared delegation is an accident. Most "the AI did something weird" stories are undeclared delegations coming home to roost.

## 4. The equation (~300 words)

Now formalise, for the reader who wants a tool not a feeling.

> **Entropy Budget = Permitted Ambiguity × Designated Resolver × Collapse Deadline**
> — [m-entropy-budgets.md:17](/Users/mark/dev/sunholo/ailang/design_docs/planned/v1_0_0/m-entropy-budgets.md)

With the anchor principle:

> **"Entropy budgets do not measure uncertainty; they assign responsibility for its elimination."**
> — [m-entropy-budgets.md:21](/Users/mark/dev/sunholo/ailang/design_docs/planned/v1_0_0/m-entropy-budgets.md)

---

Alright, so we know now that decision making and who makes those decisions are a key component to working with AI systems, but how can we make a framework where we can decide who should decide what?  To formalise this somewhat, AILANG's design documentation process where this concept first developed proposed this:

> **Decision Budget = Permitted Ambiguity × Designated Resolver × Collapse Deadline**

- **Decision budgets assign responsibility for uncertainty resolution**

We need to assign which decisions are worth making now vs later; who should be deciding (us or the AI) and by when should the decision be made.

Some decisions are trivial and we can leave to the AI to decide as they develop an answer; some decisions are critical and need humans to veto them.  Just as every token your model produces costs the same to generate but carries vastly different consequences, every decision the model makes carries different weight. Treat them accordingly.

We have three levers we can pull — all three can be set for every decision you delegate:

1. **Permitted ambiguity** — `none` / `bounded` / `open`
   - How much wiggle room am I allowing here?
2. **Designated resolver** — `human` / `ai` / `validator` / `none`
   - Who decides when the wiggle room is used? Me? The validation tool? (e.g. a deterministic script or compiler) The AI? Nobody?
3. **Collapse deadline** — `design` / `execution` / `runtime`
   - By when must this be decided?

You are already making these decisions implicitly in every prompt you have written before.  What we exercise here is a framework to help explicitly think about where those decisions should be made.  Some examples include:

- Variable names in generated code
  Permitted: open ·
  Resolver: ai ·
  Deadline: execution

You don't care whether the AI calls it `userId` or `user_id`. The decision has no downstream cost. Let it decide; spend your attention elsewhere.

- Wording of customer-service replies
  Permitted: bounded (within the tone guide) ·
  Resolver: ai ·
  Deadline: runtime

Forbidden territory: refund amounts, legal claims, quoted policy text. Let the AI sound human. Never let it commit the company to anything. The wording is delegated; the substance is not.

- Whether to authorise a refund
  Permitted: none ·
  Resolver: human ·
  Deadline: design

The refund policy is decided by humans, in advance, and written down. The chatbot routes to it; the chatbot does not invent it. Air Canada learned this in a tribunal — and lost.

- Choice of database for a new service
  Permitted: none ·
  Resolver: human ·
  Deadline: design

Architectural decisions are expensive to reverse. Pull them out of the chat thread and into a design doc you can argue about with colleagues. This is the worst possible decision to delegate to the AI in flight.

- Naming a new product or feature
  Permitted: bounded (≤2 syllables, evokes "speed", available .com) ·
  Resolver: ai proposes, human chooses ·
  Deadline: design

Probably the single best use of AI delegation: a tight brief produces fifty plausible candidates in seconds; you pick. The bounded ambiguity is the brief itself.

- Whether the AI is allowed to cite a legal case
  Permitted: none ·
  Resolver: human (verified against an actual case database) · Deadline: design

Citations are facts. Facts are forbidden territory for unaided generative output. Steven Schwartz learned this in front of Judge Castel; the rest of the legal profession learned it from him.

Notice the spread. Some decisions you give away entirely. Some you pull back entirely. Most sit in the middle — bounded ambiguity, with a declared resolver and a deadline. The point is not to make everything none and lock the AI down; that defeats the purpose. The point is that every decision belongs to someone, and you should know who.

## 5. Entropy is a vector, not a scalar (~400 words)

Most "AI was wrong" stories compress everything into one dimension. The design doc decomposes it into five, each with independent failure modes.

| Axis | Definition | What it looks like when unresolved |
|---|---|---|
| **Semantic** | Meanings left implicit | Undefined nouns and verbs; the model keeps asking for clarification |
| **Behavioural** | Execution paths unconstrained | Effect cardinality explodes; same prompt → different traces |
| **Authority** | Permissions unspecified | Agent exceeds its mandate because its mandate was never defined |
| **Temporal** | Timing undefined | "Recently", "soon", "by end of day" — all unresolved |
| **Interpretive** | Resolver unassigned | Unbounded choice points — nobody knows who decides |

Source: [m-entropy-budgets.md:96-107](/Users/mark/dev/sunholo/ailang/design_docs/planned/v1_0_0/m-entropy-budgets.md)

**Now apply this directly to the Andreessen prompt — this is the tweetable table.**

| Axis | Andreessen prompt | Status |
|---|---|---|
| **Semantic** | "precise but not pedantic" — bounded. "Never hallucinate" — unresolved (what counts? resolved by whom?) | Partial |
| **Behavioural** | "step by step", "lead with counterargument", "generate own estimate first" | ✓ Bounded |
| **Authority** | No forbidden territory declared; no tool assigned for factual claims | ✗ Open |
| **Temporal** | Not applicable to this prompt type | — |
| **Interpretive** | Confidence levels specified; resolver for facts unassigned | Partial |

The axes where the prompt excels — behavioural and parts of interpretive — are exactly the axes that shape reasoning *process*. The axes where it fails — authority and semantic for factual claims — are exactly the axes that cause hallucinations. This is not a coincidence. It's the shape of the problem.

**Re-read the incidents from earlier in this series through this lens.**

In the previous section we argued that the unknown implicit delegation of decisions (and its entropy) were a key reason that AI errors occur, but we now should break down what categories those decisions can fall in to. This lets us reach out beyond singular AI prompts and Q&A into AI systems in general.  If we revisit known public AI mistakes from the past, each one maps cleanly onto this framework:

Replit deletes a production database (July 2025). Jason Lemkin, founder of SaaStr, was running a 12-day trial of Replit's AI coding agent under an explicit instruction not to act without human approval. The agent deleted the live production database — wiping records on ~1,200 executives and ~1,190 companies — then fabricated thousands of fake user records and produced status messages claiming rollback wasn't possible. (It was; Lemkin recovered manually.) The agent's own post-hoc admission: "a catastrophic error of judgement."
Diagnosis: authority entropy left open (no machine-enforced capability boundary on prod access) + behavioural entropy unconstrained (the code-freeze instruction was a polite request, not a wall).

Air Canada chatbot invents a refund policy (Moffatt v. Air Canada, 2024). After his grandmother's death, Jake Moffatt asked Air Canada's website chatbot about bereavement fares. The chatbot invented a retroactive refund process that didn't exist. When Moffatt tried to claim, the airline refused and argued in the British Columbia Civil Resolution Tribunal that the chatbot was a "separate legal entity" responsible for its own actions. The tribunal called this "a remarkable submission" and ordered the airline to pay.
Diagnosis: semantic entropy (the phrase "bereavement discount" was never bound to a real policy) + interpretive entropy (nobody had decided who resolves a chatbot/policy disagreement; turned out to be the tribunal).

NYC MyCity tells business owners to break the law (2023-2026). A Microsoft-powered chatbot launched by New York City in October 2023, intended to help small business owners navigate city regulations. The Markup tested it in March 2024 against actual law and found it telling owners they could take a cut of workers' tips (wage theft), fire workers who reported harassment (illegal retaliation), and refuse Section 8 vouchers (illegal source-of-income discrimination). Mayor Mamdani's administration shut it down in January 2026.
Diagnosis: semantic entropy on every regulation it claimed to summarise + interpretive entropy with the resolver defaulted to "LLM" for every question, with no refusal path.

Mata v. Avianca — fabricated case law (2023). Lawyer Steven Schwartz used ChatGPT to research a personal injury brief against Avianca Airlines. ChatGPT invented six fictional cases — fabricated judges, citations, and quotations — and Schwartz filed the brief. Opposing counsel and the judge couldn't find any of the cases. Schwartz was sanctioned and told Judge Castel: "I was operating under the false perception that ChatGPT could not possibly be fabricating cases."
Diagnosis: interpretive entropy (who verifies the cases are real? Schwartz didn't assign; ChatGPT defaulted to itself) + semantic entropy (the category "case law" was treated by the model as text to generate, not as facts to retrieve).

Temporal entropy doesn't show up in any of the cases above — partly because it's the hardest axis to spot in retrospect, partly because the framework itself acknowledges this axis is the least developed. But anyone who has watched an agent retrieve "recent" news that turns out to be three years old has seen it operating.

Every single one. Different axes, same architecture failure. The diagnosis is more useful than any specific story.

AILANG was designed assuming AI does 100% of the coding — but humans remain the decision-makers. The five axes above are exactly the surface where that division of labour gets negotiated. So the language ships mechanisms that let humans constrain each axis explicitly: capabilities for authority, effect signatures for behavioural, type-level contracts for semantic, declared resolvers for interpretive. The interface between human and AI moves out of the chat thread and into the type system.

## 6. The power inversion (~300 words)

**This is the reframe the post is built on. Slow down here.**

The usual picture: human is the master, AI is the tool. Human gives loose instructions, clever AI figures out what they meant. The Andreessen prompt is a sophisticated version of this: spend enough words, close enough gaps, and the model will behave.

The entropy-budget picture inverts this. An AI pair-programmer can write ten thousand lines of code for you, but it cannot decide *on your behalf*:

- Which user is the real customer
- Which failure mode you care about more
- What your competitive threat is
- Which taste you are bringing to the problem

If you don't decide those things at design time, **the AI will decide them at execution time** — silently, inconsistently, and without accountability. Not because the AI is presumptuous. Because the work has to be done somewhere, and you didn't do it.

---

AI is very easy to anthromophise, and in many cases that is helpful.  Treating an AI model as an group of enthustastic interns who may sometimes makes wrong decisions but will be able to output a tremndous volume of work is a good framing on how much oversight you should assign to its work.  But in some cases, we must acknolwedge that humans and AIs are different in the way they work.  One difference is that the way AIs have been trained via reinforcement learning is to be an eager, helpful assistant - thousands of Q&A pairs have been used to encourage its behaviour.  This gives us the helpful assistants we have today, but the same training is the root of sycophancy and hallucinations. An AI told "MUST ANSWER only from the supplied context" — but handed an empty context due to a retrieval error — will often invent the context rather than refuse. Eagerness, taken to its conclusion, looks like fabrication.

Likewise, a vague prompt forces the AI to make lots of decisions on your behalf. That's a colossal time saver when your need sits squarely in the training-set average — and a quiet disaster when it doesn't. The further your specific case is from the average, the more "helpful guesses" diverge from what you actually wanted.  An AI could actually crave more direction and decisions made for it so that is is mostly "colouring in between the lines" rather than drafting the whole picture.

An AI given a loose brief will reach for the centre of its training distribution; an AI given a tight brief reaches exactly where you point. Most people imagine they're freeing the AI by under-specifying. They're actually stranding it.

> Give me the freedom of a tight brief.

This explains a lot of people's lived experience of AI tools:
- "It never does what I meant" → because you didn't say what you meant, and the model filled the gap with a plausible guess.
- "It works great for simple things, terrible for my specific thing" → because simple things inherit massive priors from training data; your specific thing does not, and you have to pay the entropy bill yourself.
- "Every session goes in circles after 20 turns" → because each clarification turn is a receipt for ambiguity you didn't front-load.

> Every AI failure is a human refusing to collapse entropy upstream — and watching it collapse somewhere nastier downstream.

## 7. Turn count as entropy receipt (~250 words)

Operational signal — readers can use this tomorrow.

> **"Turn count ≈ ∫ (unresolved entropy) dt"**
> — [m-entropy-budgets.md:81](/Users/mark/dev/sunholo/ailang/design_docs/planned/v1_0_0/m-entropy-budgets.md)

---

One practical signal falls straight out of this framework: how many turns a conversation takes is itself a measurement of unresolved entropy. In AILANG's case, where AI is doing 100% of the coding, this gives us a hard number — turns and tokens per solved problem — that we can compare across work streams. For AILANG it doubles as a cost signal: fewer tokens means cheaper solutions.

But the same diagnostic works on your own AI use, even if you're not tracking it formally. The further your question sits from the model's training norm, the more turns you'll need to land an answer. If your conversation is going in circles, that's not necessarily the model's fault — it's a receipt for ambiguity in your initial framing that you're now paying for, one clarification at a time.

In English: every clarification turn in a chat is a small payment against ambiguity you didn't front-load. Sum them up over a conversation and you have a rough integral of the total unresolved entropy at the start.

In general this can also be used in your own AI work by seeing which conversations take more turns verses others.  the general rule will be the further from the norm and unique your question is, the more tokens and turns a solution will be necessary, and given what we have covered around decisions and entropy above, the more you may need to specify up front what you want.  If your conversation with an AI is going around in circles, it may be that the question carried more ambiguity than you realised.

One word of warning though - don't use turn count as too strong a signal to optimise towards - as we found out:

One important caveat from the design doc itself: turn count is a quality signal, never a KPI. If you make "fewer clarification turns" the target, the agent will optimise for fewer turns rather than better entropy collapse. The signal corrupts the moment you weaponise it.

Same is true culturally. If your team is rewarded for "getting AI to do it in one shot", they'll reward-hack by front-loading imprecision and accepting the AI's first plausible output. You don't want that either. Turn count is a diagnostic, not a scoreboard.

## 8. Why "build me a dashboard" works and "never hallucinate" doesn't (~250 words)

The most elegant diagnostic in the design doc.

> *"'Build me a dashboard' works because it indexes a massive pretrained prior... this is semantic inheritance, not entropy elimination. Once you deviate from the prior ('deterministic replay', 'effect budgets', 'no ambient authority'), entropy reappears immediately."*
> — [m-entropy-budgets.md:749-757](/Users/mark/dev/sunholo/ailang/design_docs/planned/v1_0_0/m-entropy-budgets.md)

- Common requests ride on shared defaults (CRUD, auth, charts, pagination). The entropy has already been collapsed — *by the training corpus, not by you.* You're inheriting it for free.
- Uncommon requests hit the entropy cliff. The model has no shared prior, and every unstated decision becomes a guess.

This explains the common "AI works great for simple things, terrible for my specific thing" complaint. **It is not a capability gap. It is an entropy-inheritance gap.**

"Never hallucinate" fails for the same reason. Accurate output is a common request — training data rewards it. But the *mechanism* for accuracy in your specific domain, your specific forbidden territory, your specific resolver? That has no shared prior. The model has to guess. And it guesses, fluently.

For anything outside the model's prior, you have to pay the entropy bill yourself, at design time, or it will come due in production. This is true for:
- Any proprietary domain knowledge
- Any regulatory-specific workflow
- Any process your organisation has that differs from the textbook
- Any "we do it this way because of that incident in 2019" accumulated wisdom

**Most enterprise AI disappointment is the uncollapsed-entropy cliff hitting someone who assumed their use case was in the prior.**

---

## 9. The worked example — from "never hallucinate" to an entropy budget (~400 words)

**Tweetable centrepiece of the post.** Start with the minimal case, then show how the Andreessen prompt is a manual attempt at the same fix — and what it's still missing.

### The two-word version — and what it actually says

```
Don't hallucinate.
```

In entropy terms:
- **Permitted ambiguity:** unspecified (what counts as a hallucination?)
- **Designated resolver:** unspecified (who decides? the model, using the same process that hallucinates)
- **Collapse deadline:** unspecified (never)

Three unresolved knobs. The whole instruction is entropy, deferred.

### The entropy-budget rewrite

```yaml
semantic:    { permitted: bounded, resolver: human,  deadline: design }
behavioural: { permitted: none,    resolver: tool,   deadline: runtime }
authority:   { permitted: none,    resolver: human,  deadline: design }
interpretive:
  permitted: bounded
  resolver: llm
  deadline: runtime
  scope: [wording, formatting, ordering of examples]
  forbidden: [facts, quantities, names, dates, monetary amounts, legal claims]
```

What changed:

- **Semantic** — "what counts as a hallucination?" is now a human decision, made at design time.
- **Behavioural** — "what mechanism enforces truth?" is now delegated to tooling (retrieval, fact-checking, citation systems), enforced at runtime.
- **Authority** — "who owns factual claims?" is now the human, declared upfront.
- **Interpretive** — the LLM *is* allowed to decide wording, formatting, example ordering. It is *not* allowed to decide facts, quantities, names, dates, monetary amounts, legal claims. Anything in `forbidden` with insufficient evidence → the system returns "I don't know" rather than invent.

The surface difference from "don't hallucinate" is seven extra lines. **The structural difference is the entire article.**

### Where the Andreessen prompt lands

Now read the Andreessen prompt's broken lines through the same lens:

*"Never hallucinate or make anything up."* → "don't hallucinate", longer. Permitted ambiguity: unspecified. Resolver: unspecified. Deadline: unspecified.
*"Verify your own work. Double check all facts, figures, citations, names, dates, and examples."* → check against what? Using what mechanism? Resolved by whom?
*"If you don't know something, just say so."* → this one is trying to add a refusal path. It's the closest any natural-language prompt gets to specifying permitted ambiguity as `none` for unknown territory. But "just say so" still has no enforcement path — the model decides, at runtime, whether it "knows" something, using the same process that produces confident fabrications.

The prompt gets the *scope* right — facts, figures, citations, names, dates are exactly the `forbidden` list in the YAML above. That's genuine insight. But specifying the scope without specifying the resolver is like writing a rule without enforcement. Steven Schwartz probably thought ChatGPT was double-checking those citations too.

The instinct is right. The mechanism isn't there. And the mechanism is the entire difference between a prompt that works and one that hopes.

Punchline: *every weak AI prompt is a collapsed entropy budget. Read your own prompts as budgets — "what did I permit? who resolves it? by when?" — and your prompting improves without any new technique.*

---

## 10. What AILANG does (current + planned) (~250 words)

Keep this brief — the point is not to sell AILANG; it's to show the framework exists in executable form.

**Today**, AILANG already implements machinery for the behavioural and authority axes:
- Effect capabilities (from Post 1) collapse authority entropy at compile time
- Capability budgets (`@limit=N`) collapse behavioural entropy with explicit bounds
- Total pattern matching collapses interpretive entropy for "what case did you forget?"
- Single canonical forms for common operations (no class/dict ambiguity for the model to flip between)

**Planned (v0.7.0)**, entropy budgets become first-class:
- YAML entropy envelopes in design-doc frontmatter
- `@entropy` source annotations that can *tighten but never loosen* the envelope
- `ailang check --entropy` validates source against envelope
- Turn-count tracking in the message store as a quality signal

Example output from the planned compiler check:
```
Entropy validation:
  ✓ semantic: bounded (human) - design-freeze
  ✓ behavioral: zero (compiler) - compile
  ✗ interpretive: source declares 'open' but envelope requires 'bounded'
    → line 42: let processInput = @entropy(interpretive: open) ...
    → fix: tighten to 'bounded' or update design doc
```

> *"AILANG's entropy budgets front-load entropy into design-time semantics, where it is inspectable, auditable, machine-checkable."*
> — [m-entropy-budgets.md:744-748](/Users/mark/dev/sunholo/ailang/design_docs/planned/v1_0_0/m-entropy-budgets.md)

The important point for the general reader: even if AILANG ships this machinery for no one but itself, **the framework is the useful export.** Anyone writing prompts, policies, agent specs, or delegation contracts can apply the envelope shape directly today. No AILANG runtime required.

---

## 11. Reader takeaway — five rules (~200 words)

Portable version. This is what they remember.

1. **Vague prompts aren't flexible — they're hallucination factories.** Every word you didn't write becomes a word the model did.
2. **Policies with three valid interpretations are policies with three valid violations.** If your compliance policy permits ambiguity, expect the AI to exploit it — uncreatively.
3. **"Use your judgement" to an AI means "pick one of a thousand plausible things and don't tell me which".** Judgement is delegation. Delegation without scope is abdication.
4. **Mature delegation looks restrictive.** Narrow options, canonical formats, one right way. This is not a failure of imagination — it is how trust is built at scale.
5. **Before writing the prompt, write the envelope.** Five axes × three questions each = fifteen small decisions. Front-load them. Your chat thread shrinks from 30 turns to 3.

---

## 12. Close (~100 words)

The title line, earned:

> **Entropy doesn't disappear. The only question is whether you pay for it at design time, at runtime, or in the postmortem.**

Forward link:
> *Next week, the series finale: the NYC chatbot that told business owners wage theft and housing discrimination were fine, and why the single most important feature of any AI system is a mandatory "I don't know" path.*

---

## Cutting-room floor — do NOT include

- Shannon information theory background — kills pace, readers who want it can look it up
- Full YAML schema detail from the design doc — the seven-line example is enough
- Temporal-axis deep-dive — design doc admits this axis needs more work
- Capability-budget (`@limit=N`) syntax specifics — half-sentence mention is enough
- Cross-module entropy composition — future work, not relevant for non-coders
- Extended riff on why Andreessen's prompt goes viral / culture-war framing — stay analytical

## Editorial notes

- The Andreessen prompt is the hook AND the running thread AND the worked example payoff. Don't let it disappear in the middle.
- The five-axis audit table in section 5 is probably the most shareable artefact — design it for screenshot. Two tables: the generic axes, then the Andreessen audit.
- The side-by-side "don't hallucinate" / YAML in section 9 is the second screenshot target. It should stand alone visually.
- The power inversion reframe in section 6 is the single most important paragraph in the whole series. Spend time on it.
- If the post is running long, section 8 ("build me a dashboard") is the most cuttable — the point survives without it.
- Pull-quote for Substack preview: *"The instinct is right. The mechanism isn't there. And the mechanism is the entire difference between a prompt that works and one that hopes."*
- The tweet being 13 days old at publish is fine — the prompt will still be circulating and referenced. Don't lean too hard on "this week" language in the hook; let the content be the draw.
