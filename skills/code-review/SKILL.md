---
name: code-review
description: "Adversarially review an uncommitted diff (or a PR) for bugs, spec compliance, missing tests, security, scope creep, and overengineering. Output APPROVED or REQUEST_CHANGES with concrete findings. Use when the user says 'review this', 'review the diff', 'code review', or as the review step in the Blueprint."
version: 0.1.0
maturity: battle-tested
related-workflow: the-blueprint
related-playbook: [adversarial-verification]
metadata:
  tags: [code-review, verification, bugs, security, agents]
---

# code-review

Adversarially audit a change. Your job is **not** to be encouraging; it's to find what's wrong.
Default to **REQUEST_CHANGES** when you're unsure. (See [adversarial-verification](../../playbook/adversarial-verification.md).)

## When to use

The user says "review this" / "review the diff" / "code review", or you're the review step of the
[Blueprint](../../workflows/the-blueprint.md). **For best results, run as a *different* model than
the one that wrote the code** — a builder can't see its own blind spots.

## How to review

1. Get the scope: the uncommitted diff (`git diff` / `git diff --staged`) or the PR. Read changed
   files fully where the diff lacks context. If a plan exists, read it and check the diff against it.
2. Audit each dimension:
   - **Spec compliance** — does it do what the plan/task said? Anything missing?
   - **Bugs / regressions** — logic errors, edge cases, null/async/race issues, wrong event targets, off-by-one.
   - **Missing tests/checks** — is the risky logic actually covered, or is the green suite false confidence?
   - **Security & validation** — secrets, injection, authz, unvalidated input, leaked credentials.
   - **Overengineering** — abstractions for hypothetical needs, handling for impossible cases.
   - **Scope creep** — changes beyond what the task called for.
3. **Do not modify files.** Review only.

## Output

A one-line verdict first, then findings:

```
APPROVED — <one-line summary>
```
or
```
REQUEST_CHANGES — <one-line summary>
```
For REQUEST_CHANGES, list each finding with **severity (HIGH/MED/LOW), file:line, the issue, and a
concrete fix.** Be specific — cite real lines, not vibes. List what's done *right* separately so the
verdict is fair.

## Notes
- Skepticism is the value. "Looks fine" is not a review.
- If verifying a claim or finding (not code), the same stance applies: try to refute it; assume it's wrong until it survives.
