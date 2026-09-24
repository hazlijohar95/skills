---
name: intake
description: Close readiness check that opens a close. Use when starting a close for a period, when the user asks whether books are ready to close, or when validating a trial balance and GL export against statements.
---

# Intake

Plugin root: the folder three levels above this file, which is
`<plugin root>/skills/financial-close/intake/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

Take whatever the user has provided, prove what it can prove, and produce a close readiness
report on the spot: what is present, what is missing, and what each gap blocks. The report is
the artifact; the request list lives inside it. Never make the user assemble a perfect data
package before seeing value.

## Inputs

Work with any subset of:

- Trial balance for the period (required for a full close; a GL export can substitute, see
  degradation below)
- Prior-period trial balance
- General ledger detail export (CSV or Excel, any system)
- Bank and credit card statements for the period
- Subledger listings or schedules (AR aging, AP aging, prepaid schedule, fixed asset
  register, loan statements)

If a client profile exists (`clients/<client>/profile.md`, or `profile.md` at the root in
a single-client workspace, or in the project's knowledge), read it first: it names the
accounts, schedules, and statements this client's close expects, which turns the generic
checklist below into a client-specific one.

## Workflow

1. Inventory what was provided. Identify each file's type, system of origin, and period
   coverage from its contents, not its filename. Normalize the TB, prior TB, and GL into
   the close kit's canonical CSVs (the close skill's "The close kit" section; kit at
   `<plugin root>/scripts/closekit.py`) under `inputs/normalized/`, and record
   the column mapping you used on the report.
2. Validate the trial balance with `closekit tb`, and the prior TB the same way: debits
   equal credits; the period label matches what the user asked to close. If a prior TB is
   available, confirm prior close balances roll into this period's opening balances and
   flag any account that moved outside the period.
3. Tie the GL export to the TB with `closekit tie --tb --gl --prior`: for each account,
   opening balance plus period activity equals the closing TB balance. List every account
   that does not tie. Before diagnosing any cause, run the constant-difference test on the
   failures: difference per account per period. Constant from the first period means the
   records disagree about openings; a difference that appears partway means activity or
   cutoff. A test that cannot distinguish the two supports no conclusion. The kit runs the
   test when the GL carries opening rows and a prior TB is given, and prints which case
   each failure is.
4. Check period completeness: GL activity spans the full period, and no activity is dated
   after period end without explanation. A quiet stretch at either boundary is
   indistinguishable from a truncated export on its own; corroborate against the bank
   statement's first and last items when a statement is available, and say which check you
   used.
5. Build the coverage map: for each balance sheet account, note what evidence exists to
   support it this period (statement, subledger, schedule, or nothing yet). Then check the
   map against the profile's business reality: every fact recorded there (contracts
   spanning periods, inventory, loans, leases, related parties, foreign currency) must
   have matching evidence in the map or a line on the request list naming what is missing
   and what it blocks. A recorded fact with no evidence is a gap, never an ignore.
6. Write the close readiness report (format below) and, inside it, the missing-items request
   list as a client-ready message. Use
   [reference/request-list-format.md](reference/request-list-format.md) for the message.
7. If this run is part of a close (a close folder exists or the user wants one), file the
   report in `workpapers/` and keep exactly one copy of each input inside the close
   folder's `inputs/`, which is the close's canonical data set (the user's originals may
   live elsewhere in the workspace; on any divergence, stop and confirm which is current).
   Within the close folder, never fork a second copy; a corrected file replaces the
   original. Fingerprint the inputs
   (`closekit fingerprint inputs/normalized/*.csv --out workpapers/inputs.fingerprint.json`)
   and quote each file's row count and totals on the report, adding each statement's
   ending balance by hand, so a later phase confirms with `fingerprint --check` that the
   data it builds on is the data this report validated. Append the outcome to the close log when
   one is kept. Standalone, just deliver the report and offer to start a close folder.

## Degradation

| Missing input | Fallback |
| --- | --- |
| Trial balance | Derive a working TB from the GL export and label every figure derived, not stated |
| Prior-period TB | Skip roll-forward and flux checks; note that comparatives are unavailable |
| Prior TB with balance sheet accounts only (post-closing) | Roll-forward and balance sheet flux proceed; P&L comparatives unavailable, disclosed |
| GL detail | Validate the TB alone; reconciliation and cleanup will be blocked and say so |
| Statements | Mark cash and card accounts unverifiable this period; the reconcile phase carries the exception |
| Subledgers and schedules | Mark those balances unsupported; adjustments will need them for roll-forwards |

A missing input downgrades the report; it never stops it.

## When to ask vs proceed

**How to ask.** Every question to the user goes through the AskUserQuestion tool as
multiple choice, never as a question in prose. Each gets two to four options, the
recommended one first and marked "(Recommended)", each described by what it changes,
with the figure where there is one. Follow `<plugin root>/skills/financial-close/close/reference/asking.md` for batching,
approvals, and what to do when the tool is unavailable.

- Fact: the data can settle it. Derive it; never ask.
- Precedent: this client's prior periods settle it. Follow the precedent and note it.
- Judgment: more than one defensible treatment. Below materiality, take the conservative
  path, proceed, and disclose. Above materiality, hard to reverse, or in a profile-flagged
  risk area, queue a question.

Two hard rules on the queue. Write a question down (close log or exceptions register)
the moment it is queued; a question held only in working memory is a question that will be
silently answered. And track the running total of proceed-and-disclose judgments: the
moment their aggregate crosses materiality, stop treating them as individually small,
convert the open ones to questions, and say the aggregate out loud. Twenty immaterial
guesses are one material guess.

Queue questions and raise them once, at the end, inside the report. Running unattended, take
every proceed-and-disclose default and finish with disclosed exceptions rather than stalling.

## Completion criteria

Readiness is done when every box below is checkable:

- [ ] Every provided file is classified and either used or explicitly set aside with a reason
- [ ] The TB balances, or the imbalance is quantified and flagged
- [ ] Every TB account either ties to the GL or is on the exceptions list with the difference
- [ ] Every balance sheet account has its evidence status mapped: supported, or on the
      request list with what its absence blocks
- [ ] The verdict is stated: ready to close, ready with exceptions, or blocked, with the
      blocking items named

## Guardrails

- Figures come from the provided data. A number the data cannot support is a gap on the
  request list, never an estimate.
- Diagnose from file contents, not filenames or the user's description of what a file should
  contain.
- State the verdict plainly. "Ready with exceptions" must name the exceptions; never round up
  to "ready".

## Deliverable

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

```markdown
### Intake: <client>, <period>

**Verdict:** <ready / ready with exceptions / blocked>
**Provided:** <files received and what each covered>
**Proven:** <TB balanced, GL tie-out result, roll-forward result>
**Gaps:** <each missing item and what it blocks>
**Request list:** <client-ready message, per reference/request-list-format.md>
**Next step:** <one action>
```

## Reference files

- [reference/request-list-format.md](reference/request-list-format.md): the client-ready
  missing-items message format.
