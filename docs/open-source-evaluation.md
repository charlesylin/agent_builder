# Open-source evaluation

**Evaluation date:** 2026-09-08

**Scope:** Determine whether v0.1 should adopt an existing runtime or scaffold.

## Result

No evaluated runtime was adopted in v0.1 because the approved release contains governance
and project scaffolding only. The projects remain candidates or sources of established
patterns; Agent Builder does not copy their source code.

| Project | License | Hands-on result | Disposition |
| --- | --- | --- | --- |
| [PydanticAI](https://github.com/pydantic/pydantic-ai) | MIT | Its slim install, offline test model, and declarative agent loading worked. The project has strong typed Python conventions and extensive tests. | Leading candidate for a future default runtime; retain independent output validation. |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | MIT | Its deterministic scripted model completed an offline agent run without an API key. | Strong optional runtime adapter. |
| [mcp-agent](https://github.com/lastmile-ai/mcp-agent) | Apache-2.0 | A clean install admitted an incompatible MCP 2.x package and failed before scaffolding. Pinning MCP below 2 restored its initializer; its dependency footprint was materially larger. | Reuse architectural ideas, not the current package as the default. |
| [Google Agent Development Kit](https://github.com/google/adk-python) | Apache-2.0 | Documentation and project structure were reviewed during the initial survey. | Revisit only when runtime requirements justify it. |
| [LangGraph new-project template](https://github.com/langchain-ai/new-langgraph-project) | MIT | Its project-template approach was reviewed. | Useful precedent, but more runtime-specific than v0.1. |

The evaluation also considered the official
[A2A samples](https://github.com/a2aproject/a2a-samples) for interoperability patterns. The
v0.1 handoff remains a small local JSON contract so the template does not prematurely adopt
a network protocol.

## Reuse standard

Before adding a future capability, record:

1. the problem and minimum required behavior;
2. maintained open-source candidates;
3. license and attribution obligations;
4. activity, adoption, documentation, tests, security history, and dependency weight;
5. a focused hands-on test when the choice is consequential; and
6. the reason to adopt, adapt, defer, or build.

Any open-source license may be considered, but its obligations and compatibility with the
project's intended distribution must be documented before reuse.
