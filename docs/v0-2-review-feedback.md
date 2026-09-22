# v0.2 Review feedback — Sean, 2026-09-14

Relayed by the author from Sean's own agent-generated feedback on his v0.1-seeded project.
Much of what Sean's agent listed was addressed by the v0.2 redesign; the author extracted the
three points that were not. They are recorded here verbatim in substance, with the analysis
and the proposals they led to. Decisions are `proposed` until the author confirms them.

Sean is the intended first user: new to agent building, on Windows, working without the author
present. Feedback from him counts more than feedback from anyone who already knows what a
phase is.

---

## 1. "The value of the thing is only as good as the author's ability to articulate the value proposition."

Proposed fix, from the author: Define should ask, explicitly and early — *what problem are you
solving? how is it solved today? what is the value if you solve it? who are you solving it
for?* — and the answers should be stored in the design.

### What Define does today

Kind → one-sentence purpose → logistics → seed. The purpose sentence is the only articulation
demanded before files exist. `planning/open-questions.md` then asks twelve questions, of which
Q1–Q3 touch purpose and scope, but nothing asks *what is wrong today* or *what it is worth to
fix it*. A person can produce a fluent purpose sentence for a thing that solves no problem
anyone has — and the skill's own runs show it will happily draft one for them.

### Proposal — AB-D033: problem framing comes before the purpose, and the purpose is derived from it

- Define opens with the four questions, one turn each. They are the decisions; logistics stay
  batched.
- The skill drafts the purpose sentence **from the four answers** and reads it back. Today it
  drafts from the opening request; the difference is that a purpose derived from a stated
  problem and value cannot be fluent about nothing.
- The answers are seeded into a new base file, `planning/definition.md`, under four headings,
  and summarized in D001's rationale, so the ledger's first entry says *why*, not just *what*.
- `check.py --leaving define` (new) fails if any of the four is still a placeholder. That is
  the CI-bindable version of "you cannot leave Define without a problem statement", and it is
  the first check that binds a *phase transition* rather than file structure.

Cost: the pre-seed conversation gains four turns. Sean's point is that those are the four turns
that matter most, and the runs so far show the skill spending turns on things that matter less.

## 2. "The agent-builder gives lots of suggestions… users are saying yes to everything and this is creating bloat. Simpler is definitely better."

The author is right that this is intentional at its source: the decision protocol asks for
recommendations, and the closeout asks *what should you be asking that you are not?* Both are
there to explore the space. The failure is downstream — every exploration becomes a
commitment, because the only response the person is offered is yes.

The v0.1 evidence already contains this failure in miniature: D003 and D004 are template
defaults seeded as `proposed`, and the skill itself called one of them "worth rejecting rather
than leaving to rot." Proposals that nobody rejects become scope by inertia.

### Proposal — AB-D034: adopt "build only what you need" as a principle

rewrites.bio's 4.2 was never carried into `principles/`. Its core line is exact for this
problem: *"A rewrite that does four things correctly is more valuable than one that claims
fifteen and does twelve right. Scope can expand as the project matures; it cannot easily
contract once users depend on it."* Add it as `principles/11-build-only-what-you-need.md`, so
it renders into `SKILL.md`, every adapter, and every seeded operating agreement — the same
mechanism that put Nokkvi's law everywhere.

`planning/definition.md` gains two sections the principle needs to bite: **Smallest version
that delivers the value** and **Not in the first version**. The skill is told to test every
proposal against them before making it.

### Proposal — AB-D035: suggestions are not scope; there is a parking lot, and proposals expire

Three deterministic changes so that saying yes to everything cannot create bloat:

1. Seed `planning/later.md`. Anything the skill suggests that the author did not ask for —
   including every closeout question — is written there by default, not into scope. Moving an
   item out of `later.md` requires the author to ask for it in their own words, and produces a
   decision.
2. Proposed decisions **expire at phase close.** `check.py --leaving <phase>` lists every
   decision still `proposed`; each must be confirmed or rejected before the transition. The
   decision protocol keeps its four statuses; nothing new to learn. This kills the D003/D004
   rot mechanically, and it means a phase transition is the moment scope is *closed*, not just
   advanced.
3. The closeout asks **one** "what should you be asking" question, framed as a question and
   not a recommendation, and the skill never converts a closeout question into a decision or a
   task on a "yes". `SKILL.md` §4 says so in words; the parking lot gives the words somewhere to
   point.

## 3. "Novice users click approve on everything. The risk is they don't read what they're clicking."

The author's judgment — fine, but risky — is right. The fix is not to stop asking; it is to
make the consequential answers cost a sentence.

### Proposal — AB-D036: consequential approvals are typed, not clicked

For the purpose sentence, the MVP statement, a phase transition, seeding, creating a remote, and
any grant of send/spend/publish/delete authority: the skill states in one line what a yes
commits the person to, then asks for a typed word or a restatement — never a picker. Pickers
remain for exploratory questions, where a wrong click costs nothing. The phase gate already
works this way ("in words that leave no doubt"), and it is the one rule that held in every run.

One idea recorded but not proposed as a decision: if the author accepts several defaults in a
row, the skill could say so and offer a *minimal mode* — stop offering options, do the smallest
version, park everything else. It matches "simpler is better" and it is cheap; it also risks
feeling like being scolded. Worth a try in Review, not a rule yet.

---

## What these have in common

Every mechanism v0.2 built — the phases, the ledger, the offer, the briefing — is about
*opening* a project well. None of it *closes* anything: no proposal expires, no suggestion has
a place to go other than scope, no approval costs more than a click. Sean's three points are
one point. The four proposals above add the closing half: a problem statement you cannot skip,
a principle against accumulation, a parking lot with an expiry, and a typed yes where yes is
expensive.

## Status

Recorded 2026-09-14. The author entered Review the same day and confirmed AB-D033, AB-D034,
AB-D035, and AB-D036 as written above, added AB-D037 (Nokkvi's law turns outward when the person
is frustrated or confused), and authorized AB-D038: incorporate the feedback as release 0.2.1
during Review, under v0.1's precedent for author-approved refinements (AB-D015, AB-D016).
0.2.1 is what Review continues against; the `CHANGELOG.md` entry lists what changed. Whether
the four questions, the parking lot, and typed approvals actually change what novices build
is the thing Review still has to observe — Sean is the first tester.

## Review findings after 0.2.1

### F-017 — the desktop app is a second, separate install, and the docs misdescribe it

2026-09-15. The author already had the plugin installed in Claude Code (CLI) from the
Dropbox-path marketplace and tried to get it into the Claude Desktop app. The two do not share
plugin state. The working procedure in the app is **Customize → Plugins → Add → Add
marketplace → GitHub URL**, then **Add** on `agent-builder`. The app then reports "couldn't sync
your plugins just now" and clicking Add again does nothing; **restarting the app** is what
completes the install. The Claude GitHub App was installed on the repository along the way,
which is what the *Sync automatically* toggle needs, but it was not the fix for the toast.

The cost was not the procedure — it was the assistant guiding the author from vendor
documentation that describes a different UI (an "Add from a repository" option that does not
exist, a Code-tab plugin browser that only reads CLI marketplaces), and repeatedly re-checking
the CLI install that was already fine. Two lessons recorded: `docs/INSTALL.md` now describes
the screen, not the docs; and when a colleague reports a UI that differs from documentation,
ask for a screenshot first, not third.

Carried into Review: whether the account-level sync also delivers hooks to Cowork (untested),
and whether a colleague with no CLI install at all gets a clean first run from the app path.

## Extended-use findings — author, 2026-09-22

The author supplied these findings after a week of using Agent Builder across projects. They
are Review evidence, not decisions for the next iteration. Several strengthen principles that
already exist but have proved too weak or too late in the workflow; the distinction matters
because the next Define should solve the observed behavior rather than merely repeat the
current wording more emphatically.

### F-018 — search must be a build-or-adopt gate, not only implementation guidance

Agent Builder already says to search for validated open-source solutions before building
(AB-D003), but the observed behavior does not make that search a required project-level
decision. Before committing to a build, it should determine whether an existing public solution
satisfies the project's requirements. When one does, it should recommend using it and stopping
the project, with the reason recorded, rather than inventing work to justify the scaffold.

Open for the next Define: whether "public" means only open-source software or also hosted,
commercial, standards-based, and other generally available solutions; and what evidence is
enough to conclude that the requirements are satisfied.

### F-019 — every cycle needs its own minimum viable outcome

"Build only what you need" (AB-D034) reduced feature accumulation, but a project's stated
smallest version can still be interpreted as the whole intended product. Agent Builder should
scope each Define → Plan → Build → Review cycle to one useful, testable step rather than
trying to complete the full product in a single cycle. Later capabilities remain visible but
out of the current version.

This is coupled to F-024: the cycle boundary needs a versioned name so "minimum" has a concrete
meaning for the author and the implementation agent.

### F-020 — reuse includes organizational code, and new code should be reusable

The current search principle covers open source, and replaceable boundaries cover coupling,
but neither requires discovery of code the organization already owns. Agent Builder should
ask about—or be configured with—organizational code sources before planning. For Two River Bio,
the named source is <https://github.com/tworiverbio>; it must not be hard-coded into a general
utility.

Two candidate mechanisms were identified, with no decision yet:

1. ask each project author which codebases, organizations, or repository sets should be
   searched; or
2. load user- or organization-level Agent Builder configuration that declares them.

The same principle runs in the other direction: when new code is genuinely needed, prefer
small modules with explicit contracts that can be reused without coupling future projects to
the current implementation.

### F-021 — capability and skill discovery belongs before planning

Agent Builder should know which skills and other approved capabilities are available in the
current environment, or load a configured organizational baseline, before proposing how to
build. The concrete example is Grafify: the organization wants it used to help manage codebase
structure, and wants existing reference repositories checked for prior Grafify structure
before new structure is imposed.

Open for the next Define: whether capability inventory is host discovery, configuration, or a
combination; how optional or unavailable skills are represented; and whether Agent Builder
invokes such skills itself or records them as required capabilities for the generated project.

### F-022 — the neutral `project` kind has real-use support

The author reports that the `project` format works well: it brings the governance workflow
without presupposing that the result is an agent or a skill. Together with F-015, this supplies
the real requesting-project evidence AB-D023 required before adding another kind. It is input
to the next Define, not authorization to implement the kind during Review.

### F-023 — novice recommendations need a technical-quality gate

In observed use, Agent Builder can talk a novice into implementing approaches that an
experienced developer would reject. Before recommending an approach, it should reason about at
least four questions: is this the most efficient route to the current MVP; does an existing or
organizational tool already solve it; is the approach robust enough for the stated use; and is
its scaling path proportionate to realistic demand? The author's example is sideloading a
browser for an agent, which failed all four tests.

This finding is broader than typed approval (AB-D036). Making a novice type approval does not
improve a poor recommendation. The recommendation itself needs an evidence-backed quality
check, with uncertainty and tradeoffs exposed rather than fluently rationalized.

### F-024 — versions should be explicit, useful stepping stones

Agent Builder should use standard versioning conventions and treat important versions as
"good enough" states to deploy, use, and test. During big-picture onboarding it should ask the
author what outcome belongs in the first version—for example, "What do you want to tackle for
v0.1?"—and keep later outcomes outside that cycle.

Open for the next Define: the default versioning convention, how it applies to non-software
projects, and whether each completed Review necessarily produces a release.

### F-025 — the author should help define tests, expected results, and controls

Mechanical smoke and unit testing already appears in plans and builds, but the project author
is not systematically involved in defining what evidence would count as success. Before Build,
Agent Builder should elicit expected outcomes, representative examples, failure cases, and any
available control datasets. Where the work is empirical, prospective hypotheses and positive
and negative controls are first-class acceptance inputs rather than retrospective explanations.

Open for the next Define: which test commitments belong in Define versus Plan, what minimum
evidence every project kind must supply, and how unavailable or sensitive control data is
recorded without weakening security rules.

## Provisional Review classification

These findings do not contradict v0.2's scoped deliverable: an installable skill, deterministic
seeder and checker, generated governance, and tested phase behavior. They show that the next
iteration must improve the quality and boundaries of the technical work that governance
permits. The recommended classification is therefore **inputs to the next Define, not v0.2.1
acceptance blockers**, subject to the author's explicit acceptance decision.

The main themes for that Define are:

1. decide whether to build at all, after public and organizational discovery;
2. define one version-sized MVP and its evidence before planning implementation;
3. use configured repositories and capabilities, including skills, before inventing code;
4. require technically prudent recommendations for novice users; and
5. add the neutral `project` kind now that real-use evidence exists.
