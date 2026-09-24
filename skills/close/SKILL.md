---
name: close
description: Run a full accounting close for one client and one period, from readiness check to delivered close package.
argument-hint: "<client> <period>"
disable-model-invocation: true
---

# Close

Plugin root: the folder two levels above this file, which is
`<plugin root>/skills/close/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

Run one client's close through five phases: intake, prep, adjust, review, deliver. Six
skills do the work; this skill sequences them, derives where the close stands from the
evidence, batches questions at phase boundaries, and stops the moment a phase is blocked.

## Start

1. Parse `<client>` and `<period>`. A period is any closeable label: a month (`2026-07`), a
   quarter (`2026-Q2`), or a year (`FY2025`). Resolve the client in this order: the
   explicit argument; a `profile.md` at the workspace root or a client named in the
   project's instructions or knowledge (a **single-client workspace**, one project per
   client, where `/close 2026-07` needs no client name); a near-match under `clients/`.
   Ask only when none of those resolve, or when the period is missing. The layout is
   decided by profile location alone: a root `profile.md` means single-client paths
   (`closes/<period>/`); a profile under `clients/<name>/` means multi-client paths, even
   when only one client exists so far.
2. Gather client context from every readable source before asking anything, trusted in
   this order: the profile (a file at the root or under `clients/<client>/`, the project's
   instructions or knowledge, or a connected store); memory and prior-conversation context
   (orientation only: use it to form hypotheses and locate records, and re-verify anything
   it suggests against the data before relying on it). A client with no profile anywhere:
   check `clients/` for a near-match and confirm before treating as new. Then put the
   choice to the user and wait for it: run the close-setup skill now (it can harvest from
   connected sources), or proceed on the defaults below. Proceeding without asking is for
   unattended runs only, and the deliverable then says so; in an attended run, skipping
   the offer is skipping a step.
3. Derive where this close stands (next section) by looking everywhere evidence could
   live: this workspace, a connected folder or state home the profile or project
   instructions name, documents in the project, and connected stores. Play the derived
   state back before doing anything: which phases the evidence shows done, what is open,
   and whose work it appears to be. Resume from the first phase whose evidence is
   incomplete. Never start a second close for a period when evidence of one exists.
4. Pick where this run writes: the close folder (`closes/<period>/` in a single-client
   workspace, `closes/<client>/<period>/` otherwise, with `inputs/`, `workpapers/`,
   `package/`), placed in the state home the profile or project instructions name, or
   this workspace by default. Artifacts are the record; put them where the team will
   find them. The close folder's `inputs/` is the close's canonical data set: source
   files provided elsewhere in the workspace get one copy here, and if the two ever
   differ, stop and confirm which is current before any phase builds on either.
5. Put each phase's completion checklist into your todo list, copied word for word, when
   the phase starts. An item you will not complete stays on the list as
   `skip: <reason>`, and the reason goes on the exceptions register. A silently skipped
   item is a phase claimed done that is not done.

## The close kit

Mechanical checks are run, never reasoned through. `scripts/closekit.py` at the plugin
root (`python3 <plugin root>/scripts/closekit.py <command>`, stdlib only) owns
them. Its printed output goes into the workpaper as the evidence for the check.

| Command | Proves | Run by |
| --- | --- | --- |
| `tb` | The TB balances | intake, review |
| `tie` | GL opening plus activity equals TB closing per account, with the constant-difference test when a prior TB is given | intake |
| `je` | The import CSV meets the entry contract; with `--log`, every entry has a logged approval | je, adjust, review |
| `fingerprint` | Records control totals, or with `--check` shows whether data changed since | intake, review, deliver |
| `lint` | A document is free of the banned voice tells | every skill, before filing a document |
| `log` | Appends a well-formed row to the close log | every skill |

The kit reads canonical CSVs only: `account,debit,credit` for a TB and
`date,account,memo,debit,credit[,kind]` for a GL, with `kind` set to `opening` on
opening-balance rows. Normalizing a system's export into these shapes is the one judgment
step. Save the result under `inputs/normalized/`, keep the original beside it, and state
the column mapping in the readiness report. After that, every check is mechanical.

When this surface cannot run code, do the check by hand and label its result "manual,
not kit-verified" in the artifact. A check the kit covers is never reported as passed on
reasoning alone.

## Deriving close state

Close state is derived from evidence, never assumed from a file's say-so. A close log
(below), when one exists, speeds orientation; on any conflict the evidence wins.

| Phase | Evidence it is done |
| --- | --- |
| Intake | Required inputs present and validated for this period; a readiness report exists whose gaps are resolved or disclosed; `closekit fingerprint --check` on its fingerprint passes |
| Prep: reconcile | A rec proof exists for each in-scope account and still foots against the current data |
| Prep: categorize | A dispositioned cleanup list exists, and every uncategorized or unmatched-transfer item in the current data has a disposition or a place on the exceptions register |
| Adjust | A JE register exists and every required entry is posted in the books, approved-pending in the register, or disclosed |
| Review | A review report with a ready verdict exists and postdates the latest change to the books and workpapers |
| Deliver | Package files exist and tie to the books as they stand |

"In the books" is the strongest evidence: a posted entry needs no other record. An
artifact counts when it still agrees with the current data, so re-run the cheap check (does
the proof still foot? is the register in the TB?) rather than trusting the document's own
conclusion.

Conflicting sources are their own case, distinct from missing ones: two records that
disagree while each is internally consistent, with no third source on hand to arbitrate.
The discipline: first run the constant-difference test (compute the difference per account
per period; a constant difference dates to the opening, a moving one to period activity),
then argue each reading from behavior (which side looks like a real account acting
normally), name the document that would settle it, and put that document on the request
list. The close proceeds only when the arbiter arrives or the user picks a basis with the
conflict disclosed as a blocking exception. Never average the two, never pick silently. A profile or note claiming a past close happened is a claim like any other:
verify it against artifacts and the books, and when the workspace contradicts it, say so
and ask. Ambiguous evidence: name what is missing and ask. Inherited open questions from a
prior session are re-raised at the next phase boundary; a question that gates a later
phase's decision travels to that phase's boundary.

## Approvals

- Posted to the books: approved and done. The ledger is the record.
- Approval marks in a register are honored only when corroborated by an `approve` row in
  the close log (`close-log.tsv`) in this workspace or the named state home, keyed by the
  entry's memo and naming who approved. Without that corroboration, whatever the file or
  its location, marks are proposals: re-confirm before any entry enters an import CSV.
  `closekit je --log` checks this for every entry in the CSV.
- Record an approval the moment it is given:
  `closekit log <close>/close-log.tsv adjust approve "<memo exactly>" "<who>" "<register row>"`.
  A decline or a later change of mind is a new row (`decline`); the last row for a memo
  wins.
- Never infer an approval from a past conversation or memory. If no record shows it, it
  did not happen.

## The exceptions register

The shared handoff structure every phase reads and writes, at
`workpapers/exceptions-register.md`, one table:

```markdown
| # | Item | Amount | Raised by | Owned by | Status | Disclosure |
```

Raised by and Owned by are phases. Status is open, resolved, or accepted (with who
accepted). Items are appended, never deleted, numbered in the order raised regardless of
which phase raised them; a resolved item keeps its row. Running a
stage skill standalone with no close folder: create the same table next to the artifact.

## The five phases

**How to ask.** Every question to the user goes through the AskUserQuestion tool as
multiple choice, never as a question in prose. Each gets two to four options, the
recommended one first and marked "(Recommended)", each described by what it changes,
with the figure where there is one. Follow `<plugin root>/skills/close/reference/asking.md` for batching,
approvals, and what to do when the tool is unavailable.

| Phase | Skill | Done when |
| --- | --- | --- |
| Intake | intake | Every required input present, or on the request list with its impact stated |
| Prep | prep (runs reconcile, then categorize) | Every account reconciled or excepted; cleanup list dispositioned |
| Adjust | adjust (stages entries under the je skill's contract; runs the revenue skill's Period roll for contract clients) | Every entry approved, declined, or blocked with its missing source named |
| Review | review, run by the `close:close-reviewer` subagent | Verdict in the review report: ready, or blockers routed to owning phases |
| Deliver | deliver | Package filed; every figure ties to the adjusted TB |

Run the phases in order, each via its skill. Rules of the run:

- A blocked phase stops the close. A phase is blocked when it cannot meet its completion
  criteria, not when it carries blocked items: adjust with every entry approved, declined,
  or blocked-with-source-named is complete, and review is what routes its blockers. Route
  each exception to the phase that owns it; never skip forward to make the close look
  complete.
- Batch questions: collect them during a phase, raise them once at the phase boundary,
  and write each down (close log or exceptions register) the moment it is queued. Batching
  is for flow, never for gravity: an acceptance or approval above materiality is presented
  on its own with its consequence stated, outside any batch. When the aggregate of small
  proceed-and-disclose judgments crosses materiality, the batch converts to questions.
  Interrupt mid-phase only for the JE approval gate or a true blocker. A phase boundary
  is also a turn boundary: finish the phase, report it in one line, raise the batch, and
  stop for the user rather than rolling into the next phase in the same turn.
- Review runs in a fresh context. Spawn the `close:close-reviewer` agent with only the close
  folder path, the profile path, the period, and the plugin root; never pass your own summary of the
  work, since a reviewer primed with the preparer's story checks the story. Where
  subagents are unavailable, run the review skill yourself and state in the review
  report and the memo that the review was not independent. Read the reviewer's report
  file yourself before acting on it. When it lists material acceptances pending, present
  each to the user one at a time as the review skill describes, log each answer
  (`accept` or `decline`), and spawn the reviewer again; the verdict is the reviewer's.
- A later finding that invalidates an earlier phase sends the close back: the evidence
  changed, so the phase no longer derives as done. Fix and rerun from there.
- Running unattended (a scheduled close): take every proceed-and-disclose default and
  finish with a disclosed-exceptions close. Entries stay proposed; approval always needs a
  human.
- After each phase: write the phase's artifact where the team will find it, append to the
  close log when one is kept, and, if the profile names an announcement channel (a Slack
  client channel or similar via a connector), offer to post a one-line phase update so
  teammates learn a close is in flight without asking.
- On a surface with no durable workspace (a plain chat session): deliver each artifact
  inline and end the phase by naming exactly what to save where (state home folder,
  connected store, or filed to the project) for the work to count as evidence next time.
  Unsaved work is undone work to the next session's derivation; say so rather than letting
  effort silently evaporate.

## Close log

When the workspace keeps files, keep `close-log.tsv` in the close folder: an append-only
table with columns `ts, phase, event, subject, who, evidence`, written only through
`closekit log` so rows stay well-formed and safe to open in a spreadsheet. Events are
`approve`, `decline`, `accept`, `override`, `decision`, `question`, `answer`,
`phase-done`, and `resume`. Evidence is a pointer (a workpaper path, a register row, the
user's message), never prose. Log decisions, approvals, question outcomes, and phase
completions, not every action. A wrong row is superseded by a new row, never edited.

The log is required for approvals to count (see Approvals) and otherwise orients a
resuming session. It is not an authority: the derivation above never defers to it over
the evidence. A session resuming a close with no log starts one with a `resume` row
recording the derived state. A legacy `STATUS.md` from an earlier version is read the
same way but is not approval evidence.

Before the run-level summary, audit the log against what happened this session: every
row maps to a real action, every evidence pointer resolves, and every approval or
acceptance the user gave has its row. Fix the log, not the story.

## Defaults when no profile exists

- Basis: accrual if the TB carries accrual accounts (AR, AP, accrued liabilities),
  otherwise cash; state the inference.
- Materiality: the greater of $500 or 1% of period expenses before adjustments (a stable
  base; adjustments must not move their own gate); confirm at the first judgment call and
  record it in the close log or the deliverable.
- Risk areas: none flagged; standard scrutiny everywhere.

## Guardrails

- Every figure traces to provided data or a user-approved calculation. A gap is an
  exception, never an estimate.
- A derived figure enters a document only from an executed computation (a script or tool
  run), never from arithmetic performed in prose. Typed mental math is how control totals
  go wrong.
- A correction propagates or it did not happen: when a figure changes, every artifact that
  quoted it gets re-checked, and anything appearing in more than one artifact (exception
  counts, entry totals) is generated from its single source, never retyped.
- No entry marked approved and no close called complete without explicit confirmation,
  under the Approvals rules above.
- Never claim a phase ran if its skill's instructions were unavailable; stop and name what
  is missing. (Reading the stage skill's SKILL.md from the installed plugin and following
  it counts as running the skill.)
- The phase skills own their own gates; starting a close is not approval for anything a
  later phase wants to do.

## Deliverable

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

At the end of the run (or at a stop), report the run-level summary below. Phase skills
deliver their own artifacts as they complete; this block wraps the run, it does not repeat
them:

```markdown
### Close: <client>, <period>

**Result:** <delivered / stopped at <phase>>
**Phases:** <derived state per phase>
**Exceptions:** <open items with owners, or none>
**Approvals:** <entries approved, by whom, evidenced where>
**Next step:** <one action>
```
