---
name: review
description: Reviewer pass over a prepared close. Use when reviewing a close before delivery, running flux analysis on draft statements, or when a manager asks to check work a preparer finished.
---

# Review

Plugin root: the folder three levels above this file, which is
`<plugin root>/skills/financial-close/review/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

Fresh eyes on a prepared close. Re-derive everything from the working folder's artifacts and
data; trust no stage's claim about itself. The verdict is binary, ready or not ready, and
every not-ready has its blockers routed to the phase that owns the fix. This is the manager's
entry point: it runs on any close folder, whoever or whatever prepared it.

## Inputs

- The close folder (`closes/<client>/<period>/`, or `closes/<period>/` in a single-client
  workspace) with `inputs/`, `workpapers/`, and the close log when one is kept
- The client profile for materiality and risk areas, when it exists

No close folder? Review whatever the user provides (a TB and draft statements at minimum)
and scope the verdict to what was checkable.

## Workflow

Re-derive each check from the underlying data, not from the workpaper's own summary line.
Where the close kit (`<plugin root>/scripts/closekit.py`) covers a check, rerun the kit
yourself; a kit output pasted into a workpaper is the preparer's evidence, not yours. First
run `closekit fingerprint --check workpapers/inputs.fingerprint.json` when it exists: data
that changed since intake sends the close back to intake before anything else is reviewed.

1. TB roll: `closekit tb` on the adjusted TB, then prior TB plus GL activity plus approved
   adjustments equals the final adjusted TB, account by account. List every account that
   does not roll.
2. Balance sheet substantiation: every material balance sheet account ties to a
   reconciliation proof, a schedule, or a named exception on the register. A material
   account with none of the three is a blocker. Equity in a first period: the equity
   roll (contributions traced to cash receipts plus income) is its substantiation; later
   periods carry it via the roll-forward. Substantiation includes the reality
   check: every business fact the profile records (contracts, inventory, loans, leases,
   related parties, foreign currency) maps to evidence in this close or to a named
   exception; a recorded fact the close never touched is a finding. For a client with
   a profile Revenue section: rerun `closekit rev schedule` and `rev balances` over the
   contract files, and tie revenue by stream, deferred revenue, unbilled receivables,
   contract assets, refund liabilities, and deferred commissions to the adjusted TB.
   A contract billed this period with no contract file, or an amendment with no memo, is
   a finding owned by adjustments.
3. Entries check: `closekit je <csv> --coa --label --log` passes, so every entry in the
   CSV carries a logged approval. Every approved entry in the JE register appears in the
   adjusted TB at the approved amount; no unapproved entry leaked in. Reversal flags set where the register
   says auto-reverse.
4. Flux: compare the adjusted P&L and balance sheet to prior period. For each move above
   materiality, pull the explanation from GL detail (what actually drove it), not from
   plausibility. Profile risk areas get explained regardless of size. This is a review
   analytic feeding the verdict; deep driver decomposition belongs to the advisory workflow.
   Impairment and collectability screens ride along: receivables aged past 90 days or
   stale against their own history, and fixed assets carrying impairment indicators from
   the roll-forward (idle, damaged, discontinued line, fully depreciated but load-bearing)
   are flagged as disclosures for the memo, with measurement routed to the preparer. The
   close never books an allowance or an impairment on its own.
5. Exceptions register: every open item has an owner phase and a disclosure; nothing aged
   out silently. Anything the earlier phases marked investigate is either resolved or
   consciously accepted by the user.
6. Verdict:
   - **Ready**: all checks pass; open exceptions are disclosed and below materiality, or
     explicitly accepted, recording who accepted. Acceptance above materiality is informed
     consent, never a checkbox: present each such exception one at a time, stating its
     consequence in the deliverable's terms ("accepting this means the balance sheet shows
     $7,000 of receivables nobody has verified"), and never fold material acceptances into
     a batch approval. One exception is unacceptable at any size: books that do not
     balance or an unexplained difference inside the data itself; that always blocks.
     When an acceptance substantively belongs to the client rather than the preparer (an
     unsupported material balance, a judgment on their revenue), the operator may accept
     for this close but the memo discloses it as pending client confirmation.
   - **Not ready**: any check fails or any unaccepted material exception remains. List each
     blocker with its owning phase (readiness, reconcile, cleanup, adjustments) so the fix
     lands in the right place.
7. Record the verdict in the review report filed in `workpapers/` (and the close log when
   one is kept). The review report is what unlocks the deliver skill. Staleness is
   judged by content, never by file dates (timestamps lie when folders move between
   machines): the report records the figures it reviewed (adjusted TB totals, entry count
   and total, exception count), and when the books or the other workpapers no longer match
   those figures, the report is stale and the review reruns. Make that mechanical: after
   writing the report, run `closekit fingerprint` over the normalized inputs, the adjusted
   TB, the JE CSV, and the exceptions register with
   `--out workpapers/review.fingerprint.json`, and name the fingerprint in the report.

## Degradation

| Missing input | Fallback |
| --- | --- |
| Prior TB | Flux limited to accounts with prior data; say comparatives were unavailable |
| Prior TB with balance sheet accounts only (post-closing) | Balance sheet flux proceeds; P&L flux unavailable, disclosed. TB roll treats P&L accounts as opening at zero |
| Prior TB carrying YTD P&L balances | TB roll rolls P&L accounts from prior YTD; state the assumption |
| Workpapers for an account | That account fails substantiation; route to its owning phase |
| Close log | Derive scope from the artifacts and books alone and note the review ran without a log |

## When to ask vs proceed

**How to ask.** Every question to the user goes through the AskUserQuestion tool as
multiple choice, never as a question in prose. Each gets two to four options, the
recommended one first and marked "(Recommended)", each described by what it changes,
with the figure where there is one. Follow `<plugin root>/skills/financial-close/close/reference/asking.md` for batching,
approvals, and what to do when the tool is unavailable.

- Fact: the data settles whether a check passes. Derive it; never ask.
- Judgment: whether a disclosed exception is acceptable is the user's call when it is
  material; below materiality, accept, disclose, and move on.

Queue judgment calls and raise them once, with the draft verdict, writing each down as it
is queued. Running unattended, a material unaccepted exception means not ready; never
accept it on the user's behalf. Aggregation is a review check in its own right: sum the
close's proceed-and-disclose judgments and disclosed exceptions; an aggregate above
materiality is itself a material finding, even when every component was individually small.

## Anti-patterns

- **Reviewing the summary.** Confirming a workpaper by reading its own conclusion. The tell:
  a review pass with no recomputation. Every check re-derives from data.
- **The narrative flux.** An explanation that would be equally true of any period ("revenue
  grew due to increased sales"). The tell: no transaction, customer, or vendor named. A flux
  explanation cites what moved in the GL.
- **Verdict creep.** "Ready, mostly" or "ready pending items". The tell: qualifiers on the
  word ready. The verdict is binary; pending material items mean not ready.

## Completion criteria

Review is done when every box below is checkable:

- [ ] TB rolls account by account, or every non-rolling account is a named blocker
- [ ] Every material BS account is substantiated or a named blocker
- [ ] Register and adjusted TB agree: all approved entries in, no unapproved entries in
- [ ] Every flux above materiality and every risk-area move has a GL-sourced explanation
- [ ] The verdict is recorded in the review report with blockers routed to owning phases

## Guardrails

- Independence: recompute; never accept a stage's self-report as evidence.
- The verdict cannot be negotiated past a failed check; fix and re-review.
- Review is read-only. It proposes no entries and edits no workpapers; it routes.

## Deliverable

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

```markdown
### Review: <client>, <period>

**Verdict:** <ready / not ready>
**TB roll:** <clean, or accounts listed>
**Substantiation:** <n of m material BS accounts tied; failures listed>
**Entries:** <register vs TB result>
**Flux:** <each material move: amount, driver from GL>
**Blockers:** <each with owning phase, or omit when ready>
**Accepted exceptions:** <each with who accepted it, or omit>
```
