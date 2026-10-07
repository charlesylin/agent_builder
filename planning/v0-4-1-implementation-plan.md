# Agent Builder v0.4.1 — implementation plan

Status: approved by the author on 2026-10-07; Build is open.
Scope: the Windows checkout/hash patch in
[the Define record](v0-4-1-definition.md). The
[build-or-adopt evaluation](v0-4-1-solution-evaluation.md) recommends Git's
existing attributes mechanism.

## Change

1. Add a root `.gitattributes` rule that marks the entire pinned
   `skills/agent-builder/vendor/spec-kit/` payload `-text`. Git must not
   rewrite any of the 25 manifest-listed files on checkout; the committed
   upstream bytes and hashes stay unchanged.
2. When the seeder includes Spec Kit assets for Claude Code or Codex, also
   create a narrow `.gitattributes` in the new project. Mark the six
   `.specify/scripts/bash/` helpers, four `.specify/templates/` files, and
   `third_party/spec-kit/LICENSE` `-text`. Gemini-only projects keep their
   prior scaffold. Do not add a global line-ending rule for ordinary project
   files or relax the hash checks.
3. Add regression coverage that uses a Git checkout with
   `core.autocrlf=true`: verify the source bundle, then seed and Git-round-trip
   a project for each target host and check its pinned assets. Retain a
   negative test that detects a real byte change. Run the existing all-kind
   seed tests, bundle verifier, generated-file check, unit suite, and lint.
4. Set release metadata and the seeded template version to `0.4.1`; update
   affected exact-version tests and the changelog. Do not move the published
   `v0.4.0` tag, silently update older projects, or publish/tag v0.4.1 during
   Build.

## Why this boundary

`-text` is chosen over `text eol=lf` because the contract is exact upstream
bytes, not merely a preferred newline style. The current pinned assets are LF
in Git's index; Git's documented `-text` behavior leaves those bytes alone on
check-in and checkout. Scope the rules to pinned files so ordinary project
source can follow its owner's line-ending policy. The seeder already writes
the pinned assets as bytes, and the checker already detects drift; neither
needs a new normalization layer.

The proposed patterns were tested in temporary Git repositories on 2026-10-07.
Before adding attributes, a `core.autocrlf=true` clone failed the source bundle
verifier, and a seeded project's clone failed on all eleven pinned assets.
After committing the proposed attributes to those temporary repositories and
cloning again with the same setting, the source bundle verifier and seeded
project checker both passed; `git ls-files --eol` reported `i/lf w/lf attr/-text`
for representative pinned files. This tests Git's behavior without changing
the product repository during Plan.

## Verification and limits

Build is done only if the local `core.autocrlf=true` reproduction passes for
both source and seeded project after a fresh checkout, existing checks pass,
and the negative drift case still fails. The GitHub Windows CI job should pass
after the patch is pushed, but no push is authorized by this Plan approval
alone. A simulated CRLF checkout on macOS is strong regression evidence, not
a claim that Windows CI already passed. Existing v0.4.0 projects are not
rewritten by this release.
