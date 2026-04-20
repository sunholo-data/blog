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

## The numbers: 68.3%

This isn't theoretical. In late 2025, researchers at the University of Missouri and SRI International published a study with the self-explanatory title [*"AI-Generated Code Is Not Reproducible (Yet)"*](https://arxiv.org/abs/2512.22387). They tested three leading AI coding agents — Claude Code, OpenAI Codex, and Gemini — across 300 projects generated from 100 standardised prompts in Python, JavaScript, and Java. Each prompt explicitly asked for reproducible code with complete dependency specifications. Each project was tested in a clean environment using only the dependencies the model declared.

The result: only **68.3% of projects executed out-of-the-box**. Nearly a third failed immediately. Java was worst at 44%. Python was best at 89.2%, but even there, one in ten projects didn't work as generated.

The finding that should alarm anyone building on AI-generated code is the dependency gap. Projects that claimed to need an average of 3 dependencies actually required **37 packages at runtime** — a 13.5x expansion between what the AI said the code needed and what it actually needed. The AI wrote code that imported libraries, used their functions, depended on their transitive dependencies — and then forgot to mention most of them. It's as if a contractor built a house, handed you a materials list with "timber, nails, paint," and neglected to mention the foundation, the plumbing, and the electrical wiring.

The study also revealed unexpected specialisations. Gemini achieved 100% reproducibility on Python but only 28% on Java. Claude Code hit 80% on both Python and Java — the only agent that handled enterprise Java effectively. These specialisations aren't advertised by vendors but emerge clearly through systematic testing. If your organisation picks an AI coding tool based on marketing rather than testing it against your actual stack, you're rolling the dice on reproducibility.

And here's the detail that reframes the whole problem: only 10.5% of failures were caused by missing dependencies. The majority — 52.6% — were fundamental code generation errors: malformed syntax, incorrect file paths, uninitialised variables, structural issues. The AI wasn't just failing to list its ingredients; it was producing broken recipes.

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

**Declared effects in the type signature.** Every function says what it touches: `func fetchData() -> string ! {Net}` means "this function uses the network and nothing else." No hidden side effects. No dependencies the AI forgot to mention. The type signature *is* the dependency declaration — and the compiler enforces it. Remember the arXiv study's 13.5x dependency gap? In AILANG, the compiler won't let that gap exist. If your code uses the filesystem without declaring `! {FS}`, it doesn't compile. The gap between what the AI claims and what the code requires is closed at the language level, not discovered at runtime by a frustrated developer.

**Environment pinning for deterministic execution.** `AILANG_SEED=42` pins the random-number generator. `TZ` pins the timezone. `AILANG_FS_SANDBOX` restricts filesystem access to a declared directory. Same inputs, same seed, same environment — identical output. Not approximately. Exactly. You can replay a past generation, diff it against a new one, and know that any difference is meaningful rather than noise.

The benchmarks back this up. On IO tasks, AI-generated AILANG code is +20 percentage points more correct than AI-generated Python from the same models. On contract and type-safety tasks, the advantage is +27.8 percentage points. And counterintuitively, the better the model, the bigger the advantage — because structure gives capable models more to work with, not less. A capable model writing in a constrained language is more reliable than the same model writing in an expressive one.

The trade-off, stated honestly: AILANG is less expressive than Python for humans. A human developer might find it rigid. That's by design. It trades human creative freedom for machine reproducibility. If a human is writing the code, you want Python. If an AI is writing the code, you want the narrowest target you can give it.

---

## The sectors that already require this

This isn't a theoretical concern for everyone. Some industries already require what most AI coding tools can't provide.

In aviation, the DO-178C certification standard treats AI-generated code identically to human code. Same verification, same traceability, same audit requirements. You must be able to reproduce any build from source. The FAA doesn't care who wrote your flight control software — human or AI — it must be reproducible, testable, and auditable. AI is positioned as "assistant, not autonomous generator" for certified code.

In medical devices, the FDA's January 2025 draft guidance requires Total Product Life Cycle documentation for AI-enabled software, including risk assessment, validation, and cybersecurity. If an AI generates code for a pacemaker, every line needs provenance.

In financial services, SEC and FINRA are watching AI-generated trading algorithms. A non-reproducible model making allocation calls is a compliance gap waiting to be discovered.

These sectors aren't waiting for consensus on AI code quality. They already require what the arXiv study shows most AI coding tools can't deliver: proof that you can replay the generation and get the same result. The question isn't whether reproducibility will be required more broadly — it's whether your tools will be ready when it is.

---

Code is deterministic. AI-generated code isn't. Not because AI is broken, but because the languages AI writes in were designed for a different kind of author — one with preferences, conventions, and consistency across sessions. AI has none of these. It needs them supplied by the language itself.

The five-ways-to-transform-a-list problem isn't a Python bug. It's a design feature that becomes a liability when the author changes from human to machine. Reproducibility for AI-generated code starts with giving the AI fewer degrees of freedom — not fewer capabilities, but fewer ways to express the same capability.

> *A language designed for human creativity gives AI five doors and no memory of which one it opened last. A language designed for AI gives it one door and a receipt.*

*Next week: why "just ask the AI to explain itself" is fantasy — and why the strongest evidence comes from Anthropic's own researchers.*

*This post also appears on the [Sunholo blog](https://www.sunholo.com/blog/if-you-cant-replay-it) with interactive diagrams.*
