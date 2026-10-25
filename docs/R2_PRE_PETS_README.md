# 夜璃 · Nyra

R2 独立 macOS 动画预览。黑紫 V3 成年猫耳造型；同一个独立 App 延续 R1 的拖动、缩放、一键换装、全屏、隐藏与退出。

**P0 已交付：20 张真实画稿 / 23 个槽位 / 4 组动作。完整 Pets 尚未完成：跑动质量门未通过，未创建或选中 Nyra。**

- 双击 `夜璃 Nyra Preview.app` 或 `启动夜璃.command` 启动。
- `− / +` 缩放，拖动卡片移动，`衣` 一键换装，`⛶` 全屏，`×` 隐藏。
- 菜单栏 `◈ 夜璃 → 退出夜璃` 完全退出；再次启动可恢复隐藏窗口。
- `动作` / 菜单可选择 idle、working、gaze/head、verified_success。事件演示始终为 **SIMULATION**。
- 原生职场透明图只有静态一张，标为 **STATIC_OUTFIT_ONLY**；另保留三张 R1 低清概念参考并明确标注。

[本轮交付状态和素材缺口](R2_DELIVERY.md) · [全部源文件及输出哈希](production-r2/reports/artifact-hashes.json) · [P0 验收](production-r2/reports/p0-final-audit.json) · [Pets 未完成原因](production-r2/reports/pets-readiness-final.json)

当前运行目录有 65 张原生 1024×1536 PNG；其中包含未验收的扩展候选和 3 张失败跑动族候选，不能把数量当作合格图集数量。独立 App 只打包已通过的 P0 动画。

声音 **NOT_PRODUCED**；TWOS **NOT_CONNECTED**；未读取 TWOS 私人资料，未改主应用。没有 Live2D/3D 模型。R2 未 Commit、Push、Tag、Release 或公开发布。原私有仓库 R1 保持不变。

## 本地审片

进入 `production-r2`，用本机已有 Python 启动 `python3 -m http.server 8769 --bind 127.0.0.1`，打开 `http://127.0.0.1:8769/preview/animation_review.html`，点击“加载当前工程 PNG”。缺帧动作禁播。关闭网页可结束审片；服务器在终端按 Ctrl-C 退出。

`production-r2/preview/rendered/` 另含离线 GIF 与逐帧图。播放计数只证明播放执行，画稿和宿主验收另记。

## 重建与校验

需要本机已有 Xcode Command Line Tools：`scripts/build.py` 构建，`scripts/verify.py` 验证当前 App。R2 打包用 `scripts/package_r2.py`。`scripts/package.py` 和 `verify_package.py` 是保留的 R1 历史流程，不用于 R2。

Apple Silicon / Intel 通用二进制，macOS 13+；实际设备验证为 Apple Silicon。本地 ad-hoc 签名，无开发者公证。

[R1 原始 README](docs/R1_README.md)、R1 报告和输入 ZIP 原样保留在工程中。
