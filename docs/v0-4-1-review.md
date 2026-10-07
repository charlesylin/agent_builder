# v0.4.1 Review evidence

Status: evidence complete; author acceptance and release tag pending.

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
Review remains open until the author decides whether to accept v0.4.1. No
v0.4.1 tag has been created, and the v0.4.0 tag remains unchanged.
