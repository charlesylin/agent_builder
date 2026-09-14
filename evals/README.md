# Evals

Measured evidence that the `agent-builder` skill fires when it should, stays quiet when it
should not, and behaves as `SKILL.md` says once loaded. Needs Claude Code 2.1.269 or later.

## Run the trigger sweep first — it is the cheap one

This is what F-007 is about: does the description match how colleagues actually phrase a
request? Seven phrasings, one negative case.

```sh
claude plugin eval . --tag trigger --tag negative --ablation none -j 4 --judge-model sonnet
```

- **`--ablation none`** matters. In the default two-arm mode a `tool_used: Skill` grader is
  reported as an indicator and **not scored**, because it could never pass without the plugin.
  Single-arm mode scores it, which is the number we are after.
- **`-j 4`** runs four at a time. The default is **1**, and a serial suite takes far longer
  than it looks like it should.
- No tool grants needed: these cases only need to ask a question. `max_turns: 3` keeps them
  short.

Roughly 24 runs, a few minutes, low cost. Read `skill-fired` per case: that fraction is the
trigger rate for that phrasing.

## Then the behavior cases

```sh
claude plugin eval . --tag resume --scaffold --allow-tools Write Edit Bash -j 2 --judge-model sonnet
```

- **`--scaffold`** runs each case's `fixture.sh`, which seeds a project into the run's
  workspace. The shared script is `_seed-fixture.sh`; read it before running a suite you did
  not write.
- **`--allow-tools Write Edit Bash` is required.** Claude Code strips `Bash`, `Write`, and
  `Edit` from a run unless you grant them, whatever `allowed_tools` says. Without the grant,
  `resume-refuses-phase-change-on-momentum` passes because the agent *cannot* edit the phase,
  not because it chose not to — a vacuous pass. This happened on 2026-09-14.

## Everything, for a release

```sh
claude plugin eval . --scaffold --allow-tools Write Edit Bash -j 4 \
  --judge-model sonnet --json evals-$(date +%Y%m%d).json
```

Budget it: 14 cases × 3 runs × 2 arms is ~84 agent runs plus judge calls. Add
`--max-cost-usd` if you want a ceiling.

## Cases

| Case | Tag | Passes when |
| --- | --- | --- |
| `triggers-natural-request` | trigger, f007 | The 2026-09-14 run-3 DepMap prompt fires the skill and gets a question, not a design |
| `triggers-build-agent` | trigger, control | The run-1 prompt that already worked |
| `triggers-make-skill` | trigger | A skill-kind request in plain words |
| `triggers-new-tool-plain` | trigger | "we need an internal tool… where do I start?" |
| `triggers-automate-task` | trigger | "i keep manually reformatting… can we automate that?" |
| `triggers-help-me-build` | trigger | "help me build a little service that…" |
| `triggers-starting-a-project` | trigger | "starting a new project today… what's the right way to set it up?" |
| `ignores-general-coding-question` | negative | A Python question is answered and the skill does **not** fire |
| `resume-status` | resume | Briefing names Define, cites decision IDs, ends with the closeout |
| `resume-refuses-phase-change-on-momentum` | resume, phase-gate | `phase.current` is still `define` and the reply asks for explicit approval |

## Reading the result

**Trigger sweep.** `skill-fired` at 3/3 is the description matching that phrasing; 0/3 is the
F-007 shape. Fix by editing `description` in
`scripts/stencils/skills/agent-builder/SKILL.md`, rendering, and re-running the same command.
Keep the wording with the better rate; record both numbers in `docs/v0-2-skill-test.md`.

**`ignores-general-coding-question`** below 1.0 means the description has become greedy. Watch
it every time the description changes — it is the counterweight to the trigger sweep.

**Δ on the resume cases is expected to be ~0, and that is not a failure.** A seeded project
carries an adapter file (`CLAUDE.md`) that already tells the host to read governance and give a
briefing, so the no-plugin arm passes too. That is AB-D030's floor working as designed. These
cases are regression guards on behavior, not measures of what the skill adds. If Δ ever goes
*negative*, the skill is making things worse and that is worth investigating.

Record any run whose numbers change a decision in `docs/v0-2-skill-test.md`, with the date and
the Claude Code version.
