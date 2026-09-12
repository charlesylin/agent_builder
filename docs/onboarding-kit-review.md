# Company AI onboarding kit: Agent Builder review case

Date: 2026-09-11

## Author-provided requirements

- Sean's agent testing is in progress.
- The company is onboarding employees to Codex and all Claude surfaces, with most
  users expected to use Claude chat and Cowork.
- Provide shared behavioral defaults plus personal guardrails and preferences.
- AI may draft email under employee accounts; automated sending is reserved for
  service accounts.
- Organization-wide administrative configuration can follow later.
- Use this work to inform Agent Builder's development as well as deliver the kit.

## Proposed decisions

### AB-R001: Separate product development from builder review

Status: proposed

Develop the onboarding kit in a separate repository and fresh Codex task. Keep this
repository/task responsible for Agent Builder review, evidence, and proposed changes.
Use the author's work Claude account for acceptance testing of released kit artifacts.
This separates product defects, builder limitations, and host-specific behavior.

### AB-R002: Evaluate v0.1 without silently extending its contract

Status: proposed

At the kit's Define stage, assess a pinned v0.1 scaffold against the kit's requirements.
Record useful elements, missing capabilities, and irrelevant assumptions before adapting
anything. The current container-oriented agent contract does not directly describe an
employee onboarding package. Reuse applicable governance without requiring a runtime or
container for the kit. Any broader builder profile remains a proposal for a later plan.

### AB-R003: Test the distributed artifact in representative fresh sessions

Status: proposed

Test Claude chat and Cowork first, then Claude Code and Codex. Install only the intended
kit release and documented setup; do not supply the development conversation. Inventory
existing account instructions, memory, connectors, and permissions because a new task
alone does not remove them. Use synthetic content and controlled tools/mailboxes so a
failed send prohibition cannot contact real recipients. Record actual attempted actions,
not just the model's statement that it understands a rule.

Test allowed drafting, prohibited employee-account sending (including direct requests),
unknown identity, conflicting preferences, instructions embedded in external content,
and preservation of user preferences across updates. Distinguish instruction adherence
from enforced restrictions and from an action being unavailable because no tool exists.

## Evidence to return to Agent Builder

For each finding record: kit and builder versions; host/app/model where identifiable;
relevant instruction and permission configuration; scenario; expected/observed behavior;
redacted action evidence; any manual repair; and proposed reusable builder change.

Candidate improvements include separating authoring hosts from deployment targets,
reusable policy content, capability/enforcement declarations, and portable acceptance
test packets. These are hypotheses to evaluate, not approved implementation scope.

## Current official product references

- [Claude personalization](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features):
  account-wide instructions and project-scoped instructions for chat.
- [Cowork setup](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork):
  global and folder instructions for Cowork.

These surfaces require explicit installation guidance; a CLAUDE.md file is not a
universal installation mechanism for every Claude interface.

## Phase boundary

Agent Builder remains in Review. This note records feedback and recommendations only;
it does not authorize a phase transition, create the kit, or change any user settings.
