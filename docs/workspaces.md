# Workspaces, clients, and teams

Where a close keeps its files, how to set up one Claude Project per client, and how a team shares closes. The skills work out the layout for themselves; this page is for the person setting it up.

## What a close needs from you

- Trial balance for the period (and the prior period, for roll-forwards and flux)
- General ledger detail export (CSV or Excel, from any system)
- Bank and credit card statements for the accounts you want reconciled (optional but
  recommended)

Missing pieces never stall the run: the readiness report tells you exactly what is missing and
what it blocks, and the close finishes with disclosed exceptions rather than guesses.

## One Claude Project per client

The plugin detects which layout you use, no configuration needed:

- **Shared workspace** (all clients in one place): profiles at `clients/<name>/profile.md`,
  closes at `closes/<name>/<period>/`. Invoke with the client name: `/close Acme Co 2026-07`.
- **One project per client**: the whole workspace belongs to that client. The profile sits
  at the root as `profile.md`, closes at `closes/<period>/`, and the client name becomes
  optional: `/close 2026-07`.

First-time setup for a client project (once per client, two minutes, all done by you, not
by the plugin):

1. Create the Claude Project named for the client.
2. Upload the client's standing documents to the project's knowledge: prior close package,
   schedules, anything the close should always know.
3. Run `/setup-client` once; add the profile it produces to the project's knowledge (or
   paste its block into the project's instructions).
4. Sharing this client with teammates? Add one line to the project's instructions naming
   where close artifacts live (a shared folder everyone connects), e.g.
   `Close state home: Dropbox/Clients/Acme`. Solo, skip this; the workspace is the default.

From then on, start sessions inside the client's project: Claude uses the project's
knowledge as context, so every session begins already knowing the client. Cowork never
writes to a project's knowledge, so files stay the single source of truth: the plugin
writes updates to files and reminds you when the knowledge copy drifts.

## Working as a team

Close state is derived from evidence (the books, the workpapers), not from any one file,
so a teammate's Claude can size up where a close stands from whatever artifacts it can
see. To share those artifacts, connect the same synced folder (Dropbox, Drive, OneDrive, a
network share) as the client workspace on each desktop. Profiles, workpapers, and the
close log become shared: resuming a colleague's half-done close plays back where they left
off, the log shows who approved what, and a reviewer can run `review` on any close
folder regardless of who prepared it.

One convention to keep: one preparer owns an in-flight close at a time. The files have no
locking; simultaneous runs on the same period will conflict the way any shared drive does.

No shared folder? If your Claude has a cloud storage connector (Drive, OneDrive, Notion),
the close package and client profile can be saved there at delivery, the same shared-drive
idea without the desktop folder setup.
