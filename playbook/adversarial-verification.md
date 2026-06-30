---
title: "Don't Grade Your Own Homework"
type: principle
summary: "The model that built something is the wrong one to judge it. Use a different model as an adversarial reviewer."
maturity: battle-tested
related-workflows: [the-blueprint]
related-skills: [code-review, cross-artifact-sweep]
---

# Don't Grade Your Own Homework

**The model that wrote the code is biased toward "it works." Have a *different* model try to prove it's wrong.**

## Why

A builder optimizes for "done." Ask it to review its own diff and it rationalizes the choices it
just made. A second model, pointed at the same work and told to *break* it, has no ego in the
diff. That tension between "ship it" and "prove it" is where real bugs die. Self-review catches
typos; adversarial review catches the things you were too close to see.

## In practice

- Builder = one model (e.g. Claude Code). Reviewer = a **different** model (e.g. Codex).
- The review prompt is adversarial on purpose: "try to refute this; default to REQUEST_CHANGES if unsure."
- The same pattern works beyond code: vetting findings, pressure-testing a plan, fact-checking research. Generate with one lens, attack with another.

## Receipt

> On a real public-repo review, the building model graded its own work "B+, ready to ship." An
> independent pass over the *same diff* then caught live `e.target`-vs-`currentTarget` bugs,
> missing `aria-label`s on icon controls, and trailing whitespace the first pass had declared
> clean. Same code, different eyes, real defects. The self-grade wasn't lying; it just couldn't
> see its own blind spots.

## Where it shows up

- Workflow: [The Blueprint](../workflows/the-blueprint.md) (the review step is the heart of the loop)
- Skills: [code-review](../skills/code-review/SKILL.md), [cross-artifact-sweep](../skills/cross-artifact-sweep/SKILL.md)
