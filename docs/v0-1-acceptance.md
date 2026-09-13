# v0.1 acceptance record

**Closed:** 2026-09-13
**Accepted by:** Charles Yang Lin, project author
**Decision:** AB-D017
**Tag:** `v0.1.0`

AB-D013 made practical acceptance depend on building and reviewing the first real agent
rather than on a predetermined checklist. This record closes that loop.

## What acceptance rested on

- Sean's independently generated project for sourcing secondhand laboratory equipment, taken
  through Define and Plan by an author new to agent building.
- Additional author use cases outside this repository.
- The author's judgment on 2026-09-13 that Agent Builder works as intended for its stated
  purpose: a consistent, governance-first starting point for agents.

Full transcripts, Sean's repository, and the other use cases are not published here. This
record states what the decision rested on; it is not evidence reproducible from this checkout.

## Mechanical evidence

`docs/validation.md` records the 2026-09-08 build: 8 builder tests, 3 generated-project tests,
Ruff 0.16.6 lint and format, Python compilation, and a clean wheel install. Tests and
compilation were re-verified on 2026-09-12 under Python 3.14.0. Structural tests do not prove
agent adherence, performance, or behavior on any particular host.

## Findings carried into v0.2

Neither finding blocked acceptance. Both are input to Define, not confirmed scope.

### F-001 — Resume still requires manual coaching

Cross-account, cross-host resume succeeded on 2026-09-13: a session with no prior conversation
recovered the phase, confirmed decisions, pending work, and next step from the repository
alone. It succeeded because the author supplied a prompt naming the five files to read.
Whether a fresh agent finds and follows `AGENTS.md` unprompted — by way of `CLAUDE.md` or
`GEMINI.md` — remains untested and host-dependent. Instruction files guide behavior; they do
not guarantee host enforcement or automatic loading.

### F-002 — Host Python version is an unguarded prerequisite

Agent Builder itself requires Python 3.11 or newer, because its tests import `tomllib`. It
ships no container of its own: AB-D010 containerization applies to generated agents, not to
the builder. Observed consequences: Sean's Windows onboarding stalled on missing Git and
Python, and a 2026-09-13 review environment running Python 3.10 could not execute the test
suite. There is no preflight check and no failure message that explains the requirement at
the point where it bites.

The failure is not limited to the test suite. Both entry points abort on import, because
`agent_builder.scaffold` imports `datetime.UTC`, which is Python 3.11+. Reproduced on
2026-09-13 under Python 3.10.12:

```sh
$ python3 scripts/new_agent.py ./smoke-agent --name "Smoke Agent" --purpose "..."
ImportError: cannot import name 'UTC' from 'datetime'

$ python3 scripts/validate_project.py ./smoke-agent
ImportError: cannot import name 'UTC' from 'datetime'
```

A first-time user on an older Python sees a stdlib `ImportError` naming `datetime`, with
nothing pointing at the real cause or the required version. This is the concrete shape of
the friction; it is evidence for Define, not a decision about how to resolve it.

AB-D018 records one candidate response as `proposed`, not confirmed.

## Not closed by this record

- Onboarding kit review — `docs/onboarding-kit-review.md`, AB-R001 through AB-R003.
- Existing-project adoption — `docs/existing-project-review.md`, AB-R004.
- Cowork adoption note — `docs/COWORK_EXISTING_PROJECT_ADOPTION.md`, derived from `1057a49`
  and predating Nokkvi's law. Reassess before adopting it.
- Runtime and environment profiles, deferred by AB-D008.
- Dependabot PR #1, `prek` 0.4.11 to 0.5.2. Left open deliberately so the `v0.1.0` tag matches
  the pins the validation evidence was produced against. It is a development-only optional
  dependency; CI does not use it.
