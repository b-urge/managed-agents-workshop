"""Plumbing for the Managed Agents triage lab.

The lab notebook keeps the concepts in view (agents, sessions, the custom tool
round trip). The code here handles the parts that aren't the lesson: checking
your setup, printing events readably, and downloading output files.
"""

import os
import platform
import sys
import time
from pathlib import Path

MANAGED_AGENTS_BETA = "managed-agents-2026-04-01"


def preflight(tickets_path="tickets.json"):
    """Check everything the lab needs and print one line per check.

    Returns True if every check passed.
    """
    results = []

    def report(passed, label, fix=""):
        results.append(passed)
        print(("✓ " if passed else "✗ ") + label + ("" if passed or not fix else f"\n    Fix: {fix}"))

    # Python version
    report(
        sys.version_info >= (3, 10),
        f"Python {platform.python_version()}",
        "The lab needs Python 3.10 or newer.",
    )

    # Anthropic SDK
    try:
        import anthropic
    except ImportError:
        report(False, "Anthropic SDK installed", "Run: pip install anthropic")
        return False
    report(True, f"Anthropic SDK {anthropic.__version__}")

    # API key format
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        report(False, "API key set", "Run the key cell above and paste your key.")
    elif key.startswith("apikey_"):
        report(
            False,
            "API key set",
            "That's the key's ID, not the key. Create a key in the Console and copy "
            "the value that starts with sk-ant- (it's shown only once).",
        )
    elif not key.startswith("sk-ant-"):
        report(False, "API key set", "Anthropic API keys start with sk-ant-. Check what you pasted.")
    else:
        report(True, "API key set")

    # Lab data
    report(
        Path(tickets_path).exists(),
        f"{tickets_path} found",
        "Keep tickets.json in the same folder as this notebook.",
    )

    # Managed Agents access (a cheap, read-only call)
    if key.startswith("sk-ant-"):
        client = anthropic.Anthropic()
        try:
            client.beta.sessions.list(limit=1)
            report(True, "Managed Agents API reachable with this key")
        except anthropic.AuthenticationError:
            report(False, "Managed Agents API reachable", "The key was rejected. Create a new key and paste it again.")
        except anthropic.PermissionDeniedError:
            report(False, "Managed Agents API reachable", "This key's organization doesn't have Managed Agents access.")
        except anthropic.APIConnectionError:
            report(False, "Managed Agents API reachable", "Couldn't reach api.anthropic.com. Check your network or VPN.")
        except Exception as e:  # anything unexpected: show it rather than hide it
            report(False, "Managed Agents API reachable", f"{type(e).__name__}: {e}")

    passed = all(results)
    print("\nReady to go." if passed else "\nFix the ✗ lines above, then run this cell again.")
    return passed


def print_event(event):
    """Print one session event in a readable form. Ignores event types the lab doesn't use."""
    if event.type == "agent.message":
        for block in event.content:
            if block.type == "text":
                print(block.text, end="")
    elif event.type == "agent.tool_use":  # built-in tools: bash, read, write, edit...
        print(f"\n[{event.name}] {str(event.input)[:120]}")
    elif event.type == "agent.custom_tool_use":  # tools your code answers
        print(f"\n[CUSTOM {event.name}] {event.input}")


def download(client, session_id, filename, dest_dir=".", attempts=5, wait_seconds=3):
    """Download one file the agent wrote to /mnt/session/outputs/.

    Output files can appear a few seconds after the agent finishes, so this
    retries before giving up. Returns the local Path.
    """
    for _ in range(attempts):
        files = client.beta.files.list(scope_id=session_id, betas=[MANAGED_AGENTS_BETA])
        match = next((f for f in files.data if f.filename == filename), None)
        if match:
            path = Path(dest_dir) / filename
            path.write_bytes(client.files.download(match.id).read())
            return path
        time.sleep(wait_seconds)
    found = [f.filename for f in files.data]
    raise FileNotFoundError(
        f"{filename} isn't in this session's outputs. Files found: {found}. "
        "Did the agent save it to /mnt/session/outputs/?"
    )
