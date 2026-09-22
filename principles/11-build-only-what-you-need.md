---
id: build-only-what-you-need
title: Build only what you need
---
Feature completeness is not the goal; delivering the stated value with the fewest moving parts
is. A thing that does four things correctly is more valuable than one that claims fifteen and
does twelve right. Scope can expand as the project matures; it cannot easily contract once
people depend on it.

Every project states, in `planning/definition.md`, the smallest version that delivers its value
and what is deliberately not in the first version. Record its own next deliverable as a
Semantic Versioning `MAJOR.MINOR.PATCH` target in `governance/project-state.yaml`, separate
from the Agent Builder template version. Ask what would make `v0.1.0` usable for a new project,
or what the next appropriate stepping stone is for an existing one. Each cycle delivers one
usable result, not the whole imagined product. A proposal that is not needed for that result
goes to `planning/later.md`, not into scope, however good it is. Ideas are kept; they are not
built until the author asks for them in their own words.

## Short form

Target one usable, SemVer-numbered deliverable per cycle; state what is not in it. Anything else —
including your own good ideas and every closeout question — goes to `planning/later.md`, not
into scope, until the author asks for it in their own words. Scope expands easily and contracts
badly.
