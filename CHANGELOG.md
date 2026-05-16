# CHANGELOG.md

## 2026-05-16 角色视觉参考同步

### Added
- 新增 `CHARACTER_VISUAL_REFERENCES.md`，记录主角团视觉参考图读取规则。
- 新增 `assets/characters/lan-bingyu-poster.png`。
- 新增 `assets/characters/lin-jianzhou-poster.png`。
- 新增 `assets/characters/lu-heng-poster-v2.png`。
- 新增 `assets/characters/xu-mingjin-poster-v2.png`。
- 新增 `assets/characters/lingstar-poster.png`。
- 新增 `assets/characters/main-cast-group-poster.png`。

### Changed
- 更新 `CHATGPT_START_HERE.md` 和 `AGENTS.md`，把 `CHARACTER_VISUAL_REFERENCES.md` 加入优先读取顺序。
- 更新 `SYNC_PACKET.md`，说明后续关键帧生成必须参考角色海报，避免角色外观漂移。

## 2026-05-16 第一集关键帧 Prompt

### Added
- 新增 `EPISODE_01_KEYFRAMES.md`，基于第一集大纲 V1 拆分 16 个关键帧。
- 每个关键帧包含镜头编号、剧情功能、画面描述、角色状态、场景氛围、视觉关键词、中英 AI 绘图 Prompt 和禁止项。
- 关键帧统一风格为近未来科幻情感悬疑、冷雾、低饱和、电影感、细腻动画剧集感。
- 记录首批关键帧测试建议：优先 KF-02、KF-03、KF-06、KF-13、KF-16；可选补充 KF-14。

### Changed
- 更新 `TASK_BOARD.md`，将“建立第一集关键帧 Prompt”标记为 DONE，并新增关键帧审阅任务。
- 更新 `SYNC_PACKET.md`，同步关键帧文件状态和优先测试图建议。

### Notes
- `漫剧关键帧Prompt生成器.html` 是早前同步进仓库的既有工具文件，不是本轮新增；已在“2026-05-16 GitHub 同步”段落中记录。

## 2026-05-16 第一集大纲 V1 修订

### Changed
- 修订 `EPISODE_01_OUTLINE.md` 为 V1，保留《尾灯照见的鞋》核心事件和原段落结构。
- 弱化第一集中的“末班车 / 已到站 / 无人列车”意象，避免与第 5 集《无人到站》重复。
- 将第一集重点进一步收束到失物招领室、临时安置点、儿童等待区、儿童鞋和等待被误解。
- 增加澪星无台词陪伴动作：用额头星核照住澜冰屿变淡的影子，用尾灯确认他的影子没有继续消失。
- 降低第一集设定解释密度，B-07 仅保留为结尾伏笔。
- 更新 `TASK_BOARD.md` 和 `SYNC_PACKET.md`，同步第一集 V1 状态和下一步建议。

## 2026-05-16 第一集大纲草案

### Added
- 新增 `EPISODE_01_OUTLINE.md`，建立第一集“澜冰屿 + 澪星”完整剧情大纲草案。
- 第一集标题暂定为《尾灯照见的鞋》。
- 第一集从废弃车站、雾、澪星尾灯和儿童鞋展开。
- 第一集遗憾循环暂定为“小夏在车站等待母亲，误以为自己被遗忘”。
- 第一集结尾加入 `B-07 锚点状态：存在痕迹下降` 作为澜冰屿非普通人和代价的伏笔。

### Changed
- 更新 `TASK_BOARD.md`，将“编写第一集完整剧情大纲草案”标记为 DONE，并新增审阅任务。
- 更新 `SYNC_PACKET.md`，同步第一集大纲草案状态和下一步建议。

## 2026-05-16 项目入口校准

### Added
- 新增 `PROJECT_OVERVIEW.md`，作为新读者项目总入口。
- 新增 `STORY_BIBLE.md`，作为故事设定入口。
- 新增 `CHARACTER_BIBLE.md`，作为角色设定入口。
- 新增 `WORLD_RULES.md`，作为世界观规则入口。
- 新增 `EPISODE_PLAN.md`，作为分集规划入口。
- 新增 `CODEX_TASKS.md`，作为 Codex 任务池。
- 新增 `CHATGPT_MEMORY_SYNC.md`，作为 ChatGPT / Codex 同步规则说明。

### Changed
- 更新 `CHATGPT_START_HERE.md`，加入更完整的读取顺序和 404 处理提示。
- 更新 `AGENTS.md`，让 Codex 优先读取新增入口文件。
- 更新 `SYNC_PACKET.md`，记录 GitHub 访问 404 的处理判断和入口校准结果。

## 2026-05-16 GitHub 同步

### Added
- 新增 `CHATGPT_START_HERE.md`，说明 ChatGPT 读取顺序、协作方式、接手提示词和写回规则。
- 将 `F:\边界回声` 中的核心项目资料同步到 `F:\CodexSharedCockpit`，便于通过 GitHub 仓库交给 ChatGPT 读取。

### Synced Files
- `PROJECT_CONTEXT.md`
- `SYNC_PACKET.md`
- `TASK_BOARD.md`
- `DECISIONS.md`
- `CHANGELOG.md`
- `README.md`
- `CONVERSATION_LOG.md`
- `IMPORT_INBOX.md`
- `PROMPT_LIBRARY.md`
- `边界回声_项目总览.md`
- `边界回声_角色圣经.md`
- `边界回声_剧情设定补充.md`
- `漫剧关键帧Prompt生成器.html`
- `online/index.html`
- `online/README.md`

## 2026-05-16

### Added
- 新增 `边界回声_剧情设定补充.md`，整理静海系统、静海断层、异常区等名词解释。
- 新增澜冰屿与澪星作为开局双人组的叙事结构。
- 新增林见舟详细设定、能力边界、隐藏伏笔和人物弧光。
- 新增澪星“泊舟体系”来源、能力边界、隐藏伏笔和与澜冰屿的关系。
- 新增单元事件样例《无人到站》，用于展示主角团能力与分工。
- 新增主角团能力与装备来源：澜冰屿人形锚点、澪星泊舟体系、陆衡取证终端、林见舟心律共鸣晶体、许明烬工业机械右手。

### Changed
- 更新 `边界回声_项目总览.md`，将第一季前段结构调整为“澜冰屿 + 澪星先行，其他成员逐步加入”。
- 更新 `边界回声_角色圣经.md`，同步澜冰屿、林见舟、澪星的新关系、能力边界和伏笔。
- 更新陆衡视觉道具逻辑：妹妹照片改为贴在旧相机包内侧或肩带背面，关键时刻由取证终端投射妹妹影像残帧。
- 更新 `SYNC_PACKET.md`，把项目阶段推进到核心设定与前段叙事结构细化阶段。

## 2026-05-15

### Added
- 创建 F:\边界回声 项目档案夹。
- 添加 README.md。
- 添加 PROJECT_CONTEXT.md。
- 添加 CONVERSATION_LOG.md。
- 添加 IMPORT_INBOX.md。
- 添加 TASK_BOARD.md。
- 添加 DECISIONS.md。
- 添加 PROMPT_LIBRARY.md。
- 添加 SYNC_PACKET.md。
- 添加 CHANGELOG.md。

### Notes
- 当前 Codex 无法访问 ChatGPT 外部历史对话。
- 已搜索本地当前工作目录和 F:\CodexSharedCockpit，未找到“边界回声”相关旧记录。
