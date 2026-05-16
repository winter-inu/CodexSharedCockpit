# CHATGPT_MEMORY_SYNC.md

## 用途

这是 ChatGPT 和 Codex 的同步规则。它说明每次 Codex 改动后，用户应该把哪些内容交给 ChatGPT，避免两边理解不同步。

## 每次给 ChatGPT 的最小同步包

Codex 完成一次任务后，用户可以把以下内容复制给 ChatGPT：

1. `SYNC_PACKET.md` 的全文。
2. `TASK_BOARD.md` 的全文。
3. `CHANGELOG.md` 中最新日期段落。
4. 本次被修改的具体设定文件片段。

如果 ChatGPT 能读取 GitHub 仓库，只需要让它先读：

1. `CHATGPT_START_HERE.md`
2. `PROJECT_OVERVIEW.md`
3. `SYNC_PACKET.md`
4. `TASK_BOARD.md`
5. 本次相关的源文件

## ChatGPT 给 Codex 的最小交接包

ChatGPT 产出规划后，请让用户复制以下内容给 Codex：

1. 已确认的新决定。
2. 不允许改动的设定边界。
3. 下一步让 Codex 执行的具体任务。
4. 验收标准。
5. 需要写回哪个 Markdown 文件。

## 写回位置

| 内容类型 | 写回文件 |
| --- | --- |
| 当前状态、最新决定、下一步 | `SYNC_PACKET.md` |
| 任务拆分和状态 | `TASK_BOARD.md` 或 `CODEX_TASKS.md` |
| 重要设定决定 | `DECISIONS.md` |
| 世界观和剧情结构 | `边界回声_项目总览.md`、`边界回声_剧情设定补充.md` |
| 角色设定 | `边界回声_角色圣经.md` |
| Prompt 和风格锁 | `PROMPT_LIBRARY.md` |
| 变更历史 | `CHANGELOG.md` |

## 如果 ChatGPT 看到 GitHub 404

通常原因是仓库是 private，或者 ChatGPT 没有 GitHub 连接器授权。解决方式：

1. 把仓库设为 public。
2. 或在 ChatGPT 中授权 GitHub 连接器。
3. 或把仓库下载为 zip 上传给 ChatGPT。
4. 或至少复制 `CHATGPT_START_HERE.md`、`PROJECT_OVERVIEW.md`、`SYNC_PACKET.md` 和 `TASK_BOARD.md` 给 ChatGPT。

不要因为 404 就重新创建一套设定文件；应先确认访问权限。
