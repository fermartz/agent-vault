---
title: "Keep the Agent's Brain in One Folder"
type: convention
summary: "Put every working file the agent reads and writes in one well-known directory: .agent/. Tool config stays in .claude/; the agent's brain lives in .agent/."
maturity: battle-tested
related-playbook: [memory-system]
related-workflows: [the-blueprint]
---

# Keep the Agent's Brain in One Folder

**Every file the agent reads and writes as it works belongs in one well-known directory: `.agent/`.**

## Why

Scattering memory, plans, and notes across the repo makes them hard to find, easy to forget, and
noisy in diffs. One folder gives the agent (and you) a single place to look, a single thing to
gitignore, and a clean mental model: **tool config lives in `.claude/`; the agent's brain lives in
`.agent/`.** The name is deliberately tool-agnostic — it reads the same whether you're driving
Claude Code, Codex, or anything else.

## The layout

```
.agent/
├── memory.md      always-loaded index (state, phase, key paths)
├── map.md         source map: what IS in the code
├── tasks.md       work items: active / backlog / done
├── decisions.md   decisions log (date + rationale)
├── plans/         one short plan per task
└── reviews/       review findings (only when REQUEST_CHANGES)
```

## Local vs public

For a public repo, **gitignore `.agent/`** — it's working memory you regenerate as you go — but
**promote `decisions.md` to `docs/DECISIONS.md`** so the reasoning ships. Working files stay
private; durable decisions go public.

## Receipt

> I landed on this after months across many projects with Claude Code and Codex. On Delphy Agent
> it was a `.hermes/` folder holding plans, reviews, and the working memory, and it worked so well
> that the only thing worth changing for a public recommendation is the name. One folder, always in
> the same place, gitignored except for the decisions that deserve to ship.

## Where it shows up

- Principle: [Give the Agent a Memory](./memory-system.md) (this is *where* that memory lives)
- Workflow: [The Blueprint](../workflows/the-blueprint.md) ("The files in play")
- Skill: [agent-init](../skills/agent-init/SKILL.md) (scaffolds this folder in a new repo)
