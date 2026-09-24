---
name: deliver
description: Assemble the close package. Use when producing final statements, the close memo (a Word document opening with the executive summary), or a workpapers workbook after review returns ready.
---

# Deliver

Plugin root: the folder two levels above this file, which is
`<plugin root>/skills/deliver/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

Turn a reviewed close into the deliverable: financial statements, a close memo delivered
as a Word document that opens with the owner-facing executive summary, and a workpapers
workbook. Every figure in the package traces to the adjusted trial balance; the package
contains nothing the close did not prove.

## Precondition

A review report from the review skill with a **ready** verdict that is current
against the books and workpapers, judged by content, not file dates: the report records
the figures it reviewed, and it is stale when the books or the other workpapers (the
report itself excluded) no longer match them. Check it with
`closekit fingerprint --check workpapers/review.fingerprint.json` (kit at
`<plugin root>/scripts/closekit.py`); a failed check is a stale report. No report, a not-ready
verdict, or a stale report: stop and say so. Never package silently past a missing, failed, or stale review.

**Delivering not ready is a real path, not an edge case.** A first close on messy books
often ends not ready, and the client still needs something in hand. On the user's explicit
choice, build the interim package: the same artifacts, with the memo and cover leading
with NOT READY and the blockers named, every statement labeled draft, and the memo's
executive summary opening with what these numbers cannot yet prove rather than burying it. The
override is recorded in the memo and the close log when one is kept. An interim package
that reads like a finished one is the failure; the label is the product.

## Inputs

- The close folder: adjusted TB, workpapers, JE register, review report, exceptions register
- The client profile for deliverable preferences (naming, emphasis, recipients), when it
  exists

## Workflow

1. Build the statements from the adjusted TB: P&L, balance sheet, and cash flow (indirect),
   each with prior-period comparatives when a prior TB exists. Formats in
   [reference/close-package-format.md](reference/close-package-format.md). Retained earnings
   proof: prior equity plus net income ties to the balance sheet.
2. Build the workpapers workbook (one Excel file): a summary tab listing every material
   account with its support, linked to one tab per area (each reconciliation proof, each
   schedule, the JE register, the cleanup list). Summary tab figures reference the detail
   tabs; nothing is retyped.
3. Write the close memo as a Word document (.docx), never markdown. It opens with the
   executive summary for the owner: plain language, the three to five things that mattered
   this period, flux highlights with their drivers, and cash position. Then the preparer's
   sections: scope and basis, what was reconciled, entries booked (count and total), open
   items and accepted exceptions, the review verdict, and a sign-off checklist with the
   preparer and reviewer lines. One document serves both readers; there is no separate
   executive summary file. For a client with a profile Revenue section, the preparer's
   sections add revenue by stream and by timing (over time, point in time), opening and
   closing contract balances from `closekit rev balances`, the revenue positions approved
   this period with their memo paths, and any change to what was previously booked.
4. Name and file everything in `package/` per the file set in
   [reference/close-package-format.md](reference/close-package-format.md). If a
   cloud storage or docs connector is available (Drive, OneDrive, Notion, SharePoint),
   offer to save the package and the updated profile there too; a connected store is
   durable across sessions and visible to teammates, which the session workspace is not.
   The workspace copy remains the working copy; note where the shared copy went in the
   memo and the close log when one is kept.
5. Close out: note the delivery date and post-close follow-ups (accrual reversals due next
   period, aging investigate items, schedule updates such as new assets or new deferral
   contracts found this close) in the memo, and in the close log when one is kept.
6. Offer the profile update: one short list of things learned this close (new recurring
   items, coding conventions, a threshold the user corrected). Save to the profile file
   only what the user explicitly approves.
7. In a single-client project, end with the knowledge sync list: the files worth adding or
   refreshing in the project's knowledge, each with a one-line reason. Typically the
   profile (if it changed this close) and the close memo (so future chats know what
   happened this period). Agents cannot write to project knowledge; the user adds these
   themselves, so name the exact files and paths to make it a ten-second job. Workpapers
   and the close log stay out of knowledge on purpose: they are per-period audit
   artifacts, not standing context.

## Degradation

| Missing input | Fallback |
| --- | --- |
| Prior TB | Statements without comparatives; memo says so |
| Cash flow inputs (no prior balance sheet) | Deliver P&L and balance sheet; state why cash flow is omitted |
| Client profile | Default naming and a standard package; offer setup afterward |

## When to ask vs proceed

**How to ask.** Every question to the user goes through the AskUserQuestion tool as
multiple choice, never as a question in prose. Each gets two to four options, the
recommended one first and marked "(Recommended)", each described by what it changes,
with the figure where there is one. Follow `<plugin root>/skills/close/reference/asking.md` for batching,
approvals, and what to do when the tool is unavailable.

Packaging is mechanical; the judgment already happened. The only questions worth asking are
presentation preferences, and only when the profile does not answer them. Running unattended,
use the defaults and note them.

## Completion criteria

The package is done when every box below is checkable:

- [ ] Every statement line traces to the adjusted TB; statements foot and cross-foot
- [ ] Balance sheet balances, and retained earnings proves
- [ ] Workbook summary tab covers every material account with a link to its support
- [ ] Memo discloses every open item and accepted exception from the register
- [ ] The memo is a Word document that opens with the executive summary
- [ ] Files are named to convention and filed in `package/`
- [ ] `closekit lint` passes on the memo, the statements, and every other text file in
      `package/`
- [ ] `closekit fingerprint --check` on the review fingerprint still passes after packaging

## Guardrails

- The package reports the close as it is. No figure is adjusted, smoothed, or reclassified
  at packaging time; a late find goes back through adjustments and review.
- Statements come from the adjusted TB alone, never from partially updated sources.
- The executive summary simplifies language, never numbers.

## Deliverable

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

```markdown
### Close package: <client>, <period>

**Delivered:** <file list with paths>
**Statements:** <P&L net income, BS total assets, cash flow net change>
**Entries booked:** <count, total>
**Open items:** <disclosed exceptions and follow-ups, or none>
**Verdict packaged under:** <ready / user override, logged>
**Profile updates offered:** <saved / declined / none>
```

## Reference files

- [reference/close-package-format.md](reference/close-package-format.md): statement layouts,
  memo template, and workbook tab map.
