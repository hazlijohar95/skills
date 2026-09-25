# Changelog

## 0.7.0

First public release.

- Financial close: `close`, `setup-client`, `intake`, `prep`, `reconcile`, `categorize`, `adjust`, `journal-entry`, `review`, `deliver`.
- Technical accounting: `revenue-recognition` (ASC 606 for subscription and services contracts).
- Agents: `close-reviewer` and `revenue-challenger`, each run in a fresh context that sees only the files.
- The close kit (`scripts/closekit.py`): `tb`, `tie`, `je`, `fingerprint`, `lint`, `log`, `rev`.
