---
name: categorize
description: Transaction review and cleanup for a period. Use when sweeping uncategorized or miscoded transactions, matching transfers between accounts, or hunting duplicates before a close.
---

# Categorize

Plugin root: the folder two levels above this file, which is
`<plugin root>/skills/categorize/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

Sweep the period's transactions so every one sits in the right account exactly once. The
artifact is a cleanup list: proposed recategorizations, matched transfers, and suspected
duplicates, each waiting on the user's approval. Nothing is fixed silently.

## Inputs

- GL detail export for the period
- The client profile (`clients/<client>/profile.md`, or `profile.md` at the root in a
  single-client workspace) for materiality, risk areas, and known category conventions,
  when it exists
- Prior-period GL detail when available (precedent for how this client codes things)

Inside a close, take scope from the close context (the readiness report and profile, plus
the close log when one is kept) and write the cleanup list to the close folder's
`workpapers/`. Standalone, sweep whatever export the user provides.

## Workflow

1. Uncategorized sweep: list every transaction in a suspense, uncategorized, or
   ask-my-accountant account. Propose a category for each, sourced from this client's own
   precedent (same vendor, same amount pattern in prior periods) before any generic rule.
   One rule for the no-precedent case: below materiality with an unambiguous description
   (a known vendor whose category is obvious), propose it marked low-confidence and let
   batch approval handle it; ambiguous, or above materiality, it goes to the question queue.
2. Miscoding scan: for each expense and income account, flag transactions that break the
   account's own pattern: a vendor that always posts elsewhere, an amount an order of
   magnitude off the account's normal range, personal-looking spend in business accounts.
   Profile-flagged risk areas get a line-by-line read, not a sampling.
3. Transfer matching: pair each transfer-out with its transfer-in across accounts, amounts
   equal and dates within a few business days. Both legs must exist and both must be coded
   as transfers, not income or expense. An unmatched leg is an exception with a proposed
   resolution.
4. Duplicate detection: same vendor, same amount, dates within a few days of each other.
   Show every candidate pair side by side with full detail. Never resolve a duplicate
   yourself; the user says which record survives.
5. Assemble the cleanup list (format below), get the user's approval item by item or as a
   batch, and record the decisions. Approved fixes become either a recategorization list
   (when the user has a live system to re-code transactions in directly) or entries routed
   to the adjust skill when a journal entry is the only way to move the amount;
   in a file-only workspace with no live system, a journal entry is always the way.
6. The dispositioned cleanup list in `workpapers/` is the record; record every item this
   phase questioned or dispositioned on the exceptions register too, so the adjustments
   phase's completeness scan builds on it instead of re-asking the same question. Append
   the outcome to the close log when one is kept.

## Degradation

| Missing input | Fallback |
| --- | --- |
| Prior-period GL | No precedent available; apply the no-precedent rule from workflow step 1 (low-confidence proposals below materiality, questions above) |
| Vendor or memo fields | Match on amount and date only; raise the duplicate threshold to exact-amount matches |
| Client profile | Use the default materiality from the close and treat no account as a flagged risk area |

## When to ask vs proceed

**How to ask.** Every question to the user goes through the AskUserQuestion tool as
multiple choice, never as a question in prose. Each gets two to four options, the
recommended one first and marked "(Recommended)", each described by what it changes,
with the figure where there is one. Follow `<plugin root>/skills/close/reference/asking.md` for batching,
approvals, and what to do when the tool is unavailable.

- Fact: the data can settle it. Derive it; never ask.
- Precedent: this client's prior coding settles it. Follow the precedent and note it.
- Judgment: more than one defensible category. Below materiality, propose the conservative
  one and disclose. Above materiality, or in a profile-flagged risk area, queue a question.

Two hard rules on the queue. Write a question down (close log or exceptions register)
the moment it is queued; a question held only in working memory is a question that will be
silently answered. And track the running total of proceed-and-disclose judgments: the
moment their aggregate crosses materiality, stop treating them as individually small,
convert the open ones to questions, and say the aggregate out loud. Twenty immaterial
guesses are one material guess.

Queue questions and raise them once, with the assembled cleanup list. Running unattended,
leave unresolved proposals as disclosed exceptions; never auto-approve your own proposals.

## Anti-patterns

- **The confident guess.** A category proposed from a vague memo reads as authoritative. The
  tell: a proposal with no precedent citation. Every proposal names its source: precedent,
  vendor default, or judgment.
- **Transfer income.** A transfer-in coded as revenue inflates the P&L. The tell: an income
  transaction whose counterparty is the client's own account. Both legs of a transfer are
  transfers.

## Completion criteria

Cleanup is done when every box below is checkable:

- [ ] Zero transactions remain uncategorized without either an approved category or a place
      on the exceptions register
- [ ] Every flagged miscoding is approved, declined by the user, or on the register
- [ ] Every transfer leg is matched, or its missing counterpart is on the register with a
      proposed resolution
- [ ] Every duplicate candidate was shown side by side and dispositioned by the user

## Guardrails

- Propose, never apply. The user approves each fix; unapproved proposals die with the run.
- Duplicates are dispositioned by the user only, with both records shown in full.
- Recategorizations above materiality are itemized individually; batch approval is for the
  small stuff.

## Deliverable

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

```markdown
### Cleanup list: <client>, <period>

**Uncategorized (<n>):** <txn, amount, proposed category, source: precedent/default/judgment>
**Suspected miscodings (<n>):** <txn, current account, proposed account, why>
**Transfers:** <matched pairs count; unmatched legs listed with proposed resolution>
**Duplicate candidates (<n>):** <each pair side by side>
**Approved / declined / open:** <counts, and where approved fixes went>
```
