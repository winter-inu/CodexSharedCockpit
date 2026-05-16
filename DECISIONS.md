# DECISIONS.md

## Confirmed Decisions

| Date | Decision | Reason | Owner |
| --- | --- | --- | --- |
| 2026-05-15 | Use shared markdown files as the source of truth between ChatGPT and Codex | ChatGPT and Codex do not automatically share full working memory | User |
| 2026-05-15 | Use AGENTS.md to tell Codex how to work in this project | Codex can reliably read project-local instructions | User |
| 2026-05-15 | Use SYNC_PACKET.md as the handoff document | Keeps planning and implementation aligned | User |

## Proposed But Not Confirmed

| Proposal | Status | Notes |
| --- | --- | --- |
| Add JSON import/export for shared task state | Open | Useful later if the workflow grows. |
| Use Git branches/worktrees for parallel Codex tasks | Open | Good for larger projects with independent tasks. |
| Keep prompt templates in PROMPT_LIBRARY.md | Open | Useful if the project involves AI production prompts. |

## Rejected Decisions

| Date | Rejected Idea | Reason |
| --- | --- | --- |
| 2026-05-15 | Rely on ChatGPT or Codex memory alone for project state | Too easy for details to drift or disappear. |

