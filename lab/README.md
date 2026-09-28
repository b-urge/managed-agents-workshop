# Claude Managed Agents lab: support-ticket triage

Build an agent that ranks a queue of support tickets, using account data that only your code can provide. The agent works in Anthropic's sandbox; your notebook answers it when it asks for customer data.

**Time:** about 55 minutes  
**For:** engineers who have called an LLM API but haven't built on Managed Agents

## What's here

| File | What it is |
|---|---|
| `lab.ipynb` | The lab. Start here. |
| `requirements.txt` | The exact package versions the lab was tested with |
| `helpers.py` | Setup checks, event printing, and file downloads, kept out of the notebook so the concepts stay in view |
| `tickets.json` | The eight support tickets the agent triages |
| `solutions/lab_solution.ipynb` | The completed lab, for instructors |

## Before you start

You need Python 3.10 or newer (tested on 3.14) and an Anthropic API key with Managed Agents access. Create a key at [platform.claude.com/settings/keys](https://platform.claude.com/settings/keys) and copy it right away: the Console shows the full key only once.

## Setup

From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

`requirements.txt` pins the exact package versions this lab was tested with. Managed Agents is in beta, so a newer SDK may change behavior; install from the file rather than upgrading.

Open `lab.ipynb` and run the preflight in step 0. It checks everything the lab needs and tells you what to fix.

Leave the terminal window open while you work. Closing it stops Jupyter. Next time, start again with:

```bash
source .venv/bin/activate && jupyter lab
```

## Troubleshooting

| What you see | What to do |
|---|---|
| Preflight says "That's the key's ID, not the key" | You copied the key's ID (`apikey_...`) from the Console's key list. Create a new key and copy the value that starts with `sk-ant-`. |
| `AuthenticationError` | The key was rejected. Create a new key and paste it again. |
| `PermissionDeniedError` | This key's organization doesn't have Managed Agents access. |
| `command not found: jupyter` | Activate the environment first: `source .venv/bin/activate`. |
| The browser says it can't connect to Jupyter | The terminal running Jupyter was closed. Start it again from this folder. |
| Step 2's loop stops at the first lookup | That's the point of step 2. Step 3 fixes it. |
| A cell never finishes after the agent asks for a lookup | Your `requires_action` branch didn't answer every call the session is waiting on. See hint 1 in step 3. |
| "Some calls were answered more than once" | The session re-lists calls it hasn't processed yet. Skip IDs you've already answered (hint 3). |
| The agent says it wrote a file, but it's not in this folder | Output files stay in the sandbox at `/mnt/session/outputs/` until you download them. Run the `helpers.download` cell. |
| `FileNotFoundError` from `helpers.download` | Files can take a few seconds to appear. Run the cell again. If it still fails, check the agent saved to `/mnt/session/outputs/`. |
| `SyntaxError` after copying a sample solution | You copied the explanation along with the code. Copy only the code block. |
| `Environment ... is archived` | You ran the final cleanup lines in step 6. Run `del environment, agent` in a new cell, then run the step 1 agent and environment cells again. |

## Learn more

- [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)
- [Managed Agents cookbooks](https://github.com/anthropics/claude-cookbooks/tree/main/managed_agents)
