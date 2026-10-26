# v0.6.0 reuse decision

- Need: Categorized change budgets, concise governance and session version notices.
- Search date: 2026-10-21
- Public sources searched: [Git diff](https://git-scm.com/docs/git-diff), [ls-remote](https://git-scm.com/docs/git-ls-remote), [cloc](https://github.com/AlDanial/cloc), [scc](https://github.com/boyter/scc).
- User-provided codebases checked: Agent Builder; no additional repository supplied.
- Candidate fit: Git supplies diffs/refs; cloc and scc count languages but lack governance and version checks.
- Utilization and maintenance: Established counters with visible tests; cloc 2.10 released July 2026. Existing Git already required.
- Tests and security history: Git fixture verified rename/binary/untracked/count behavior; cloc/scc security pages show no published advisories, not an audit. Neither installed.
- License obligations: Invoke installed Git/Python; no redistribution. Agent Builder MIT; cloc GPL-2.0 plus notices; scc MIT.
- Setup and operating burden: No new dependency; cloc needs Perl/binary, scc a binary.
- Outcome: adapt
- Evidence-backed reason: Two small stdlib helpers bridge Git mechanics to approved budgets and metadata notices; another counter adds setup without solving scope control.
- Author confirmation: "ok build" after reviewing the implementation, budgets and cleanup.
- Decision record: AB-D090
- Reused components and replaceable boundary: Git subprocesses, existing seeder/checker/renderer, unchanged pinned Spec Kit.
- Failure behavior and robustness: Fail on invalid budgets; unavailable/invalid remote information stays unknown. No fetching or updating code.
- Why this is the simpler, maintainable option: Standard-library scripts copied into new projects; existing instruction entrypoints, no hook lifecycle.

Local evidence: Git 2.54.0 (Apple Git-157), Python 3.9.6. Codex 0.163.0-alpha.10.2;
Claude unavailable. Actual session behavior requires Review. The local/shared split is
our choice, informed by GitHub's focused README, Issues and tag-based release conventions.

2026-10-26, v0.6.1 maintenance: reuse the accepted Git/Python adaptation above.
The observed gaps are physical-line-only reporting and insufficiently explicit presentation/
test instructions; extend existing code and instruction sources without a new dependency.

2026-10-26, v0.6.2 maintenance: retain the existing Python seeder; no new dependency.
The installed payload omits one template. Propose an ordinary source filename with exact
output mapping; actual-channel Review must confirm delivery. Omission stage remains unknown.
