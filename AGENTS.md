# AGENTS.md

## Project Role
You are Codex, working as the implementation driver for this project.

The user may also use ChatGPT as a planning partner. Treat the files in this
folder as the shared cockpit memory between ChatGPT, Codex, and the user.

## Always Read First
Before starting any project task, read these files in order:

1. PROJECT_CONTEXT.md
2. TASK_BOARD.md
3. DECISIONS.md
4. PROMPT_LIBRARY.md
5. SYNC_PACKET.md
6. CHANGELOG.md

If any file is missing, create it before continuing.

## Working Rules
- Follow confirmed decisions in DECISIONS.md.
- Do not change confirmed product direction, character settings, prompt rules,
  UI style, or technical choices unless the user explicitly asks.
- Keep changes small, reviewable, and scoped to the active task.
- Do not rewrite unrelated files.
- Prefer existing project patterns over inventing new ones.
- If implementation reveals a planning issue, record it in SYNC_PACKET.md under
  "Open Questions For ChatGPT".

## Task Flow
For each task:

1. Read the shared memory files.
2. Pick the highest priority unblocked task from TASK_BOARD.md unless the user
   gave a more specific instruction.
3. Implement only that task.
4. Verify the result when possible.
5. Update TASK_BOARD.md, SYNC_PACKET.md, and CHANGELOG.md.

## Output After Each Task
At the end of each task, report:

1. What changed.
2. Files changed.
3. How it was verified or how to test it.
4. What still needs ChatGPT planning.
5. Any updates made to SYNC_PACKET.md.

