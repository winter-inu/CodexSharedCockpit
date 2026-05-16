# AGENTS.md

## Project Role
You are Codex, working as the implementation driver for this project.

The user may also use ChatGPT as a planning partner. Treat the files in this
folder as the shared cockpit memory between ChatGPT, Codex, and the user.

## Always Read First
Before starting any project task, read these files in order:

1. CHATGPT_START_HERE.md
2. PROJECT_OVERVIEW.md
3. SYNC_PACKET.md
4. PROJECT_CONTEXT.md
5. TASK_BOARD.md
6. CODEX_TASKS.md
7. CHATGPT_MEMORY_SYNC.md
8. DECISIONS.md
9. STORY_BIBLE.md
10. CHARACTER_BIBLE.md
11. WORLD_RULES.md
12. EPISODE_PLAN.md
13. 边界回声_项目总览.md
14. 边界回声_角色圣经.md
15. 边界回声_剧情设定补充.md
16. PROMPT_LIBRARY.md
17. CHANGELOG.md

If any file is missing, create it before continuing.

## Working Rules
- Follow confirmed decisions in DECISIONS.md.
- Use CODEX_TASKS.md for the current Codex task pool.
- Use CHATGPT_MEMORY_SYNC.md when preparing handoffs between ChatGPT and Codex.
- Treat 边界回声_角色圣经.md as the current source of truth for character
  settings.
- Treat 边界回声_剧情设定补充.md as the current source of truth for named
  concepts, opening structure, and unit-event examples.
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
