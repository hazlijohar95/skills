# Ship as one plugin; skills are not installed one at a time

Matt Pocock's skills repo, whose layout this repo follows, keeps every skill self-contained, so `npx skills add` can copy any single skill folder into a project. These skills cannot work that way, and we do not pretend they can.

## Why

Three things every skill here depends on live outside any one skill folder:

- **The close kit** (`scripts/closekit.py`). Every figure comes from an executed check, never from arithmetic in prose. A skill without the kit falls back to "manual, not kit-verified", which is the failure the kit exists to prevent.
- **The agents** (`agents/close-reviewer.md`, `agents/revenue-challenger.md`). Review and the second look at revenue judgments run in a fresh context that never sees the preparer's account of the work. A copied skill has no agent to spawn.
- **Shared rules** (`skills/financial-close/close/reference/asking.md`). How to put questions and approvals to the user is written once and read by every skill.

Copying the kit into each skill would give us eleven copies to keep in sync. Moving the agents' work into each skill would make review stop being independent.

## Decision

- Distribute the whole set as one Claude plugin, `better-accountant`: `.claude-plugin/marketplace.json` makes this repo its own marketplace for Claude Code, and `git archive` builds the zip for Claude and Cowork upload.
- `.claude-plugin/plugin.json` lists the shipped skills explicitly, because skills sit one bucket deeper than a plugin's default `skills/<name>/` discovery.
- No skills.sh route, and no Codex plugin, until a skill can find the kit and the agents on its own.
- Skills reach shared files by `<plugin root>/...` paths, and locate the root from their own position. See `CLAUDE.md` for what a move has to update.

## Verified

2026-09-25, Claude Code 2.1.282: `claude plugin validate --strict` passes for the marketplace; the plugin manifest passes with one expected warning (the maintainers' `CLAUDE.md` is not plugin context); and `claude -p --plugin-dir .` loads all eleven skills and both agents under the `better-accountant:` namespace.

Not verified: whether clients that read the root `plugin.json` (Agent Plugins v1 schema, which has no `skills` field) discover skills nested inside bucket folders.
