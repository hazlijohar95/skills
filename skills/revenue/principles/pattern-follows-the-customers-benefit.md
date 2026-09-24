# Pattern follows the customer's benefit

Apply when deciding over time or point in time, choosing a measure of progress, or
revising an estimate of total effort.

A performance obligation is satisfied over time when the customer consumes the benefit as
the entity performs, when the work builds something the customer controls as it goes, or
when the output has no other use to the entity and the entity has a right to be paid for
work done so far. Otherwise it is satisfied at a point in time. Over time, pick the one
measure that best tracks what the customer receives, and use it consistently.

**Why.** Revenue should rise as the customer gets value. A stand-ready service delivers
value every day, so time elapsed tracks it. A migration project delivers value as datasets
land, so effort tracks it better than time or billing milestones.

**Pattern.**
- Stand-ready SaaS: time elapsed, ratable. Daily or monthly convention per the client's
  election, applied consistently.
- Fixed-fee services: input method (hours or cost) against total estimated input,
  usually. Exclude inputs that do not transfer anything: rework from the entity's own
  mistakes, wasted materials. Keep extra effort caused by the job being harder than
  scoped. That is still work performed for the customer.
- An estimate of total effort is re-estimated each close. The change goes through as a
  cumulative catch-up (`method: cumulative`, `price_change: 0`).
- The right-to-invoice expedient fits time and materials when each invoice matches the
  value delivered. It fails when rates change retrospectively, when front-loaded rates
  exceed value, or when a cap or rebate means invoices do not track value.
- Billing milestones are not a measure of progress unless they happen to track delivery.
  Test that. Don't assume it.
- Point in time: when control passes (training delivered, a license made available).

**Deciding facts.** Where the work happens and who owns the output as it is made. What a
customer owes on termination for convenience. Hours or cost to date and the latest
estimate at completion. Why the estimate changed.

**The tell.** Revenue by billing milestone, progress against a stale estimate, or
the right-to-invoice expedient on an engagement with a retrospective rebate.

**Codification.** 606-10-25-27, 55-16 to 55-21, 55-18.
