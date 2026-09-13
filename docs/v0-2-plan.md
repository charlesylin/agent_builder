# v0.2 Plan — reorganizing the repository

**Status:** Plan drafted 2026-09-13, awaiting author double-check before Build.
**Phase:** Plan (entered 2026-09-13 by explicit author authorization).
**Builds on:** `docs/v0-2-define.md`. Nothing here changes what we are building; it says how,
in what order, and resolves the open questions Define left.

---

## 1. Answers to Define's open questions

Each is recorded as a proposed decision in §5. Override any of them before Build.

| # | Question | Answer | Why |
| --- | --- | --- | --- |
| 1 | Python floor | **3.9** | macOS ships 3.9 as system Python; most Windows installs are newer. Only three things in the code need 3.10+: `slots=True` on two dataclasses, `datetime.UTC`, and `tomllib` in one test. All trivial to replace. |
| 2 | Package or single files | **Three self-contained files**: `seed.py`, `check.py`, `render.py`. Delete `src/agent_builder/`. | Skills ship as a folder; a single file with no import path is what runs reliably on someone else's machine. The shared helpers are ~40 lines and are duplicated deliberately. |
| 3 | Codex | **Best-effort.** Same skill folder placed in `.agents/skills`; one manual smoke test recorded in Review. Not a gating success signal. | Claude is the org's primary host. Codex uses the identical format, so the cost of trying is near zero; the cost of *guaranteeing* is a second test matrix. |
| 4 | Marketplace location | **This repository is the marketplace.** `.claude-plugin/marketplace.json` at the root lists one plugin at `./`. | Simplest thing that works. An org-wide `<org>/claude-plugins` repo can reference this one later without moving anything. |
| 5 | Internal or public | **Repo stays public (it already is, MIT); audience is internal.** No badge, no website. | Nothing to change. Tone in docs is "for colleagues", not "for the world". |
| 6 | Who is admin | **Assumed: the author.** | If wrong, `docs/INSTALL.md` becomes a request to IT. Flagged, not blocking. |
| 7 | Sean's project | **Leave as-is.** Note in his packet that `check.py --since 0.1.0` will report the differences once v0.2 ships. | AB-D012. Migrating it during his active test would change his baseline mid-experiment. |

## 2. Build sequence

Eight small commits. Every one leaves `python3 -m unittest discover -s tests` green and is
independently revertible. Nothing is deleted until its replacement is tested.

### B1 — Python floor and preflight
- Replace `from datetime import UTC` with `timezone.utc` (2 files).
- Drop `slots=True` from the two dataclasses.
- Replace `tomllib` in the test with a regex on the one `version = "..."` line it checks.
- Add a five-line preflight at the top of both entry scripts:
  *"Agent Builder needs Python 3.9 or newer; this is 3.8.10."* Exit code 2.
- CI matrix: `3.9` and `3.12` on `ubuntu-latest`, `3.12` on `windows-latest`.
- **Done when:** tests pass on all three CI legs; the smoke test from F-002 now prints the
  one-sentence message under an old interpreter instead of a traceback.

### B2 — `principles/` and `build/render.py`
- Create `principles/`, one file per principle, cut from `governance/operating-agreement.md`.
  Nine files; IDs match the headings that exist today.
- Write `build/render.py` (stdlib; ~60 lines): load principles, walk a fixed list of stencil
  files, fill `{{principle:<id>}}`, write outputs, fail on unknown or unused IDs.
- Convert to stencils: root `AGENTS.md`, this repo's `governance/operating-agreement.md`
  (principles section only — purpose and phase text stay hand-written), the template operating
  agreement, and the three adapter templates. Stencils live at `<output>.stencil` beside each
  output; render writes the output next to it.
- Add `tests/test_render.py`: render to a temp dir, compare byte-for-byte with committed
  outputs, fail with the "edit principles/ and run build/render.py" message.
- Run render once; commit the generated outputs. This commit's diff *is* the proof that the
  six copies now agree.
- **Done when:** the drift test passes; editing one principle file and re-rendering changes all
  six outputs in one diff.

### B3 — Move templates to the repo root
- `git mv src/agent_builder/templates templates`.
- Split: everything agent-specific (`contracts/`, `deployment/`, `src/__PYTHON_PACKAGE__/`,
  `tests/test_scaffold.py.tmpl`, the runtime README) moves to `templates/kinds/agent/`;
  the rest stays in `templates/base/`. `templates/adapters/` folds into `templates/base/`.
- Update the one path constant in `scaffold.py`; add `--kind` (default `agent`) that layers
  `kinds/<kind>/` over `base/`.
- **Done when:** existing tests pass unchanged except for the path; a generated agent project
  is byte-identical to before the move.

### B4 — The `skill` kind
- `templates/kinds/skill/`: `SKILL.md` scaffold with `name`/`description` frontmatter and a
  `{{PURPOSE}}`-filled body, `scripts/README.md`, `references/README.md`, `evals/README.md`
  with one example scenario, `.claude-plugin/plugin.json` stub.
- One test: seed a `skill` project, validate it, assert `SKILL.md` frontmatter parses.
- **Done when:** `seed.py --kind skill` produces a folder Claude recognizes as a skill.

### B5 — `skills/agent-builder/` and retirement of the package
- Create `skills/agent-builder/scripts/seed.py` and `check.py` as self-contained files,
  assembled from `scaffold.py` + `models.py` + `cli.py` and `validation.py` respectively.
- Move `build/render.py`'s input list and the generated references under
  `skills/agent-builder/references/`.
- Write `skills/agent-builder/SKILL.md`: authored procedure (open Define; the four kind
  questions; the five facts; when seeding is permitted; closeout format; resume loop; never
  advance phase without explicit confirmation) with `{{principle:…}}` holes for the principles.
  Add it to render's stencil list.
- Add root `.claude-plugin/plugin.json` and `marketplace.json`.
- Point tests at the new scripts; delete `src/agent_builder/`, `scripts/new_agent.py`,
  `scripts/validate_project.py`, and the `[project.scripts]` entry in `pyproject.toml`.
- **Done when:** tests pass with the package gone; `/plugin marketplace add <this repo>` then
  `/plugin install agent-builder` loads the skill in Claude Code.

### B6 — Thin adapters, version pin, `--since`
- Adapter templates shrink to: project name, current phase (read at seed time), "this project
  follows Agent Builder — use the `agent-builder` skill", and a link to the reference.
- Seeded `.agent-builder.json` already records `template_version`; add `source_commit`.
- `check.py --since <version>`: prints the CHANGELOG sections between that version and the
  current one. Deliberately that simple.
- Seeded `.agents/skills/agent-builder/` and `.claude/skills/agent-builder/` contain a
  pointer `SKILL.md` (not a copy) so the skill loads in-repo.
- **Done when:** a seeded `CLAUDE.md` is under fifteen lines and a Windows-less test proves
  the pointer files exist.

### B7 — Documentation and evals
- `docs/INSTALL.md`: Claude org marketplace (GitHub sync, *Installed by default*), Claude Code
  managed settings with the exact keys, Codex paths. Dated; sources cited.
- `docs/AUTHORING.md`: how to change a principle, run render, run tests, run evals, bump
  `plugin.json` version, update CHANGELOG.
- `README.md` rewritten for the new shape. `CHANGELOG.md` gets an `[Unreleased]` section.
- `evals/` at the repo root with four scenarios as plain markdown (prompt, expected behavior,
  pass criteria): opens Define before offering to seed; refuses to advance phase on momentum;
  produces the four-section closeout; resumes cold from a seeded repo.
- **Done when:** a colleague can follow INSTALL.md without asking a question.

### B8 — Dogfood
- Run `seed.py --kind skill` into a temp dir with Agent Builder's own name and purpose; diff the
  result against `skills/agent-builder/`. Reconcile the template toward the real skill, not the
  other way round.
- Bump `plugin.json` to `0.2.0`; tag; hand to Review.
- **Done when:** success signal 5 in the Define record holds.

## 3. What is deliberately not in the sequence

- No change to `governance/` beyond the principles-section stencil in B2.
- No touching `.generated/`, Sean's packet, or any review artifact.
- No GitHub template-repo mirroring. It is a one-line CI job once B3 is done; add it when
  someone needs the no-tooling path.
- No `mcp` or `project` kinds.

## 4. Risks

| Risk | Mitigation |
| --- | --- |
| B5 is the largest step and touches tests, scripts, and packaging at once. | Land B5 as two commits if needed: create the new files and make tests pass against both old and new; then delete the old. |
| Stencil syntax `{{principle:x}}` collides with seed-time `{{PROJECT_NAME}}` placeholders in the same files. | Render runs first and only touches `{{principle:…}}`; seed only touches `{{UPPER_CASE}}`. Both regexes are anchored to their own shape; a test asserts neither matches the other's tokens. |
| Skill triggers too eagerly or not at all. | The `description` line is the whole trigger surface. Write it last, from the four kind questions, and test it in the evals. |
| The author is not the org admin. | INSTALL.md is written so it can be handed to whoever is. |

## 5. Proposed decisions from Plan

| ID | Proposal |
| --- | --- |
| AB-D025 | Python floor is 3.9 for all shipped scripts. |
| AB-D026 | `seed.py`, `check.py`, `render.py` are self-contained single files; `src/agent_builder/` is retired in B5. |
| AB-D027 | This repository is its own plugin marketplace. |
| AB-D028 | Codex support is best-effort in v0.2: same folder, one recorded smoke test, not a gating signal. |
| AB-D029 | Build proceeds as the eight commits in §2, each leaving tests green; B5 may split in two. |

## 6. Double-check list for the author

Before authorizing Build, confirm:

- [ ] Python 3.9 floor is acceptable for the org's machines.
- [ ] Deleting `src/agent_builder/` and the pip entry point is acceptable — nobody depends on `pip install agent-builder-template`.
- [ ] This repo as the marketplace is fine for now.
- [ ] Codex best-effort matches how many people actually use Codex.
- [ ] You are the org admin, or you know who is.
- [ ] The eight-step order looks right. In particular: principles and render (B2) come *before* the big move (B3, B5), so the drift test is protecting the copies while they move.
