# Agent Builder: next usable version

Target: v0.3.0. Phase: Define. The author has confirmed the purpose, scope, version, and
success evidence. Moving to Plan requires a separate, explicit decision.

## What problem does this solve?

> We want to codify the "project" mode, create a logical versioning system and also enact the
> governance and guidance around re-use, modularity and simplicity

## How is it solved today?

> we are trying to solve for vibe coding creating spaghetti code, re-inventing the wheel, and
> not being scalable to an organization

The current approach relies too much on ad hoc building and recommendations that can enlarge
the product beyond what is needed.

## What is the value if it is solved?

> should formally enact project mode for agent-builder so that will help anyone in the near term
> building projects and it will also improve agent-builder by helping it constrain and simplify
> the user vs. suggesting too much

## Who is it for?

> primary user(s) remain the members of the two river bio organization

## Purpose

The next Agent Builder version will formally enact project mode and establish governance for
logical versioning, reuse, modularity, and simplicity, so Two River Bio members can build
useful project increments without spaghetti code, reinventing existing solutions, or making
choices that cannot scale across the organization. It will also constrain Agent Builder from
proposing more than the user needs.

## Smallest version that delivers the value

Deliver a usable, validated neutral `project` mode that guides a Two River Bio member through
one version-sized MVP. Before Build, require an evidence-backed build-or-adopt decision, a
standard version stepping stone, preference for reusable modular components, and evidence for
the simplicity, robustness, and organizational scalability of technical recommendations.
Maintain structured agent-readable memory while making the human experience plain and
proportionate. Internal identifiers need not appear in human-facing interactions.

## Not in this version

- Organizational-repository configuration.
- Grafify or skill discovery.
- Formal testing or control improvements.

## Versioning

Agent Builder targets v0.3.0 under Semantic Versioning 2.0.0. Each governed project tracks the
versions of its own deliverables independently, with one usable outcome per cycle. If adopting
an existing solution fully resolves the need, record that solution's version and archive the
project without claiming a new project release.

## Success evidence

The main real-use case is a DepMap-like request. Agent Builder identifies a suitable public
solution, records evidence of fit, utilization, maintenance, testing, security history, and
license obligations, recommends adoption, and archives the project after typed author
confirmation without entering Build. Additional Two River Bio feedback should show at least
one of: a shorter path to a useful outcome, more evidence-backed adoption recommendations, or
effective pushback that reduces product sprawl. Do not invent numerical thresholds before a
baseline exists.

In real use, a member should understand status, important decisions, and next action without
decoding internal identifiers. Each approval should have a concrete consequence, and user
feedback should find the process clear and appropriately lightweight.
