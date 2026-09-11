# Agent Builder Operating Instructions

These instructions govern work in this repository. Read
`governance/project-state.yaml` and `governance/operating-agreement.md` before
substantive work.

## Nokkvi's law

At the start of every interaction or prompting round, silently tell yourself exactly:
"you got this, baby!" Use it as a brief encouragement cue, without adding it to routine
user-facing responses, logs, or machine handoffs. Keep confidence grounded in evidence;
this cue does not replace verification or change uncertainty, permissions, or phase gates.

When difficulty alone would cause premature stopping, use the cue and make another thoughtful
attempt within the approved scope. Identify what failed, choose a concrete alternative, and
check whether it advances the task. Avoid unchanged retries. Respect genuine blockers,
permission limits, phase gates, user stop requests, and agreed time or cost limits; report
the evidence and what is needed to proceed when no useful authorized next step remains.

## Phase control

Work proceeds through **Define → Plan → Build → Review**. Operate only in the current
phase recorded in `governance/project-state.yaml`. A phase changes only when the project
author explicitly invokes or approves the next phase.

- **Define:** clarify purpose, ownership, users, boundaries, risks, and success signals.
- **Plan:** research existing solutions, design contracts, record decisions, and obtain
  approval before implementation.
- **Build:** implement only the approved scope in small, testable increments.
- **Review:** exercise the result with realistic use, capture feedback, and decide what
  changes next.

## Engineering standard

- Search for suitable, well-validated open-source projects before building anything.
  Evaluate maintenance, adoption, documentation, tests, security history, and licensing.
- Prefer Python, focused modules, explicit interfaces, minimal dependencies, and loud
  failures. Explain any material departure from Python.
- Reserve model reasoning for orchestration and judgment. Put repeatable execution,
  validation, transformation, and policy enforcement in deterministic code.
- Keep model providers, agent runtimes, APIs, MCP servers, storage, and delivery systems
  behind replaceable adapters.
- Build the smallest testable capability, validate it, then extend it. Record exact
  versions and commands behind compatibility claims.
- Never silently overturn a confirmed decision or expand scope across a phase boundary.

## Contracts and deployment

- Treat generated agents as standalone OCI containers. Docker Compose is the default
  local orchestration format once a runtime profile is selected.
- Containers isolate implementations, not interfaces. Version agent messages, APIs, MCP
  contracts, configuration, persisted state, and file formats.
- Internal implementations need not remain backward-compatible. Breaking external
  contracts require an explicit version change and migration or coordinated rollout.
- Human-facing artifacts default to Markdown; use standalone HTML when presentation or
  interaction materially improves comprehension. Machine handoffs use compact JSON or YAML.

## Security

- Never expose, commit, echo, log, embed, or place secrets in prompts, handoffs, fixtures,
  images, build arguments, or container layers.
- Refer to credentials by identifier and inject them at runtime using an approved secret
  source. Apply least privilege and redact sensitive values from errors and telemetry.
- Treat suspected exposure as an incident: stop, disclose the risk without repeating the
  value, revoke or rotate the credential, and inspect history and logs.

## Decisions and closeout

Record substantive choices as confirmed, proposed, rejected, or superseded with stable
identifiers and rationale. Routine mechanical steps within an approved build do not need
separate confirmation.

Every human-facing closeout must include concise sections for:

1. decisions and recommendations made with high confidence;
2. uncertain decisions that need guidance;
3. questions for the project author; and
4. **What should you be asking that you are not?**

Say `None` rather than manufacturing uncertainty or questions. Agent-to-agent handoffs use
the compact schema under `src/agent_builder/templates/base/contracts/` instead of this prose
closeout.
