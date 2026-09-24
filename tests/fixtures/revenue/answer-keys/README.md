# Tallow Labs, July 2026: revenue answer keys

Grading material for `../tallow-labs/`. Never copy this folder into a workspace a run can
see. Each key gives the treatment, the fact that decides it, what a template gets wrong,
and the July numbers. The numbers come from `closekit rev` run over the contract file of the
same name in this folder. `expected-2026-07.csv` holds them for the self-check.

These keys state one well-supported answer. Where a second answer is defensible, the key
says so and what a memo must show to reach it. Grade the reasoning: a run that reaches an
accepted alternative with the deciding facts named passes. A run that lands on the right
number by applying a template without naming the deciding fact fails that scenario.

A US CPA should review these keys before they are used to gate a release. The judgment
calls are collected in `SIGN-OFF.md`. Signed off: not yet.

## Grading rubric (per scenario)

1. Names the fact that decides the treatment, citing the document it came from.
2. Argues at least one rejected alternative and says why the facts reject it.
3. Reaches the key's treatment or an accepted alternative.
4. July numbers come from a kit run, not prose arithmetic, and match the key to the cent,
   or match the kit run over the key's method with the run's own stated and supportable
   inputs (an SSP point inside the documented range, for example). Files under
   `alternatives/` are the accepted alternatives, rerunnable.
5. Flags the correction to what the client already booked, where there is one.
6. Asks the user only what the documents cannot answer.

## 1. Northwind: implementation fee that is not a separate promise

- **Deciding facts.** `pricing.md`: implementation is never sold standalone, only Tallow
  can do it, and the customer cannot use the platform until it is done. `notes.md`: data
  loaded 2026-02-26, first login 2026-02-27. Renewals skip the fee. Customer life
  averages 3 years.
- **Treatment.** Implementation is setup, not a promise. The service the customer pays
  for starts when it can be used. Under the monthly convention that is 2026-03-01. The
  $24,000 is recognized over March 2026 to January 2027. The $6,000 upfront fee gives a
  material right, because renewing customers pay $24,000 while new customers pay $30,000.
  It is recognized over the 3-year expected life from access. This equals the renewal
  alternative in 55-45: $24,000 to year 1 and $6,000 to the renewal right.
- **Accepted alternatives** (in `alternatives/`):
  - Start on the contract date (2026-02-01), if the memo argues the 27 days of setup are
    immaterial ($181.82 a month): July $2,166.67, correction −$5,000.00.
  - Recognize the fee over the 12-month term, if the memo argues a 20% discount against a
    new customer's first year is not material: July $2,500.00, correction −$3,000.00,
    below the item threshold.
- **Template trap.** Booking $6,000 to services revenue at go-live, which is what the
  client did in February.
- **July.** Revenue $2,348.48. Cumulative $11,742.42 against $18,000.00 booked. Correction
  −$6,257.58, itemized for approval. Contract liability $18,257.58.

## 2. Harbor: price ramp over a flat, non-cancellable service

- **Deciding facts.** The order form is non-cancellable, with 500 seats in every year. The
  AE email: same product each year, and the total is a normal multi-year discount.
- **Treatment.** One series of identical monthly periods with a fixed total of $270,000,
  recognized straight-line at $7,500.00 a month. Billing follows the ramp, so a contract
  liability early in each year becomes a contract asset later: $30,000 at 2026-12-31.
- **Financing component.** The memo must assess it, and the answer is that none is
  significant. Payments are annual in advance, so the customer pays roughly in step with
  or slightly ahead of the service. Discounting the actual payments against the straight-
  line pattern moves the price by only about 1% to 2%. Don't rest the conclusion on the
  budget reason in the email: a customer's budget limit is not among the reasons other
  than financing that the guidance recognizes (PwC Viewpoint 4.4.1.3). Significance is
  the argument.
- **Template trap.** Recognizing as billed, $5,000 a month in 2026. That is right only if
  the service rose each year or the customer could cancel. Birch (scenario 5) is the
  contrast.
- **July.** Revenue $7,500.00. Cumulative $52,500.00. Contract liability $7,500.00.

## 3. Quarry: usage overage in the month it happens

- **Deciding facts.** The platform fee covers events within a calendar month, and unused
  events do not roll over. The overage price is fixed per event and relates only to that
  month's service.
- **Treatment.** A series of distinct monthly service periods. The overage is variable
  consideration that relates only to the month it is earned, so it goes entirely to that
  month. It is not estimated over the year and not deferred. July overage is 24,000 events
  × $0.05 = $1,200.00, recognized in July. It is invoiced in August, and the right to it
  is unconditional once July ends, so it is an unbilled receivable.
- **Template trap.** Recognizing overage when invoiced, a month late. The client booked
  June's $95.00 in July. That is below materiality: note it and fix the practice.
- **July.** Revenue $4,200.00 (platform $3,000.00, overage $1,200.00). Unbilled
  receivable $1,200.00.

## 4. Cedar: SLA credit reduces the month it relates to

- **Deciding facts.** The credit is 10% of the affected month's fee, triggered by that
  month's uptime (99.1% in July).
- **Treatment.** An SLA credit is variable consideration, a price concession. It is not an
  expense. It relates to July's service period, so it reduces July revenue by $1,000.00.
  The credit owed is a refund liability, presented apart from any contract liability,
  until the credit memo applies it to August's invoice.
- **Accepted alternative.** An inception estimate of expected credits under the
  expected-value method, trued up in July. On one credit in twelve months the difference
  is trivial.
- **Template trap.** Recording the credit in August when the credit memo issues, or booking
  it to an expense account.
- **July.** Revenue $9,000.00. Refund liability $1,000.00. No other contract balance.

## 5. Birch: the same ramp, flipped by a termination right

- **Deciding facts.** The special terms let the customer terminate for convenience on 60
  days' notice with a refund and no penalty. Tallow can enforce payment only for the
  notice period.
- **Treatment.** The contract runs only as long as the enforceable rights: effectively a
  rolling contract with a short notice period, not a 3-year commitment. There is no
  3-year transaction price to spread, so 2026 revenue follows the 2026 fee, $2,000.00 a
  month. The 2027 and 2028 fees are not in the transaction price.
- **Presentation.** Of the $10,000 prepaid and unserved at July 31, $4,000 covers the
  enforceable notice window (August and September) and is a contract liability. The
  $6,000 beyond it is refundable on termination, so it is a refund liability (Deloitte
  Roadmap 4.4.1.1.1, 14.3). One $10,000 contract liability is a weaker presentation. It
  passes only if the memo addresses the refund right.
- **Template trap.** Averaging $96,000 over 36 months at $2,666.67, because the order form
  looks like Harbor's.
- **July.** Revenue $2,000.00. Contract liability $4,000.00. Refund liability $6,000.00.

## 6. Alder: add-on seats below standalone price

- **Deciding facts.** The add-on price is $100 a seat. `pricing.md` shows add-on seats at a
  median of $118 with 80% of orders between $112 and $120. The AE email calls $100 a
  one-off retention concession. Training session 2 is still undelivered.
- **Treatment.** The amendment adds distinct services, but not at their standalone price
  adjusted for this customer's circumstances. So it is not a separate contract. The
  remaining services (the rest of the subscription for 150 seats, and training 2) are
  distinct from what has transferred. So the old contract is treated as terminated and a
  new one created, prospectively. The unrecognized consideration ($7,499.99) plus the
  $2,500.00 added is reallocated between the remaining subscription (SSP 150 seats × $118
  × 6/12 = $8,850) and training 2 (SSP $2,500).
- **SSP points.** At inception, the key uses the $114 new-logo median for the original
  seats, which treats the order form as Alder's first. At the modification date, all 150
  remaining seats take the $118 add-on and existing-customer median, because Alder is by
  then an existing customer buying more of the same seats. A memo that uses $117 or $118
  at inception (Alder as an existing customer), or keeps $114 for the original seats at
  the modification ($1,292.97 July, $8,707.02 liability), passes if it says why.
- **Accepted alternative.** Treating it as a separate contract fails unless the memo shows
  $100 falls within a supportable SSP range for this customer, adjusted for its
  circumstances.
- **Template trap.** Booking the $2,500 on its own over six months ($416.67 a month) on
  top of the old schedule.
- **July.** Revenue $1,299.56. Training 2 carries $2,202.64, recognized on delivery in
  September. Contract liability $8,700.43.

## 7. Elm and Pine: who is the customer

- **Elm, deciding facts.** Tallow sets the price, the buyer accepts Tallow's MSA, and the
  marketplace has no obligation to provide the software. Elm is Tallow's customer. The
  marketplace is an agent collecting the price.
- **Elm, treatment.** Revenue is gross, $48,000 recognized ratably from 2026-06-01. The 3%
  fee ($1,440) is a cost of obtaining the contract, not a revenue reduction. With a
  12-month term it may be expensed under the one-year practical expedient. The profile
  records no election, so the memo must propose one. Otherwise the fee is capitalized and
  amortized over the 12 months.
- **Pine, deciding facts.** Pine buys at $90 a seat, sets its own price, and must pay Tallow
  whether or not its customer pays. Pine is Tallow's customer.
- **Pine, treatment.** Revenue is $3,600 recognized ratably over the 12-month service
  period, not $5,400 (Pine's price to Lakeview), and not all in July.
- **Template traps.** Revenue booked net at cash received ($46,560 in June). A reseller
  deal grossed up to the end-customer price. Either one booked in full on receipt.
- **July.** Elm $4,000.00, Pine $300.00. Corrections through July: Elm −$38,560.00 of
  revenue (booked $46,560.00 in June against $8,000.00 earned), with the $1,440.00 fee to
  expense or deferred commissions per the election. Pine −$3,300.00. Contract liability:
  Elm $40,000.00, Pine $3,300.00.

## 8. Spruce: fixed-fee services measured by effort, with a revised estimate

- **Deciding facts.** The work is done in the customer's warehouse, and datasets belong to
  the customer as they load. On termination for convenience the customer pays cost plus
  margin. Either fact supports recognizing over time. The estimate rose to 450 hours
  because the schemas were messier, which is more work, not wasted effort.
- **Treatment.** Over time, measured by hours against total estimated hours. The revised
  estimate is a change in estimate with a cumulative catch-up in July: 180 / 450 = 40% of
  $80,000 = $32,000.00 cumulative. Billing milestones do not measure progress. A loss
  check shows 450 hours × $120 = $54,000, below the $80,000 fee, so no loss contract.
- **Note.** If the overrun had come from Tallow's own rework, those hours would not
  measure progress and would be excluded.
- **Template trap.** Recognizing per billing (50% at kickoff), or 180 / 400 against the
  stale estimate ($36,000).
- **July.** Revenue $20,000.00. Contract liability $8,000.00.

## 9. Willow: time and materials with a retrospective rebate

- **Deciding facts.** Once total hours pass 150, the $150 rate applies to all hours,
  retrospectively. CR-2 was signed on 22 July and the forecast is 190 hours.
- **Treatment.** CR-2 is a signed change in scope, so it is a contract modification. The
  memo must say which kind. The key treats the engagement as one performance obligation
  (an integrated advisory deliverable), partly satisfied, so the modification is a
  cumulative catch-up under 25-13(b). The total price becomes 190 × $150 = $28,500 (under
  the $35,000 cap), recognized on hours: 145 / 190 gives $21,750.00 cumulative. The right-
  to-invoice expedient does not fit: with a retrospective rebate, the invoiced $175 does
  not match the value delivered.
- **Accepted alternative.** Hours as a series of distinct services, making the
  modification prospective under 25-13(a). The $11,000 unrecognized is spread over the
  remaining 90 hours: July $5,500.00, a contract asset of $1,250.00, and a refund
  liability of $3,625.00 (`alternatives/willow-prospective.json`). The memo must name the
  fact that makes the hours distinct.
- **Template trap.** Recognizing what was invoiced, $7,875.00 for July.
- **July.** Revenue $4,250.00. Refund liability $3,625.00, the $25 an hour to be credited
  on 145 billed hours. No other contract balance.

## 10. Maple: success fee fully constrained

- **Deciding facts.** The bonus depends on the customer's IT team, outside Tallow's
  control. The customer's CIO wrote on 29 July that go-live is mid-October, after the
  30 September deadline. The 5-of-6 track record is outweighed by that specific evidence.
- **Treatment.** The bonus is variable consideration with two outcomes, estimated at the
  most likely amount. At July 31 the most likely amount is zero, and even a positive
  estimate would fail the constraint: a significant reversal is not unlikely. Include
  nothing and reassess at each close. The fixed fee is recognized over time on hours:
  70 / 200 of $30,000 in July.
- **Template trap.** Including $15,000 because the history says 83% hit their date.
- **July.** Revenue $10,500.00. No contract balance.

## 11. Aspen: prepaid credits with expected breakage

- **Deciding facts.** 118 expired orders with a stable 85% usage rate, and no refunds or
  extensions ever. That is enough history to expect breakage.
- **Treatment.** Recognize expected breakage in proportion to credits used. The $20,000 is
  spread over the 340,000 credits expected to be used, not 400,000. Revenue per credit is
  $0.0588, not $0.05.
- **Accepted alternative.** Recognize breakage only when the chance of use becomes remote,
  if the memo shows the history is not predictive for this customer. The study makes that
  hard to argue.
- **Also.** The memo notes that unclaimed property rules were considered. Credits
  forfeited to a business customer rarely escheat, but that is a check to make, not an
  assumption.
- **Template trap.** $0.05 per credit with the unused remainder at expiry, which is the
  client's current practice.
- **July.** Revenue $1,764.71. Cumulative $7,647.06, against $6,500.00 recognized under
  the current practice. Catch-up $1,147.06 (below materiality, disclosed). Contract
  liability $12,352.94.

## 12. Oak: commissions that must be capitalized

- **Deciding facts.** The AE's 10% and the manager's 1% override are paid only because
  Oak signed, so both are incremental. The SDR's $500 is paid whether or not the prospect
  signs, so it is not. Renewal commissions (2%) are not commensurate with the initial 10%,
  and customers stay 3 years on average.
- **Treatment.** Capitalize $6,600.00 and amortize it over the expected benefit period,
  including anticipated renewals: 3 years from 2026-04-01. The one-year practical
  expedient is not available, because the amortization period is longer than one year.
  Expense the SDR's $500.
- **Accepted alternative.** The split approach (PwC Viewpoint 11.4). The part of the AE
  commission matching the 2% renewal rate ($1,200) is amortized over the 12-month term,
  and the excess ($4,800) plus the $600 override over 36 months. That gives $250.00 in
  July and a $5,600.00 asset (`alternatives/oak-bifurcated.json`). It becomes the client's
  policy and applies to every contract.
- **Template trap.** Expensing all $7,100 as paid (the plan's stated practice), under the
  one-year expedient.
- **July.** Amortization $183.33. Cumulative $733.33. Deferred commissions asset $5,866.67.
  Correction: move $6,600.00 from April expense to the asset, less $733.33 amortization
  through July.

## Held-out scenarios

No file under `skills/` mentions scenarios 13 to 15, not even as a pattern. The principles
cover them only in general terms. They test whether a run reasons from the documents.

## 13. Lumen: a hosted deal that may contain a software license

- **Deciding facts.** Section 4.3: the customer may download the current release and run
  it itself or with another host, for the rest of the term, at no additional charge.
  Fees do not change if it self-hosts, and a self-hosted copy gets no new releases.
  `product-notes.md`: nine customers already run the on-premise edition on standard
  Kubernetes.
- **The judgment.** A hosting arrangement contains a license only if the customer can take
  possession without significant penalty. The documents cut both ways. Nothing extra is
  charged and self-hosting is common, which points to no significant penalty and a
  license. But fees keep running after self-hosting, and future releases stop. The
  Deloitte Roadmap (12.2.1) lists both as indicators of a penalty. A passing memo names
  both sides and decides.
- **Key's treatment.** No significant penalty: the customer pays the same either way and
  loses only releases it can do without for a term license. So the contract holds a term
  license (functional IP) recognized when download opens on 2026-07-01, plus hosting,
  recognized ratably. SSP: license $45,000 (the standalone median). Hosting has never been
  sold standalone, so its SSP is uncertain: cost plus margin gives $20,000.
- **Accepted alternatives** (in `alternatives/`):
  - A significant penalty, so pure SaaS at $5,000.00 a month, with no correction.
  - Residual SSP for hosting (uncertain, never sold standalone): July $46,250.00.
- **A strong answer also addresses** whether the right to download "the current release
  at any time" is a separate promise of later versions, and whether the $45,000 standalone
  licenses include support.
- **Template trap.** $5,000 a month as a subscription with the self-hosting clause never
  analyzed.
- **July.** Revenue $43,076.92 (license $41,538.46, hosting $1,538.46). Contract liability
  $16,923.08. Correction +$38,076.92, itemized for approval.

## 14. Kestrel: cash paid to the customer

- **Deciding facts.** The letter agreement: $6,000 paid to help Kestrel exit its old
  vendor, with nothing required from Kestrel in return.
- **Treatment.** Consideration payable to a customer, with no distinct good or service
  received for it. It reduces the transaction price to $42,000, recognized over the
  12-month term. The reduction is recognized as the related revenue is recognized, since
  the payment came first.
- **Accepted presentation.** Net within the contract (contract liability $38,500.00), or
  gross ($44,000.00 deferred revenue and a $5,500.00 asset for the unamortized payment),
  if the memo explains the choice. Either way July revenue is $3,500.00.
- **Template trap.** $6,000 to marketing expense and $4,000 a month of revenue.
- **July.** Revenue $3,500.00. Reverse the $6,000.00 marketing expense.

## 15. Osprey: a side letter changes the term and adds a refund right

- **Deciding facts.** The CEO-signed, countersigned side letter from the week of signing:
  two free months extending service to 2027-06-30, and a refund right if the integration
  misses 2026-07-31. `integration-status.md` confirms the integration went live on
  2026-05-20.
- **Treatment.** The side letter is part of the contract. It is binding, and it was signed
  with the order form. The service period is 14 months for a fixed $36,000, so $2,571.43 a
  month. The refund right is variable consideration. With the integration live and
  confirmed in writing, the refund is not expected and no constraint applies. Before
  2026-05-22 the memo would have had to weigh it.
- **Template trap.** $3,000 a month over the 12 months on the order form, with the side
  letter never read.
- **July.** Revenue $2,571.43. Cumulative $7,714.29 against $9,000.00 booked: reduce revenue
  by $1,285.71 (below materiality, disclosed). Contract liability $28,285.71.

## Held-out round 2

Added after the first blind run, to test the fixes on contracts no run has seen. As with
13 to 15, nothing under `skills/` mentions them.

## 16. Heron: blend and extend

- **Deciding facts.** The amendment extends the same 200 seats to 2028-06-30 for $27,000
  over 18 months, which is $1,500 a month. The account manager's email calls it "well under
  our renewal pricing" and a one-time approval. The renewal median is $117 a seat, so
  $1,950 a month.
- **Treatment.** The extension adds distinct service periods, but not at standalone price,
  so it is not a separate contract. The remaining periods are distinct from those already
  delivered. So the change is prospective: the $12,000 unrecognized on the 2026 term plus
  the $27,000 added, spread over the 24 months from 2026-07-01, is $1,625.00 a month.
- **Template trap.** Keeping $2,000 a month through December, then $1,500. That front-loads
  revenue into the months Heron paid the old rate for.
- **July.** Revenue $1,625.00. Contract liability $10,375.00. Correction to booked
  −$375.00, cumulative (July only). The contract liability runs off to zero by
  2028-06-30 ($2,250 at 2026-12-31). It never becomes a contract asset.

## 17. Tern: a minimum commitment drawn down by usage

- **Deciding facts.** The order form grants platform access for the full term, sets a
  $60,000 minimum invoiced regardless of usage, and says unused commitment is forfeited.
  The customer's ops lead expects 450,000 events, well under the 600,000 the minimum
  covers.
- **Treatment, and the judgment it rests on.** The answer turns on the nature of the
  promise, and a memo must argue it both ways.
  - The key's view: Tallow promises stand-ready access for the year, and the customer
    pays $60,000 for that access whatever it uses. That is a series of identical monthly
    periods, recognized ratably at $5,000.00 a month.
  - Accepted alternative: the promise is to process events, with the unused commitment
    as expected breakage recognized in proportion to usage. That gives $0.1333 per event
    on the 450,000 expected ($5,333.33 in July, $33,333.33 cumulative;
    `alternatives/tern-units-view.json`).
  - A memo that picks one without arguing against the other fails criterion 2.
  - The units view recognizes breakage in proportion to use only if Tallow expects to be
    entitled to it. Tern is one first-year customer, and the only evidence is one ops
    lead's forecast. A memo that finds that too thin, and recognizes the shortfall when
    use becomes remote, lands on the client's current numbers legitimately. The memo has
    to make that argument.
- **Template trap.** $0.10 per event with the shortfall taken in December, adopted without
  deciding what the customer is buying.
- **July.** Revenue $5,000.00. Contract liability $10,000.00. Correction to booked
  +$10,000.00 cumulative, above materiality and itemized. Under the alternative: July
  $5,333.33, liability $11,666.67, correction +$8,333.33.

## 18. Plover: two papers, one deal

- **Deciding facts.** The AE's email of 25 June: the $10,000 SOW price was conditional on
  the seats at list, and "two papers because legal wants the SOW separate". The SOW was
  signed eight days after the order form, with the same customer. The workflow design is
  normally about $17,000 (rate card: 100 hours at the $168 standalone effective rate is
  $16,800), and the customer keeps the designs on its own.
- **Treatment.** Combine the two contracts. They were negotiated as a package, and one's
  price depends on the other. There are two performance obligations, subscription and
  workflow design, both distinct. The combined $58,000 is allocated by standalone price:
  seats at the $114 new-logo median ($45,600) and design at $16,800. That gives
  $42,384.62 to the subscription (ratable) and $15,615.38 to design (over time, 40 of 100
  hours in July).
- **Accepted alternative.** Other supportable SSP points, documented.
- **Template trap.** Two contracts at invoice prices: $4,000 of subscription and nothing
  for services until the SOW is invoiced (the client's practice), or $4,000 of services
  at 40% of $10,000.
- **July.** Revenue $9,778.20 (subscription $3,532.05, design $6,246.15). Contract liability
  $38,221.80, net for the combined contract. Correction to booked +$5,778.20, above
  materiality.
