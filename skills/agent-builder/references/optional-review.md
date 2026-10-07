# Optional independent code review

Read this only after the user accepts the large-change Review offer. A fresh
reviewer should see the code, original problem, and expected behavior, but not
the builder's conclusions. Ask them to report reviewed and skipped files,
important findings, and uncertainty. A second session is not guaranteed unbiased.
Do not install a tool, index repositories, post results, or commit raw output
without the member's authorization.

Use a reviewer suited to the changed material. Two River Bio's
[`code-review-agent` v0.1.0](https://github.com/tworiverbio/code-review-agent/tree/v0.1.0)
is an **optional organization-only** choice for Python code. It is not bundled
with Agent Builder and has no selected license for external distribution.
For non-Python code or a prose-only skill, choose a capable independent review
instead; do not install this tool merely to satisfy the offer.

For a Two River member who opts in:

1. Check that `tr-review --help` works and that the `tr-review` skill is visible
   in the active Codex or Claude Code host. These are separate installations.
   Check GitHub SSH access and `uv` before offering the pinned CLI install.
2. If the skill is missing, offer the appropriate host setup, then verify
   discovery in a new session. Claude Code:

   ```sh
   claude plugin marketplace add tworiverbio/claude-plugins
   claude plugin install tr-review@tworiver
   ```

   Codex:

   ```sh
   codex plugin marketplace add git@github.com:tworiverbio/claude-plugins.git
   codex plugin add tr-review@tworiver
   ```

   If Codex's marketplace route fails, the [reviewer README](https://github.com/tworiverbio/code-review-agent/blob/v0.1.0/README.md)
   documents a local skill-folder fallback. Diagnose rather than claiming the
   untested route worked.
3. If the command is missing, offer the [pinned CLI install](https://github.com/tworiverbio/code-review-agent/blob/v0.1.0/README.md)
   and confirm it after the member authorizes installation:

   ```sh
   uv tool install git+ssh://git@github.com/tworiverbio/code-review-agent@v0.1.0
   tr-review --help
   ```

   A PATH change may be needed; ask before changing the member's shell setup.
4. Use a fresh review session with the original goals and a specific target.
   Repository onboarding clones and indexes code, so obtain the member's
   consent before running it. Branch/PR mode checks committed Python changes;
   path mode can read working-tree files. The packet has a 150,000-character
   source cap and can skip files. Examine its searched/skipped report, verify
   findings with `tr-review validate`, and state coverage plainly. Keep raw
   packets and reviewer output outside the committed repository; summarize
   durable conclusions only.

The [Two River marketplace](https://github.com/tworiverbio/claude-plugins) declares
the skill for both hosts, but installation was not live-tested on both in the
v0.5.0 Plan. The [reviewer source](https://github.com/tworiverbio/code-review-agent/blob/v0.1.0/src/two_river_code_review_agent/packet.py)
and [acceptance feedback](https://github.com/tworiverbio/code-review-agent/blob/v0.1.0/planning/acceptance-feedback.md)
document its scope and skipped-file risk.
