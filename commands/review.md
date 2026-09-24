---
name: review
description: Reviewer pass over a prepared close. Use when reviewing a close before delivery, running flux analysis on draft statements, or when a manager asks to check work a preparer finished.
argument-hint: "[the close folder, or client and period, to review]"
---

# /review

Load `${CLAUDE_PLUGIN_ROOT}/skills/financial-close/review/SKILL.md` and follow it end-to-end.

Plugin root: ${CLAUDE_PLUGIN_ROOT}. Wherever a skill or agent file says `<plugin root>`, it
means this folder. Pass it to any plugin agent you spawn.

Input for this run: $ARGUMENTS
