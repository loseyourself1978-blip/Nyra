# 夜璃 · Nyra V3｜真正运行素材补齐与 Pets 准入 R2

执行位置：**官方 Codex 原「夜璃 / Nyra」独立工程会话**，不是 TWOS 主研发会话，不是 LDD 项目。以下可直接粘贴；附件中的概念图不能作为已完成动画证据。

```text
CONTINUE TWOS-COMPANION-V3-NYRA
WORK_ORDER: NYRA-V3-RUNTIME-ASSETS-AND-PETS-READINESS-R2
MODE: GENERATE_REAL_ART_THEN_VALIDATE_TARGETED_ATLAS
EXECUTION_SURFACE: OFFICIAL_CODEX_EXISTING_NYRA_THREAD
EXECUTE NOW
DO_NOT_START_DUPLICATE_JOB

一、读取真实基线，不重复静态预览

读取本轮补充包README、DELIVERY_STATUS、SOURCE_AND_TARGET_RECONCILIATION、
PRODUCTION_PLAN、ART_LOCK_AND_ALPHA、完整prompts与specs，以及原R1报告。

既有工程线索：
/Users/hj/Documents/Codex/2026-10-23/pets-plugin-work-pets-openai-curated/outputs/Nyra
私有仓库：loseyourself1978-blip/Nyra
按本机实际目录/分支/HEAD/活动作业核对，不克隆第二份、不覆盖未知变更。
不要扫描TWOS源码/业务库，不修改Owner运行的TWOS App。

R1是STATIC_PREVIEW，原302×517主裁片和86×212换装只是参考。
原拖动、缩放、全屏、隐藏恢复与退出证据保留，不重做来凑本轮进度。
本轮补充包当前运行画稿=0；78份prompt不是78张图片，工具自测不是角色PASS。

二、先确认图像生产能力和目标载体

读取实际已安装的官方图像生成能力与Pets创建skill。
可能叫hatch-pet或create-pet，以本机实际版本为准，不猜路径/API参数。
没有图像生成工具时，不用低清裁片放大、海报摇摆、批量复制静帧或代码几何人形充数；
明确记录BLOCKED_IMAGE_GENERATION_NOT_AVAILABLE，并完成无依赖的目标核对/工具接入。
只使用已授权的现有额度，不购买、充值、新订阅或私自切到付费供应商。

独立App画布1024×1536；附件Pets v2为1536×2288/8×11/73有效槽；
当前公开网页Pets上传要求1536×1872，不能把两者混为同一目标。
先记录实际宿主App版本、skill/hash、真实预检器、逐行动作和方向顺序。
默认生成目标为该Mac实际内置Pets的受支持版本；不凭网页上传尺寸推定桌面格式。
方向顺序不明确时先生成母版/P0，不提前拼最终图集。

三、真的补图，停止画综合海报

以选定V3和原ART_BIBLE锁定夜璃/Nyra：
约25岁成年、黑紫猫耳、深色长卷发、紫晶眼睛、角色解剖左侧紫晶饰物、
黑颈饰、黑紫细尾；不透明完整内衬的黑紫裙装、深色袜和短跟靴。
成熟、温柔、优雅和可爱通过表情与动作呈现，不改幼态Q版，不画裸露或色情姿态。

先真实生成一个完整透明中立母版：
runtime/default/nyra_neutral.png
1024×1536 RGBA/sRGB，人物外alpha=0，核心不透明，头耳手脚发尾尾尖完整。
统一脚锚点(512,1444)，top/side约8%、bottom约6%，无标题/棋盘格/地面/独立符号。
保存原始输出、实际分辨率、来源/额度路径和hash。
不假报原生分辨率；抠图和统一归一化处理如实留痕。

母版实际审核同一人设后，以它为reference逐族生成P0：
20张唯一PNG，明确映射为23槽：idle6、working6、gaze/head5、verified_success6。
母版共享关系按standalone_p0.json；重复引用不能计为新增表演。
身体局部必须实际改变：眨眼、肩发/尾、手腕手指、头眼联动、点头挥手。
不能对整张立绘缩放平移冒充动作；成功动作只播一次，PARTIAL不庆祝。
使用prompts逐目标文件，不一次生成带很多小人的低清综合板。

四、Pets扩展与换装边界

P0四套实际播放合格后，按已核实目标补其余动作。
附件v2规划为idle6、向右8、向左8、挥手4、跳跃5、failed8、waiting6、
running工作6、review6、16方向视线；共73有效槽与15透明空格。
左右步态不能简单镜像导致左侧标志饰物换边。
16向先四向锚点再两组八方向；眼头共同变化，不能旋转全身代替看向。

所有帧共用尺度/原点/光源；不逐帧自动裁紧再铺满格子。
编译器的全组等比变换是导出处理，不是人物动画。
职场中立换装单独制作，保持同脸同姿态同锚点；
未补完该服装全部动作，标STATIC_OUTFIT_ONLY，不宣称完整动画换装。
晚礼服、扩展表情与音频按后续范围如实列缺，不能让第一套动画再次停在静态预览。

五、执行质检，保留真实缺口

使用现有Python/Pillow；缺依赖按现有工程规范处理，不私自购买或联网安装。
运行补充包工具：
python tools/nyra_assets.py inspect runtime/default/nyra_neutral.png
python tools/nyra_assets.py audit --subset p0 --report reports/p0_current.json

登记真实hash、来源处理和native_resolution_provenance，不复制示例PASS。
在preview/animation_review.html中加载实际PNG，检查黑/白/棋盘格/紫色底，
填写visual_review.json：身份、解剖、覆盖、alpha边缘、锚点及序列连续性。
审片不能仅看截图；真正循环播放和一次性动作都要检查。

冻结目标profile和target_environment证据后，才编译最终图集：
python tools/nyra_assets.py profile <实际选择的profile>
python tools/nyra_assets.py build --profile <实际选择的profile> --output exports/<明确目标文件>.png

工具当前默认BLOCKED是因为缺图/目标未确认，不要删除这些门槛。
合成自测图只能用于工具验证，不进运行目录、不上传Pets、不宣传为已制作角色。
图集编译成功后还需运行真实创建skill自带预检、alpha/方向/连续性检查及宿主播放。
不虚构脚本名称、preflight结果或API字段。

六、独立App、Pets、语音和TWOS联动分别判定

独立App复用原框架加载真实帧，先完成四动作和可恢复显示，测新动画性能，
不拿静态0%CPU回执证明动画性能。

GitHub上传/本机有App不等于Pet在列表中。
本次材料补齐默认到READY_FOR_PETS_CREATION；
仅当已有明确创建/选中授权时使用实际支持入口继续，否则给一次准确创建/选择动作。
先列现有Pet并去重，不创建多个Nyra、不替换未知活动Pet。
实际建立后分别记录Pet ID、列表可见、选择、真实播放，不能仅说“重启就会出现”。

内置Pets的Ready只代表宿主活动状态，不等于TWOS业务已验证或Owner已接受。
不擅加读取TWOS私有数据库的接口。真实TWOS联动继续单独授权，只读最小事件。
声音当前未制作；系统TTS或第三方预置声音不能称专属原创女声，默认静音。
不自动下载音色或访问麦克风、录屏、辅助功能、全盘权限。

七、仓库与交付

只在独立Nyra工程处理新素材、工具和文档；保留原参考和R1报告。
原私有仓库上传授权仅保留原范围，本次不自动远端Push/Tag/公开Release。
整理一个增量包，包含实际PNG、动作帧表、源/输出hash、审片、目标profile及真实回执。
没有实际画稿不得返回“全套素材补齐”，不以文档数量替代图片数量。

回传必须包含：
REAL_IMAGE_GENERATION_CHANNEL_AND_COST_BOUNDARY:
ACTUAL_NEW_NATIVE_RUNTIME_PNG_COUNT:
P0_FOUR_ANIMATIONS_AND_PLAYBACK:
REFERENCE_VS_RUNTIME_ASSETS:
ALPHA_ANCHOR_AND_IDENTITY_REVIEW:
TARGET_PETS_APP_SKILL_VERSION_AND_LAYOUT:
ATLAS_VALIDATION_AND_SPRITE_VERSION:
PET_CREATED_LIST_VISIBLE_SELECTED: 分开
OUTFIT_ANIMATION_COVERAGE:
ORIGINAL_VOICE_STATUS:
TWOS_READONLY_INTEGRATION_STATUS:
OWNER_TWOS_PRESERVATION:
PURCHASES_AND_PUBLICATION: NONE
MISSING_ITEMS_AND_ONE_NEXT_ACTION:

现在先核实可用图像能力与目标格式，真正生成和检查透明母版，
随后连续完成P0四套动作；不要再次只交静态预览App或综合设定海报。
```
