# v0.4.1 build-or-adopt evaluation

Checked 2026-10-07 for the narrow Windows checkout failure in
[the Define record](v0-4-1-definition.md). This is a repair to Agent Builder's
existing distribution, not a new application. No organizational codebase was
offered for this patch; the relevant existing solution is Git's own attributes
mechanism.

## Evidence

In a local clone made with `git -c core.autocrlf=true clone`, Git reported the
bundled Spec Kit files as `i/lf w/crlf attr/`, and
`python3 scripts/refresh_spec_kit.py --check` failed on the MIT notice. A
newly seeded project committed and cloned under the same setting reported drift
for all eleven pinned assets. The source files are LF in Git's index and have
no attributes override. This reproduces the failure without a Windows host;
the published v0.4.0 Windows CI result remains the real-host observation.

[Git's `gitattributes` documentation](https://git-scm.com/docs/gitattributes)
states that unsetting `text` on a path disables check-in and checkout line-ending
conversion, even when `core.autocrlf` would otherwise control it. It also
documents `text eol=lf`, which normalizes text to LF. Both are built-in Git
features with no package, license, or setup burden beyond the Git already used
by these repositories. Git's published documentation and broad use support the
mechanism; this record makes no separate claim that it has been security-audited.

## Routes

| Route | Fit and cost | Verdict |
| --- | --- | --- |
| Adopt a new external tool | Adds a dependency to solve a Git checkout behavior that Git itself controls. No separate tool improves this exact need. | Reject. |
| Adapt the repositories with narrow `.gitattributes` rules | Preserves manifest hashes and upstream assets without new runtime code or member setup. Applies to the source bundle and newly seeded projects. | Recommend. |
| Normalize CRLF in the hash checker | Would allow modified working-tree bytes to pass as pinned assets and could leave Bash scripts with CRLF on Windows. Adds custom logic to both verifier and generated-project checker. | Reject. |
| Set `core.autocrlf=false` only in CI or tell members to change Git config | Could make one checkout pass but leaves organization Windows installations and generated projects vulnerable. | Reject. |

The recommendation reuses Git's established attribute mechanism rather than
building a line-ending repair tool or replacing Agent Builder. Existing
v0.4.0-generated projects remain unchanged; any migration would be explicit.
