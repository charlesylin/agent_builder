# Agent Builder v0.5.0 — implementation plan

**Status:** The original plan was approved and built. The author returned from
Review to Plan on 2026-10-08 for the cleanup and test-design amendments below;
the author approved both and reopened Build on 2026-10-08. The
[Define record](v0-5-definition.md) sets the outcome; the
[reuse evaluation](v0-5-solution-evaluation.md) supports adapting
the existing Agent Builder instructions and templates.

## Operating behavior to implement

1. **Keep the current task moving.** Before asking a user, distinguish a true
   blocker (authority, consequential choice, missing input, or unsafe ambiguity)
   from a later issue. Ask only about the blocker. Record a nonblocking issue
   once in the project's existing `planning/later.md`, with enough context to
   recover it, and continue. Check every proposed addition against the
   agreed problem, version-sized outcome, or current task; defer product sprawl
   unless the author explicitly changes scope. Do not display a new checklist
   in every reply or create an extra question log.
2. **Inspect before every commit.** Use `git status --short --untracked-files=all`
   to inventory all candidates, then review `git diff`, `git diff --cached`,
   `git diff --cached --stat`, and `git diff --cached --numstat` after staging.
   Stage selected paths, not everything indiscriminately. Keep disposable
   previews, raw review output, and draft notes out of Git; summarize durable
   findings in the existing appropriate record. Preserve intentional,
   necessary generated assets such as pinned Spec Kit files. If additions are
   unusual, explain what they are and split independent work where useful;
   do not split one coherent vendor update just to meet a number. Never remove
   an existing user's file merely because it looks temporary. Git's counts
   omit untracked paths until staged and represent binary changes as `-`, so
   inspect those separately.
3. **Prove changed behavior.** For each behavior change, identify expected
   normal, failure, and boundary outcomes with the user when that choice is
   material; otherwise propose them and proceed. Add focused unit tests for
   the changed behavior and run the relevant suite. State which behavior each
   check verifies and what remains untested. A generic scaffold check or
   compilation alone is not a behavioral test. Do not force Python's runner
   on a non-Python project or add a coverage-percentage target without need.
4. **Write for the next member.** Keep a concise human README that says what
   the project does, how to use and test the current version, and its important
   limits. Keep machine decisions and evidence in their existing records;
   link to them only when useful. Remove template suggestions that make a raw
   review transcript or handoff note look like a required committed artifact.
5. **Offer independent review once in Review when very large.** At the start
   of Build, retain `git rev-parse HEAD` in the normal phase checkpoint.
   During Review compare that base to the completed cycle with Git's
   `--numstat` and `--name-only`, not just its last commit. The proposed
   trigger is at least **1,000 added lines or 25 changed paths**, including
   generated/vendor paths; the author's +10,000/-30 case
   always triggers. This is an invitation, not a Build stop or an automatic
   review. Say what drove the count. If declined, run nothing. If accepted,
   guide a fresh reviewer session supplied with the code and original goals,
   not the builder's conclusions. For a Two River member, offer Erico's
   reviewer when Python code is in scope; for other languages or a prose-only
   skill, suggest a capable independent review instead. Confirm the skill *and*
   `tr-review` command exist before use. If missing, offer host-appropriate
   installation steps and verify after the user authorizes installation.
   Report files actually reviewed, files skipped, and limits; a second model
   session is more independent, not guaranteed unbiased.

The threshold is a deliberately simple prompt signal, not a maximum commit
size. In this repository's 81-commit history, it would have signaled 10
commits, including the 7,015-added-line Spec Kit integration. Recent ordinary
Define and corrective-patch commits would not have signaled. Review should
adjust the threshold only if real use shows too many interruptions or missed
large changes; no extra prompt is needed for a normal increment.

## Small Build slices

1. Edit the three relevant principle sources and the Agent Builder skill
   stencil; render generated copies. Keep one clear rule per behavior above,
   without a new phase, CLI, validator, or dependency. Avoid repeating the
   entire policy in every host adapter.
2. Tighten the shared planning README and kind-specific human README or
   contributing templates only where they currently encourage disposable
   records or describe scaffold tests as full behavior verification. Keep
   the mandatory governance and selected Spec Kit artifacts intact. Add a
   compact optional-review reference inside the installed skill with generic
   guidance and a clearly labeled Two River route. Do not embed reviewer code.
3. Add targeted repository tests for rendered-source agreement and the
   changed seed templates across agent, skill, and project kinds. Test that
   no new mandatory file/dependency was introduced and that older generated
   projects remain untouched. Run the existing Python test matrix, Ruff,
   bundle verifier, render check, and generated-project checker. These
   mechanical tests verify packaging; realistic agent behavior remains for
   Review.

## Optional reviewer setup and limits

The [organization marketplace](https://github.com/tworiverbio/claude-plugins)
lists `tr-review@tworiver` for both hosts at reviewer tag `v0.1.0`, and the
[reviewer README](https://github.com/tworiverbio/code-review-agent/blob/v0.1.0/README.md)
requires a separate CLI install. The current Codex host discovers the
`tr-review` skill and has the command, while this machine's Claude Code
plugin list lacks it. A manifest and CLI-help check verifies the proposed
paths, **not** a fresh installation on both hosts.

After opt-in and access/SSH checks, Claude Code can use
`claude plugin marketplace add tworiverbio/claude-plugins` then
`claude plugin install tr-review@tworiver`; Codex can use
`codex plugin marketplace add git@github.com:tworiverbio/claude-plugins.git`
then `codex plugin add tr-review@tworiver`. Install the separately pinned CLI
with `uv tool install git+ssh://git@github.com/tworiverbio/code-review-agent@v0.1.0`.
Check `tr-review --help` and actual skill discovery in a new host session;
then run the review against a target the tool can cover. If Codex marketplace
installation does not expose the skill, the reviewer's documented local-skill
path is a fallback, not a claim of tested parity. Its current branch/PR
mode reviews committed Python changes; path mode can inspect working-tree
files. Either may omit files past its 150,000-character packet cap, so inspect
its search/skipped report and never present partial findings as complete
coverage. No install, repository onboarding, external review, or posting happens without the
member's acceptance and applicable access.

## Review of this version

Use the three scenarios in the Define record on a new project, recording
observable user turns, committed paths, unit-test cases, human comprehension,
and the optional-review response. Compare with a similar v0.4.0 cycle; do not
infer faster cycles from instruction text alone. A missing install or review
coverage claim is a failure to report, not a reason to silently waive the
scenario. Do not tag or publish v0.5.0 during Build.

## Approved cleanup amendment — 2026-10-08

The author asked to make this repository itself leaner after reviewing its size.
Keep v0.5.0's existing behavior and release target. This amendment concerns
historical material in the active checkout and the current machine checkpoint,
not generated projects or the bundled Spec Kit dependency.

- Remove the two full 2026-09-14 skill-test transcripts from the current tree
  (2,435 lines together). The results and decisions remain in
  `docs/v0-2-skill-test.md`, which currently links to both files. Replace those
  two links with exact Git-history retrieval instructions: the first transcript
  is in commit `db98f06f554cc04dbb435dfe5c83afc3a274e39e`, the second in
  `7cc90d702c48eb4ae3482ea1e6b845608cea38f3`. Verify each blob before
  removal. Do not rewrite history or discard the summarized evidence.
- Remove the completed v0.1 Sean test packet and v0.4 Erico handoff from the
  current tree (267 lines together). Neither is referenced by current tracked
  files. Their last recorded contents are recoverable at commits
  `be443d01de8f324eeb4880ac36cff438e847a24a` and
  `c871984d348d92e18fc2139fdcf7c783633abfcb`, respectively. Preserve
  the concise acceptance records; do not remove other historical documents.
- Shorten `governance/handoff.json` (314 lines, including 38 repeated decision
  summaries) to the current phase, immediate decisions, essential artifact
  pointers, evidence limits, and next action. Keep its existing top-level
  fields and `schema_version`; `governance/decisions.yaml` remains the complete
  authority. Update `docs/RESUME.md` consistently.

Before staging, inspect the exact deletions and references. Verify the four
Git-history blobs, no live Markdown links to deleted paths, valid handoff JSON,
and unchanged phase/decision facts. Run the full Python test suite, render
check, pinned Spec Kit verifier, Ruff checks, and `git diff --check`; report
which checks do and do not exercise behavior. Stage only these durable changes.
No push, tag, or v0.5.0 acceptance is part of this amendment.

The independent review also suggested splitting two long Python functions and
annotating one CLI parameter. Those changes may improve maintainability but
will not materially shrink the repository and would add a second kind of work
to this cleanup. Keep them visible as later maintenance candidates rather
than expanding this amendment to refactor behavior-tested code.

## Approved test-design amendment — 2026-10-08

The author wants fewer performative checks within v0.5.0's existing lean,
behavior-tested outcome. Distinguish three purposes:

- **Plan:** State inputs and expected normal, failure, and relevant boundary
  outcomes for each changed behavior. Ask the author about product choices or
  control data; otherwise state assumptions. Run one-off feasibility probes in
  a temporary location, not Git. Record only a concise finding and the exact
  command/version when a probe supports a decision. If it reproduces a defect
  or establishes a supported compatibility promise, add a focused committed
  regression test in Build.
- **Build:** Add focused unit tests for changed logic and persistent
  integration/contract tests for supported dependency, host, environment, or
  external-boundary guarantees. State what each protects. Label lint,
  compilation, packaging, and scaffold checks honestly; do not call them
  behavior tests or use an undefined "smoke test" label. Audit all three seeded
  test templates and generated CI: remove redundant seed-time assertions,
  retain continuing contracts, and do not imply an empty product is tested.
  Update `principles/06-work-small-fail-loudly.md`, the skill stencil and
  rendered copies, templates, and targeted repository tests; add no new
  test-management script or report.

**Size signal, not a cap:** This repository has 1,475 first-party Python test
lines versus 1,947 Python source lines, excluding vendor and rendered
copies. If tests exceed code, review duplication, setup, snapshots, and
obsolete scaffolding, then explain justified exceptions. A hard cap could
discourage security/boundary tests or encourage inflated code; a freshly
seeded project may have no product code. Add no ratio gate in v0.5.0.

In Review, inspect a real project cycle for disposable probes absent from Git,
unit cases for changed behavior, and a regression check for any *promised*
compatibility. Do not create a compatibility claim merely to pass this check;
report actual coverage and remaining risk, not a count of green checks.
