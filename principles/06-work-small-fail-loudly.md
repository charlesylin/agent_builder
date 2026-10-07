---
id: work-small-fail-loudly
title: Work small and fail loudly
---
Start with the smallest function or vertical slice that produces testable output. Validate
each increment with realistic inputs. Unsupported capabilities and invalid states produce
clear failures; they are never silently ignored. Record exact versions, inputs, commands,
and limitations behind compatibility claims.

For changed behavior, establish the expected normal result, failure response, and relevant
boundary before implementation. Ask the author when an expectation changes the product;
otherwise state a reasonable assumption and proceed. Add focused unit tests for those cases
and run them with the project's test runner. Say what a check verifies and what remains
untested; compiling or validating a scaffold does not prove product behavior.

Before each manual commit after seeding, inspect tracked, staged, and untracked changes.
Stage only the durable source, tests, and concise records needed for this version. Keep
disposable previews, raw review output, and draft notes out of the commit. Explain unusually
large additions and split independent work when useful, while preserving necessary generated
dependencies.

## Short form

Build the smallest testable capability, validate it, then extend it. Fail loudly on unsupported
or invalid input. Test changed behavior's normal, failure, and boundary cases. Inspect the
full staged and untracked change before committing; keep disposable artifacts out. Record
exact versions and commands behind any compatibility claim.
