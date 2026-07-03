# Skills — the *what*

Loadable `SKILL.md` tools. To use one, copy its folder into your project's `.claude/skills/`
(or `~/.claude/skills/` for all projects) and your agent can invoke it.

| Skill | What it does |
|---|---|
| [blueprint](./blueprint/SKILL.md) | Run a change through the plan → build → verify → review loop (the executable twin of [The Blueprint](../workflows/the-blueprint.md)) |
| [code-review](./code-review/SKILL.md) | Adversarially review a diff and return APPROVED / REQUEST_CHANGES with findings |
| [cross-artifact-sweep](./cross-artifact-sweep/SKILL.md) | After a fix, keep docs/memory in sync with the code so review loops stay short |
| [public-repo-audit](./public-repo-audit/SKILL.md) | Audit a whole repo as a skeptical external engineer: quality, security, CI, tests, hygiene |

*More skills get added as I extract the ones I reach for most.*

Back to [the vault](../README.md).
