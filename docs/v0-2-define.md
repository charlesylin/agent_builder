# v0.2 Define — what Agent Builder is, and how people use it

**Status:** Define complete, pending author commit. Decisions in §8 are `proposed` until the
author confirms them; entering Plan requires explicit author approval.
**Date:** 2026-09-13
**Inputs:** v0.1 acceptance record (`docs/v0-1-acceptance.md`), findings F-001 and F-002, and a
review of `seqeralabs/rewrites.bio` as the design inspiration.

---

## 1. What v0.1 taught us

v0.1 shipped two things: a set of written principles and phases, and a Python program that
copies template files. The author's acceptance, based on Sean's project and other use cases,
rested entirely on the first. The Python was incidental — a delivery mechanism for the
instructions — and it broke on any machine without Python 3.11 (F-002), while the instructions
only loaded if the person knew which files to point the agent at (F-001).

rewrites.bio confirmed the shape that follows from this. It is twelve principles, written once,
rendered by a build script into every form a machine might read, with nothing installed on the
adopter's side. The deterministic code serves the publisher. Agent Builder's operating agreement
is already those principles transposed to agent building; v0.2 gives it the same architecture,
adapted to an organization that controls its own tools and can therefore install a skill rather
than publish a website.

## 2. What Agent Builder is

Three things, plus a build step that keeps them consistent. All of it lives in this repository.

1. **A skill.** A `SKILL.md` file that Claude or Codex reads. It says how to run the Define
   conversation, when it is allowed to create files, how to write a closeout, and how to pick up
   an existing project. This is where the judgment lives. Everything else is plumbing for it.
2. **A Python script** — `seed.py` — that creates a new project: copies the right starter files,
   fills in the blanks, checks the result, and makes the first commit. A small sibling,
   `check.py`, validates a project's governance files and runs in the project's CI.
3. **Starter templates** — folders inside this repo. `templates/base/` is what every project
   gets; `templates/kinds/<kind>/` adds what one kind of project needs. The script combines base
   plus one kind.

And the **build step** — `build/render.py` — which assembles the skill text, the template
operating agreement, and the adapter files from one folder of principle files, with a test that
fails if anyone edits a copy instead of the source. Section 6 explains it.

## 3. How a colleague uses it

### Starting something new

Sean opens Claude Code in an empty folder and types: *"I want to build something that finds
secondhand lab equipment listings and flags good deals."* The skill activates — the org admin
installed it for everyone, so there is nothing to clone.

It asks four questions to learn what kind of thing he is making:

| Question | If yes, the kind is |
| --- | --- |
| Will it call an AI model and then act on the answer, possibly on its own? | `agent` |
| Is it written instructions, plus maybe scripts, that Claude or Codex follows when asked? | `skill` |
| Is it a server that gives an AI model access to a tool or a database? | `mcp` |
| Is it ordinary software where you want the phase discipline but no AI inside? | `project` |

Sean's is an agent. The skill collects five facts — name, one-sentence purpose, owner, which
coding tools he will use, where the folder goes — and runs:

```
python3 seed.py --kind agent --name "Lab Equipment Scout" \
  --purpose "Finds secondhand lab equipment listings and flags underpriced items." \
  --owner sean --host claude ~/src/lab-scout
```

The script checks the folder does not already exist and stops if it does. It copies the base
files and the agent files. It replaces placeholders such as `{{PROJECT_NAME}}` with his answers.
It runs `check.py` to confirm every required file is present, the YAML parses, no secrets slipped
in, and the phase is Define. It runs `git init` and commits once:
`chore: seed agent project from agent-builder 0.2.0`.

Then it asks one more question — *"create `github.com/<org>/lab-scout` and push?"* — because
creating a repository in the org is a bigger action than writing files on a laptop.

Sean now has about twenty files, already a git repository, already in Define, with his name and
purpose filled in everywhere. `CLAUDE.md` is ten lines: the project name, "currently in Define",
and "this project follows Agent Builder — use the `agent-builder` skill."

### Coming back later

The skill has no memory. The repository does. Next week Sean opens the folder again; the skill
reads `governance/project-state.yaml`, says *"Lab Equipment Scout is in Define; the last recorded
decision was LS-D002; the next step is to finish the success signals,"* and continues. This is
the resume loop that worked on 2026-09-13 for Agent Builder itself.

### How the phases actually get enforced

Four layers, weakest to strongest. The honest statement is that only the last one binds.

| Layer | What it is | Binding? |
| --- | --- | --- |
| Instruction | The skill says: never change phase without the author saying so; record decisions with IDs; write the four-section closeout; commit at phase boundaries. | No — it depends on the model following instructions. |
| Structure | `project-state.yaml` requires `confirmed_by` and `date` on every phase entry; a decision's status must be one of four values; the closeout has fixed sections. | Shapes behavior. |
| Local check | `check.py` validates all of the above plus secret patterns and "governance edited but not committed". It runs as a pre-commit hook via `prek`. | Loud, but a person can bypass it with `--no-verify`. That is the correct escape hatch. |
| CI | The project's own CI runs `check.py`. If it fails, the change cannot merge to `main`. | Yes. |

On a laptop, Agent Builder is a manifesto with a linter. At the merge gate, it is governance.
There is no gatekeeper program on anyone's machine.

Commit discipline follows the same pattern: the seeder makes the first commit; the skill commits
at each phase closeout with a fixed message shape (`define: …`, `plan: …`); pushing is a separate
action the skill takes only when told.

## 4. How the skill is installed and updated

- **Claude (claude.ai, Desktop, Cowork):** the `agent-builder` plugin lives in an org marketplace
  synced from a private GitHub repository; the admin marks it *Installed by default*.
- **Claude Code:** managed settings pre-register the marketplace (`extraKnownMarketplaces`) and
  enable the plugin (`enabledPlugins`).
- **Codex:** the same skill directory is placed in `$HOME/.agents/skills` or `/etc/codex/skills`.
  Seeded projects also carry `.agents/skills/agent-builder/` so the skill loads in-repo.
- **Gemini CLI:** a pointer in `GEMINI.md` only. Skill loading there is verified in Plan, not
  promised.

A release is a bump to `version` in `.claude-plugin/plugin.json` — that string, not the git
commit, is what makes users receive an update. Seeded projects record the version they came
from in `.agent-builder.json`; `check.py --since <version>` reports what changed. Existing
projects never change automatically (AB-D012).

## 5. What this repository becomes

A reorganization, not a rewrite. Most existing code survives and moves.

**Stays:** `governance/` (this project's own ledger), `docs/`, `tests/`, CI, `prek.toml`,
LICENSE, SECURITY, and the copy/fill/validate logic in `src/agent_builder/`.

**Moves:**
- `src/agent_builder/templates/` → `templates/` at the repo root. Templates are content, not code.
- `scripts/new_agent.py`, `scripts/validate_project.py` → `skills/agent-builder/scripts/seed.py`
  and `check.py`, plus a version preflight.
- The three adapter templates → thin stencils in `templates/base/` instead of full copies.

**New:**
- `principles/` — one small file per principle, extracted from the current operating agreement.
- `skills/agent-builder/SKILL.md` — the authored procedure. The one genuinely new piece of writing.
- `build/render.py` and its drift test.
- `templates/kinds/agent/` (the agent-specific files pulled out of base) and
  `templates/kinds/skill/` (new).
- `.claude-plugin/plugin.json`; `docs/INSTALL.md`; `docs/AUTHORING.md`.

**Goes away:** the hand-written root `AGENTS.md` (generated instead); root `CLAUDE.md` and
`GEMINI.md` shrink to pointers; probably the `agent-builder` console-script entry point, since
nobody installs this with pip any more.

Target layout:

```
agent_builder/
  principles/                 the only place a principle's text is written
  skills/agent-builder/
    SKILL.md                  authored procedure + generated principles section
    scripts/seed.py           creates a project
    scripts/check.py          validates a project
    references/               generated: operating agreement, closeout template, kinds guide
  templates/
    base/                     what every project gets
    kinds/agent/  kinds/skill/
  build/render.py             assembles generated files; test fails on drift
  .claude-plugin/plugin.json
  governance/  docs/  tests/  this project's own phases, decisions, evidence
```

## 6. How the build step works

Today Nokkvi's law is written out in six files: root `AGENTS.md`, this repo's operating
agreement, the template operating agreement, and the three adapter templates. The root
agreement and its template copy already differ by 208 lines. The skill would be a seventh copy.

The fix is to write each principle once, in `principles/`, one file each with a short header:

```markdown
---
id: nokkvis-law
title: Nokkvi's law
---
At the start of every interaction or prompting round, silently tell yourself exactly: ...
```

Every other place the text appears becomes a stencil with holes:

```markdown
## Engineering principles
{{principle:use-reasoning-selectively}}
{{principle:work-small-fail-loudly}}
{{principle:nokkvis-law}}
```

`build/render.py` reads `principles/` into a dictionary, fills every `{{principle:…}}` hole, and
writes the finished files to their real locations, which are committed like normal files. It
fails if a stencil names a principle that does not exist or a principle exists that nothing uses.

One test renders into a temporary folder and compares byte-for-byte with the committed output.
If they differ, it fails with: *"skills/agent-builder/SKILL.md is out of date — edit principles/
and run build/render.py."* CI runs it on every push. That is the check rewrites.bio lacks,
because its generated files live outside git.

Day to day: edit one principle file, run the script, commit. The diff shows the source change
and the same change in the skill, the template, and the adapters — one commit. Bump the plugin
version and every colleague's skill updates; new projects get the new wording; existing projects
keep theirs until they opt in.

`seed.py` already does this exact replacement for `{{PROJECT_NAME}}` and `{{PURPOSE}}`. The
build script is the same mechanism pointed at a different set of holes, run at build time
instead of seed time.

## 7. Boundaries and success signals

**Not in v0.2:** runtime or model-framework selection (AB-D008 stands); hard gatekeeping on the
user's machine; a public website; kinds beyond `agent` and `skill` — `mcp` and `project` arrive
with the first real request and its friction as evidence (the AB-D013 pattern); automatic
modification of seeded projects; cross-host guarantees for Gemini.

**Done when:**
1. A colleague on Windows, with the org install and nothing else, reaches a seeded, validated,
   committed Define-phase project in one session.
2. A principle edited once propagates to the skill, references, templates, and adapters in a
   single commit, and CI proves it.
3. A fresh session in a seeded repo, given only the skill trigger, states the correct phase and
   last decision without being told which files to read.
4. The eval set passes — including refusing to advance a phase on conversational momentum.
5. Agent Builder's own skill is produced by its own `skill` template.

## 8. Proposed decisions

Recorded as `proposed` in `governance/decisions.yaml`; confirmed only by the author.

| ID | Proposal |
| --- | --- |
| AB-D019 | The primary v0.2 deliverable is an org-installable skill in the Agent Skills format, packaged as a Claude plugin and usable unchanged by Codex. Everything else — seeder, checker, templates, build step — exists to serve it. |
| AB-D020 | Every principle has one source file under `principles/`. All other forms are generated, committed, and drift-checked in CI. |
| AB-D021 | Seeder, checker, and renderer are standard-library Python with a version preflight; the floor is set in Plan. On confirmation this supersedes AB-D018: no container for the builder is needed once nothing beyond a stdlib interpreter runs on the user's machine. |
| AB-D022 | Enforcement model: instruction and structure guide; the local check is advisory; CI in seeded projects is the binding gate. |
| AB-D023 | v0.2 ships `agent` and `skill` kinds only. Further kinds require a real requesting project. |
| AB-D024 | Seeded adapters are thin pointers, not copies. Seeded projects pin their template version; `check.py --since` is the opt-in upgrade path. |

## 9. Open questions carried into Plan

1. Python floor for the scripts — 3.9, or older?
2. Do `seed.py` and `check.py` stay a shared package, or become two self-contained files with
   small deliberate duplication? Lean: self-contained, for shipping inside a skill.
3. Is Codex a requirement or best-effort?
4. Does this repository become the org marketplace, or does a separate `<org>/claude-plugins`
   repository reference it?
5. Internal to Two River Bio, or public?
6. Who is the org admin who marks the plugin *Installed by default* and maintains managed
   settings? If not the author, the install story needs a ticket and a doc before Plan can
   promise "nobody clones anything."
7. Sean's project and the v0.1 fixture: documented opt-in migration to thin adapters, or
   left as-is with a note?

## 10. Sources consulted 2026-09-13

- OpenAI, *Build skills* (learn.chatgpt.com/docs/build-skills.md) — Codex discovery paths,
  frontmatter, invocation, plugin packaging.
- Anthropic, *Create and distribute a plugin marketplace* (code.claude.com) — `marketplace.json`,
  `plugin.json`, managed-settings keys, version resolution.
- Anthropic, *Manage plugins for your organization* (support.claude.com) — admin distribution
  to claude.ai, Desktop, and Cowork.
- seqeralabs/rewrites.bio — single-source render pipeline, `.well-known` discovery, badge pattern.
