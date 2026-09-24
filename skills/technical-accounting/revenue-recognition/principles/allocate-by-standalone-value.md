# Allocate by standalone value

Apply when a contract has more than one performance obligation, a discount, or a variable
amount that might belong to one part only.

Split the transaction price across the performance obligations in proportion to what each
would sell for alone. Two exceptions move amounts to one part only: a discount with
observable evidence that it belongs to a subset, and a variable amount whose terms relate
specifically to one obligation or one period of a series.

**Why.** The invoice lines are the seller's presentation, not the value delivered. A
"free" implementation or a steep services discount makes the invoice say services are
worth little and software a lot, or the reverse. Allocation by standalone price removes
that choice from the sales team, so revenue timing does not depend on how a deal was
quoted.

**Pattern.**
- Standalone selling price is the observable price when the item is sold alone to similar
  customers. When it sells in a range, use a point the data supports and say which.
  Without observable sales, estimate by adjusted market assessment or cost plus a margin.
  Residual only when the price is highly variable or uncertain, never as a plug. A
  service that has never been sold standalone counts as uncertain. Residual and cost plus
  margin are both open for it: pick one, and show the other's result.
- Use one SSP basis per customer situation and say which: new-logo, renewal, or add-on.
  The same seats can move from one basis to another at a modification, when the customer
  has become an existing one. State that when it happens.
- Document the SSP evidence once per stream in the policy memo. A contract memo then cites
  it rather than rebuilding it.
- Allocate a discount to all obligations proportionally by default. A subset gets the
  whole discount only with observable evidence that the subset is regularly sold as a
  bundle at that discount.
- A variable amount goes wholly to one obligation or one month when its terms tie to that
  part (overage priced per month's events, an SLA credit on one month's fee) and the
  result is a fair reflection of value. Usage and credits in SaaS usually qualify. A
  bonus for the whole project usually does not.
- The kit does the math: `closekit rev allocate` with `ssp` on each obligation, or
  `allocated` on each when a judgment (subset discount, residual) fixed the split.

**Deciding facts.** Standalone sales data and its range. Price books. Partner pricing for
the same service. Whether a discount pattern repeats across bundles.

**The tell.** Allocations equal to invoice lines. The residual method used for a product
with a tight observable price range. Overage estimated over a year when its price is
monthly.

**Codification.** 606-10-32-33, 32-34, 32-36, 32-37, 32-39 to 32-41.
