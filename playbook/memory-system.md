---
title: "Give the Agent a Memory"
type: principle
summary: "An agent's context window is small and resets. Durable knowledge belongs in files, not in the chat."
maturity: battle-tested
related-workflows: [the-blueprint]
related-skills: [agent-init]
---

# Give the Agent a Memory

**Context is precious and ephemeral. Externalize what matters into files so the agent never re-derives it (or drifts) across sessions.**

## Why

A conversation is working memory: small, expensive, and gone when the session ends. If the only
record of a decision lives in the chat, the next session re-discovers it (wasting tokens) or
contradicts it (drifting). Files are long-term memory. A small, always-loaded **index** plus
one-fact-per-file gives the agent continuity it can't get from context alone.

## In practice

- **An always-loaded index** (`.agent/memory.md`): one line per memory, loaded every session.
- **One fact per file**, with frontmatter (what it is, when it's relevant) so recall is by relevance, not by scrolling.
- **A source map** (what *is* in the code) and a **tasks file** (what needs to change), kept separate.
- Update memory *after* structural changes and decisions, not "later." Stale memory is worse than none.
- Code always wins over the map; the map wins over your assumptions.

## Receipt

> This very library was designed across multiple sessions days apart. Each time, the agent opened
> a one-line index, followed it to the right memory file, and resumed mid-thought — including a
> homepage redesign that picked back up *on its exact open questions* after a multi-day gap. None
> of that state lived in the conversation; it lived in files.

## Where it shows up

- Convention: [Keep the Agent's Brain in One Folder](./the-agent-folder.md) — *where* these files live (`.agent/`)
- Workflow: [The Blueprint](../workflows/the-blueprint.md) ("The files in play" — memory index, map, tasks, decisions)
- Related principle: [context-hygiene](./context-hygiene.md) (memory is what lets you keep the live context small)
