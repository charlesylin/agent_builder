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
version and command when a check supports a decision. If it reproduces a defect or establishes
a supported compatibility promise, retain a focused regression test in Build.

In Build, add focused unit tests for changed logic and persistent contract or integration tests
for supported dependency, host, environment, or external-boundary guarantees. Run the relevant
tests and say what each verifies and what remains untested. Label lint, compilation, packaging,
and scaffold checks by their actual purpose; they do not prove product behavior. If test code
exceeds first-party source code, review it for duplication and obsolete setup, but do not cut
valuable boundary tests or inflate implementation to meet a line ratio.

Before each manual commit after seeding, inspect tracked, staged, and untracked changes.
Stage only the durable source, tests, and concise records needed for this version. Keep
disposable previews, raw review output, and draft notes out of the commit. Explain unusually
large additions and split independent work when useful, while preserving necessary generated
dependencies.

## Short form

Build the smallest testable capability, validate it, then extend it. Fail loudly on unsupported
or invalid input. Design expected behavior in Plan; keep one-off checks temporary and commit
focused tests for behavior and supported guarantees. Inspect the full staged and untracked
change before committing; keep disposable artifacts out. Record exact versions and commands
behind compatibility claims.
