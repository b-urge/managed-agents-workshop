# Claude Managed Agents: enablement workshop

A workshop that takes engineers who have used the Messages API to building their first agent on Claude Managed Agents. It has a 20-minute session with a live demo, a 60-minute hands-on lab, and a hand-off guide for the instructor who teaches it.

In the lab, learners build a support-ticket triage agent. The agent works in Anthropic's sandbox, and learners write the code that answers it when it needs account data only their system has.

## The four deliverables

| Deliverable | Where |
|---|---|
| **Session** (20 min, presented live) | [Live deck](https://claude.ai/artifact/72hUiY2Dsaw3PeBKLi5ty9) · [`session/session.pdf`](session/session.pdf) · [`session/speaker-script.md`](session/speaker-script.md) · [`session/demo.ipynb`](session/demo.ipynb), with [`demo_prerun.ipynb`](session/demo_prerun.ipynb) as the offline fallback |
| **Lab** (60 min, self-guided) | [`lab/`](lab/). Start with its [README](lab/README.md), then [`lab.ipynb`](lab/lab.ipynb). The answer key is in [`lab/solutions/`](lab/solutions/). |
| **Instructor hand-off guide** | [`handoff-guide.md`](handoff-guide.md) |
| **Design note** | [`design-note.md`](design-note.md), with [`design-log.md`](design-log.md) as the record behind it |

## Where to start

1. Page through the deck, reading the speaker notes, to see what the cohort hears first.
2. Open [`lab/lab.ipynb`](lab/lab.ipynb) to see what they build. It reads fine on GitHub without running it.
3. Read the [design note](design-note.md) for the decisions behind both, including what I changed from Claude's drafts.

## Testing

The lab and demo were run end to end against the live API. One pilot tester, an engineer new to Managed Agents, completed the lab in 50 minutes without help. The package versions the lab was tested with are pinned in [`lab/requirements.txt`](lab/requirements.txt).
