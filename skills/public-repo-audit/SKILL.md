---
name: public-repo-audit
description: "Audit an entire public repository the way a skeptical senior engineer (or a recruiter evaluating a hire) would read it. Grade code quality, security, tooling rigor, tests, and hygiene; report findings with severity + file:line. Use when the user says 'audit this repo', 'review the whole codebase', 'is this repo interview-ready', or wants a public repo hardened before sharing."
metadata:
  version: 1.0.0
  maturity: battle-tested
  related-workflow: the-blueprint
  related-playbook: [adversarial-verification]
  tags: [audit, code-review, security, ci, tests, hygiene, public-repo]
---

# public-repo-audit

Read the whole repo as a **skeptical external engineer** would: someone deciding whether this
person is worth hiring, or whether this library is worth trusting. Your job is to find what *caps
the impression* in the first ten minutes, not to be encouraging. Assume the reader is sharp.

## When to use

The user says "audit this repo", "review the whole codebase", "is this interview-ready", or wants
a public repo hardened before it's shared. **Not** for a single diff — use [code-review](../code-review/SKILL.md) for that.

## Scope

Only files that ship: run `git ls-files` and audit tracked files. Ignore `node_modules`, build
output, and gitignored files. Read files fully before judging.

## Dimensions to audit

1. **Security & secrets** — scan tracked files for committed secrets (`.env`, keys, tokens,
   `sk-`, PRIVATE KEY, cloud creds). Check `.gitignore` correctness and how credentials are
   handled at runtime. State explicitly whether the repo is secret-clean.
2. **Tooling & CI rigor** — is there CI that *gates* quality (lint + typecheck + test + build) on
   push/PR, or just a vanity badge? Does lint actually cover the source (not a no-op)? Type-config
   strictness. `npm audit` / dependency health (separate dev-only from production exposure).
3. **Licensing & metadata** — LICENSE present? package metadata (description, author, repo, license)?
   (A public repo with no license reads as an oversight.)
4. **Language/stack quality** — adapt to the stack: type safety (`any`, strict mode), memory
   safety and lint for systems languages (e.g. `cargo clippy -D warnings`), idioms, error handling.
5. **Correctness** — real bugs, race conditions, resource cleanup (intervals/listeners/handles/
   subprocesses), effect-dependency hygiene, unhandled rejections.
6. **Duplication & dead code** — repeated logic that wants an abstraction; unused files/exports.
7. **Tests** — are they behavioral or trivial smoke tests? Is the *riskiest* logic actually
   covered, or does a high count hide uncovered core paths (false confidence)?
8. **Accessibility** (if there's a UI) — focus states, keyboard operability, semantic markup, aria.
9. **Docs & self-consistency** — README accuracy vs reality; does the code honor the project's own
   stated decisions/principles (grep the docs, flag drift)?
10. **The impression** — what would a senior engineer conclude about rigor from the scaffolding alone?

## How to run (scale to the repo)

- Small repo: one careful pass.
- Large / multi-language repo: **fan out parallel reviewers by area** (e.g. frontend, backend/
  systems, build+CI+security) and synthesize. Each reads its slice fully.
- **Verify before reporting.** Run an independent adversarial pass over the findings and drop any
  that don't hold up (see [adversarial-verification](../../playbook/adversarial-verification.md)).
  An unverified finding wastes the owner's time and burns trust.
- **Do not modify files.** Audit only; the owner decides what to fix.

## Output

1. A one-paragraph honest **verdict + letter grade.**
2. **Confirm secret-free** (or list hits) explicitly.
3. Findings grouped by dimension, each with **SEVERITY (HIGH/MED/LOW), file:line, the issue, and a
   concrete fix.**
4. A separate **"what's done right"** list, so the grade is fair.
5. Prioritized **order of attack** (biggest signal-per-effort first).

## Notes
- This is [The Blueprint](../../workflows/the-blueprint.md)'s review lens applied at *repo* scale.
- The highest-leverage findings on a public repo are usually the cheap ones: missing LICENSE,
  no real CI, a lint step that lints nothing. Fix those first; they shape the whole impression.
