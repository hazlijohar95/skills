# Reconciling item classification

Every unmatched item lands in exactly one bucket. The bucket decides what happens next.

## Bucket 1: timing

The transaction is real and recorded on both sides; the periods just straddle. Deposits in
transit, outstanding checks, card charges posted after cutoff, ACH in flight.

**Test:** the item clears within a normal window after period end (checks: weeks; electronic
items: days).
**Resolution:** no entry. List the item on the proof and confirm it cleared when the next
statement arrives.

## Bucket 2: adjustment required

One side is right and the GL is wrong or incomplete. Bank fees and interest not yet booked,
processor fees netted from deposits, recorded amounts that differ from cleared amounts, items
recorded to the wrong account.

**Test:** outside evidence shows a real transaction or a real amount the GL does not.
**Resolution:** route to the adjust skill via the exceptions register with account,
amount, and reason. The reconciliation itself books nothing.

## Bucket 3: investigate

Cannot yet be placed in bucket 1 or 2. Unrecognized withdrawals, duplicate-looking deposits,
differences with no candidate match, anything that smells like error or fraud.

**Test:** you cannot state which side is right.
**Resolution:** document what was tried, keep the item on the exceptions register, and
escalate to the user. An investigate item never converts to timing just because the period
needs to close.

## Aging rules

- A timing item that fails to clear by the next statement becomes investigate.
- Outstanding checks older than 90 days: flag for reissue or void; a void is an adjustment.
- Any investigate item older than one period blocks calling the account reconciled.

## Escalation

| Trigger | Action |
| --- | --- |
| Unexplained difference above materiality | Account is blocked; close cannot call it reconciled |
| Suspected unauthorized transaction | Stop matching, tell the user immediately |
| Same item recurring three periods | Recommend a root-cause fix in the close memo |
