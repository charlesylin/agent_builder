# v0.2 acceptance record

**Closed:** 2026-09-22
**Accepted by:** Charles Yang Lin, project author
**Decision:** AB-D039
**Release:** `0.2.1`
**Tag:** `v0.2.1`

Agent Builder v0.2 is accepted at release 0.2.1. The author explicitly closed Review and
opened the next Define iteration after confirming the organization-install acceptance test.

## What acceptance rested on

- Sean, the intended novice user, used the organization-installed v0.2.1 plugin on Windows
  without separate local setup and reached a seeded, validated, committed Define-phase project
  in one session. The author confirmed this result on 2026-09-22; Sean's repository and full
  transcript are not published here.
- A week of extended use produced F-018 through F-025. The findings are substantive and are
  carried into the next Define, but they do not invalidate v0.2's scoped deliverable: an
  installable governance skill with deterministic seeding, checking, rendering, and phase
  behavior.
- The author's judgment that v0.2.1 is a useful, accepted stepping stone rather than an attempt
  to complete Agent Builder in one cycle.

## Success signals

| Signal from `docs/v0-2-define.md` | Outcome |
| --- | --- |
| Windows colleague reaches a seeded, validated, committed Define project through the organization install | Met by Sean; author-confirmed evidence above. |
| One principle edit propagates everywhere and CI proves it | Met by the single-source renderer and drift test. |
| A fresh seeded-repository session recovers phase and decisions without a file list | Met in the recorded run-2 resume test. |
| Evals cover triggering and refusal to advance a phase on momentum | Met with a qualification: behavior cases and deterministic hook tests pass; the description-only trigger baseline was 48%, so AB-D032 made explicit invocation primary and added the tested offer hook. |
| Agent Builder's skill is produced by its own skill template | Met in substance by B8 dogfood; intentional source-repository differences are recorded as F-016. |

The 2026-09-22 closeout reran the Review exit gate, generated-file drift check, compilation,
and 54 unit and behavioral tests successfully. Ruff 0.16.6 was not installed in the active
local environment for the documentation and governance closeout; the accepted v0.2.1 release
itself passed the full pinned gate on 2026-09-14.

The full generated-project scaffold check is not applicable to this source repository: it
predates `.agent-builder.json`, contains template tokens by design, and has the larger plugin
layout recorded in F-016. The phase-specific `check.py . --leaving review` gate passed before
the transition. Missing scaffold files were not fabricated to make an inapplicable check green.

## Findings carried into the next Define

F-018 through F-025 are inputs, not confirmed scope or selected solutions:

- make public-solution discovery a build-or-adopt decision;
- scope every cycle to a version-sized MVP;
- discover and reuse organizational code while producing reusable modules;
- discover available or configured skills and capabilities;
- add a neutral `project` kind, now backed by real-use evidence;
- apply a technical-quality gate to recommendations made to novices;
- use explicit standard versions as deployable and testable stepping stones; and
- have authors define expected results, cases, hypotheses, and controls.

The full evidence and unresolved design choices are in `docs/v0-2-review-feedback.md`.

## Not decided by acceptance

- The next version number, purpose, and scope.
- Whether organizational repositories and capabilities are discovered through conversation,
  user configuration, organization configuration, or a combination.
- The versioning convention for non-software projects.
- Which test commitments belong in Define versus Plan.
- Codex guarantees beyond the best-effort support accepted for v0.2.
- F-016 (`planning/` versus `docs/` in this legacy source repository) and the remaining F-017
  Cowork hook and clean first-run observations.
