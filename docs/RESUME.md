# Resume Agent Builder

Checkpoint: 2026-09-13. v0.1 is accepted and closed; release `v0.1.0` is tagged. Agent Builder
is now in **Define** for v0.2, authorized by the project author on 2026-09-13. v0.2 scope is
open. This checkpoint does not approve Plan, Build, or any runtime implementation.

## Recover context

Read these files completely, in order:

1. `AGENTS.md`
2. `governance/project-state.yaml`
3. `governance/operating-agreement.md`
4. `governance/decisions.yaml`
5. This file, then `docs/v0-1-acceptance.md`.

The compact machine handoff is `governance/handoff.json`. Its schema is
`src/agent_builder/templates/base/contracts/schemas/agent-handoff.schema.json.tmpl`.
Current governance and newer author instructions take precedence over this checkpoint.
Check Git status and recent commits before editing. Preserve existing changes.

The root `CLAUDE.md` and `GEMINI.md` direct their coding hosts to `AGENTS.md`. In any chat
environment without repository access, ask the author to supply the required files. Do not
claim to have read unavailable files or assume account memory includes previous sessions.
Instruction files guide behavior; they do not guarantee host enforcement or automatic loading.

## What v0.1 shipped, and what it did not

- A Python 3.11+ scaffold generator and structural validator with no runtime dependencies.
  Entry points: `scripts/new_agent.py` and `scripts/validate_project.py`.
- Generated projects start in Define and select Codex, Claude Code, and/or Gemini CLI adapters.
- Define → Plan → Build → Review with explicit author-approved transitions.
- Engineering defaults: lean Python; deterministic execution; model judgment for orchestration;
  open-source evaluation before custom work; replaceable providers and interfaces.
- Deployment defaults recorded as policy, not artifacts: standalone OCI containers for
  generated agents, Docker Compose locally. External contracts are versioned.
- Secrets never enter committed files, prompts, logs, images, or handoffs.
- Nokkvi's law and practical persistence guidance (AB-D015, AB-D016), committed in `453d8cb`.

No runtime, model client, MCP server, custom API, Dockerfile, or Compose service is supplied.
The initializer refuses existing destinations. Generated projects never update automatically.
Template version remains 0.1.0; record the source Git commit or the `v0.1.0` tag when
comparing tests.

## Acceptance outcome

The author accepted v0.1 on 2026-09-13 under AB-D017, based on Sean's generated sourcing
project taken through Define and Plan and on additional use cases outside this repository.
Those transcripts and repositories are not in this checkout. `docs/v0-1-acceptance.md` records
what acceptance rested on and what it did not close.

Two findings were carried forward rather than treated as blockers:

- **F-001** — resume from repository records works, but the 2026-09-13 test still relied on an
  author-supplied prompt naming the files to read. Unprompted instruction discovery is untested.
- **F-002** — Agent Builder itself requires host Python 3.11+, with no preflight check and no
  container of its own. AB-D018 (proposed) records one candidate response.

The scheduling-agent test remains abandoned; do not resume it here.

## Current phase: Plan for v0.2 — drafted, pending author double-check

Define closed on 2026-09-13; the author confirmed AB-D019 through AB-D024 and authorized Plan.
Read `docs/v0-2-define.md` (what and why) and then `docs/v0-2-plan.md` (how, in what order).

The Plan answers Define's seven open questions, lays out eight small Build commits B1–B8 that
each leave the tests green, and records five further decisions AB-D025 through AB-D029 as
`proposed`. The author has a double-check list in the Plan's section 6. Build starts only when
the author explicitly authorizes it. Do not begin B1 before then.

Open proposals preserved from Review, none of them confirmed product scope:

- `docs/onboarding-kit-review.md` — not in v0.2.
- `docs/existing-project-review.md` — not in v0.2; the future `project` kind is its likely home.
- `docs/COWORK_EXISTING_PROJECT_ADOPTION.md` — derived from `1057a49`, predates Nokkvi's law.
- `docs/SEAN_CODEX_TEST_PACKET.md` — preserves the `1057a49` baseline. Leave Sean's project
  as-is (Plan answer 7).

## Open item outside the phase

Dependabot PR #1 bumps the development-only pin `prek` 0.4.11 → 0.5.2 in `pyproject.toml`. It
was deliberately left open so the `v0.1.0` tag matches the pins the validation evidence was
produced against. `prek` is not a runtime dependency and CI does not use it. If it is merged,
run `prek install` once locally to confirm the `repo = "builtin"` hooks still resolve under
0.5.x.

## Verification

On 2026-09-12, Python 3.14.0 ran these successfully:

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall -q src scripts tests
```

All 8 builder tests passed, including the generated project's 3 tests. Wheel and lint evidence
in `docs/validation.md` applies to its dated build. Structural tests do not prove agent
adherence, performance, or Windows, Claude, or ChatGPT behavior. They were not re-run for the
2026-09-13 closeout, which changed governance and documentation only.

## Next action

Walk the author through the double-check list in `docs/v0-2-plan.md` §6. Record any amendments.
On explicit authorization, begin Build at B1 and stop after each step for tests to pass.
