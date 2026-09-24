# Better Accountant

Agent skills that close the books the way a careful preparer would.

Drop in a trial balance and a general ledger export from any accounting system, type `/close`, and work through intake, prep, adjust, review, and deliver. The agent derives what the data can prove, follows this client's precedent, and brings you one list of open items instead of fifty interruptions. For US GAAP clients, it also makes ASC 606 revenue calls from the contracts themselves.

No connectors required. Nothing is posted anywhere: adjusting entries leave as an approved register plus an import-ready CSV you load into your own system.

Built for accountants and bookkeepers who sign their name to the result. More at [better-accountant.com](https://better-accountant.com).

## Installation

### Claude Code

```
/plugin marketplace add hazlijohar95/skills
/plugin install better-accountant@better-accountant
```

### Claude and Cowork

1. Download `better-accountant.zip` from the latest release.
2. Open **Customize** → **Plugins** → **Add** → **Upload plugin** (in Cowork, Customize is in the left sidebar).
3. Select the zip and confirm. The trust warning is expected for any uploaded plugin. This plugin reads and writes only files in your workspace.

Run full closes in **Cowork**, or anywhere with a file workspace: a close's state lives in its files. Quick questions and one-off checks work in any chat.

## Quick start

```
/setup-client Acme Co      ← optional: a 5-minute interview that saves the client profile
/close Acme Co 2026-07     ← runs the close; the period can be a month, quarter, or year
```

Or start smaller: drop a trial balance into the chat and ask "are these books ready to close?"

## Why these skills exist

An agent can already do bookkeeping. These skills fix the ways it does it badly.

### #1: The numbers are made up

**The problem.** A model will add a column in prose, get it slightly wrong, and write the result into a memo with full confidence. When data is missing, it fills the gap with a plausible estimate.

**The fix.** Every figure traces to your data or to an executed computation. The [close kit](#the-close-kit) runs the mechanical checks (the TB balances, the GL ties to the TB, the entries balance) so they are executed, never reasoned through, and its output goes into the workpaper as evidence. A gap in the data becomes an exception on the register, never an estimate.

### #2: Nobody actually approved it

**The problem.** "Approved" in a spreadsheet, or in a past conversation, is a claim. An agent that trusts it ships entries nobody signed off.

**The fix.** An approval counts only when it is posted in the books or recorded in the close log, naming who gave it. `closekit je --log` refuses an import CSV holding any entry without one. No entry is marked approved, and no close is called complete, without your explicit confirmation.

### #3: The preparer grades its own work

**The problem.** A reviewer who has read the preparer's summary checks the story, not the books.

**The fix.** [`review`](./skills/financial-close/review/SKILL.md) runs in a separate `close-reviewer` agent that sees only the close folder and reruns the kit's checks itself. By default, a revenue judgment that is material or contested goes to a `revenue-challenger` agent whose only job is to argue the other side.

### #4: Revenue by template

**The problem.** Most revenue schedules follow the invoices. ASC 606 follows control of what was promised, and the facts that change the answer (a side letter, a termination right, a discounted option) sit in the documents, not the billing system.

**The fix.** [`revenue-recognition`](./skills/technical-accounting/revenue-recognition/SKILL.md) reads the contract documents first and works five questions from first principles. Each conclusion names its deciding fact and the treatment it rejected, in a position memo. The kit does the allocation and schedule arithmetic, and codification references come only from a verified table.

### #5: Fifty interruptions

**The problem.** An agent that asks every question the moment it thinks of it turns a close into a chat.

**The fix.** Questions are batched at phase boundaries and put as multiple choice, with a recommended answer and the figure at stake. Only an entry approval or a true blocker interrupts a phase, and anything above materiality is asked on its own.

## Reference

These split on who can start them. **User-invoked** skills start only when you type them; `close` is one, because starting a close is your decision. **Model-invoked** skills can be typed, or the agent reaches for them when the task fits, and each also works on its own.

### Financial close

Close one client's books for one period, from trial balance and GL exports.

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

### Technical accounting

Judgments under an accounting standard, reasoned from the source documents.

**Model-invoked**

- **[revenue-recognition](./skills/technical-accounting/revenue-recognition/SKILL.md)**: ASC 606 for subscription and services contracts: revenue policy, new or nonstandard contracts, modifications, and the monthly revenue roll.

### Agents

Spawned by the skills, each in a fresh context that sees only the files.

- **[close-reviewer](./agents/close-reviewer.md)**: Runs `review` on a close folder it did not prepare.
- **[revenue-challenger](./agents/revenue-challenger.md)**: Argues the strongest case against a draft revenue conclusion.

## How a close flows

| Phase | Skill | What it produces |
| --- | --- | --- |
| Intake | `intake` | Readiness report, with the request list for what is missing |
| Prep | `prep` → `reconcile`, `categorize` | A reconciliation proof per account; a dispositioned cleanup list |
| Adjust | `adjust`, using `journal-entry` and `revenue-recognition` | JE register and import CSV |
| Review | `review`, in the `close-reviewer` agent | Verdict: ready, or blockers routed to the phase that owns them |
| Deliver | `deliver` | Statements, close memo, workpapers workbook |

Close state is derived from evidence (the books and the workpapers), not from a status file, so the next session or a teammate can resume a close. Setting up a workspace per client, and sharing closes across a team, is covered in [docs/workspaces.md](./docs/workspaces.md). The words the skills use are defined in [CONTEXT.md](./CONTEXT.md).

## The close kit

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

Run `python3 scripts/closekit.py <command> --help` for flags.

## Safety contract

- Every figure traces to your data or a calculation you approved. A gap in the data is an exception, never an estimate.
- No entry is marked approved, and no close is called complete, without your explicit confirmation.
- The skills never fetch external URLs. They read a connected source (a CRM, a shared drive) only when you have connected it, and post an update anywhere only when you say yes. Your data stays in your workspace.

## Contributing

Repo conventions (buckets, naming, invocation, how to verify a skill change) are in [CLAUDE.md](./CLAUDE.md).

MIT licensed.
