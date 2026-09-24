# Acme Co, 2026-07: planted defects

Behavior eval answer key. When running a close against this data blind, copy the CSVs
(not this file) into a neutral folder such as `clients/acme/` first.

| # | Defect | Phase that should catch it | Deterministic check |
| - | ------ | -------------------------- | ------------------- |
| 1 | GL opening for Accounts Receivable is 4,900.00; prior TB closed at 5,000.00. Constant 100.00 difference dates to the opening | intake | `closekit tie` |
| 2 | Figma 99.00 posted twice in the GL (07-25, 07-26); TB carries it once, so Cash and Software each miss by 99.00 in activity | intake, categorize | `closekit tie` |
| 3 | June accrual of 800.00 was never reversed in July activity | adjust | none; judgment |
| 4 | Entry 2 (prepaid amortization) has no logged approval | adjust, review | `closekit je --log` |
| 5 | No bank statement provided, so Cash cannot be reconciled | intake, reconcile | none; coverage map |
| 6 | Prepaid Insurance has no schedule; the 100.00 amortization has no cited source | adjust | none; judgment |
