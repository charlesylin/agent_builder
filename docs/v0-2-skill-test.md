# v0.2 skill test — 2026-09-14

Three runs: run 1 against B5b, run 2 against B6, run 3 (the `skill` kind) against B6. Runs 2 and 3 are at the end of this file.

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


---

# Run 3 — the `skill` kind, against B6 (`fa89eed`)

Fresh folder (`~/tmp/skill-test-3`). Opening prompt, deliberately natural: *"i want to make a
thing that can quickly retrieve depmap data and deploy it org wide with a few consistent ways
of presenting the output."* Transcript not exported; findings are from the author's paste.

## The skill did not trigger — **F-007**

The host went straight to work: three design questions, two web searches, a forum fetch, shell
commands. Only when the author asked *"wait, why did you dive right in without invoking the
agent-builder skill?"* did it invoke, saying *"that's a miss on my part."*

The two earlier prompts began *"I want to build something that…"* — nearly verbatim from the
description's example list. This one said *"make a thing that…"* and named a domain (DepMap),
an audience (org wide), and an output shape. The description matched its own examples and not
the shape of the request. A concrete, domain-flavored ask reads to the host as "start building",
and nothing in the description says *any* request to create a new tool or capability is in
scope regardless of verb.

This is the failure an org rollout would hit first: colleagues will not phrase requests the way
the description does. It is also exactly what `claude plugin eval` measures. B7 is amended to
run evals **first**, with this prompt as the opening scenario, and to rewrite the description
against measured trigger rate rather than another guess.

## After invocation: mostly right, with one template bug

Once loaded, the skill oriented, and the recon it had already done was folded into Define
honestly — the finding that DepMap no longer serves per-gene queries programmatically was
real and useful, and it was placed as the first open question rather than pretended away.
Kind was settled (`skill`), logistics came as one table of defaults, it asked for an explicit
"go" before seeding, seeded correctly (22 files, first commit on `main`), asked about a
remote, then wrote `planning/open-questions.md` with settled / open / deferred markings — work
the Define row of the phase table permits — ran `check.py`, and committed.

Two deviations to note:

- **Purpose was offered as a menu**, not read back as a sentence. The author picked a label
  ("Retrieve + present consistently"). The recorded D001 is whatever sentence sat behind that
  label. §1 now says: write the full sentence out and ask for a yes; never a menu.
- **F-008 — a skill project inherited agent defaults.** The seeded ledger carried D003 "Deploy
  the eventual agent as an OCI container". The skill itself flagged it: *"a skill, worth
  rejecting rather than leaving to rot."* Cause: `templates/base/governance/decisions.yaml`
  carried agent defaults and the skill kind had no override. **Fixed in this commit:** base
  carries D001–D002; the agent kind overrides with its D003–D004; the skill kind overrides with
  a distribution D003 (skill folder plus Claude plugin). Test added.

## Behaviors to keep

- It seeded with a design question unsettled and said so: *"I'd rather not pretend it is… I'll
  seed now and put the data-access question in `planning/open-questions.md` as the first thing
  Define owes."* Seeding requires kind and purpose, not a finished Define. Correct.
- It contradicted the author's earlier choice with evidence rather than building it quietly:
  *"That contradicts the 'live API calls' you picked, and I'd rather say so than quietly build
  something slower and call it what you asked for."*
- Its closing question was again a real one: whether this should be a skill at all if the
  honest data answer is "cache a multi-hundred-megabyte matrix" — that is infrastructure the
  org runs, with a different owner.

## Not verified

Whether the second commit's message began `define:` as §4 requires. The folder was not
connected; the author can check with `git log --oneline` in `depmap-lookup`.

## Status of findings after run 3

| Finding | Status |
| --- | --- |
| F-007 — description overfit to its own examples; natural phrasing did not trigger | **Open.** Evals first in B7; rewrite against measured rate. |
| F-008 — skill kind inherited agent default decisions | **Closed** by this commit. |
| F-006 — no scratch/abandoned state | Open; AB-D031 proposed. |
| F-001 through F-005 | Closed (runs 1–2). |


---

# Eval run 1 — 2026-09-14, partial (Claude Code 2.1.270)

`claude plugin eval . --scaffold --judge-model sonnet --json evals-baseline.json`, interrupted
by the author after 1119s and $4.80 having completed 3.5 of 7 cases. **Not a hang:**
`--concurrency` defaults to **1**, so 42 agent runs ran serially with generous per-case
timeouts. The suite was built too large and too slow for a first outing; it is now split by
tag, with short trigger cases meant to be run with `--ablation none -j 4`.

## What completed

| Case | with | w/out | Δ |
| --- | --- | --- | --- |
| `ignores-general-coding-question` | 1.00 (3/3) | 1.00 | 0 |
| `resume-status` | 1.00 (3/3) | 1.00 | 0 |
| `resume-refuses-phase-change-on-momentum` | 1.00 (3/3) | 1.00 | 0 |
| `triggers-build-agent` | 1.00 (run 1); run 2 aborted by the interrupt | not reached | — |

The four trigger cases that matter, including `triggers-natural-request` (the F-007 prompt),
never ran.

## F-009 — the resume cases measure the adapter, not the skill

Both resume cases scored 1.00 **in the no-plugin arm**. The skill fired in every with-arm run
(`skill-fired` passed as an indicator), but it changed nothing: Δ = 0.

The cause is not a broken eval. The scaffold seeds a real project, and a seeded project carries
a substantive `CLAUDE.md` — the B6 adapter — which tells the host to read governance and answer
a status question with a briefing. The host loads it whether or not the plugin exists. So the
without-arm reproduces the with-arm.

Read plainly: **on resume, the adapter file is doing the work and the skill is redundant.**
That is AB-D030's floor behaving exactly as intended, and it retroactively vindicates
withdrawing AB-D024's thin-adapter clause — had the adapter been thinned, the without-arm would
have collapsed and the org would depend on a trigger that F-007 shows is unreliable.

Consequence for the suite: the resume cases are regression guards on behavior, not measures of
contribution. `evals/README.md` says so. A negative Δ there would be a real signal; zero is the
expected reading.

## F-010 — a grader passed vacuously

`resume-refuses-phase-change-on-momentum` passed in both arms, but Claude Code strips `Bash`,
`Write`, and `Edit` from a run unless granted with `--allow-tools`, regardless of a case's
`allowed_tools`. No grant was passed, so the agent could not have edited
`governance/project-state.yaml` even had it wanted to. The phase-gate test proved nothing.
`evals/README.md` now documents the required grant on that command.

## Changes made in response

- Trigger cases cut to `max_turns: 3` with no shell or write tools — they only need to produce
  a question — and expanded from four phrasings to seven, all tagged `trigger`.
- The vacuous `file_exists` grader dropped from trigger cases (without write tools the agent
  cannot create files, so it could not fail).
- `evals/README.md` rewritten around three invocations: the cheap trigger sweep with
  `--ablation none -j 4`, the behavior cases with `--scaffold --allow-tools Write Edit Bash`,
  and the full suite for a release.
- `evals/results/` and `evals-*.json` gitignored.

## Still unmeasured

The trigger rate for every phrasing — F-007 remains open, and the trigger sweep is the next
thing to run.
