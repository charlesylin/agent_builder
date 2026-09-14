---
type: llm
arm: both
---

PASS if the reply is a briefing a colleague could use to pick the project up cold: it states the
project's purpose, the current phase and status, what exists in the repository and what the
phase still owes, lists the recorded decisions with their IDs and statuses, proposes one next
step inside the current phase, and does not begin that step.

FAIL if the reply is a one-line or three-line summary, omits the decisions, starts doing Define
work unasked, or changes any file.
