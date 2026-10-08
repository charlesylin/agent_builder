# v0.5.0 Define: lean, faster, behavior-tested cycles

Status: Define closed by the author on 2026-10-07; Review is open. Target:
v0.5.0. This record owns the agreed outcome and Review evidence, not the
implementation method.

## Problem and value

Recent Two River Bio projects have accumulated too much code and too many
committed previews, drafts, review notes, and other temporary files. Human
documentation remains hard to read. Routine checks run, but new behavior is
not consistently covered by thorough unit tests. Large, hard-to-inspect
commits make it difficult for members to trust and maintain the result. Too
many nonblocking questions also slow cycles and invite scope growth.

The useful outcome is a faster path through each version-sized cycle, leaving
a small, understandable, behavior-tested repository without losing decisions
or evidence needed to resume work. Two River Bio members are the primary users;
Agent Builder should remain useful outside the organization.

## Smallest usable result

- Before a commit, inspect the full change and account for unusually large
  additions. Keep temporary previews, raw reviewer output, and draft notes
  out of the committed repository; retain only concise, durable conclusions.
- At each interaction, ask the user only when a decision or missing input is
  needed to move the current work forward safely and correctly. Record other
  issues once in the existing `planning/later.md` and continue; do not turn
  every reply into a question list. Check proposed work against the initial
  problem, the agreed smallest outcome, or the task in this cycle. If it does
  not advance one of those, say so plainly, recommend finishing this cycle,
  and defer it unless the author explicitly changes scope.
- Make human-facing documentation explain what the project does, how to use and
  verify it, and its important limits, without making readers decode agent
  records.
- For changed behavior, define expected results and add unit tests for normal,
  failure, and boundary cases. Describe what each check actually verifies.
- During Review, when the change is very large, ask the user whether they want
  an independent code review. For Two River Bio, Erico's code-review-agent is a
  candidate reviewer. If the user accepts, check that its skill and command are
  available on their Codex or Claude Code host; if not, help them install and
  verify both. Do not install or run it silently. A fresh review should not
  inherit the builder's conclusions and must disclose skipped files and other
  limits; no automated review can be promised to be bias-free.

Do not bundle a private organization tool into general Agent Builder, force
automatic installation or review, add a visible checklist to every reply,
create more permanent reports to demonstrate compliance, or retroactively
rewrite existing projects. The exact large-change signal below its obvious
case and host-specific installation steps belong in Plan.

## Review evidence

1. In the same small project scenario, Agent Builder asks about a real blocker,
   records nonblocking issues once for later, and continues without extra user
   turns. When offered an off-scope idea, it explains why the current outcome
   comes first. Compare this with v0.4.0 behavior; do not claim a faster cycle
   without observing fewer interruptions or shorter time to the same outcome.
2. In a Build example containing a behavior change and disposable previews or
   reviewer notes, the committed result contains only durable files, concise
   human instructions, and unit tests for expected, failure, and boundary
   behavior. A member can say what it does, how to run and test it, and its
   important limits without reading the machine ledger.
3. A change like the author's `+10000 / -30` example always counts as very
   large. Review offers an independent code review; declining runs nothing.
   On acceptance, a missing reviewer leads to host-appropriate installation
   help and verification on Codex and Claude Code. The review states its
   actual coverage and skipped files. Plan should set a proportionate signal
   for smaller changes without making normal increments require extra prompts.

Keep the exact commands, thresholds below the obvious case, and any tool
adaptation in Plan. No Build authorization is implied.

## Review feedback: minimum sufficient fix

The author reports that a Project Aurora container used UID 10001 against
Mac-mini files owned by UID 501, after a one-run UID 501 override had already
worked. The eventual fix was a `501:20` live Compose service setting and a
resolved-configuration check. The agent also built a discovery wrapper,
application-level preflight, tests, and extensive notes; these addressed no
demonstrated second failure and were removed. This is reported user experience,
not a verified v0.5.0 test run.

For corrective work, the next Plan amendment should require the observed
failure, evidenced cause, smallest direct fix, and any prior validating trial.
Before adding a wrapper, runtime check, dependency, or lasting test, identify
the concrete failure that would remain after that fix; otherwise defer it.
Scale verification and documentation to the actual change. A large proposed
implementation must justify the additional failure it prevents before Build.
