# Costs follow the revenue

Apply when the entity pays commissions, bonuses, marketplace fees, or other amounts that
exist because a contract was signed, or spends to set up for delivery.

Incremental costs of obtaining a contract (costs that would not exist had the contract not
been signed) are capitalized when expected to be recovered. They are amortized over the
period the contract's goods or services transfer, including specific anticipated renewals.
A cost incurred regardless of whether the contract is won is expensed. The one-year
expedient allows expensing when the amortization period is a year or less.

**Why.** A commission paid to win a customer who stays three years buys three years of
revenue. Expensing it when paid puts the cost of growth in the quarter the deal closed,
and makes fast-growing periods look worse than they are.

**Pattern.**
- Incremental: paid only because this contract signed. Commissions on signing and
  overrides tied to specific contracts qualify, even with a clawback. Base salaries,
  per-meeting bonuses, and team targets paid regardless of any one contract do not.
- Period: the initial term, extended by anticipated renewals when the renewal
  commission is not commensurate with the initial one. Customer life data sets the
  length.
- The one-year expedient is an election, and it only works when the amortization period
  really is a year or less. A non-commensurate renewal commission usually rules it out.
- Two amortization methods are accepted. One is a single period over the expected customer
  life. The other splits it: the part of the initial commission matching the renewal
  rate goes over the initial term, and the excess over the customer life. Whichever the
  client adopts is its policy, applied to every contract, and it goes in the profile's
  elections.
- Fulfillment costs are capitalized only when they relate to a specific contract, build a
  resource used to perform, and will be recovered. Most setup labor in SaaS fits this
  shape. Test it before booking.
- Model the asset as a contract file with `"kind": "cost"`: one ratable obligation over
  the benefit period, billings as the amounts capitalized.
- The asset is built from commissions actually paid (payroll or a commission register),
  contract by contract. No register means no balance: state the treatment, request the
  register, and stop. A figure built from the plan's rates and an assumption about which
  deals were new logos is not a balance to propose, however it is labeled.

**Deciding facts.** The commission plan's triggers. Renewal commission against initial.
Customer life data.

**The tell.** All commissions expensed as paid under "the one-year expedient" while
renewals pay a fraction of new-logo rates.

**Codification.** 340-40-25-1, 25-2, 25-4, 25-5, 35-1.
