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


---

# Eval run 2 — trigger sweep, 2026-09-14 (Claude Code 2.1.270)

`claude plugin eval . --tag trigger --tag negative --ablation none -j 4 --judge-model sonnet`
— 8 cases, 231s, $3.92 list-price estimate (subscription usage, not billed).

## F-011 — the turn cap was too low, and contaminated the run

Five of eight cases reported `Reached maximum number of turns (3)`. `max_turns: 3` cannot hold
the sequence `SKILL.md` §0 prescribes: look at the directory, call `Skill`, then reply. Runs
that fired the skill and were cut off before answering scored 0 exactly like runs that never
fired. Raised to 8 for trigger cases and 6 for the negative case. **Read the `turns` column
before believing a low score.** Numbers below are `skill-fired` per run, which survives the
contamination where the run completed.

## Trigger rate by phrasing

| Prompt shape | skill-fired | Note |
| --- | --- | --- |
| "I want to **build something that** finds secondhand lab equipment…" | **3/3** | control; clean |
| "**starting a new project** today — a CLI… what's the right way to set it up?" | **3/3** | clean |
| "can you help me **make a skill** that turns my rough notes…" | **3/3** | 1 run capped after firing |
| "i want to **make a thing** that can quickly retrieve depmap data…" | **1/3** | F-007 prompt; 2 clean non-fires |
| "i keep manually reformatting… **can we automate that?**" | **0/3** | 2 clean non-fires |
| "**help me build** a little service that watches our S3 bucket…" | **0/3** | 1 clean non-fire, 2 capped |
| "we need an **internal tool** that summarizes… **where do I start?**" | **0/3** | 3 clean non-fires |

**10 of 21 — 48%.** `ignores-general-coding-question` scored 1.00 with the skill not firing:
the widened description is not greedy.

## What the pattern says

It is not vocabulary. "Help me **build** a little service" contains the verb and never fired;
"starting a new project… what's the right way to set it up" contains no build verb and fired
every time.

The discriminator is **how much the request already specifies**. An abstract ask — "something
that finds lab equipment", "how should I set this up" — leaves nothing to code, so the skill
wins. A concrete ask — "a service that watches our S3 bucket and kicks off the pipeline" —
gives the host enough to start, and starting is its default.

This is the hypothesis raised after manual run 3, now measured. Its uncomfortable implication
for a rollout: the colleagues most likely to get a bad first experience are the ones who know
exactly what they want, which is not the population a governance tool can afford to lose.

Whether a description rewrite can beat a host's default on concrete requests is the open
question. B7b tests it: re-baseline with the corrected turn cap, rewrite the description to
lead with the shape of the *situation* (a new thing is being created, nothing exists yet)
rather than a list of verbs, re-run the identical command, and keep the better number. If the
concrete phrasings stay near zero after a fair attempt, the honest answer is that the empty
folder needs a second entry point that does not depend on triggering — the counterpart to the
adapter file that already covers every existing project (see F-009).

## Status of findings

| Finding | Status |
| --- | --- |
| F-007 — description overfit | **Measured at 48%.** Open; B7b. |
| F-011 — eval turn cap too low | Closed 2026-09-14. |
| F-009, F-010 | See eval run 1. |


---

# B7c — the offer hook (2026-09-14)

AB-D032. F-007 is answered by a hook rather than by a wider description.

`hooks/agent_builder_offer.py` is a `UserPromptSubmit` hook: Claude Code runs it before every
prompt and adds anything it returns in `additionalContext` to the model's context. Hooks cannot
ask a person anything, so this one asks *Claude* to make the offer, and Claude asks.

## Why a hook beats a better description

A description competes for the model's attention against a request the host already knows how
to start on — that is the measured 0/3 on concrete asks. A hook does not compete: it runs
before the model sees the prompt. Its matcher is a pure function over text, so it is tuned
offline, in unit tests, with no model calls and no cost. And the error costs invert: a false
positive is one question the person declines, where a false negative is silent and the
colleague never learns the skill exists.

## Behavior

Silent unless all three hold: the prompt matches a create-something pattern; the working
directory is not already a seeded project (those carry an adapter that points at the skill);
and the session has not been muted. Always exits 0 — a broken hook must never break a prompt.
Muting is a marker file keyed by `session_id` under the temp directory, written by Claude when
the person declines. 17 ms per silent invocation.

## Measured

| Check | Result |
| --- | --- |
| The seven eval phrasings | 7/7 matched, including the three the description scored 0/3 on |
| Seven counter-examples (fix, explain, refactor, rename, summarize, run tests, a Python question) | 7/7 silent |
| "why does the build script create a stale agent?" | silent — negatives win over positives |
| Inside a seeded project | silent |
| After `--mute <session>` | silent for that session, offers in the next |
| Empty, malformed, non-object, oversized input | exit 0, no output |

Nineteen tests in `tests/test_hook.py`; 40 tests total, green on 3.9 and 3.10.

## Consequences recorded

The plugin now executes a script on every prompt in Claude Code. `docs/INSTALL.md` has a
section for whoever reviews the plugin: what it reads, what it writes, that it makes no network
calls, and how to disable it while keeping the skill. Hooks are Claude Code only — Codex relies
on `$agent-builder` and training (AB-D028).

`SKILL.md` §0 now states that deliberate invocation, a description match, and an accepted hook
offer are all normal entry points, and that a decline is not to be revisited that session.

## F-012 — `--plugin-dir` does not load plugin hooks

The first live attempt, 2026-09-14, showed no offer: a concrete S3-watcher prompt in an empty
folder produced a design conversation, exactly as before the hook existed. The hook was never
invoked. **Plugin hooks run only when the plugin is installed**; `--plugin-dir` loads skills,
commands and agents but not hooks — a defensible line, since a hook executes on every prompt
and `--plugin-dir` points at an unvetted directory.

Consequences: every earlier `--plugin-dir` test measured the skill description alone, which is
what those runs were for, so nothing is invalidated. But the hook cannot be tested that way,
and `docs/INSTALL.md` and `docs/AUTHORING.md` now say so. Two diagnostics worth knowing:
`/hooks` lists every registered hook and its source file, and `claude --debug` records which
hooks matched, their exit codes, and their output.

Whether the org-wide path is affected: no. Installed-by-default and available-for-install both
install the plugin properly, so hooks run there. The limitation is specific to local
development.

## The offer works — 2026-09-14, third live attempt

With the fixed hook registered in the test folder, the S3 prompt produced the offer. The trace
records the payload schema Claude Code 2.1.270 actually sends:

```
keys=['cwd', 'hook_event_name', 'permission_mode', 'prompt', 'prompt_id',
      'scratchpad_dir', 'session_id', 'transcript_path']
```

The typed text is under **`prompt`**. There is no `user_prompt` and no `user_prompt_raw`. A
test now asserts the hook handles that exact key set.

## F-014 — the offer repeated after being declined

The same trace showed a second offer fourteen seconds later. The person had answered *"build
directly without agent-builder"* — which is itself a create-something sentence, so it matched,
and nothing had muted the session because muting depended on Claude choosing to run a command
it did not run.

The docstring already claimed "offers at most once per session"; the code implemented "offers
until muted". The code now matches the claim: **the marker is written when the offer is made**,
so a session is asked once regardless of what the person says, whether they accept, decline, or
ignore it. `--mute` remains for Claude to call explicitly and is idempotent. The offer text no
longer asks Claude to run anything.

Verified: offer, then silent for two further create-shaped prompts in the same session, then
offered again in a new session.

## Verified through the installed plugin — 2026-09-14

Project-settings diagnostic removed; only `enabledPlugins` remained in the test folder, so the
plugin was the sole source of the hook. Transcript:

```
❯ help me build a little service that watches our S3 bucket for new FASTQs and kicks off the pipeline

Want to use the agent-builder skill to scaffold this, or should I just build it directly?

✻ Worked for 1s

❯ build it directly without using the agent-builder skill

  Read 1 file, listed 1 directory, ran 1 shell command
  [proceeds with the actual task]
```

Every part of the design held:

- the offer is one sentence, with no work started while asking — "Worked for 1s";
- declining drops it and the actual request is served;
- the decline sentence itself matches the create pattern, and produced **no second offer**
  (F-014);
- the prompt is the one that scored 0/3 for the description alone in eval run 2.

**B7c is done.** The offer works through the real distribution path.

## What this step cost, and why

Three live attempts were needed. The first could not have worked (`--plugin-dir` does not load
hooks, F-012). The second ran the hook against a key the payload never contained (F-013). The
third offered twice (F-014). Each time the unit tests were green, because each test constructed
its payload from the same misunderstanding the code held.

The lesson is narrow and worth keeping: unit tests confirm the author's model of an external
contract, they do not check it. The thing that found all three was making the hook report what
it actually received — `AGENTS_BUILDER_HOOK_LOG`, added for an unrelated reason, then used to
pin the schema in a test. Anything this repository builds against an interface it does not own
should be able to say what it saw. Pending an installed-plugin test.


---

# The accepted offer, and F-015 — 2026-09-14

Same prompt, answered "yes" to the offer. The skill loaded, oriented, and asked the kind
question with three options tailored to an S3 watcher rather than the four abstract kinds:

1. *Deterministic plumbing* — "maps to kind `project`, which the seeder doesn't support yet —
   I'd tell you the options before seeding anything."
2. *Model in the loop* — maps to `agent`.
3. *Mostly plumbing, one judgment step* — "Composite — takes its primary kind, which I'd want
   to settle with you."

## The adaptive phrasing is correct, not drift

§1 says "Ask **enough of these** to settle it, **in plain words**", which licenses exactly
this. Across the runs so far it has offered two kinds, three, or four depending on which are
live possibilities for the request. It also honored the two harder clauses: it surfaced the
composite case, and it named an unsupported kind before the person could pick it rather than
steering them quietly to `agent`.

The cost is that two colleagues describing similar work may see differently framed questions.
For a tool whose value is consistency that is worth watching, but the artifact is what carries
consistency — the ledger, the phases, the closeout are identical — and the question is the part
that should adapt. Left as is.

## F-015 — real requests keep landing on the `project` kind

The most natural request in the whole test series — a service that watches a bucket and
launches a pipeline, no model anywhere in it — is a `project`, and `project` is not shipped.
The skill handled it honestly, but the only paths available are to seed an `agent` (which
brings `contracts/`, `deployment/`, and an agent-handoff schema the project has no use for —
the F-008 failure in a new guise) or to seed nothing.

AB-D023 deferred `mcp` and `project` until "a real project in the organization requests one,
with that project's friction as evidence". This is that evidence. Recorded, not acted on:
adding a kind is scope, v0.2 is at its release step, and the sensible place for it is the
first item after the Review that follows.

Not urgent for the org test: a colleague who hits it gets an honest explanation rather than a
wrong scaffold. It becomes urgent the first time someone accepts `agent` for a project that is
not one.


---

# AB-D031 — a project can say it has stopped (2026-09-14)

Confirmed by the author and shipped. `project.status` in `governance/project-state.yaml` is one
of `active`, `paused`, `abandoned`, `archived`, seeded as `active`, validated by `check.py`,
and absent means `active` so projects generated before the field keep validating.

It sits **alongside** the phases, not inside them. The phase records how far the work got; the
status records whether anyone is still doing it. A project abandoned in Define stays in Define.

`SKILL.md` gains a section 6: when someone says a project is a test, scratch, on hold, dead or
done, set the status, add a dated phase-history entry with the reason, run `check.py`, and
commit — rather than shrugging and moving on, which is what happened twice in these tests.
Section 3 leads the briefing with the status when it is not `active`, since a paused project is
not waiting for its next step.

This repository sets its own `status: active`.

Closes F-006, which the skill raised about itself during run 2: *"the skill may need somewhere
in-repo to record 'this is scratch' — or Define's closeout may need to run even when the answer
is 'never mind.'"*


---

# B8 — dogfood and release (2026-09-14)

`seed.py --kind skill` with Agent Builder's own name, purpose, owner, and hosts produced a
23-file project that validates and whose own tests pass. Compared against the real
`skills/agent-builder/` and the repository around it:

## F-016 — the builder has outgrown its own template, in ways worth knowing

| Seeded | Real | Reading |
| --- | --- | --- |
| single-skill plugin: `SKILL.md` and `.claude-plugin/plugin.json` at the project root | plugin root holds `skills/agent-builder/`, `hooks/`, `evals/`; `SKILL.md` one level down | Both valid layouts. The real one exists because the plugin carries a hook and may carry more skills. |
| `scripts/README.md`, `references/README.md` placeholders | `seed.py`, `check.py`; three references | Expected — the scaffold is where those start. |
| — | `templates/` (38 files), `principles/`, `scripts/render.py` + stencils | Specific to a skill whose job is seeding other projects. Not template material. |
| `planning/open-questions.md`, `planning/definition.md`… | `docs/v0-2-define.md`, `docs/v0-2-plan.md` | **A real inconsistency.** The builder tells others to plan under `planning/` and plans itself under `docs/`. Recorded for Review; renaming now is churn without a decision. |
| `evals/001-….md` — a prose scenario | `evals/<case>/prompt.md` + `graders/` — `claude plugin eval` | **The template was wrong.** Fixed in this step: the skill kind now seeds a trigger case and a negative case in the format that actually runs. |
| `.agent-builder.json` | none | The builder predates its own manifest. Left out rather than fabricated. |

Running `check.py` against this repository as a skill project fails on the missing single-skill
files, on the phase not being Define, and — pleasingly — on `docs/AUTHORING.md` containing a
literal `{{UPPER_CASE}}` in prose, which the secret-and-token scan flags. All correct behavior
for a checker pointed at something that is not what it was built to check.

**Success signal 5** — "Agent Builder's own skill is produced by its own `skill` template" — is
met in substance: the template produces a valid skill plugin that a person would grow into
this, and reconciling it improved the template. It is not met byte-for-byte, and forcing that
would mean growing the template to carry things no other skill needs. Recorded as such.

## Release

Version `0.2.0` in `plugin.json`, `pyproject.toml`, and `TEMPLATE_VERSION`; `CHANGELOG.md`
cut; tagged `v0.2.0` on the commit that follows. Phase remains Build until the author approves
Review. Review's acceptance test is the opt-in org install and the friction it produces.

## Carried into Review

- F-015 — the `project` kind, twice requested by realistic prompts.
- F-016 — `planning/` versus `docs/` in the builder's own repository.
- Untested: Codex on any path; `SKILL.md` §6 (marking a project paused or abandoned) in a live
  session; the eval trigger sweep with the corrected turn cap.
- The 48% description trigger rate is recorded with a caveat and no longer gates anything.
