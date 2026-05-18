# 《边界回声》GitHub 仓库清理计划

状态：待审阅  
日期：2026-05-18  
目的：先做分析和清单，不执行删除、不移动文件、不改正文内容。

---

## 一、清理目标

- 只保留《边界回声》最新有效内容。
- 删除或移出旧版记录、旧版样片流程、旧版关键帧和过期审阅文件。
- 降低 Codex 上下文负担。
- 减少版本混淆。
- 方便后续审核和视频制作。

本计划只提供清理建议。实际删除、移动、重命名必须在二次确认后单独执行。

---

## 二、建议保留文件清单

### 项目入口文件

- README.md
- PROJECT_OVERVIEW.md
- PROJECT_CONTEXT.md
- CHATGPT_START_HERE.md
- AGENTS.md
- DECISIONS.md
- CODEX_TASKS.md
- TASK_BOARD.md
- SYNC_PACKET.md
- CHANGELOG.md

### 世界观设定

- STORY_BIBLE.md
- WORLD_RULES.md
- 边界回声_项目总览.md
- 边界回声_剧情设定补充.md
- docs/boundary_echo_style_guide.md

### 角色设定

- CHARACTER_BIBLE.md
- CHARACTER_VISUAL_REFERENCES.md
- 边界回声_角色圣经.md

### 角色海报 / prompt

- assets/characters/lan-bingyu-poster.png
- assets/characters/lingstar-poster.png
- assets/characters/lin-jianzhou-poster.png
- assets/characters/lu-heng-poster-v2.png
- assets/characters/xu-mingjin-poster-v2.png
- assets/characters/main-cast-group-poster.png
- prompts/character_locks.md
- prompts/global_style_lock.md
- prompts/environment_locks.md
- prompts/kling_consistency_lock.md
- prompts/prompt_templates.md
- prompts/boundary_echo_quick_prompt_pack.md

### 第一季剧情

- EPISODE_PLAN.md

### 第一集 V3 最新文件

- EPISODE_01_OUTLINE_V3_EMOTIONAL.md
- EPISODE_01_EMOTIONAL_ACTION_TABLE.md
- EPISODE_01_V3_KEYFRAME_VIDEO_PLAN.md

### 视觉风格

- CHARACTER_VISUAL_REFERENCES.md
- docs/boundary_echo_style_guide.md
- prompts/global_style_lock.md
- prompts/environment_locks.md
- prompts/kling_consistency_lock.md

### 制作流程

- CLEANUP_PLAN.md
- PROMPT_LIBRARY.md
- 漫剧关键帧Prompt生成器.html
- online/README.md
- online/index.html

---

## 三、建议删除文件清单

以下均为建议删除或归档候选，不在本次执行。

### 被 V3 替代的旧版第一集剧情文件

- EPISODE_01_OUTLINE.md  
  删除原因：旧版第一集大纲，已被 `EPISODE_01_OUTLINE_V3_EMOTIONAL.md` 替代，容易让 Codex 回到旧版事件推进结构。
- EPISODE_01_STORYBOARD.md  
  删除原因：旧版 38 镜头分镜脚本，基于旧版事件推进逻辑，容易和 V3 情感推进计划混用。
- EPISODE_01_KEYFRAMES.md  
  删除原因：旧版关键帧 Prompt 草案，包含旧版 KF/S 编号体系，容易覆盖 V3 K01-K15。
- EPISODE_01_PRODUCTION_SHOTLIST.md  
  删除原因：旧版正式图像测试制作清单，已不再作为当前制作主线。
- EPISODE_01_FINAL_KEYFRAMES.md  
  删除原因：旧版 A 类主关键帧最终清单，基于旧版样片流程，会干扰 V3 样片优先级。

### 旧版 S18-S24 样片流程相关文件

- EPISODE_01_VIDEO_TEST_PLAN.md  
  删除原因：旧版视频化测试方案，包含旧版 S18-S24 样片流程；当前明确暂缓，不再直接作为制作样片。
- EPISODE_01_B_SHOT_MOTION_PLAN.md  
  删除原因：旧版 B 类镜头动效方案，服务于旧版全片测试流程，不属于当前 V3 第一版样片 P0。
- EPISODE_01_POST_TEXT_LIST.md  
  删除原因：旧版后期文字添加清单，基于旧版 S 编号；V3 应重建后期文字清单。

### 临时测试审阅文件

- EPISODE_01_TEST_REVIEW.md  
  删除原因：第一批测试图审阅表，属于历史测试记录。
- EPISODE_01_TEST_REVIEW_BATCH_02.md  
  删除原因：第二批测试图审阅表，属于历史测试记录。

### 已过期任务记录 / 上下文负担文件

- CONVERSATION_LOG.md  
  删除原因：长期对话记录容易把旧决策重新带入上下文，增加版本混淆。
- IMPORT_INBOX.md  
  删除原因：临时导入收件箱，若内容已吸收进正式文件，可删除或清空后重建。
- CHATGPT_MEMORY_SYNC.md  
  删除原因：若其中仍包含旧版任务同步，可在清理后重建为 V3 专用同步文件。

### 旧版测试图资产

- assets/episode01/test-frames/  
  删除原因：第一批旧版测试图资产，基于旧版 S 编号和旧版审阅流程。
- assets/episode01/test-frames-revised/  
  删除原因：第一批旧版修订测试图资产，保留会让 Codex 误以为旧版测试仍是当前制作源。
- assets/episode01/test-frames-main-batch-02/  
  删除原因：第二批旧版 A 类主关键帧测试图资产，已不再作为 V3 样片直接输入。
- assets/episode01/test-frames-main-batch-02-revised/  
  删除原因：第二批旧版修订测试图资产，属于历史版本。

### 可选删除或转存的压缩包 / 临时包

- 主角团人物海报.zip  
  删除原因：若全部角色海报已解压并纳入 `assets/characters/`，压缩包可移出仓库或放入外部归档，减少重复资产。

---

## 四、建议移动 / 重命名文件清单

以下为建议结构调整，不在本次执行。

### 移动到 docs/world/

- STORY_BIBLE.md -> docs/world/STORY_BIBLE.md
- WORLD_RULES.md -> docs/world/WORLD_RULES.md
- PROJECT_OVERVIEW.md -> docs/world/PROJECT_OVERVIEW.md
- PROJECT_CONTEXT.md -> docs/world/PROJECT_CONTEXT.md
- 边界回声_项目总览.md -> docs/world/project_overview_cn.md
- 边界回声_剧情设定补充.md -> docs/world/story_setting_supplement_cn.md

### 移动到 docs/characters/

- CHARACTER_BIBLE.md -> docs/characters/CHARACTER_BIBLE.md
- 边界回声_角色圣经.md -> docs/characters/character_bible_cn.md

### 移动到 docs/visual/

- CHARACTER_VISUAL_REFERENCES.md -> docs/visual/CHARACTER_VISUAL_REFERENCES.md
- docs/boundary_echo_style_guide.md -> docs/visual/boundary_echo_style_guide.md
- assets/characters/ -> docs/visual/characters/

### 移动到 episodes/season_01/

- EPISODE_PLAN.md -> episodes/season_01/EPISODE_PLAN.md
- EPISODE_01_OUTLINE_V3_EMOTIONAL.md -> episodes/season_01/episode_01/EPISODE_01_OUTLINE_V3_EMOTIONAL.md
- EPISODE_01_EMOTIONAL_ACTION_TABLE.md -> episodes/season_01/episode_01/EPISODE_01_EMOTIONAL_ACTION_TABLE.md
- EPISODE_01_V3_KEYFRAME_VIDEO_PLAN.md -> episodes/season_01/episode_01/EPISODE_01_V3_KEYFRAME_VIDEO_PLAN.md

### 保留在 prompts/

- prompts/global_style_lock.md
- prompts/character_locks.md
- prompts/environment_locks.md
- prompts/kling_consistency_lock.md
- prompts/prompt_templates.md
- prompts/boundary_echo_quick_prompt_pack.md

### 移动到 production/

- PROMPT_LIBRARY.md -> production/PROMPT_LIBRARY.md
- 漫剧关键帧Prompt生成器.html -> production/tools/漫剧关键帧Prompt生成器.html
- online/ -> production/online/
- CLEANUP_PLAN.md -> production/CLEANUP_PLAN.md

---

## 五、建议的新仓库结构

```text
CodexSharedCockpit/
├─ README.md
├─ AGENTS.md
├─ TASK_BOARD.md
├─ SYNC_PACKET.md
├─ CHANGELOG.md
├─ CLEANUP_PLAN.md
├─ docs/
│  ├─ world/
│  │  ├─ PROJECT_OVERVIEW.md
│  │  ├─ PROJECT_CONTEXT.md
│  │  ├─ STORY_BIBLE.md
│  │  ├─ WORLD_RULES.md
│  │  ├─ project_overview_cn.md
│  │  └─ story_setting_supplement_cn.md
│  ├─ characters/
│  │  ├─ CHARACTER_BIBLE.md
│  │  └─ character_bible_cn.md
│  └─ visual/
│     ├─ CHARACTER_VISUAL_REFERENCES.md
│     ├─ boundary_echo_style_guide.md
│     └─ characters/
│        ├─ lan-bingyu-poster.png
│        ├─ lingstar-poster.png
│        ├─ lin-jianzhou-poster.png
│        ├─ lu-heng-poster-v2.png
│        ├─ xu-mingjin-poster-v2.png
│        └─ main-cast-group-poster.png
├─ episodes/
│  └─ season_01/
│     ├─ EPISODE_PLAN.md
│     └─ episode_01/
│        ├─ EPISODE_01_OUTLINE_V3_EMOTIONAL.md
│        ├─ EPISODE_01_EMOTIONAL_ACTION_TABLE.md
│        └─ EPISODE_01_V3_KEYFRAME_VIDEO_PLAN.md
├─ prompts/
│  ├─ global_style_lock.md
│  ├─ character_locks.md
│  ├─ environment_locks.md
│  ├─ kling_consistency_lock.md
│  ├─ prompt_templates.md
│  └─ boundary_echo_quick_prompt_pack.md
└─ production/
   ├─ PROMPT_LIBRARY.md
   ├─ tools/
   │  └─ 漫剧关键帧Prompt生成器.html
   └─ online/
      ├─ README.md
      └─ index.html
```

---

## 六、风险提示

- 清理前建议创建 git tag：`archive-before-cleanup-2026-05-18`。
- 删除前必须二次确认。
- 不要删除最新 V3 文件：
  - EPISODE_01_OUTLINE_V3_EMOTIONAL.md
  - EPISODE_01_EMOTIONAL_ACTION_TABLE.md
  - EPISODE_01_V3_KEYFRAME_VIDEO_PLAN.md
- 不要删除角色设定和视觉风格锁定文件：
  - CHARACTER_BIBLE.md
  - CHARACTER_VISUAL_REFERENCES.md
  - 边界回声_角色圣经.md
  - prompts/character_locks.md
  - prompts/global_style_lock.md
  - prompts/environment_locks.md
  - prompts/kling_consistency_lock.md
- 如果需要保留旧版历史，请优先通过 git tag、GitHub release 或外部 archive 文件夹保存，而不是继续放在主工作区。
- 任何实际移动都需要同步更新引用路径，尤其是 `AGENTS.md`、`TASK_BOARD.md`、`SYNC_PACKET.md`、prompt 文档和制作工具里的路径。
