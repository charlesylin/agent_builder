# v0.5.0 Define: lean, understandable, behavior-tested builds

Status: outcome and broad scope confirmed by the author on 2026-10-07. The
version target remains tentative; exact success evidence and the meaning of
"very large" are still open. Agent Builder remains in Define.

## Problem and value

Recent Two River Bio projects have accumulated too much code and too many
committed previews, drafts, review notes, and other temporary files. Human
documentation remains hard to read. Routine checks run, but new behavior is
not consistently covered by thorough unit tests. Large, hard-to-inspect
commits make it difficult for members to trust and maintain the result.

The useful outcome is that each Build increment leaves a small, understandable,
behavior-tested repository without losing the decisions or evidence needed to
resume work. Two River Bio members are the primary users; Agent Builder should
remain useful outside the organization.

## Smallest usable result

- Before a commit, inspect the full change and account for unusually large
  additions. Keep temporary previews, raw reviewer output, and draft notes
  out of the committed repository; retain only concise, durable conclusions.
- Make human-facing documentation explain what the project does, how to use and
  verify it, and its important limits, without making readers decode agent
  records.
- For changed behavior, define expected results and add unit tests for normal,
  failure, and boundary cases. Describe what each check actually verifies.
- During Review, when the change is very large, ask the user whether they want
  an independent code review. For Two River Bio, Erico's code-review-agent is a
  candidate reviewer. Do not run it without the user's choice. A fresh review
  should not inherit the builder's conclusions and must disclose skipped files
  and other limits; no automated review can be promised to be bias-free.

Do not bundle a private organization tool into general Agent Builder, force
automatic review, or create more permanent reports to demonstrate compliance.
The exact large-change signal and reviewer invocation belong in Plan.

## Evidence still to define

Agree on realistic before/after cases: an oversized change with disposable
artifacts, a behavior change with expected results and meaningful unit tests,
a member reading the human documentation, and a Review in which the user can
accept or decline independent review. Record what was checked and what was
skipped. No phase change or Build authorization is implied by this record.
