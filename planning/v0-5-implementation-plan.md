# Agent Builder v0.5.0 — proposed implementation plan

**Status:** Approved by the author on 2026-10-07; Build is open. The [Define record](v0-5-definition.md)
sets the outcome; the [reuse evaluation](v0-5-solution-evaluation.md)
recommends a small adaptation of existing Agent Builder instructions and templates.

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
