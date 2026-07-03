---
name: agent-init
description: "Scaffold the .agent/ working-memory folder in a fresh or existing repo: create memory.md, map.md, tasks.md, decisions.md, plans/ and reviews/, gitignore the folder, and generate the initial source map by crawling the code. Use when the user says 'set up the agent folder', 'init agent memory', 'create the source map', or when the Blueprint starts in a repo that has no .agent/ yet."
metadata:
  version: 0.1.0
  maturity: experimental
  related-workflow: the-blueprint
  related-playbook: [memory-system, the-agent-folder, context-hygiene]
  tags: [memory, source-map, bootstrap, setup, agents]
---

# agent-init

Day zero of the memory system: scaffold the [`.agent/` folder](../../playbook/the-agent-folder.md)
so the agent has durable memory before the first slice of work. The vault's other docs describe
the steady state; this skill is how you *enter* it.

## When to use

The user says "set up the agent folder", "init agent memory", "create the source map" — or you're
starting the [Blueprint](../blueprint/SKILL.md) in a repo that has no `.agent/` yet.

**Do NOT use** when `.agent/` already exists and is healthy — fill gaps only, never overwrite
working memory that's already there.

## Procedure

1. **Check what exists.** If `.agent/` is already present, create only the missing pieces and stop
   touching the rest. Existing memory always wins over a fresh scaffold.

2. **Create the layout** (from [the-agent-folder](../../playbook/the-agent-folder.md)):
   ```
   .agent/
   ├── memory.md      always-loaded index (state, phase, key paths)
   ├── map.md         source map: what IS in the code
   ├── tasks.md       work items: ACTIVE / BACKLOG / DONE
   ├── decisions.md   decisions log (date + rationale)
   ├── plans/         one short plan per task
   └── reviews/       review findings (only when REQUEST_CHANGES)
   ```

3. **Gitignore it.** Add `.agent/` to `.gitignore` (create the file if missing). Working memory is
   regenerable and stays local; if durable decisions should ship, promote them to
   `docs/DECISIONS.md` later.

4. **Generate `map.md` by crawling the code.** Record what *IS*: entry points, commands/routes,
   state shape, key modules and exports, test layout, build/verify commands. Don't speculate and
   don't editorialize — the map is a mirror, not a wishlist. For a large repo, delegate the
   crawling to parallel sub-agents that return summaries, so the main context stays clean (see
   [context-hygiene](../../playbook/context-hygiene.md)). End the map with a
   "last structural change" line.

5. **Seed `tasks.md`** with `ACTIVE / BACKLOG / DONE` sections. Pull real items from the user,
   open TODOs in the code, or the issue tracker. Empty sections are fine; invented tasks are not.

6. **Write `memory.md`** as a short always-loaded index: date, project phase, key paths, one line
   per fact. Keep it small — it's loaded every session, so every line pays rent.

7. **Start `decisions.md`** with a header and any decisions already discoverable in the README or
   docs (with dates if known). Otherwise leave it empty — it fills as real choices get made.

8. **Re-read every file you wrote.** Same rule as the Blueprint's end-of-slice sweep: after
   editing an artifact, re-read it. Then tell the user what was scaffolded and what the map found.

## Notes

- Code always wins over the map; the map wins over assumptions. Regenerate rather than argue.
- This is the setup step the [Blueprint](../blueprint/SKILL.md) assumes has already happened —
  its step 1 ("read the memory index, source map, and tasks file") needs these files to exist.
- Principle behind it: [Give the Agent a Memory](../../playbook/memory-system.md).
