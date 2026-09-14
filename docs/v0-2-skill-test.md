# v0.2 skill test — 2026-09-14

Two runs: run 1 against B5b, run 2 against B6. Run 2 is at the end of this file.

**Tester:** Charles Yang Lin
**Build state:** B5b (`bd44074`), plugin version `0.2.0-dev`
**Host:** Claude Code, `claude --plugin-dir ~/Dropbox/codex/project_agent_builder`
**Transcript:** `docs/evidence/2026-09-14-skill-test-transcript.md` (verbatim; the `SKILL.md`
text embedded in it is the 2026-09-14 rendering and will drift from `principles/`)

Two sessions. Session 1 started in an empty directory and ran the Define conversation through
to a seeded project. Session 2 started fresh in the seeded project with the plugin loaded and
asked only "what's the status here?".

---

## Session 1 — start a new project

### Result: pass

The skill triggered implicitly on *"I want to build something that finds secondhand lab
equipment listings and flags good deals."* No explicit invocation. It then executed the
procedure in order: listed the directory, found neither `.agent-builder.json` nor
`governance/project-state.yaml`, said so in one sentence, and asked the kind question first.

The seeded project was verified independently: 23 files, clean working tree, one commit
`09c2881` on `main`, `.agent-builder.json` carrying `kind: agent` and
`owner: charles@tworiver.bio`, `check.py` reporting valid, and the project's own test suite
passing.

### Behaviors the procedure specified, and got

- Orient before anything else; one sentence about what was found.
- Kind settled before any file was written.
- Purpose drafted, the three things that would change it named, reformulated after author
  input, read back, and held until the author replied "confirmed".
- `seed.py` invoked with the correct flags rather than files written by hand.
- Seeder output reported verbatim.
- Remote creation and push asked about, not assumed.
- Four-section closeout, with `None` used where a section was empty.

### Behaviors that were not specified and are worth keeping

1. **Progressive disclosure worked.** Asked "what are all of the things that you can build?",
   it read `references/kinds.md` on demand instead of answering from the summary in `SKILL.md`.
   It then named `mcp` and `project` as not-yet-supported, which the kind picker had omitted.
   The reference file earned its place; `SKILL.md` stayed short.
2. **It refused a meaningless action.** Told "do a local commit", it checked `git status`,
   found a clean tree, declined to create an empty commit, and explained that the seeder's
   commit already carried every file. Compliance would have been worse than refusal.
3. **A principle became behavior.** Opening Define, it built an authority ladder — read only /
   alert the author / contact sellers / spend — directly from the read, write, send, spend,
   publish, delete levels in `principles/09-security-and-authority.md`, applied to this
   project. The principles are not decorative in practice.

### Deviation to adopt

`SKILL.md` §1 says "One question per turn." The skill asked kind and purpose one at a time,
then batched name, owner, hosts, and destination with proposed defaults and a one-line "all
defaults" accept. The author took the shortcut. Substantive facts deserve their own turn;
logistics do not. The instruction should be rewritten to match what worked.

### Minor

An `AskUserQuestion` was declined by the author in favor of clarifying; the skill recovered by
asking what needed clarifying. No procedural fault.

---

## Session 2 — resume an existing project

### Result: the skill did not trigger; the adapter file carried the work

With the plugin loaded, "what's the status here?" produced no `Skill(agent-builder:agent-builder)`
invocation. The reply opened *"I'll read the governance files first, as the project
instructions require"* — the seeded `CLAUDE.md` — and ran about thirty lines: phase, what
exists, a four-row decisions table, a next step, and a full closeout.

`SKILL.md` §3 specifies **at most three lines, then wait.** That is not what happened, and the
`Skill` tool was never called. The adapter file did the whole job.

### Two findings, in opposite directions

**F-003 — the description does not cover resume.** Its trigger phrases are oriented at
starting work ("build an agent that…", "make a skill for…", "set up a new project"). The only
resume-ish phrase is "what phase are we in". A generic "what's the status here?" in a governed
repository did not match. This is the gap that matters for F-001: repository records carry
enough context, but the skill does not reliably wake up to read them.

**F-004 — the specified resume output was the wrong shape.** The author found the fuller
briefing more useful than three lines, and gave the reason: *"this could be beneficial if I
decide to pick up the development of someone else's agent."* Three lines assumes the reader
already knows the project. Cold pickup of a colleague's work is the case that matters, and
the briefing serves it better. §3 should specify the briefing, not the summary.

### Consequence for B6

B6 as planned — thin the adapters to a pointer — would have removed the only thing that
worked in this session. A resumed project would have had no instruction to read governance, no
phase discipline, and no closeout format, with the skill not reliably firing to supply them.

Separately, AB-D024's stated rationale for thinning was that thin adapters drift less. AB-D020
already made drift structurally impossible: adapters are generated from `principles/` and CI
fails when a generated copy is edited. The premise no longer supports the conclusion.

Recorded as AB-D030, which supersedes AB-D024's thin-adapter clause. AB-D024's version pin and
`check.py --since` upgrade path stand.

---

## Status of the v0.1 findings

| Finding | Status |
| --- | --- |
| F-001 — resume needs manual coaching | **Partly closed.** A cold session recovers phase, decisions, and next step from repository records with no resume prompt. It does so through the adapter file, not the skill; the skill's own resume path is untested because it never fired. |
| F-002 — host Python prerequisite | **Closed for this path.** `seed.py` and `check.py` ran on the author's machine with no install step and no version complaint. |

## Not yet tested

- The `skill` kind end to end through the skill (only `agent` was exercised).
- Codex, on any path.
- The counter-case: a nearby request the skill should ignore.
- `claude plugin eval`, which would measure trigger rate rather than demonstrate it once.


---

# Run 2 — against B6 (`fa89eed`)

**Transcript:** `docs/evidence/2026-09-14-skill-test-run2-transcript.md`. Fresh folder
(`~/tmp/skill-test-2`), same two sessions, same opening prompt.

## Session 1 — start: pass, and the §1 revision behaved as written

The `Skill` tool was the very first call, before any directory listing. The kind picker this
time offered three options including `mcp`, labelled "not yet supported by this builder — I'd
tell you and we'd fall back to agent", which is the §1 table followed literally. Purpose went
draft → two clarifying dimensions → reformulation → read-back → "yes". Logistics arrived as one
table of four defaults, accepted in one line — the revised §1 exactly. Seeder ran with correct
flags; output verbatim; remote asked about, not assumed.

The seeded project was verified independently: one commit on `main`, clean tree,
`source_commit` = `fa89eed…`, `check.py` valid, adapter opens with the skill-invocation line.

## Session 2 — resume: **F-003 closed, F-004 closed**

"what's the current status?" → the host listed the directory, read the adapter, said *"This is
an agent-builder project — invoking the skill to brief properly"*, and called
`Skill(agent-builder:agent-builder)`. The briefing matched §3 point for point: purpose in the
ledger's words; phase, status, and *how long* ("roughly an hour ago"); what exists and what
Define still owes (`planning/definition.md` missing, `open-questions.md` untouched); the four
decisions in a table; a proposed next step with the reason for that one first; the closeout;
*"I've made no changes and moved no phase."*

Whether the description or the adapter line caused the invocation cannot be separated from
one run. It does not need to be: AB-D030's design is that the adapter is the floor and the
skill is the ceiling, and both layers did their job.

Two unplanned behaviors worth recording:

- It noticed `../session-transcript.md` in the parent folder, read it, learned from it that the
  project had been declared a test, and **reconciled that against the ledger** rather than
  believing either: *"The repo itself doesn't record that."* It then made the next step
  conditional on which was true. That is §3's checkpoint rule applied to a file it was never
  told about.
- Its closing question was a product finding, not a project one — see F-006.

## New findings

**F-005 — summarized principles had no names.** Asked *"confirm to me what Nokkvi's law is"*,
the session replied it had never heard of it and declined to confirm something unknown right
after being told the preceding minutes were a test. That was the right answer to the wrong
situation: `SKILL.md` and the seeded `CLAUDE.md` rendered every principle as an anonymous
paragraph — `{{principle:…|short}}` without `|title` — so the model had the rule and not its
name. Only the full operating agreement carried the heading. **Fixed in this commit:** every
summarized principle is now prefixed `**Title.**` in `SKILL.md`, the three adapters, and the
root `AGENTS.md`, with a test. The skepticism itself is behavior to keep.

**F-006 — a project cannot say it is scratch.** The session's own words: *"the skill may need
somewhere in-repo to record 'this is scratch' — or Define's closeout may need to run even when
the answer is 'never mind.'"* The phase model has no terminal state. An abandoned or test
project is indistinguishable in its ledger from a live one awaiting Define. In an organization
that will start many projects and finish fewer, that gap matters. Recorded as AB-D031,
`proposed`: it changes the project-state contract and needs the author.

## Status of findings after run 2

| Finding | Status |
| --- | --- |
| F-001 — resume needs manual coaching | **Closed.** A cold session with only the skill trigger phrase recovered the full picture and invoked the skill unprompted. |
| F-002 — host Python prerequisite | Closed (run 1). |
| F-003 — description did not cover resume | **Closed** by B6. |
| F-004 — three-line resume was the wrong shape | **Closed** by B6. |
| F-005 — summarized principles unnamed | **Closed** by this commit. |
| F-006 — no scratch/abandoned state | Open; AB-D031 proposed. |

## Still not tested

The `skill` kind through the skill; Codex; the counter-case; `claude plugin eval`.
