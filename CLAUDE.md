Skills are organized into bucket folders under `skills/`:

- `financial-close/`: the close and its phases, run from trial balance and GL exports
- `technical-accounting/`: judgments under an accounting standard, made from source documents (ASC 606 today)

A new bucket is created when its first skill needs it, not before. Use `in-progress/` for a skill that is public but not shipped, and `deprecated/` for one that is retired; neither is listed in `.claude-plugin/plugin.json` or the top-level `README.md`.

Every shipped skill has all of these, and a skill is not added, renamed, or removed until each one is updated:

- an entry in `.claude-plugin/plugin.json`'s `skills` array (the plugin ships exactly that list)
- a wrapper at `commands/<name>.md` that loads the skill and passes the plugin root
- a line in its bucket's `README.md` and in the top-level `README.md`, with the name linked to its `SKILL.md`, grouped into **User-invoked** and **Model-invoked**
- its terms in `CONTEXT.md`, when it introduces a term another skill or a user will use

Run `claude plugin validate . --strict` and `claude plugin validate .claude-plugin/plugin.json` after touching any manifest. The second one warns that this file is not loaded as plugin context; that is intended, since it is for maintainers, and it is the only warning allowed. Bump `version` in `.claude-plugin/plugin.json` and `plugin.json` together.

## Naming

A phase skill is named for its phase (`intake`, `prep`, `reconcile`, `categorize`, `adjust`, `review`, `deliver`), because `close` maps phase to skill one to one. Every other skill names its job in full words an accountant would say: `journal-entry`, not `je`; `revenue-recognition`, not `revenue`. Agents are named for their role (`close-reviewer`, `revenue-challenger`) and are addressed as `better-accountant-skills:<agent>`.

Close log values (the `phase` column, such as `je` in `closekit log ... je approve`) are a data format the kit reads, not skill names. Renaming a skill never renames them.

## Invocation

- **User-invoked**: `disable-model-invocation: true`. Only a person can start it, and its `description` is one human-facing line. `close` is the only one, because starting a close is a decision.
- **Model-invoked**: the default. The `description` keeps its "Use when..." triggers so the agent reaches for it. `setup-client` stays model-invoked because `close` offers to run it; a user-invoked skill cannot be reached from another skill.

## Paths inside skills

Skills are not self-contained; see [.agents/adr/0001-ship-as-a-plugin.md](./.agents/adr/0001-ship-as-a-plugin.md). They reach shared files through `<plugin root>/...`:

- `scripts/closekit.py`, the close kit
- `skills/financial-close/close/reference/asking.md`, the shared rules for questions

Each `SKILL.md` locates the root from its own path ("three levels above this file"), each agent from `scripts/closekit.py`, and each command passes `${CLAUDE_PLUGIN_ROOT}`. Moving a skill changes all three; grep for the old path before committing.

## Prose

No em dashes anywhere: skills, docs, READMEs, ADRs, code comments. Rewrite the sentence with a comma, colon, period, or parentheses. `python3 scripts/closekit.py lint <file>` enforces this and the rest of the house style; run it on every document you change.

## Verifying a change

- `python3 tests/test_closekit.py` is the kit's self-check. Run it after any kit change.
- `tests/fixtures/acme-2026-07/` is a small client with planted defects listed in `answer-key.md`. After a skill edit, copy the CSVs (not the answer key) into a neutral workspace such as `clients/acme/`, run `/close Acme Co 2026-07` with `claude --plugin-dir <this repo>`, and grade the run against the key.
- `tests/fixtures/revenue/` holds Tallow Labs, a SaaS and services client whose contracts each turn on one fact buried in its documents. `answer-keys/` grades them. Scenarios 13 onward are held out: nothing under `skills/` may mention them.
- Run fixtures blind. Copy the plugin without `tests/`, and keep words like test and eval out of anything the run can see; an agent that knows it is graded behaves differently.
- A skill edit is settled by running it, not by argument: delete the line, rerun the fixture, and if the result holds, it stays deleted.

## Release

`git archive --format=zip -o better-accountant-skills.zip HEAD` builds the upload zip for Claude and Cowork. `.gitattributes` keeps `tests/`, `.agents/`, and this file out of it.
