# Close package formats

## Voice

Everything in the package reads as the accountant's own work product: plain professional
prose, short sentences of varied length, sentence-case headings, figures over adjectives.
The executive summary especially: the owner should hear their accountant. Write "July lost
$2,517, mostly the workstation purchase". `closekit lint` checks every file in `package/`
against the house style list.

## File set

```
package/
  close-package-<client>-<period>.xlsx      workpapers workbook
  close-memo-<client>-<period>.docx         close memo, executive summary first
  statements-<client>-<period>.md           P&L, balance sheet, cash flow
  adjusting-entries-<client>-<period>.csv   copied from workpapers (approved entries)
```

There is no separate executive summary file. The executive summary is the opening section
of the close memo, so the owner and the preparer read one document.

## Statements

Comparative columns: Current, Prior, Change $, Change %. Subtotals: gross profit, operating
income, net income on the P&L; current/non-current on the balance sheet. Cash flow indirect:
net income, non-cash add-backs (depreciation, amortization), working capital changes from
the comparative balance sheet, ending cash ties to the reconciled cash balance.

## Workbook tab map

| Tab | Contents |
| --- | --- |
| Cover | Color legend, tickmark key, sign-off lines, tab map (see formatting standards) |
| Summary | Every material account: TB balance, support type, link to its tab |
| Adjusted TB | The full adjusted trial balance the Summary references |
| Rec: <account> | One tab per reconciliation proof |
| Sched: <type> | One tab per schedule (prepaid, FA, deferred rev, accruals; loan roll when a lender statement exists) |
| Equity roll | Opening equity + net income + contributions and distributions = closing, tied to the balance sheet |
| JE register | The register with approval status |
| Cleanup | The dispositioned cleanup list |

Within the workbook, figures flow by cell reference: source data is entered once on its
detail tab, and the Summary pulls from there. A Summary number typed independently of its
detail tab is the defect this workbook exists to prevent.

## Workbook formatting standards

The conventions professionals expect (Training The Street and Wall Street Prep house
style, adapted for accounting workpapers). Apply them when generating the xlsx.

**Font color code** (the industry-standard scheme; put the legend on the cover tab, since
a reviewer cannot assume a generated workbook follows convention):

| Color | Meaning |
| --- | --- |
| Blue | Keyed from a source document (statement figure, schedule input) |
| Black | Formula calculated on the same tab |
| Green | Link pulled from another tab in this workbook |
| Red | Reserved for exception and adjustment flags, never data |

External workbook links are banned outright; everything the workbook needs lives in it.

**Totals**: bold; a single top border above a subtotal; a double bottom border under a
grand total (the accounting double rule). Totals are SUM over the range, never cells added
one by one.

**Numbers**: accounting format throughout; negatives in parentheses; thousands separators;
zeros display as a dash; two decimals (workpapers carry cents, unlike banking models in
millions); currency symbol on the first and last row of a schedule only; units and
currency stated once in the header. Percentages to one decimal, italic.

**Tie-out checks**: every tab with a control-account tie carries a check cell using a
custom format that reads OK at zero and ERROR otherwise, so a broken tie is visible
without reading a single number.

**Layout**: one font (Calibri or Arial), 10 to 11 pt, larger only in the two title rows;
no merged cells anywhere (center across selection where needed); gridlines off; narrow
spacer column A, wide label column B, indented detail rows; every tab headed client name,
workpaper title, period, units; column headers bold with a fill and a bottom border;
freeze panes under the header row.

**References**: a figure is typed once, at its source tab, and linked everywhere else,
directly rather than through chains of intermediate cells; anchor with `$` so one formula
copies across its row.

**Cover tab** (first tab): the color legend, the tickmark key (tied to source document,
recalculated, agreed to TB), preparer and reviewer sign-off lines, and the tab map.

**Generation discipline**: one idempotent script builds the whole workbook in a single
run, capturing row positions as it writes rather than hardcoding cell addresses (an
inserted row must not strand a reference). Sheet names avoid characters that need quoting
in cross-sheet references (ampersands, spaces, leading digits): `PnL`, not `P&L`. Tabs
that mirror another artifact (the exceptions tab mirrors the register) are generated from
that source file, never retyped, so the two cannot drift.

## Close memo template

The memo ships as a Word document (.docx), never markdown. Use the heading structure
below: sentence-case headings, one font, bold on totals only, no decorative styling. The
sign-off checklist renders as real checkboxes or underscored lines, not markdown syntax.

```markdown
# Close memo: <client>, <period>

**Basis:** <accrual/cash> · **Prepared:** <date> · **Verdict:** <ready / delivered with override>

## Executive summary
<owner language, before any preparer detail: the three to five things that mattered this
period, flux highlights with their drivers, and the cash position. Headline figures over
adjectives; a business owner should hear their accountant's voice, not an analyst's.>

## Scope
<accounts closed, statements delivered, anything excluded and why>

## Work performed
- Reconciled: <n accounts, list>
- Cleanup: <n items dispositioned>
- Entries: <n approved, $ total; CSV delivered for import>

## Open items
<each: description, amount, owner, expected resolution, or "None">

## Accepted exceptions
<each with who accepted it, or "None">

## Follow-ups for next period
<reversals due, aging items, schedule updates>

## Sign-off
- [ ] Preparer: ____________  date ______
- [ ] Reviewer: ____________  date ______
```

## Executive summary section

The executive summary lives inside the close memo, first section, never as its own file.
It covers: the three to five headline figures (revenue, net income, cash, and the period's
one surprise), what mattered this period in owner language, and the cash position. Ending
cash anywhere in the summary is the adjusted GL book balance (the reconciled figure),
never the bank statement's ending balance; where the two differ, state the bank-to-book
bridge (outstanding items and unbooked fees) in one line so the figures visibly agree.
