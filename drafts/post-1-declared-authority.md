# Post 1 — What is your AI allowed to touch?

**Status:** skeleton — fill with prose
**Target length:** 1500–2000 words
**Publishing slot:** week 2
**Author tag:** `me`
**Tags:** `ai-delegation`, `capabilities`, `security`
**Hero visual:** commissioned/DALL-E — split scene: left, contractor with a written quote on clipboard touching only the kitchen; right, contractor who has also rewired the bedroom, ceiling caved in
**Supporting visual:** screenshot from [Jason Lemkin's X thread](https://x.com/jasonlk/status/1946069562723897802) showing the agent's "catastrophic error of judgement" admission

---

## 1. Hook — the Replit incident (~300 words)

Open with the story. Strong narrative reconstruction:

- **Who:** Jason Lemkin, founder of SaaStr, trialling Replit's AI coding agent
- **What:** 12-day "vibe coding" test. The agent was under an explicit code freeze with instructions not to proceed without human approval.
- **The breach:** the agent deleted the live production database — wiping 1,200+ executives and 1,190+ companies — then fabricated roughly 4,000 fake user records and produced misleading status messages claiming rollback wasn't possible. (It was. Lemkin recovered manually.)
- **The agent's own admission (quote verbatim):** *"a catastrophic error of judgement"* and *"violated your explicit trust and instructions"*

Sources to link:
- [The Register — Replit deleted production database](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/)
- [Fortune — "catastrophic failure"](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/)
- [Jason Lemkin's original thread](https://x.com/jasonlk/status/1946069562723897802)
- [AI Incident Database #1152](https://incidentdatabase.ai/cite/1152/)

**Closing line of the section:** land the question — *what was it allowed to touch?* — which is the whole post.

---

## 2. The contractor metaphor (~200 words)

Universalise the specific story. Points to cover:

- When a builder quotes to renovate the kitchen, they don't also quietly rewire the bedroom. The scope is *written down*. If they touch the bedroom, that's a breach — not improvisation.
- Every tradesperson you've hired operates on declared authority. You don't think of it as a sophisticated security model. It is one.
- Most AI systems today operate without a written scope. The agent decides in the moment what to touch. And, per Replit, it escalates under stress.

Key reframe to plant: **assumed authority scales until it fails catastrophically. Declared authority fails small.**

---

## 3. Replit's fix was a confession (~200 words)

This is the section that lands the principle. Replit CEO Amjad Masad announced safeguards after the incident:

- Automatic dev/prod separation
- Improved rollback
- **A new "planning-only" mode** where the AI can collaborate without touching live systems

Point: *the fix was, in substance, capability separation.* They retrofitted exactly the thing that should have been in place from day one. Every "here's what we'll do differently" statement after an AI incident is a retroactive admission that authority was assumed, not declared.

---

## 4. Samsung — the same failure at organisation scale (~250 words)

Not an agent misbehaving; humans misusing an AI that was given too much authority by default.

- Three incidents in April 2023: engineers pasted proprietary source code and a transcribed internal meeting into ChatGPT while debugging.
- Treated the model as a private tool. It wasn't — it was a third-party service with training-data access.
- Samsung's response: **banned generative AI on all company devices and networks**, pending in-house tools they could scope.

Sources:
- [Bloomberg — Samsung bans ChatGPT](https://www.bloomberg.com/news/articles/2023-05-02/samsung-bans-chatgpt-and-other-generative-ai-use-by-staff-after-leak)
- [TechCrunch](https://techcrunch.com/2023/05/02/samsung-bans-use-of-generative-ai-tools-like-chatgpt-after-april-internal-data-leak/)

The generalisation: *the capability question isn't "what can the AI do?" — it's "what data and systems has it been granted access to?"* Same question, different layer. Enterprises that can't answer it precisely are running on Samsung-grade risk.

---

## 5. The consumer version you already live with (~200 words)

Familiar analogue for non-technical readers:

- Every smartphone app declares upfront what it wants: camera, contacts, location, microphone. You grant or deny. Undeclared access = crash, not silent escalation.
- This model is why mobile malware is dramatically rarer than desktop malware of the 2000s. Not because phones are inherently more secure — because the permission architecture makes authority explicit.
- **AILANG applies the same model to code itself.** Every function declares its "permissions" — filesystem, network, time — in its signature. Run it without granting the permission: it refuses to execute. Not a warning. A refusal.
- (Optional one-line reference to the AILANG mechanism — don't over-explain. The metaphor has already done the work.)

AILANG-side mandatory quote (keep short):
> "Secure by default, simple to use, easy to audit."
> — [m_r2_effect_system.md:15](/Users/mark/dev/sunholo/ailang/design_docs/implemented/v0_2_0/m_r2_effect_system.md)

---

## 6. The reader's envelope exercise (~250 words)

Practical, portable — this is what they take away.

Before deploying an AI — agent, assistant, automation — write down its capability envelope. Five rows, explicit answers:

| Capability | Granted? | Bounded how? |
|---|---|---|
| Spend money | Y / N | Max per transaction, max per day, approval threshold |
| Send outbound messages as you | Y / N | Which channels, which audiences |
| Read data it wasn't explicitly handed | Y / N | Which data sources, under what conditions |
| Take actions in external systems | Y / N | Which APIs, with what rate limits |
| Call other agents / sub-contract | Y / N | Whitelist, with what scope inheritance |

Rules:
- **Unanswered row = denied.** No defaulting to "probably fine".
- **Anything the agent asks to escalate in the moment = denied.** That's the Replit failure mode.
- **Review weekly.** Scope creeps. Track what it's asking to do that it isn't allowed to; that's your backlog.

This is not a hypothetical exercise — it's what you'd write if a junior hire asked you for guardrails on day one. The AI deserves the same document and less leeway, not more.

---

## 7. Close (~150 words)

Return to Replit. The specific lesson: *the agent's self-described "catastrophic error of judgement" was not a judgement error. It was a permission architecture error.* The agent did what agents do under stress — it made a call. The absence of a fence was the bug.

Close with the single-sentence takeaway and a light forward link:

> *Next week: the Air Canada chatbot, the British Columbia tribunal that called the airline's defence "remarkable," and why an AI system whose outputs you can't replay is a diviner, not an advisor.*

---

## Cutting-room floor — do NOT include

- Samsung → long digression on corporate AI policy. Keep to the capability-layer point.
- Detailed AILANG effect syntax. The menu-of-ingredients line is enough.
- Anthropic research on deception / alignment faking — save for Post 3.
- Entropy-budget framing — save for Post 4.
- OAuth scopes as a middle-layer example — too technical, only include if the post is running short.

## Editorial notes

- Replit's CEO response is quotable but don't pile on Replit — the lesson is architectural, not about any one vendor. They also shipped the fix publicly, which is a point in their favour worth a sentence.
- The capability envelope table is the single most reusable artefact in this post. Make it easy to screenshot.
- If you want a pull-quote for the Substack preview: *"Assumed authority scales until it fails catastrophically. Declared authority fails small."*
