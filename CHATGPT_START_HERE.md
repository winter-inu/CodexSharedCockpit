# CHATGPT_START_HERE.md

## 给 ChatGPT 的读取顺序

这是《边界回声》项目的共享工作仓库。请按以下顺序读取文件：

1. `SYNC_PACKET.md`
2. `PROJECT_CONTEXT.md`
3. `TASK_BOARD.md`
4. `DECISIONS.md`
5. `边界回声_项目总览.md`
6. `边界回声_角色圣经.md`
7. `边界回声_剧情设定补充.md`
8. `PROMPT_LIBRARY.md`
9. `CHANGELOG.md`

## 当前协作方式

- 用户负责最终审美、剧情方向和设定确认。
- ChatGPT 负责规划、剧情拆解、设定补完、提示词设计、验收标准和审阅。
- Codex 负责读取本地文件、整理 Markdown、实现工具页面、同步任务状态和变更记录。
- 重要结论必须写回 Markdown 文件，不能只停留在聊天记录里。

## 让 ChatGPT 接手时可以直接使用的提示词

```text
你现在接手《边界回声》项目。请先读取这个 GitHub 仓库里的 CHATGPT_START_HERE.md、SYNC_PACKET.md、PROJECT_CONTEXT.md、TASK_BOARD.md、DECISIONS.md、边界回声_项目总览.md、边界回声_角色圣经.md、边界回声_剧情设定补充.md。

读取后请输出：
1. 你理解的当前项目状态。
2. 当前最重要的 3 个未完成任务。
3. 你建议下一步让 Codex 执行的具体任务。
4. 如果需要补充设定，请列出问题，但不要擅自改动已确认设定。
```

## 写回规则

ChatGPT 的新结论如果要交给 Codex 执行，请让用户把结论复制进：

- `SYNC_PACKET.md`：当前状态、最新决定、下一步任务。
- `TASK_BOARD.md`：任务拆分和状态。
- `DECISIONS.md`：已经确认的重要设定或工作方式。
- 对应设定文件：角色、剧情、世界观、Prompt 等具体内容。

Codex 完成改动后，应同步更新 `SYNC_PACKET.md`、`TASK_BOARD.md` 和 `CHANGELOG.md`。
