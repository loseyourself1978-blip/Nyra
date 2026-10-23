# TWOS-COMPANION-V3-NYRA-R1｜可直接粘贴Codex的完整指令

执行位置：**官方Codex独立桌宠开发会话**，建议名“TWOS Companion V3｜夜璃”。绑定明确独立目录 `/Users/hj/Downloads/twos-companion-v3`；若目录已存在先确认归属，不覆盖无关文件。不是出行清单业务会话，也不直接在Owner运行的TWOS产品上修改。

```text
START TWOS-COMPANION-V3-NYRA-R1
MODE: OPTIONAL_READONLY_DESKTOP_COMPANION
EXECUTION_SURFACE: OFFICIAL_CODEX_ISOLATED_COMPANION_THREAD
EXECUTE NOW
DO_NOT_START_DUPLICATE_JOB

一、目标和冻结范围

实现TWOS专属成年动漫女桌宠V3，暂用名“夜璃 / Nyra”。
以最新V2/V3对比图下半区的黑紫猫耳形象为唯一母版，
使用本包实际交付的3张综合设定图及8张裁切参考片，不回退至白紫V2或早期红发版本。
8张独立高清透明运行素材尚未完成，不将参考图当作它们的替代。
要求精细、优雅、妩媚、可爱；通过独立表情、姿态和动作表达。
首版选择原生macOS + 2D素材动画，暂不开发3D模型/Live2D编辑器。

这是一项可关闭的附加组件，不改变20.1/20.2已接受工作，
不把桌宠作为LDD运营/券商/专业Gate的前置条件。
不重做主产品登录、工作台、执行器或主线程调度。

二、先读材料和目录，不把规范当成现成资产

读取工程包的README、ART_BIBLE、IMAGE_PROMPTS、asset_catalog、
事件schema、animation_states、voice_lines、VOICE_DIRECTION和ACCEPTANCE。
先读取GENERATED_ASSET_RECEIPT.md：本次有3张合成图及从主图裁出的8张参考片，不是8张独立高清透明原稿。读取实际文件，建立ID到文件的对应及hash。
附件没到达就明确MISSING，并列准确缺项；不要声称看过。
角色参考是参考，不是PSD、Live2D rig、3D mesh或无缝sprite。
系统TTS是功能预览，不是已经制作好的专属声线。

核对当前Codex授权的独立cwd；建议目录如存在先保留内容。
TWOS研发仓库仅是可选只读接口参考：
/Users/hj/Downloads/tianma-work-os/.phase63a-worktree
不在其内直接实施桌宠，不扫描私人账本和认证文件。
不套用旧build；不直接替换/Applications/Tianma Work OS.app。
无同一桌宠作业再开始，已有执行则接续而非重建。

三、素材制作与验真

保留3张综合原图和8张裁切参考片原样，逐项审查同脸同衣、解剖、边缘、图板布局。
独立裁切透明运行时PNG；根据实际像素定位，不假定理想等分网格。
检查alpha、背景残留、标签、脚底和尾尖；棋盘格不是透明。
主立绘、8工作姿态、8交互姿态、12表情建立实际manifest，
记录真实宽高、crop rect、anchor、hash、source和人工可视检查。

没有可用动作素材时，先列缺项，不用无关立绘替代。
可实现STATIC_PREVIEW但不能将其报为完整动画桌宠。
不得通过裁头裁脚、拉伸身体、模糊或大幅整体缩放掩盖缺图。

先制作4个真实可区分的动画：
idle眨眼/呼吸；working手部或键盘动作；视线/头部跟随；成功短动作。
发梢、尾巴、眼睛、口型等使用真实独立图层或经验证的关键帧。
不宣称图板已自动成为Live2D；若只有音量驱动口型则标近似。

四、独立原生桌面组件

优先Swift/AppKit、NSPanel和系统图像/动画能力，复用本机工具链。
透明非激活浮动面板，不抢焦点，不要求注入Safari/其他App。
普通姿态默认高度约280pt，可调整；默认屏幕边缘、手动拖动。
提供菜单栏：显示/隐藏、复位位置、大小、静音、减少动态、退出。
关闭组件必须立即停止动画/音频/事件连接且不停止TWOS主程序。
首次不加入开机自启，不购买依赖，不新增后台常驻模型。

透明区域不拦截底层点击；可见身体允许轻点/拖动，菜单独立命中。
不要仅按矩形窗口吞点击；按实际alpha/hit-mask与系统行为验证。
默认不全局记录鼠标轨迹；跟随仅取当前指针位置、小幅目光/头部动作，
不做全局键盘监听、不读取其他App输入、不录屏、不启用麦克风。
不为桌宠申请不必要的辅助功能或全盘权限。
避开Dock/菜单栏与屏幕外；屏幕断开可恢复；不覆盖批准/发送按钮。

五、事件系统是只读观察，不是新的Agent

companion_event.schema.json是拟定协议，不假称TWOS已实现。
先实现明确标SIMULATION的演示器，覆盖所有状态。
再核对TWOS实际已公开/已授权的只读事件能力，做最薄映射适配。
仅通过已允许的本机受认证通道订阅最小字段，
不直接改/读完整业务数据库、不读取原始prompt、私人持仓、密码或日志正文。
桌宠不创建订单、改计划、批准、执行Codex、补跑任务或写财务。
没有只读事件通道时独立预览仍可完成，LIVE_INTEGRATION标BLOCKED，
列出一个最小接口缺口，不偷偷加高权限或让用户手工维护数据库。

真实性规则必须实现：
- 接收到指令只点头，不能立刻显示开始/成功。
- channel completed而business unverified/partial，不得庆祝完成。
- 等待批准只提示需要用户动作，桌宠不能替用户点批准。
- 验证通过和Owner接受分别表达。
- progress只有实际数值才显示百分比，无数值用忙碌状态。
- 模拟事件始终SIMULATION；断线显示状态未知。
- 重复event_id不重复动作/语音，按session/sequence/execution隔离乱序。
- 高优先级失败/批准状态不能被鼠标俏皮动作长期覆盖。

鼠标/动画事件不调用大模型；文本提示来自本地固定台词。
轻点只做角色反馈，安全菜单可以定位用户主动选择的现有任务页面，
但不自动操作其审批；从未信任事件任意打开URL或执行命令。

六、专属声音与低打扰

以VOICE_DIRECTION和voice_lines实现语音层。
先枚举本机已有系统声音，用户开启后试听；默认静音。
用系统TTS可标SYSTEM_TTS_PREVIEW，不写CUSTOM_VOICE_READY。
角色定制音色只能用用户已授权原创录音或合法服务，
未有现成音频就明确NOT_PRODUCED；禁止复制演员/主播/真人声线。
不购买、不充值、不默默下载新音色；不上传私人内容做TTS。

一次状态变化最多一句，冷却/合并/优先级遵循规范；
run.progress不连续播报，鼠标反应不连发撒娇语音。
静音、专注、隐藏始终优先，停止时清空过期音频。
口型真实音素同步与音量近似分别披露。

七、工程和验收节奏

先实现独立可交互预览App与真实图片动画，
再接本地模拟器与语音，最后只读接真实TWOS事件。
不让Owner等待全套复杂主产品回归才能先看桌宠，
但模拟预览不能冒充真实联动。

真实测试：启动/退出/拖动/命中穿透/恢复位置/隐藏/静音；
关键4种动画、表情可见且身份一致；
事件received/running/awaiting/partial/failed/verified正确；
重复与乱序、断线重连、不同任务事件不串台；
模拟和LIVE清楚区分；
输入焦点不丢、底层按钮可点击，桌宠不会替人批准；
性能按5分钟idle、2分钟active、1分钟hidden实际采样，
记录硬件和方法。目标是idle单核2%以内、active单核8%以内、RSS180MB以内，
这些是设计目标而非已实现事实，超出报告原因/降级，不伪造数字。

所有必要故障测试用隔离工程实例，不重放Owner原任务。
真实TWOS事件需工程任务实际产生；看见相同字样不算协议接入。
主产品无输入改变时不为桌宠重跑上千项全套，
若适配必须改主产品，先明确差异和权限，不能直接热改。

八、唯一交付与结果

交付独立TWOS Companion Preview.app，必要时单独本机DMG，
附可替换assets、manifest、事件映射、语音台词、可视预览和README。
保留图板与实际运行时资产区别；无法完成的分层/音色明示。
不覆盖主TWOS包、不远端Push/Tag/Release/公证；
独立项目可做必要本地源码提交，但不动原业务仓库和账本。
任何联网或额外服务费用需另行明确许可，不恢复旧调用次数限制。

沿现有报告习惯输出：
ACTUAL_WORKSPACE_AND_SOURCE
V3_IDENTITY_AND_ASSET_INVENTORY
IMAGE_SHEETS_VS_RUNTIME_ASSETS
ALPHA_CROP_ANCHOR_AND_HASH_CHECKS
FOUR_REAL_ANIMATION_LOOPS
DESKTOP_INPUT_FOCUS_AND_CLICK_THROUGH
STATE_TRUTH_AND_APPROVAL_BOUNDARIES
SIMULATION_RESULT
REAL_TWOS_READONLY_INTEGRATION
SYSTEM_TTS_PREVIEW_AND_CUSTOM_VOICE_STATUS
PERFORMANCE_MEASUREMENT
OWNER_MAIN_PRODUCT_PRESERVATION
ONE_LOCAL_PREVIEW_APP_OR_DMG
KNOWN_GAPS
EXACT_OWNER_NEXT_ACTION

只要有真实可运行预览就给准确可视启动步骤；
未完成的专属声音、分层动画、真实接口不能统称PASS。
不要求Owner再选择V2/V3，V3已定；不重新做其他三版。
现在开始独立桌宠工程：读真实V3素材，先做可拖动、可关闭、
有真实不同动作的桌宠，再按边界接TWOS只读进度和声音。
```
