# Design note

I built a workshop that takes engineers who have used the Messages API to shipping a first agent on Claude Managed Agents. It's one scenario from start to finish: a support-ticket triage agent that runs in Anthropic's sandbox and asks the learner's code for account data it can't reach. The session shows it working; the lab has learners build the part the demo hid.

I used Claude throughout: for reading the docs, drafting code, notebooks, and slides, and assembling files. What follows is where my judgment changed the result, and how I checked it. The row-by-row record is in [`design-log.md`](design-log.md).

## The decisions that shaped it

**One build, not a notebook series.** My first plan was a series of notebooks that grew more complex, ending in three or four separate exercises. I dropped it after rereading the brief: "from setup to a small working build" describes one continuous build, and separate exercises at the end would scatter learners right when they should be finishing something. My pilot tester later suggested splitting the lab into two or three notebooks. I kept it as one, because step 2's designed failure only works when the same agent carries straight into step 3.

**A scenario the cookbook doesn't cover, where the custom tool is necessary.** Anthropic's Managed Agents cookbooks already cover code-fixing and CSV analysis, so a reworded version of either would teach reviewers nothing new. In triage, the agent can read the tickets but can't know a customer's plan or renewal date without calling back to "your CRM." That makes the custom tool round trip, the concept that's actually new to Messages API users, necessary rather than decorative. I planted three cases in the data: a minor-sounding ticket from the biggest account, an all-caps ticket from a free customer, and a customer missing from the CRM. The checkpoints know the right answer ahead of time.

**A step designed to fail.** In step 2, learners run the quickstart's event loop, which treats every idle event as "done," and it quits at the first lookup. They see the session pause and wait for them before being asked to fix it. That makes step 3 a problem they understand instead of a template to fill in.

**Self-serve help instead of a hidden answer key.** I originally wanted the final answer key visible only to instructors. The brief says a learner has to finish without an instructor in the room, so learners need a way to get unstuck on their own. Step 3 has three hints of increasing detail, then a sample solution, each behind a click. The instructor copy is in `lab/solutions/`.

**Checks that test the concept, not the model's taste.** The agent's output varies between runs, so the checks use ranges ("T-1004 in the top 3," not "T-1004 is #2"), and they check the downloaded file, not the agent's summary of it. A check that fails on reasonable output teaches learners to distrust checks. Check cells also handle unfinished work, printing "complete the TODOs" instead of crashing. That pattern, along with the task-block-with-success-criteria format, came from studying the OpenHackathons ALCHEMI bootcamp notebooks.

## Where what I shipped differs from what Claude produced

The most useful thing I did was take the lab myself, as a learner, and treat every moment I hesitated as a defect.

- **The event loop Claude wrote sent 21 tool results for 6 tool calls.** The output looked right, and the agent tolerated the duplicates. I only caught it because the loop printed every answer. The fix tracks which calls have been answered, and the lesson became hint 3.
- **The drafted lab asked learners to "decide" what to return for an unknown customer, but the solution silently depended on one specific answer** (a dict with an `"error"` key). I caught it by asking how a learner would know what to write. The instruction now points back to the tool's description, which had promised the agent an error. That turned a trap into a lesson: a custom tool's description is a contract.
- **A checkpoint under a silent cell.** In step 1, the "You know it worked when" line sat under a cell that prints nothing, so a learner could read the silence as failure. The cell now prints a confirmation, and the checkpoint names it.
- **Copying the sample solution grabbed the explanation too**, and the English sentence caused a `SyntaxError`. Explanations now sit above the code.
- **Cleanup that could end the lab by accident.** When I went back to the optional section after running step 6's final cleanup lines, starting a session failed because the environment was archived. Step 6 now says plainly that nothing above will run afterward, and the README covers the recovery.
- **Setup friction I kept out.** My own install fought me, but the audience is engineers. I asked whether my friction applied to them and shipped a preflight cell plus one troubleshooting row, not a setup tutorial.

## How I tested it

- I built and ran the full solution against the live API, then took the lab as a learner in a fresh notebook, then ran the solution notebook end to end.
- I rehearsed the demo and saved the run as `demo_prerun.ipynb`, the offline fallback the speaker script points to.
- One pilot tester, an engineer new to Managed Agents, completed the lab in 50 minutes without help. I took one of his suggestions (pinned package versions) and declined one (splitting the notebook, for the reason above).
- Package versions are pinned in `lab/requirements.txt`, since Managed Agents is in beta.

## What I'd do with more time

- Run the checks across many more runs to measure how often the agent's ranking passes.
- Pilot with two or three more people, including someone on Windows, to test setup beyond my own machine.
- Test the power user section's approval prompt with longer pauses, since it waits on human input while the event stream stays open.
