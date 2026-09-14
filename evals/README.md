# Evals

Measured evidence that the `agent-builder` skill triggers when it should, stays quiet when it
should not, and behaves as `SKILL.md` says once loaded. Run with `claude plugin eval`
(Claude Code 2.1.269 or later). Each case runs three times with the plugin and three times
without, so the report shows what the plugin contributes (`Δ`), not just whether Claude got
the answer.

## Run

From the repository root:

```sh
claude plugin eval . --scaffold --judge-model sonnet
```

- `--scaffold` is required for the two `resume-*` cases: it lets `fixture.sh` seed a project
  into the run's workspace before Claude starts. The script is `_seed-fixture.sh` in this
  directory; read it before running suites you did not write.
- `--judge-model sonnet` makes the `llm` graders less noisy than the default small judge.
- Add `--ablation none` to skip the no-plugin baseline while iterating on graders (half the
  cost, no `Δ`).
- Add `--json results.json` to keep the numbers.

Every run costs model calls against your plan. The suite is 7 cases × 3 runs × 2 arms, plus
judge calls.

## Cases

| Case | Prompt shape | Passes when |
| --- | --- | --- |
| `triggers-natural-request` | The 2026-09-14 run-3 prompt that did **not** trigger the skill (F-007) | Skill fires; reply asks what kind of thing this is before researching or building; no files written |
| `triggers-build-agent` | The run-1 prompt that did trigger — a control | Same |
| `triggers-make-skill` | A skill-kind request in plain words | Same |
| `triggers-new-tool-plain` | "we need an internal tool… where do I start?" | Same |
| `ignores-general-coding-question` | A Python question | Skill does **not** fire; question answered |
| `resume-status` | "what's the status here?" in a seeded project | Skill fires; briefing names Define, cites decision IDs, ends with the closeout |
| `resume-refuses-phase-change-on-momentum` | "looks good, next" in a seeded project | `phase.current` still `define`; reply asks for explicit approval or continues Define |

`tool_used: Skill` graders are reported but not scored in the two-arm comparison (they can
never pass without the plugin). The behavioral graders carry `arm: both` so `Δ` is meaningful.

## Reading the result

- A trigger case at `WITH 1.0 / W/OUT 0.0` is the skill doing its job.
- A trigger case low in both arms means the description is not matching that phrasing —
  the F-007 shape. Rewrite `description` in `scripts/stencils/skills/agent-builder/SKILL.md`,
  render, re-run, keep the better number.
- `ignores-general-coding-question` at anything under 1.0 means the description is greedy.
- If a `resume-*` case fails with a run error, the scaffold did not run: check `--scaffold`
  and that `python3` is on `PATH`.

Record each run's date, Claude Code version, and headline numbers in
`docs/v0-2-skill-test.md` when the result changes a decision.
