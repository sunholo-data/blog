# Post 3 — Visibility: notes & material to build from

**Status:** notes / scaffolding
**Series principle:** *"Visibility, not opacity, produces authority."*
**Question this post answers:** "Can we observe what the AI did?"
**Author tag:** `me`
**Tags:** `ai-delegation`, `visibility`, `observability`, `audit`, `ailang`

---

## Series-intro framing to anchor on

From the series introduction (post 0 / wrong-question-ai-trust):

> "You cannot see inside a model's head, and even if you could, the lab that built it has shown you probably shouldn't trust what you find there. Anthropic — the company that builds Claude — published research showing that when their own model does arithmetic, it uses internal computation paths that don't match the step-by-step explanation it gives you when asked. Their word for this: 'bullshitting.' The reasoning a model shows you is a performance, not a transcript. It's been trained to be a helpful assistant, but in some sense that is just cosplay. But you don't *need* to understand how the AI thinks — if you can see what it *did* — every input, every output, every side effect — then you can judge the AI based on its actions, not its intent. Asking an AI to explain its thoughts is mostly fantasy. Explainability of action is mandatory and achievable today."

**Post 3's central pivot:** the AI's explanation of itself is unreliable, but the AI's *actions* are observable. We swap explainability-of-thought for explainability-of-action.

Anthropic source: [Reasoning models don't always say what they think](https://www.anthropic.com/research/reasoning-models-dont-say-think)

---

In the third blog about how to trust AI, we talk about visibility.  This refers to getting accountability on what an AI model did.  We can't just ask the AI like we could perhaps do with a human developer - the answers AI will give you on why it did what it did are a complete fiction.  AIs are cosplaying a 'helpful assistant' and are answering in patterns that its training has reinforced, but the ACTUAL intentions of what happened at the time are buried deep within their neural nets. Anthropic — the company that builds Claude — published research showing that when their own model does arithmetic, it uses internal computation paths that don't match the step-by-step explanation it gives you when asked. Their word for this: 'bullshitting.' The reasoning a model shows you is a performance, not a transcript.

But for trust, we don't actually need this.  Just as we can never know (or have the right to know?) the workings of other humans' inner motivations, it is the actions that can be judged instead.  We can get a paper trail of actions taken, and paradoxically when using AI we can actually get a much better one than before with a purely human process.  We can't get explanability of thoughts, but we can get explaintability of action

--- 

## Forward link from post 2

End of post 2 promises: *"why 'just ask the AI to explain itself' is fantasy, why the strongest evidence comes from Anthropic's own researchers, and why what the AI did is more useful than what the AI says it did."*

That's the three-act structure of post 3 already:

1. Why asking the AI to explain itself is fantasy (Anthropic's "bullshitting" research)
2. The alternative: action-level observability
3. AILANG's Observatory as a worked example — chains, traces, dashboard

---

## Material moved here from post-2 v2 (audit trail section)

This was originally drafted into post 2 but is fundamentally a *visibility* argument, not a reproducibility argument. The reproducibility post is about whether the same prompt produces the same code. This material is about whether you can **see what happened**. Belongs here.

### Section: "The audit trail you never had with humans"

**Counterintuitive thesis:** delegating coding to AI gives you more provenance, not less, than having a human do it.

The conventional framing is the opposite. The AI is the black box; the human is accountable. Ask a developer why they made a decision and they'll tell you. Ask an AI and you get a hallucinated rationalisation. Conventional wisdom: handing work to an AI loses you the audit trail.

That's only true if you're not capturing what the AI does. And here's the thing about AI — it has to think in text. Every reasoning step, every tool call, every "let me try this approach instead," every retry after a failed test, every decision about which library to use, all of it happens in language. The model literally cannot reason without producing tokens. If it makes a decision, that decision exists as words somewhere in the trace.

Compare that to a human developer. Most of their reasoning happens silently, inside their head. They open a file, stare at it, type three lines, run the tests, commit with the message "fix bug." The decision-making process — why those three lines, why that approach, why not the alternative — is gone. You can ask them a week later, but what you'll get is a reconstruction, not a record. The vast majority of what humans actually decide leaves no paper trail.

This flips the audit story. With AI-generated code, properly captured, you have the exact prompt, the full context window the model saw, every tool call with arguments and results, every intermediate reasoning step, the final code diffable against the prompt, and the cost and token count of the whole exchange.

AILANG's Observatory makes this concrete. Run `ailang chains list` to see every AI-driven task. Run `ailang chains chat <chain-id>` to read the turn-by-turn conversation that produced a specific code change — exactly which prompt, which response, which retry, which fix. Run `ailang chains tree <chain-id>` to see the full hierarchy of stages with cost and turn counts per stage. Run `ailang chains journey <chain-id>` for a narrative step-by-step replay including which model failed and why. Run `ailang chains stats --by-agent` for cost and token rollups. The dashboard surfaces all of it visually. None of this is hypothetical; it's how we work on AILANG itself.

[IMAGE: Screenshot of `ailang chains chat` output showing turn-by-turn conversation, or dashboard view of chain history]

The implication is uncomfortable for some readers and freeing for others. In domains where audit trails matter — regulated industries, legal evidence, compliance reviews — AI-generated code can be *more* defensible than human-generated code, provided you capture the chain. You can't subpoena a developer's thought process. You can subpoena a chat log.

The five doors of post 2 don't just get reduced to one — every door the model considered along the way is logged, including the ones it didn't take.

---

## Material moved here from post-2 v2 (analytics-for-AI-code section)

Originally drafted into post 2 under the heading *"Reproducibility is just analytics for AI code,"* but the substance is observability/visibility, not reproducibility. Belongs here. This is also the spine of the *"Analytics for AI Agents"* talk (Analytics.dev Copenhagen, 29 April 2026) — that talk's material can be lifted into this post directly.

### Section: "Visibility is just analytics for AI code"

If you've spent any time in digital analytics, this should feel familiar in shape if not in detail. We spent fifteen years figuring out how to capture web events — pageviews, sessions, conversions — and the discipline of making sure that data was reliable, complete, and reproducible. The same discipline now applies to AI outputs, and the mapping is direct. Conversion rate becomes task success rate. Bounce rate becomes hallucination and retry rate. Cost per acquisition becomes cost per generation. Funnels become trace trees. The metrics rename; the thinking doesn't.

The AILANG benchmark dashboard is essentially a GA4 for AI code generation. Task success rate per model. Cost per task. Dependency completeness. Repair effectiveness. Cross-harness comparison. It's the same shape of report you'd build for any digital product, applied to code artefacts instead of pageviews — and most teams shipping AI-generated code aren't building it at all. They have no equivalent of bounce rate. No cost-per-acquisition. They ship and hope.

This matters because of where the competitive surface for AI products has moved. Three things make a viable AI product: the unique data only you have, the model behind it, and the harness around it — the eval pipeline, the trace capture, the tool catalogue, the language the AI writes in. The model is increasingly a commodity. Everyone has access to GPT, Claude, and Gemini. Your data is yours. **Your harness is your moat.** Visibility is what makes the harness work — without it, your evals are blind, your traces are noise, your costs are guesses.

A language designed for AI is part of that harness. AILANG isn't competing with Python for human developers; it's the layer of the harness that makes generated code measurable. Same logic as Langfuse-as-harness for chat conversations: AILANG-as-harness for code artefacts. If you can't see the generation, you can't analyse it. If you can't analyse it, you can't improve it.

---

## Connection to the Analytics for AI Agents talk (29 April 2026)

Talk outline at: `/Users/mark/dev/sunholo/presentations/analytics-for-ai-agents/outline.md`

Reusable material from the talk that lands in this post:

- **The Rosetta Stone mapping** (talk §1.2) — GA4 → Langfuse: session→trace, pageview→generation, event→tool call, user ID→thread ID, custom dimensions→metadata. *"You're not tracking a journey. You're tracking reasoning."*
- **The new metrics mapping** (talk §3.7) — pageviews→tool calls, sessions→traces, conversion rate→task success rate, bounce rate→hallucination & retry rate, cost per acquisition→cost per task, funnels→trace trees, custom dimensions→LLM-as-judge scores. *"The tools changed. The thinking didn't."*
- **The Hero Story** (talk §2.3) — *"We thought everyone was doing X. They were actually doing Y."* — concrete example of using prompt logs to discover the real workflow vs. the documented one.
- **The Trifecta** (talk §3.5) — unique data (yours alone) + commodity model + harness/UX (your surface). *"Your website used to be the destination. Now it's the visible surface of your harness."*
- **Closing line** — *"The richest analytics data in your organisation might not be in your website tags anymore. It might be in the conversations your users are having with AI. Don't give that gold away."*

---

## OSS bans — a real-world provenance failure case

Major open-source projects have started refusing AI-generated contributions specifically because the licensing chain can't be verified. This is provenance failure made concrete, and it makes a strong anchor for the visibility post.

### The four projects

| Project | Date | Position | Reasoning |
|---|---|---|---|
| **NetBSD** | May 2024 | Ban | "Code generated by a large language model... is presumed to be tainted code, and must not be committed without prior written approval by core." |
| **Gentoo** | April 2024 | Ban (Council motion 6–0) | Copyright infringement risk + quality + ethics. Górny: "an extension of current rules on copyrighted code." |
| **QEMU** | June 2025 | Ban | *"With AI content generators, the copyright and license status of the output is ill-defined with no generally accepted, settled legal foundation,"* so contributors cannot credibly assert DCO clauses (b) or (c). |
| **Linux kernel** | Early 2026 | Permitted with disclosure | AI-assisted patches allowed, but: AI MUST NOT add `Signed-off-by` (only humans can sign DCO), and AI involvement must be disclosed via `Assisted-by: <model>` trailer. |

The pattern across all four: **the DCO / license chain cannot be honestly signed for LLM output** because the training corpus contains code under incompatible licenses. Three projects refuse the contribution; the kernel relocates the liability onto the human signer.

### Why this fits visibility, not reproducibility

The OSS projects don't object that AI generates *different* code each time — they object that you can't trace where any one line *came from*. That's a visibility/audit-trail argument: provenance is a kind of trace. The NetBSD / Gentoo / QEMU bans are what happens when visibility fails — when the chain from training data → model → output isn't legible enough for legal sign-off.

### The AILANG counter-angle (genuinely interesting)

Worth using as a punchline somewhere in post 3 — possibly the close, possibly its own short aside:

> *AILANG isn't in any model's training corpus. The series introduction establishes this directly: the model gets a two-page prompt describing the language, then writes code from scratch. So when an AI generates AILANG, it can't be regurgitating GPL'd Python or proprietary C — there's nothing to regurgitate. The provenance problem that NetBSD, Gentoo, and QEMU are refusing contributions over largely doesn't apply to AILANG, because the model is reasoning structurally from the prompt rather than recalling training examples. Visibility into the provenance chain is trivial: there is no chain.*

This is a structural benefit of the language design that no Python-target AI tool can match. The novel language is the audit trail.

### Sources

- [NetBSD Commit Guidelines](https://www.netbsd.org/developers/commit-guidelines.html)
- [Gentoo Council AI policy](https://wiki.gentoo.org/wiki/Project:Council/AI_policy)
- [The Register — Gentoo bans AI code](https://www.theregister.com/2024/04/16/gentoo_linux_ai_ban/)
- [QEMU code-provenance docs](https://www.qemu.org/docs/master/devel/code-provenance.html)
- [QEMU policy commit 3d40db0](https://github.com/qemu/qemu/commit/3d40db0efc22520fa6c399cf73960dced423b048)
- [Linux kernel AI Coding Assistants policy](https://docs.kernel.org/process/coding-assistants.html)
- [SFC comments to US Copyright Office (Nov 2023)](https://sfconservancy.org/news/2023/nov/01/us-copyright-office-generative-ai-machine-learning/) — useful neutral third-party voice
- [SFC on SCOTUS Thaler denial (Mar 2026)](https://sfconservancy.org/blog/2026/mar/04/scotus-deny-cert-dc-circuit-thaler-appeal-llm-ai/) — human-authorship requirement reaffirmed

---

## Other beats post 3 should hit

- **Anthropic "bullshitting" research** — the model's chain-of-thought is a performance, not a transcript. Strongest evidence because the company building the model is the one publishing it.
- **The flip from explainability-of-thought to explainability-of-action** — you don't need to know what the AI thought; you need to know what it did. Every input, every output, every side effect.
- **Observability stack mapping** — Langfuse for chat traces, OpenTelemetry for tool calls, AILANG Observatory for code-generation chains. All the same idea: capture actions, not intentions.
- **The harness-as-moat argument** (echo from post 2 analytics section) — if you can't see what your AI did, you can't improve it. Visibility IS the harness.
- **Regulated sectors revisited** — EU AI Act Article 13 (transparency requirements), Article 86 (right to explanation). Insurance / hiring / credit-scoring AI must produce audit trails by August 2026.
- **Possible incident anchor** — Cigna PXDX (1.2-second denials with no audit trail) or UnitedHealth nH Predict. These were originally drafted into post 2 but they're about opacity, not non-determinism — they fit here.

---

## Sources to draw on

- [Anthropic — Reasoning models don't always say what they think](https://www.anthropic.com/research/reasoning-models-dont-say-think)
- [EU AI Act Article 13 (Transparency)](https://artificialintelligenceact.eu/article/13/)
- [EU AI Act Article 86 (Right to Explanation)](https://artificialintelligenceact.eu/article/86/)
- [ProPublica — Cigna's algorithm](https://www.propublica.org/article/cigna-pxdx-medical-health-insurance-rejection-claims) — if using as opacity anchor
- [CBS News — UnitedHealth AI denials](https://www.cbsnews.com/news/unitedhealth-lawsuit-ai-deny-claims-medicare-advantage-health-insurance-denials/) — if using as opacity anchor
- AILANG Observatory docs: `/Users/mark/dev/sunholo/ailang/docs/docs/guides/agent-workflows.mdx`, `traces.md`
- AILANG `chains` command sources: `/Users/mark/dev/sunholo/ailang/cmd/ailang/chains*.go`

---

## Concrete `ailang chains` examples (verified 2026-05-03)

Live data from the AILANG Observatory, ready to lift into the post or use as screenshots. All commands run against the local `ailang` binary; data flows from real eval runs over the past 30 days.

### Headline aggregate (mirrors the analytics-talk framing)

`ailang chains stats --by-agent`:

```
Chain Stats (all time)
═══════════════════════════════════════════
  Chains:     68 total (53 completed, 6 active, 9 failed)
  Total Cost: $310.3006
  Avg/Chain:  $4.5632
  Tokens:     139,289,193

By Agent:
  AGENT          STAGES  DONE  FAILED  COST       TOKENS
  eval-agent     3,196   2,211   985   $220.36    100.6M in / 3.2M out
  eval-standard  3,415   2,362  1,037  $89.94      34.4M in / 1.1M out
```

This is the GA4-for-AI-code dashboard from the talk made literal. *"Cost per acquisition becomes cost per generation"* → there it is, $4.56 average per chain.

### Chain-as-task overview

`ailang chains list` returns a table that reads like a session log:

```
ID               STATUS     SOURCE                                        STAGES  COST    CREATED
b2ed8a07-bc2...  completed  eval_suite:eval-1777283287104819000/agent     34      $3.16   2026-04-27 11:48
2dc63da0-5f1...  completed  eval_suite:eval-1777272689996723000/agent     398     $57.33  2026-04-27 08:51
93727165-54b...  completed  eval_suite:eval-1777271634184221000/standard  307     $15.86  2026-04-27 08:33
```

One chain. 398 stages. $57.33. Every stage individually addressable.

### Tree view — hierarchy with success/failure markers

`ailang chains tree b2ed8a07-bc2`:

```
completed eval_suite (eval-1777283287104819000/agent)
├── ✗ eval-agent
├── ✓ eval-agent (8 turns, $0.10)
├── ✗ eval-agent (10 turns, $0.09)
├── ✓ eval-agent (4 turns, $0.04)
├── ✓ eval-agent (5 turns, $0.08)
├── ✓ eval-agent (11 turns, $0.10)
├── ✗ eval-agent (22 turns, $0.23)
...
```

Stage-by-stage, you can see which attempts succeeded, which failed, and what each one cost. *"Five doors of post 2 don't just get reduced to one — every door the model considered along the way is logged, including the ones it didn't take."*

### Chat — the turn-by-turn record

`ailang chains chat b2ed8a07-bc2 --stage 4 --compact` shows a clean retry-after-failure loop in raw form:

```
Session: d16e7d5c-538... (Stage 4: config_file_parser)
46 messages, 10 turns, 9 tool calls

─── Turn 0 (assistant) ───
I'll solve this AILANG benchmark step by step. Let me start by reading the solution file template.
  [tool] Read: solution.ail

─── Turn 4 (assistant) ───
Now let me verify the solution by running it:
  [tool] Bash: cd /var/folders/.../benchmark && ailang run solution.ail

─── Turn 5 (user) ───
  [result:ERROR] Exit code 1
  → Type checking...
  → Effect checking...

─── Turn 5 (assistant) ───
Let me check the directory and fix the path:
  [tool] Bash: pwd && ls -la /var/folders/...

─── Turn 6 (assistant) ───
  [tool] Edit: solution.ail
```

This is the paragraph from the audit-trail section made literal: *"every retry after a failed test, every decision about which library to use, all of it happens in language."* Strong screenshot candidate — this *is* the audit trail you never had with humans.

### Journey — the narrative replay

`ailang chains journey b2ed8a07-bc2`:

```
Steps:
  1. [FAILED] Ran agent evaluations
     Error: executor "gemini" failed for model "gemini-3-flash-preview": exit status 1
  2. [done]   Ran agent evaluations  $0.10  35s
  4. [FAILED] Ran agent evaluations  $0.09  49s
  20. [FAILED] timeout after 1m0s (hard ceiling)
  25. [FAILED] executor "claude" failed for model "haiku": timeout after 1m0s
  30. [FAILED] executor "opencode" failed for model "anthropic/claude-haiku-4-5": opencode produced no output within 30s (prefill timeout)
```

Worth a paragraph in its own right: **the failure modes are themselves the audit gold.** Which model. Which executor. Which timeout. What it cost. No human PR review carries this kind of forensic detail. This is the harness-as-moat argument concretised — your AI's failures are observable in a way that humans' aren't.

### Caveats / known gaps to address before publishing

- **`ailang chains diff` currently returns "No diffs available (worktrees may have been cleaned up)"** for the chains in our window. Either drop the diff claim from the draft or run a fresh chain with worktree retention before screenshotting. Right now `tree` + `journey` carry the load.
- **`chains health` shows empty** because the most recent chain is from 2026-04-27 (6 days ago) — outside the 24h window. Not broken; just stale. Run a fresh chain before screenshotting if you want a populated health report.
- **All 68 chains in the last 30 days are `eval_suite` chains** — no coordinator-driven coding tasks. So *"Run `ailang chains list` to see every AI-driven task"* is slightly aspirational; current data shows benchmark eval runs, not feature work. Either run a coordinator task before screenshotting, or reframe as *"every benchmarked AI run"*.
- The post should probably show one fresh coordinator chain (with `diff` working) alongside the existing eval data, to demonstrate both the macro analytics view (60+ chains, $310, by-agent rollup) and the micro audit-trail view (one task, every turn, every tool call, the resulting diff).

---

## Pull-quote candidates

- *"You can't subpoena a developer's thought process. You can subpoena a chat log."*
- *"Asking the AI to explain itself is fantasy. Asking the harness what the AI did is mandatory and achievable."*
- *"Explainability of thought is unreliable. Explainability of action is your moat."*
