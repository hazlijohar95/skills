# Financial close

Close one client's books for one period, month, quarter, or year, from a trial balance and general ledger export out of any accounting system.

## User-invoked

Reachable only when you type it (`disable-model-invocation: true`).

- **[close](./close/SKILL.md)**: Run a full close for one client and one period, from readiness check to delivered close package.

## Model-invoked

Type them, or the agent reaches for them when the task fits. Each one also works on its own, outside a close.

- **[setup-client](./setup-client/SKILL.md)**: Build or update a client's profile (basis, materiality, risk areas, recurring schedules) from their existing sources plus a short interview.
- **[intake](./intake/SKILL.md)**: Close readiness check: what is present, what is missing, and what each gap blocks.
- **[prep](./prep/SKILL.md)**: The prep phase as one call: `reconcile`, then `categorize`, with one batch of questions.
- **[reconcile](./reconcile/SKILL.md)**: A reconciliation proof per account, ending at zero or at named reconciling items.
- **[categorize](./categorize/SKILL.md)**: Sweep the period's transactions for miscoding, unmatched transfers, and duplicates.
- **[adjust](./adjust/SKILL.md)**: The JE register: accruals, reversals, prepaids, depreciation, and deferred revenue, each waiting on approval.
- **[journal-entry](./journal-entry/SKILL.md)**: One journal entry drafted to contract: balanced, sourced, approved, and CSV-ready.
- **[review](./review/SKILL.md)**: Fresh-eyes review of a prepared close, ending in a ready or not-ready verdict.
- **[deliver](./deliver/SKILL.md)**: The close package: statements, a close memo opening on the executive summary, and a workpapers workbook.
