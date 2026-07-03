---
name: blueprint
description: "Run a non-trivial coding change through plan → build → verify → review, with a second model as an adversarial reviewer. Use when the user says 'use the blueprint' / 'run the blueprint' / 'plan and build this properly', or starts a non-trivial feature, refactor, or subsystem that should be planned, reviewed, and verified before shipping."
version: 0.1.0
maturity: battle-tested
related-workflow: the-blueprint
metadata:
  tags: [workflow, planning, code-review, verification, agents]
---

# blueprint

Execute the Blueprint loop. This is the agent-facing, do-this version of
[`workflows/the-blueprint.md`](../../workflows/the-blueprint.md) — read that for the *why*,
the diagram, and the lessons behind each step.

## When to use

The user says any of: "use the blueprint", "run the blueprint", "plan and build this properly",
or kicks off a non-trivial feature / refactor / subsystem.

**Do NOT use for** one-line fixes, typos, or throwaway scripts. Match the ceremony to the stakes.

## The loop

```
plan → build → verify → review → (fix → sweep → verify → re-review)* → approve
```
One model builds; a **different** model reviews. Nothing ships until the independent review approves.

## Procedure

1. **Before building**
   - Read the memory index, source map, and tasks file. If `.agent/` doesn't exist yet, scaffold
     it first (see [agent-init](../agent-init/SKILL.md)). Read relevant docs/schemas/examples.
   - Identify the files likely to change.
   - Write a **concise plan (< 200 lines)** to `.agent/plans/<date>_<task>.md`: purpose, success
     criteria, scope (in/out), locked decisions, checkpoints, risks. NOT pseudocode or type signatures.
   - **Get the user's approval BEFORE writing code.**

2. **Build** — smallest clean change that satisfies the task. No unrelated rewrites, no
   speculative abstractions, no comments unless the *why* is non-obvious. Never touch secrets/.env.

3. **Verify** — run the project's suite: tests, lint/typecheck, schema/artifact checks,
   `git diff --check`. Fix anything red before review.

4. **Hand off to the reviewer** — give the user an adversarial review command for a *second* model:
   ```
   codex exec "Review the uncommitted diff. Plan: <plan-file>. Check: spec compliance, bugs,
   missing tests, security, scope creep, overengineering. Do not modify any project files —
   the only file you may create is the review report. Output ONLY APPROVED or REQUEST_CHANGES
   + a one-line summary; if REQUEST_CHANGES, write details to .agent/reviews/<task>.md"
   ```

5. **If REQUEST_CHANGES** — read the review, fix the blockers, then run the **cross-artifact sweep**
   (see [`skills/cross-artifact-sweep`](../cross-artifact-sweep/SKILL.md)): list what changed, grep
   each removed/changed term across memory + map + tasks + decisions + the plan, update or
   contextualize every hit, re-verify, re-grep, then re-review. Loop until APPROVED — with a
   **round budget of 3**: after 3 REQUEST_CHANGES rounds, stop and re-examine the plan with the
   user. A non-converging loop usually means the plan is over-specified or mis-scoped, not the code.

6. **On APPROVED — end-of-slice sweep** before claiming done: update the state index, the source
   map (list the actual files; re-read moved prose), move the task to DONE with the verdict, log any
   decision, check the plan's boxes. Re-read each artifact after editing.

7. **Do not commit unless explicitly asked.**

## Notes
- Keep the plan a contract for *what/why*, not a spec for *how* — over-specified plans generate
  review rounds that catch documentation drift, not bugs.
- The cross-artifact sweep (step 5) is the gate that keeps review loops short. Don't skip it.
