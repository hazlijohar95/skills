---
name: reconcile
description: Account reconciliation for a period. Use when reconciling bank or credit card accounts to statements, tying a subledger (AR, AP, payroll, loans) to its control account, or proving a GL balance against outside evidence.
---

# Reconcile

Plugin root: the folder two levels above this file, which is
`<plugin root>/skills/reconcile/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

Prove each account: outside evidence on one side, the GL on the other, and a proof that ends
at zero or at a named list of reconciling items. The artifact is one reconciliation proof per
account. An unexplained difference is never absorbed, plugged, or rounded away.

## Inputs

- GL detail for the period (per account: opening balance, activity, closing balance)
- The outside evidence per account: bank or card statement, subledger listing, lender
  statement, payroll register
- The client profile (`clients/<client>/profile.md`, or `profile.md` at the root in a
  single-client workspace) for materiality and the expected account list, when it exists

Inside a close, take scope from the close context (the readiness report and profile, plus
the close log when one is kept) and write proofs to the close folder's `workpapers/`.
Standalone, reconcile whatever pair of sources the user provides and offer to start a close
folder.

## Workflow

1. List the accounts in scope: every cash and card account, plus each account with a
   provided subledger or third-party statement. Schedule-backed accounts (prepaids, fixed
   assets, deferred revenue, standing accruals) are out of scope here: their period-end
   proof is the adjustments phase's roll-forward, since a schedule states an opening
   position, not independent evidence of the closing one. An in-scope account with no
   outside evidence is an exception (routed to the readiness request list), not a skipped
   account.
2. For each account, build the proof:
   - Start from the statement or subledger ending balance.
   - Match items to GL activity: exact amount first, then amount within rounding and date
     within a few business days. Match deposits and withdrawals separately; never net.
   - Everything unmatched on either side becomes a reconciling item.
3. Classify every reconciling item into exactly one of the three buckets in
   [reference/reconciling-items.md](reference/reconciling-items.md): timing, adjustment
   required, or investigate.
4. Items classified adjustment required go on the exceptions register for the
   adjust skill, with the proposed account, amount, and reason. Do not draft the
   entry here; the adjustments skill owns entries.
5. Write the proof per account (format below). The proof must foot: statement balance plus
   or minus reconciling items equals the GL balance, difference zero.
6. The proofs in `workpapers/` are the record: each account reconciled or excepted, every
   adjustment-required item carried forward by name on the exceptions list. Subledger ties
   are filed as their own named workpapers (`ar-aging-tieout`, `ap-aging-tieout`,
   `payroll-tieout`, and so on) so a reviewer finds them at a glance rather than inside a
   bank proof. Append the outcome to the close log when one is kept.

## Degradation

| Missing input | Fallback |
| --- | --- |
| Statement for a cash/card account | Account is unreconciled this period; state the GL balance and flag it unverified |
| Subledger for a control account | Tie-out skipped; balance marked unsupported, carried as an exception |
| Opening GL balance | Reconcile activity only and say the proof covers movement, not position |
| Prior reconciliation | Treat all pre-period open items as this period's reconciling items and note the assumption |

## When to ask vs proceed

**How to ask.** Every question to the user goes through the AskUserQuestion tool as
multiple choice, never as a question in prose. Each gets two to four options, the
recommended one first and marked "(Recommended)", each described by what it changes,
with the figure where there is one. Follow `<plugin root>/skills/close/reference/asking.md` for batching,
approvals, and what to do when the tool is unavailable.

- Fact: the data can settle it. Derive it; never ask.
- Precedent: this client's prior periods settle it (a recurring timing item, a known fee
  pattern). Follow the precedent and note it.
- Judgment: more than one defensible treatment. Below materiality, take the conservative
  path, proceed, and disclose. Above materiality, hard to reverse, or in a profile-flagged
  risk area, queue a question.

Two hard rules on the queue. Write a question down (close log or exceptions register)
the moment it is queued; a question held only in working memory is a question that will be
silently answered. And track the running total of proceed-and-disclose judgments: the
moment their aggregate crosses materiality, stop treating them as individually small,
convert the open ones to questions, and say the aggregate out loud. Twenty immaterial
guesses are one material guess.

Queue questions and raise them once, when all proofs are drafted. Running unattended, take
every proceed-and-disclose default and finish with disclosed exceptions rather than stalling.

## Anti-patterns

- **The plug.** A small unexplained difference gets booked to miscellaneous expense to make
  the proof foot. The tell: a reconciling item whose only description is the amount itself.
  Every difference gets a bucket; an unexplainable one stays in investigate, on the register.
- **Netting.** Matching a deposit against a withdrawal because the net agrees. The tell: one
  GL line matched to two statement lines with opposite signs. Match each direction on its
  own.
- **Trusting the label.** Accepting "reconciled" from the source system without evidence.
  The tell: a proof with no statement balance on it. A proof starts from outside evidence or
  it is not a proof.

## Completion criteria

Reconciliation is done when every box below is checkable:

- [ ] Every in-scope account has a proof that foots to zero difference, or is on the
      exceptions register with the unreconciled amount stated
- [ ] Every reconciling item is in exactly one bucket with an expected resolution
- [ ] Every adjustment-required item is on the register with account, amount, and reason
- [ ] No investigate item was silently dropped; each is on the register with what was tried

## Guardrails

- Figures come from the provided statements, subledgers, and GL. Never fill a gap with an
  estimate.
- An unreconciled difference above materiality blocks the account; say so rather than
  presenting a proof that does not foot.
- Reconciling is read-only: this skill proposes no entries and changes no data. Entries
  belong to the adjust skill.

## Deliverable

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

One proof per account. The proof is two-sided: timing items adjust the statement side,
adjustment-required items adjust the GL side, and the two adjusted balances meet. The
labeled lines below fit a bank or card account; for a subledger tie, swap them for that
subledger's reconciling categories (unposted invoices, payments in transit, unapplied
credits) and keep the two-sided shape, which is the contract.

```markdown
### Reconciliation: <account>, <period>

Statement / subledger ending balance        <amount>
  + Deposits in transit                     <amount>
  - Outstanding checks / charges            <amount>
Adjusted statement balance                  <amount>

GL balance                                  <amount>
  +/- Adjustments required, not yet booked  <amount, listed>
Adjusted GL balance                         <amount>

Difference                                  $0.00

**Reconciling items:** <each: description, amount, bucket, expected resolution>
**Exceptions:** <unreconciled or unsupported amounts, or omit when none>
```

## Reference files

- [reference/reconciling-items.md](reference/reconciling-items.md): the three-bucket
  classification with expected resolutions and aging rules.
