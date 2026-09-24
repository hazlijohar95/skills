---
name: adjust
description: Period-end adjusting entries. Use when booking or rolling forward accruals and reversals, amortizing prepaids, recording depreciation, or recognizing deferred revenue for a period.
---

# Adjust

Plugin root: the folder three levels above this file, which is
`<plugin root>/skills/financial-close/adjust/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

Turn schedules and exceptions into a JE register: every adjusting entry the period needs,
each with its workpaper, waiting on explicit approval. Approved entries leave as an
import-ready CSV for the user's own system. This skill posts nothing anywhere.

## Scope

Owned here, the 80% core:

- Accrued expenses and revenue, with automatic reversal of prior-period accruals
- Prepaid amortization
- Depreciation and amortization from a fixed asset schedule
- Deferred revenue recognition for streams whose invoices match delivery (one
  obligation, billed for its own service period, no variable terms). Anything else is
  the revenue-recognition skill's: when the profile has a Revenue section, run the revenue-recognition skill's
  Period roll playbook for those streams and take its proposed entries onto this
  register. Its judgments are already approved positions. This skill books them and
  does not revisit them.
- Reclassification and capitalization entries approved in cleanup or raised by
  reconciliation, when a journal entry is how the amount moves

Out of scope, each with its manual path: inventory and COGS (needs a count or costing
method; do it in a workpaper and import the result), FX remeasurement (needs rate policy),
tax provision (preparer's call), equity compensation (needs the grant ledger), intercompany
(needs both entities' books), AR allowance and bad debt write-offs (the review skill's
collectability screen flags candidates; measuring and booking the reserve is the
preparer's policy call), asset impairments (screens flag indicators; measurement needs a
valuation judgment), contract cost estimation and loss provisions (the WIP schedule takes
estimated total cost as the user's input and flags loss contracts; estimating costs or
booking the loss is the preparer's). Name these in the deliverable when the data suggests
they exist; never attempt them.

Out of scope converts when the user supplies the governing judgment mid-run. A stated
policy or measurement from the user (an allowance percentage, an estimated total cost, a
costing method) is theirs, not ours: record it, offer to save it to the profile, then run
it like any authorized policy, with schedule-shaped arithmetic, an entry under the journal-entry
contract, and the usual gate. Out of scope means the judgment is not ours to make; a
judgment the user hands us is made.

## Inputs

- The client profile (`clients/<client>/profile.md`, or `profile.md` at the root in a
  single-client workspace): recurring schedules, estimation policies, materiality
- Schedules: prepaid schedule, fixed asset register, deferred revenue schedule, standing
  accrual list. Formats in [reference/schedule-formats.md](reference/schedule-formats.md).
- The exceptions register from the reconcile and categorize skills, when running inside a close
- GL detail and TB for control account tie-outs

## Workflow

1. Collect the work: profile schedules to roll forward, adjustment-required items from the
   register, and standing accruals due this period.
2. Check reversals first: every prior-period accrual marked auto-reverse either has its
   reversal in this period's GL, was settled directly against the liability (a payment
   debiting the accrual, documented on the schedule), or gets a reversal proposed here. An
   accrual relieved neither way is the first entry on the register; an accrual relieved
   both ways is a double-relief flag. The prior period's JE register is the
   machine-readable carrier of auto-reverse obligations: read its flags when it is
   available, and fall back to the GL pattern when it is not.
3. Roll each schedule forward per
   [reference/schedule-formats.md](reference/schedule-formats.md), including the optional
   loan roll-forward with its interest recalc whenever a lender statement is on hand. Each
   schedule must tie to its GL control account exactly: schedule closing balance equals TB
   balance, rounding documented on the schedule, never absorbed silently.
4. Completeness scan against the period's activity, both directions: a new payment to a
   prepaid-type vendor with no schedule row, an asset-sized purchase not on the register,
   and, the easy one to miss, a new billing whose service period extends past the close
   (a customer with an existing deferral contract, or invoice language like "annual" or
   "12 months") sitting fully in revenue. For a contract client, a new or amended
   contract routes to the revenue-recognition skill instead of a question here: bundles, setup fees,
   usage, credits, ramps, and amendments are revenue judgments, not schedule rows. Check the exceptions register first: an item
   cleanup already dispositioned or already asked about is settled, not re-asked. Each
   fresh hit is a question or a new schedule row, never silently left where it landed.
   The scan includes an **unrecorded liabilities check**: read whatever post-period
   evidence exists (early next-period GL or bank activity, bills dated after period end
   for period services, statements arriving late) for expenses that belong in the period
   but sit in neither AP nor accruals. In-period patterns count as evidence too; the
   payroll cutoff is the classic case: a pay cadence whose last run predates period end
   means earned, unpaid wages, and the run summary is the source to request. Each catch becomes a proposed accrual with the
   evidence cited; file the scan as its own small workpaper listing what was searched and
   what was found, including a clean result. No post-period data provided: the scan is
   limited to bills and statements on hand, disclosed as such.
   The scan also runs against the profile's business reality: when the profile records
   revenue earned on a different pattern than it is billed (contracts spanning periods,
   progress billings), the matching schedule (WIP, deferral) is a required input like any
   other; missing means this area is blocked with the schedule on the request list, never
   quietly treated as billed-equals-earned.
5. Draft each entry under the journal-entry skill's contract: balanced, dated within the period,
   accounts from the client's chart, a stable memo, a cited source, and a workpaper
   showing source, calculation, and tie-out.
6. Missing source data blocks that adjustment. A blocked adjustment goes on the register
   with what is missing; it is never estimated into existence, unless the profile authorizes
   a named estimation policy for exactly that item (then apply the policy and label the
   figure estimated per policy).
7. Present the JE register for approval. Itemize entries above materiality individually;
   offer the rest as a reviewed batch.

   **Gate: do not mark any entry approved without the user's explicit confirmation.** No
   confirmation, no approval; the entry stays proposed.

8. Emit the import CSV of approved entries only, per the journal-entry skill's CSV contract, and file
   it with the register in `workpapers/`. Run `closekit je` on it with `--coa`, `--label`,
   and `--log` (kit at `<plugin root>/scripts/closekit.py`) and put the output on the register; the CSV
   is done only when the kit passes. The register is the record of what was approved,
   declined, and blocked; append the outcome to the close log when one is kept.

Cash-basis client (per profile): steps 2 to 5 collapse to a reversal and carryover check,
and accrual conversion is offered as an explicit opt-in, never assumed.

## Degradation

| Missing input | Fallback |
| --- | --- |
| A profile schedule | Rebuild it from GL history when the pattern is unambiguous, labeled rebuilt; otherwise blocked with a request for the schedule |
| Fixed asset register | Depreciation blocked; propose carrying prior period's entry only if the profile authorizes it as policy |
| Exceptions register | Standalone run: work from provided schedules only and say cleanup items were not sourced |
| Prior-period GL | Reversal check limited to what the user confirms; each unverified reversal disclosed |

## When to ask vs proceed

**How to ask.** Every question to the user goes through the AskUserQuestion tool as
multiple choice, never as a question in prose. Each gets two to four options, the
recommended one first and marked "(Recommended)", each described by what it changes,
with the figure where there is one. Follow `<plugin root>/skills/financial-close/close/reference/asking.md` for batching,
approvals, and what to do when the tool is unavailable.

- Fact: the schedule and GL settle it. Derive it; never ask.
- Precedent: the client books this the same way every period. Follow it and note it.
- Judgment: more than one defensible treatment. Below materiality, take the conservative
  treatment, proceed, and disclose. Above materiality, hard to reverse, or in a flagged risk
  area, queue a question.

Two hard rules on the queue. Write a question down (close log or exceptions register) the
moment it is queued; a question held only in working memory is a question that will be
silently answered. And track the running total of proceed-and-disclose judgments: the
moment their aggregate crosses materiality, stop treating them as individually small,
convert the open ones to questions, and say the aggregate out loud. Twenty immaterial
guesses are one material guess.

Queue questions and raise them with the register presentation; the approval gate is the
natural checkpoint. Running unattended, leave every entry in proposed state with the register
complete; approval never happens without a human.

## Anti-patterns

- **The estimate that closes the gap.** A schedule that will not tie gets a rounding entry to
  force it. The tell: an entry whose memo cannot name a source document or policy. The gap
  goes on the register instead.
- **The permanent accrual.** An accrual repeats every period but its reversal never posts,
  quietly doubling the liability. The tell: a liability balance that only ever grows.
  Reversals are checked before new accruals are drafted.

## Completion criteria

Adjustments are done when every box below is checkable:

- [ ] Every schedule ties to its control account exactly, with rounding documented
- [ ] Every prior-period auto-reverse accrual is reversed, or its missing reversal is on the
      register
- [ ] Every register entry is approved, declined, or blocked with the missing source named
- [ ] The CSV contains approved entries only, and it foots: `closekit je --log` passes
- [ ] Out-of-scope adjustments the data suggests are named in the deliverable

## Guardrails

- **No entry is marked approved without explicit confirmation.** Batch approval is fine;
  silent approval is not. An approval mark in a register of unknown provenance (found on a
  shared drive or in project documents with no session trail) is a proposal: re-confirm
  before that entry enters the import CSV.
- Figures come from schedules, source documents, or authorized policy. A data gap is a
  blocked adjustment, never an estimate.
- A method gap blocks the same way a data gap does. Any measurement with more than one
  accepted method (inventory costing, contract revenue recognition, depreciation
  convention, FX rates) runs under the profile's stated method or stops with a question;
  an assumed method is never the silent default, no matter how common it is.
- Nothing is posted to any system. The CSV is the handoff; the user imports it.

## Deliverable

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

```markdown
### JE register: <client>, <period>

| # | Entry | Dr | Cr | Amount | Source | Status |
| - | ----- | -- | -- | ------ | ------ | ------ |
| 1 | <description> | <account> | <account> | <amount> | <schedule/doc/policy> | <approved/proposed/blocked> |

**Schedules:** <each: closing balance, control account, tie-out result>
**Reversals:** <prior accruals reversed or flagged>
**Blocked:** <each with the missing source>
**Out of scope observed:** <named, with manual path, or omit>
**CSV:** <path, entry count, total Dr = total Cr>
```

## Reference files

- [reference/schedule-formats.md](reference/schedule-formats.md): roll-forward formats for
  prepaids, fixed assets, deferred revenue, standing accruals, and the optional loan roll.

The entry contract and import CSV format live with the journal-entry skill.
