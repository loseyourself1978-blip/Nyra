# 独立App、Pets与TWOS联动是三个不同验收范围

## 1. 独立Nyra App

R1已证明静态预览的部分窗口交互。新动画要复用该App框架，不重写已通过拖动/隐藏/退出功能，也不能把旧静态CPU/RSS数据当作动画性能。

新P0至少检验：四套真实动画、无弹跳裁切、完整衣装、隐藏时停止动画、恢复无多实例、reduced motion时静帧、轮廓/窗口命中边界、全屏前后位置恢复。系统主目录、其他App和TWOS业务资料不读写。

## 2. 内置Pets

PNG放进仓库/ZIP、生成独立App、重启官方App，都不能代替Pet创建/导入/选中。按当前目标官方入口和实际创建skill处理，不编造API或配置路径、不直接修改内部数据库。

宿主的Running/Needs input/Ready/Blocked属于其线程活动语义；Ready不能在Nyra台词里扩展为“业务已独立验证、Owner已接受”。外观素材不能自行赋予TWOS事件读取、语音或审批能力。

## 3. TWOS只读联动

原包的JSON schema和示例是拟定契约，R1未连接。不得扫描TWOS业务库或读取私有prompt以“实现联动”。当前只补文档，不修改主TWOS。

后续单独批准的最小只读事件通道只接收：不透明execution/session ID、序号、时间、事件类型、通道/业务/验证状态；不需要持仓、病例、聊天正文、路径或凭据。保留去重、乱序拒绝、断线unknown、终态防回退及重试新attempt。

行为优先级：隐藏/静音/减少动画偏好先于表演；等待用户决定、失败、断线不被鼠标撒娇覆盖。completed独立于verification；PARTIAL不庆祝；owner.accepted与verification.passed分开。真实百分比缺失就不显示百分比。

本轮全部事件示例只能标SIMULATION，不能宣称真实TWOS联动或多任务仲裁已测。
