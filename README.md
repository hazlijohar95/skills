# Close

Run an accounting close start to finish, for any client, any period, out of any accounting
system. Drop in a trial balance and a general ledger export, type `/close`, and work through
intake, prep, adjust, review, and deliver with an assistant that behaves like a careful
preparer: it derives what the data can prove, follows this client's precedent, and brings you
one list of open items instead of fifty interruptions.

No connectors required. Nothing is posted anywhere: adjusting entries are delivered as an
approved register plus an import-ready CSV you load into your own system.

## Install

1. Download `close-plugin.zip`.
2. In Claude, open **Customize** → **Plugins** → **Add** → **Upload plugin** (in Cowork,
   Customize is in the left sidebar).
3. Select the zip and confirm. You will see a trust warning; that is expected for any uploaded
   plugin. This plugin reads and writes only files in your workspace.
4. Type `/` to see `close`, `close-setup`, and the eight workflow skills. Installed
   plugins surface in both chat and Cowork.

Where to run what: quick questions and one-shot checks work anywhere. Run full closes in
**Cowork**, which has the file workspace the close's state lives in. On desktop, connect a
local folder for the client so profiles, workpapers, and packages persist on your own disk
between sessions.

## Quick start

```
/close-setup Acme Co          ← optional: 5-minute interview, saves the client profile
/close Acme Co 2026-07        ← runs the close; period can be a month, quarter, or year
```

Or start smaller: drop a trial balance into the chat and ask "are these books ready to
close?" Each skill below also works on its own.

## What's inside

`/close` sequences five phases. Each skill below is also useful standalone:

| Phase | Skill | What it produces |
| --- | --- | --- |
| Intake | `intake` | Close readiness report + missing-items request list |
| Prep | `prep` | Runs the two prep workers below as one phase |
| Prep | `reconcile` | A reconciliation proof per account |
| Prep | `categorize` | Cleanup list: uncategorized, miscoded, transfers, duplicates |
| Adjust | `adjust` | Schedules, approved JE register, import CSV |
| Adjust | `je` | One journal entry, drafted to contract: sourced, gated, CSV-ready |
| Review | `review` | Fresh-eyes review verdict: ready or not ready |
| Deliver | `deliver` | Statements, close memo, workpapers workbook, executive summary |
| Any | `revenue` | ASC 606 position memos, contract files, revenue schedule and balances |

`/close-setup` interviews you once per client and saves a profile (basis, materiality, risk
areas, recurring schedules) that every close for that client reads. Profiles live in your
workspace at `clients/<client>/profile.md`; each close works in `closes/<client>/<period>/`.

## One Claude Project per client

The plugin detects which layout you use, no configuration needed:

- **Shared workspace** (all clients in one place): profiles at `clients/<name>/profile.md`,
  closes at `closes/<name>/<period>/`. Invoke with the client name: `/close Acme Co 2026-07`.
- **One project per client**: the whole workspace belongs to that client. The profile sits
  at the root as `profile.md`, closes at `closes/<period>/`, and the client name becomes
  optional: `/close 2026-07`.

First-time setup for a client project (once per client, two minutes, all done by you, not
by the plugin):

1. Create the Claude Project named for the client.
2. Upload the client's standing documents to the project's knowledge: prior close package,
   schedules, anything the close should always know.
3. Run `/close-setup` once; add the profile it produces to the project's knowledge (or
   paste its block into the project's instructions).
4. Sharing this client with teammates? Add one line to the project's instructions naming
   where close artifacts live (a shared folder everyone connects), e.g.
   `Close state home: Dropbox/Clients/Acme`. Solo, skip this; the workspace is the default.

From then on, start sessions inside the client's project: Claude uses the project's
knowledge as context, so every session begins already knowing the client. Cowork never
writes to a project's knowledge, so files stay the single source of truth: the plugin
writes updates to files and reminds you when the knowledge copy drifts.

## Working as a team

Close state is derived from evidence (the books, the workpapers), not from any one file,
so a teammate's Claude can size up where a close stands from whatever artifacts it can
see. To share those artifacts, connect the same synced folder (Dropbox, Drive, OneDrive, a
network share) as the client workspace on each desktop. Profiles, workpapers, and the
close log become shared: resuming a colleague's half-done close plays back where they left
off, the log shows who approved what, and a reviewer can run `review` on any close
folder regardless of who prepared it.

One convention to keep: one preparer owns an in-flight close at a time. The files have no
locking; simultaneous runs on the same period will conflict the way any shared drive does.

No shared folder? If your Claude has a cloud storage connector (Drive, OneDrive, Notion),
the close package and client profile can be saved there at delivery, the same shared-drive
idea without the desktop folder setup.

## What it needs from you

- Trial balance for the period (and the prior period, for roll-forwards and flux)
- General ledger detail export (CSV or Excel, from any system)
- Bank and credit card statements for the accounts you want reconciled (optional but
  recommended)

Missing pieces never stall the run: the readiness report tells you exactly what is missing and
what it blocks, and the close finishes with disclosed exceptions rather than guesses.

## Revenue recognition (ASC 606)

`/revenue` handles subscription and services revenue for US GAAP clients. It reasons from
the contract documents rather than a billing-based template. Five questions (what is
enforceable, what the customer is buying, the price, the allocation, the timing), eleven
first-principles files it reads as it applies them, and four playbooks: policy setup, a
new or nonstandard contract, a modification, and the monthly period roll the close's
adjust phase runs. Each judgment is written up as a position memo that names its deciding
fact and the treatment it rejected. Anything material goes to an independent
`rev-challenger` agent that argues the other side. `closekit rev` does all the arithmetic
from a JSON contract file (allocation, schedules, modifications, contract balances).
Codification references come only from a verified table in the skill.

## The close kit

`scripts/closekit.py` (Python 3.9+, standard library only) runs the mechanical checks so
they are executed rather than reasoned through: the TB balances (`tb`), the GL ties to the
TB with the constant-difference test (`tie`), the JE CSV meets its contract and every entry
has a logged approval (`je`), data has not changed since it was validated or reviewed
(`fingerprint`), deliverables are free of banned voice tells (`lint`), and the close log
stays well-formed (`log`). Each skill says when to run which. Its output is pasted into
the workpaper as evidence. Run `python3 scripts/closekit.py <command> --help` for flags.

Approvals are recorded as rows in `closes/.../close-log.tsv`, keyed by the entry memo and
naming the approver. `closekit je --log` refuses a CSV holding any entry without one.

The review phase runs in a separate `close-reviewer` agent that sees only the close
folder, so it checks the evidence rather than the preparer's account of it.

## Verifying the plugin

- `python3 tests/test_closekit.py` is the kit's self-check. Run it after any kit change.
- `tests/fixtures/revenue/` holds Tallow Labs, a SaaS and services client with 15
  contracts, each turning on one fact buried in its documents. `answer-keys/` grades them;
  scenarios 13 to 15 are held out (nothing in the skill mentions them). Run them blind the
  same way as below, copying the plugin without `tests/`.
- `tests/fixtures/acme-2026-07/` is a small client with planted defects, listed in its
  `answer-key.md`. To check skill behavior after a skill edit, copy the CSVs (not the
  answer key) into a neutral workspace such as `clients/acme/`, run `/close Acme Co
  2026-07` there, and grade the run against the key. Keep words like test and eval out
  of anything the run can see; an agent that knows it is being graded behaves
  differently.

## Safety contract

- Every figure traces to your data or a calculation you approved. A gap in the data is an
  exception, never an estimate.
- No entry is marked approved, and no close is called complete, without your explicit
  confirmation.
- The plugin never fetches external URLs and never connects to anything. Your data stays in
  your workspace.
