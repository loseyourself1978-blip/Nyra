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
    var image: NSImage? { didSet { rebuildMask() } }
    private var alphaMask = [UInt8](repeating: 0, count: 64*96*4)
    func rebuildMask() {
        guard let cg = image?.cgImage(forProposedRect: nil, context: nil, hints: nil) else { return }
        alphaMask.withUnsafeMutableBytes { bytes in
            guard let ctx = CGContext(data: bytes.baseAddress, width: 64, height: 96, bitsPerComponent: 8,
                bytesPerRow: 64*4, space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { return }
            ctx.clear(CGRect(x: 0, y: 0, width: 64, height: 96))
            ctx.draw(cg, in: CGRect(x: 0, y: 0, width: 64, height: 96))
        }
    }
    func containsArt(_ point: NSPoint) -> Bool {
        guard let image = image else { return false }
        let rect = Geometry.fit(image: image.size, in: bounds)
        guard rect.contains(point) else { return false }
        if !isRuntime { return true }
        let x = min(63,max(0,Int((point.x-rect.minX)/rect.width*64)))
        let y = min(95,max(0,Int((rect.maxY-point.y)/rect.height*96)))
        return alphaMask[(y*64+x)*4+3] > 16
    }
    var isRuntime = false
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
        if !isRuntime { NSColor.white.setFill(); fitted.fill() }
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
        art.frame = NSRect(x: 28, y: 78, width: w-56, height: max(50, h-208))
        note.isHidden = true; quality.isHidden = true; truth.isHidden = true
        quality.frame = NSRect(x: 29, y: 124, width: w-58, height: 24)
        truth.frame = NSRect(x: 29, y: 97, width: w-58, height: 24)
        boundary.frame = NSRect(x: 29, y: 61, width: w-58, height: 17)
        let actionWidth = min(126, (w-56)/CGFloat(max(1, actions.count)))
        for (i,b) in actions.enumerated() {
            b.frame = NSRect(x: 28+CGFloat(i)*actionWidth, y: 25, width: actionWidth-6, height: 32)
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
    let sound = NyraAudio()
    var soundPopover: NSPopover?
    var hoverTimer: Timer?
    var resizeStartHeight: CGFloat = 280
    let animationNames = ["idle", "working", "gaze_head", "verified_success", "running_right", "running_left", "waving", "jumping", "failed", "waiting", "review", "look_around"]
    let animationLabels = ["待机", "专注工作", "抬头注视", "庆祝", "向右跑", "向左跑", "挥手", "跳跃", "失落", "等待", "阅读", "环顾四周"]
    var desiredHeight: CGFloat = 400
    var passThrough = false
    var demo: DemoState = .none
    var screenObserver: NSObjectProtocol?
    var motionObserver: NSObjectProtocol?
    var runtimePlan: RuntimePlan?
    var frameCursor: FrameCursor?
    var frameImages: [String: NSImage] = [:]
    var frameTimer: Timer?
    var animationName = "idle"
    var displayedFrames: [String: Int] = [:]
    let resources = Bundle.main.resourceURL!
    var lockFD: Int32 = -1
    var stateDirectory: URL {
        FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0].appendingPathComponent("Nyra", isDirectory: true)
    }
    var prefsURL: URL { stateDirectory.appendingPathComponent("preview-settings.json") }

    func applicationDidFinishLaunching(_ notification: Notification) {
        do {
            try FileManager.default.createDirectory(at: stateDirectory, withIntermediateDirectories: true)
            let legacySettings = Bundle.main.bundleURL.deletingLastPathComponent().appendingPathComponent(".local/preview-settings.json")
            if !FileManager.default.fileExists(atPath: prefsURL.path), FileManager.default.fileExists(atPath: legacySettings.path) {
                try FileManager.default.copyItem(at: legacySettings, to: prefsURL)
            }
            lockFD = open(stateDirectory.appendingPathComponent("preview.lock").path, O_CREAT | O_RDWR, 0o600)
            guard lockFD >= 0, flock(lockFD, LOCK_EX | LOCK_NB) == 0 else {
                // A second instance exits without creating a duplicate window or job.
                if lockFD >= 0 { close(lockFD); lockFD = -1 }
                NSApp.terminate(nil); return
            }
            sound.customDirectory = stateDirectory
            let data = try Data(contentsOf: resources.appendingPathComponent("assets/outfits.json"))
            wardrobe = try JSONDecoder().decode(Wardrobe.self, from: data).validated()
            let runtimeData = try Data(contentsOf: resources.appendingPathComponent("runtime/standalone_r3.json"))
            runtimePlan = try JSONDecoder().decode(RuntimePlan.self, from: runtimeData).validated()
            for id in Set(runtimePlan!.sequences.values.flatMap(\.assetIDs)) {
                guard FileManager.default.fileExists(atPath: resources.appendingPathComponent("runtime/default/\(id).png").path)
                else { throw PreviewError.imageMissing(id) }
            }
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
            status.button?.toolTip = "夜璃 · Nyra｜悬停 + 控制环"
            makePanel()
            restoreSettings()
            updateOutfit()
            showPanel()
            screenObserver = NotificationCenter.default.addObserver(forName: NSApplication.didChangeScreenParametersNotification,
                                                                     object: nil, queue: .main) { [weak self] _ in self?.clampPanel() }
            motionObserver = NSWorkspace.shared.notificationCenter.addObserver(forName: NSWorkspace.accessibilityDisplayOptionsDidChangeNotification,
                object: nil, queue: .main) { [weak self] _ in
                    guard let self = self else { return }
                    self.playAnimation(self.animationName)
                }
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
        if panel != nil && !panel.isVisible && stage?.isVisible != true { showPanel() }
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
        panel.title = "夜璃 · Nyra｜交互桌宠"
        panel.appearance = NSAppearance(named: .darkAqua)
        panel.isOpaque = false; panel.backgroundColor = .clear
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
            ("tshirt", #selector(nextOutfit), "一键换装 · 黑紫 / 职场"),
            ("arrow.up.left.and.arrow.down.right", #selector(fullscreen), "全屏幕展示"),
            ("speaker.wave.2", #selector(showSound), "声音 · 试听 / 静音 / 音量"),
            ("play.fill", #selector(showAnimationMenu), "选择动作"),
            ("minus", #selector(smaller), "缩小夜璃"),
            ("plus", #selector(larger), "放大夜璃"),
            ("eye.slash", #selector(hideAll), "隐藏夜璃 · 菜单栏可恢复"),
            ("power", #selector(quit), "退出夜璃")]
        panelView.controls = specs.map { orbitButton($0.0, title: $0.2, target: self, action: $0.1) }
        for b in panelView.controls { panelView.addSubview(b) }
        panelView.configureHub()
        panelView.grip.onBegin = { [weak self] in self?.resizeStartHeight = self?.desiredHeight ?? 280 }
        panelView.grip.onResize = { [weak self] delta in
            guard let self = self else { return }
            self.desiredHeight = min(max(self.resizeStartHeight+delta,160),max(160,self.currentScreen().visibleFrame.height-64))
            self.setPanelSize()
        }
        panelView.grip.onEnd = { [weak self] in self?.saveSettings(); self?.writePlaybackState("drag_resize") }
        let screen = currentScreen().visibleFrame
        panel.setFrameOrigin(NSPoint(x: screen.maxX-panel.frame.width-24, y: screen.minY+40))
    }

    func currentScreen() -> NSScreen {
        panel.screen ?? NSScreen.main ?? NSScreen.screens[0]
    }

    func resize(factor: CGFloat) {
        guard factor.isFinite, factor > 0 else { return }
        desiredHeight = min(max(desiredHeight*factor, 160), max(160, currentScreen().visibleFrame.height-64))
        setPanelSize(); saveSettings()
    }
    func setPanelSize() {
        guard panel != nil else { return }
        let available = currentScreen().visibleFrame
        let artHeight = min(desiredHeight, max(100, available.height-64))
        let outfit = wardrobe.outfits[selected]
        let width = max(320, artHeight*CGFloat(outfit.width)/CGFloat(outfit.height)+70)
        let origin = panel.frame.origin
        panel.setFrame(Geometry.clamp(NSRect(x: origin.x, y: origin.y, width: width, height: artHeight+52), to: available), display: true)
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
        guard NSEvent.pressedMouseButtons == 0 else { return }
        panelView.layoutSubtreeIfNeeded()
        let point = panelView.convert(panel.convertPoint(fromScreen: NSEvent.mouseLocation), from: nil)
        let near = panelView.bounds.insetBy(dx: -8, dy: -8).contains(point)
        panelView.setHovered(near)
        panel.ignoresMouseEvents = passThrough || !panelView.visibleHit(point)
    }
    func startHoverTimer() {
        hoverTimer?.invalidate()
        let t = Timer(timeInterval: 0.1, repeats: true) { [weak self] _ in self?.updateHitTesting() }
        t.tolerance = 0.03; hoverTimer = t; RunLoop.main.add(t, forMode: .common)
    }
    @objc func showPanel() {
        if stage?.styleMask.contains(.fullScreen) == true {
            pendingDesktop = true; stage?.toggleFullScreen(nil); return
        }
        if let stage = stage { stage.orderOut(nil) }
        panel.orderFrontRegardless(); clampPanel(); startHoverTimer(); updateHitTesting(); playAnimation(animationName); rebuildMenu()
    }
    @objc func hideAll() {
        hoverTimer?.invalidate(); hoverTimer = nil; sound.stop(); soundPopover?.close()
        stopFrameTimer()
        panel.orderOut(nil)
        if stage?.styleMask.contains(.fullScreen) == true {
            pendingHide = true; stage?.toggleFullScreen(nil)
        } else { stage?.orderOut(nil) }
        writePlaybackState("hidden")
        rebuildMenu()
    }
    @objc func toggleVisibility() {
        if panel.isVisible || stage?.isVisible == true { hideAll() } else { showPanel() }
    }
    @objc func togglePassThrough() {
        passThrough.toggle(); updateHitTesting(); rebuildMenu()
    }

    @objc func nextOutfit() {
        let wearable = wardrobe.outfits.indices.filter { wardrobe.outfits[$0].isTransparentArt }
        let position = wearable.firstIndex(of: selected) ?? -1
        selected = wearable[(position+1)%wearable.count]
        updateOutfit(); saveSettings(); sound.chime("outfit")
    }
    @objc func selectOutfit(_ sender: NSMenuItem) {
        selected = sender.tag; updateOutfit(); saveSettings()
    }
    @objc func selectSegment(_ sender: NSSegmentedControl) {
        selected = sender.selectedSegment; updateOutfit(); saveSettings()
    }
    func updateOutfit() {
        let outfit = wardrobe.outfits[selected]
        stopFrameTimer(); frameImages.removeAll(); frameCursor = nil
        panelView.art.isRuntime = outfit.isTransparentArt
        stageView?.art.isRuntime = outfit.isTransparentArt
        panelView.badge.stringValue = "夜璃 · " + (outfit.isStaticOutfit ? "职场 · 静态服装" : outfit.runtimeReady ? "黑紫 V3" : "概念参考")
        panelView.art.image = images[outfit.id]; panelView.art.needsDisplay = true
        panelView.detail.stringValue = outfit.isStaticOutfit ? "静态服装 · 拖动移动 / 滚轮缩放" : outfit.runtimeReady ? "拖动移动 · 滚轮缩放 · + 展开" : "概念参考 · 非运行服装"
        stageView?.art.image = images[outfit.id]; stageView?.art.needsDisplay = true
        stageView?.note.stringValue = outfit.note
        stageView?.wardrobe.selectedSegment = selected
        stageView?.previewOutfit = outfit
        stageView?.truth.stringValue = demo.label
        stageView?.subtitle.stringValue = outfit.runtimeReady ? "V3 / 真实帧动画 / SIMULATION" : "V3 / \(outfit.stateLabel)"
        stageView?.boundary.stringValue = "职场为静态服装 · 系统合成语音 / 自有音频 · TWOS 未连接"
        stageView?.needsLayout = true
        setPanelSize(); playAnimation("idle"); rebuildMenu()
    }

    func makeStage() {
        let w = StageWindow(contentRect: NSRect(x: 0, y: 0, width: 900, height: 800),
                         styleMask: [.titled, .closable, .miniaturizable, .resizable], backing: .buffered, defer: false)
        w.title = "夜璃 · Nyra｜全屏舞台"
        w.onEscape = { [weak self] in self?.backToDesktop() }
        w.appearance = NSAppearance(named: .darkAqua)
        w.minSize = NSSize(width: 720, height: 620)
        w.isReleasedWhenClosed = false; w.delegate = self
        w.collectionBehavior = [.fullScreenPrimary]
        let view = StageView(frame: w.contentView!.bounds)
        view.wardrobe = NSSegmentedControl(labels: wardrobe.outfits.map(\.name), trackingMode: .selectOne,
                                          target: self, action: #selector(selectSegment))
        view.wardrobe.setAccessibilityLabel("选择服装 · 静态参考单独标注")
        view.addSubview(view.wardrobe)
        view.actions = [button("回到桌面", self, #selector(backToDesktop), hint: "回到浮动桌宠"),
                        button("全屏 / 返回", self, #selector(fullscreen), hint: "切换全屏展示"),
                        button("动作", self, #selector(showAnimationMenu), hint: "选择实际动作"),
                        button("声音", self, #selector(showSound), hint: "声音 · 试听 / 静音 / 音量"),
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
        hoverTimer?.invalidate(); hoverTimer = nil; soundPopover?.close()
        updateOutfit()
        stage!.makeKeyAndOrderFront(nil); NSApp.activate(ignoringOtherApps: true)
        playAnimation("idle"); rebuildMenu()
    }
    @objc func fullscreen() {
        if stage?.isVisible != true { showStage() }
        stage?.toggleFullScreen(nil)
        sound.chime("open")
    }
    @objc func backToDesktop() {
        if stage?.styleMask.contains(.fullScreen) == true {
            stage?.toggleFullScreen(nil)
            pendingDesktop = true
        } else { showPanel() }
    }
    var pendingDesktop = false
    var pendingHide = false
    func windowDidExitFullScreen(_ notification: Notification) {
        if pendingHide { pendingHide = false; pendingDesktop = false; stage?.orderOut(nil); writePlaybackState("hidden"); rebuildMenu() }
        else if pendingDesktop { pendingDesktop = false; showPanel() }
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
        playAnimation(demo == .running ? "working" : demo == .verified ? "verified_success" : "idle")
        rebuildMenu()
    }

    func stopFrameTimer() { frameTimer?.invalidate(); frameTimer = nil }
    var mayAnimate: Bool {
        wardrobe.outfits[selected].runtimeReady && (panel.isVisible || stage?.isVisible == true)
            && !NSWorkspace.shared.accessibilityDisplayShouldReduceMotion
    }
    func playAnimation(_ name: String) {
        stopFrameTimer()
        guard wardrobe.outfits[selected].runtimeReady, let seq = runtimePlan?.sequences[name] else { return }
        animationName = name
        frameCursor = FrameCursor(sequence: seq)
        frameImages.removeAll()
        // Cache only the active sequence; hidden windows have no animation timer.
        for id in Set(seq.assetIDs) {
            if let im = NSImage(contentsOf: resources.appendingPathComponent("runtime/default/\(id).png")) {
                im.size = NSSize(width: 1024, height: 1536); frameImages[id] = im
            }
        }
        if NSWorkspace.shared.accessibilityDisplayShouldReduceMotion {
            panelView.art.image = images["runtime-default"]; stageView?.art.image = images["runtime-default"]
            panelView.art.needsDisplay = true; stageView?.art.needsDisplay = true
            return
        }
        displayFrame(); scheduleFrame()
    }
    func displayFrame() {
        guard let cursor = frameCursor, let im = frameImages[cursor.assetID] else { return }
        panelView.art.image = im; panelView.art.needsDisplay = true
        stageView?.art.image = im; stageView?.art.needsDisplay = true
        panelView.detail.stringValue = animationName == "idle" ? "拖动移动 · 滚轮缩放 · + 展开" : "\(animationLabels[animationNames.firstIndex(of: animationName) ?? 0]) · 本地演示"
        displayedFrames[animationName, default: 0] += 1
        if displayedFrames[animationName, default: 0] % 6 == 0 { writePlaybackState("frame_progress") }
    }
    func writePlaybackState(_ event: String) {
        // Local evidence about this app only. No TWOS events, screen capture or personal data.
        let state: [String: Any] = ["pid": ProcessInfo.processInfo.processIdentifier,
            "event": event, "animation": animationName, "displayed_frames": displayedFrames,
            "panel_visible": panel.isVisible, "stage_visible": stage?.isVisible == true,
            "control_ring_expanded": panelView.expanded, "hover_timer_scheduled": hoverTimer?.isValid == true,
            "outfit": wardrobe.outfits[selected].id, "desired_height": desiredHeight,
            "window_frame": NSStringFromRect(panel.frame), "sound": sound.snapshot,
            "stage_fullscreen": stage?.styleMask.contains(.fullScreen) == true,
            "timer_scheduled": frameTimer?.isValid == true,
            "reduce_motion": NSWorkspace.shared.accessibilityDisplayShouldReduceMotion,
            "uptime": ProcessInfo.processInfo.systemUptime]
        if let data = try? JSONSerialization.data(withJSONObject: state, options: [.sortedKeys]) {
            try? data.write(to: stateDirectory.appendingPathComponent("playback-state.json"), options: .atomic)
        }
    }
    func scheduleFrame() {
        guard mayAnimate, let cursor = frameCursor else { return }
        let timer = Timer(timeInterval: cursor.duration, repeats: false) { [weak self] _ in
            guard let self = self, self.mayAnimate else { return }
            self.frameCursor?.advance()
            if self.frameCursor?.finished == true { self.playAnimation("idle") }
            else { self.displayFrame(); self.scheduleFrame() }
        }
        timer.tolerance = min(0.02, cursor.duration*0.1)
        frameTimer = timer; RunLoop.main.add(timer, forMode: .common)
    }
    func makeAnimationMenu() -> NSMenu {
        let menu = NSMenu(title: "SIMULATION · 实际画稿")
        for i in animationNames.indices {
            let item = NSMenuItem(title: animationLabels[i] + " · SIMULATION", action: #selector(selectAnimation), keyEquivalent: "")
            item.target = self; item.tag = i; item.isEnabled = wardrobe.outfits[selected].runtimeReady
            menu.addItem(item)
        }
        return menu
    }
    @objc func selectAnimation(_ sender: NSMenuItem) {
        playAnimation(animationNames[sender.tag])
        sound.chime("open")
    }
    @objc func showAnimationMenu(_ sender: NSButton) {
        makeAnimationMenu().popUp(positioning: nil, at: NSPoint(x: 0, y: sender.bounds.maxY), in: sender)
    }
    func rebuildMenu() {
        guard status != nil, wardrobe != nil else { return }
        let menu = NSMenu()
        @discardableResult func item(_ title: String, _ action: Selector?, key: String = "") -> NSMenuItem {
            let i = NSMenuItem(title: title, action: action, keyEquivalent: key)
            i.target = self; menu.addItem(i); return i
        }
        item("夜璃 · Nyra  /  R3 交互桌宠", nil)
        item("显示 / 隐藏", #selector(toggleVisibility))
        item("打开动作预览与换装", #selector(showStage))
        item("全屏幕展示 / 返回", #selector(fullscreen))
        item("一键换装", #selector(nextOutfit))
        let wardrobeItem = item("选择造型（各自状态见标注）", nil)
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
        item("动作 · 本地演示", nil).submenu = makeAnimationMenu()
        item("TWOS：未连接 / LIVE BLOCKED", nil)
        item(sound.isMuted ? "声音：已静音" : "声音设置 · 中英女性系统合成", #selector(showSoundFromMenu))
        item(NSWorkspace.shared.accessibilityDisplayShouldReduceMotion ? "系统减少动态：显示母版" : "动画：隐藏时停止计时", nil)
        menu.addItem(.separator())
        item("退出夜璃", #selector(quit), key: "q")
        status.menu = menu
        NSApp.mainMenu?.items.first?.submenu = menu.copy() as? NSMenu
    }

    func saveSettings() {
        guard panel != nil, wardrobe != nil else { return }
        let data: [String: Any] = ["interaction_version": 3, "outfit": wardrobe.outfits[selected].id, "height": desiredHeight,
                                   "x": panel.frame.minX, "y": panel.frame.minY,
                                   "muted": sound.isMuted, "volume": sound.volume, "language": sound.language]
        if let bytes = try? JSONSerialization.data(withJSONObject: data, options: [.prettyPrinted, .sortedKeys]) {
            try? bytes.write(to: prefsURL, options: .atomic)
        }
    }
    func restoreSettings() {
        guard let data = try? Data(contentsOf: prefsURL),
              let prefs = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return }
        if let id = prefs["outfit"] as? String, id != "v3-master", let index = wardrobe.outfits.firstIndex(where: { $0.id == id }) { selected = index }
        if let muted = prefs["muted"] as? Bool { sound.isMuted = muted }
        if let volume = prefs["volume"] as? Float { sound.volume = min(1,max(0,volume)) }
        if let language = prefs["language"] as? String, ["auto","zh","en"].contains(language) { sound.language = language }
        if let height = prefs["height"] as? Double, height.isFinite { desiredHeight = min(max(height, 160), 1000) }
        if prefs["interaction_version"] == nil { desiredHeight = max(400, desiredHeight) }
        if let x = prefs["x"] as? Double, let y = prefs["y"] as? Double, x.isFinite, y.isFinite {
            panel.setFrameOrigin(NSPoint(x: x, y: y))
        }
        clampPanel()
    }
    @objc func quit() { NSApp.terminate(nil) }
    func applicationWillTerminate(_ notification: Notification) {
        stopFrameTimer(); frameImages.removeAll(); hoverTimer?.invalidate(); hoverTimer = nil; sound.stop()
        writePlaybackState("terminating")
        if let observer = screenObserver { NotificationCenter.default.removeObserver(observer) }
        if let observer = motionObserver { NSWorkspace.shared.notificationCenter.removeObserver(observer) }
        saveSettings()
        if lockFD >= 0 { flock(lockFD, LOCK_UN); close(lockFD); lockFD = -1 }
        if status != nil { NSStatusBar.system.removeStatusItem(status) }
    }
}

if CommandLine.arguments.contains("--self-test") {
    do {
        try runCoreTests()
        let data = try Data(contentsOf: Bundle.main.resourceURL!.appendingPathComponent("runtime/standalone_r3.json"))
        try runRuntimeTests(JSONDecoder().decode(RuntimePlan.self, from: data))
        try runInteractionTests()
    } catch { fputs("FAIL: \(error)\n", stderr); exit(1) }
} else {
    let app = NSApplication.shared
    let companion = Companion()
    app.delegate = companion
    app.run()
}
