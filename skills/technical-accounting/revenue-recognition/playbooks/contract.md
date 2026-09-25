### Contract

**You own the conclusion and every fact under it.** One contract, or one group of
contracts the combination test joins, reasoned from its documents to a contract file and
a position memo.

1. Gather every document for the customer: order forms, MSA version, amendments, SOWs,
   side letters, sales and deal-desk emails, usage and time data, billing history. List
   what you read.
2. Triage against the stream policy. Walk the reading list and mark each term present.
   No deviations: build the contract file from the policy, cite the policy, and skip to
   step 7. Any deviation: continue.
3. Work the five questions in order. For each question with a deviation, read the leaf
   principle, write the deciding fact with its file, and write the strongest rejected
   treatment with the fact that rejects it. Questions the policy settles get one line
   citing it.
4. Where a deciding fact is missing, write the question: the fact needed, the document
   that would hold it, and the number under each answer (run the kit both ways).
5. Build the contract file per [../reference/contract-file.md](../reference/contract-file.md).
   Run `closekit rev allocate`, `rev schedule` through the current period, and
   `rev balances`. Paste the commands and output into the memo.
6. Compare with what the client booked. Quantify the difference by period and by account.
7. When the profile's second-review setting (SKILL.md) covers this conclusion, spawn
   `better-accountant-skills:revenue-challenger` with the documents folder, the draft memo, and the plugin root,
   nothing else. Resolve each
   challenge: accept it and revise, or answer it with a fact. Unresolved means open, and
   both treatments go to the user with their numbers.
8. Write the memo per [../reference/position-memo.md](../reference/position-memo.md),
   lint it, and present it for approval with the questions batched.

**Done when** every reading-list term is marked present or absent, every judgment carries
a deciding fact and a rejected alternative, every figure in the memo appears in its kit
output, the challenger has run or the memo says why not, and the memo lints clean.

**Reply:** the Revenue block from SKILL.md, plus the memo and contract file paths.
