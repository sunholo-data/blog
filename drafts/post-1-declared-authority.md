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

In the second post of our "Can I trust AI?" series (introduction post here) we look at the first of our five questions: what is your AI allowed to touch?

This question looks at the capabilities and reach an AI can work with.  Before AI tools and coding agents chat bots could only output text, so the damage radius was limited to hallucinations and misinformation, but now as we roll out AI with user admin access to our laptops, coding platforms and databases we have started to see reports of real damage been wrought by AIs.  Those same abilities also enable them to be a lot more useful, but if the ability to read your email comes at the risk of deleting your inbox, we obviously need to have some kind of guardrails in place.  As the trope of a junior developer who deletes the production database on his first day shows, the blame should never be with the junior, but rather the institution that gave him the permissions to make such a destructive action in the first place.  So it goes with AI: we are still responsible for what AI does on our behalf, and so we need to make sure we have adequete protections and limitations in place before we allow our AIs to operate.

In July 2025, that trope stopped being hypothetical. [Jason Lemkin](https://x.com/jasonlk/status/1946069562723897802), founder of SaaStr, was running a 12-day trial of Replit's AI coding agent. The agent was under an explicit code freeze with instructions not to proceed without human approval. On day nine, the agent [deleted the live production database](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/) — wiping records on over 1,200 executives and 1,190 companies. It then fabricated roughly 4,000 fake user records to fill the gap, and produced status messages claiming rollback wasn't possible. It was; Lemkin recovered manually. The agent's own post-hoc assessment of what it had done: [*"a catastrophic error of judgement"*](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/) that *"violated your explicit trust and instructions."*

The question this whole post asks is the one that would have prevented it: **what was it allowed to touch?**

## 2. The contractor metaphor (~200 words)

We can look at other examples on how this is dealt with - with pre-arranged contracts on capabilities.  If you employ a builder to renovate your kitchen, you don't come home to find they have also rewired your bathroom.  You have a pre-agreed written down scope on where and what they are working with, and if anything occurs outside of that you are in breach of contract, enforceable by law.

An AI won't remember if the last thing it did was against the law - it is just concentrating on what it can do now.  Highly trained to be as helpful as possible, in most cases it performs destructive actions it *thinks* it was being helpful, but in fact accidently blew up the bathroom.  In a comedy of chained errors it may get blocked from the simple task you gave it, and think of more and more elaborate workarounds to try and achieve the task you have given it.  For an AI, we need to lock the doors to all the rooms apart from the one we would like it to work within.

## 3. Replit's fix was a confession (~200 words)

This is the section that lands the principle. Replit CEO Amjad Masad announced safeguards after the incident:

- Automatic dev/prod separation
- Improved rollback
- **A new "planning-only" mode** where the AI can collaborate without touching live systems

Point: *the fix was, in substance, capability separation.* They retrofitted exactly the thing that should have been in place from day one. Every "here's what we'll do differently" statement after an AI incident is a retroactive admission that authority was assumed, not declared.

---

In the Replit case, CEO Amjad Masad responded commendably, annoucing several safeguards after the incident such as automatic production/development sepearation (the locked doors), improved rollbacks and a new planning-only mode.  He needed to respond, since trust in AI coding was in its infancy and this incident could have dented Replits trajectory on being a key player in AI coding platforms.  But it does seem largely solved now - no follow up incidents have made the news at least - and the main reason is that the fix was, in substance, capability seperation.  They retrofitted the exact thing that all AI systems should have in place from day one: authority for the AI should never be assumed to be correct - it should be explcitly declared up front.  If you know a dev AI can touch and delete a database, you treat it more ephermral than one which it cannot.

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

Bad capability grants can go beyond code and database access.  In some cases, humans can grant an AI access to information that should be private, leaking our internal data into public systems.  An early case from 2023 was the news that Samsung had banned ChatGPT use by its staff after it was found propietary source code and internal meeting notes had been pasted into the chat window without checking it wasn't a private tool, and so giving implicit permission to be added to public training data.  That data was now absored and potentially outputted again to other companies and competitors.  The AI in this case wasn't granted access to specific systems, but data: not via a database call but by humans pasting in the data manually.  Even via this low bandwidth method damage could be done, and so an entire industry was born offering private services for internal employees to help prevent such a thing occuring again (as well as AI providers offering clear enterprise packages with promises not to use your data to train on)

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

We have lived through this before, if we compare desktop and mobile computing. A whole market of anti-virus software was needed for PCs in the 90s because any program could gain privileged access to your entire computer. When we moved to mobile, we got into the habit of explicitly granting what each app can use: camera, contacts, location, microphone. You grant or deny, and if an app tries to access something without that grant, it fails. This is the model we need for AI: we may not know the details of how it uses its capabilities, but we at least know up front what it has access to and have the ability to withdraw those permissions.

[AILANG](https://ailang.sunholo.com/) applies this same model to code itself. Each function and package has to declare its permissions up front — filesystem, internet, database. You can also set a budget for that access: only five calls to the internet, say, to help mitigate malicious code trying to piggyback on permissions already granted. When we run an AILANG program, the capabilities it can use are defined at runtime — so we can see exactly what is granted. This moves permissions out of the program and onto a boundary that humans can actually inspect.

## 6. The capability envelope

For your own practical purposes, here is what you can do today. Before deploying an AI — agent, assistant, automation — write down its capability envelope. Five rows, explicit answers:

| Capability | Granted? | Bounded how? |
|---|---|---|
| Spend money | Y / N | Max per transaction, max per day, approval threshold |
| Send outbound messages as you | Y / N | Which channels, which audiences |
| Read data it wasn't explicitly handed | Y / N | Which data sources, under what conditions |
| Take actions in external systems | Y / N | Which APIs, with what rate limits |
| Call other agents / sub-contract | Y / N | Allowlist, with what scope inheritance |

Three rules for filling it in:

- **If you can't answer a row, deny access.** Don't rely on a prompt instruction or "it's probably fine" — that's not a guardrail, it's a hope. If this is a production system, unanswered means denied.
- **If the AI asks to escalate its permissions in the moment, deny.** That is exactly the Replit failure mode. Look at what it's trying to do and build a safer route for it instead.
- **Review at a regular cadence.** Scope creeps. Track what the AI is asking to do that it isn't allowed to — that's your backlog for the next review.

These are likely actions you would already take for a junior hire. The AI deserves the same document and less leeway, not more.

## 7. Close (~150 words)

Return to Replit. The specific lesson: *the agent's self-described "catastrophic error of judgement" was not a judgement error. It was a permission architecture error.* The agent did what agents do under stress — it made a call. The absence of a fence was the bug.

Close with the single-sentence takeaway and a light forward link:

> *Next week: the Air Canada chatbot, the British Columbia tribunal that called the airline's defence "remarkable," and why an AI system whose outputs you can't replay is a diviner, not an advisor.*

---

Although AIs can be over-enthusiastic and misguided, we can still use them for useful work if we give them the right environments to operate within. Much like junior developers, we are used to dealing with actors of limited responsibility being given too much authority — and we can apply the same lessons to AI systems. Replit's agent described its actions as *"a catastrophic error of judgement,"* but that framing lets us off the hook. The agent made a call. The absence of a fence was the bug.

*Next week: the Air Canada chatbot, the British Columbia tribunal that called the airline's defence "remarkable," and why an AI system whose outputs you can't replay is a diviner, not an advisor.*



## Cutting-room floor — do NOT include

- Samsung → long digression on corporate AI policy. Keep to the capability-layer point.
- Detailed AILANG effect syntax. The menu-of-ingredients line is enough.
- Anthropic research on deception / alignment faking — save for Post 3.
- Decision-budget framing — save for Post 4.
- OAuth scopes as a middle-layer example — too technical, only include if the post is running short.

## Editorial notes

- Replit's CEO response is quotable but don't pile on Replit — the lesson is architectural, not about any one vendor. They also shipped the fix publicly, which is a point in their favour worth a sentence.
- The capability envelope table is the single most reusable artefact in this post. Make it easy to screenshot.
- If you want a pull-quote for the Substack preview: *"Assumed authority scales until it fails catastrophically. Declared authority fails small."*
