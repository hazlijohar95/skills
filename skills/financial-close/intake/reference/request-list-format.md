# Missing-items request list format

The request list is a message the accountant can forward to their client unedited. Write it
for a business owner, not a bookkeeper.

Rules:

- One line per item. Name the document, the account it covers, and the period.
- Say what each item unblocks in plain language ("so I can verify your checking account
  balance"), never in close jargon ("required for cash substantiation").
- Group by how the client would fetch them: bank portal items together, payroll items
  together, "reply with an answer" items last.
- No blame framing. The list is a normal part of a close, not a deficiency notice.
- End with the single most useful item if they only do one thing today.
- Uncategorized or vague spend gets one summary line here at most ("six July payments
  totaling X came through with vague descriptions"); the item-level questions belong to
  the categorize phase, which asks them properly.
- Sound like their accountant: sentences end in periods, and the warmth comes from being
  specific and brief, the way a good accountant's actual emails read.

Template:

```markdown
Hi <name>, to finish the <period> close I need a few things:

**From your bank portal**
- <Bank> checking statement for <period> (verifies the account ending <last 4>)
- <Card> statement for <period>

**From <payroll provider / lender / system>**
- <item> for <period>

**Quick answers**
- <one-line question the client can answer from memory>

If you only get to one today, the <item> matters most: it unblocks <impact>.
```
