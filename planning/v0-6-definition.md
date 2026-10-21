# v0.6.0 Define: proportionate changes and clear version status

Status: Define approved and closed by the author on 2026-10-21; Plan open.
Target: v0.6.0. The outcome, five requirements, and success evidence below are
approved. Implementation choices remain in Plan; Build is not approved.

## Problem, users, and value

Two River Bio members still see simple fixes produce hundreds of lines, low-value
tests, and excessive committed planning records despite v0.5.0's lean-work guidance.
They also cannot readily tell which version they are using or whether it is current.
Approved outcome: make the smallest next change understandable before approval,
keep implementation, verification, and shared records proportionate, and show
trustworthy version status when starting a session.

## Author-requested requirements

1. **Build size:** before Build approval, estimate additions, removals, net change,
   and percentage growth or reduction by category: code broken down by language
   or implementation type, documentation, and explicitly identified miscellaneous
   files. Make useful cleanup and reduction visible alongside additions. Track
   actual changes against the estimate and enforce proportionate scope during Build.
2. **Useful testing:** choose verification proportional to the change. A retained
   test must protect functionality of the agent, skill, or tool; omit performative
   checks whose failure has no consequence for supported behavior.
3. **Minimal next step:** explicitly flag out-of-scope work for later, show it to
   the author, and ask whether any belongs in the current scope. Recommend saving
   it for later by default; do not silently include it in the Build.
4. **Lean shared governance:** substantially simplify committed governance.
   Distinguish local working notes from durable shared information; avoid large
   committed plans, reviews, and discussion records. Use established GitHub/software
   practices to guide the boundary.
5. **Session version notice:** Agent Builder and things built with it identify
   their name, version, last-update date, and whether they are current against
   the remote or behind it at the beginning of each session.

## Approved smallest outcome and evidence

- One concise pre-Build proposal shows the direct change and estimated additions,
  removals, net change, and net percentage change against a named baseline for each
  category and overall. Code rows distinguish Python, JavaScript/TypeScript, shell,
  or other actual implementation types, with test code shown separately by language.
  Skill instructions are implementation; guides, READMEs, and governance prose are
  documentation. Miscellaneous rows name their contents: configuration, dependency
  manifests/lockfiles, images, or other assets; no unexplained "misc" total. Assign
  each file once and identify generated/vendor content within its category.
  Report binary changes in files/bytes, not fictional line counts; use N/A for a
  percentage with no existing baseline. Show gross additions and removals even when
  net change is near zero, so rewrites do not conceal their size. Useful cleanup
  is a positive outcome when required behavior is preserved. Include relevant
  tests and what failure each detects, plus flagged-for-later items. Review uses
  the same breakdown for actual changes; material growth during Build requires
  revisiting scope before adding the extras.
- A simple correction stays small and stops after its agreed evidence passes.
  Necessary failure-path, security, installation, and compatibility tests qualify
  when they protect supported behavior. A formatting or wording assertion without
  that connection does not. No blanket test-to-code ratio substitutes for judgment.
- Present deferrals together at the planning checkpoint, recommending that they
  stay deferred. Promote an item only when the author chooses it; do not repeat
  unchanged optional questions throughout execution.
- A fresh checkout retains enough concise shared state and rationale for a colleague
  to understand the current outcome and resume safely. Local scratch discussion,
  draft plans, and raw review output do not accumulate in the committed tree.
  Judge documents by purpose, not extension: a skill's Markdown can be the product.
- At session start, show the actual version in use and its update date, plus a
  verified remote comparison. Exercise current, behind, locally modified, and
  unavailable-remote cases. Missing evidence must yield an explicit unknown status,
  not a claim of being current. Distinguish a generated tool's own version from
  the Agent Builder template version that originally created it.

## Boundaries still to settle

Plan must choose the counting baseline, estimate tolerance and enforcement mechanism,
the minimal committed record set and treatment of existing records, and the version
and date authority. Latest accepted release and remote branch tip are distinct;
recommend reporting both when relevant rather than calling unreleased code a release.
Existing generated projects need an explicit upgrade path; reporting version status
does not authorize automatic updates. No history rewrite or external publication is
requested here. Additional scope requires a separate author decision.

## Source grounding

Checked 2026-10-21: GitHub describes a [README](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
as information needed to get started, [Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)
as a place to plan/discuss/track work, and [releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
as tagged software iterations. The proposed local/shared split is our design judgment;
GitHub does not prescribe excluding all Markdown or require our governance format.
