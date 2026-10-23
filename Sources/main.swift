import AppKit
import Darwin

let ink = NSColor(calibratedRed: 0.075, green: 0.062, blue: 0.105, alpha: 1)
let violet = NSColor(calibratedRed: 0.70, green: 0.57, blue: 0.91, alpha: 1)

func text(_ title: String, size: CGFloat = 12, color: NSColor = .white) -> NSTextField {
    let view = NSTextField(labelWithString: title)
    view.font = .systemFont(ofSize: size)
    view.textColor = color
    view.maximumNumberOfLines = 0
    view.lineBreakMode = .byWordWrapping
    return view
}

func button(_ title: String, _ target: AnyObject, _ action: Selector, hint: String) -> NSButton {
    let b = NSButton(title: title, target: target, action: action)
    b.bezelStyle = .rounded
    b.toolTip = hint
    b.setAccessibilityLabel(hint)
    return b
}

final class PetPanel: NSPanel {
    override var canBecomeKey: Bool { false }
    override var canBecomeMain: Bool { false }
}

final class ArtView: NSView {
    override func acceptsFirstMouse(for event: NSEvent?) -> Bool { true }
    var image: NSImage?
    var onDragEnd: (() -> Void)?
    var onZoom: ((CGFloat) -> Void)?
    var onMenu: ((NSEvent) -> Void)?
    var dragStartScreen: NSPoint?
    var dragStartOrigin: NSPoint?
    override func draw(_ dirtyRect: NSRect) {
        super.draw(dirtyRect)
        guard let image = image else { return }
        let fitted = Geometry.fit(image: image.size, in: bounds)
        // Supplied art has a baked panel background; display it honestly on white.
        NSColor.white.setFill()
        fitted.fill()
        image.draw(in: fitted, from: .zero, operation: .sourceOver, fraction: 1,
                   respectFlipped: true, hints: [.interpolation: NSImageInterpolation.high])
    }
    override func mouseDown(with event: NSEvent) {
        guard let window = window, window is PetPanel else { return }
        dragStartScreen = window.convertPoint(toScreen: event.locationInWindow)
        dragStartOrigin = window.frame.origin
    }
    override func mouseDragged(with event: NSEvent) {
        guard let window = window, let start = dragStartScreen, let origin = dragStartOrigin else { return }
        let point = window.convertPoint(toScreen: event.locationInWindow)
        window.setFrameOrigin(NSPoint(x: origin.x+point.x-start.x, y: origin.y+point.y-start.y))
    }
    override func mouseUp(with event: NSEvent) {
        dragStartScreen = nil; dragStartOrigin = nil; onDragEnd?()
    }
    override func rightMouseDown(with event: NSEvent) { onMenu?(event) }
    override func scrollWheel(with event: NSEvent) {
        guard abs(event.scrollingDeltaY) > 0.1 else { return }
        onZoom?(event.scrollingDeltaY > 0 ? 1.08 : 0.92)
    }
    override func magnify(with event: NSEvent) { onZoom?(1 + event.magnification) }
}

final class PanelView: NSView {
    override func acceptsFirstMouse(for event: NSEvent?) -> Bool { true }
    var art = ArtView()
    let badge = text("STATIC_PREVIEW", size: 9, color: violet)
    let detail = text("", size: 9, color: .lightGray)
    var controls: [NSButton] = []
    var onDragEnd: (() -> Void)?
    var dragStartScreen: NSPoint?
    var dragStartOrigin: NSPoint?
    override init(frame: NSRect) {
        super.init(frame: frame)
        addSubview(badge); addSubview(art); addSubview(detail)
    }
    required init?(coder: NSCoder) { fatalError() }
    var visiblePath: NSBezierPath {
        NSBezierPath(roundedRect: bounds.insetBy(dx: 7, dy: 7), xRadius: 14, yRadius: 14)
    }
    func visibleHit(_ point: NSPoint) -> Bool { visiblePath.contains(point) }
    override func draw(_ dirtyRect: NSRect) {
        ink.setFill(); bounds.fill()
        violet.withAlphaComponent(0.35).setStroke(); visiblePath.lineWidth = 1; visiblePath.stroke()
    }
    override func layout() {
        super.layout()
        badge.frame = NSRect(x: 17, y: bounds.height-29, width: bounds.width-34, height: 15)
        art.frame = NSRect(x: 17, y: 72, width: bounds.width-34, height: bounds.height-108)
        detail.frame = NSRect(x: 17, y: 47, width: bounds.width-34, height: 23)
        let width = (bounds.width-34)/CGFloat(max(1, controls.count))
        for (i, b) in controls.enumerated() {
            b.frame = NSRect(x: 17+CGFloat(i)*width, y: 14, width: width-2, height: 27)
        }
    }
    override func mouseDown(with event: NSEvent) {
        guard let window = window else { return }
        dragStartScreen = window.convertPoint(toScreen: event.locationInWindow)
        dragStartOrigin = window.frame.origin
    }
    override func mouseDragged(with event: NSEvent) {
        guard let window = window, let start = dragStartScreen, let origin = dragStartOrigin else { return }
        let point = window.convertPoint(toScreen: event.locationInWindow)
        window.setFrameOrigin(NSPoint(x: origin.x+point.x-start.x, y: origin.y+point.y-start.y))
    }
    override func mouseUp(with event: NSEvent) {
        dragStartScreen = nil; dragStartOrigin = nil; onDragEnd?()
    }
}

final class StageView: NSView {
    let art = ArtView()
    let title = text("夜璃 · Nyra", size: 27)
    let subtitle = text("V3 / 黑紫成年猫耳 / STATIC_PREVIEW", size: 12, color: violet)
    let note = text("", size: 12, color: .lightGray)
    let truth = text("", size: 12, color: violet)
    let quality = text("", size: 11, color: .lightGray)
    let boundary = text("静态参考预览 · 动画素材缺失 · 原创声音未制作 · TWOS 未连接", size: 11, color: .lightGray)
    var wardrobe: NSSegmentedControl!
    var actions: [NSButton] = []
    var previewOutfit: Outfit?
    override init(frame: NSRect) {
        super.init(frame: frame)
        wantsLayer = true; layer?.backgroundColor = ink.cgColor
        for view in [art, title, subtitle, note, truth, quality, boundary] as [NSView] { addSubview(view) }
        art.onDragEnd = nil
    }
    required init?(coder: NSCoder) { fatalError() }
    override func layout() {
        super.layout()
        let w = bounds.width, h = bounds.height
        title.frame = NSRect(x: 28, y: h-62, width: w-56, height: 36)
        subtitle.frame = NSRect(x: 29, y: h-85, width: w-58, height: 20)
        wardrobe?.frame = NSRect(x: 28, y: h-127, width: min(540, w-56), height: 30)
        note.frame = NSRect(x: 29, y: h-174, width: w-58, height: 40)
        art.frame = NSRect(x: 28, y: 152, width: w-56, height: max(50, h-342))
        quality.frame = NSRect(x: 29, y: 124, width: w-58, height: 24)
        truth.frame = NSRect(x: 29, y: 97, width: w-58, height: 24)
        boundary.frame = NSRect(x: 29, y: 73, width: w-58, height: 22)
        for (i,b) in actions.enumerated() {
            b.frame = NSRect(x: 28+CGFloat(i)*126, y: 25, width: 120, height: 32)
        }
        if let outfit = previewOutfit {
            let shown = Geometry.fit(image: CGSize(width: outfit.width, height: outfit.height), in: art.bounds)
            let factor = shown.height/CGFloat(outfit.height)*(window?.backingScaleFactor ?? 1)
            quality.stringValue = String(format: "源图 %d × %d px · 当前显示约 %.1f× 源像素%@", outfit.width, outfit.height, factor,
                                         factor > 1 ? " · 放大会显像素；未提升原始清晰度" : "")
        }
    }
}

final class Companion: NSObject, NSApplicationDelegate, NSWindowDelegate {
    var wardrobe: Wardrobe!
    var images: [String: NSImage] = [:]
    var selected = 0
    var panel: PetPanel!
    var panelView: PanelView!
    var stage: NSWindow?
    var stageView: StageView?
    var status: NSStatusItem!
    var desiredHeight: CGFloat = 280
    var passThrough = false
    var demo: DemoState = .none
    var screenObserver: NSObjectProtocol?
    let resources = Bundle.main.resourceURL!
    var lockFD: Int32 = -1
    var stateDirectory: URL { Bundle.main.bundleURL.deletingLastPathComponent().appendingPathComponent(".local", isDirectory: true) }
    var prefsURL: URL { stateDirectory.appendingPathComponent("preview-settings.json") }

    func applicationDidFinishLaunching(_ notification: Notification) {
        do {
            try FileManager.default.createDirectory(at: stateDirectory, withIntermediateDirectories: true)
            lockFD = open(stateDirectory.appendingPathComponent("preview.lock").path, O_CREAT | O_RDWR, 0o600)
            guard lockFD >= 0, flock(lockFD, LOCK_EX | LOCK_NB) == 0 else {
                // A second instance exits without creating a duplicate window or job.
                if lockFD >= 0 { close(lockFD); lockFD = -1 }
                NSApp.terminate(nil); return
            }
            let data = try Data(contentsOf: resources.appendingPathComponent("assets/outfits.json"))
            wardrobe = try JSONDecoder().decode(Wardrobe.self, from: data).validated()
            for outfit in wardrobe.outfits {
                let path = resources.appendingPathComponent("assets/"+outfit.file)
                guard let image = NSImage(contentsOf: path) else { throw PreviewError.imageMissing(outfit.file) }
                image.size = NSSize(width: outfit.width, height: outfit.height)
                images[outfit.id] = image
            }
            NSApp.setActivationPolicy(.accessory)
            makeMainMenu()
            status = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
            status.button?.title = "◈ 夜璃"
            status.button?.toolTip = "夜璃 · Nyra｜独立概念预览"
            makePanel()
            restoreSettings()
            updateOutfit()
            showPanel()
            screenObserver = NotificationCenter.default.addObserver(forName: NSApplication.didChangeScreenParametersNotification,
                                                                     object: nil, queue: .main) { [weak self] _ in self?.clampPanel() }
            rebuildMenu()
        } catch {
            let alert = NSAlert()
            alert.messageText = "夜璃预览无法启动"
            alert.informativeText = "素材或目录不可用：\(error)。请从完整交付目录启动。"
            alert.runModal()
            NSApp.terminate(nil)
        }
    }

    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool {
        if panel != nil { showPanel() }
        return false
    }

    func makeMainMenu() {
        let menu = NSMenu()
        let item = NSMenuItem(); let appMenu = NSMenu()
        let quit = NSMenuItem(title: "退出夜璃", action: #selector(quit), keyEquivalent: "q")
        quit.target = self; appMenu.addItem(quit); item.submenu = appMenu
        menu.addItem(item); NSApp.mainMenu = menu
    }

    func makePanel() {
        panel = PetPanel(contentRect: NSRect(x: 100, y: 100, width: 220, height: 388),
                         styleMask: [.borderless, .nonactivatingPanel], backing: .buffered, defer: false)
        panel.title = "夜璃 · Nyra｜STATIC_PREVIEW"
        panel.appearance = NSAppearance(named: .darkAqua)
        // This phase has baked reference panels, not a transparent character matte.
        // Keep every intercepted pixel visibly part of the opaque concept card.
        panel.isOpaque = true; panel.backgroundColor = ink
        panel.hasShadow = false; panel.level = .floating
        panel.hidesOnDeactivate = false; panel.isReleasedWhenClosed = false
        panel.isMovableByWindowBackground = true
        panel.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
        panel.acceptsMouseMovedEvents = true
        panelView = PanelView(frame: panel.contentView!.bounds)
        panel.contentView = panelView
        panelView.art.onDragEnd = { [weak self] in self?.clampPanel(); self?.saveSettings() }
        panelView.onDragEnd = panelView.art.onDragEnd
        panelView.art.onZoom = { [weak self] f in self?.resize(factor: f) }
        panelView.art.onMenu = { [weak self] event in
            guard let self = self, let menu = self.status.menu else { return }
            NSMenu.popUpContextMenu(menu, with: event, for: self.panelView.art)
        }
        let specs: [(String, Selector, String)] = [
            ("−", #selector(smaller), "缩小夜璃"), ("+", #selector(larger), "放大夜璃"),
            ("衣", #selector(nextOutfit), "一键换装（概念参考）"),
            ("⛶", #selector(fullscreen), "全屏幕展示"), ("×", #selector(hideAll), "隐藏夜璃")]
        panelView.controls = specs.map { button($0.0, self, $0.1, hint: $0.2) }
        for b in panelView.controls { panelView.addSubview(b) }
        let screen = currentScreen().visibleFrame
        panel.setFrameOrigin(NSPoint(x: screen.maxX-panel.frame.width-24, y: screen.minY+40))
    }

    func currentScreen() -> NSScreen {
        panel.screen ?? NSScreen.main ?? NSScreen.screens[0]
    }

    func resize(factor: CGFloat) {
        guard factor.isFinite, factor > 0 else { return }
        desiredHeight = min(max(desiredHeight*factor, 160), max(160, currentScreen().visibleFrame.height-138))
        setPanelSize(); saveSettings()
    }
    func setPanelSize() {
        guard panel != nil else { return }
        let available = currentScreen().visibleFrame
        let artHeight = min(desiredHeight, max(100, available.height-138))
        let outfit = wardrobe.outfits[selected]
        let width = max(220, artHeight*CGFloat(outfit.width)/CGFloat(outfit.height)+34)
        let origin = panel.frame.origin
        panel.setFrame(Geometry.clamp(NSRect(x: origin.x, y: origin.y, width: width, height: artHeight+108), to: available), display: true)
        panelView.needsLayout = true
        updateHitTesting()
    }
    @objc func smaller() { resize(factor: 0.85) }
    @objc func larger() { resize(factor: 1.18) }
    @objc func resetPosition() {
        let screen = currentScreen().visibleFrame
        panel.setFrameOrigin(NSPoint(x: screen.maxX-panel.frame.width-24, y: screen.minY+40))
        clampPanel(); saveSettings()
    }
    func clampPanel() {
        guard panel != nil, !NSScreen.screens.isEmpty else { return }
        let screen = NSScreen.screens.max { a, b in
            let ia = a.visibleFrame.intersection(panel.frame), ib = b.visibleFrame.intersection(panel.frame)
            return ia.width*ia.height < ib.width*ib.height
        }!
        panel.setFrame(Geometry.clamp(panel.frame, to: screen.visibleFrame), display: true)
        updateHitTesting()
    }

    func updateHitTesting() {
        guard panel != nil else { return }
        panel.ignoresMouseEvents = passThrough
    }
    @objc func showPanel() {
        if let stage = stage { stage.orderOut(nil) }
        panel.orderFrontRegardless(); clampPanel(); updateHitTesting(); rebuildMenu()
    }
    @objc func hideAll() {
        panel.orderOut(nil); stage?.orderOut(nil)
        rebuildMenu()
    }
    @objc func toggleVisibility() {
        if panel.isVisible || stage?.isVisible == true { hideAll() } else { showPanel() }
    }
    @objc func togglePassThrough() {
        passThrough.toggle(); updateHitTesting(); rebuildMenu()
    }

    @objc func nextOutfit() {
        selected = (selected+1)%wardrobe.outfits.count
        updateOutfit(); saveSettings()
    }
    @objc func selectOutfit(_ sender: NSMenuItem) {
        selected = sender.tag; updateOutfit(); saveSettings()
    }
    @objc func selectSegment(_ sender: NSSegmentedControl) {
        selected = sender.selectedSegment; updateOutfit(); saveSettings()
    }
    func updateOutfit() {
        let outfit = wardrobe.outfits[selected]
        panelView.art.image = images[outfit.id]; panelView.art.needsDisplay = true
        panelView.detail.stringValue = "\(outfit.name)\n\(outfit.width)×\(outfit.height) · 静态参考"
        stageView?.art.image = images[outfit.id]; stageView?.art.needsDisplay = true
        stageView?.note.stringValue = outfit.note
        stageView?.wardrobe.selectedSegment = selected
        stageView?.previewOutfit = outfit
        stageView?.truth.stringValue = demo.label
        stageView?.needsLayout = true
        setPanelSize(); rebuildMenu()
    }

    func makeStage() {
        let w = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 900, height: 800),
                         styleMask: [.titled, .closable, .miniaturizable, .resizable], backing: .buffered, defer: false)
        w.title = "夜璃 · Nyra｜概念预览与换装"
        w.appearance = NSAppearance(named: .darkAqua)
        w.minSize = NSSize(width: 720, height: 620)
        w.isReleasedWhenClosed = false; w.delegate = self
        w.collectionBehavior = [.fullScreenPrimary]
        let view = StageView(frame: w.contentView!.bounds)
        view.wardrobe = NSSegmentedControl(labels: wardrobe.outfits.map(\.name), trackingMode: .selectOne,
                                          target: self, action: #selector(selectSegment))
        view.wardrobe.setAccessibilityLabel("服装概念参考选择")
        view.addSubview(view.wardrobe)
        view.actions = [button("回到桌面", self, #selector(backToDesktop), hint: "回到浮动桌宠"),
                        button("全屏 / 返回", self, #selector(fullscreen), hint: "切换全屏展示"),
                        button("模拟状态", self, #selector(showDemoMenu), hint: "SIMULATION 状态文字示例"),
                        button("隐藏", self, #selector(hideAll), hint: "隐藏全部预览"),
                        button("退出夜璃", self, #selector(quit), hint: "完全退出独立夜璃进程")]
        view.actions.forEach { view.addSubview($0) }
        w.contentView = view
        stage = w; stageView = view
        w.center()
    }
    @objc func showStage() {
        if stage == nil { makeStage() }
        panel.orderOut(nil)
        updateOutfit()
        stage!.makeKeyAndOrderFront(nil); NSApp.activate(ignoringOtherApps: true)
        rebuildMenu()
    }
    @objc func fullscreen() {
        if stage?.isVisible != true { showStage() }
        stage?.toggleFullScreen(nil)
    }
    @objc func backToDesktop() {
        if stage?.styleMask.contains(.fullScreen) == true {
            stage?.toggleFullScreen(nil)
            pendingDesktop = true
        } else { showPanel() }
    }
    var pendingDesktop = false
    func windowDidExitFullScreen(_ notification: Notification) {
        if pendingDesktop { pendingDesktop = false; showPanel() }
    }
    func windowShouldClose(_ sender: NSWindow) -> Bool {
        hideAll(); return false
    }
    @objc func showDemoMenu(_ sender: NSButton) {
        let menu = makeDemoMenu()
        menu.popUp(positioning: nil, at: NSPoint(x: 0, y: sender.bounds.maxY), in: sender)
    }
    func makeDemoMenu() -> NSMenu {
        let menu = NSMenu(title: "SIMULATION")
        for (i,state) in DemoState.allCases.enumerated() {
            let item = NSMenuItem(title: state.menuTitle, action: #selector(selectDemo), keyEquivalent: "")
            item.target = self; item.tag = i; item.state = state == demo ? .on : .off
            menu.addItem(item)
        }
        return menu
    }
    @objc func selectDemo(_ sender: NSMenuItem) {
        demo = DemoState.allCases[sender.tag]
        stageView?.truth.stringValue = demo.label
        rebuildMenu()
    }
    func rebuildMenu() {
        guard status != nil, wardrobe != nil else { return }
        let menu = NSMenu()
        @discardableResult func item(_ title: String, _ action: Selector?, key: String = "") -> NSMenuItem {
            let i = NSMenuItem(title: title, action: action, keyEquivalent: key)
            i.target = self; menu.addItem(i); return i
        }
        item("夜璃 · Nyra  /  STATIC_PREVIEW", nil)
        item("显示 / 隐藏", #selector(toggleVisibility))
        item("打开概念预览与换装", #selector(showStage))
        item("全屏幕展示 / 返回", #selector(fullscreen))
        item("一键换装（切换概念参考）", #selector(nextOutfit))
        let wardrobeItem = item("选择服装参考", nil)
        let outfits = NSMenu()
        for (index,outfit) in wardrobe.outfits.enumerated() {
            let i = NSMenuItem(title: outfit.name, action: #selector(selectOutfit), keyEquivalent: "")
            i.target = self; i.tag = index; i.state = index == selected ? .on : .off; outfits.addItem(i)
        }
        wardrobeItem.submenu = outfits
        menu.addItem(.separator())
        item("放大", #selector(larger)); item("缩小", #selector(smaller))
        item("复位位置", #selector(resetPosition))
        let passthrough = item("整窗点击穿透（从菜单栏恢复）", #selector(togglePassThrough))
        passthrough.state = passThrough ? .on : .off
        menu.addItem(.separator())
        item("SIMULATION · 状态文字示例", nil).submenu = makeDemoMenu()
        item("TWOS：未连接 / LIVE BLOCKED", nil)
        item("静音 · 无音频 / CUSTOM_VOICE NOT_PRODUCED", nil)
        item("减少动态：静态预览，无动画播放", nil)
        menu.addItem(.separator())
        item("退出夜璃", #selector(quit), key: "q")
        status.menu = menu
        NSApp.mainMenu?.items.first?.submenu = menu.copy() as? NSMenu
    }

    func saveSettings() {
        guard panel != nil, wardrobe != nil else { return }
        let data: [String: Any] = ["outfit": wardrobe.outfits[selected].id, "height": desiredHeight,
                                   "x": panel.frame.minX, "y": panel.frame.minY]
        if let bytes = try? JSONSerialization.data(withJSONObject: data, options: [.prettyPrinted, .sortedKeys]) {
            try? bytes.write(to: prefsURL, options: .atomic)
        }
    }
    func restoreSettings() {
        guard let data = try? Data(contentsOf: prefsURL),
              let prefs = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return }
        if let id = prefs["outfit"] as? String, let index = wardrobe.outfits.firstIndex(where: { $0.id == id }) { selected = index }
        if let height = prefs["height"] as? Double, height.isFinite { desiredHeight = min(max(height, 160), 1000) }
        if let x = prefs["x"] as? Double, let y = prefs["y"] as? Double, x.isFinite, y.isFinite {
            panel.setFrameOrigin(NSPoint(x: x, y: y))
        }
        clampPanel()
    }
    @objc func quit() { NSApp.terminate(nil) }
    func applicationWillTerminate(_ notification: Notification) {
        if let observer = screenObserver { NotificationCenter.default.removeObserver(observer) }
        saveSettings()
        if lockFD >= 0 { flock(lockFD, LOCK_UN); close(lockFD); lockFD = -1 }
        if status != nil { NSStatusBar.system.removeStatusItem(status) }
    }
}

if CommandLine.arguments.contains("--self-test") {
    do { try runCoreTests() } catch { fputs("FAIL: \(error)\n", stderr); exit(1) }
} else {
    let app = NSApplication.shared
    let companion = Companion()
    app.delegate = companion
    app.run()
}
