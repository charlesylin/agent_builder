# Principles

The only place a principle's text is written. Everything else that states a principle — the
skill, this repository's `AGENTS.md` and operating agreement, the template operating agreement,
and the coding-agent adapter files — is generated from these files by `scripts/render.py`. Edit
here, run the renderer, commit the result. A test fails if a generated copy is edited directly.

Each file has YAML-style front matter with `id` and `title`, then the full text, then an
optional `## Short form` section used where a one-paragraph statement is enough.

| id | title |
| --- | --- |
| `phases` | Phase control |
| `decision-protocol` | Decision protocol |
| `nokkvis-law` | Nokkvi's law |
| `use-reasoning-selectively` | Use reasoning selectively |
| `search-before-building` | Search before building |
| `work-small-fail-loudly` | Work small and fail loudly |
| `keep-boundaries-replaceable` | Keep boundaries replaceable |
| `containerize-the-deployed-agent` | Containerize the deployed agent |
| `security-and-authority` | Security and authority |
| `communication-and-handoffs` | Communication and handoffs |
| `build-only-what-you-need` | Build only what you need |

Reference a principle in a stencil as `{{principle:<id>}}` (full text),
`{{principle:<id>|short}}` (short form), or `{{principle:<id>|title}}`.
