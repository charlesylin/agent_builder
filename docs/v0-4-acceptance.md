# v0.4.0 acceptance

**Accepted:** 2026-10-06 by Charles Yang Lin, project author

**Release:** `0.4.0` (`v0.4.0` tag)

The author accepted this version for organization use after reviewing Erico's real Codex
skill-building test and the correction that keeps bundled Spec Kit files from appearing
as separate skills. Review is closed. The next Define iteration is deliberately not
open; members will use the release and report what works or fails before another build
cycle is considered.

## What the evidence supports

- The approved Build produced a pinned Spec Kit 1.1.0 bundle and new Claude Code/Codex
  seeds for `agent`, `skill`, and `project` kinds. Disposable tests on both hosts
  produced the expected research artifact; six clean-copy host/kind seeds and helper
  checks passed. These pilots did not verify public sources. See
  [Build verification](v0-4-build-verification.md).
- Erico's Computerator test used Agent Builder 0.4.0 on Codex from source commit
  `c871984`. The supplied agent-authored execution record says Agent Builder read the
  bundled Codex research, specification, plan, tasks, and analysis instructions,
  supplied project context, and ran selected bundled Bash helpers. The project
  produced sourced research, an adapt recommendation, one feature specification,
  plan, tasks, and a consistency analysis. Erico confirmed the adapt/build direction.
  The full chat transcript and his own comparison with v0.3 were not supplied.
- During Review, the 14 upstream instruction files were renamed without changing
  their contents, and Agent Builder's references and manifest were updated. A fresh
  Codex 0.159.2 skill inventory listed Agent Builder but no Spec Kit entries. The
  release bundle check, render check, 75 repository tests under Python 3.9 and 3.14,
  Ruff lint/format, and skill validation passed after that correction. No live
  project session was rerun after the rename.

## What this release does not claim

The suitable-public-solution adopt-and-archive scenario was not run for v0.4. The
analysis was not challenged with a deliberately planted semantic contradiction.
The full installed-host/kind matrix was checked structurally, not through six real
user sessions. There is no measured time or quality comparison with v0.3 and no
independent replay of Erico's complete session. The older Claude plugin eval suite
was not rerun for this release. These are explicit limits of the
evidence, not passing results. The author chose to release now for broader
organization use with these limits visible.

Feedback from that use should focus on actual adoption recommendations, the value
and burden of the added planning detail, record duplication, and failures that keep
a member from using the release. Improvements are candidates for a later Define
cycle; none is silently added to v0.4.0.
