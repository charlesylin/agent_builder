# Agent Builder v0.1 test packet for Sean

Hi Sean —

We are testing an early Agent Builder template by using it to explore an agent broadly
concerned with sourcing secondhand laboratory equipment. You are intentionally not being
given a detailed specification. Part of the test is whether the generated repository and
Codex help you define the problem, make decisions, and develop a useful plan.

This is a test of the template, not of you. Work naturally, ask questions when something is
unclear, and record any place where the process is confusing or unhelpful.

## 1. Let Codex prepare the project

You do not need to use a terminal yourself.

1. In Windows File Explorer, create an empty local folder named `agent_builder_test`.
2. Open the Codex desktop app and add that folder as a local project.
3. Attach or drag this file into a new Codex task.
4. Send: **Please carry out the bootstrap instructions in the attached test packet.**
5. Review and approve only the installation requests you understand and expect.

The following bootstrap instructions are for Codex:

> Prepare the Agent Builder v0.1 acceptance test on this Windows computer. Sean should not
> need to type or paste shell commands; run the necessary commands yourself and explain any
> approval he must provide.
>
> 1. Confirm that the current workspace is the empty local `agent_builder_test` folder. Do
>    not write outside it without explicit permission.
> 2. Inspect the environment for Git and a Python interpreter version 3.11 or newer. Check
>    common Windows commands such as `git`, `py`, and `python`; do not assume `python3` exists.
> 3. If Git or Python is missing, ask Sean to approve installing only the missing tool with
>    the Windows package manager `winget`. Use the official Git package and a supported
>    Python 3 release. Do not install Node.js, WSL, Docker, GitHub CLI, or other unrelated
>    tools for this bootstrap.
> 4. If an installation requires an app or terminal restart, explain that clearly and stop
>    at a safe checkpoint. Resume after Sean restarts Codex. Do not weaken PowerShell policy,
>    disable the sandbox, or request broad machine access to work around a problem.
> 5. Clone `https://github.com/charlesylin/agent_builder.git` into an `agent_builder`
>    subdirectory and check out exact commit `1057a49`. Do not modify its source.
> 6. Use its existing generator to create a sibling subdirectory named
>    `used_lab_equipment_agent` with:
>    - name: `Used Laboratory Equipment Agent`
>    - purpose: `Help our company source secondhand laboratory equipment.`
>    - adapter: `codex`
> 7. Run the repository's existing validator against the generated project. If it fails,
>    report the exact failure instead of manually repairing the generated output.
> 8. Initialize a local Git repository with a `main` branch in
>    `used_lab_equipment_agent`, stage the generated files, and commit them with the message
>    `chore: initialize from Agent Builder v0.1`.
> 9. If Git identity is not configured, ask Sean for the name and work email to configure
>    for this repository only. Never invent an identity and do not request credentials.
> 10. Do not create a remote repository, authenticate to GitHub, push, begin designing the
>     agent, or make changes to Agent Builder.
> 11. Finish by reporting the detected and installed tool versions, validation result,
>     generated-project path, and commit hash. Then tell Sean to open
>     `used_lab_equipment_agent` as a new local project in Codex and provide him with the
>     initial prompt from section 2 of this packet.

If a company security policy blocks installation, Codex should stop and report the blocker.
Sean should not use an unofficial installer or bypass company controls.

## 2. Begin the test in the generated project

After bootstrap succeeds, open `used_lab_equipment_agent` as a new local project in Codex.
This is important: do not continue the design exercise from the bootstrap task or from the
`agent_builder_test` parent folder.

Paste this as the first prompt in the generated project:

> Follow the instructions in this repository.
>
> I am new to building agents. I want to explore an agent that could help our company source
> secondhand laboratory equipment, but I do not yet know its exact users, capabilities,
> boundaries, workflow, or implementation.
>
> Guide me through the project's current phase at an appropriate level for a beginner.
> Explain important choices and tradeoffs without assuming a design. Stop at a useful
> checkpoint for my input.

The prompt is deliberately broad. Converse with Codex normally after sending it.

A remote GitHub repository is not needed for the initial Define and Plan test. If one is
added later, it should be private and company-owned, and Sean should confirm that GitHub is
authenticated with the intended company account before pushing.

## 3. How to conduct the test

- For this first pass, work through **Define** and **Plan**, then stop. A runtime or deployed
  agent is not expected from Agent Builder v0.1.
- Do not approve a phase transition until you understand and agree with the result.
- Do not manually remind Codex of repository rules merely to make the test succeed. If it
  misses a rule, record that as a template finding. Intervene only when needed to prevent an
  unsafe action or unintended external change.
- Ask Codex to commit the approved repository changes at the end of each phase.
- Never enter credentials, API keys, tokens, confidential pricing, personal information, or
  proprietary company data. Use placeholders or synthetic examples.

Suggested checkpoint commits:

```text
chore: initialize from Agent Builder v0.1
docs: complete Define phase
docs: complete Plan phase
```

## 4. Evidence to return after each phase

Please send Charles:

1. The transcript for the phase, after removing sensitive information.
2. Codex's final closeout.
3. The resulting commit hash or repository diff.
4. The Codex model and reasoning setting used.
5. Brief answers to these questions:
   - What was clear and helpful?
   - What was confusing, excessive, or missing?
   - What assumptions did Codex make that you did not expect?
   - What did you have to remind Codex to do?
   - At the end of the phase, did you understand what had been decided and what came next?

Do not clean up awkward parts of the transcript. Friction and mistakes are valuable evidence
for improving Agent Builder.

## 5. What success looks like

The template succeeds if Codex helps a new agent builder reason through an underdefined
problem, respects phase boundaries, makes decisions explicit, investigates existing
solutions before proposing custom work, handles security appropriately, and leaves the user
clear about the next step without requiring separate coaching from Charles.
