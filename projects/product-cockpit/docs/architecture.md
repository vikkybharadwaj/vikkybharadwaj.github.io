# Architecture deep-dive

> Companion to the [overview](../index.html). For the reader who wants to know *why* each layer exists and how they fit together. All examples use a fabricated stand-in domain (a consumer **habit-building app**); the real domain is under NDA.

The whole architecture rests on one principle:

> **Separate what observes, what judges, and what executes — and never let the system's description drift from its reality.**

Everything below is an expansion of that sentence.

---

## The three-verb model

Most "AI in our workflow" setups collapse automation, judgement, and procedure into one undifferentiated pile of prompts. Keeping them distinct is what makes the system legible and maintainable.

### Hooks — *observe*

Deterministic shell scripts the harness fires automatically at points in the session lifecycle (start, end, prompt-submit). Their defining constraint: **they surface information; they never decide.**

- Pull the latest reference material so context is never stale.
- Detect structural drift (did the folder map change?) and warn.
- Load cross-session memory so the agent starts informed.

Why shell, not the agent? Because these jobs must happen *every* time, identically, with zero judgement. Determinism belongs in scripts. The moment a task needs judgement, it stops being a hook.

### Policies — *judge*

Plain-language markdown rules, each with a **trigger** and a **procedure**. Crucially, they're loaded *only when their trigger fires* — not dumped into context on every session. This keeps the working context lean while still applying consistent judgement at exactly the moments it's needed.

Example trigger/procedure (generalized):

> **When:** any change under `roadmap/` or `capabilities/`.
> **Do:** walk six alignment signals — pillar, core job, persona, evidence, trade-off, constraints. If any fails, push back before merge.

A policy is how you encode "the way we judge this kind of situation" *once*, so the hundredth decision gets the same rigor as the first.

### Skills — *execute*

Packaged, repeatable, multi-step workflows invoked on demand. The input may be messy; the output is always the same disciplined shape.

- `/interview-to-brief` — raw research → structured problem brief (cited).
- `/feature-critique` — a feature description → a structural critique.
- `/strategy-sync-audit` — flag where the roadmap has drifted from strategy.

Skills compound: every use adds to a shared pattern library instead of being re-improvised.

### The distinction, in one table

| | Hooks | Policies | Skills |
|---|---|---|---|
| Form | shell script | markdown rule | packaged workflow |
| Runs | automatically | when triggered | on demand |
| Job | observe & surface | judge | execute |
| Decides? | never | guides | carries out |

---

## The supporting layers

### Anchors

Two documents — the **target user** and the **core job** — that sit above everything. Every brief, every roadmap change, every feature idea is checked against them. They're the answer to "is this drift?" Without anchors, a backlog slowly fills with things that serve *someone*, just not the someone you're building for.

### Compounding memory

Four structures that make sure nothing learned is lost:

- **Learnings log** — non-obvious operational insights, appended after meaningful work.
- **Backlog with rationale** — deferred decisions *and why*, so "we'll do it later" doesn't become "we forgot."
- **Episode index** — a rolling summary of the last ~20 sessions, loaded at start.
- **Feedback loop** — a channel for improving the system itself, captured as structured entries.

This is the difference between memory and a filing cabinet: the memory is *re-loaded into context automatically*, so each session stands on the last.

### Governance — the anti-drift loop

The layer that makes the system durable. The rule: **any new primitive must update every registry that names it — including the visual self-portrait — or the change fails its own audit.**

Concretely, adding a skill forces:

1. The skill itself lands in its folder.
2. A policy fires: "register this everywhere."
3. The index, the capabilities map, and the self-portrait diagram all update.
4. An audit checks the diagram against reality. Mismatch → blocked.

The payoff: six months later, the map is still the territory. A newcomer can trust the system's description of itself, because the system *can't* let that description go stale.

Governance also includes **ownership** (who can merge what, where) and a **maintenance cadence** (a recurring pass to prune the learnings log, retire orphaned folders, refresh stale specs). Unglamorous, and exactly the kind of rigor that separates a system that lasts from a clever one-off.

---

## Why an AI agent changes the calculus

None of these primitives are novel on their own — teams have had scripts, checklists, and templates forever. What changes when an AI coding agent reads the same context:

- **The checklist gets *applied*, not just *available*.** A policy isn't a wiki page someone might remember to consult; it's loaded and acted on the moment its trigger fires.
- **The reconstruction tax can actually hit zero.** The agent assembles the relevant evidence in the first seconds of a session, because it's been loaded by hooks and structured for retrieval.
- **The division of labour becomes a design surface.** Deciding what the machine should *observe* vs. *judge* vs. *execute* is itself the core skill — and it's the thing this whole system is a demonstration of.

---

*Back to the [overview](../index.html) · or see the [artifacts](../appendix.html).*
