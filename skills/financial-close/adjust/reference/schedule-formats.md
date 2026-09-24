# Schedule roll-forward formats

Every schedule shares one invariant: **closing balance ties to the GL control account
exactly**, with rounding shown as its own labeled line. A schedule that does not tie is not
done.

The formats below are the common cases, not the closed set. Any recurring measurement the
profile records (inventory valuation under a stated costing method, and the like) can ride
the same pattern: the user supplies the method and the judgment inputs, the schedule does
the arithmetic, and the result ties to its control account. Build the schedule in this
shape and file it with the others; never improvise the method itself.

## Prepaid amortization

One row per prepaid item:

| Item | Vendor | Service period | Total paid | Opening balance | This period | Closing balance |
| ---- | ------ | -------------- | ---------- | --------------- | ----------- | --------------- |

- Straight-line over the service period. Monthly amount = total / months; put any rounding
  remainder in the final month so the item amortizes to exactly zero.
- This period's entry: Dr expense, Cr prepaid, for the "this period" column total.
- A new payment to a prepaid vendor with no schedule row is a question, not a guess at the
  service period.

## Fixed assets and depreciation

One row per asset:

| Asset | In service | Cost | Method | Life | Accumulated opening | This period | Accumulated closing |
| ----- | ---------- | ---- | ------ | ---- | ------------------- | ----------- | ------------------- |

- Use the client's stated method and in-service convention from the profile. Method
  missing: straight-line, disclosed. Convention (full-month, mid-month, following-month)
  missing: derive it from an existing asset's accumulated math when one exists and say so;
  otherwise full month in the in-service month, disclosed.
- Compute this period cumulative-exact: cost x months-elapsed / life, minus prior
  accumulated. This reproduces schedules whose stated monthly amount is rounded (15 months
  of a 333.33 schedule accumulate to exactly 5,000.00, not 4,999.95); document the
  pennies whenever the stated monthly and the cumulative figure disagree.
- Entry: Dr depreciation expense, Cr accumulated depreciation.
- An asset purchased this period without life/method guidance goes to the question queue.
- Disposals are out of the core scope; flag them, do not improvise gain/loss.
- Impairment indicators ride along with the roll: an asset marked idle or damaged, a
  discontinued line's equipment, or a fully depreciated asset still load-bearing gets
  flagged as a disclosure. The close never books an impairment; measurement is the
  preparer's.

## WIP / percent-complete (when the profile records contracts spanning periods)

One row per open contract:

| Contract | Contract price | Est. total cost | Cost to date | % complete | Revenue earned | Billed to date | Over/(under) billing |
| -------- | -------------- | --------------- | ------------ | ---------- | -------------- | -------------- | -------------------- |

- Percent complete = cost to date / estimated total cost. Cost to date comes from the GL
  (job-costed accounts) or the user's job ledger; **estimated total cost is the user's
  judgment, asked for, never derived**. Revenue earned = contract price x percent
  complete.
- Overbilled (billed > earned): Dr revenue, Cr billings in excess (liability).
  Underbilled (earned > billed): Dr costs in excess / unbilled AR (asset), Cr revenue.
  Both tie to their balance sheet accounts exactly.
- A profile that records contracts but no schedule and no estimated costs: this whole area
  is blocked with the schedule on the request list. Billed-equals-earned is never the
  silent fallback for a contract client.
- Loss contracts (est. total cost > contract price) are flagged, never provisioned here;
  the loss provision is the preparer's.

## Loan roll-forward (optional, when a lender statement is provided)

One row per loan:

| Loan | Lender | Opening principal | Draws | Principal paid | Closing principal | Interest per statement | Interest per GL |
| ---- | ------ | ----------------- | ----- | -------------- | ----------------- | ---------------------- | --------------- |

- Closing principal ties to the lender statement and the GL liability account exactly.
- The last two columns are the interest recalc: statement interest vs what the GL expensed.
  A gap usually means a payment coded entirely to principal or entirely to expense; the
  difference is an adjustment-required item with the split from the statement.
- No lender statement: no roll; the loan balance stays a reconcile-phase exception.

## Deferred revenue

For invoices that match delivery only: one obligation, billed for its own service
period, no variable terms. A bundle, setup fee, ramp, usage term, credit, or amendment
makes the billed amount the wrong base. Those contracts get a contract file and the
revenue skill's schedule, which allocates the transaction price instead.

One row per contract or invoice:

| Contract | Billed | Service period | Opening deferred | Recognized this period | Closing deferred |
| -------- | ------ | -------------- | ---------------- | ---------------------- | ---------------- |

- Straight-line over the service period unless the profile states another policy. Each
  contract recognizes to exactly its billed amount over its life; rounding remainder in the
  final period.
- Entry: Dr deferred revenue, Cr revenue.
- Completeness cuts both ways: scan the period's revenue for new billings whose service
  extends past the close (a customer already on this schedule, or invoice language like
  "annual" or "12 months"). A hit sitting fully in revenue is a question or a new row,
  never left as-is.

## Standing accruals

One row per recurring accrual:

| Accrual | Basis | Prior period amount | Reversal posted? | This period amount | Source |
| ------- | ----- | ------------------- | ---------------- | ------------------ | ------ |

- Check the reversal column first; a missing reversal is an entry before any new accrual.
- Each accrual books as: Dr expense, Cr accrued liability, with next-period auto-reverse
  noted in the memo.
- "Basis" names where the amount comes from: invoice received after cutoff, contract,
  or an estimation policy from the profile. No basis, no accrual.
