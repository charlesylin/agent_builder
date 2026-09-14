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

> **B2 as built (2026-09-13):** the renderer and stencils live at `scripts/render.py` and
> `scripts/stencils/`, not `build/`, because `build/` is gitignored as packaging output and the
> tool would have been silently excluded. The operating agreements no longer state a current
> phase; `project-state.yaml` is the source. Ruff lint/format was added to CI here rather than
> in B7, at the author's request.

### B3 — Move templates to the repo root
- `git mv src/agent_builder/templates templates`.
- Split: everything agent-specific (`contracts/`, `deployment/`, `src/__PYTHON_PACKAGE__/`,
  `tests/test_scaffold.py.tmpl`, the runtime README) moves to `templates/kinds/agent/`;
  the rest stays in `templates/base/`. `templates/adapters/` folds into `templates/base/`.
- Update the one path constant in `scaffold.py`; add `--kind` (default `agent`) that layers
  `kinds/<kind>/` over `base/`.
- **Done when:** existing tests pass unchanged except for the path; a generated agent project
  is byte-identical to before the move.

> **B3 as built (2026-09-14):** `templates/adapters/<host>/` stays a sibling of `base/` and
> `kinds/` rather than folding into `base/`, because adapters are selected per host and `base/`
> is copied whole. `pyproject.toml.tmpl` and `.dockerignore.tmpl` moved to `kinds/agent/` along
> with the files the plan listed. `README.md.tmpl`, `CONTRIBUTING.md.tmpl`, and `ci.yml.tmpl`
> stayed in `base/` unchanged to keep output byte-identical; they still describe an agent
> layout and B4 must give the `skill` kind overrides for them.

### B4 — The `skill` kind
- `templates/kinds/skill/`: `SKILL.md` scaffold with `name`/`description` frontmatter and a
  `{{PURPOSE}}`-filled body, `scripts/README.md`, `references/README.md`, `evals/README.md`
  with one example scenario, `.claude-plugin/plugin.json` stub.
- One test: seed a `skill` project, validate it, assert `SKILL.md` frontmatter parses.
- **Done when:** `seed.py --kind skill` produces a folder Claude recognizes as a skill.

> **B4 as built (2026-09-14):** the skill kind also overrides `README.md`, `CONTRIBUTING.md`,
> `ci.yml`, and `governance/project-state.yaml` (no runtime/deployment blocks; a
> `distribution` block instead), and ships `tests/test_skill.py` so its CI has something to
> run. `kind` is recorded in `.agent-builder.json` and `project-state.yaml` for every kind.
> The validator became kind-aware here rather than later; v0.1 manifests without `kind`
> validate as agents. `plugin.json` has no `author` because the seeder does not yet collect an
> owner — B5's skill procedure asks for one, so the field lands there.

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

> **B5 as built (2026-09-14), two commits:** `templates/` moved *inside* `skills/agent-builder/`
> rather than staying at the repo root, so a Codex user who copies only the skill folder has
> everything the seeder needs; `principles/`, `scripts/render.py`, and `scripts/stencils/` stay
> at the root because they are maintenance tooling, not shipped. `seed.py` imports
> `validate_project` from its sibling `check.py` instead of duplicating 200 lines; the folder,
> not the file, is the self-contained unit. The seeder gained `--owner` and a first commit on
> `main` here (the plan had the commit in B2's description of the experience, not in a step).
> `plugin.json` version is `0.2.0-dev` until B8. The "loads in Claude Code" done-when needs
> the author to run `/plugin marketplace add` against the pushed repository; it cannot be
> verified from the build environment.

> **B6 revised by AB-D030 (2026-09-14), after the skill test.** The thin-adapter clause is
> withdrawn. Evidence: with the plugin loaded, the skill did not fire on "what's the status
> here?" in a seeded project and the adapter file carried the work; thinning it would have
> left a resumed project with nothing. AB-D024's drift rationale was already satisfied by
> AB-D020. B6 now: keep adapters substantive and add an explicit line telling the host to
> invoke the `agent-builder` skill; widen the skill `description` to cover resume phrasing;
> replace `SKILL.md` §3's "at most three lines" with the briefing shape that actually helped;
> relax §1's "one question per turn" to batch logistics with defaults. Version pin and
> `check.py --since` are unchanged. See `docs/v0-2-skill-test.md`.

### B6 — Adapters, version pin, `--since`
- Adapter templates shrink to: project name, current phase (read at seed time), "this project
  follows Agent Builder — use the `agent-builder` skill", and a link to the reference.
- Seeded `.agent-builder.json` already records `template_version`; add `source_commit`.
- `check.py --since <version>`: prints the CHANGELOG sections between that version and the
  current one. Deliberately that simple.
- Seeded `.agents/skills/agent-builder/` and `.claude/skills/agent-builder/` contain a
  pointer `SKILL.md` (not a copy) so the skill loads in-repo.
- **Done when:** a seeded `CLAUDE.md` is under fifteen lines and a Windows-less test proves
  the pointer files exist.

> **B6 as built (2026-09-14):** per AB-D030. The in-repo pointer skills
> (`.agents/skills/agent-builder/`, `.claude/skills/agent-builder/`) were dropped: a pointer
> cannot load a skill that is not installed, and the adapter file — loaded unconditionally by
> every host — is a strictly more reliable carrier than a second trigger surface. `--since`
> reads the builder's `CHANGELOG.md` when run from a checkout and says plainly when a copied
> skill folder has none. `source_commit` is `null` from a copied folder for the same reason.

> **B7 amended (2026-09-14) after run 3 (F-007):** evals come **first**, not last. The skill
> triggered on two prompts that echoed its own description and did not trigger on a natural
> one ("i want to make a thing that can quickly retrieve depmap data…"). Scenario 1 is that
> prompt. Run `claude plugin eval` before touching the description, rewrite the description to
> describe the shape of a request (someone wants to create a new tool, capability, automation,
> or project, however phrased) rather than list verbs, re-run, and keep the version with the
> better measured rate. Then INSTALL.md, AUTHORING.md, README. Also: a line in SKILL.md for
> "this was a test / abandon this", once AB-D031 is confirmed.

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

> **B7a as built (2026-09-14):** evals, INSTALL, AUTHORING, README landed. The eval suite
> cannot run from the build environment (`claude plugin eval` needs an interactive-capable
> install); the author runs it and B7b rewrites the description against the numbers. The
> AB-D031 "this was a test" line waits for that decision.

### B7c — The offer hook (added 2026-09-14, AB-D032)

A `UserPromptSubmit` hook replaces "widen the description" as the answer to F-007. Explicit
invocation is the trained path; the hook is the safety net for people who phrase a request
concretely enough that the host would otherwise just start coding.

- **Done when:** the hook matches every eval phrasing and none of the counter-examples (unit
  tested), is silent in a seeded project and after a decline, always exits 0, and the author
  has seen the offer appear and be declined in a real session.
- **Done 2026-09-14**, through the installed plugin, after three failed attempts recorded as
  F-012 (`--plugin-dir` does not load hooks), F-013 (the hook read a key the payload never
  sent) and F-014 (the offer repeated after a decline). B7b's original goal — widening the
  description — was superseded by AB-D032 and is closed unchanged.

### B8 — Dogfood
- Run `seed.py --kind skill` into a temp dir with Agent Builder's own name and purpose; diff the
  result against `skills/agent-builder/`. Reconcile the template toward the real skill, not the
  other way round.
- Bump `plugin.json` to `0.2.0`; tag; hand to Review.
- **Done when:** success signal 5 in the Define record holds.
- **Done 2026-09-14.** The template seeded a valid skill plugin; reconciling it moved the
  skill kind's `evals/` to `claude plugin eval` format. Layout differences are recorded as
  F-016 rather than forced. `v0.2.0` tagged; Review awaits author approval.

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
