# Getting started

From zero to a working skill in a few minutes. Pick the way in that fits, install what the skill
needs, run it once, then make it yours.

## 1. Get the repo

```sh
git clone https://github.com/fermartz/agent-vault.git
cd agent-vault
```

Or skip this step and let your agent do it (section 3).

## 2. Install a skill

A skill is a folder with a `SKILL.md` (and sometimes a script). Copy the whole folder.

**Claude Code**: all your projects, or just one:

```sh
mkdir -p ~/.claude/skills && cp -r skills/meeting-to-notes ~/.claude/skills/   # every project
mkdir -p .claude/skills && cp -r skills/meeting-to-notes .claude/skills/       # this project only (run inside it)
```

Claude Code lists installed skills and loads one when your request matches its description.

**Codex, or any agent that reads an instructions file**: copy the folder into your project and
point to it from `AGENTS.md` (or your agent's equivalent):

```markdown
## Skills
- When I share a meeting recording, read `skills/meeting-to-notes/SKILL.md` and follow it.
- For any non-trivial code change, follow `skills/blueprint/SKILL.md`.
```

**Skills that call each other** (`meeting-to-notes` uses `video-transcript`; `llm-wiki` uses both
when you ingest recordings): install them together so their relative links resolve.

## 3. Or hand it to your agent

Paste this into your agent and edit the list:

```text
Read https://github.com/fermartz/agent-vault (README, then the skills I name).
Install these skills for me: meeting-to-notes, video-transcript, llm-wiki.
For each one, read its Requirements section, check what's already installed on my
machine, and tell me what's missing with the install command. Ask me before
installing anything. Then add the brevity block from playbook/human-context.md to
my CLAUDE.md (or AGENTS.md), and tell me how to try each skill once.
```

## 4. What each skill needs

Every skill that needs a tool has a **Requirements** section with check and install commands for
macOS (Homebrew) and Debian/Ubuntu Linux, and it checks before its first run and asks before installing anything (Windows: [see below](#windows)). The short version:

| Skill | Needs |
|---|---|
| video-transcript | Python 3.10+, ffmpeg, yt-dlp (links only), uv or whisper |
| meeting-to-notes | Python 3.10+, ffmpeg, uv or whisper |
| llm-wiki | git; qmd optional |
| agent-deploy | Node.js, Vercel CLI, Cloudflare MCP or wrangler, dig, curl |
| blueprint, code-review | git, plus a second agent for the audit (Codex or Claude Code) |
| skill-builder | Python 3.10+ and PyYAML, for its checker only |
| teach-in-bites, agent-init, cross-artifact-sweep, public-repo-audit | git at most |

### Windows

**Recommended: WSL.** In PowerShell as administrator run `wsl --install`, restart, and open the
Ubuntu app it installs. Run your agent inside Ubuntu; every Linux command in the skills then works
as written. One limit: `video-transcript` can't borrow your Windows browser's login from inside WSL,
so login-gated Instagram, Facebook or X posts need the native setup; public links and local files
work.

**Native Windows (untested).** These are the equivalent commands, in PowerShell, but nobody has run
the skills this way yet. If you do, tell me what broke.

| Tool | Check | Install |
|---|---|---|
| git | `git --version` | `winget install Git.Git` |
| Python 3.10+ | `py -c "import sys; assert sys.version_info >= (3, 10)"` | `winget install Python.Python.3.12` |
| ffmpeg | `ffmpeg -version` | `winget install Gyan.FFmpeg` |
| yt-dlp | `yt-dlp --version` | `winget install yt-dlp.yt-dlp` |
| uv | `uv --version` | `winget install astral-sh.uv` |
| whisper (instead of uv) | `whisper --help` | `py -m pip install openai-whisper` |
| PyYAML | `py -c "import yaml"` | `py -m pip install pyyaml` |
| Node.js + npm | `node --version; npm --version` | `winget install OpenJS.NodeJS.LTS` |
| Vercel CLI, wrangler | `vercel --version`, `wrangler --version` | `npm i -g vercel wrangler` |
| Codex or Claude Code | `codex --version`, `claude --version` | `npm i -g @openai/codex` or `npm i -g @anthropic-ai/claude-code` |
| DNS and HTTP checks | `Resolve-DnsName example.com`, `curl.exe -I https://example.com` | built in (use these instead of `dig` and `curl`) |

Where the skills say `python3`, use `py`. Install a skill for Claude Code:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse skills\meeting-to-notes "$HOME\.claude\skills\"
```

## 5. Try it once

- **meeting-to-notes**: drop a call recording and say "transcribe the meeting and update my notes".
- **llm-wiki**: "set up a wiki here" in an empty folder; it starts from the
  [starter schema](../skills/llm-wiki/references/starter-schema.md).
- **blueprint**: "use the blueprint to add X". It rates the change S/M/L/XL first.
- **skill-builder**: "help me make a skill". With nothing to extract from, it interviews you one
  question at a time.

## 6. Make it yours

**The audit switch.** One line in `CLAUDE.md` / `AGENTS.md`:

```markdown
Audit: auto      # default: S/M changes skip the second-agent audit, L/XL get it
Audit: always    # every change
Audit: off       # none (the agent says so once on each L/XL change)
```

Per change, say "skip the audit" or "audit this one"; that beats the setting either way, and every
audit skipped that the setting would have run is logged. Why I keep it on:
[the audit switch](../workflows/the-blueprint.md#your-call-the-audit-switch).

**Short answers.** Paste the block from [Protect the Human's Context](../playbook/human-context.md#make-it-stick).

**Your change levels.** Write your project's own S/M/L/XL table with its real test commands and
boundary files ([change levels](../workflows/the-blueprint.md#size-the-ceremony-change-levels)).

**Your own skills.** Load [skill-builder](../skills/skill-builder/SKILL.md). Before sharing, run its
checker with a private word list kept outside the repo:

```sh
python3 skills/skill-builder/scripts/check_skills.py . --deny-file ~/private-words.txt
```

## 7. Stay up to date

```sh
cd agent-vault && git pull
mkdir -p ~/.claude/skills && cp -r skills/meeting-to-notes ~/.claude/skills/   # re-copy the skills you use
```

If you edited your installed copy (your own paths, your own projects), compare before overwriting.
