---
title: "A Plan Is a Contract, Not a Spec"
type: principle
summary: "Plan what to build and why. Leave how to the code. Over-specified plans generate review rounds that catch drift, not bugs."
maturity: battle-tested
related-workflows: [the-blueprint]
related-skills: [blueprint]
---

# A Plan Is a Contract, Not a Spec

**A plan locks the *what* and the *why*. The *how* belongs in the code, decided while you build.**

## Why

The moment a plan spells out *how* (pseudocode, exact signatures, step-by-step state), it becomes
a second source of truth. A reviewer then audits the code against the plan and flags every place
they diverge, generating review rounds that catch documentation drift instead of real defects.
Worse, you "fix" each finding by adding more detail to the plan, which creates more surface area
for the next round. Keep the plan a contract and the code stays the single source of truth.

## In practice

- Aim for **under 200 lines.** Purpose, success criteria, scope (in/out), locked decisions, checkpoints, risks.
- **Not** in the plan: pseudocode, function signatures, exhaustive types, state transitions.
- Get approval on the contract *before* writing code. Cheap to change a plan; expensive to change a built thing.

## Receipt

> An MCP feature plan (Delphy Agent) ballooned to **339 lines / 70KB across 4 revision rounds.**
> Each round added implementation detail to satisfy a reviewer finding, which created new surface
> area for the next round to catch. The reviews were accurate; the errors were self-inflicted, all
> caused by the plan over-specifying things that should have been decided during the build.

## Where it shows up

- Workflow: [The Blueprint](../workflows/the-blueprint.md) ("Plan scope and size")
- Skill: [blueprint](../skills/blueprint/SKILL.md) (step 1 enforces the contract-sized plan)
