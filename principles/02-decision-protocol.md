---
id: decision-protocol
title: Decision protocol
---
A substantive decision changes purpose, scope, authority, facts, architecture, contracts,
dependencies, security posture, data handling, outputs, or deployment. Routine mechanical work
implementing an approved decision does not require separate approval.

- Present consequential recommendations with rationale and evidence. If the author has already
  explicitly authorized the exact choice, record that confirmation without asking again;
  otherwise request confirmation before marking the decision confirmed.
- Surface low-confidence decisions individually with alternatives, tradeoffs, and missing
  information.
- Record decisions with stable internal identifiers and one of `proposed`, `confirmed`,
  `rejected`, or `superseded`. Explain them to people in ordinary language unless an identifier
  is useful for audit or lookup. Never silently reverse a confirmed decision.
- A `proposed` decision does not survive a phase close. Before the phase ends it is confirmed,
  rejected, or moved to `planning/later.md`; `check.py --leaving <phase>` refuses otherwise.
- Approval of a consequential choice that has not already been explicitly authorized — purpose,
  smallest version, phase change, seeding, a remote, or authority to send, spend, publish, or
  delete — is typed by the author in their own words after the exact choice has been read back.
  Do not use a menu pick or button as a substitute, but do not create a second approval round
  for the author's own clear instruction. Routine execution inside an approved plan needs no
  extra ceremony.

## Short form

Keep substantive choices in `governance/decisions.yaml` with stable internal IDs and explicit
status. Speak about their meaning, not their codes. A clear author instruction is confirmation;
otherwise ask for typed agreement on consequential choices, not routine implementation.
Proposals do not survive a phase close. Never silently overturn a confirmed decision or expand
scope across a phase boundary.
