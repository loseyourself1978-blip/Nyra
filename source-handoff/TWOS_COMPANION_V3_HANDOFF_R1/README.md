# TWOS V3 桌宠｜角色与工程交接包 R1

用户已选择最后一张 V2/V3 对比图的下半区 V3：黑紫、猫耳、深色长卷发、紫眼、成熟妩媚。reference/V3_SELECTED_REFERENCE.png 是对该已给定图的裁切引用，不是新绘制素材。

暂用角色名：**夜璃 · Nyra**（可配置显示名，不代表商标已注册）。角色明确为约25岁的成年原创动漫女性。

## 本次文件内容
- CODEX_TASK.md：可直接执行的完整专业工单。
- ART_BIBLE.md：固定造型、表情、动作、镜头及视觉一致性。
- IMAGE_PROMPTS.md：8张套图的完整生成要求和后续补图提示词。
- specs/asset_catalog.json：计划资产、图板拆分和运行时验证要求，**不是已完成资产清单**。
- specs/companion_event.schema.json：拟定的只读桌宠事件协议，**不宣称已存在于TWOS**。
- specs/animation_states.json：优先级、循环、过渡、状态真实性规则。
- specs/demo_events.jsonl：明确标记 simulator 的合成事件，不是业务回执。
- voice/VOICE_DIRECTION.md 与 voice/voice_lines.json：原创音色方向和中英台词，不含录音或音色模型。
- ACCEPTANCE.md：视觉、运行、只读事件、权限、性能和语音验收。
- tools/audit_assets.py：离线PNG与清单检查器，不自动抠图、不制造通过。
- SOURCES.md：工程参考的Apple官方文档。

## 素材真实性
本包最初在出图前准备，现已补入本次实际生成的3张合成设定图，以及从第一张的8个区块裁出的8张参考图。完整数据见 `GENERATED_ASSET_RECEIPT.md` 和 `specs/asset_catalog.json`。这些裁片不是独立高清重绘，不具备真实alpha；**可用于造型和实现参照，不冒称可直接绑定的最终sprite**。

图板是设计/切图来源，不能直接当成Live2D模型、PSD层、3D模型或已测试sprite atlas。Codex须审图、裁切、检测alpha、对齐、记录hash；无真实资产不得虚报完整。音色设计不是已经产出的女声，系统TTS仅允许标记为预览替代。

## 一条落地路线
原生macOS独立预览App + 2D状态动作素材 + 少量分层/逐帧动画 → 带模拟标记的事件演示 → 在实际接口许可范围内只读连接TWOS。不要重构TWOS、关闭主研发验收或扩大交易/专业权限。

## 执行位置
官方Codex新开一个独立会话“TWOS Companion V3｜夜璃”，目录建议 `/Users/hj/Downloads/twos-companion-v3`。该目录须在Codex里明确绑定；若已有无关文件，不覆盖。勿使用出行清单目录、LDD/Dashu业务目录或在正在修复的TWOS右栏执行自身扩展。

交接时直接附上本包（已包含3张实际综合设定图和8张裁切参考片），再粘贴CODEX_TASK.md全文。尚未交付8张独立高清透明运行素材，不能按已经齐备处理。先完成素材核查及独立可关闭的预览；预览不冒称正式动画桌宠，不自动替换 `/Applications/Tianma Work OS.app`。
