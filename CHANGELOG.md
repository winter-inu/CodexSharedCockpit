# CHANGELOG.md

## 2026-05-17 澪星尾灯设定同步

### Added
- 更新 `CHARACTER_BIBLE.md`，补充澪星尾灯设定：青蓝色尾部悬浮引航灯不是可随意拆卸的道具，而是通过细微蓝色能量牵引线与澪星连接。
- 明确澪星尾灯平时贴近尾部；照明、指路、边界校准、回声定位或记忆碎片收纳时可短距离悬浮展开；蓝色发光细线代表工作状态，无明显细线代表待机或弱光状态。

### Changed
- 更新 `EPISODE_01_TEST_REVIEW.md`，修正审图原则：澪星允许保留温柔、陪伴、可亲近的生命感，不把“偏可爱”视为主要问题。
- 同步 `SYNC_PACKET.md`，记录澪星尾灯规则和审图原则更新。

## 2026-05-17 第一批测试图审阅表

### Added
- 新增 `EPISODE_01_TEST_REVIEW.md`，建立第一集第一批测试图审阅表。
- 审阅范围包括 S02、S03、S11、S14、S18、S20、S29、S38。
- 新增 `assets/episode01/test-frames/`，同步 8 张第一批测试图文件。
- 每张图包含镜头编号、是否通过、画面优点、主要问题、需要修正的 Prompt、是否需要重生成、是否可进入后期动效。
- 在 `EPISODE_01_TEST_REVIEW.md` 中补充每张测试图的仓库路径，方便 ChatGPT / Codex 共同审阅。
- 新增统一修正原则：正式生成画面尽量不出现可读文字；澪星避免猫型机器人化、红项圈、铃铛和腹部圆口袋；澜冰屿贴近角色海报；小夏保持半透明记忆回声感；场景保持低饱和、冷雾、废弃车站、湿地反光、近未来情感悬疑。

### Changed
- 更新 `TASK_BOARD.md`，记录第一批测试图审阅表已完成，并新增填写审阅表任务。
- 更新 `SYNC_PACKET.md`，同步第一批测试图审阅表和下一步测试图审阅流程。

## 2026-05-17 第一集正式图像测试制作清单

### Added
- 新增 `EPISODE_01_PRODUCTION_SHOTLIST.md`，基于 `EPISODE_01_STORYBOARD.md` 整理第一集正式图像测试制作清单。
- 将 38 个分镜拆成 A 类主关键帧、B 类局部动效 / 推拉 / 裁切、C 类声音 / 转场 / 屏幕信息。
- 新增第一批测试图清单：S02、S03、S11、S14、S18、S20、S29、S38。
- 为 A 类镜头补充对应关键帧编号、画面目的、生成难点、角色参考图需求和优先测试建议。
- 为 B 类镜头补充依赖的 A 类镜头和推荐动效方式。
- 为 C 类镜头补充声音 / 转场 / 屏幕信息方案，并明确 S13 不建议生成完整人群大场面，改为“人流残影经过隔离门的局部镜头”。

### Changed
- 更新 `TASK_BOARD.md`，将“根据分镜脚本修订关键帧生成顺序”标记为 DONE，并新增制作清单审阅和第一批测试图任务。
- 更新 `SYNC_PACKET.md`，同步制作清单、第一批测试图和下一步图像测试流程。

## 2026-05-17 第一集 15 分钟版分镜脚本

### Added
- 新增 `EPISODE_01_STORYBOARD.md`，基于 `EPISODE_01_OUTLINE.md` V2 / 15 分钟版和 `EPISODE_01_KEYFRAMES.md` 整理第一集分镜脚本。
- 按 9 个时间段拆分：0:00-1:30、1:30-3:00、3:00-5:00、5:00-7:30、7:30-9:30、9:30-11:30、11:30-13:00、13:00-14:20、14:20-15:30。
- 将第一集 15 分钟版拆成 9 个时间段、38 个分镜镜头。
- 每段包含剧情内容，并按镜头列出镜头编号、景别、画面、动作、台词/声音、情绪目的和对应关键帧编号。
- 分镜已覆盖 KF-01～KF-16 和 6 个补充关键帧。

### Changed
- 更新 `TASK_BOARD.md`，将“第一集 15 分钟版分镜脚本”标记为 DONE，并新增分镜审阅任务。
- 更新 `SYNC_PACKET.md`，同步第一集分镜脚本已完成，下一步为审阅分镜并测试首批关键帧图。
- 同步 `TASK_BOARD.md` 和 `SYNC_PACKET.md`，将下一步更新为：审阅分镜脚本 → 调整关键帧顺序 → 进入第一集正式图像测试 / 视频化流程。

## 2026-05-17 补充关键帧 Prompt 格式

### Changed
- 本轮强制复核并重新提交 5 个文件：`EPISODE_01_KEYFRAMES.md`、`EPISODE_PLAN.md`、`TASK_BOARD.md`、`SYNC_PACKET.md`、`CHANGELOG.md`。
- 修正 `EPISODE_01_KEYFRAMES.md` 文件用途为 V2 / 15 分钟版。
- 更新 `EPISODE_PLAN.md`，将下一步建议改为：审阅第一集 15 分钟版结构、通过后审阅补充关键帧 Prompt、再整理第一集 15 分钟版分镜脚本。
- 扩写 `EPISODE_01_KEYFRAMES.md` 的“15 分钟版本补充关键帧建议”，把 KF-03.5、KF-05.5、KF-07.5、KF-10.5、KF-11.5、KF-14.5 补齐为与 KF-01～KF-16 相同的完整关键帧 Prompt 格式。
- 修正补充关键帧字段层级，统一使用 `### 剧情功能`、`### 画面描述`、`### 角色状态`、`### 场景氛围`、`### 视觉关键词`、`### AI 绘图 Prompt 中文版`、`### AI 绘图 Prompt 英文版`、`### 禁止项`。
- 更新 `TASK_BOARD.md` 和 `SYNC_PACKET.md`，记录补充关键帧 Prompt 已完成、第一集 15 分钟版已完成，下一步为整理第一集 15 分钟版分镜脚本。
- 为 6 个补充关键帧补齐中英文 Prompt。
- 同步 `TASK_BOARD.md` 和 `SYNC_PACKET.md`。

## 2026-05-17 第一集 15 分钟版结构

### Changed
- 升级 `EPISODE_01_OUTLINE.md`，将第一集《尾灯照见的鞋》从短片式回收大纲改为约 15 分钟单集结构。
- 增加“第一次失败”段落：澜冰屿不能直接带小夏离开，并差点被识别成等待者。
- 明确“被切断的留言”是真正源点，而不是儿童鞋本身。
- 增加“小夏反问澜冰屿：那你呢？有人会绕回来找你吗？”作为情绪反扣。
- 保留 `B-07 锚点状态：存在痕迹下降` 结尾钩子。
- 更新 `EPISODE_PLAN.md`，记录第一集建议时长、功能和第 5 集意象保留规则。
- 更新 `EPISODE_01_KEYFRAMES.md`，仅新增“15 分钟版本补充关键帧建议”，不重写原关键帧。
- 更新 `TASK_BOARD.md` 和 `SYNC_PACKET.md`，同步下一步为审阅 15 分钟结构、补充关键帧与整理分镜。

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
