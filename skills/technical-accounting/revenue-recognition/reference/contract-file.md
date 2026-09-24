# Contract file

One JSON file per contract (or per group of combined contracts), in
`workpapers/revenue/contracts/` for a close, or next to the memo when running standalone.
The file holds only conclusions. The memo holds the reasoning. `closekit rev` reads it and
does all the arithmetic.

```json
{
  "id": "EX-001",
  "customer": "Example Co",
  "kind": "revenue",
  "convention": "monthly",
  "transaction_price": "20000.00",
  "unbilled": "contract_asset",
  "obligations": [
    {"id": "subscription", "pattern": "ratable", "start": "2026-01-01", "end": "2026-12-31", "ssp": "18000.00"},
    {"id": "training-1", "pattern": "point", "date": "2026-03-10", "ssp": "4000.00"},
    {"id": "overage", "pattern": "usage", "usage": [{"period": "2026-07", "amount": "640.00"}]}
  ],
  "billings": [{"date": "2026-01-01", "amount": "20000.00"}],
  "modifications": [
    {"date": "2026-07-01", "method": "prospective", "price_change": "6000.00", "note": "Amendment 1",
     "obligations": [{"id": "subscription", "pattern": "ratable", "start": "2026-07-01", "end": "2026-12-31", "ssp": "15000.00"}]}
  ]
}
```

## Fields, and the judgment each one records

| Field | Records | Notes |
| --- | --- | --- |
| `transaction_price` | Question 3: fixed consideration plus constrained variable estimates | Excludes amounts on `usage` obligations, which are allocated to their own period |
| `obligations` | Question 2: the performance obligations | A series (SaaS) is one `ratable` obligation |
| `ssp` | Question 4: standalone selling price | Needed when more than one non-usage obligation exists |
| `allocated` | Question 4 when a judgment fixes the split (subset discount, residual) | Give it on every non-usage obligation or none. Must sum to the price |
| `pattern` | Question 5 | `ratable` (start, end), `point` (date), `progress` (cumulative fraction complete per period), `usage` (amount per period, negative for credits) |
| `convention` | Client election | `daily` (default) or `monthly`, which needs whole-month service periods |
| `unbilled` | Presentation | `contract_asset` (right still conditional) or `receivable` (unconditional, just not invoiced) |
| `kind` | `revenue`, or `cost` for capitalized contract costs | A `cost` file's `billings` are the amounts capitalized |
| `billings` | Invoices, dated when issued | Drive the balances, never the revenue |
| `billings` with a negative amount | Consideration paid to the customer, when presented net within the contract | Revenue reduction itself goes in `transaction_price` |
| `modifications` | Changes to the contract, and re-estimates | See below |
| `refund_liability` | Amounts owed back at a period end: credits due, rebates, prepayments refundable on exit. `[{"period": "2026-07", "amount": "1000.00"}]`, the balance at that period end | `rev balances` shows it apart and nets the rest |
| `booked` | What the client already recorded as revenue, per period: `[{"period": "2026-05", "amount": "3000.00"}]` | `rev balances` prints the cumulative correction through the period. Report that figure, never a one-month difference |

## Modifications and re-estimates

- `"method": "prospective"`: the old contract ends the day before `date`. Unrecognized
  consideration plus `price_change` is allocated across `obligations`, which lists only
  what remains, with SSP at the modification date. Every non-usage obligation must start
  on or after `date`.
- `"method": "cumulative"`: `obligations` restates the whole obligation set as it now
  stands, from inception, and the price becomes the old price plus `price_change`. The
  difference in cumulative revenue lands in the modification's period. Use it for
  partly satisfied single obligations and for changes in estimate (progress totals,
  variable consideration), with `price_change` of the estimate change or `"0.00"`.
- Separate contract: a new file. Not a modification entry.

## Progress fractions

`complete` is cumulative, from 0 to 1, for the period it names. Compute it as a fraction
(hours to date over estimated total hours), written with enough decimals that the kit's
rounding lands on the cent: ten places is plenty. For breakage, it is credits used over
credits expected to be used.

## Commands

```
closekit rev allocate <files>                          allocation at inception and after each change
closekit rev schedule <files> --through YYYY-MM [--from YYYY-MM] [--out schedule.csv]
closekit rev balances <files> --asof YYYY-MM           net position per contract
```
