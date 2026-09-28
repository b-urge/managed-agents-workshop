# Design log: Managed Agents workshop

Sep 28, 2026

## How to use this log

I added one row each time I changed, rejected or caught something, whether it came from Claude, the docs or my own confusion. Each row says what happened, what I shipped instead and why.

This log is the raw material for the design note. The brief grades the difference between what the model produced and what I shipped, so every row here is evidence of judgment.

## Entries

| Date | What happened | What I shipped | Why |
| --- | --- | --- | --- |
| Sep 23 | Installing JupyterLab through Homebrew failed: it couldn't reach GitHub and tried to compile LLVM from source. A Python venv with pip worked. The quickstart itself then took under 5 minutes. | A preflight cell and one troubleshooting row, not a setup tutorial. | I noticed my own setup friction and asked whether it applied to the audience. |
| Sep 23 | The AI-written event loop sent 21 tool results for 6 custom tool calls. The output looked correct. I caught it only because the loop printed every answer. | The loop tracks which calls it has answered and sends results in one batch. Lab hint: track what you've already answered. | Correct-looking output isn't proof. Printing each step is what exposed the bug. |
| Sep 23 | First checkpoint idea was an exact rank for the canary ticket. | Asserts use ranges (T-1004 in the top 3) and check the downloaded file, not the agent's summary. | A check that fails on reasonable model output teaches learners to distrust checks. Verifying the file is borrowed from the cookbook. |
| Sep 27 | Taking the lab as a learner, step 1: the "You know it worked when" line sits under the start\_session cell, which prints nothing. A learner could read the silence as a failure. | The start\_session cell now prints "start\_session is ready", and the checkpoint line names it. | A checkpoint should sit next to the output it describes. |
| Sep 27 | Step 3: the Claude-drafted lab tells learners to "decide" what lookup\_account returns for a missing customer. But run\_turn's solution checks "error" in result, so returning None, raising, or a plain string breaks step 3 through a connection nobody states. I caught it by asking how a learner would know what to write. | Instruction 1 now quotes the tool description's promise and asks learners to keep it: return the record as a dict, or a dict with an "error" key. The scaffold's TODO says the same. | A "decision" that silently breaks later code is a trap, not a lesson. Tying it to the tool description teaches that a custom tool's description is a contract with the agent. |
| Sep 27 | Power user: copying the sample solution grabbed the explanation paragraph under the code too. Running it gave a SyntaxError on the English sentence. | Both sample solutions now put the explanation above the code, so the code block is the last thing in the box. | Learners copy from the solution to the end of the box. Nothing they'd reasonably select should break. |
| Sep 27 | Went back to the power user section after running step 6 with the "done with the lab" lines uncommented. Starting a session failed: 400, "Environment ... is archived." | Step 6's text and comment now say nothing above will run afterward, and why. The README's troubleshooting table covers the recovery. | Learners don't always go in order. Cleanup that can be undone by accident should say what it ends. The error itself is a useful lesson: an archived environment can't start sessions. |
| Sep 28 | Redrew two slides as diagrams: slide 3 as a boundary between your side and Anthropic's, slide 5 as agent, environment, and files feeding a session that trades events with your app. Left the rest as text and tables. | Diagrams only where the picture carries the idea. Slide 3 now mirrors slide 2, so the before and after are visual. |
| Sep 28 | Pilot tester suggested splitting the lab into two or three notebooks: basics, then exercises. | Kept one notebook. | The brief asks for one 60-minute build from setup to a working thing, and step 2's designed stop only works because the same agent carries straight into step 3. |
| Sep 28 | Pilot tester flagged unpinned package versions. The README installed the newest anthropic SDK on whatever day someone ran it. | requirements.txt generated from my tested environment; the README installs from it and notes the tested Python version. | Managed Agents is in beta. An instructor running this months later needs the versions it was known to work on. |
| Sep 28 | Pilot tester, new to the lab, finished it in 50 minutes. | No change to the core lab. The optional power user section covers fast finishers. | 50 minutes leaves room inside the 60-minute budget for slower learners, setup trouble, and the power user section. |