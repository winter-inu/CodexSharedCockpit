# PROMPT_LIBRARY.md

## How To Use This File
Store reusable prompts here so ChatGPT and Codex work from the same wording.
Keep prompts short, specific, and easy to update.

## ChatGPT Planning Prompt

```text
这是当前项目的 SYNC_PACKET.md：
"""
粘贴 SYNC_PACKET.md 的内容
"""

请基于它继续拆任务，输出：
1. 下一轮任务优先级
2. 给 Codex 的任务 Prompt
3. 风险点
4. 需要更新到 PROJECT_CONTEXT.md / DECISIONS.md / TASK_BOARD.md 的内容
```

## Codex Implementation Prompt

```text
请先阅读 AGENTS.md、PROJECT_CONTEXT.md、TASK_BOARD.md、DECISIONS.md、PROMPT_LIBRARY.md、SYNC_PACKET.md、CHANGELOG.md。

然后完成 TASK_BOARD.md 中最高优先级的一个未阻塞任务。

要求：
1. 只修改必要文件。
2. 完成后更新 TASK_BOARD.md。
3. 完成后更新 SYNC_PACKET.md。
4. 完成后更新 CHANGELOG.md。
5. 最后告诉我改了哪些文件、怎么测试、还有什么需要 ChatGPT 继续规划。
```

## ChatGPT Review Prompt

```text
这是 Codex 完成任务后的摘要：
"""
粘贴 Codex 的最终回复
"""

这是当前 SYNC_PACKET.md：
"""
粘贴 SYNC_PACKET.md 的内容
"""

请帮我做一次产品和实现验收：
1. 是否符合目标
2. 是否有遗漏
3. 下一步最高优先级任务
4. 给 Codex 的下一条明确任务
```

## Character Lock Prompt Template

```text
角色名：
固定外观：
固定服装：
性格关键词：
说话方式：
禁止变化：
负面提示词：
适用场景：
```

