---
name: revenue-recognition
description: Revenue recognition under ASC 606 for subscription and services contracts, reasoned from the contract documents. Use to set a client's revenue policy, analyze a new or nonstandard contract, account for a modification, run the monthly revenue roll, or answer how an arrangement is recognized.
argument-hint: "[client, contract, or the question]"
---

# Revenue

Plugin root: the folder three levels above this file, which is
`<plugin root>/skills/technical-accounting/revenue-recognition/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

Decide how a contract's revenue is recognized by asking what the customer is buying and
when they get it. Then turn the decision into a contract file the close kit can schedule.
The artifacts are a position memo per judgment, a contract file per contract, and a
revenue schedule that ties to the ledger. The close's `adjust` phase consumes the
schedule. This skill makes the accounting call. `adjust` books it.

## Non-negotiables

Start every run with a todo list whose first item is to read the five questions and the
situation principles below. Open each principle's leaf file before applying it. The memo
names each principle that shaped a conclusion and the choice it changed.

- **The contract is the evidence.** Read the order form, MSA, amendments, SOWs, side
  letters, and emails before reasoning. If a document answers a question, it is not the
  user's question. The client's current booking is a claim to test. Precedent counts
  only when a policy memo backs it.
- **Name the deciding fact.** Every conclusion points to the clause, data point, or
  message that decides it, quoted with its file. A conclusion with no deciding fact is a
  guess. When the deciding fact is missing, that fact is the question to ask.
- **Argue the alternative.** Every judgment names at least one treatment you rejected and
  the fact that rejects it. If no fact separates two treatments, the judgment is open, and
  the memo says so with both treatments' numbers.
- **Reason, then check the pattern.** Work the five questions below from the facts first.
  Only then walk [reference/reading-list.md](reference/reading-list.md) for terms you
  missed. A template consulted first becomes the answer.
- **The kit does the arithmetic.** Allocations, schedules, catch-ups, and balances come
  from `closekit rev` over a contract file
  (`python3 <plugin root>/scripts/closekit.py rev --help`). The memo shows the command
  and its output.
- **Cite only what is verified.** Codification references come from
  [reference/codification.md](reference/codification.md). A paragraph that isn't there
  gets named by topic, not by a number from memory.
- **Elections belong to the client.** Practical expedients and policy choices (portfolio
  approach, the one-year commission expedient, the right-to-invoice expedient, the
  financing expedient, the monthly or daily convention) are recorded in the profile once,
  with the user's approval. A run without one proposes it as an open question.
- **Second review follows the profile.** The profile's `Second review` line decides which
  conclusions go to the `better-accountant:revenue-challenger` agent before the user sees them. A
  conclusion is *material* when it, or its correction to what was booked, is above
  materiality, and *contested* when two supported treatments remain.
  - `material or contested` (the default when the profile is silent): either one.
  - `every judgment`: every conclusion that needed reasoning beyond the stream policy.
  - `contested only`: contested conclusions, whatever their size.

  A conclusion the setting leaves out gets "not run" and the reason in its memo.

## The five questions

Every question applies one idea: revenue follows control of what was promised, in the
amount the entity expects to keep. Invoices and cash are evidence about that, never the
event ([principles/revenue-follows-control.md](principles/revenue-follows-control.md)).
Ask the questions in order, for every contract. Standard contracts on an approved stream
policy answer most of them by reference. Only the deviations need fresh reasoning.

1. **What is enforceable, and for how long?** Parties, approval, payment terms,
   collectibility, and the term each side can actually enforce. Termination rights, side
   letters, and contracts signed together can change the contract you are accounting for.
   ([principles/enforceable-rights-set-the-contract.md](principles/enforceable-rights-set-the-contract.md))
2. **What is the customer buying?** Separate the promises the customer can benefit from
   on their own, and that are separable in this contract, from the setup work the entity
   must do to deliver them. Subscriptions are usually one series of identical periods.
   Options priced below what others pay are promises too.
   ([principles/find-what-the-customer-is-buying.md](principles/find-what-the-customer-is-buying.md),
   [principles/options-can-be-promises.md](principles/options-can-be-promises.md))
3. **How much does the entity expect to keep?** Fixed fees, plus variable amounts
   (usage, credits, rebates, bonuses, refunds) estimated and constrained. Adjust for
   financing and for amounts paid back to the customer.
   ([principles/price-is-what-you-expect-to-keep.md](principles/price-is-what-you-expect-to-keep.md))
4. **Which promise earns which dollars?** Allocate by standalone selling price, unless a
   variable amount belongs to one promise or one period alone.
   ([principles/allocate-by-standalone-value.md](principles/allocate-by-standalone-value.md))
5. **When does the customer get it?** Over time or at a point, and for over-time
   promises, the measure that tracks what the customer receives.
   ([principles/pattern-follows-the-customers-benefit.md](principles/pattern-follows-the-customers-benefit.md))

## Situation principles

Open the leaf when its situation is in the contract.

- **Who controls before transfer**
  ([principles/who-controls-before-transfer.md](principles/who-controls-before-transfer.md)).
  A reseller, marketplace, or subcontractor sits in the chain.
- **Modifications change the future**
  ([principles/modifications-change-the-future.md](principles/modifications-change-the-future.md)).
  Scope or price changed after inception, or an estimate moved.
- **Costs follow the revenue**
  ([principles/costs-follow-the-revenue.md](principles/costs-follow-the-revenue.md)).
  Commissions or other costs of winning or fulfilling the contract.
- **Balances net per contract**
  ([principles/balances-net-per-contract.md](principles/balances-net-per-contract.md)).
  Every period end.

## Playbooks

Match the task to a playbook, open it, and copy its steps into your todo list word for
word before reasoning about the task. A step you choose not to do stays on the list as
`skip: <reason>`.

- **Policy setup.** First revenue work for a client, a new revenue stream, or a client
  moving off a billing-based deferred revenue spreadsheet.
  [playbooks/policy-setup.md](playbooks/policy-setup.md)
- **Contract.** A new contract, or an existing one never analyzed, that deviates from its
  stream policy or has no policy to follow.
  [playbooks/contract.md](playbooks/contract.md)
- **Modification.** An amendment, add-on, downgrade, early renewal, concession, or
  anything else that changes scope or price after inception.
  [playbooks/modification.md](playbooks/modification.md)
- **Period roll.** The monthly revenue schedule, balances, and entries for a close, run
  from the `adjust` phase or on its own.
  [playbooks/period-roll.md](playbooks/period-roll.md)
- **Question.** "How should we account for X?" with no close attached. Run the Contract
  playbook's reasoning steps, and deliver the memo without contract files or entries.

## When to ask vs proceed

**How to ask.** Every question to the user goes through the AskUserQuestion tool as
multiple choice, never as a question in prose. Each gets two to four options, the
recommended one first and marked "(Recommended)", each described by what it changes,
with the figure where there is one. Follow `<plugin root>/skills/financial-close/close/reference/asking.md` for batching,
approvals, and what to do when the tool is unavailable.

- **Fact.** A document or data file settles it. Read it. Never ask.
- **Policy.** An approved stream policy or profile election settles it. Apply it and cite
  it.
- **Judgment with a deciding fact in hand.** Conclude, show the rejected alternative, and
  send it for second review when the profile's setting calls for it.
- **Judgment missing its deciding fact.** Ask for exactly that fact. Name the document
  that would hold it and what each answer would change. "What is your SSP for add-on
  seats?" beats "how should we treat this amendment?"

Batch questions at the end of a playbook, one list. Write each down in the close log
(`question` event) or the memo the moment it is queued. Running unattended, record every
open judgment as an exception with both treatments and their numbers, and book neither.

## Gates

- **Position approval.** A memo's conclusion becomes the treatment only when the user
  approves it. Record it with `closekit log <log> revenue approve "<contract id>: <memo
  title>" "<who>" "<memo path>"`. An unapproved position may be scheduled for review, but
  no entry from it enters an import CSV.
- **Policy changes.** Moving a stream to a new policy, or correcting what the client
  booked in a prior period, is its own approval. It carries the cumulative effect as a
  figure and says whether the correction is an error in a prior period. Materiality
  decides whether that correction needs restatement discussion with the user.
- **Entries.** Revenue entries go through the journal-entry skill's contract and the close's approval
  gate like any other entry.

## Guardrails

- A contract that deviates from its stream policy goes through the Contract or
  Modification playbook before anything is scheduled or booked for it.
- Out of scope: tax basis revenue (IRC section 451), industry guidance for construction
  loss contracts, and public-company disclosure. Say so when they appear, and name who
  owns them.
- The conclusion follows the facts wherever the client's current booking stands. When
  the booking is wrong, the memo says so and quantifies the correction.

## Deliverable

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

Every playbook's reply ends with this block:

```markdown
### Revenue: <client>, <scope>

**Conclusion:** <treatment per contract or stream, one line each>
**Deciding facts:** <fact, document>, one per conclusion
**Rejected:** <alternative, and the fact that rejects it>
**Numbers:** <period revenue, balances; kit command that produced them>
**Changes to what was booked:** <cumulative through the period, from `rev balances` with `booked` filled in, or none>
**Open:** <questions with the fact each needs, or none>
**Challenger:** <agreed / disagreed on X, resolved how / not run under the second-review setting>
```

## Reference files

- [reference/contract-file.md](reference/contract-file.md): the contract file the kit
  reads, and how each judgment maps onto it.
- [reference/position-memo.md](reference/position-memo.md): the memo format.
- [reference/reading-list.md](reference/reading-list.md): contract terms that change the
  answer, and the principle each one tests.
- [reference/codification.md](reference/codification.md): verified ASC 606 and 340-40
  references. Cite from here only.
