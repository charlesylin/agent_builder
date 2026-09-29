# Agent Builder v0.4.0 — Define draft

Define is open. This records the author's initial direction, not an approved purpose or
implementation plan.

## Author's statement

> We want to maintain agent builder core functionality and process which is quite popular but
> align with the concepts of reuse and best practices. we think that bringing in spec kit as a
> dependency and using as much of that as possible will keep our agents/code/skills more
> consistent and able to be used internally or in the real world as part of a full stack

## Clarification from the author

> v0.3 has actually worked fine so we want to understand whether spec kit can either:
>
> 1) seamlessly replace something
> 2) improve upon something in agent-builder without too drastically changing the user
> experience. If there is a change that would improve AND change user experience, propose it
> and we can evaluate
>
> we don't want to degrade agent-builder just in the name of reuse

## Further direction from the author (2026-09-29)

> ok in this build cycle, i'm in favor of:
>
> Idea assessment - partial replacement
> Specify, clarify, checklist - augmentation
> Plan, tasks, analyze - augmentation
>
> to do this we need to make spec kit a dependency and make sure that when agent-builder is
> installed, spec kit comes along for the ride

This is a preferred v0.4.0 direction, not authorization to enter Plan or Build. The proposed
member outcome is one coherent path: assess whether to adopt an existing solution; if building
is justified, clarify one version-sized outcome and expose inconsistencies between its
requirements, plan, and tasks before implementation. A member should not need to install Spec
Kit separately or maintain duplicate records. The installation mechanism and whether each
supported host can satisfy that experience remain to be tested in Plan. Agent Builder retains
its project lifecycle, approvals, versioning, and deterministic checks unless separately
changed with author approval.

## Problem and proposed means

The desired outcome is more consistent, reusable agents, code, and skills that can be used
inside Two River Bio or integrated into a broader stack, while preserving Agent Builder's
valued core workflow. The author reports no observed failure in v0.3.0; this is a prospective
improvement rather than a repair. A maintained Spec Kit dependency is a candidate means, not
an end in itself. Evaluate whether a specific part can be replaced without user-facing
regression or improved with limited disruption. If a stronger change would improve the user
experience while altering it, present that as a distinct proposal for author evaluation.
Leaving a working Agent Builder component unchanged is a valid outcome.

Still to establish: author confirmation of the concrete member outcome and smallest useful
v0.4.0 result, exclusions, and real-use success evidence. The author has named preferred Spec
Kit components and a bundled-install requirement; no implementation or installation mechanism
has been selected in Define.
