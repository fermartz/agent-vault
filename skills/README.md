# Skills — the *what*

Loadable `SKILL.md` tools. To use one, copy its folder into your project's `.claude/skills/`
(or `~/.claude/skills/` for all projects) and your agent can invoke it.

| Skill | What it does |
|---|---|
| [agent-init](./agent-init/SKILL.md) | Scaffold the [`.agent/`](../playbook/the-agent-folder.md) working-memory folder and generate the initial source map |
| [agent-deploy](./agent-deploy/SKILL.md) | Deploys, env vars, domains and DNS on Vercel + Cloudflare, with a cost check and a human yes before anything billable or public |
| [blueprint](./blueprint/SKILL.md) | Run a change through the plan → build → verify → review loop (the executable twin of [The Blueprint](../workflows/the-blueprint.md)) |
| [code-review](./code-review/SKILL.md) | Adversarially review a diff and return APPROVED / REQUEST_CHANGES with findings |
| [cross-artifact-sweep](./cross-artifact-sweep/SKILL.md) | After a fix, keep docs/memory in sync with the code so review loops stay short |
| [public-repo-audit](./public-repo-audit/SKILL.md) | Audit a whole repo as a skeptical external engineer: quality, security, CI, tests, hygiene |
| [llm-wiki](./llm-wiki/SKILL.md) | Ingest, query and lint a markdown + git wiki the agent maintains (the executable twin of [The LLM Wiki](../workflows/llm-wiki.md)) |
| [meeting-to-notes](./meeting-to-notes/SKILL.md) | Turn a call recording into notes: local transcript kept as evidence, takeaways confirmed, then tasks and open loops updated |
| [video-transcript](./video-transcript/SKILL.md) | Pull the spoken text out of a social video or a local audio/video file, locally, and say what it actually claims |
| [teach-in-bites](./teach-in-bites/SKILL.md) | Teach a topic one bite at a time, the human sets the pace, then file the lesson as a primer |

*More skills get added as I extract the ones I reach for most.*

Back to [the vault](../README.md).
