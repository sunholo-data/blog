# If you can't replay it, you can't ship it

*This is the third post in a six-part series on AI delegation, trust, and authority. Read the [series introduction here](/blog/wrong-question-ai-trust).*

---

Code is deterministic. You run it, it does the same thing every time. That's the whole point — code is a recipe, not a conversation. So when an AI writes code for you, the output should be deterministic too, right? Same prompt, same code, same result.

Wrong. The code is deterministic once it exists. The act of *generating* it is not.

Here's why, and this is the part that surprises people: human programming languages were designed for human expressiveness. Python has at least five idiomatic ways to transform a list — list comprehension, `map()`, for-loop with append, generator expression, `filter()` with a lambda. All correct. All different. A human developer picks one style and stays consistent. They have preferences, team conventions, muscle memory.

An AI has none of these. Each generation is a fresh sample from a probability distribution. It picks whichever form emerges from the dice roll *that particular run*. Next run, it picks differently. Both are correct Python. Neither is the same code.

What this means in practice: you ask an AI to write a data-processing function on Monday. It gives you a list comprehension. Tests pass. You ship. On Tuesday, a colleague asks for the same function. The AI gives them a for-loop with append. Functionally identical. Structurally different. Their tests pass too. Now you have two implementations of the same logic in the same codebase, written by the same "developer," and neither of you knows why they're different.

This is the second question you need to ask of any AI system you delegate to: **can I replay what it did?** And for AI-generated code, the answer is almost always no — not because the AI is broken, but because the *language* gives it too many degrees of freedom.

---

## Reproducibility is the precondition

You can trust a recipe because it doesn't depend on the chef's mood. You can *love* improvisation — it's creative, it's surprising, it occasionally produces something brilliant — but you can't certify it. You can't put it in a cookbook. You can't hand it to someone else and say "do exactly this."

Reproducibility isn't a nice-to-have for AI-generated code. It's the precondition of every other property we want. Testing — you can't regression-test against a moving target. Caching — you can't cache a build if the inputs produce different outputs. Auditing — you can't audit code that's different every time you look at it. Code review — you can't review what you can't reproduce. All of these are downstream of being able to replay the same generation twice.

And the reason we don't have reproducibility isn't that AI models are bad at coding. It's that the languages they write in were designed for a different author.

---

## The numbers: model, language, harness

This isn't theoretical. We've been running our own benchmark suite against AILANG and Python side-by-side, across six leading models — Claude Opus 4.7, Claude Sonnet 4.6, GPT-5.5, GPT-5.4-mini, Gemini 3.1 Pro, Gemini 3 Flash — through three different evaluation harnesses: single-shot API, single-shot-with-repair, and full agentic CLI (Claude Code, Gemini CLI, opencode, Codex). 33 standardised benchmarks per combination. The latest run — v0.15.0, generated this morning — covered 396 standard runs and 180 agent runs.

[COMPONENT: `<LanguageChart />` from BenchmarkDashboard — shows AILANG vs Python success rates per model. Source: `https://ailang.sunholo.com/benchmarks/latest.json`]

The headline result is more interesting than "AILANG wins" or "Python wins." On single-shot generation, Python edges AILANG by a few points: Python 79.3% vs AILANG 75.8%. On agent mode with a repair loop, Python pulls further ahead: 97.1% vs 86.2%. If you read the marketing of any AI coding tool, this is roughly the story you expect — Python is what the models were trained on, and the models do better on what they were trained on.

But the headline averages hide the real finding, which is the variance.

[COMPONENT: `<ModelChart />` showing per-model breakdown — same data, sliced by model rather than language]

GPT-5.5 writing AILANG hits **90.9%** on single-shot. The same model on Python hits 81.8%. Gemini 3 Flash on AILANG: 66.7%. On Python: 66.7%. Claude Opus 4.7 on Python: 87.9%. On AILANG: 84.8%. Different models, different languages, different success rates — and there's no single "best" combination that holds across the board.

The picture changes again when you switch evaluation harness. The same model writing the same language gets dramatically different results depending on whether it runs as a single API call, a single call with repair, or a full agentic CLI session. Some opencode + AILANG combinations hit **100%**. Some single-shot AILANG runs barely scrape 60%. The harness matters as much as the language. Sometimes more.

[COMPONENT: `<HarnessComparisonTable />` from `LanguageLeaderboard` — cross-harness comparison showing same model under different CLIs]

The point isn't that any one combination is best. It's that **success rate is a function of language × model × harness, and most teams measuring "is this AI any good?" are only varying one of those three**. They pick a model and stick with it. They pick Python and stick with it. They pick a single-shot API call and stick with it. Then they wonder why the results aren't reproducible — because the search space is far larger than they realised, and they haven't measured it.

The full live data, including the 33 benchmarks, six models, multiple harnesses, and historical trends across versions, is on the [AILANG benchmarks dashboard](https://ailang.sunholo.com/docs/benchmarks/performance). Outside corroboration: an [arXiv study from late 2025](https://arxiv.org/abs/2512.22387) tested three coding agents across 300 projects in Python, JavaScript, and Java and found similar variance — only 68.3% of projects ran out of the box, with a 13.5× gap between declared and actual dependencies. Same pattern, broader scope.

---

## Temperature zero doesn't fix this

The first objection from technical readers will be: "just set temperature to zero." Temperature controls randomness in token selection — at zero, the model picks the single most probable next token every time. Sounds deterministic.

It isn't. Even at temperature zero, AI code generators can produce different outputs on identical prompts because of non-deterministic GPU maths (floating-point reduction order varies between runs), silent model-version upgrades by the provider, prompt-cache behaviour, and system-prompt changes the vendor makes without telling you.

But even if temperature zero *were* perfectly deterministic, it wouldn't solve the structural problem. The model would deterministically pick *one* of Python's five ways to transform a list. Change the prompt slightly — add a comment, reorder a paragraph, provide a slightly different context window — and it deterministically picks a *different* one. The language still has five doors; temperature zero just fixes which door the AI walks through for that exact input.

**The problem isn't randomness. The problem is optionality.** A language with five ways to do the same thing gives the AI five chances to be inconsistent — whether or not the token selection is stochastic. For code, this is catastrophic in a way it isn't for chat. A chatbot giving a slightly different phrasing is fine. An AI generating structurally different code means your tests pass Tuesday and fail Wednesday on identical inputs. It means a security audit is meaningless because the code it audited isn't the code that shipped.

---

## What a language designed for AI does differently

Every programming language makes a trade-off between expressiveness and consistency. Human languages — Python, JavaScript, Ruby — maximise expressiveness: many ways to say the same thing, because human creativity thrives on choice. That's a feature when a human is writing.

But AI doesn't need creative freedom in syntax. It needs a narrow, predictable target. Fewer ways to express the same logic means less entropy per generation, which means more reproducible output. This is the design thesis behind [AILANG](https://ailang.sunholo.com/): a programming language built for AI as the primary author, where reproducibility is a first-class design goal rather than an afterthought.

Three things make the difference:

**One canonical form per operation.** In Python, list transformation has five or more idiomatic forms. In AILANG: `result = map(f, items)`. That's it. One way. The AI doesn't choose between forms because there's nothing to choose between. Same prompt, same structure, reproducible generation. This isn't a constraint — it's the elimination of unnecessary entropy. One right way is a feature, not a limitation.

**Declared effects in the type signature.** Every function says what it touches: `func fetchData() -> string ! {Net}` means "this function uses the network and nothing else." No hidden side effects. No dependencies the AI forgot to mention. The type signature *is* the dependency declaration — and the compiler enforces it. The 13.5× dependency gap the arXiv study found in Python and Java code can't exist in AILANG: if your code uses the filesystem without declaring `! {FS}`, it doesn't compile. The gap between what the AI claims and what the code requires is closed at the language level, not discovered at runtime by a frustrated developer.

**Environment pinning for deterministic execution.** `AILANG_SEED=42` pins the random-number generator. `TZ` pins the timezone. `AILANG_FS_SANDBOX` restricts filesystem access to a declared directory. Same inputs, same seed, same environment — identical output. Not approximately. Exactly. You can replay a past generation, diff it against a new one, and know that any difference is meaningful rather than noise.

The benchmark data shows this isn't a clean win — yet. On single-shot generation, Python's familiarity to the models still edges out AILANG's structural advantage by a few points overall. But the per-model picture is more revealing: where the language design actually pays off is with capable models in agentic harnesses. GPT-5.5 hits 90.9% on AILANG single-shot. Sonnet 4.6 in opencode hits 91.7% on AILANG. Several harness × AILANG combinations cross **100%**. The pattern: the better the model and the better the harness, the more AILANG's reproducibility guarantees translate into measurable success.

[COMPONENT: `<RepairEffectiveness />` or `<ModelDeltaTrend />` showing how repair-loop and agent-mode change the AILANG vs Python gap per model]

The trade-off, stated honestly: AILANG is less expressive than Python for humans, and the models have far more Python in their training data. That's why we run the benchmarks in both languages — so we can measure the gap, watch it close as models get better at AILANG, and prove the design thesis holds. If a human is writing the code, use Python. If an AI is writing the code in a context where reproducibility matters, the question stops being "which language do humans prefer?" and starts being "which language gives the AI the narrowest target?"

---

## The audit trail you never had with humans

Here's the part of this that's genuinely counterintuitive: **delegating coding to AI gives you more provenance, not less, than having a human do it.**

The usual framing is the opposite. AI is the black box; the human is accountable. Ask a developer why they made a decision and they'll tell you. Ask an AI and you get a hallucinated rationalisation. So the conventional wisdom is that handing work to an AI loses you the audit trail.

That's only true if you're not capturing what the AI does. And the thing about AI is — it has to think in text. Every reasoning step, every tool call, every "let me try this approach instead," every retry after a failed test, every decision about which library to use — all of it happens in language, and all of it can be logged. The model literally cannot reason without producing text. If it makes a decision, that decision exists as words somewhere in the trace.

Compare that to a human developer. Most of their reasoning happens silently, inside their head. They open a file, stare at it for two minutes, type three lines, run the tests, commit. The commit message says "fix bug." The decision-making process — why those three lines, why that approach, why not the alternative — is gone. You can ask them a week later, but what you'll get is a reconstruction, not a record. Most of what humans actually decide leaves no paper trail at all.

This flips the audit story on its head. With AI-generated code, properly captured, you have:
- The exact prompt that initiated the work
- The full system prompt and context window the model saw
- Every tool call the model made, with arguments and results
- Every intermediate reasoning step
- The code that came out, diffable against the prompt
- The cost and token count of the whole exchange

AILANG's Observatory makes this concrete. Run `ailang chains list` to see every AI-driven task. Run `ailang chains chat <chain-id>` to read the turn-by-turn conversation that produced a specific code change — exactly which prompt, which response, which retry, which fix. Run `ailang chains diff <chain-id>` to see the resulting code change tied back to the conversation. Run `ailang chains stats --by-agent` for cost and token rollups. The dashboard surfaces all of it visually. None of this is hypothetical; it's how we work on AILANG itself.

[COMPONENT: screenshot of `ailang chains chat` output showing turn-by-turn conversation, or dashboard view of chain history]

The implication is uncomfortable for some readers and freeing for others: in domains where audit trails matter — regulated industries, legal evidence, compliance reviews — AI-generated code can be *more* defensible than human-generated code, provided you capture the chain. You can't subpoena a developer's thought process. You can subpoena a chat log.

This is what reproducibility looks like at scale. Not just "same prompt produces same code" but "and here's the entire reasoning trail that got us there, recorded automatically, queryable forever, diffable against any other run." The five-doors problem we opened with isn't just solved — it's inverted. With humans, you don't even know which five doors there were. With AI plus the right harness, every door the model considered is logged.

---

## Reproducibility is just analytics for AI code

If you've spent any time in digital analytics, this should feel familiar in shape if not in detail. We spent fifteen years figuring out how to capture web events — pageviews, sessions, conversions — and the discipline of making sure that data was reliable, complete, and reproducible. The same discipline now applies to AI outputs, and the mapping is direct. Conversion rate becomes task success rate. Bounce rate becomes hallucination and retry rate. Cost per acquisition becomes cost per generation. Funnels become trace trees. The metrics rename; the thinking doesn't.

The benchmark dashboard above is essentially a GA4 for AI code generation. Task success rate per model. Cost per task. Dependency completeness. Repair effectiveness. Cross-harness comparison. It's the same shape of report you'd build for any digital product, applied to code artefacts instead of pageviews — and most teams shipping AI-generated code aren't building it at all. They have no equivalent of bounce rate. No cost-per-acquisition. They ship and hope.

This matters because of where the competitive surface for AI products has moved. Three things make a viable AI product: the unique data only you have, the model behind it, and the harness around it — the eval pipeline, the trace capture, the tool catalogue, the language the AI writes in. The model is increasingly a commodity. Everyone has access to GPT, Claude, and Gemini. Your data is yours. **Your harness is your moat.** And reproducibility is what makes the harness work — without it, your evals don't replay, your traces don't compare, your costs don't reconcile.

A language designed for AI is part of that harness. AILANG isn't competing with Python for human developers; it's the layer of the harness that makes generated code measurable. Same logic as Langfuse-as-harness for chat conversations: AILANG-as-harness for code artefacts. If you can't replay the generation, you can't analyse it. If you can't analyse it, you can't improve it. And the team that can — the team whose harness produces measurable, reproducible AI output — wins on something the model commoditisation can't take away.

---

## The sectors that already require this

This isn't a theoretical concern for everyone. Some industries already require what most AI coding tools can't provide.

In aviation, the DO-178C certification standard treats AI-generated code identically to human code. Same verification, same traceability, same audit requirements. You must be able to reproduce any build from source. The FAA doesn't care who wrote your flight control software — human or AI — it must be reproducible, testable, and auditable. AI is positioned as "assistant, not autonomous generator" for certified code.

In medical devices, the FDA's January 2025 draft guidance requires Total Product Life Cycle documentation for AI-enabled software, including risk assessment, validation, and cybersecurity. If an AI generates code for a pacemaker, every line needs provenance.

In financial services, SEC and FINRA are watching AI-generated trading algorithms. A non-reproducible model making allocation calls is a compliance gap waiting to be discovered.

These sectors aren't waiting for consensus on AI code quality. They already require what the benchmark data shows most AI coding stacks can't reliably deliver: proof that you can replay the generation and get the same result. The question isn't whether reproducibility will be required more broadly — it's whether your tools will be ready when it is.

---

Code is deterministic. AI-generated code isn't. Not because AI is broken, but because the languages AI writes in were designed for a different kind of author — one with preferences, conventions, and consistency across sessions. AI has none of these. It needs them supplied by the language itself.

The five-ways-to-transform-a-list problem isn't a Python bug. It's a design feature that becomes a liability when the author changes from human to machine. Reproducibility for AI-generated code starts with giving the AI fewer degrees of freedom — not fewer capabilities, but fewer ways to express the same capability.

> *A language designed for human creativity gives AI five doors and no memory of which one it opened last. A language designed for AI gives it one door and a receipt.*

*Next week: why "just ask the AI to explain itself" is fantasy — and why the strongest evidence comes from Anthropic's own researchers.*

*This post also appears on the [Sunholo blog](https://www.sunholo.com/blog/if-you-cant-replay-it) with interactive diagrams.*
