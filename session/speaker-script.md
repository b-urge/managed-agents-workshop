# Speaker script: Managed Agents session

A 20-minute session in nine slides, with a live demo at slide 7. Times in each heading add up to 19:30, leaving 30 seconds of slack.

## Before the session

The demo is the only part that can fail live, so set it up ahead of time.

**The day before**

- [ ] Run `demo.ipynb` top to bottom once, as a rehearsal.
- [ ] Save that run with its output as `demo_prerun.ipynb` (File → Save Notebook As). This is your fallback if the network fails.

**15 minutes before**

- [ ] Start Jupyter and open `demo.ipynb`. Paste the API key.
- [ ] Run every cell above **Demo starts here**. This creates the agent and environment and uploads the tickets, so the demo opens on the first run.
- [ ] Open `demo_prerun.ipynb` in a second tab.
- [ ] Open the deck in present mode.

**After the session**

- [ ] Run the cell under **After the session** in `demo.ipynb` to archive the demo sessions.

## Part 1 · Why (slides 1–4, 7:00)

### Slide 1 · From your loop to theirs (0:30)

Read the one line under the title out loud. Everything in this session hangs on it: the agent loop, the sandbox, and the history move to Anthropic, and your code keeps one job.

Tell the room what's coming: about 20 minutes, a live demo in the middle, then a 60-minute hands-on lab where they build the thing you demo.

### Slide 2 · You've written this loop (2:00)

Ask: who has written a tool loop against the Messages API? Most hands should go up; this cohort has.

Walk the code top to bottom: call the model, check whether it wants a tool, run the tool, append the result, go again. Then land the two cards. The history lives in your list: you store it and resend it every call. The tools run on your machine: you execute them.

**Say:** "Everything on this slide is code you maintain. Today's question is what happens when you stop maintaining it."

The helper names (`user`, `assistant`, `run_tools`) are shorthand; nobody needs to read them closely.

### Slide 3 · What comes off your plate (1:30)

This slide is slide 2 redrawn: on slide 2, everything was yours. Point at the right side first. The loop, the sandbox, and the event log all moved to Anthropic.

- **The loop:** Anthropic calls the model and decides when to go again.
- **The sandbox:** a real container, so the agent can write a script and run it, not just talk about it.
- **The event log:** every event is stored, so a follow-up message picks up where the last one ended.

Then point at the left side and the arrows: your code talks to the session in events. Read the bottom line. Be honest here: your code doesn't disappear. It still answers custom tool calls, and that's slide 6 and the whole lab.

### Slide 4 · When to reach for it (3:00)

This is the decision slide, so slow down. Walk the three rows left to right.

- **Messages API:** you run everything.
- **Agent SDK:** the same kind of agent harness, but it runs inside your own process and keeps session state on your filesystem.
- **Managed Agents:** Anthropic runs the loop, tools execute in Anthropic's sandbox, and state lives in a hosted event log. The one exception is custom tools, which run in your code; that's slide 6.

Then the box at the bottom, which solutions architects need on day one: because sessions are stateful by design, Managed Agents is currently not eligible for Zero Data Retention or HIPAA BAA coverage. If a customer's agent must touch local files or a private network, point them at the Agent SDK or a self-hosted environment.

**Likely question:** "Why not always use Managed Agents?" **Answer:** data retention requirements, access to local resources, and how much control they want over the runtime.

**Pricing questions:** send people to the pricing page rather than quoting a number from memory.

## Part 2 · How (slides 5–6, 4:30)

### Slide 5 · Agent, environment, session (2:30)

Read the diagram top to bottom. The top row is what you create ahead of time.

- **Agent:** configuration you create once and reuse across many sessions. It carries a version number.
- **Environment:** a container template, meaning which packages are installed and what network access it has. It holds none of your data.
- **Your files:** uploaded once.
- **Session:** one job. All three arrows point into it: it takes the agent, starts a fresh container from the environment, and mounts your files into it.

Then the right side: your app and the session trade events, which is what the demo will show streaming. Read the bottom line and name the mix-up out loud: people assume files belong to the environment because the environment is "where the agent runs." They don't; each session gets its own. It's a common mistake, and the author of this course made it the first time too, so it's a safe one to ask about.

Environments can also be self-hosted; we won't cover that here.

### Slide 6 · Custom tools are a round trip (2:00)

Walk the four steps. Orange rows happen on Anthropic's side; the blue row is your code.

1. The agent decides it needs your tool, for example "look up this customer," and emits an event with the tool name and input.
2. The session goes idle, but the stop reason is `requires_action`, and it lists the calls it's waiting on.
3. Your code runs the lookup and sends back a result event.
4. The agent reads the result and continues.

Then the bottom line: a loop that treats every idle event as "finished" quits at step 2.

**Don't give away the fix.** Lab step 2 has learners hit exactly this on purpose, and step 3 is where they write the answer.

**Likely question:** "What happens if you never answer?" **Answer:** the session waits.

## Part 3 · Show and hand off (slides 7–9, 8:00)

### Slide 7 · Live demo: a support-ticket triage agent (6:00)

Switch to `demo.ipynb`. The setup cells should already have run (see **Before the session**).

**Beat 1 · Run the triage (about 2 minutes).** Run the triage cell. It streams for roughly 25 seconds. Narrate as it goes:

- Lines in brackets like `[read]` are built-in tools running in Anthropic's sandbox.
- Lines starting with `CUSTOM` are the agent asking our notebook for account data.
- The `answered` lines are our code replying.

Point at C-999: our tool returned an error, and the agent kept going and flagged the ticket for a human.

**Beat 2 · Read the ranking (about 2 minutes).** Run the download cell. Point at T-1004 near the top. The customer called it a small thing, but the CRM says it's the biggest account, renewing soon, with its finance team's quarter close depending on the fix. Then T-1003, the all-caps ticket, near the bottom: free plan, cosmetic complaint.

**Say:** "The ranking changed because of data only our code had."

**Beat 3 · Follow up (about 2 minutes).** Run the follow-up cell and point at `lookups this turn: 0`. The session already held the tickets, the account data, and its own ranking. With the Messages API, you would resend all of that yourself.

If the agent does look something up again, that's its choice to re-check; the point stands that you resent nothing.

**If the network fails:** switch to `demo_prerun.ipynb` and walk the same three beats over the saved output.

### Slide 8 · What you get by default (1:00)

These values came back in the agent record when the demo agent was archived; nobody set them.

- **Version:** every agent carries one. Check the docs on how updates are versioned before editing an agent that live sessions use.
- **Effort:** the model's effort level, medium unless you set it.
- **always\_allow:** the one to dwell on. Built-in tools like bash and file writes run without asking for confirmation. That's reasonable in a sandbox, especially with limited networking like the demo uses, but it's a choice to make on purpose.

Don't go deep on permission policies; point people to the docs and move on.

### Slide 9 · Write the part the demo hid (1:00)

Hand off. Everything they saw in the demo, they now build, and the one part they write themselves is step 3, the code that answers the agent.

**Say:** "Step 2 stops on purpose. Read what it tells you before you fix anything."

Point them to the README's troubleshooting table and the hints under step 3 before they ask you. Fast finishers have an optional section: a second tool that needs a human's approval before it runs.
