# Instructor hand-off guide

You're teaching engineers who have used the Messages API to build their first agent on Claude Managed Agents: a 20-minute session with a live demo, then a 60-minute hands-on lab. You don't need to have taught this before. Budget about 90 minutes of prep, one or two days ahead.

## Your prep (about 90 minutes)

1. **Read the deck with the [speaker script](session/speaker-script.md) open (30 min).** The script has what to say on every slide, timings, and the likely questions.
2. **Do the lab yourself (50 min).** Work through [`lab/lab.ipynb`](lab/lab.ipynb) using the hints, not the solution. You'll answer questions far better having hit the same spots learners will. The answer key is [`lab/solutions/lab_solution.ipynb`](lab/solutions/lab_solution.ipynb).
3. **Rehearse the demo (15 min).** Run [`session/demo.ipynb`](session/demo.ipynb) top to bottom once, then save that run with its output as your own `demo_prerun.ipynb`. It's your fallback if the network fails.

**Setup:** Python 3.10 or newer, then `pip install -r lab/requirements.txt`. You need an Anthropic API key with Managed Agents access. **Confirm before the day that learners' keys have Managed Agents access too.** It's the one thing you can't fix in the room.

## The three ideas to land

- **Agent, environment, session.** The agent and environment are created once; each job is a session. Files attach to the session, not the environment. Nearly everyone mixes this up at first.
- **A custom tool is a round trip.** The agent calls your tool, the session pauses with `requires_action`, your code sends back a result, and the session resumes. Idle doesn't mean done.
- **Sessions keep state.** A follow-up message uses everything the session already holds, with nothing resent.

## Where learners get stuck

| What happens | What to do |
|---|---|
| Preflight says "that's the key's ID" | They copied the key's ID from the Console list. They need to create a new key and copy the `sk-ant-` value. |
| Step 2's loop stops at the first lookup | **That's intended. Don't fix it for them.** Ask what the output says the session is waiting for. |
| Stuck on step 3 | Point them to the hints in order. Hint 2 shows the exact shape of a result. |
| "Some calls were answered more than once" | Hint 3: the session re-lists calls it hasn't processed yet, so skip IDs already answered. |
| Step 3 breaks on the unknown customer (C-999) | Their `lookup_account` must return a dict with an `"error"` key. Instruction 1 explains why. |
| "The agent says it wrote the file, but it's not here" | Output stays in the sandbox until the download cell runs. |
| `Environment ... is archived` | They ran step 6's final cleanup lines early. The fix is in the troubleshooting table in [`lab/README.md`](lab/README.md). |

## Questions you'll get

- **"Why not the Agent SDK?"** The SDK runs the agent loop in your own process and keeps state on your filesystem. Managed Agents runs it for you, in Anthropic's sandbox, with a hosted event log.
- **"Can we use it with regulated data?"** Managed Agents is currently not eligible for Zero Data Retention or HIPAA BAA coverage.
- **"What does it cost?"** Send people to Anthropic's pricing page rather than quoting a number.
- **"What if my code never answers a tool call?"** The session waits.

## Timing and pacing

A pilot tester new to Managed Agents finished the lab in 40 minutes. Fast finishers have an optional power user section at the end: a second tool that needs a human's approval before it runs. Nobody needs it to finish.

## If something breaks

Managed Agents is in beta. The lab was tested in September 2026 with the package versions in [`lab/requirements.txt`](lab/requirements.txt), the `claude-opus-5-5` model, and the `agent_toolset_20260401` toolset. If a cell fails in a way the troubleshooting table doesn't cover, check the installed SDK version against `requirements.txt` first.
