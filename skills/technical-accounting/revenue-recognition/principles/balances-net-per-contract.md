# Balances net per contract

Apply at every period end, and whenever a balance sheet line for deferred revenue,
unbilled revenue, or credits owed is prepared.

Each contract nets to one position. Paid or billed ahead of performance: a contract
liability. Performed ahead of an unconditional right to bill: a receivable (unbilled if
not yet invoiced). Performed ahead of a right that still depends on something other than
time passing: a contract asset. Amounts expected to be refunded or credited are refund
liabilities, not deferred revenue.

**Why.** Deferred revenue promises future revenue. A refund liability promises cash going
out. A contract asset carries performance risk that a receivable does not. Lenders read
these lines differently, so mixing them misstates the balance sheet even when revenue is
right.

**Pattern.**
- Net within a contract, never across contracts. Customer A's deferred revenue does not
  offset customer B's unbilled amount.
- Usage earned in the month and billable after month end is an unbilled receivable
  (`"unbilled": "receivable"`). Revenue recognized ahead of billing under a ramp, where
  billing depends on continuing to serve, is a contract asset.
- A retrospective rebate, an SLA credit owed, or a prepayment refundable on exit is a
  refund liability. Record it in the contract file's `refund_liability` for the period.
  `rev balances` then presents it apart and never nets it into deferred revenue or
  against a contract asset.
- Tie every total to the ledger: deferred revenue, unbilled receivables, contract assets,
  refund liabilities, deferred commissions. A difference is a reconciling item with a
  bucket, never a plug.

**Deciding facts.** Billing terms and dates. Whether the right to bill depends on further
performance. Credit and rebate terms.

**The tell.** One deferred revenue account that nets all customers, carrying debit
balances for some. Credits owed sitting in deferred revenue.

**Codification.** 606-10-45-1 to 45-4.
