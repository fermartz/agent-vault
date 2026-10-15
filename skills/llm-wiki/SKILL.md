---
name: llm-wiki
description: "Run a personal knowledge wiki in plain markdown + git that the agent maintains: ingest sources (links, papers, pastes, meeting transcripts, 'I did X today') into raw evidence plus linked pages, answer questions from the pages, and lint the whole thing. Use when the user says 'ingest this', 'add this to the wiki', 'save this', 'what does the wiki say about X', 'lint the wiki', 'set up a wiki / second brain / knowledge base', or shares a source or a fact about their projects in a repo that has a SCHEMA.md and index.md."
metadata:
  version: 0.10.0
  maturity: working
  related-workflow: llm-wiki
  related-playbook: [write-time-synthesis, memory-system, human-context]
  related-skills: [meeting-to-notes, video-transcript]
  tags: [knowledge, wiki, memory, notes, markdown, agents]
---

# llm-wiki

The executable twin of [The LLM Wiki](../../workflows/llm-wiki.md). Raw sources are evidence; pages
are where the synthesis lives; `index.md` and `log.md` are the backbone. The thinking happens at
ingest, per [Synthesize When You Write](../../playbook/write-time-synthesis.md).

## Requirements

| Tool | Check | Install |
|---|---|---|
| git | `git --version` | `brew install git` / `sudo apt install git` |
| qmd (optional, better search) | `qmd --version` | see [its README](https://github.com/tobi/qmd); without it, search falls back to grep + `index.md` |

**Check before the first run.** Run the check command. If anything is missing, tell the user exactly what and the install command, and **ask before installing anything**: installing changes their machine ([Hand Over Keys, Not the Keyring](../../playbook/least-privilege.md)). On Windows, use WSL or the commands in [getting started](../../docs/getting-started.md#windows).

## Startup (every session, before any operation)

1. Read `SCHEMA.md`, the contract. If the instruction file and `SCHEMA.md` disagree on a
   `schema_version:`, stop and ask. The schema wins on any schema question.
2. Skim `index.md` (what exists) and the last ~30 lines of `log.md` (what happened lately).
3. If git has commits from elsewhere (another machine, a scheduled job), pull before writing.

**No wiki yet?** Create one from [references/starter-schema.md](./references/starter-schema.md):
the folders, `SCHEMA.md`, an empty `index.md` and `log.md`, and a short instruction file pointing at
the schema. Commit it.

## Ingest

1. **Capture the raw source.** URL, file or paste → `raw/<kind>/<slug>.md` with provenance
   frontmatter. Self-report → append `## HH:MM — <label>` to today's `raw/journal/YYYY-MM-DD.md`
   (take the time from the clock), linking every person and project with `[[slug]]`. Recordings go
   through [meeting-to-notes](../meeting-to-notes/SKILL.md); social videos through
   [video-transcript](../video-transcript/SKILL.md).
2. **Give the takeaways in a few lines and confirm** before writing pages. Skip the confirmation for
   plain facts the user just stated.
3. **Find every page it touches.** Index first, then search (see below). List them before editing:
   one source usually affects several pages.
4. **Write.** Update existing pages; create a page only when 2+ sources cover the subject or this
   source is about it. Link both ways. Add the raw path to `sources:`. Bump `updated:`. Conflicts:
   keep both positions with dates and set `contradictions:`; never silently overwrite.
5. **Open loops.** Anything waiting on someone, or owed by the user, becomes a task page with a
   status, and a line on the status page if the wiki has one. Resolved loops: `status: done` plus a
   one-line outcome.
6. **Hub sweep.** A person or project that changed state: update the pages that summarize it
   (owner page, status page) now.
7. **Backbone.** One `index.md` line per new page (in its section, alphabetical), one `log.md` line
   per changed file.
8. **Commit** with an explicit file list (`git status` first; leave out anything unexpected and say
   so), then refresh the search index if there is one.
9. **Report** the changed files, one line each.

## Query

1. Index → search → open the pages. Read the page before citing it; a search snippet is not a source.
2. Answer short, citing `[[slug]]` for each claim.
3. File the answer to `queries/` only if it's substantial: it spans several pages, makes a new
   comparison, or is worth rereading. Then index and log it like any page.

## Lint

Run every check in the schema's lint list. Report grouped by check, one line per finding with the
file. **Never fix during lint.** Ask which findings to act on, then act only on those.

## Search, cheapest first

1. Exact names, slugs, IDs, numbers → `grep -rn` / `rg`.
2. Questions → local hybrid search if installed (keywords + meaning + rerank, e.g.
   [qmd](https://github.com/tobi/qmd)); write the keyword and meaning sub-queries yourself.
3. Escalate only when the top hit is weak. If the search tool is missing or stale, fall back to
   grep + `index.md`.

## Things that look helpful and aren't

- **Pages for passing mentions.** They fragment the wiki; a line on an existing page is enough.
- **Filler links** to hit a link count. Links should be real connections.
- **Rewriting raw files** to fix a typo in what someone said. Put the correction on the page.
- **Leaving research in the chat.** If it was worth doing, it's worth filing now.
- **Long answers.** The wiki holds the depth; the answer points to it.
