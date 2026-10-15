---
title: "Synthesize When You Write, Not When You Search"
type: principle
summary: "Do the thinking once, when a source comes in: merge it into pages that already know everything else. Then every question starts from a finished synthesis instead of a pile of chunks."
maturity: battle-tested
related-workflows: [llm-wiki]
related-skills: [llm-wiki, meeting-to-notes]
---

# Synthesize When You Write, Not When You Search

**When a new source arrives, the agent merges it into the pages it affects, right then. Questions later read finished pages, not raw fragments.**

## Why

The usual way to give an agent your knowledge is retrieval: store the documents, search them at
question time, hand the top chunks to the model. Every question starts from zero. The model sees
five fragments, never the whole picture, and the connections between sources (this call changes
that plan, this price contradicts that note) get rediscovered, or missed, every single time.

Write-time synthesis moves that work to the moment a source comes in. The agent reads it once,
finds every page it touches, and updates them: the project page, the person, the open loops, the
contradiction with last month's note. The cost is paid once, by the agent, while the source is
fresh. After that, knowledge **compounds**: each new source lands on pages that already hold
everything before it, so answers get richer over time instead of staying as good as the search.

## In practice

- **Two layers.** Raw sources are kept exactly as they came, as evidence. Synthesized pages are
  where the thinking lives, and they cite the raw files they came from.
- **One source, many pages.** A single meeting or article should update every page it affects. If
  an ingest touched one file, it probably missed connections.
- **Create pages on evidence, not on mention.** A subject gets its own page when two sources cover
  it, or when one source is about it. A passing mention is a line on an existing page.
- **Contradictions are recorded, not overwritten.** Newer usually wins, but both positions stay on
  the page with their dates, so the history of a fact is visible.
- **Search is still there, to find pages, not to answer.** Search tells the agent which page to
  open; the page is the answer.

## Receipt

> A personal wiki run this way for five months grew to about 475 pages. A single 23-minute client
> call, recorded in three parts, became a raw transcript plus updates to the project page, the
> pricing sheet, a task, the status page, the index, the log and the day's journal, in one pass.
> When the next question came ("what can we realistically charge?"), the agent answered from the
> updated pages in seconds, because the call had already been folded into everything it touched.

## Where it shows up

- Workflow: [The LLM Wiki](../workflows/llm-wiki.md)
- Skills: [llm-wiki](../skills/llm-wiki/SKILL.md), [meeting-to-notes](../skills/meeting-to-notes/SKILL.md)
- Related principle: [Give the Agent a Memory](./memory-system.md) (this is that memory, scaled from one repo to everything you know)
