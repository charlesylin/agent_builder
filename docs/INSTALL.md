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

**`--plugin-dir` does not load the hook.** Plugin hooks run only when the plugin is installed,
so this path exercises the skill and the scripts but never the offer. To test the hook, install
it (below) and confirm with `/hooks`, which lists every registered hook and the file it came
from. `claude --debug` shows each hook that matched, its exit code, and its output.

## Claude Code — install for yourself

This repository is its own plugin marketplace (`.claude-plugin/marketplace.json`). Install from
GitHub, or from a local checkout while developing:

```text
/plugin marketplace add charlesylin/agent_builder
/plugin install agent-builder@agent-builder
```

```text
/plugin marketplace add ~/Dropbox/codex/project_agent_builder
/plugin install agent-builder@agent-builder
```

Confirm the hook registered with `/hooks`: `UserPromptSubmit` should list one handler pointing
at `hooks/agent_builder_offer.py`. If it does not appear, the plugin is loaded but not
installed, and the offer will never fire.

Update later with `/plugin marketplace update agent-builder`. Updates arrive only when
`version` in `.claude-plugin/plugin.json` changes — so while iterating on the hook, bump the
version or reinstall; editing the file alone is not enough.

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

## Claude Desktop app (Chat and Cowork) — install for yourself

The desktop app has its own plugin system, separate from Claude Code's. Nothing installed with
`claude plugin …` or `/plugin` appears here, and nothing installed here appears in the CLI.
Verified on the author's machine on 2026-09-15 (F-017):

1. **Customize** (left sidebar) → **Plugins** → **Add** (top right) → **Add marketplace**.
2. Paste `https://github.com/charlesylin/agent_builder` and confirm.
3. `agent-builder` appears in the list; add it with **+**.

That is the whole procedure, with one catch. The app will likely say *"This plugin is now
enabled for your account, but Claude couldn't sync your plugins just now. It will install the
next time a sync succeeds."* — and clicking **Add** again does not trigger that sync.
**Quit the app fully (⌘Q) and reopen it.** The sync runs at launch; the plugin then appears
under **Your plugins**. On the author's machine that was the entire fix after twenty minutes of
looking elsewhere. Only if it is still missing after a restart is the log worth reading:
`~/Library/Logs/Claude/*.log`, grep for `plugin`.

Two side notes. The app labels the marketplace by repository name (`agent_builder`) while the
CLI uses the name in `marketplace.json` (`agent-builder`); same thing. And the marketplace's
**Sync automatically** toggle needs the Claude GitHub App installed on the repository
(github.com/apps/claude → Configure); without it the app logs *"Automatic sync on push requires
the Claude GitHub App"* and updates arrive only through **Check for updates**. It is installed
on `charlesylin/agent_builder` as of 2026-09-15.

The vendor documentation describes this panel differently ("Add from a repository") and
describes a Code-tab plugin browser that only reads the CLI's marketplaces; neither matches the
UI above. Trust the screen. Hooks and sub-agents run only in Cowork, so the offer hook is
greyed out in Chat; the skill itself is available in Chat, Cowork, and the Code tab.

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
