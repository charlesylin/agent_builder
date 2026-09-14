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

Recorded 2026-09-14 while the project is still formally in Build (v0.2.0 tagged, Review not
yet approved). These are Review inputs. Implementing them is Build work for a 0.2.x or 0.3;
v0.1's precedent (AB-D015, AB-D016) allows author-approved instruction refinements during
Review.
