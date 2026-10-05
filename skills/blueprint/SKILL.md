---
name: blueprint
description: "Run a non-trivial coding change through plan → build → verify → review, with a second model as an adversarial reviewer. Use when the user says 'use the blueprint' / 'run the blueprint' / 'plan and build this properly', or starts a non-trivial feature, refactor, or subsystem that should be planned, reviewed, and verified before shipping."
metadata:
  version: 1.1.0
  maturity: battle-tested
  related-workflow: the-blueprint
  tags: [workflow, planning, code-review, verification, agents]
---

# blueprint

Execute the Blueprint loop. This is the agent-facing, do-this version of
[`workflows/the-blueprint.md`](../../workflows/the-blueprint.md) — read that for the *why*,
the diagram, and the lessons behind each step.

## When to use

The user says any of: "use the blueprint", "run the blueprint", "plan and build this properly",
or kicks off a non-trivial feature / refactor / subsystem.

**Match the ceremony to the stakes:** step 0 rates the change, and the rating decides how much of the
loop runs. Throwaway scripts need none of it.

## The loop

```
recon → plan → build → verify → review → (fix → class-sweep → verify → re-review)* → approve
```
One model builds; a **different** model reviews. At L and XL, nothing ships until the independent
review approves.

## Procedure

0. **Rate the change, and say it** (e.g. "S change, about a minute"); the user can bump it. When
   unsure, go one level up. Full table and receipt:
   [change levels](../../workflows/the-blueprint.md#size-the-ceremony-change-levels).
   - **S, copy** (a title, label, wording): no recon, no plan, no review.
   - **M, one screen or module**: no recon, no plan, no review; read the map first.
   - **L, feature**: recon and a plan when the change is non-trivial; review.
   - **XL, risky** (security, auth, data writes, a dependency, a schema, the project's boundary
     files, whatever their size): recon, a plan and the review are all required.
   Each step below says what it runs at each level. Never S or M: anything on the XL list, or a
   rename, move or removal of anything the docs describe (that is at least L). The rating sets the checks
   only; step 8 still holds.

1. **Recon — before planning** (L when non-trivial, XL always; not S or M)
   - Inventory the live state the plan will touch with **read-only commands**, exhaustively —
     accounts, schemas, dependencies, consumers. If the plan will claim a boundary (security,
     compatibility, cost), enumerate the *entire class* the boundary is drawn over, not just
     the parts that seem relevant.
   - Verify every external fact (prices, current versions, API defaults, provider behavior)
     against **live sources at plan time** — never from memory/training data.
   - **No claim without its command:** every factual claim in the plan cites the read-only
     command that proves it, actually run before the claim is written.

2. **Before building**
   - All levels: read the memory index, source map, and tasks file. If `.agent/` doesn't exist yet, scaffold
     it first (see [agent-init](../agent-init/SKILL.md)). Read relevant docs/schemas/examples.
   - Identify the files likely to change.
   - L when non-trivial, XL always (never S or M): write a **concise plan (< 200 lines)** to `.agent/plans/<date>_<task>.md`: purpose, success
     criteria, scope (in/out), locked decisions, checkpoints, risks. NOT pseudocode or type signatures.
   - When there is a plan, **get the user's approval BEFORE writing code.**

3. **Build** — smallest clean change that satisfies the task. No unrelated rewrites, no
   speculative abstractions, no comments unless the *why* is non-obvious. Never touch secrets/.env.

4. **Verify**, by level:
   - **S:** lint/typecheck, the one test that names the text, `git diff --check`.
   - **M:** S + the unit tests + only the changed area's end-to-end tests and snapshots; show the
     result.
   - **L and XL:** the project's full suite (tests, lint/typecheck, schema/artifact checks,
     `git diff --check`), and for changes with a runtime surface, exercise the changed flow
     end-to-end; a green suite proves the tests pass, not that the feature works.
   Fix anything red before moving on.

5. **Hand off to the reviewer** (L and XL only) — give the user an adversarial review command for a *second* model:
   ```
   codex exec "Review the uncommitted diff. Plan: <plan-file>. Check: spec compliance, bugs,
   missing tests, security, scope creep, overengineering. Do not modify any project files —
   the only file you may create is the review report. Output ONLY APPROVED or REQUEST_CHANGES
   + a one-line summary; if REQUEST_CHANGES, write details to .agent/reviews/<task>.md"
   ```
   Codex is an example — any second model works (`gemini`, a separate Claude Code session). If
   none is available, use a **fresh session of the same model** with the same prompt: weaker,
   but far better than self-review in the same conversation.

6. **If REQUEST_CHANGES** — read the review, then **fix the class, not the instance**: identify
   each finding's defect *category* and audit everywhere that category can live before revising
   (one stale admin user → enumerate everything that can hold admin; one wrong price → re-verify
   every price). Then run the **cross-artifact sweep**
   (see [`skills/cross-artifact-sweep`](../cross-artifact-sweep/SKILL.md)): list what changed, grep
   each removed/changed term across memory + map + tasks + decisions + the plan, update or
   contextualize every hit, re-verify, re-grep, then re-review. Loop until APPROVED — with a
   **round budget of 3**: after 3 REQUEST_CHANGES rounds, stop and re-examine the plan with the
   user. A non-converging loop usually means the plan is over-specified, mis-scoped, or was
   written without recon (step 1), not that the code is subtly wrong.

7. **End-of-slice sweep** before claiming done. S and M: a one-line task note, plus the map if
   files were added. L and XL, on APPROVED: update the state index, the source
   map (list the actual files; re-read moved prose), move the task to DONE with the verdict, log any
   decision, check the plan's boxes. Re-read each artifact after editing.

8. **Do not commit unless explicitly asked.**

## Notes
- Keep the plan a contract for *what/why*, not a spec for *how* — over-specified plans generate
  review rounds that catch documentation drift, not bugs.
- The cross-artifact sweep (step 6) is the gate that keeps review loops short. Don't skip it.
- Recon (step 1) is what keeps round 1 short: the reviewer's cheapest wins are facts you asserted
  from memory instead of checking. (Receipt: 7 REQUEST_CHANGES rounds on fermartz-infra's first
  RDS plan, 2026-08-23 — nearly all findings were pre-existing live-state facts.)
