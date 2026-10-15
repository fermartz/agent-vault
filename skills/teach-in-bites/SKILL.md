---
name: teach-in-bites
description: "Teach the user a concept, technology, course chapter or codebase one bite at a time: plan the bites, deliver one, stop, and continue only when the user says so; answer side questions in between; file the finished lesson as a primer. Use when the user says 'teach me', 'explain how X works', 'walk me through', 'I want to learn', or continues a course."
metadata:
  version: 0.1.0
  maturity: working
  related-playbook: [human-context]
  tags: [teaching, learning, communication, agents]
---

# teach-in-bites

Teach the way a good tutor talks: one idea, a pause, the next idea. The human sets the pace. This is
[Protect the Human's Context](../../playbook/human-context.md) applied to learning.

## When to use

- The user asks to be taught or to understand something: "teach me X", "how does X work", "walk me
  through Y".
- A course or series is in progress and the user says "go", "next", or "continue".

Not for a quick factual question. That gets a short answer, not a lesson.

## Procedure

1. **Source the material.** If notes, docs or a repo cover the topic, read them first and teach from
   them. Otherwise teach from what you know, and say where you're unsure.
2. **Plan the bites, don't show the plan.** Split the topic into 3 to 6 bites, each one idea (e.g.
   setup → the core mechanism → scale or edge cases → the payoff → takeaways). Keep the list to
   yourself, except to name the next bite.
3. **Deliver one bite.** Two or three short paragraphs at most. Start from first principles, not from
   comparisons to something else. Use one concrete example, ideally from the user's own world.
4. **Stop.** Close with one line: "When you're ready, we continue with <next bite>." Don't continue
   until the user signals.
5. **Handle what comes back.**
   - *A check of understanding* ("so it's basically X?"): confirm what's right, then add the one
     nuance that matters. Don't re-teach the bite.
   - *A side question:* answer it short, then point back to the next bite.
   - *"Go":* deliver the next bite.
6. **Takeaways last.** The final bite is a short recap plus what the topic explains in the user's
   daily work.
7. **File the lesson.** Once the last bite is out, save the whole lesson (all bites plus the side
   questions worth keeping) wherever the user keeps notes, as a primer they can reread. If the user
   asks, save each bite as it goes.

## Notes

- Bites are about attention, not about holding back. If the user asks for the whole thing at once,
  give it.
- Never invent precise numbers to make a bite feel complete. "Not published" is an answer.
- The user's interruptions are the best signal for what the next bite should cover. Adjust the plan.
