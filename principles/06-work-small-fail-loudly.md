---
id: work-small-fail-loudly
title: Work small and fail loudly
---
Start with the smallest function or vertical slice that produces testable output. Validate
each increment with realistic inputs. Unsupported capabilities and invalid states produce
clear failures; they are never silently ignored. Record exact versions, inputs, commands,
and limitations behind compatibility claims.

## Short form

Build the smallest testable capability, validate it, then extend it. Fail loudly on unsupported
or invalid input. Record exact versions and commands behind any compatibility claim.
