# CPA sign-off: revenue answer keys

For a licensed US CPA reviewing the Tallow Labs keys before they gate a release. Each row
is a judgment where the key picks one answer and accepts others. The mechanics (kit
arithmetic, deciding facts present in the documents) were checked by an adversarial
review against Deloitte DART and PwC Viewpoint in September 2026. What's left needs a
professional's call.

For each row, tick the treatment you would accept as the key's main answer, strike any
you would fail, and initial. Numbers are July 2026, from `closekit rev` over the files
named. `README.md` has the full reasoning for each scenario.

| # | Question | Key's answer (July) | Alternatives (July) | Accept key | Also accept | Initials |
| - | -------- | ------------------- | ------------------- | ---------- | ----------- | -------- |
| 13 | Lumen: is paying the same fee after self-hosting, and losing future releases, a significant penalty? Is "download the current release at any time" a separate promise of later versions? | License plus hosting, $43,076.92 (`lumen.json`) | Pure SaaS, $5,000.00 (`alternatives/lumen-pure-saas.json`). Residual SSP for hosting, $46,250.00 (`alternatives/lumen-residual-ssp.json`) | [ ] | [ ] [ ] | |
| 9 | Willow: is the engagement one performance obligation (cumulative catch-up) or a series of distinct hours (prospective)? | One obligation, $4,250.00 (`willow.json`) | Series, $5,500.00, contract asset $1,250.00 (`alternatives/willow-prospective.json`) | [ ] | [ ] | |
| 1 | Northwind: does the subscription start at access (2026-02-27) or on the contract date? Is a 20% renewal discount against new-customer pricing a material right? | Access and material right, $2,348.48 (`northwind.json`) | Contract date, $2,166.67 (`alternatives/northwind-from-contract-date.json`). No material right, $2,500.00 (`alternatives/northwind-12-month-fee.json`) | [ ] | [ ] [ ] | |
| 17 | Tern: is the promise stand-ready access or a quantity of events? Is one ops lead's forecast enough to recognize expected breakage? | Stand-ready, $5,000.00 (`tern.json`) | Units with proportional breakage, $5,333.33 (`alternatives/tern-units-view.json`). Units with breakage when remote: client's $4,000.00 | [ ] | [ ] [ ] | |
| 5 | Birch: is the prepayment beyond the 60-day window a refund liability or deferred revenue? | Split: $4,000 contract liability, $6,000 refund liability | One $10,000 contract liability, with the refund right addressed | [ ] | [ ] | |
| 6 | Alder: which SSP applies to the original 100 seats at inception and at the modification (new-logo $114, renewal $117, add-on $118)? Is $100 a supportable "adjusted for circumstances" price for a retention deal? | $114 at inception, $118 at modification, prospective, $1,299.56 | $114 held for original seats, $1,292.97. Separate contract, only with an SSP argument for $100 | [ ] | [ ] [ ] | |
| 12 | Oak: amortize the commission over customer life, or split it (renewal-rate part over the term, excess over the life)? | Single 36-month period, $183.33 (`oak-commissions.json`) | Split, $250.00 (`alternatives/oak-bifurcated.json`) | [ ] | [ ] | |
| 4 | Cedar and Willow: is a credit applied to the next invoice for future service a refund liability, or in substance a contract liability? | Refund liability, presented apart | Contract liability, if the memo argues the credit is settled only against future service | [ ] | [ ] | |
| 2 | Harbor: is "no significant financing component" supported by the size of the effect alone (about 1% to 2%)? | No adjustment, $7,500.00 | Adjust for financing (key would fail this) | [ ] | [ ] | |

Reviewer: ______________________  License state and number: ______________  Date: __________

After sign-off, change the keys and `expected-2026-07.csv` to match any row where the
reviewer's pick differs from the key, rerun `python3 tests/test_closekit.py`, and record
the reviewer and date at the top of `README.md`.
