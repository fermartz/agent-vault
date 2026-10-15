---
name: skill-builder
description: "Turn something the user does over and over with an agent into a reusable SKILL.md: capture the real workflow from the conversation (or interview the user one question at a time when there's nothing to extract), write the skill with a description that triggers, strip anything private, run the checks, get a second agent to review it, and install it. Use when the user says 'make this a skill', 'turn this into a skill', 'add this to my skills', 'write a skill for X', 'help me make a skill', 'publish this workflow', or after a workflow has been repeated enough that it should be written down, even if they don't say the word skill."
metadata:
  version: 0.10.0
  maturity: working
  related-playbook: [adversarial-verification, least-privilege, human-context]
  related-skills: [code-review]
  tags: [skills, authoring, agents, review]
---

# skill-builder

A skill is a workflow you stopped explaining. Write it down once, the way you actually do it, and
every future agent starts from there instead of from zero. These are the rules this repo's skills
were written under, and the mistakes that cost review rounds along the way.

## Requirements

Only for the checker script: Python 3.10+ and PyYAML.

| Tool | Check | Install |
|---|---|---|
| Python 3.10+ | `python3 -c 'import sys; assert sys.version_info >= (3, 10)'` | `brew install python` / `sudo apt install python3` (3.10+; older distros need a newer Python) |
| PyYAML | `python3 -c "import yaml"` | `python3 -m pip install pyyaml`; if your system Python refuses ("externally managed"), use a virtualenv (on Debian/Ubuntu first `sudo apt install python3-venv`): `python3 -m venv ~/.venvs/skills && ~/.venvs/skills/bin/pip install pyyaml`, then run the checker with `~/.venvs/skills/bin/python` |

**Check before the first run.** Run the check command. If anything is missing, tell the user exactly what and the install command, and **ask before installing anything**: installing changes their machine ([Hand Over Keys, Not the Keyring](../../playbook/least-privilege.md)). On Windows, use WSL or the commands in [getting started](../../docs/getting-started.md#windows).

## 1. Start from the real thing

- **Extract, don't invent.** The best source is a conversation where the work was just done: the
  steps in order, the tools, and above all the **corrections** the user made ("the file date is
  wrong, it was last week's call"). Corrections are the parts no tutorial has.
- One skill, one job. If the description needs "and also", it's two skills; let one call the other
  (a meeting skill calls a transcription skill).
- Ask the user only what the conversation can't answer.

### Guided mode: when there's nothing to extract

If the user arrives with an idea and no conversation behind it ("I want a skill for X"), interview
them. **One question per message**, wait for the answer, and let each answer shape the next
question ([Protect the Human's Context](../../playbook/human-context.md)):

1. **The job.** "In one sentence, what should this skill get done?"
2. **The trigger.** "What would you actually type when you want it? Give me two or three ways you'd
   say it." These become the description.
3. **The last time.** "Walk me through the last time you did this by hand, step by step." This is
   the procedure. If they've never done it, say so: the skill starts as `experimental`.
4. **What goes wrong.** "Where does it usually break, or what do people get wrong?" These become
   the notes, and they're usually the most valuable part.
5. **The stakes.** "Does it spend money, touch passwords, keys or accounts, or publish anything?" A yes
   makes it high-stakes: section 3's safety rules apply and the review is XL (section 6).
6. **Done looks like.** "How will you know it worked?" This becomes the last step, and the test.

Skip any question the user already answered. Then play the skill back in five lines (job, trigger,
steps, risks, done) and get a yes before writing the file.

## 2. Write the SKILL.md

```
skills/<name>/
├── SKILL.md            required
├── references/         long material, loaded only when the skill points to it
└── scripts/            code the skill runs instead of rewriting it each time
```

**Frontmatter.** `name` (equals the folder) and `description` at the top level; everything else
under `metadata:`:

```yaml
---
name: <folder-name>
description: "<what it does>. Use when the user says '<phrase>', '<phrase>', or <situation>, even if <the case where they don't name it>."
metadata:
  version: 0.1.0
  maturity: experimental | working | battle-tested
  related-workflow: <workflow-slug>          # if it's the executable twin of a workflow
  related-playbook: [<principle-slugs>]
  related-skills: [<skill-names>]
  tags: [<tags>]
---
```

**The description decides whether the skill ever runs.** Agents tend to under-use skills, so make it
a little pushy: what it does, the exact phrases people say, and the situation where they won't name
it. The description must carry every trigger on its own; a short "When to use" section in the body
is fine for nuance (and for when *not* to use it), but the agent only sees the body after choosing
the skill.

**The body**, in this order: one paragraph on why the skill exists (link the principle it applies);
a **Requirements** section if it needs any tool beyond git (a table with the check and install
commands, and the rule to check before the first run and ask before installing); the procedure as
numbered steps; notes; and a "Never" list only if the skill touches money, secrets
or anything public. Explain the reason behind a rule instead of shouting it: an agent that knows
*why* handles the case the rule didn't foresee. Keep it under ~500 lines; move long reference
material to `references/` and say when to read it.

**Bundle repeated work.** If every run would write the same helper, write it once in `scripts/`
and have the skill call it by a path relative to the skill folder, never your home directory.

## 3. Make it safe to share

- **No private details.** No client or people's names, prices from real work, account or zone IDs,
  personal paths. Examples are anonymized: "a 23-minute client call", not who it was with.
- **Skills that touch providers** follow [Hand Over Keys, Not the Keyring](../../playbook/least-privilege.md):
  secrets never pass through the agent, cost check before anything billable, a human yes before
  anything public or irreversible.
- A personal copy can keep its private specifics (your own paths, your own projects). The shared
  copy is the generic one; sync the scripts between them, not the prose.

## 4. Maturity and version, honestly

| maturity | means | version |
|---|---|---|
| experimental | written, not yet run for real | 0.x |
| working | the practice has run for weeks; the written form is new | 0.x |
| battle-tested | used repeatedly on shipped work, in this written form | 1.0.0+ |

A changed procedure bumps the minor version; a wording fix bumps the patch.

## 5. Wire it in

- Every principle in `related-playbook` links back: the skill appears in that principle's
  `related-skills` and under "Where it shows up".
- The skills README gets one row; the main README's counts stay true.
- If it's the executable twin of a workflow, each links the other.

## 6. Check, then get a second opinion

1. Run the checks: `python3 <this-skill-folder>/scripts/check_skills.py <repo> --deny-file <private-words.txt>`
   (inline links, skill frontmatter, the version policy, and every private word you list; keep that
   list outside the repo). It reports where a private word is, never the line, so the output is safe
   to paste into a review. It's a first pass, not proof: read the diff too.
2. **A different agent reviews it**, per [Don't Grade Your Own Homework](../../playbook/adversarial-verification.md).
   A new skill is at least an L change; one that is **high-stakes** (spends money, touches secrets,
   keys or accounts, or publishes anything) is XL. Tell the
   reviewer to read the scripts as code, not prose: a review of what looked like a documentation
   move found three real bugs in a bundled transcription script.
3. The user reads it before it's committed. They know when an example is too close to a real client.

## 7. Install and test

- Copy the folder to `.claude/skills/` (one project) or `~/.claude/skills/` (everywhere); the agent
  lists it once installed.
- Test with two or three prompts a real user would type, including one where they don't name the
  skill. For formal evals, benchmarks and description tuning, Anthropic's `skill-creator` does that
  well; this skill is about writing one worth testing.
