# 升级与卸载

## 升级

结束本机动作试播，从 Nyra 菜单正常退出。用新版已签名 App 替换应用程序中的 **Nyra.app** 后重新打开。TWOS 的内置组件随整个 TWOS App 更新，不要修改正在运行的 App 包内文件。新版接受前保留旧安装包。

生产环境内置与独立 Nyra 共用 `~/Library/Application Support/Nyra` 偏好。仅在共享设置不存在时迁移旧内置设置。正常退出保留显示/隐藏意愿，明确点击隐藏才改变该偏好；既有音量、静音、服装和大小继续保留。工程诊断目录另行隔离。

同一用户只运行一个兼容生产实例。打开另一兼容版本只向已有实例发送显示请求；不兼容时要求正常退出，不强杀或静默降级。TWOS 关闭不得杀死用户独立启动的 Nyra。

## 卸载

退出后，在 Finder 将所选 Nyra App 移到废纸篓。删除 TWOS 会移除它的内置组件，不删除独立 Nyra 或个人偏好；删除 Nyra 不删除 TWOS 项目，也不停止模型任务。Application Support 数据保留以便重装，删除它是用户另行明确决定的可选操作。本产品不自动注册开机登录项。

[English](UPGRADE_AND_UNINSTALL.en.md) · [README](../../README.zh-CN.md)
