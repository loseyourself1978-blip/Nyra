# 夜璃 · Nyra R1 交付报告

日期：2026-10-23（Asia/Shanghai）。交付等级：`ASSET_AUDIT + STANDALONE_STATIC_PREVIEW`。不是 `FULL_PET`，不声明 Owner Acceptance。

## ACTUAL_WORKSPACE_AND_SOURCE

实际独立目录：`/Users/hj/Documents/Codex/2026-10-23/pets-plugin-work-pets-openai-curated/outputs/Nyra`。

输入是用户指定的 `TWOS_COMPANION_V3_HANDOFF_R1.zip`。读取了 README、GENERATED_ASSET_RECEIPT、CODEX_TASK、ART_BIBLE、IMAGE_PROMPTS、ACCEPTANCE、资产目录、动画状态、事件 schema/示例、声音方向/台词和审计器。原包、完整解压资料均保留。单主代理，无子代理，无另起重复 Pet 任务。

## V3_IDENTITY_AND_ASSET_INVENTORY

以夜璃 / Nyra、成年约 25 岁、黑紫猫耳为固定主形象。3 张综合图、8 张裁片、1 张来源参考实际到达；26 项原包文件校验通过。主预览图实际 302×517。

## IMAGE_SHEETS_VS_RUNTIME_ASSETS

图板/裁片均分类为参考，合格透明运行资产 **0**。没有 PSD 层、绑定、Live2D 或 3D。参考换装为半身 86×212，不能称完整服装套件。

## ALPHA_CROP_ANCHOR_AND_HASH_CHECKS

已逐项测实际像素、alpha 分布、SHA-256，并核对 8 个裁区。生成 PNG 实为 RGBA，纠正了交接文本的 RGB 说法；alpha 不构成人物轮廓遮罩。预览衍生裁区、源/输出哈希、`anchor=null` 和未对齐状态见 `assets/outfits.json`。

## FOUR_REAL_ANIMATION_LOOPS

**MISSING**。idle、working、gaze/head、success 都未制作合格动作序列。程序没有整张海报摇摆、缩放循环或伪造运动。所需尺寸、帧位、透明度、锚点、衣装同步、分层要求见 `MINIMUM_ASSETS.md`。

## DESKTOP_INPUT_FOCUS_AND_CLICK_THROUGH

实际验证过：独立启动；图像拖动后保存新坐标；放大/缩小；三种服装参考切换；全屏实际截图；退出全屏返回浮窗；隐藏；从访达重新打开同一个 App 恢复浮窗；菜单退出后进程不存在。重新打开未产生第二个进程。

日常浮动面板使用 nonactivating NSPanel，不能成为 key/main；展示页由用户主动打开并获得焦点。当前是可见不透明概念卡片，拦截区与可见矩形一致；没有透明边缘隐藏命中区，也没有全局鼠标轮询/事件 tap。

整窗穿透菜单已实现，入口始终在菜单栏；跨 App 底层点击与焦点保持尚未做完整实测。人物轮廓级 alpha 命中因缺合格素材未实现。多显示器真实断开、Spaces、睡眠唤醒、Intel 运行未测，不宣布完整 Gate B 通过。

拖动采用本面板自身 `mouseDown/mouseDragged/mouseUp`，首次鼠标事件可接收，释放后按屏幕可见区限制位置并保存。无全局输入监听。

## STATE_TRUTH_AND_APPROVAL_BOUNDARIES

手动示例“收到”不显示已开始；“执行结束”保持尚未核验；PARTIAL 不当成完成；验证通过与 Owner 接受分开；断线显示未知；无百分比来源则不显示百分比。所有示例均带 `SIMULATION`。没有审批、任务运行、交易或 URL 执行功能。

## SIMULATION_RESULT

**MANUAL_TEXT_EXAMPLES_ONLY**。是 UI 状态措辞示例，不是实时事件模拟器或协议适配器。原包的 JSONL/schema 被保留，程序不消费它们。事件去重、乱序隔离、终态回归/多任务仲裁、断线重连均未实现或测试，不以静态标签推导其通过。

## REAL_TWOS_READONLY_INTEGRATION

**BLOCKED / NOT_CONNECTED**。本阶段未扫描 TWOS 代码或数据，未验证其接口存在。最小接口缺口是一个经授权的本机只读最小事件通道；需后续独立核对。没有真实事件回执，不宣称联动成功。

## SYSTEM_TTS_PREVIEW_AND_CUSTOM_VOICE_STATUS

系统 TTS 未启用；没有任何声音播放。原创音频和音色 `NOT_PRODUCED`，口型同步未实现。原始方向文档和台词完整保留，不能称专属声音。

## PERFORMANCE_MEASUREMENT

设备：MacBookPro18,3，Apple M1 Pro，16 GiB RAM，macOS 27.0.1，arm64。采样只读指定 `NyraPreview` PID，按累计 CPU 时间差 / 单调时钟间隔计算单核百分比；5 秒取样，RSS 是常驻内存，不等于完整内存 footprint。

隐藏 60.018 秒：CPU 累计增量 0.00 秒（分辨率下约 0.00% 单核），最大 RSS 105.56 MiB。原始样本见 `reports/performance-hidden.json`。该隐藏测试在仅增加 reopen 恢复入口之前的同一静态实现上完成；不外推为最终动画性能。

最终构建空闲 300.016 秒：CPU 累计增量 0.00 秒（采样分辨率下约 0.00% 单核），最大 RSS 38.28 MiB，见 `reports/performance-idle.json`。这是重新启动后的静态浮窗；前述隐藏样本是在打开过全屏页后的暖进程上采集，两个 RSS 数值不作为同条件节省比例比较。

2 分钟动画 active 测试因无动画资产 **NOT_MEASURED / NOT_APPLICABLE_TO_STATIC_SCOPE**。没有宣布完整性能 Gate E 通过。静态显示无播放定时器，隐藏不刷新动画。

## OWNER_MAIN_PRODUCT_PRESERVATION

没有修改、替换、构建、关闭或重放 Owner 的 TWOS App、任务、业务代码、账本或认证资料。所有源码/配置/中间结果/交付物均在本次独立目录；开发时只重启夜璃自己的测试进程。未申请麦克风、录屏、辅助功能或全盘权限；无服务购买、自启、后台模型。

## ONE_LOCAL_PREVIEW_APP_OR_DMG

交付一个 `夜璃 Nyra Preview.app`，包含 arm64+x86_64 通用二进制、静态参考资源和默认关闭的模拟文字示例。另有启动脚本、全部源码、原始资料、审计/验证/截图与可分发 ZIP。未制作 DMG、开发者签名或公证。

离线构建成功，严格签名校验通过；7 项核心检查通过，覆盖负坐标屏幕恢复、超大窗口收敛、长宽比、状态真实性、模拟标记与素材路径越界。精确可执行文件哈希见 `reports/build-verification.json`。

GitHub 仅新建私有项目，标题“夜璃 · Nyra”、仓库地址名 `Nyra`。远端隐私和上传结果以回执及实际 main 树校验为准。没有 Tag、公开 Release 或站点。

## KNOWN_GAPS

正式透明主立绘、4 种真实动作、8 工作/8 交互/12 表情运行稿、同姿态换装套件、分层与绑定、原创音频、真实 TWOS 事件协议与适配、ChatGPT Pets v2 图集与其完整 QA、轮廓命中和跨 App/多屏/休眠完整回归均未完成。

## EXACT_OWNER_NEXT_ACTION

现在可双击 App 查看；菜单栏“◈ 夜璃”可隐藏/退出，隐藏后也能双击 App 恢复。需要完整动画桌宠时，先按 `MINIMUM_ASSETS.md` 补齐透明母版和四套动作；本次不要求重新选择 V2/V3，也不要求为静态预览修改 TWOS。
