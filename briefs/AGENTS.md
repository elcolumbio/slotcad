# AGENTS.md — rules for any agent working in this repo

This repo is deliberately empty of secrets. Nothing in it is confidential, nothing here talks to a
private system, and no credential belongs in it — not in a file, not in an example, not in a test.

## The task

`PROMPT-1-research.md` runs first and writes into `research/`. It settles which vendors' CAD may be
redistributed.
`PROMPT-2-build.md` builds the library. **Commit no vendor STEP file unless phase 1 cleared it** —
default assumption is that it may not be redistributed. What ships is the *measurements* derived from
it, in `registry/`, each with the source URL and a checksum.

Read the research output before writing code.

See `LEGAL.md` before deciding what to publish. Its short version: link freely and name the vendor,
claim no relationship, ship measurements and never their files, never mirror the catalogue or prices,
and refuse to emit a cut list the tool cannot stand behind.

## Scope

- Work **only inside this repository**. Do not read, write or list anything outside it, and do not
  walk up to a parent directory. There is nothing here that needs the rest of the machine.
- Do not push to any remote. Commit locally; a human reads the diff before anything is published.
- Do not add telemetry, analytics, or any call-home. Do not upload repository contents anywhere.

## How the code is written

- Python, run as `uv run python -m <module>`. A `Makefile` is the source of truth for how to run
  anything; every command shown in the README exists as a make target.
- Standard library first. Every third-party dependency is justified in one line of comment in
  `pyproject.toml`. SQLite for append-only state (`PRAGMA busy_timeout=30000`); DuckDB only if an
  analytical query genuinely needs it; never both over the same data.
- HTML deliverables are self-contained: f-strings, `html.escape`, inline CSS. No Jinja, no framework,
  no build step, no JS requirement to read a page.
- English throughout — code, comments, commits, README, site copy. This repo has an international
  audience.
- Commit messages: one lower-case line saying what changed and why. No `feat:` prefixes.
- Tests use real fixtures captured from live responses, committed once. Never mock a fetcher against
  a hand-written dict that has never existed in the wild.

## How the data is treated

- Every dimension carries its provenance: `measured` (from the vendor solid), `vendor` (a published
  table), or `assumed` (a default nobody checked). An `assumed` value never reaches a cut list
  without a visible flag.
- A failure is stored as a failure, never as a result. An errored fetch is `status='error'` and does
  not count as covered — otherwise an outage reads later as "this employer posts nothing".
- The bill of materials and the geometry come from one topology object, always. A test asserts that
  changing a parameter changes the cut list — the claim is the product, so it is tested.
- Mixing fastener families is a hard error, never a warning. A failed interference check emits no
  cut list.
- Anything scheduled is a systemd user timer with `Persistent=true`, never cron.
- No personal data at any point. Names and contact details found in postings are dropped at ingest,
  not filtered at render.
- Nothing behind a login, paywall or bot gate is ever fetched. `robots.txt` is obeyed by the code that
  actually does the fetching, not by a separate checker that ignores it.
