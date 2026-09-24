### Modification

**You own the line between a changed contract and a changed estimate.** The method
decides whether the past moves, so the reasoning behind it goes in writing.

1. Read the change document and everything around it (deal-desk approvals, sales emails,
   the customer's request). Date it when the parties approved it, not when it was invoiced.
2. Decide whether enforceable rights changed. Nothing signed or agreed, only a forecast or
   estimate moved: this is a re-estimate. Update the contract file with a
   `method: cumulative` event whose `price_change` is the estimate change, and go to
   step 6.
3. Separate-contract test: are the added goods or services distinct, and priced at SSP
   adjusted for this customer's circumstances? Compare the unit price with the stream's
   SSP range and name the deciding evidence (the range, a deal-desk note calling it a
   concession).
4. Otherwise, remaining goods or services distinct from those delivered: prospective.
   Not distinct (a partly done single obligation): cumulative. A mix: each part its way.
   Read [../principles/modifications-change-the-future.md](../principles/modifications-change-the-future.md)
   and write the rejected method with the fact that rejects it.
5. Update the contract file: a `modifications` entry with the method, the date, the price
   change, and the obligations as they stand after the change (for prospective, only what
   remains, with SSP at the modification date).
6. Run `closekit rev allocate` and `rev schedule` for the modification period and after.
   Compare with what the client booked.
7. Second review per the profile's setting, as in the Contract playbook. Then memo, lint,
   approval.

**Done when** the memo names the method chosen and the method rejected, each with its
deciding fact, the contract file's modification entry reproduces the memo's figures in a
kit run, and the correction to what was booked is stated cumulatively.

**Reply:** the Revenue block, naming the method chosen and the one rejected.
