# Skills For Better Accountants

Agent skills for closing real books, not vibe bookkeeping.

Closing books with an agent is hard to trust. It will add a column in prose and get it wrong, call an entry approved because a spreadsheet said so, and spread revenue the way the invoices were written. Generic prompts don't fix that, and neither does a tool that hides the work.

These skills are small, readable, and composable. Each one is a procedure a careful preparer already follows, written down so the agent follows it too, with the arithmetic done by code instead of by the model. They're built on how a close is actually run and reviewed. Read them. Adapt them to your firm. Enjoy.

To keep up with changes to these skills, and new ones as they ship, follow along at [better-accountant.com](https://better-accountant.com).

## Installation (30-second setup)

### 1. Get the skills

<details>
<summary><strong>Claude Code</strong></summary>

```
/plugin marketplace add hazlijohar95/skills
/plugin install better-accountant-skills@better-accountant
```

The whole set installs as one plugin. The skills share a close kit and two reviewer agents, so they aren't installed one at a time.

</details>

<details>
<summary><strong>Claude and Cowork</strong></summary>

1. Download `better-accountant-skills.zip` from the latest release.
2. Open **Customize** → **Plugins** → **Add** → **Upload plugin** (in Cowork, Customize is in the left sidebar).
3. Select the zip and confirm. The trust warning is expected for any uploaded plugin; these skills read and write only files in your workspace.

Run full closes in **Cowork**, or anywhere with a file workspace, because a close's state lives in its files. Quick questions work in any chat.

</details>

### 2. Run `/setup-client` for each client

Once per client. It will:

- Read what already exists (CRM notes, call notes, prior workpapers) before asking you anything
- Ask for what's missing: basis, materiality, risk areas, recurring schedules
- Save a profile every close for that client reads

It's optional. A close runs without a profile, on stated defaults; it's just sharper with one.

### 3. Run `/close Acme Co 2026-07`

The period can be a month, a quarter (`2026-Q2`), or a year (`FY2025`). Or start smaller: drop a trial balance into the chat and ask "are these books ready to close?"

## Why These Skills Exist

I built these skills to fix the ways an agent fails at the work accountants actually sign.

### #1: The Numbers Are Made Up

**The Problem**: A model does arithmetic by predicting text. It adds a column in prose, gets it slightly wrong, and writes the result into a memo with full confidence. When data is missing, it fills the gap with a plausible estimate.

**The Fix** is to take arithmetic away from the model. The [close kit](#the-close-kit) runs every mechanical check (the TB balances, the GL ties to the TB, the entries balance, the revenue schedule) as code, and its output goes into the workpaper as the evidence. A gap in the data becomes an exception on the register, never an estimate.

### #2: Nobody Actually Approved It

**The Problem**: "Approved" in a spreadsheet, or in last week's conversation, is a claim. An agent that trusts it ships entries nobody signed off.

**The Fix**: an approval counts only when it is posted in the books or recorded in the close log, naming who gave it. `closekit je --log` refuses an import CSV holding any entry without one. No entry is marked approved, and no close is called complete, without your explicit confirmation.

### #3: The Preparer Grades Its Own Work

**The Problem**: A reviewer who has read the preparer's summary checks the story, not the books. An agent reviewing its own close is the extreme case.

**The Fix**: [`/review`](./skills/financial-close/review/SKILL.md) runs in a separate `close-reviewer` agent that sees only the close folder and reruns the kit's checks itself. A revenue judgment that is material or contested goes to a `revenue-challenger` agent whose only job is to argue the other side.

### #4: Revenue By Template

**The Problem**: Most revenue schedules follow the invoices. ASC 606 follows control of what was promised, and the facts that change the answer (a side letter, a termination right, a discounted option, a second contract signed the same week) sit in the documents, not the billing system.

**The Fix**: [`/revenue-recognition`](./skills/technical-accounting/revenue-recognition/SKILL.md) reads the contract documents first and works five questions from first principles. Each conclusion names its deciding fact and the treatment it rejected, in a position memo. The kit does the allocation and schedule arithmetic, and codification references come only from a verified table.

### #5: Fifty Interruptions

**The Problem**: An agent that asks every question the moment it thinks of it turns a close into a chat, and the question that matters gets lost among the ones that don't.

**The Fix**: questions are batched at phase boundaries and put as multiple choice, with a recommended answer and the figure at stake. Only an entry approval or a true blocker interrupts a phase, and anything above materiality is asked on its own.

### Summary

Accounting fundamentals matter more with an agent, not less: evidence over assertion, approval that is recorded, review that is independent. These skills are my best effort at writing those fundamentals down as repeatable procedure, so the close you sign is one you can defend.

## Reference

These split on one axis: who can invoke them. **User-invoked** skills are reachable only when you type them (e.g. `/close`); starting a close is your decision. **Model-invoked** skills can be typed by you, or reached for automatically by the agent when the task fits; each also works on its own.

### Financial Close

Close one client's books for one period, from trial balance and GL exports out of any accounting system.

**User-invoked**

- **[close](./skills/financial-close/close/SKILL.md)**: Run a full close for one client and one period, from readiness check to delivered close package.

**Model-invoked**

- **[setup-client](./skills/financial-close/setup-client/SKILL.md)**: Build or update a client's profile (basis, materiality, risk areas, recurring schedules) from their existing sources plus a short interview.
- **[intake](./skills/financial-close/intake/SKILL.md)**: Close readiness check: what is present, what is missing, and what each gap blocks.
- **[prep](./skills/financial-close/prep/SKILL.md)**: The prep phase as one call: `reconcile`, then `categorize`, with one batch of questions.
- **[reconcile](./skills/financial-close/reconcile/SKILL.md)**: A reconciliation proof per account, ending at zero or at named reconciling items.
- **[categorize](./skills/financial-close/categorize/SKILL.md)**: Sweep the period's transactions for miscoding, unmatched transfers, and duplicates.
- **[adjust](./skills/financial-close/adjust/SKILL.md)**: The JE register: accruals, reversals, prepaids, depreciation, and deferred revenue, each waiting on approval.
- **[journal-entry](./skills/financial-close/journal-entry/SKILL.md)**: One journal entry drafted to contract: balanced, sourced, approved, and CSV-ready.
- **[review](./skills/financial-close/review/SKILL.md)**: Fresh-eyes review of a prepared close, ending in a ready or not-ready verdict.
- **[deliver](./skills/financial-close/deliver/SKILL.md)**: The close package: statements, a close memo opening on the executive summary, and a workpapers workbook.

### Technical Accounting

Judgments under an accounting standard, reasoned from the source documents.

**Model-invoked**

- **[revenue-recognition](./skills/technical-accounting/revenue-recognition/SKILL.md)**: ASC 606 for subscription and services contracts: revenue policy, new or nonstandard contracts, modifications, and the monthly revenue roll.

### Agents

Spawned by the skills, each in a fresh context that sees only the files.

- **[close-reviewer](./agents/close-reviewer.md)**: Runs `review` on a close folder it did not prepare.
- **[revenue-challenger](./agents/revenue-challenger.md)**: Argues the strongest case against a draft revenue conclusion.

## How A Close Flows

| Phase | Skill | What it produces |
| --- | --- | --- |
| Intake | `intake` | Readiness report, with the request list for what is missing |
| Prep | `prep` → `reconcile`, `categorize` | A reconciliation proof per account; a dispositioned cleanup list |
| Adjust | `adjust`, using `journal-entry` and `revenue-recognition` | JE register and import CSV |
| Review | `review`, in the `close-reviewer` agent | Verdict: ready, or blockers routed to the phase that owns them |
| Deliver | `deliver` | Statements, close memo, workpapers workbook |

Close state is derived from evidence (the books and the workpapers), not from a status file, so the next session or a teammate can resume a close. Setting up one workspace per client, and sharing closes across a team, is in [docs/workspaces.md](./docs/workspaces.md). The words the skills use are defined in [CONTEXT.md](./CONTEXT.md).

## The Close Kit

`scripts/closekit.py` (Python 3.9+, standard library only) runs the checks that must be executed rather than reasoned through:

| Command | Proves |
| --- | --- |
| `tb` | The trial balance balances |
| `tie` | GL opening plus activity equals TB closing per account, with the constant-difference test |
| `je` | The import CSV meets the entry contract; with `--log`, every entry has a logged approval |
| `fingerprint` | Whether data changed since it was validated or reviewed |
| `lint` | A document is free of the banned voice tells |
| `log` | A well-formed row is appended to the close log |
| `rev` | ASC 606 allocation, schedules, modifications, and contract balances from a contract file |

## Safety Contract

These skills prepare work for a qualified accountant to review and sign. They are not accounting, tax, or legal advice, and their output is not an audit, review, or compilation engagement. You remain responsible for every figure you deliver.

- Every figure traces to your data or a calculation you approved. A gap in the data is an exception, never an estimate.
- No entry is marked approved, and no close is called complete, without your explicit confirmation.
- The skills never fetch external URLs. They read a connected source (a CRM, a shared drive) only when you have connected it, and post an update anywhere only when you say yes. Your data stays in your workspace.

## Contributing

This repo doesn't accept pull requests. If a skill reaches the wrong treatment or doesn't fire when it should, [open an issue](https://github.com/hazlijohar95/skills/issues) with what you expected and what it did. Fork freely: it's MIT licensed, and [CLAUDE.md](./CLAUDE.md) explains the conventions (buckets, naming, invocation, how to verify a change).
