# v0.4.0 build-or-adopt evaluation

Checked 2026-10-05 for the approved v0.4.0 outcome in
[`v0-4-definition.md`](v0-4-definition.md). This is a decision about Agent Builder itself,
not a recommendation that every project it creates should be built.

## Need and sources

Two River Bio members should retain Agent Builder's working project lifecycle and
build-or-adopt gate while gaining Spec Kit-backed research and coherent, version-sized
requirements and tasks after one Agent Builder installation. The author specifically
requested adapting Agent Builder, not replacing it merely to maximize reuse. No other
specific organizational implementation was offered as a v0.4.0 replacement. The author
had previously supplied the Two River Bio GitHub organization as a general reuse source;
a read-only repository and indexed-code search on 2026-10-05 did not identify an existing
Spec Kit integration to adopt there. Private repositories were not exhaustively audited
and no private content was copied into this record. The source repository, its accepted
v0.3.0 behavior, and GitHub Spec Kit are the relevant candidates.

Sources checked: the accepted [v0.3.0 review](../docs/v0-3-acceptance.md),
[Spec Kit v1.1.0 release](https://github.com/github/spec-kit/releases/tag/v1.1.0),
[integration reference](https://github.github.io/spec-kit/reference/integrations.html),
[CLI reference](https://github.github.io/spec-kit/reference/core.html),
[MIT license](https://github.com/github/spec-kit/blob/v1.1.0/LICENSE),
[upstream test workflow](https://github.com/github/spec-kit/actions/workflows/test.yml),
and [security page](https://github.com/github/spec-kit/security). Local pinned-tag probes
are recorded in [`v0-4-spec-kit-feasibility.md`](v0-4-spec-kit-feasibility.md).
The organization check used authenticated `gh repo list` and `gh search code` read-only;
it is a search lead, not an audit of private repositories.

## Candidates and quality evidence

| Route | Fit and reuse | Utilization, maintenance, tests | Security, license, setup |
| --- | --- | --- | --- |
| Adopt Spec Kit alone | It covers idea research and specification/planning, but stock initialization creates its own constitution and feature records. Its idea verdict does not implement Agent Builder's author-approved adopt-and-archive lifecycle, independent release target, or existing organization skill entry point. | The official site reports 130K+ GitHub stars and 270+ contributors; v1.1.0 was released 2026-10-02. The upstream repository has a Test & Lint Python workflow. These are maintenance/use signals, not proof of fit in this organization. | MIT permits distribution with its notice. No published advisory appeared on the checked security page; that is not an audit or proof of safety. Normal member setup requires the CLI and Python 3.11+, then project initialization. |
| Keep Agent Builder v0.3.0 unchanged | Preserves the accepted one-install governance experience, but does not deliver the specified Spec Kit-backed research, requirement-quality, and cross-artifact checks. | Accepted by the author after three real-use scenarios; 64 local tests passed at the last verification. | Existing install path and Python 3.9 floor remain. No new dependency or license burden. |
| Adapt Agent Builder with selected pinned Spec Kit assets | Retains Agent Builder as the authority for purpose, phase, version, adoption, and approvals; uses selected upstream research and build-detail steps without a member CLI or a second lifecycle. | Reuses maintained upstream instructions, scripts, and templates. Release-time regeneration and pinned provenance avoid a hand-maintained fork. Local structural and helper-script probes passed; full host behavior has not. | Bundle the MIT notice and manifest, review changes at every upstream refresh, and keep the CLI's Python 3.11+ requirement in the release build only. Seeded projects need Bash for the selected helper scripts; no `specify` runtime command. |
| Build equivalent workflows from scratch | Could fit Agent Builder exactly but would duplicate a large maintained process and test burden. | No independent utilization or maintenance benefit. | No upstream license, but more local code and more organization maintenance. |

## Recommendation

**Adapt Agent Builder with a pinned, release-time-generated Spec Kit payload.** This is the
smallest route that can meet both the author's reuse goal and the accepted v0.3.0 behavior.
Adopting Spec Kit wholesale would require replacing or duplicating Agent Builder's
governance, and leaving Agent Builder unchanged would not deliver v0.4.0. Do not treat
Spec Kit's own research artifact as a complete build-or-adopt decision: Agent Builder still
checks fit, use, maintenance, tests, security history, license, and setup burden before
recommending adoption or a build.

The recommendation is conditional on the host-behavior and member-install gates in
[`v0-4-implementation-plan.md`](v0-4-implementation-plan.md). The checked security page
and release cadence do not remove the need to review bundled asset changes and
dependencies when refreshing the pin. If the selected route cannot meet the one-install,
single-owner experience without regression, stop and return to Plan rather than ship a
weaker v0.4.0.
