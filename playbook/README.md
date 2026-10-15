# Playbook — the *why*

The principles behind how I work with AI agents. Each page is a short, quotable conviction:
the belief, why I hold it, how it shows up in practice, and a real receipt. Workflows and skills
point back up to these.

| Principle | The belief in one line |
|---|---|
| [Give the Agent a Memory](./memory-system.md) | Context is precious and resets. Durable knowledge belongs in files, not the chat. |
| [A Plan Is a Contract, Not a Spec](./plan-build-review.md) | Plan the *what* and *why*. Leave *how* to the code. |
| [Don't Grade Your Own Homework](./adversarial-verification.md) | The model that built it is the wrong one to judge it. Use a different model to attack it. |
| [Protect the Context](./context-hygiene.md) | An agent reasons best with a small, relevant window. One slice at a time. |
| [Synthesize When You Write, Not When You Search](./write-time-synthesis.md) | Fold each source into the pages it affects when it arrives, so knowledge compounds instead of being re-searched. |
| [Hand Over Keys, Not the Keyring](./least-privilege.md) | An agent that runs your ops holds real keys. Scope them, keep secrets out of the chat, ask before anything billable or irreversible. |
| [Protect the Human's Context](./human-context.md) | Your attention is a window too. Short by default, teach in bites, deep only on request. |

*More principles get added as I write them down — section-by-section, smallest-clean-change, code-wins-over-docs, build-in-public.*

### Conventions

| Convention | What it standardizes |
|---|---|
| [Keep the Agent's Brain in One Folder](./the-agent-folder.md) | Put all working files (memory, map, tasks, decisions, plans, reviews) in one tool-agnostic `.agent/` directory. |

Back to [the vault](../README.md).
