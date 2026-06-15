# The No‑Code Leader's Playbook
### Build a beautiful portfolio site with Claude Code + GitHub — even if you've never written a line of code

> 📖 **There's a visual, interactive version of this playbook** at **`/playbook/`**
> (`playbook/index.html` in this repo) — same content, laid out as a polished web page you can send
> to anyone. This Markdown file is the plain‑text companion. *The visual version was itself built
> with Claude + GitHub — it's a live demo of the thing it teaches.*

> **The ladder at a glance (climb one rung at a time — don't do it all at once):**
>
> | Level | Phase | You get |
> |---|---|---|
> | **0 · Crawl** | Accounts + first live page | A website you own, live today |
> | **1 · Crawl** | Claude Code + the core loop + versioning | You can change your site by talking |
> | **2 · Walk** | `CLAUDE.md` (memory) + context | Claude knows your voice & your truth |
> | **3 · Walk** | Content architecture + branches/PRs | A real, credible portfolio |
> | **4 · Run** | Skills + permissions + hooks | Claude works *your* way, every time |
> | **5 · Run** | Routines & loops (GitHub Actions) | A site that maintains itself |
>
> Most people live happily on Levels 0–2 for weeks before climbing higher. That's the point.

> **Who this is for.** A senior operator — 10–20 years of P&L, general management, marketing,
> and team leadership — who has *never coded*, doesn't "do systems thinking," and is a little
> suspicious that any of this is for them. It is. You will not be writing code. You will be
> **directing** an AI that writes the code, the same way you've spent a career directing teams,
> agencies, and vendors toward an outcome. Your edge — knowing what a great strategy, a real
> financial result, and a credible leadership story actually *look like* — is the part Claude
> can't do. This playbook hands you the rest.
>
> **What you'll end up with.** A live website at `https://<yourname>.github.io` that you own,
> can edit by *talking* to an AI, and that costs **$0 to host**. Along the way you'll learn the
> handful of AI‑builder skills everyone's hiring for: setting up Claude, writing a `CLAUDE.md`,
> prompting with good context, and running automated "loops."
>
> **Time:** ~1 focused hour a day. **Feeling fluent:** ~30 days. **First live page:** day one.

---

## Table of contents

1. [The mindset: you are the director, not the typist](#1-the-mindset)
2. [The mental model: how these four tools fit together](#2-the-mental-model)
3. [Phase 0 — Set up your accounts (30 min, one time)](#3-phase-0--accounts)
4. [Phase 1 — Get a live site on the internet today](#4-phase-1--live-today)
5. [Phase 2 — Install Claude Code and have your first conversation](#5-phase-2--first-conversation)
6. [Phase 3 — Write your `CLAUDE.md` (the brief that makes Claude *yours*)](#6-phase-3--claudemd)
7. [Phase 4 — Context & harness, explained without jargon](#7-phase-4--context-and-harness)
8. [Phase 5 — The core loop: Idea → Prompt → Review → Publish](#8-phase-5--the-core-loop)
9. [Phase 6 — Architect the content: turning 15 years into a site](#9-phase-6--content-architecture)
10. [Phase 7 — Work safely: branches, PRs, and "undo"](#10-phase-7--work-safely)
11. [Phase 8 — Loops: make the site maintain itself](#11-phase-8--loops)
12. [The 30‑day plan (one hour a day)](#12-the-30-day-plan)
13. [Prompt library (copy / paste)](#13-prompt-library)
14. [Troubleshooting & guardrails](#14-troubleshooting)
15. [Glossary for the non‑technical](#15-glossary)

---

<a name="1-the-mindset"></a>
## 1. The mindset: you are the director, not the typist

Everything that follows is easier if you hold one idea firmly:

> **You manage Claude the way you've managed your best agency or your sharpest analyst.**

You don't open the hood and rewire the engine. You give a crisp brief, you react to drafts, you
say "warmer," "shorter," "lead with the number," "that headline is generic — make it sound like a
P&L owner wrote it." Claude does the typing, the syntax, the file‑wrangling, the debugging. The
"technical heavy lifting" is genuinely handled for you.

What this means in practice:

- **You will never be asked to memorize code.** If you see code, you skim it the way you'd skim a
  contract — looking for the one clause that matters — and you ask Claude to explain anything you want.
- **Trial and error is the method, not a failure.** Builders ship something rough, look at it, and
  say "now do this." You already do this with decks and forecasts.
- **The skill you're building is *articulation*** — describing the outcome you want precisely
  enough that a very capable, very literal collaborator can hit it. That is a leadership skill, not
  a coding skill, and you already have 15 years of it.

Keep a running note (on your phone is fine) titled **"things I want to change."** Every time you
look at the site and something bugs you, jot it down. That note *is* your backlog. Feeding those
lines to Claude, one at a time, is the entire job.

---

<a name="2-the-mental-model"></a>
## 2. The mental model: how the four tools fit together

There are only four things in this world. Here's each one in a sentence, with the real‑world analogy.

| Thing | What it actually is | Business analogy |
|---|---|---|
| **GitHub** | A website that stores your files and remembers every version of them. | The shared drive + the filing cabinet that keeps every past draft of every document, forever. |
| **GitHub Pages** | A free feature of GitHub that turns your files into a live public website. | The printing press that publishes your filing cabinet to the world at a real URL. |
| **Claude Code** | An AI assistant that lives in your project, reads your files, and edits them when you ask. | The brilliant, tireless analyst/agency who actually does the building. |
| **`CLAUDE.md`** | A plain‑English brief you write once that Claude reads every time. | The onboarding doc / standing brief you give a new hire so you don't repeat yourself. |

The flow, end to end:

```
   You (idea, in plain English)
        │
        ▼
   Claude Code  ── reads ──►  CLAUDE.md (your standing brief)
        │                     + your files (the website)
        │                     + context you point it at (your CV, achievements, LinkedIn)
        ▼
   edits your HTML files
        │
        ▼
   GitHub  (saves the new version, keeps the old one)
        │
        ▼
   GitHub Pages  (re‑publishes the live site in ~1 minute)
        │
        ▼
   You refresh the browser, see it, say "now make it ..."
```

That loop — **idea → Claude edits → GitHub saves → Pages publishes → you look → repeat** — is the
whole craft. Everything in this playbook is just doing that loop better, safer, and eventually
*automatically*.

> **A note on "a website is just files."** This trips people up, so let's defuse it. A website is a
> folder of plain text files. The main one is called `index.html` — it's the home page. "HTML" is
> just the format that browsers read, the way `.docx` is the format Word reads. You will not write
> HTML. You'll say *"add a section about my Party City turnaround with three metric tiles,"* and
> Claude writes the HTML. You're the editor‑in‑chief; HTML is the typesetter's problem.

---

<a name="3-phase-0--accounts"></a>
## 3. Phase 0 — Set up your accounts (≈30 minutes, one time)

Do these in order. You'll need an email and a credit card on file for Claude (there's a paid plan;
more below).

**A. Create a GitHub account.**
1. Go to **github.com** → **Sign up**. Pick a username carefully — **it becomes part of your
   website address.** `vishwasbharadwaj` → your site will live at `vishwasbharadwaj.github.io`. Use
   your real name; this is a public professional asset.
2. Verify your email. Choose the **Free** plan. That's all you need; Pages hosting is free.

**B. Get Claude + Claude Code.**
1. Go to **claude.ai**, create an account (use the same professional email).
2. Subscribe to a paid plan. For this work the **Pro** plan is the sensible starting point; if you
   find yourself building heavily every day, **Max** gives more headroom. (Claude Code needs a paid
   plan or API access — the free tier won't run it.)
3. **Two ways to run Claude Code — pick based on comfort:**
   - **Claude Code on the web (easiest, nothing to install).** Go to **claude.com/code**, connect
     your GitHub account, and you can point Claude at your repository and work entirely from the
     browser (and even your phone). For a non‑technical user, **start here.** It handles all the
     plumbing.
   - **Claude Code in the terminal (the "real" desktop tool).** This is the classic experience and
     worth graduating to. Installation is one command; see Phase 2. Don't let the word "terminal"
     scare you — you'll type whole English sentences into it, not code.

**C. (Optional but recommended) Install a code editor to *look* at your files: VS Code.**
Download from **code.visualstudio.com**. You won't edit in it much — you'll just open your project
folder to *see* what Claude changed. Think of it as the "track changes" view.

> **Budget reality check.** GitHub Pages: free. Claude Pro: a monthly subscription (think "one nice
> dinner"). A custom domain like `vishwasbharadwaj.com` if you want one later: ~$12/year. That's the
> whole cost. No servers, no hosting bills, no developer retainer.

---

<a name="4-phase-1--live-today"></a>
## 4. Phase 1 — Get a live site on the internet *today* (before you learn anything else)

The single biggest motivation booster is seeing **your own URL load in a browser** on day one. We'll
do that with an almost‑empty page, then make it good later. Momentum first.

**The trick that makes Pages free and automatic:** name your repository exactly
`<your-username>.github.io`. GitHub treats that specific name as "publish this to the web."

### Option A — let Claude Code on the web do it (recommended for non‑technical start)

In Claude Code on the web, after connecting GitHub, paste this:

> "Create a new public GitHub repository named **`vishwasbharadwaj.github.io`** (use my GitHub
> username). Add a single file `index.html` that says, in large friendly text, *'Vishwas Bharadwaj —
> site coming soon'* with my name as the page title. Add an empty file named `.nojekyll`. Commit and
> push to the `main` branch, then tell me the exact URL where this will be live and roughly how long
> until it appears."

Claude will create the repo, the files, and explain the URL. Then go to your repo on github.com →
**Settings → Pages** and confirm the source is set to **Deploy from branch → `main`**. (Claude can
walk you through this screen if you ask.)

### Option B — do it by hand on github.com (no tools at all)

1. github.com → **New repository** → name it **`vishwasbharadwaj.github.io`** → **Public** → check
   "Add a README" → **Create**.
2. **Add file → Create new file** → name it `index.html` → paste:
   ```html
   <!doctype html>
   <html>
     <head><title>Vishwas Bharadwaj</title></head>
     <body style="font-family: system-ui; text-align:center; margin-top:20vh">
       <h1>Vishwas Bharadwaj</h1>
       <p>Site coming soon.</p>
     </body>
   </html>
   ```
   → **Commit changes**.
3. **Add file → Create new file** → name it `.nojekyll` → leave it empty → **Commit**.
   (`.nojekyll` just tells GitHub "serve my files exactly as they are.")
4. **Settings → Pages** → Source: **Deploy from branch**, Branch: **main /(root)** → **Save**.
5. Wait ~1 minute, then open **`https://vishwasbharadwaj.github.io`**.

🎉 **You now have a live website you own.** It's plain. That's fine — it's *yours*, it's *real*, and
from here on you only ever *improve* it. Take a screenshot; you'll want the "before."

---

<a name="5-phase-2--first-conversation"></a>
## 5. Phase 2 — Install Claude Code and have your first conversation

If you started on the web, you can keep using it indefinitely. But the terminal version is the tool
most "AI builders" mean when they say Claude Code, and it's worth ten minutes to set up.

**Install (Mac or Windows), one command:**
- Open the **Terminal** app (Mac: ⌘+Space, type "Terminal"; Windows: install "Windows Terminal" from
  the Microsoft Store). Paste this and press Enter:
  ```
  npm install -g @anthropic-ai/claude-code
  ```
  - If it complains that `npm` isn't found, that just means Node.js isn't installed yet. Install it
    from **nodejs.org** (the "LTS" button), reopen Terminal, and run the line again. *(If any of this
    snags, paste the exact error into Claude on claude.ai and ask "how do I fix this on my Mac/PC?"
    — it'll talk you through it.)*

**Get your project onto your computer ("clone" it):**
```
cd ~/Documents
git clone https://github.com/vishwasbharadwaj/vishwasbharadwaj.github.io.git
cd vishwasbharadwaj.github.io
```
- `cd` = "change directory" = "open this folder." `clone` = "download a copy of my repo that stays
  linked to GitHub." You now have your website in `~/Documents/vishwasbharadwaj.github.io`.

**Start Claude inside the project:**
```
claude
```
The first time, it'll ask you to log in (a browser window opens — sign in with your Claude account).
Now you're talking to an assistant that can *see and edit every file in this folder.*

**Your first real conversation — try exactly this:**
> "You're helping me, a non‑technical eCommerce/DTC executive, build my portfolio site. First, just
> *describe* what's currently in this project in plain English — what each file is and what the home
> page looks like. Don't change anything yet."

Read its answer. You just had Claude explain your own codebase to you. That move — **"explain this to
me before we change it"** — is one you'll use constantly and never outgrow.

> **The two habits that make you good at this fast:**
> 1. **Ask before you act:** "Before you change anything, tell me your plan in 3 bullets." You
>    approve the plan, *then* let it build. (In the terminal, "Plan mode" — toggled with **Shift+Tab**
>    — does exactly this: Claude proposes, you approve, then it executes.)
> 2. **One change at a time.** Don't say "redesign my whole site." Say "make the headline bigger and
>    change it to X." Small, reviewable steps. You can always go faster later.

---

<a name="6-phase-3--claudemd"></a>
## 6. Phase 3 — Write your `CLAUDE.md` (the brief that makes Claude *yours*)

This is the highest‑leverage thing in the entire playbook, so slow down here.

**What it is:** `CLAUDE.md` is a plain‑text file you put in your project. **Every time** Claude
starts working in this folder, it reads this file first — automatically, without you mentioning it.
It's the standing brief, the onboarding doc, the "house style guide" all in one. Write it once;
benefit on every prompt thereafter.

**Why it matters for you specifically:** without it, you'll re‑explain "I'm non‑technical, keep the
code simple, write in a confident executive voice, never invent numbers" on every single request.
With it, Claude already knows.

**How to create it:** the easiest way is to ask Claude to. In your session:
> "Create a `CLAUDE.md` file in the root of this project. I'll give you the contents — write exactly
> what I paste, then show it back to me."

Then paste a version of the template below (edit the bracketed parts). This is a *starting* template
tuned for a non‑technical commercial leader — adjust freely.

````markdown
# CLAUDE.md — Working brief for this portfolio

## Who I am
I'm Vishwas Bharadwaj, a senior eCommerce / DTC / marketplace executive with 15+ years
owning P&L (up to ~$350M), general management, marketing, and team leadership. I am
**non-technical** — I have never coded. Explain things to me in plain business English and
do the technical work for me.

## What this project is
My personal portfolio website, hosted free on GitHub Pages at
https://vishwasbharadwaj.github.io. It is a set of plain HTML files. The home page is
`index.html`. I want it to look modern, credible, and senior — think "operator who ships,"
not "flashy agency."

## How to work with me
- Before making any non-trivial change, give me a short plan (max 3 bullets) and wait for
  my go-ahead.
- Make ONE change at a time and tell me what to look at to check it.
- After each change, give me the exact git commands (or do it for me) to save and publish,
  and remind me the live site updates ~1 minute later.
- When you must show code, keep it minimal and add a one-line plain-English caption above it.
- If I ask for something that would break the site or is a bad idea, say so and propose a
  better path. I'd rather be told "no, because…" than get a broken page.

## Voice & content rules (important)
- Write in a confident, senior, results-first voice. Lead with outcomes and numbers.
- **Never invent or inflate metrics.** Only use numbers I explicitly give you. If a number
  is missing, leave a clearly marked placeholder like `[ADD METRIC]` — do not guess.
- Prefer specifics ("grew DTC revenue 38% to $X over 2 years") over adjectives
  ("results-oriented leader").
- Keep it skimmable: short sections, strong headlines, metric tiles, scannable bullets.
- No buzzword salad. A CMO and a CFO should both find it credible.

## Technical guardrails
- Keep the stack simple: hand-written HTML/CSS, no frameworks, no build step, no
  dependencies I'd have to maintain. It must keep working untouched for years.
- Keep everything in this one repo and self-contained (no external services that could
  break). Use relative links between pages.
- Don't add analytics, trackers, or third-party scripts without asking me first.
- The file `.nojekyll` must stay. Don't delete files without confirming with me.

## My links (use these, don't guess)
- LinkedIn: [PASTE YOUR LINKEDIN URL]
- Email: [your email]
- GitHub: https://github.com/vishwasbharadwaj
````

**The point of every line above** is to remove a decision Claude would otherwise make *for* you,
possibly wrongly. The "never invent metrics" rule alone will save you from the single most dangerous
failure mode — an AI confidently writing "$500M" when the real number was $350M. You are the source
of truth for your own career; the `CLAUDE.md` makes Claude respect that.

> **Living document.** Every time Claude does something you have to correct twice, add a line to
> `CLAUDE.md` so it never happens a third time. ("Always spell it 'marketplace,' one word." "Use
> en‑dashes in date ranges.") Over a few weeks this file becomes *your* operating standard, and new
> work just comes out right.

---

<a name="7-phase-4--context-and-harness"></a>
## 7. Phase 4 — Context & "harness," explained without jargon

Two words you asked about. Here they are stripped of mystique.

### Context = "what Claude can see right now"
Claude is brilliant but it only knows what's **in front of it**: your `CLAUDE.md`, the files in the
project, and whatever you paste or point it at in the conversation. It does **not** automatically
know your career unless you give it the material. **Good output is mostly a function of good
context.** Garbage in, garbage out; gold in, gold out.

So before you ask Claude to write your "Experience" section, *give it the raw material.* Concretely,
create a folder for source material and drop your real career documents in it:

```
your-project/
  index.html
  CLAUDE.md
  content/              ← your raw material (Claude reads it; you decide what's public)
    linkedin.txt        ← paste your full LinkedIn profile text here
    achievements.md     ← your real numbers: revenues, growth %, P&L size, team sizes
    bio.md              ← a few paragraphs in your own words
    roles/
      party-city.md     ← one file per role with the story + the metrics
      dormify.md
      newell.md
```

Then your prompt becomes: *"Using `content/roles/party-city.md`, write a portfolio case‑study
section. Lead with the financial outcome. Use only the numbers in that file."* Now Claude is working
from **your truth**, not its imagination. This is the entire secret to output that sounds like *you*.

> **Tip:** dumping your LinkedIn export and a plain "here are my real numbers" file into `content/`
> on day one is the best 20 minutes you'll spend. Everything downstream gets better.

### Harness = "the setup that lets Claude act, not just chat"
When you use ChatGPT in a browser, it can only *talk* — it hands you text and you go paste it
somewhere. The **harness** is everything that upgrades Claude from "talks" to "does": the fact that
it's running *inside your project*, can *read and write your files*, can *run commands*, can *save to
GitHub*, can *publish*. Claude Code **is** a harness. You don't build it; you just benefit from it.

The practical takeaway: because Claude is *in the harness*, you can say *"add the section and publish
it,"* and it actually edits the file and pushes to GitHub — no copy‑pasting. As you grow, the harness
is also what lets you wire up **loops** (Phase 8) — Claude acting on a schedule, unattended.

The mental upgrade is: **stop thinking "AI that gives me answers," start thinking "AI that gets work
done in my project."** Context is *what it knows*; the harness is *what it can do*. You supply the
first; Claude Code supplies the second.

---

<a name="8-phase-5--the-core-loop"></a>
## 8. Phase 5 — The core loop: Idea → Prompt → Review → Publish

This is the daily rhythm. Internalize it and you can build anything, one step at a time.

### Step 1 — Idea (you, in business terms)
From your "things I want to change" note. e.g. *"My home page should open with a one‑line value
proposition and three headline metrics from my career."*

### Step 2 — Prompt (you, to Claude)
Translate the idea into a brief. A good prompt usually has four parts — **Context, Task, Constraints,
Output**:
> **[Context]** "On the home page (`index.html`), below the name… **[Task]** add a hero section with
> a one‑sentence value proposition and a row of three metric tiles. **[Constraints]** Use only these
> numbers: managed $350M P&L; grew DTC +38% over 2 years; led teams up to 40. Match the existing
> style; keep it senior and clean. **[Output]** Show me the plan first, then make the change and tell
> me what to refresh."

You don't need to be this formal every time — but when output disappoints, it's almost always because
one of those four was missing.

### Step 3 — Review (you, like reviewing a deck)
Claude makes the change. **Look at the live site** (refresh your browser) or ask Claude for a
screenshot/preview. React the way you'd react to an analyst's draft:
- "The metric tiles are great. The headline is generic — rewrite it to sound like a P&L owner."
- "Too much text. Cut it 40%."
- "I don't like the blue. Try a deep charcoal and a single warm accent."

Iterating 3–5 times on one section is **normal and correct**, not a sign you're doing it wrong.

### Step 4 — Publish (Claude, on your say‑so)
When you like it, publish. Either let Claude do it, or run the three‑command "save & ship":
```
git add -A
git commit -m "Add hero section with value prop and 3 metrics"
git push
```
In plain English: *add* = "stage my changes," *commit* = "save this version with a label," *push* =
"send it to GitHub." ~1 minute later the live site updates. (Claude will happily run these for you —
*"save and publish that for me"* — and write a sensible label.)

**That's the loop.** Pick the next line from your note and run it again. Twenty reps in, it's muscle
memory.

---

<a name="9-phase-6--content-architecture"></a>
## 9. Phase 6 — Architect the content: turning 15 years into a site

This is where *your* expertise dwarfs any developer's. A great portfolio for a commercial leader
isn't a résumé reprint — it's a **highlight reel of outcomes**, organized so a hiring CEO, a board, or
a recruiter "gets it" in 20 seconds and can go deeper if they want. Here's a proven structure; tell
Claude to build the home page around it.

### The recommended structure (a "hub" home page + deep‑dive pages)

This mirrors how strong operator portfolios are built (and how this very repo is built — a tidy home
page that opens "front doors" into deeper case studies):

1. **Hero** — Name, a one‑line positioning statement ("eCommerce & DTC P&L leader — I scale
   marketplace and direct businesses from $0→$300M+"), and 3 headline metrics. This is your billboard.
2. **The numbers strip** — 4–6 metric tiles that quantify your career at a glance: *P&L owned, revenue
   grown, markets/channels launched, teams led, years.* CFOs love this; recruiters screenshot it.
3. **Selected work / case studies** — 3–4 **front‑door cards**, each opening to a one‑page deep dive.
   For each, use a simple, repeatable template:
   - **Situation** (1–2 lines: what was broken or the opportunity)
   - **Strategy** (your commercial thesis — the part only you could have authored)
   - **Action** (what you and the team actually did)
   - **Result** (the numbers — revenue, margin, growth %, share, speed)
   - **Leadership** (team you built/led, how you operated)
   > Good candidates from your background: *the Party City marketplace turnaround, the Dormify DTC
   > build, a Newell channel expansion, a marketplace GMV‑tripling peak‑season play.*
4. **How I operate** — your leadership & operating philosophy. People, team‑building, decision‑making,
   how you run a P&L. This is the "would I want to work for/with this person" section.
5. **Capabilities** — a scannable grid: *DTC, Amazon/marketplaces, P&L ownership, demand generation,
   pricing & margin, omnichannel, team leadership, GTM strategy.* (Pull straight from your "Core
   Competencies.")
6. **About** — a short, human, first‑person bio. Warmth, not buzzwords.
7. **Contact** — LinkedIn, email, and a clear "let's talk" line.

### How to build it — the prompt
> "Using my files in `content/` (especially `linkedin.txt` and `achievements.md`), rebuild
> `index.html` as a modern single‑page portfolio with these sections in order: hero, metrics strip,
> selected work (3 front‑door cards), how I operate, capabilities grid, about, contact. Follow the
> structure and voice rules in `CLAUDE.md`. Use **only** the metrics in my files; mark anything
> missing as `[ADD METRIC]`. Show me the plan first. Make it look senior and clean — generous
> whitespace, strong type, one accent color."

Then iterate section by section. **Build the home page first; add the deep‑dive case‑study pages one
at a time** over the following days (one role per session is a perfect daily‑hour task).

> **On design:** you don't need to know design vocabulary. React like a buyer: "looks dated," "too
> busy," "I want it to feel like a premium consultancy," "show me three different color directions."
> Claude will translate taste into CSS. If you see a site you love, tell Claude *"make mine feel more
> like that"* and describe it.

---

<a name="10-phase-7--work-safely"></a>
## 10. Phase 7 — Work safely: branches, PRs, and the "undo" button you always have

You asked about eventually moving toward a more professional workflow. Here's the safety net — and the
reassurance that **you can never permanently break anything.**

**The superpower of this whole setup: every version is saved forever.** Because GitHub remembers every
`commit`, you can always go back. If a change makes the site worse, you say:
> "That made it worse — undo your last change and take us back to how it looked before."

Claude can revert it. You are working with an infinite undo. This alone should remove the fear.

**Branches (when you're ready, ~week 2–3).** A *branch* is a **private sandbox copy** of your site
where you can experiment without touching the live version. The live site keeps running off `main`;
you play on a branch; when you like it, you merge it in.
> "Create a branch called `redesign-hero` so we can try a bold new homepage without affecting my live
> site. We'll merge it only once I approve."

**Pull Requests (PRs).** A *PR* is a "please review and merge this batch of changes" proposal — a tidy
before/after summary of what changed. Even working solo, PRs are a great habit: they give you a clean
review screen and a record of *why* each change happened. Claude can open one:
> "Open a draft pull request for this branch summarizing what we changed and why."

You don't need branches and PRs on day one. Use the simple `add/commit/push` loop until it's
comfortable, then graduate. The mental model: **`main` is the published magazine; a branch is the
rough draft on your desk; a PR is handing the draft to the editor (you) before it goes to print.**

---

<a name="10b-level-4"></a>
## 10½. Level 4 — Teach Claude your standards (skills, permissions, hooks)

Everything so far works **without** this rung. Climb it only when you catch yourself *repeating the
same instructions* or wanting tighter guardrails. These are the tools that turn Claude into **your**
operating system — and they're exactly the kind of hands‑on AI fluency worth showing off. Three
ideas, easy → advanced. You won't configure any of them by hand; you'll **ask Claude to set them up**
and explain them in plain English.

**A. Skills — package work you repeat.** A *Skill* is a saved set of instructions Claude runs on
command — a repeatable routine you describe once (think saved playbook / macro). Instead of re‑typing
your whole "write a case study" brief each time:
> "Create a Skill called `case-study` that takes a role file from `content/roles/` and writes a
> one‑page case study using my Situation→Strategy→Action→Result→Leadership template and the voice
> rules in `CLAUDE.md`. Save it in `.claude/skills/` and explain how I invoke it."

Now each new role is a one‑liner: *"use the case‑study skill on `content/roles/dormify.md`."* (A
lighter cousin is a **custom slash command** — a shortcut for a prompt you reuse, saved in
`.claude/commands/`.)

**B. Permissions / policies — guardrails.** *Permissions* decide what Claude may do freely vs. what it
must **ask** about first. The sweet spot for a non‑technical owner: let it edit and preview freely,
but always ask before deleting files or publishing to the live site.
> "Set up my Claude permissions so you can read, edit, and preview files freely, but you must ASK me
> before deleting any file or pushing to the live site. Put it in `.claude/settings.json` and explain
> each rule in one line."

Good guardrails make you *faster*, not slower — once Claude can act freely on the safe stuff, you
stop approving every tiny step, while risky moves still pause for your sign‑off. Delegation with a
clear mandate, exactly like running a team.

**C. Hooks — things that fire automatically.** A *hook* is an action that runs **by itself** when
something happens — no asking. The difference between "Claude does it when I ask" and "it just
happens." Low‑stakes portfolio examples: show a checklist on session start; check for broken links
after every edit; before publishing, auto‑scan for any leftover `[ADD METRIC]` placeholder so you
never ship a gap.
> "Add a hook that, before any publish, scans my site for the text `[ADD METRIC]` and warns me if any
> remain. Put it in my Claude settings and explain in plain English what it does and how to turn it
> off."

> **Don't rush this rung.** Skills, permissions, and hooks are power tools — most valuable *after* the
> core loop is second nature. If a section here feels abstract, that's a sign to keep living on
> Levels 1–3 a bit longer, and come back when you think *"I keep doing this same thing."*

---

<a name="11-phase-8--loops"></a>
## 11. Phase 8 (Level 5) — Loops: make the site maintain itself

This is the "graduation" you're aiming for, and it's where the AI‑builder skillset gets genuinely
impressive. A **loop** is **work that runs on a schedule, automatically, without you starting it.**
Instead of "I prompt Claude → it acts once," it's "I set up a recurring job → it acts forever."

Two flavors, easy → advanced:

### a) The recurring prompt loop (easiest)
You can ask Claude to run a task on a repeating interval while you work — e.g. *"every 10 minutes,
re‑check the site for broken links and tell me."* Great for polishing sessions. In Claude Code this is
the **`/loop`** idea: a prompt that re‑runs itself on a timer. Low stakes, no setup.

### b) The scheduled automation (the real prize) — "your site updates itself in the cloud"
This is the pattern that powers the "live stats" you may have seen on operator portfolios — numbers
that refresh on their own with **no one touching a computer.** The recipe:
1. A small script computes something (e.g. "pull my latest metrics / refresh a 'currently building'
   stat / regenerate a section").
2. A **GitHub Action** — a free robot that lives in your repo — runs that script **on a schedule**
   (say, every day at 5pm) on GitHub's own machines.
3. It writes the result back into your page and publishes. You wake up to a freshened site.

You will **not** write this by hand. You'll say:
> "Set up a GitHub Action that runs every weekday at 9am, regenerates my 'metrics strip' from
> `content/achievements.md`, and publishes the update automatically. Explain in plain English what
> it'll do, what it costs (it's free, right?), and how I turn it off."

Claude writes the automation, you approve it, and now part of your site is **alive.** That's a genuine
"I built an autonomous AI workflow" story — exactly the kind of hands‑on AI credibility you're after,
and a great thing to *show* in the portfolio itself ("this site partially maintains itself; here's
how").

> **Where loops fit your timeline:** don't start here. Loops are a week‑3‑or‑4 reward once the core
> loop is second nature. But knowing they're the destination shapes how you build: keep your real
> numbers in clean files like `content/achievements.md`, and later a loop can read those files and
> keep the site current for you.

---

<a name="12-the-30-day-plan"></a>
## 12. The 30‑day plan (one focused hour a day)

A realistic ramp from "never set up Claude or touched HTML" to "fluent, with an automated, beautiful
site." One hour a day. Skip days as life demands — the order matters more than the calendar.

### Week 1 — Get live and get comfortable
- **Day 1:** Phase 0 + Phase 1. Accounts created; a plain site is **live at your URL.** (The win.)
- **Day 2:** Phase 2. Install Claude Code (or use the web version); have it *explain* your project.
- **Day 3:** Phase 3. Write your `CLAUDE.md` together. Paste your LinkedIn + real numbers into
  `content/`.
- **Day 4:** First real edit via the core loop — improve the headline and add your name/title nicely.
  Publish it. Feel the loop.
- **Day 5:** Add the **metrics strip** (3–6 real numbers). Iterate on look until it feels senior.
- **Days 6–7:** Rest, or play. Tell Claude "show me three different color/type directions for my
  site" and pick one.

### Week 2 — Build the substance
- **Day 8:** Build the full home‑page **skeleton** (all section headers in order, placeholder text).
- **Days 9–12:** One **case study per day.** Party City. Dormify. Newell. A marketplace win. Use the
  Situation/Strategy/Action/Result/Leadership template, real numbers only.
- **Day 13:** Write the **"How I operate"** leadership section — the part that's pure you.
- **Day 14:** Polish pass: capabilities grid, about, contact. Wire up LinkedIn + email.

### Week 3 — Make it sharp and safe
- **Days 15–17:** Learn **branches + PRs** (Phase 7). Do one redesign experiment on a branch, review
  it as a PR, merge it. Now you're working like a pro.
- **Days 18–19:** Design refinement — typography, spacing, mobile (ask "make sure it looks great on a
  phone"), a favicon, your photo.
- **Days 20–21:** Get **feedback.** Send the live URL to 3 trusted peers; turn their notes into a
  backlog; run the loop on each.

### Week 4 — Automate and own it
- **Days 22–24:** Set up your first **loop / GitHub Action** (Phase 8) — e.g. an auto‑refreshing stat
  or a weekly "currently focused on" line.
- **Day 25:** (Optional) Buy a custom domain (`vishwasbharadwaj.com`) and have Claude walk you through
  pointing it at your GitHub Pages site.
- **Days 26–28:** Write a short "how I built this with AI" page — a credibility asset in its own right,
  and proof of your AI fluency.
- **Days 29–30:** Final polish, proofread (ask Claude to "review the whole site for typos, weak
  phrasing, and any unsupported claim"), and **share it** — LinkedIn post, email signature, the works.

By day 30 you'll have a beautiful live portfolio *and* will have genuinely learned: GitHub, Claude
Code, `CLAUDE.md`, context/harness, prompting, branches/PRs, and loops. That's the real prize — the
bridge from deep commercial expertise to hands‑on AI capability.

---

<a name="13-prompt-library"></a>
## 13. Prompt library (copy / paste, then tweak)

Keep these handy. Replace the bracketed parts.

**Understand before changing**
> "Before we change anything, explain in plain English what `[index.html]` currently does and what the
> page looks like. Then suggest the 3 highest‑impact improvements for a senior commercial leader's
> portfolio."

**Make one safe change**
> "Make this one change: `[describe it]`. Show me your plan first (max 3 bullets). After I approve,
> make only that change, then tell me exactly what to refresh to see it, and offer to publish it."

**Write a case study from your real material**
> "Using `content/roles/[party-city.md]`, write a one‑page case study with the headings Situation,
> Strategy, Action, Result, Leadership. Lead with the financial result. Use ONLY numbers in that file;
> mark anything missing `[ADD METRIC]`. Match my site's style and the voice rules in `CLAUDE.md`."

**Improve the writing (your voice)**
> "Rewrite this section to sound like a confident P&L owner, not a résumé. Cut adjectives, lead with
> outcomes and numbers, keep it ~30% shorter. Don't invent anything."

**Design direction without design words**
> "Show me three distinct visual directions for the home page — describe each in a sentence and apply
> them one at a time so I can compare. I want it to feel `[premium / modern / understated / bold]`."

**Make it work on phones**
> "Check the whole site on a phone‑sized screen and fix anything cramped, overflowing, or hard to tap.
> Tell me what you changed."

**Undo / safety**
> "That made it worse. Revert your last change and take the site back to exactly how it was before, and
> confirm when done."

**Publish**
> "Save and publish everything we just did, with a clear commit message, and remind me when the live
> site will reflect it."

**Set up a loop**
> "Set up a free GitHub Action that runs `[every weekday at 9am]` to `[refresh my metrics strip from
> content/achievements.md]` and publish automatically. Explain what it does, confirm it's free, and
> show me how to pause it."

**End‑of‑project review**
> "Review the entire site as if you were a skeptical recruiter and a CFO. Flag weak headlines, vague
> claims, typos, anything that reads junior, and any number that isn't backed by my `content/` files."

---

<a name="14-troubleshooting"></a>
## 14. Troubleshooting & guardrails

**"My site didn't update."** Pages takes ~1 minute, sometimes a few. Hard‑refresh your browser
(Cmd/Ctrl+Shift+R). Confirm Claude actually ran `push` ("did you push that to GitHub?"). Check
**Settings → Pages** still points at `main`.

**"Something looks broken."** Don't panic — nothing is lost. Say *"the page looks broken, please
diagnose and fix it, and if needed revert to the last good version."* The full history is your safety
net.

**"Claude did something I didn't want."** Tell it plainly. Then add a rule to `CLAUDE.md` so it doesn't
recur. Correcting Claude is *expected*; it's how the brief gets sharper.

**"I don't understand what it's showing me."** Always allowed: *"Explain that to me like I've never
seen code — what is this and why does it matter?"* Never accept output you don't understand.

**The cardinal rule: protect your truth.** AI can sound confident while being wrong, *especially with
numbers.* You are the only authority on your own career. Keep real figures in `content/achievements.md`,
make "never invent metrics" a `CLAUDE.md` rule, and personally verify every number, date, and company
name on the live site before you share it.

**Privacy.** Your repo is public — anything you put in it (including files in `content/`) can be seen if
someone digs. Don't commit anything you wouldn't put on LinkedIn (private salary data, confidential
employer numbers, personal contact details you want kept off the web). If in doubt, ask Claude *"is
this safe to make public?"* before publishing.

---

<a name="15-glossary"></a>
## 15. Glossary for the non‑technical

- **Repository (repo):** the project folder that holds your website's files, stored on GitHub.
- **GitHub Pages:** the free feature that publishes your repo as a live website.
- **HTML:** the file format browsers read to display a page. You won't write it; Claude does.
- **`index.html`:** the home page of your site, by convention.
- **`.nojekyll`:** an empty file that tells GitHub "publish my files exactly as they are." Leave it.
- **`CLAUDE.md`:** your standing brief that Claude reads automatically every session.
- **Claude Code:** the AI assistant that reads and edits your project files and publishes for you.
- **Context:** everything Claude can see right now (your files + what you paste). Good context → good
  output.
- **Harness:** the setup that lets Claude *act* in your project (edit files, run commands, publish),
  not just chat. Claude Code is the harness.
- **Commit:** a saved snapshot of your files with a label, kept forever (your undo points).
- **Push:** sending your saved snapshots up to GitHub (which then publishes them).
- **Branch:** a private sandbox copy of your site to experiment in without touching the live version.
- **Pull Request (PR):** a reviewable proposal to merge a branch's changes into your live site.
- **GitHub Action:** a free robot in your repo that runs tasks on a schedule (the engine of "loops").
- **Loop:** work that runs automatically and repeatedly without you starting it.
- **Custom domain:** your own web address (e.g. `vishwasbharadwaj.com`) pointed at your free site.

---

### A final word for the skeptic

You spent 15 years learning to read a P&L, build a team, place a marketing bet, and own the outcome.
None of that is being replaced here — it's being **showcased**, and along the way you'll pick up the
one new literacy that pairs beautifully with it: directing AI to do real work. You don't need to
become technical. You need to stay exactly who you are — a sharp operator with taste and judgment —
and point that at a tool that handles the rest. Open the terminal, type `claude`, and describe what
you want. The first hour is the hardest. After that, it's just the loop.
