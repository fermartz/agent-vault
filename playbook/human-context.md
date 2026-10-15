---
title: "Protect the Human's Context"
type: principle
summary: "Your attention is a context window too. The agent answers short by default, teaches in bites, and gives the deep version only when you ask."
maturity: battle-tested
related-workflows: []
related-skills: [teach-in-bites]
---

# Protect the Human's Context

**The agent reasons worse when its window fills with noise. So do you. Answer short by default, teach one bite at a time, and let the human ask for more.**

## Why

[Protect the Context](./context-hygiene.md) is about the agent's window. This is the same rule
turned around. A ten-paragraph answer floods your working memory the way a dumped log floods the
model's. You skim it, miss the one line that mattered, and stop trusting long answers at all.

Agents are trained to be thorough, so they default to covering everything. Covering everything
feels helpful and reads as exhausting. The human is the slowest part of the loop and the one that
decides, so the human's attention is the scarcest resource in the system. Spend it on purpose.

## In practice

- **Short by default.** One or two paragraphs. Conclusion first, then only what supports it.
- **Offer the deep version, don't deliver it.** "Want the full breakdown?" costs one line. The
  breakdown costs the reader five minutes whether they needed it or not.
- **Ask before going long.** If a topic really needs length, give the short summary and ask.
- **Teach in bites.** One concept per message, then stop and let it land. Move on when the human
  says so. A whole lesson in one message is the human version of one-shotting a whole feature.
- **Complete where completeness is the job.** Plans, specs, scripts and filed pages stay complete.
  Brevity is for answers and status reports, not for artifacts someone will build from.

## Make it stick

Brevity has to apply to every reply, so it belongs in the always-loaded instructions, not in a
skill that loads on demand. Paste this into your `CLAUDE.md` (or `AGENTS.md`):

```markdown
### Answers: 1–2 paragraphs max
Default answer length is 1–2 paragraphs. Summarize by default; I'll ask for more detail if I want
it. If a topic genuinely needs a longer response, either ask permission first or give the short
summary and offer the deep version. This applies to explanations, status reports, and research
answers, not to artifacts whose completeness matters (plans, specs, scripts, filed pages).

### Teaching means small bites
When teaching me something, don't deliver the whole lesson in one message. One concept per
message. After each bite, stop and close with "when you're ready, we continue with <next bite>."
Advance only when I say so.
```

For lessons, use the [teach-in-bites](../skills/teach-in-bites/SKILL.md) skill.

## Receipt

> Long, complete answers were the default for months, and they wore me out. The fix was two short
> rules in the global instructions file, plus a saved feedback memory so the agent kept them across
> sessions. Answers dropped to a paragraph or two, and I ask for depth when I want it, which is
> less often than the agent used to assume. Teaching changed the same way: a lesson on how AI
> models are trained went out in five bites (what a model is, the training game, scale,
> post-training, takeaways), with my own questions in between shaping the next bite. Then it was
> filed as a primer to reread.

## Where it shows up

- Skill: [teach-in-bites](../skills/teach-in-bites/SKILL.md)
- Related principle: [Protect the Context](./context-hygiene.md) (the agent's window; this is yours)
