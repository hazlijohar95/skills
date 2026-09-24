---
name: prep
description: The prep phase of a close, reconciliation then transaction categorization. Use when prepping a period for close, or when the user wants reconciliation and categorization run together.
---

# Prep

## Summary

The prep phase, as one call: prove the accounts, then clean the transactions. This skill
sequences two workers and owns nothing else.

## Workflow

1. Run the reconcile skill for the period.
2. Run the categorize skill with the same close context. Both write to the same exceptions
   register.
3. Prep is done when both report their completion criteria met. Batch the two skills' open
   questions into one boundary checkpoint rather than two.

A blocked worker stops prep; route its exceptions to the phase that owns them and say
where things stopped.
