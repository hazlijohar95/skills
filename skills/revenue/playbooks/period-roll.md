### Period roll

**You own tying the revenue schedule to the books.** Judgment happened in the other
playbooks. This one updates the facts, runs the kit, and finds what the facts no longer
cover.

1. Collect the period's facts: billing export, usage by customer and month, hours and
   estimates at completion for projects, credits issued or owed, amendments signed, new
   contracts, terminations, cash from marketplaces and resellers.
2. Route anything new before rolling. New contracts go to their stream policy, or to the
   Contract playbook if they deviate. Amendments, concessions, and terminations go to the
   Modification playbook. A usage or credit term the contract file doesn't model is a
   deviation. Nothing new is scheduled from a template.
3. Update the contract files: append usage and progress for the period, add re-estimates
   as `cumulative` events, add billings. Re-check each open estimate (variable
   consideration, progress totals, breakage rates) against this period's evidence and
   log what changed and why.
4. Run `closekit rev schedule --from <period> --through <period> --out` and
   `closekit rev balances --asof <period>` over every contract file.
5. Tie to the trial balance: revenue by stream, deferred revenue, unbilled receivables,
   contract assets, refund liabilities, deferred commissions and their amortization.
   Each difference gets a named contract and cause. An unexplained difference goes on the
   exceptions register, never into a plug.
6. Draft the entries under the je skill's contract, citing the schedule rows and memos
   they come from. An entry from an unapproved position stays proposed.
7. File the schedule, balances output, and tie-out in `workpapers/revenue/`. When run
   inside a close, hand the entries to the adjust skill's register.

**Done when** every contract billed, used, or amended this period has an updated
contract file, every balance the kit reports ties to the trial balance or sits on the
exceptions register with its cause, and every proposed entry cites its schedule rows.

**Reply:** revenue by stream against the books, balance tie-outs, entries proposed, and
the contracts routed to a playbook this period.
