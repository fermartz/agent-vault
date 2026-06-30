---
title: "Protect the Context"
type: principle
summary: "An agent reasons best with a small, relevant working set. Build one slice at a time and keep noise out of the window."
maturity: battle-tested
related-workflows: [the-blueprint]
related-skills: []
---

# Protect the Context

**An agent's reasoning degrades as its context fills with noise. Work one slice at a time, and keep irrelevant detail out of the live window.**

## Why

Every irrelevant file, half-finished tangent, or dumped log competes for the model's attention and
dilutes its reasoning. The fix isn't a bigger window; it's discipline about what's *in* it. Ship
in small slices so the model only holds what the current slice needs, and push bulk reading out to
sub-agents that return conclusions instead of raw material.

## In practice

- **Section by section.** Build one piece, confirm it, move on. Don't one-shot a whole feature into a single sprawling turn.
- **Defer decisions until their slice.** Don't load questions you don't need to answer yet.
- **Delegate read-across to sub-agents.** When something needs sweeping many files, send a sub-agent; it returns the answer, not the file dumps, so your main thread stays clean.
- **Summarize or reset** when a thread gets long. Carry forward the conclusions, drop the scrollback.

## Receipt

> A site redesign was built strictly section by section: hero, then each project card, then the
> skills section, each confirmed before the next. Separately, understanding two sibling codebases
> was delegated to parallel explore agents that read the repos and returned tight summaries, so the
> main session held the *findings* and never the thousands of lines behind them. The work stayed
> sharp because the window stayed small.

## Where it shows up

- Workflow: [The Blueprint](../workflows/the-blueprint.md) (smallest clean change; one slice at a time)
- Related principle: [memory-system](./memory-system.md) (files hold what the window shouldn't)
