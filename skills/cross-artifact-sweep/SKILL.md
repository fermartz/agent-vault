---
name: cross-artifact-sweep
description: "After changing code, sweep the docs and memory so they don't drift from reality. List what changed, grep each removed/changed term across memory, source map, tasks, decisions, and the plan, then update or contextualize every hit. Use after a fix and before re-issuing a review, or before claiming a task done."
version: 0.1.0
maturity: battle-tested
related-workflow: the-blueprint
related-playbook: [memory-system, plan-build-review]
metadata:
  tags: [docs, memory, consistency, verification, agents]
---

# cross-artifact-sweep

Keep the written record in sync with the code after a change. This is the gate that stops review
loops from dragging on, where each round catches new drift between code and docs instead of real
bugs. Run it **after every fix, before re-review**, and again as a final pass before "done."

## When to use

- Right after fixing code in response to a review, **before** re-issuing the review.
- Before claiming a task complete.
- Any time you renamed, moved, or removed something that the docs/memory might still describe.

## Procedure

1. **List what changed.** Concretely: identifiers added/removed, file paths created/moved/deleted,
   and design phrases that no longer match reality (e.g. "stdin writer task" → "inline write").
   Write it down; don't trust memory.
2. **Grep each removed/changed term** across the written record: memory index, source map, tasks
   file, decisions log, architecture docs, and the active plan. Cast wider than feels necessary.
   ```
   grep -rn 'oldName\|old_path\|removed_term' MEMORY.md *-map.md *-tasks.md docs/ plans/
   ```
3. **For each hit, decide:** (a) update to the shipped wording, or (b) contextualize as history
   ("plan initially proposed X; review round N changed it to Y"). Both are valid; **silence is not.**
4. **Re-read moved prose, don't just grep.** Grep catches renamed symbols, NOT stale sentences. For
   any subsystem that moved, open the prose that describes it and read it against the new reality.
5. **Run verification** (tests / lint / typecheck / build / `git diff --check`).
6. **Re-grep the same terms.** Anything still stale outside contextualized history → fix now.

## Notes
- The grep in step 2 is the whole point. Extra greps cost microseconds; a wasted review round costs minutes plus the reviewer's patience.
- Classic failure: patch the one stale reference the reviewer named, re-issue, and the next round catches three more. The sweep prevents that. (See [adversarial-verification](../../playbook/adversarial-verification.md) and [the Blueprint](../../workflows/the-blueprint.md).)
