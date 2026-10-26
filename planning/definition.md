# Agent Builder v0.6.1

Maintenance scope confirmed 2026-10-26; Plan opened by the author.
Users: people building agents, skills and tools with Agent Builder.

## Problem and smallest useful correction

v0.6.0 budgets are not consistently surfaced in conversation, physical-line limits
can reward compressed code, and testing still grows beyond the behavior that matters.

- Show budgets to the user at approval, meaningful Build updates and closeout.
- Retain added/removed lines and category/language breakdowns, alongside codebase
  growth percentages that distinguish formatting from substantive growth. Preserve readability.
- Define the minimum necessary unit-test cases against the behavior contract in Plan;
  implement those tests and build toward them. Keep temporary experiments local.
  Every retained test must protect functionality or a supported guarantee.

## Success evidence and exclusions

Review sees estimates and actuals in conversation, no incentive to compress readable
code, and a clear connection between each retained test and a meaningful failure.
The measurement method, size estimate and focused checks will be proposed in Plan.
Larger v0.7 work, new analysis frameworks, runtime notices and automatic migration are out.

Accepted v0.6.0 scope: `d093440:planning/definition.md`.
