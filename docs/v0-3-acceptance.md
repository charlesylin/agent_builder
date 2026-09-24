# v0.3.0 acceptance

**Accepted:** 2026-09-24 by Charles Yang Lin, project author

**Release:** `0.3.0`

**Tag:** `v0.3.0`

The author reported that all three agreed real-use Review scenarios passed and explicitly
confirmed acceptance. The author then asked to push and use v0.3.0 for a while before
advancing to v0.4.0, so Review remains the current phase for post-release observations.
This accepts the lean project-mode release as a useful stepping stone, not as a complete
solution to every project workflow.

## Real-use evidence

1. **Adopt instead of build:** the author reported the scenario passed. The expected behavior
   was to assess a suitable public solution, recommend using it rather than custom code, and
   archive the project after confirmation without entering Build.
2. **Build one usable project version:** the author reported the scenario passed. It exercised
   neutral `project` mode, a version-sized outcome, reuse, and technical-quality pushback.
3. **Cold resume:** the author reported the scenario passed. It exercised a fresh user's
   ability to understand project status, important decisions, and next action without
   decoding internal identifiers or unnecessary ceremony.

The author supplied pass results, not transcripts, project links, tested-host details, or a
source commit for these three sessions. Their detailed behavior is therefore author-reported,
not independently reproducible from this repository. The simulated adoption and neutral
seeding checks in `docs/v0-3-build-verification.md` provide separate mechanical evidence.

## Boundary and next iteration

v0.3.0 requires the formal build-or-adopt evaluation during Plan, before Build. A quick
pre-seed check during Define was discussed in Review but was not a v0.3.0 acceptance gate;
whether to require it remains a v0.4.0 Define question. Organizational-repository
configuration, Grafify or skill discovery, formal testing/controls, and Spec Kit integration
were outside this release.

The next iteration's candidate direction, from the prior release split, is a maintained
Spec Kit dependency with targeted replacements. v0.4.0 Define has not yet opened; exact
scope and success evidence remain to be defined rather than assumed from that direction.
