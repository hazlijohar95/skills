### Policy setup

**You own the client's revenue policy until the user approves it.** The output is one
policy per revenue stream: the standard terms, the treatment those terms produce, and the
list of deviations that send a contract to its own analysis. After that, most contracts
cost a lookup and the judgment goes where the terms differ.

1. Confirm 606 applies. GAAP-basis financial statements, or a reader who expects them
   (lender, investors, an audit or review). Tax-basis or cash-basis books stop here: say
   so and name what the client would need to change.
2. Inventory the revenue streams from the GL revenue accounts, the billing export, and the
   contract templates (MSA, standard order form, SOW template, reseller and marketplace
   agreements). One stream per distinct combination of product, contract template, and
   billing pattern.
3. For each stream, work the five questions from SKILL.md against the standard template,
   reading each principle's leaf file as you apply it. Write down the deciding term in
   the template for every conclusion.
4. Build the SSP evidence per product from standalone sales, price books, and partner
   pricing. State the range and the point used. Where there is no observable evidence,
   say which estimation method applies and why.
5. Draft the elections with the user: portfolio approach per stream, daily or monthly
   convention, the one-year commission expedient, the right-to-invoice expedient for time
   and materials, the financing expedient, nonpublic disclosure elections. Each gets one
   sentence of consequence. Nothing is assumed.
6. Write the deviation list per stream: the terms from
   [../reference/reading-list.md](../reference/reading-list.md) that, when present, move
   a contract out of the stream policy and into the Contract playbook.
7. Test the policy against the open book. Build a contract file for every open contract
   (standard ones straight from the policy), run `closekit rev schedule` and
   `closekit rev balances` through the current period, and compare with the client's
   deferred revenue, unbilled, and revenue by stream. Every difference is explained by a
   named contract and cause, or it is a finding.
8. Send the policy memo, the elections, and the cumulative difference to the
   `close:rev-challenger` agent. A policy always gets second review, whatever the
   profile's setting, because it decides every contract in the stream.
9. Present for approval: the stream policies, the elections, and the transition
   adjustment with its amount and whether it corrects prior periods. Log each approval.
   Save the stream policies and elections to the client profile's Revenue section.

**Done when** every revenue stream in the GL has a policy with its deciding template
terms, every product has an SSP basis, every election is approved or listed as an open
question, every open contract has a contract file, and every difference between the kit's
balances and the client's books is traced to a named contract and cause.

**Reply:** streams and their treatments, elections, SSP basis per product, the
difference against the current books by cause, and the deviations that route contracts
to their own memo.
