# Asking the user

Every question to the user is a multiple-choice question asked through the AskUserQuestion
tool. The user answers with one click. The tool adds an "Other" choice for a typed answer
on its own, so option lists never include one.

## One question

| Part | Rule | Example |
| --- | --- | --- |
| Question | One full sentence ending in "?", naming the item and its figure | "Approve the July rent accrual of $2,000.00?" |
| Header | The item in 12 characters or fewer | `Rent accrual` |
| Options | Two to four, mutually exclusive. Labels of one to five words that are the answer itself. The recommended option first, with " (Recommended)" appended | `Approve (Recommended)`, `Decline`, `Change amount` |
| Description | What happens under this answer, in accounting terms and with the figure: what gets booked, what it does to the balance, what stays open | "Books Dr Rent Expense / Cr Accrued Liabilities $2,000.00, reversing 2026-08-01." |
| Preview | For comparing entries or treatments: the journal lines, schedule rows, or balances each option produces, side by side. Single-select questions only | The two July schedules under each treatment |
| Multi-select | For picking several from a set: which small entries to approve, which readers rely on the statements | |

Ask only what the documents and data cannot answer. A fact the data settles is derived.

## Batching

- One call holds up to four questions: the batch for a phase boundary. More than four
  means successive calls, most consequential first.
- Anything above materiality, whether an approval, an acceptance, or a judgment, gets its
  own question with its consequence. It never shares a multi-select with other items.
- Items below materiality go together in one multi-select question of up to four. More
  than four: one question, "Approve the 9 entries below materiality listed in
  workpapers/je-register.md?", with the list in the preview.

## Patterns

| Situation | Options, recommended first |
| --- | --- |
| Entry approval | Approve / Decline / Change (description: "Tell me what to change") |
| Exception acceptance | Accept and disclose (description states what the memo will say) / Send back to <phase> |
| Judgment between treatments | Treatment A (Recommended) / Treatment B, each description with its period revenue and balance, preview showing both |
| Missing fact | The likely answers, each with the figure it produces: "Onboarding finished before July 1" / "Finished after July 1" |
| Profile interview | The answer inferred from sources first, tagged with its source ("Accrual (from the TB)"), then the other common answers |
| Election | The option the skill recommends, then the others, each description stating what it changes each close |

## Recording the answer

Log every answer the moment it arrives, with `closekit log`: `approve`, `decline`,
`accept`, or `answer`, the item or memo as the subject, the user as `who`, and
`AskUserQuestion <date>` as the evidence. An answer that exists only in the conversation
is lost to the next session.

## When the tool is unavailable

In an unattended run, or on a surface without the tool, write each question in the same
shape (question, options with consequences, the recommendation) as a `question` row in
the close log and in the deliverable's open items. Take the recommended option only where
the skill allows a proceed-and-disclose default. An approval always waits for the user.
