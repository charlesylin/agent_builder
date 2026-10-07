# v0.4.1 Review evidence

Status: accepted by the author on 2026-10-07; release tag not yet authorized.

The v0.4.1 patch fixes the Windows Git checkout/hash failure without changing
the pinned Spec Kit v1.1.0 payload or relaxing its hash checks. The local
reproduction and 77-test results are recorded in
[Build verification](v0-4-1-build-verification.md).

After the author authorized a push, `main` at
`7260b4237208772080a05feda5edd9e651922359` triggered
[GitHub CI run 37670583643](https://github.com/charlesylin/agent_builder/actions/runs/37670583643)
on 2026-10-07. It completed successfully. All four jobs passed: Windows
Python 3.12, Ubuntu Python 3.9 and 3.12, and lint. The Windows job ran the
new source-bundle and generated-project Git checkout regression tests, as well
as the rest of the suite. This directly resolves the failed Windows CI control
from v0.4.0 [run 37520696645](https://github.com/charlesylin/agent_builder/actions/runs/37520696645).

No organization member has separately installed or used the v0.4.1 candidate
on a Windows workstation. That is an evidence limit, not a failed test. This
patch does not automatically change existing v0.4.0-generated projects.
At that checkpoint, Review remained open pending the author's decision. No
v0.4.1 tag had been created, and the v0.4.0 tag remained unchanged.

After this evidence was read back, the author explicitly closed Review and
opened the next Define cycle. A subsequent documentation-only push at
`d3f90eb0073e74d87a9076ef3bc5c3625e2b5a53` also passed all four jobs in
[GitHub CI run 37670796409](https://github.com/charlesylin/agent_builder/actions/runs/37670796409).
The author accepted v0.4.1 with the workstation-use limit above; no tag was
requested or created.
