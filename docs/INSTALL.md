# Install Agent Builder

Agent Builder is a skill. Installing it means getting the folder `skills/agent-builder/` in
front of a coding agent. Nothing is installed with pip; the two scripts inside need only
Python 3.9 or newer. Mechanics verified against vendor documentation on 2026-09-13.

## How people invoke it

Explicitly, which is the trained path:

- **Claude Code:** `/agent-builder:agent-builder`
- **Codex:** `$agent-builder`

Or the skill's own description matches what they typed. Or — Claude Code only — the plugin's
hook notices a prompt that looks like the start of new work and asks Claude to offer once.
Answering no mutes the offer for that session; the skill stays available by name.

## What the hook does, for whoever reviews this plugin

Enabling the plugin means `hooks/agent_builder_offer.py` runs on **every prompt** in Claude
Code. It is standard-library Python, about 120 lines, and readable in a sitting. It reads the
prompt from stdin, prints nothing at all unless the text matches a create-something pattern
*and* the working directory is not already a seeded project *and* the session has not been
muted, and always exits 0 — a failure prints nothing rather than interfering with the prompt.
It writes one empty marker file under the system temp directory when muted. It makes no
network calls and reads no files outside the working directory.

To disable it while keeping the skill, remove `hooks/` from an installed copy, or disable the
plugin and put `skills/agent-builder` in `~/.claude/skills/` instead.

## Claude Code — try it without installing

```sh
claude --plugin-dir /path/to/agent_builder
```

Loads the plugin for that session only. Nothing to uninstall. Run this from an **empty**
folder to test starting a project, or from inside a seeded project to test resuming.

## Claude Code — install for yourself

This repository is its own plugin marketplace (`.claude-plugin/marketplace.json`).

```text
/plugin marketplace add charlesylin/agent_builder
/plugin install agent-builder@agent-builder
```

Update later with `/plugin marketplace update agent-builder`. Updates arrive only when
`version` in `.claude-plugin/plugin.json` changes.

## Claude Code — for everyone in the organization

Managed settings pre-register the marketplace and enable the plugin for every user:

```json
{
  "extraKnownMarketplaces": {
    "agent-builder": {
      "source": { "source": "github", "repo": "charlesylin/agent_builder" }
    }
  },
  "enabledPlugins": {
    "agent-builder@agent-builder": true
  }
}
```

## claude.ai, Claude Desktop, Cowork — for everyone in the organization

An organization admin, in admin settings → plugins:

1. Connect this GitHub repository as a marketplace. Plugins sync when the default branch
   changes.
2. Set `agent-builder` to **Available for install** for an opt-in test, or **Installed by
   default** once Review has closed.

Distributed plugins appear in claude.ai chat, Claude Desktop, and Cowork. Claude Code users
are covered by the managed-settings block above.

## Codex

Codex reads skills from `$HOME/.agents/skills`, `/etc/codex/skills`, and a repository's
`.agents/skills`. The skill folder is self-contained — templates ship inside it — so a copy or
a symlink is enough:

```sh
mkdir -p ~/.agents/skills
ln -s /path/to/agent_builder/skills/agent-builder ~/.agents/skills/agent-builder
```

Invoke explicitly with `$agent-builder`, or let the description trigger it. Codex support is
best-effort in v0.2 (AB-D028): the format is identical, but it has been exercised less.

## Gemini CLI

Seeded projects carry a `GEMINI.md` pointer to their own governance files. Loading the skill
itself in Gemini CLI has not been verified.

## What a seeded project needs from its owner's machine

Only `git` (for the first commit; the seed succeeds without it and says so) and `python3`
3.9+ for `check.py` in CI. Nothing else.

## Uninstall

Claude Code: `/plugin uninstall agent-builder@agent-builder`, then
`/plugin marketplace remove agent-builder`. Codex: remove the symlink. Seeded projects are
unaffected; they never depended on the skill being present.
