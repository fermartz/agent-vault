# Starter SCHEMA.md

Copy this into the wiki's root as `SCHEMA.md`, change what doesn't fit, and point the agent's
instruction file (`CLAUDE.md` / `AGENTS.md`) at it. Keep `schema_version:` in both files and bump it
on every schema change. Grow it from real friction: add a type, tag or lint check when you feel its
absence, not before.

---

```
schema_version: 1
```

## Folders

```
raw/            evidence, never rewritten
  articles/     web pages, posts
  papers/       PDFs, papers
  transcripts/  meetings, calls, videos
  pastes/       anything pasted in
  journal/      one file per day: YYYY-MM-DD.md, timestamped self-reports
entities/       people, projects, products, organizations
concepts/       topics, techniques, ideas
comparisons/    side-by-side analyses
queries/        filed answers to substantial questions, lessons
summaries/      overviews across many pages (e.g. now.md: current focus, active projects, open loops)
tasks/          one open loop per file
_archive/       superseded pages and done tasks; slugs stay reserved forever
index.md        every live page, one line each, grouped by type
log.md          every change, one line each
SCHEMA.md       this file
```

## Page frontmatter

```yaml
---
title: <human-readable title>
slug: <lowercase-kebab, equals the filename without .md>
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary | task
tags: [<1–6 from the tag list>]
confidence: high | medium | low
sources: [<paths to raw files>]          # optional but expected
status: active | paused | done | abandoned  # optional; projects and goals
---
```

Task pages add:

```yaml
status: waiting | my-turn | scheduled | done
project: <slug of the page it belongs to>
waiting_on: <who>          # when waiting
due: YYYY-MM-DD            # optional
```

Body: 1–5 lines. When done: one-line outcome, then move to `_archive/` after 14 days.

## Raw frontmatter

```yaml
---
title: <title>
source_url: <url or ~>
author: <author or ~>
ingested: YYYY-MM-DD
---
```

Journal entries: `## HH:MM — <short label>` (take the time from the clock, don't estimate), and link
every person and project with `[[slug]]` at first mention.

## Links

`[[slug]]` for every link between pages: slug only, no path, no `.md`. Normal markdown links for the
web. A slug that was ever used, including in `_archive/`, is never reused.

## Tags

A closed list. Adding a tag means editing this file first. Start small, for example:
`project, person, work, business, finance, health, learning, ai, tool, reference`.

## Rules

- **Raw:** create, or append to today's journal. Never rewrite a raw body. Metadata typo fixes are
  allowed and logged.
- **New page** only when 2+ sources cover the subject or one source is about it.
- **Contradictions:** keep both positions with dates and sources; add `contradictions: [slug]`.
- **Every change** updates `index.md` (new pages) and `log.md` (one line per file).

## Lint checklist (report only, never auto-fix)

Scope: every page in the type folders and `_archive/`; `raw/` is checked only for broken links.

1. Broken `[[links]]` (a slug in `_archive/` counts as resolving).
2. Filename ≠ slug, or duplicate slugs (including `_archive/`).
3. Missing required frontmatter; tags outside the list; type ≠ folder (pages in `_archive/` keep
   their type and are exempt).
4. Live pages missing from `index.md`, or index lines with no page. `_archive/` is not indexed.
5. Orphans: live pages no other page links to (`index.md` and `log.md` don't count).
6. Pages with no outbound `[[link]]`. Two is the target, not a rule: never add filler links. A task
   page needs only the link to its `project:`.
7. Pages flagged with `contradictions:`.
8. Open tasks not updated in 14 days, or past their `due:`.
9. Done tasks still in `tasks/` after 14 days.
10. Active projects whose page hasn't changed in 14 days.
11. The status page (e.g. `summaries/now.md`) older than the newest page in the wiki.
12. `schema_version:` mismatch between this file and the instruction file (stop and ask).
