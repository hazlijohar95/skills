# JE import CSV contract

One file per close: `adjusting-entries-<client>-<period>.csv`, approved entries only.

## Columns

```csv
entry_no,date,account,memo,debit,credit
```

- `entry_no`: groups the lines of one entry (1, 1, 2, 2, 2, ...). Every group balances.
- `date`: ISO format (YYYY-MM-DD), within the close period. Accruals dated the last day of
  the period.
- `account`: exactly as named in the client's chart of accounts, taken from the TB/GL
  provided. Never invent an account name; a needed account that does not exist is a question.
- `memo`: `<period> close: <what and why>` plus `(auto-reverse <next period>)` where
  applicable. Memos are stable and reproducible so a re-run can detect already-imported
  entries by exact match.
- `debit` / `credit`: positive numbers, two decimals, one of the two per line, no currency
  symbols or thousands separators.

## Invariants

- File foots: total debits equal total credits, and each `entry_no` group foots on its own.
- Line order: within a group, debits before credits.
- Encoding: UTF-8, comma-separated, header row exactly as above.

Most systems (QuickBooks, Xero, NetSuite, and the rest) accept or trivially map this shape;
tell the user to use their system's journal import and map columns by name.
