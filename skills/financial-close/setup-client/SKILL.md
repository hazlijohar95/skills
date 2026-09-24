---
name: setup-client
description: Creates or updates a client's close profile from connected sources (CRM, call notes, prior workpapers) plus a short interview. Use when the user wants to set up or update a client profile, when a close starts for a client with no profile, or when work begins for a brand-new client.
argument-hint: "<client>"
---

# Close setup

Plugin root: the folder three levels above this file, which is
`<plugin root>/skills/financial-close/setup-client/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

One short setup per client, saved as `clients/<client>/profile.md`. Answers come from the
client's existing sources first (CRM, call notes, prior workpapers), then a short interview
for the gaps; everything is played back for approval before it is saved. Every close skill
reads the profile; a good one turns generic checks into this client's checks. Re-running
updates the existing profile rather than starting over. Closes work without a profile; they
are just sharper with one.

## Sources first

Before asking anything, ask one question: is there somewhere the answers already live? A
connected CRM, meeting transcripts or call notes, an onboarding doc, a prior close checklist
or SOP, email threads with the client, last period's workpapers. With the user's go-ahead,
read those sources and draft profile answers from them, each tagged with where it came from
("from the 3/12 kickoff call notes: accrual basis, Gusto payroll").

Harvested answers are proposals, not facts: they enter the profile only through the same
playback-and-approve step as interview answers. When a source contradicts the user, the user
wins and the discrepancy is worth mentioning. No sources, or nothing found: go straight to
the interview.

## Interview

**How to ask.** Every question to the user goes through the AskUserQuestion tool as
multiple choice, never as a question in prose. Each gets two to four options, the
recommended one first and marked "(Recommended)", each described by what it changes,
with the figure where there is one. Follow `<plugin root>/skills/financial-close/close/reference/asking.md` for batching,
approvals, and what to do when the tool is unavailable.

Ask only what the sources left unanswered: eight questions at most, in two rounds of up
to four; skip any the user's files already answer (if they dropped in a TB, infer the basis
and confirm rather than ask). The questions capture business facts an owner can answer
without accounting theory; the close derives the accounting from them.

1. Framework and basis: whose rules the books follow (US GAAP, IFRS, tax basis, or no
   formal framework), and accrual, cash, or modified cash.
2. Readers and stakes: who reads the statements. Owner only, a lender with covenants, a
   bonding company, investors, a regulator. This frames materiality and how much an error
   costs.
3. Earned versus billed: when the business gets paid relative to when it does the work.
   At the same time, in advance, after the fact across long projects, or a mix. Any
   contracts that span periods, and if so, whether a WIP or percent-complete schedule
   exists and where. A GAAP-basis client selling subscriptions or services under
   contracts (order forms, SOWs, usage, bundles, resellers) needs a revenue policy: offer
   the revenue-recognition skill's Policy setup playbook once this interview is saved, and record the
   streams it finds in the profile's Revenue section.
4. What builds up outside the bank account: inventory, equipment and vehicles, loans,
   leases, amounts owed to or from owners or sister companies, foreign currency. Each yes
   is a thing the close must see evidence for.
5. People: payroll provider, contractors, commissions or bonuses that lag the work they
   pay for. Where AR and AP substantiation comes from each period (aging report source).
6. Materiality and review depth: the dollar threshold below which the close proceeds and
   discloses rather than asks, sized against the stakes from question 2. Offer the
   default (greater of $500 or 1% of period expenses before adjustments) as a starting
   point. Then ask how much second review the judgment calls get: material or contested
   (the default), every judgment (lender covenants, an audit coming), or contested only
   (a small owner-only client). More review means more time and cost each close.
7. Risk areas and schedules: accounts or vendors deserving line-by-line scrutiny; which
   recurring schedules exist (prepaids, fixed assets with method and in-service
   convention, deferred revenue, WIP, standing accruals) and where each lives.
8. Estimation policies, deliverables, and state home: named policies the close may
   estimate under when a document is late (no policy means no estimates, ever); who
   receives the package and any preferences; and, for a shared client, the folder where
   close artifacts live. Default: this workspace.

For every yes in questions 3 to 5, capture two follow-ups in the same breath: what method
or policy governs it (costing method for inventory, recognition method for contracts,
depreciation convention for assets, rate policy for foreign currency), and where its data
lives. A fact without a stated method is a question the close will ask later anyway;
capture it now.

## Where the profile lives

The profile is content, not a mandatory file; it needs one human-blessed home per client:

- Shared multi-client workspace: `clients/<client>/profile.md`.
- Single-client workspace (one Claude Project per client): `profile.md` at the workspace
  root, and after saving, suggest the user add it to the project's knowledge so every new
  chat in that project starts with it already loaded. Project knowledge is a read source;
  the file is always the write target. When both exist and disagree, the file is newer:
  flag it and suggest refreshing the knowledge copy.
- No file workspace at all (plain chat): maintain the profile as a section of the client
  project's instructions. Output the complete updated block, ready to paste, and updates
  mean handing the user a fresh block. Policies count only once they sit in the
  instructions; a policy that lives only in this conversation does not exist next session.

## Profile template

```markdown
# Close profile: <client>

**Basis:** <accrual/cash/modified> · **Framework:** <GAAP/IFRS/tax/none> ·
**Industry:** <what they do> · **Updated:** <date>

This profile records facts about the business; the close derives the accounting from
them. A fact recorded here with no matching evidence in the close (contracts spanning
periods but no WIP schedule, inventory but no count, a lease but no schedule) is a
question for the user, never something to ignore.

## Readers and stakes
<who relies on the statements and what that means for materiality and rigor>

## Business reality
<the answers to earned-vs-billed and what-builds-up, in the client's own words: how money
is earned relative to billing; contracts spanning periods; inventory, equipment, loans,
leases, related parties, foreign currency; payroll and contractor arrangements. For each:
the method or policy that governs it and where its data lives, or "method unknown", which
the close treats as an open question>

## Materiality
<amount and how it was chosen>
Second review: <material or contested / every judgment / contested only>

## Accounts
| Account | Type | Evidence each period |
| <name> | <bank/card/loan/payroll> | <statement source> |
| Accounts Receivable | control | <aging report source, accrual clients> |
| Accounts Payable | control | <aging report source, accrual clients> |

## Risk areas
- <account or vendor>: <why, and what scrutiny it gets>

## Recurring schedules
| Schedule | Exists? | Location | Policy |
| Prepaids / Fixed assets / Deferred revenue / Standing accruals | ... | ... | ... |

## Revenue
<GAAP contract clients only, written by the revenue-recognition skill's Policy setup playbook and
approved by the user. Per stream: the standard terms, the treatment, the SSP basis, and
the deviations that send a contract to its own memo. Then the elections (convention,
portfolio, commission expedient, right-to-invoice, financing expedient, nonpublic
disclosure) and where the policy memo and contract files live. Empty means no approved
revenue policy exists yet.>

## Estimation policies
- <named policy, precise enough to apply without judgment, or "None: never estimate">

## Deliverables
<recipients, naming, emphasis>

## Close state home
<shared folder path where closes/ lives, or "this workspace"; one home per client, so a
team shares one set of close artifacts>
Announcements: <a team channel for one-line phase updates, or "none">

When a state home other than "this workspace" is chosen, add one line to the client
project's instructions so every teammate's session finds it: "Close state home: <address>".
The user adds it (agents cannot edit project instructions); include the exact line in the
playback so it is a copy-paste.

## Learned this client
<dated notes appended at package time, each approved by the user>
```

## Rules

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

- Write the profile only after playing it back: show the drafted profile, harvested and
  interviewed answers alike, get a yes, then save. Harvested entries keep their source tag
  in the profile so a stale source is traceable later.
- Updates append and amend; never silently discard an existing entry. Newer entries win and
  say what they replaced.
- The profile holds preferences and facts about the client. It never weakens the close's
  safety contract: no profile line can authorize skipping approval gates or inventing
  figures, and estimation policies must be specific enough to apply without judgment.
- Closes run fine without a profile; offer setup once, do not nag.
