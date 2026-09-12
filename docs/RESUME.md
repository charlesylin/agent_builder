# Resume Agent Builder

Checkpoint: 2026-09-12. The author requested a pause and repository push to continue from a
work Claude or ChatGPT account. Agent Builder remains in **Review**. This checkpoint does
not approve a new phase or runtime implementation.

## Recover context

Read these files completely, in order:

1. `AGENTS.md`
2. `governance/project-state.yaml`
3. `governance/operating-agreement.md`
4. `governance/decisions.yaml`
5. This file, then the review artifacts relevant to the next task.

The compact machine handoff is `governance/handoff.json`. Its schema is
`src/agent_builder/templates/base/contracts/schemas/agent-handoff.schema.json.tmpl`.
Current governance and newer author instructions take precedence over this checkpoint.
Check Git status and recent commits before editing. Preserve existing changes.

The root `CLAUDE.md` and `GEMINI.md` direct their coding hosts to `AGENTS.md`. In any chat
environment without repository access, ask the author to supply the required files. Do not
claim to have read unavailable files or assume account memory includes previous sessions.
Instruction files guide behavior; they do not guarantee host enforcement or automatic loading.

## Implemented and confirmed

- v0.1 provides a Python 3.11+ scaffold generator and structural validator, with no runtime
  dependencies. Entry points: `scripts/new_agent.py` and `scripts/validate_project.py`.
- Generated projects start in Define and select Codex, Claude Code, and/or Gemini CLI adapters.
- The workflow is Define → Plan → Build → Review with explicit author-approved transitions.
- Engineering defaults: lean Python; deterministic execution; model judgment for orchestration;
  open-source evaluation before custom work; replaceable providers and interfaces.
- Eventual deployment defaults: standalone OCI containers and Docker Compose locally.
  These are policies, not implemented deployment artifacts. External contracts are versioned;
  container isolation does not eliminate compatibility obligations.
- Secrets never enter committed files, prompts, logs, images, or handoffs. Authority is scoped.
- Human closeouts contain high-confidence decisions, uncertainties, questions, and
  “What should you be asking that you are not?” Use None when appropriate. Compact JSON is
  available for machine handoffs; Markdown and standalone HTML serve human presentation.
- Nokkvi's law and practical persistence guidance were committed in `453d8cb` (AB-D015/016).
  Follow the exact instruction in AGENTS.md. Encouragement prompts a thoughtful alternative
  when difficulty alone causes premature stopping; existing limits remain in force.

No runtime, model client, MCP server, custom API, Dockerfile, or Compose service is supplied.
The initializer refuses existing destinations. Generated projects never update automatically.
The template version remains 0.1.0; record the source Git commit too when comparing tests.

## Acceptance experience so far

The author reports that Agent Builder is useful. Full acceptance is still open.

- The original scheduling-agent test was abandoned after the author solved that problem in
  Gemini. Do not resume scheduling-agent implementation here.
- Sean is testing a separately generated project for sourcing secondhand laboratory equipment.
  He is new to agent building. Keep his problem definition and design in his project; this
  repository evaluates the builder's guidance and receives feedback.
- The initial Sean test focuses on Define and Plan. Collect redacted transcripts, phase
  closeouts, repository commits/diffs, model/settings where known, and Sean's friction notes.
  Full transcripts and his generated repository are not included in this checkout.
- Windows onboarding exposed missing Git/Python and private-repository authentication friction.
  The packet delegates setup to Sean's local coding agent with appropriate approvals.
- The author also wants pause/resume across accounts and hosts to test whether repository
  records carry enough context without prior conversation history.

## Review artifacts and open proposals

- `docs/SEAN_CODEX_TEST_PACKET.md`: Windows bootstrap and minimal ideation prompt. It preserves
  the original `1057a49` baseline. That commit predates Nokkvi's law. For a new test including
  that law, explicitly select `453d8cb` or a later reviewed commit and record the change.
  Do not silently replace an ongoing test's baseline or regenerate over Sean's files.
- `docs/onboarding-kit-review.md`: proposed separate employee onboarding kit review case,
  including distinctions among authoring hosts and instruction enforcement (AB-R001–003).
- `docs/existing-project-review.md`: proposed adoption into existing non-agent projects
  while preserving their decisions, artifacts, and phase (AB-R004).
- `docs/COWORK_EXISTING_PROJECT_ADOPTION.md`: proposed manual adaptation derived from the
  original v0.1 commit. It is not a shipped generator feature or validated scaffold and does
  not include later Nokkvi's law changes. Reassess before adopting it.

These artifacts preserve review work; proposed recommendations are not confirmed product
scope. Their external product references were recorded on 2026-09-11 and should be rechecked
when relevant. No company transcripts, credentials, or attached WSJ article are published here.

Candidate next work, requiring prioritization and the appropriate phase approval:

- Review Sean's evidence and convert actual friction into acceptance criteria.
- Evaluate simpler onboarding and safe initialization in an empty cloned repository.
- Evaluate governance reuse in existing projects and non-software work.
- Plan runtime/environment profiles when the author chooses to address them.
- Assess this restart: can the new session recover the phase, decisions, and next step without
  manual coaching? Record missing context as a builder finding.

## Verification and next action

On 2026-09-12, Python 3.14.0 ran these checks successfully:

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall -q src scripts tests
```

All 8 builder tests passed, including the generated project's 3 tests. Earlier wheel and
lint evidence in `docs/validation.md` applies to its dated build; it is not a new release
validation for this checkpoint. Structural tests do not prove agent adherence, performance,
or Windows/Claude/ChatGPT behavior.

In the resumed session, summarize the state and recommend the next Review action for the
author. Identify unavailable evidence honestly. Continue within existing authority; ask for
phase approval only when a proposed next step crosses the recorded phase boundary.
