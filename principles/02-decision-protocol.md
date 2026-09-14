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
- A `proposed` decision does not survive a phase close. Before the phase ends it is confirmed,
  rejected, or moved to `planning/later.md`; `check.py --leaving <phase>` refuses otherwise.
- Approval of anything that shapes the project — purpose, smallest version, phase change,
  seeding, a remote, or authority to send, spend, publish, or delete — is typed by the author
  in their own words after the exact text has been read back. It is never a menu pick, a
  numbered option, or a button; an approval that can be clicked without reading is not one.

## Short form

Record substantive choices in `governance/decisions.yaml` with a stable ID and one of
`proposed`, `confirmed`, `rejected`, or `superseded`. Ask before marking anything confirmed;
for purpose, smallest version, phase changes, seeding, remotes, and authority to send, spend,
publish, or delete, read the exact text back and require typed agreement, never a menu pick.
Proposals do not survive a phase close. Never silently overturn a confirmed decision or expand
scope across a phase boundary.
