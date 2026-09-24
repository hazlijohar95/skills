# Price is what you expect to keep

Apply when any amount depends on something that hasn't happened yet (usage, uptime,
volume, a deadline, a return, a customer's satisfaction), when payment timing is far from
delivery, or when the entity pays anything to the customer.

The transaction price is the amount the entity expects to be entitled to. That is the
fixed fee, plus variable amounts estimated and then constrained, less amounts expected to
flow back to the customer, adjusted for financing when it is significant.

**Why.** Revenue that later reverses misleads the reader twice: once when it is booked and
once when it comes back out. The estimate puts the likely amount in revenue now. The
constraint keeps out whatever could plausibly reverse by a significant amount.

**Pattern.**
- Name every variable term: usage and overage, SLA credits, volume rebates (especially
  retrospective ones), success fees, price protection, refunds, caps and floors.
- Pick the estimation method that predicts better: most likely amount for a binary
  outcome (a bonus is earned or not), expected value for a spread of outcomes (a portfolio
  of SLA credits).
- Then constrain. Ask how likely a significant reversal is and how big it would be. It is
  more likely when the outcome depends on things outside the entity's influence
  (the customer's IT team, the market), when experience is thin or not predictive, or
  when the range is wide. Specific recent evidence beats a historical average.
- Before estimating a variable amount across the whole contract, check whether it belongs
  to one period of a series (see allocate-by-standalone-value). Usage priced per month
  usually does, which removes the need to estimate a year of usage.
- Re-estimate every close. A changed estimate is a cumulative catch-up, not a
  modification, unless the parties changed the contract.
- Credits and concessions to the customer reduce revenue. They are not expenses, unless
  the entity receives a distinct good or service for them at fair value.
- Financing: when payment and delivery are more than a year apart, test whether the
  effect is significant. Compare the price with what the customer would pay in cash as
  the service transfers, and put the difference in the memo as a figure. Reasons other
  than financing are narrow: securing supply, protecting against non-performance, or an
  amount that varies with events outside both parties' control. A customer's budget or
  cash limit is not one of them. When the effect is small, say so with the figure.

**Deciding facts.** The variable terms themselves. Forecasts and change requests. History
of credits, rebates, bonuses. The customer's own statements about timing. Reasons for
unusual payment timing.

**The tell.** Revenue equal to invoices on a contract with a retrospective rebate. A bonus
included because the win rate is high while the customer says it will be late. SLA
credits booked as expense, or in the month the credit memo issues.

**Codification.** 606-10-32-5 to 32-9, 32-11 to 32-14, 32-15 to 32-18, 32-25 to 32-27.
