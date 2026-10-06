# Erico: test Agent Builder v0.4.0 in Codex

Agent Builder v0.4.0 is a **Review candidate**, not an accepted or tagged release. This
test uses a real skill idea to check whether the Spec Kit integration improves the
decision and planning process without adding a second workflow. The integration is
exercised mainly in **Plan**, before you write the skill itself.

You need Git, Python 3.9 or newer, and Bash for the bundled project helpers; you do
**not** need to install Spec Kit's Python CLI.

## 1. Make sure Codex is using this version

The Claude Code organization plugin does not prove which skill Codex loaded. Codex
needs its own Agent Builder skill folder. Codex can read user-level skills from
`$HOME/.agents/skills` and supports symlinked skill folders; see the
[official Codex skills guide](https://learn.chatgpt.com/docs/build-skills).

In a terminal, clone the [Agent Builder repository](https://github.com/charlesylin/agent_builder)
into a parent folder where `agent_builder` does not already exist:

```sh
git clone https://github.com/charlesylin/agent_builder.git
cd agent_builder
git switch main
git pull --ff-only origin main
git rev-parse HEAD
python3 scripts/refresh_spec_kit.py --check
```

If you already have a checkout, skip `git clone`; run `git switch main`,
`git pull --ff-only origin main`, and the two checks from that checkout. Record the
full `git rev-parse HEAD` value. The integration must include Build commit `efe22f9`
and the Build-to-Review checkpoint `a110eb3`; a fresh `main` checkout does.
The bundle check should report Spec Kit `1.1.0` at
`f1d3a4f8337ebbd3ae22760a9c12e3352b93a175`.

If you do **not** already have a user-level Agent Builder skill, run this from the
checkout root:

```sh
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/skills/agent-builder" "$HOME/.agents/skills/agent-builder"
```

If that destination already exists, inspect it before changing anything. Update an
old checkout or deliberately replace an old copy; do not leave multiple skills named
`agent-builder` and assume Codex chose the new one. Start a fresh Codex chat (restart
Codex if the update is not detected).

Before creating a project, send Codex this prompt:

> Use `$agent-builder`. Before creating files, report the absolute path of the
> `SKILL.md` you loaded. From that same skill folder, report `TEMPLATE_VERSION` in
> `scripts/seed.py` and the upstream version and commit in
> `vendor/spec-kit/manifest.json`. Stop if the version is not Agent Builder `0.4.0`
> with Spec Kit `1.1.0` at
> `f1d3a4f8337ebbd3ae22760a9c12e3352b93a175`.

Save its answer. The loaded path must point to the checkout you just updated; a
Claude plugin version or an older similarly named skill is not enough.

## 2. Build your skill and exercise the integration

Open Codex in an empty parent folder. Tell `$agent-builder` about a **real skill you
want to make** and follow its Define questions. Let it seed a new `skill` project with
the `codex` adapter; do not pre-create the destination folder. Define one useful first
version (often your skill's `v0.1.0`) and what is deliberately out of scope. That
deliverable version is separate from Agent Builder's `0.4.0` template version.

After seeding, inspect the new project's `.agent-builder.json`: it should say
`"template_version": "0.4.0"`, `"kind": "skill"`, and list `codex` under
`coding_agent_adapters`. Its `source_commit`, if populated, should match the checkout
SHA you recorded. `.specify/spec-kit-provenance.json` should show the Spec Kit pin above.
Ask Codex to run the installed Agent Builder `scripts/check.py` against the new project
and report the result.

Enter **Plan only after you explicitly approve that phase change**. In early Plan,
watch for these behaviors:

1. Agent Builder checks for existing public solutions before recommending a custom
   skill. It asks about any codebase you want considered. It reads the bundled Codex
   `speckit-assess-research` instructions through Agent Builder—not as a second skill
   you install or invoke—and writes
   `.specify/assessments/<slug>/research.md` with prior art, evidence against the idea,
   sources, and an honest confidence rating.
2. `planning/solution-evaluation.md` links to that research and compares candidate fit,
   real use/maintenance, tests/security, license, and setup burden. Claims from the
   public web should have checkable source links. If Codex cannot access or verify
   sources, it should say so rather than inventing evidence; tell us if this happens.
3. Agent Builder recommends **adopt** if something already meets your need. That is a
   successful result: after your typed confirmation it should archive the project in
   Plan, without inventing a skill release. Do not force a build just to reach later
   Spec Kit steps; a separate novel idea can test that path.
4. If you confirm **adapt or build**, Agent Builder should keep the scope to one usable
   version and use the bundled `specify`, `plan`, `tasks`, and `analyze` instructions.
   `clarify` and `checklist` should appear only for a real gap. Look for
   `.specify/feature.json` and one `specs/<feature>/` directory containing `spec.md`,
   `plan.md`, and `tasks.md`. Before entering Build, ask for an analysis of whether
   requirements and tasks agree. If practical, introduce one obvious *temporary*
   mismatch in a draft task, see whether `analyze` catches it, then fix it before
   implementation.

Throughout, Agent Builder should own the Define → Plan → Build → Review phases,
approvals, and project version. It should not ask you to install or run the `specify`
CLI, expose separate `speckit-*` skills, start a parallel lifecycle, or follow an
upstream suggestion to run `implement` or `converge`. If another skill (including
`skill-creator`) takes over governance or Plan, flag that too; using it later for
implementation is a separate question.

## 3. Send us the evidence and your verdict

You do **not** need to finish coding the skill before sending first feedback; reaching
the Plan recommendation and, if building, the analyzed spec/plan/tasks is already
valuable. Please send Charles:

- Your Codex environment (desktop or CLI), the loaded Agent Builder `SKILL.md` path,
  checkout SHA, version-check response, and whether you had to fix a stale install.
- The new skill project's repository URL or path and commit, plus
  `.agent-builder.json`, `.specify/spec-kit-provenance.json`,
  `planning/solution-evaluation.md`, and the linked `research.md`. For a build path,
  include `spec.md`, `plan.md`, `tasks.md`, and the `analyze` result or transcript.
- Whether source URLs were actually verified; what Agent Builder recommended; whether
  you agreed; the output of `check.py`; and any missing artifact, permission failure,
  wrong-version issue, unneeded ceremony, or drift into another workflow. Mark each
  major checkpoint **pass**, **fail**, or **blocked**, with the file or observation
  supporting that verdict.
- In your own words: Was this more useful than the v0.3-style process? Did it help you
  reuse something, narrow the first version, or make a better technical choice? About
  how much time did Define and Plan take, and where did you have to intervene?

If allowed by your project's confidentiality rules, a Codex chat share link or short
redacted activity trace is especially helpful: the files show the result, while the
trace can show whether Agent Builder actually read the bundled Spec Kit instructions.
Do not send credentials, private data, or secret values in the feedback.
Your real skill tests whichever outcome the evidence supports; the other adopt/build
branch can be tested in a separate project during Review.
