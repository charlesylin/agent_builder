---
id: work-small-fail-loudly
title: Work small and fail loudly
---
Start with the smallest function or vertical slice that produces testable output. Validate
each increment with realistic inputs. Unsupported capabilities and invalid states produce
clear failures; they are never silently ignored. Record exact versions, inputs, commands,
and limitations behind compatibility claims.

In Plan, establish the expected normal result, failure response, and relevant boundary for
each changed behavior. Ask the author when an expectation changes the product or needs control
data; otherwise state a reasonable assumption. Run one-off feasibility checks in a temporary
location and keep their scripts and raw output out of Git. Record a concise finding and exact
version and command when a check supports a decision. Retain a focused regression test in
Build when it protects a recurring defect or a supported compatibility promise; a one-off
configuration fix may be sufficiently checked without adding a test.

For a correction to an existing project, state the observed failure, its evidenced cause,
the smallest direct fix, and whether an earlier experiment already validated that fix.
Before proposing a larger Build, name the concrete failure that would remain after the direct
fix. Add a wrapper, runtime check, or dependency only when it addresses an evidenced
remaining failure; "more robust" alone is not a reason. Defer unsupported safeguards to
`planning/later.md`. A documented host-specific assumption and repeatable check may suffice
without a generalized discovery layer. If proposed work is substantially larger than the
direct fix, justify that difference before Build, including after any Spec Kit analysis.

For a correction that restores already agreed behavior, keep Plan to a short note of the
failure, cause, direct change, repeatable check, and exclusions. Reuse the project's existing
build-or-adopt decision if the solution choice has not changed; do not restart Spec Kit idea
assessment or feature planning for this maintenance path. A new capability, changed contract,
or changed solution choice takes the normal version-sized Plan path. At the existing Plan-to-Build
approval, state the direct change, what evidence will count as done, and what is out of scope.
Stop Build when that evidence passes. Before adding unplanned machinery, a persistent test,
a broader test run, or documentation, name the concrete failure it would prevent. Defer it if
none is evidenced; seek author approval if it materially expands the agreed scope. Routine
adjustments within that scope need no new approval.

Size and testing must be proportional to the approved outcome. Before Build, show
estimated additions/removals/net/percent against a fixed clean commit, grouped by code
language, tests, instruction Markdown, documentation and named miscellaneous types.
Approve paths and gross addition/removal ceilings; run the change-budget helper after
coherent edits and before commits. Re-estimate overruns with the author, never silently
raise limits. Generated/vendor content and binary files/bytes remain visible.
Every persistent test must protect supported functionality or a continuing guarantee;
name what a failure would break. Drop wording-only assertions and redundant checks.
Run focused checks, label lint/packaging honestly, and stop when agreed evidence passes.

Before each manual commit after seeding, inspect tracked, staged, and untracked changes.
Stage only the durable source, tests, and concise records needed for this version. Keep
disposable previews, raw review output, and draft notes out of the commit. Explain unusually
large additions and split independent work when useful, while preserving necessary generated
dependencies.

## Short form

Build the smallest testable capability and stop when its agreed evidence passes. For an
existing failure, prefer the evidenced direct fix and justify any larger safeguard against a
concrete remaining failure. Fail loudly on unsupported or invalid input. Design expected
behavior in Plan; keep one-off checks temporary and commit focused tests for behavior and
supported guarantees. Verify proportionately. Inspect the full staged and untracked change
before committing; keep disposable artifacts out. Record exact versions and commands behind
compatibility claims.
