# v0.5.0 build-or-adopt evaluation

Checked 2026-10-07 against the [confirmed outcome](v0-5-definition.md).
The question is whether an existing tool can make Agent Builder's cycles
smaller, easier to read, and better tested while preserving its accepted
Define → Plan → Build → Review experience.

| Candidate | Fit, use, and upkeep | Tests, security, license, setup |
| --- | --- | --- |
| [Git status and diff](https://git-scm.com/docs/git-status), already required for Agent Builder's commits | Shows tracked, staged, unstaged, and untracked paths; `--numstat` exposes line counts. Its maintained, widely used built-ins cover change inventory without a new package. They do not decide which artifacts are durable or when to ask a person. | No new distribution or setup. Inspecting metadata is not a secret scan or a security guarantee. Binary files need separate inspection. |
| [Python `unittest`](https://docs.python.org/3/library/unittest.html), already in seeded projects | Existing discovery and CI can run normal, failure, and boundary tests. The framework is maintained with Python, but a passing scaffold test does not prove later product behavior. | No new dependency, license, or installation for the Python projects already seeded. Test quality remains a project-specific judgment. Non-Python projects should use their own test runner. |
| [pre-commit](https://github.com/pre-commit/pre-commit) | Maintained and used hook framework, but it cannot by itself judge whether a draft belongs in a repo, a feature serves the MVP, or a test checks the right outcome. Adding and maintaining hooks in every generated project would add setup and template surface. | Public, MIT-licensed; its [security page](https://github.com/pre-commit/pre-commit/security) shows no published advisories, which is not proof of safety. Local hooks can be skipped and would still need custom rules and tests. Defer for projects that independently want hook enforcement. |
| [Spec Kit](https://github.com/github/spec-kit), already bundled selectively | Its selected specification and consistency steps can expose plan gaps, but they do not own Agent Builder's phase decisions, pre-commit hygiene, user-question triage, or independent code review. Replacing the lifecycle would regress accepted behavior. | The pinned MIT payload is already tested in this repository; its [security page](https://github.com/github/spec-kit/security) lists no published advisories, not a security audit. No member CLI or new upstream assets are needed. |
| [Two River code-review-agent v0.1.0](https://github.com/tworiverbio/code-review-agent/tree/v0.1.0) | Organization candidate for an optional, fresh Review of Python code and duplicate reuse. Its internal repo has a tagged release, CI, and tests. It is not a general-purpose code-size or test-quality gate. Its packet can skip oversized files; [prior acceptance feedback](https://github.com/tworiverbio/code-review-agent/blob/v0.1.0/planning/acceptance-feedback.md) records 32 of 51 files skipped. | No selected license and organization-only access, so do not bundle it in public Agent Builder. Requires a separately installed `tr-review` CLI, a host skill, Python 3.11+, `uv`, and access to relevant repositories. No public security audit was found or claimed. |

**Recommendation: adapt Agent Builder's existing instructions and a few seed
templates, using Git and the project's test runner.** No public candidate
satisfies the combined v0.5.0 need as a drop-in replacement. A new custom
commit-lint or review service would add code, configuration, and enforcement
edge cases to a cycle whose purpose is to reduce that burden. The internal
reviewer is an optional integration after the user accepts a Review offer;
it is neither bundled nor installed automatically.

This is not a claim that prose alone enforces quality. Build should test the
generated instructions and templates mechanically, then Review should observe
the three behavior scenarios in the Define record. If those scenarios fail,
add only the smallest deterministic check that addresses the observed gap in
a later authorized cycle.
