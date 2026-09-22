# v0.3.0 Build verification

Date: 2026-09-22. Build is complete for the confirmed lean scope, but the project remains in
Build until the author explicitly opens Review. No v0.3.0 release has been cut or pushed.

## Exercised cases

| Case | Evidence | Result and limit |
| --- | --- | --- |
| Neutral S3 watcher | `ReviewReadinessTests.test_s3_watcher_neutral_project_cli_is_seeded_validated_and_committed` calls the public `seed.py` CLI with `--kind project` in a disposable directory, then checks the generated scaffold, absence of `src/` and agent contracts, first Git commit, and clean worktree. | Pass. This proves scaffold mechanics, not that an S3 watcher was built or tested. |
| DepMap-like adoption | `BuildOrAdoptTests.test_adoption_requires_version_and_archived_status` fills a generic public-skill evaluation, confirms a ledger decision, records the adopted component/version, archives the project, and keeps it in Plan. The Plan-exit check returns `adoption-complete` to block entry to Build. | Pass as a deterministic simulated record. No public skill, including K-Dense's, is a product dependency or preferred answer. A live user/agent adoption recommendation still needs Review. |
| Adapt/build | The Plan gate tests evidence fields, a confirmed decision, technical-quality rationale, one usable goal, and a SemVer deliverable target separate from the Agent Builder template version. Old agent projects without the v0.3 marker still validate. | Pass. The checker verifies completeness and version syntax; it cannot judge whether sources or technical reasoning are true. |
| Fragile shortcut | The skill instructs the agent to challenge a proposed browser side-load using installation, permissions, update, and unattended-operation evidence and to recommend a simpler route if warranted. A test checks that guidance is shipped. | Instruction-level pass only. A live novice conversation is needed to evaluate whether the agent actually pushes back well. |
| Human status | Source principles, skill instructions, generated adapters, and project agreement keep stable internal IDs while asking for plain status, consequential decisions, and a useful next action without forced empty sections. | Structural test passes. Comprehension and process weight require Two River Bio user feedback in Review. |

## Commands and outputs

From the repository root:

```text
python3 -m unittest discover -s tests -q
Ran 64 tests — OK

python3 scripts/render.py --check
exit 0; no generated-file drift

python3 -m compileall -q skills/agent-builder/scripts tests
exit 0

python3 skills/agent-builder/scripts/check.py . --leaving build
May leave build: nothing unresolved.

git diff --check
exit 0
```

The generic `check.py .` scaffold check still does not apply to this legacy *source*
repository: it expects generated-project files and treats template tokens and a synthetic
secret test fixture as defects. It was run before governance commits, with those known
source-layout findings; generated project checks pass. The skill-creator quick validator
could not run in the available Python environments because PyYAML is absent. Existing tests
check skill front matter and render consistency without adding a product dependency.

## Remaining Review questions

- Will a Two River Bio member actually accept a suitable public solution and archive the
  project without being steered into custom work?
- Does the agent challenge a fragile implementation or oversized first version with a clear,
  evidence-backed smaller alternative?
- Can a novice explain status, key decisions, and next action without learning local codes,
  and does the process feel lightweight?

Collect concrete observations rather than inventing a cycle-time threshold without a
baseline. Spec Kit dependency integration remains a separately defined v0.4.0 candidate,
not part of this build.
