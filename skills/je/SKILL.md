---
name: je
description: Journal entry drafting with a cited source, a workpaper, explicit approval, and an import-ready CSV. Use when booking a one-off journal entry, turning a document or calculation into a balanced entry, or when the adjust skill stages entries.
---

# Journal entries

Plugin root: the folder two levels above this file, which is
`<plugin root>/skills/je/SKILL.md`. Paths written `<plugin root>/...` start there. A
command that loaded this skill may state the root outright; use that when it does.

## Summary

The entry primitive: one contract for every journal entry the close produces. Balanced
lines, a cited source, a workpaper, explicit approval, and a CSV any general ledger can
import. The adjust skill runs this contract at phase scale; standalone, this skill drafts
the one-off entry the user asks for.

## The contract

Every entry, whoever stages it:

- Debits equal credits, and each entry is dated within the period (accruals: the last day).
- Every account is exactly as named in the client's chart of accounts. A needed account
  that does not exist is a question, never an invention.
- The memo is stable and reproducible: `<period> close: <what and why>`, plus
  `(auto-reverse <next period>)` when applicable, so a rerun can recognize an
  already-imported entry.
- The source is cited: a document, a schedule, a named policy, or an approved
  categorization item. No source, no entry; a data gap is a blocked entry, never an
  estimate, unless the client profile authorizes a named estimation policy for exactly
  that item.
- A workpaper accompanies the entry: source, calculation, tie-out.

## Workflow

1. Gather the source and confirm what the entry is for. Check the books first: an entry
   already posted for the same period and memo is done, not drafted twice.
2. Draft the entry under the contract above and show it with its workpaper.
3. Gate: explicit approval before the entry is marked approved. No confirmation, no
   approval; the entry stays proposed. An approval mark of unknown provenance is a
   proposal to re-confirm. Record the approval the moment it is given, keyed by the memo
   exactly: `closekit log <close-log.tsv> je approve "<memo>" "<who>" "<workpaper>"`
   (kit at `<plugin root>/scripts/closekit.py`; standalone with no close folder, keep the log beside the CSV).
4. Emit or append the approved entry to the import CSV per
   [reference/je-csv-format.md](reference/je-csv-format.md) and file it with the
   workpaper. Then run `closekit je <csv> --coa <tb> --label <period> --log
   <close-log.tsv>` (add `--start` and `--end` for a fiscal-year period) and paste its
   output into the workpaper; a CSV the kit fails is not handed off. Nothing is posted to any system; the CSV is the handoff.

## Guardrails

- **How to ask.** Every question to the user goes through the AskUserQuestion tool as
  multiple choice, never as a question in prose. Each gets two to four options, the
  recommended one first and marked "(Recommended)", each described by what it changes,
  with the figure where there is one. Follow `<plugin root>/skills/close/reference/asking.md` for batching,
  approvals, and what to do when the tool is unavailable.
- Figures come from the cited source or an authorized policy, never from model arithmetic
  presented as fact.
- One entry, one approval. Batch approval belongs to the adjust skill's register gate.
- This skill never posts anywhere and never edits the books.

## Deliverable

Voice, for every document this skill writes: the prose a careful accountant would say
aloud to a client. Short declarative sentences of varied length, sentence-case headings,
plain words, concrete nouns, and real figures. Join clauses with a comma or start a new
sentence; the em dash is the one mark the house style rejects outright. Before
filing, run `python3 <plugin root>/scripts/closekit.py lint <file>`, which holds the house
style list, and rewrite each line it flags.

```markdown
### Journal entry: <what>, <period>

| Dr | Cr | Amount | Source |
| <account> | <account> | <amount> | <document/schedule/policy> |

**Workpaper:** <source, calculation, tie-out>
**Status:** <approved / proposed / blocked with what is missing>
**CSV:** <path, or "not emitted; entry not approved">
```

## Reference files

- [reference/je-csv-format.md](reference/je-csv-format.md): the import CSV contract.
