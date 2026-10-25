# 夜璃 · Nyra

黑紫 V3 成年猫耳夜璃。R2 本轮已完成78张原生1024×1536运行PNG，并创建、选中唯一Nyra Pet；本机宠物列表可见与选中已由Owner确认。原独立App继续保留。

- **本次恢复新增13张运行画稿**：右跑5张、左跑8张；实际图像生成15次，另外2张是腿部层/中间稿。
- Pets最终v2：1536×2288、8×11、73有效槽+15透明空槽；本机结构/质量脚本和真实宿主预检均通过。
- 左右跑可辨、支撑腿交替；中段节奏仍有顿挫。斜向视线157.5°/247.5°较细微，已记录警告。
- P0独立App仍为20张唯一画稿/23槽/4组动作；换装、拖动、缩放、全屏、隐藏与退出保留。职场服装只有静态中立图，标记STATIC_OUTFIT_ONLY。
- 声音NOT_PRODUCED；TWOS NOT_CONNECTED；所有事件演示为SIMULATION。没有Live2D/3D模型，也未读取TWOS私人资料或修改主应用。
- R2未自动Commit、Push、Tag、Release或公开发布。现有私有GitHub仓库保留原状态。

双击 `夜璃 Nyra Preview.app` 或 `启动夜璃.command`。窗口上的−/+缩放，衣切换服装，⛶全屏，×隐藏；菜单栏◈夜璃可恢复/退出。独立App显示真实P0动画，另外保留3张明确标注的R1概念服装参考。

[完整交付与限制](R2_DELIVERY.md) · [当前生命周期回执](production-r2/reports/pets-readiness-final.json) · [全部素材哈希](production-r2/reports/artifact-hashes.json)

本轮唯一最新交付包：`dist/Nyra-R2-Pets.zip`。原`dist/Nyra-R2.zip`是65张时的历史检查点，原样保留；不要用它覆盖最新文件。

## 审片与重现

在production-r2中启动已有Python的本地服务器（已有8769服务时直接复用），打开：
- `http://127.0.0.1:8769/preview/atlas_review.html`：直接播放最终WebP的真实格子。
- `http://127.0.0.1:8769/preview/animation_review.html`：查看原生PNG。

离线GIF、MP4、逐帧图位于`production-r2/bundled-run/previews`及qa目录。最终图集为`production-r2/bundled-run/final/spritesheet-extended.webp`；可安装的本地包为`production-r2/pets-ready/nyra`。

`scripts/verify.py`检查原独立App；`scripts/package_r2.py --label R2-Pets`生成一次性、不覆盖的交付包。旧R1和R2报告、输入ZIP与失败画稿保留。实际宿主UI被自动化工具禁止访问，因此宿主全部动作的逐项实播尚未由代理验证；用户确认的列表/选中状态与浏览器实播证据分别记录。
