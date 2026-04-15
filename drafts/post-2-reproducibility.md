# Post 2 — If you can't replay it, you can't defend it

**Status:** skeleton — fill with prose
**Target length:** 1500–2000 words
**Publishing slot:** week 3
**Author tag:** `me`
**Tags:** `ai-delegation`, `reproducibility`, `determinism`, `audit`
**Hero visual:** commissioned — two plates of food. Left: labelled *deterministic (replayable)*. Right: labelled *non-deterministic (charming, undefendable)*
**Supporting visual:** pull-quote box with the BCCRT tribunal's "remarkable submission" line

---

## 1. Hook — *Moffatt v. Air Canada* (~350 words)

Open with the story as human narrative first, then the legal move.

**The human story:**
- November 11, 2022. Jake Moffatt's grandmother dies. He needs a last-minute flight to Toronto.
- On Air Canada's website, a chatbot tells him there's a retroactive bereavement discount — book first, claim afterwards.
- The chatbot is wrong. The real policy required pre-booking application.
- Air Canada refuses the refund. Moffatt files with the British Columbia Civil Resolution Tribunal.

**The legal move — this is the quotable moment:**
- Air Canada's defence: the chatbot was *"a separate legal entity that is responsible for its own actions."*
- The tribunal's response (paraphrase, then the quote): the tribunal called this *"a remarkable submission"* and held that as part of Air Canada's website, the airline was responsible for everything the chatbot told users.
- Ruling: *Moffatt v. Air Canada*, 2024 BCCRT 149. Damages: $812 CAD.

**The punchline:** not the dollar figure — the precedent. *You cannot launder accountability through AI.* And, importantly for this post: the reason you can't is that Air Canada couldn't produce a defensible record of what its chatbot had told users or why.

Sources to link:
- [ABA — BC Tribunal confirms companies liable for AI chatbots](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)
- [CBC — Air Canada liable for chatbot's bad advice](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416)
- [CBS News — Air Canada chatbot costs airline discount](https://www.cbsnews.com/news/aircanada-chatbot-discount-customer/)

---

## 2. The recipe-vs-improvisation frame (~200 words)

Universalise:

- You can trust a recipe because it doesn't depend on the chef's mood. You can *love* improvisation but you can't certify it.
- If an AI gives you different answers on identical inputs, you cannot audit it. If you cannot audit it, you cannot trust it. If you cannot trust it, you certainly cannot defend it when someone sues.
- The framing flip: **reproducibility isn't an optimisation — it's the precondition of every other property we want from AI. Verification. Caching. Training data. Legal defensibility. All downstream of being able to replay the same thing twice.**

---

## 3. *Mata v. Avianca* — same bug, different profession (~250 words)

Second incident, same diagnosis:

- Lawyer Steven Schwartz prepares a brief in a personal injury case against Avianca Airlines. Asks ChatGPT for supporting case law.
- ChatGPT invents six cases — fictional judges ("Varghese", "Shaboon", "Petersen"), fabricated citations, invented quotations.
- Schwartz files the brief. Opposing counsel can't find any of the cases. The judge notices.
- Judge Castel sanctions the lawyers, $5,000 fine. Schwartz tells the court: *"I was operating under the false perception that ChatGPT could not possibly be fabricating cases."*

The deeper failure: **ChatGPT gave different, equally plausible answers each time it was asked.** None corresponded to reality. Non-determinism plus no verification path equals professional sanction.

Sources:
- [CNN — Lawyer apologizes for fake ChatGPT citations](https://www.cnn.com/2023/05/27/business/chat-gpt-avianca-mata-lawyers)
- [Wikipedia — Mata v. Avianca](https://en.wikipedia.org/wiki/Mata_v._Avianca,_Inc.)
- [AI Incident Database #541](https://incidentdatabase.ai/cite/541/)

Takeaway line: *most US courts now require AI-use disclosure in filings. They had to, because non-reproducible AI advice is indistinguishable from a confident lie — and the legal system cannot function on confident lies.*

---

## 4. The bit most people don't know: temperature=0 isn't determinism (~250 words)

Brief technical sidebar — important to debunk a common half-truth without losing the non-technical reader.

Points to cover (keep it plain):
- People often assume "turn the temperature down and the AI becomes deterministic." This is only partly true.
- Even at temperature=0, commercial LLMs can produce different outputs on identical inputs because of:
  - Non-deterministic GPU math (floating-point reduction order varies)
  - Silent model-version upgrades on the provider side
  - Context-window drift and prompt-cache behaviour
  - System-prompt changes you don't see
- **You're building on sand.** The vendor can change the model under you, and your "reproducibility" evaporates overnight.

This isn't obscure — it's the reason most enterprise AI deployments fail audits. You cannot pin what the vendor won't let you pin.

(Keep this section short. It's the proof that "we set temperature to zero" isn't the answer — and it sets up section 5.)

---

## 5. What reproducibility actually requires (~250 words)

Reader-portable checklist. Four layers, in ascending difficulty:

1. **Seed pinning** — fixed random seeds for anything stochastic. Necessary but nowhere near sufficient.
2. **Environment pinning** — fixed timezone, locale, filesystem sandbox. AILANG bakes these in with `AILANG_SEED`, `TZ`, `AILANG_FS_SANDBOX` ([m_r2_effect_system.md:158-207](/Users/mark/dev/sunholo/ailang/design_docs/implemented/v0_2_0/m_r2_effect_system.md)). One-line mention is enough.
3. **Model version pinning** — not "GPT-4", but the specific snapshot. Frontier vendors do expose dated snapshots; use them. If your contract doesn't let you pin, your contract doesn't give you reproducibility.
4. **Full input capture** — not just the user prompt. System prompt, tool definitions, retrieved context, conversation history. All of it, verbatim, logged.

**If all four are in place, you can replay a past decision. If any one is missing, you can't — and you should stop claiming you can.**

Practical framing for the non-technical reader: *ask your vendor which of the four they give you. If they can't answer, you don't have an AI advisor. You have a legal liability in chatbot form.*

---

## 6. Who this matters for right now (~200 words)

Quick tour of the sectors where this is immediate:

- **Legal work** — *Mata* is the tip. Courts now require AI-use disclosure; expect this to become AI-evidence-disclosure next.
- **Investment screening** — a non-reproducible model making allocation calls is a compliance nightmare waiting to happen.
- **Medical triage** — FDA SaMD (software as medical device) pathways already require reproducibility; LLMs don't meet the bar today, which is why hospital deployments are all scoped narrowly.
- **Hiring** — EEOC guidance leans on explainability, which requires reproducibility. Amazon's scrapped recruiter (from Post 3) is the warning shot.
- **Customer service** — Air Canada is the small claim. The class action version is coming.

One-line synthesis: *for any domain where your AI's output might be subpoenaed, reviewed, or audited — reproducibility is not optional; it is the ticket to play.*

---

## 7. Close (~150 words)

Return to the Air Canada tribunal line. The reason the airline lost wasn't that the chatbot was wrong — models are often wrong. It was that Air Canada couldn't produce a record, couldn't explain the reasoning, couldn't even commit to owning the output. **Non-reproducible advice is not a defence; it is an admission.**

Land the takeaway:
> *A non-reproducible advisor is not an advisor; it is a diviner. Pay your vendor for an advisor.*

Forward link:
> *Next week: why "just ask the AI to explain itself" is fantasy — and why the strongest evidence comes from Anthropic's own researchers.*

---

## Cutting-room floor — do NOT include

- Technical deep-dive on AILANG seed/sandbox mechanics — one-sentence mention only
- The whole Anthropic "chain of thought isn't faithful" story — that's Post 3
- The `requires`/`ensures` contract system — Post 5 territory
- EU AI Act Article 13 — keep for Post 3 or optional Post 6
- The "bullshitting" framing — Post 3

## Editorial notes

- The BCCRT tribunal's actual language is sharper than my paraphrase; if you have time, read the decision itself and pull the verbatim sentence.
- Temperature-0 section is where technical readers will judge you — get it right. If uncertain, lean on "this is what reproducibility *actually* requires" (section 5) and keep section 4 short.
- Pull-quote for Substack preview: *"A non-reproducible advisor is not an advisor. It is a diviner."*
