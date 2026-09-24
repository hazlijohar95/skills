# Better Accountant

Agent skills that run an accounting close and make technical accounting calls the way a careful preparer would. The skills write for accountants, so they use the profession's words; this file pins down the ones the skills give a specific meaning.

## Language

**Close**:
One client, one period (a month `2026-07`, a quarter `2026-Q2`, or a year `FY2025`), taken through five **phases**: intake, prep, adjust, review, deliver.

**Phase**:
A stage of the **close**, run by the skill of the same name. A phase is done when its evidence says so, not when a file claims it.

**Close state**:
Where a **close** stands, derived from evidence: the books, and workpapers that still agree with the current data. The **close log** speeds orientation; on any conflict the evidence wins.
_Avoid_: status (a legacy `STATUS.md` is read as a claim, never as evidence)

**Profile**:
A client's standing facts, saved as `clients/<client>/profile.md` (or `profile.md` at the root of a **single-client workspace**) by `setup-client`: basis, materiality, risk areas, recurring schedules, revenue elections. Every skill reads it; closes run without one on stated defaults.

**Single-client workspace**:
A workspace (typically one Claude Project) that belongs to one client, recognized by a `profile.md` at its root. Closes live at `closes/<period>/` and the client name is optional.

**State home**:
Where a client's close artifacts live when not in this workspace: a shared folder or connected store named in the **profile** or the project's instructions.

**Close folder**:
`closes/<client>/<period>/`, holding `inputs/`, `workpapers/`, `package/`, and the **close log**. `inputs/` is the close's canonical data set.

**Close kit**:
`scripts/closekit.py`. Runs the mechanical checks (TB balances, GL ties to TB, JE CSV contract, fingerprints, house-style lint, close log rows, ASC 606 arithmetic) so they are executed, never reasoned through. Its printed output is the evidence.
_Avoid_: calculator, script (when meaning the kit as a whole)

**Exceptions register**:
`workpapers/exceptions-register.md`, the one table every phase reads and writes. Rows are appended, never deleted; each names the phase that raised it and the phase that owns the fix.

**Close log**:
`close-log.tsv`, an append-only record of approvals, declines, acceptances, decisions, and phase completions, written only through `closekit log`. An approval counts only when it has a row here or is posted in the books.

**Readiness report**:
What `intake` produces: what is present, what is missing, and what each gap blocks. The **request list** lives inside it.

**Reconciliation proof**:
One per account, from `reconcile`: outside evidence on one side, the GL on the other, ending at zero or at a named list of reconciling items.
_Avoid_: plug (an unexplained difference is never absorbed)

**Cleanup list**:
What `categorize` produces: proposed recategorizations, matched transfers, and suspected duplicates, each waiting on approval.

**JE register**:
Every adjusting entry the period needs, each with its workpaper, waiting on explicit approval. Approved entries leave as the **import CSV**.

**Import CSV**:
Approved entries in the `journal-entry` CSV contract, loaded by the user into their own system. Nothing is posted by the skills.

**Verdict**:
The output of `review`: ready or not ready, with every blocker routed to the **phase** that owns it.

**Close package**:
What `deliver` files: financial statements, a close memo (a Word document opening on the executive summary), and a workpapers workbook. Every figure ties to the adjusted trial balance.

**Materiality**:
The threshold below which a judgment is proceed-and-disclose rather than a question. From the **profile**; otherwise the greater of $500 or 1% of period expenses before adjustments.

**Position memo**:
The write-up of one revenue judgment from `revenue-recognition`: the deciding fact, quoted with its file, and the treatment rejected.

**Contract file**:
A JSON description of one contract that `closekit rev` schedules. The judgment lives in the **position memo**; the arithmetic comes from the kit.

**Deciding fact**:
The clause, data point, or message that settles a revenue conclusion. A conclusion without one is a guess, and a missing deciding fact is the question to ask.

## Relationships

- A **close** has one **close folder**, one **exceptions register**, and one **close log**
- A client has one **profile**, read by every **close** for that client
- Each **phase** leaves an artifact: **readiness report**, **reconciliation proofs** and a **cleanup list**, a **JE register** and **import CSV**, a **verdict**, a **close package**
- A **position memo** decides a treatment; its **contract file** feeds the revenue schedule that `adjust` books
