---
id: decision-protocol
title: Decision protocol
---
A substantive decision changes purpose, scope, authority, facts, architecture, contracts,
dependencies, security posture, data handling, outputs, or deployment. Routine mechanical work
implementing an approved decision does not require separate approval.

- Present high-confidence recommendations with their rationale and evidence, then request
  confirmation before recording them as confirmed.
- Surface low-confidence decisions individually with alternatives, tradeoffs, and missing
  information.
- Record decisions with stable identifiers and one of `proposed`, `confirmed`, `rejected`, or
  `superseded`. Never silently reverse a confirmed decision.

## Short form

Record substantive choices in `governance/decisions.yaml` with a stable ID and one of
`proposed`, `confirmed`, `rejected`, or `superseded`. Ask before marking anything confirmed.
Never silently overturn a confirmed decision or expand scope across a phase boundary.
