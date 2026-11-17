# Install Nyra 1.0

> **Current update: minimal activity bubble, independent host focus and offline English voice.** [Instructions](MINIMAL_STATUS_AND_FOCUS.en.md) · [Actual verification and limits](MINIMAL_STATUS_VERIFICATION.en.md). The default bubble closes when no work is active; task mutations still require their separate authorization.
> **Current control-enabled version:** [Focus, compact task controls and shared Codex navigation](MINIMAL_STATUS_AND_FOCUS.en.md). The status channel remains read-only; a separate authenticated channel carries only user-selected drafts/actions. Existing standalone status grants do not gain control permission automatically. Historical read-only-only descriptions do not describe this new control channel.

Nyra 1.0.8 / 108 · [This update](MINIMAL_STATUS_AND_FOCUS.en.md)

This is the standalone companion. TWOS includes its own pinned Nyra component: TWOS users do not need this second installer.

Currently supports macOS only. A Windows version is in development; no downloadable build is available yet. This release provides Apple Silicon (arm64) only, declares a macOS 13.0 minimum and was tested on macOS 27.0.1. Other macOS versions and Intel are not claimed tested. Consult the release receipt for signatures and hashes.

1. Download the **Nyra** DMG and its matching `SHA256SUMS` from this repository's release. The work-order ZIP and automatic GitHub source ZIP are not installers.
2. Open the DMG. Drag **Nyra** into **Applications**. Eject the DMG and open the installed app. Approve only the normal macOS launch prompt for this signed product. If macOS reports an invalid signature or blocks the app, stop and consult Troubleshooting; do not disable Gatekeeper or remove quarantine.
3. A transparent character and the **◈ 夜璃** menu-bar item appear. Audio is muted by default. Nyra requires no account, email registration, model subscription, Python, Node, Pets plugin, or first-run artwork download.
4. Hover over the visible character. Use **＋** to open the control ring. Choose Actions to play one bounded preview, or change outfits. The menu bar remains available if the character is hidden.
5. The Nyra copy bundled with TWOS connects to its matching workbench. For standalone Nyra, open **TWOS → ⋯ More → Nyra status → Connect and authorize**, verify the exact standalone app and follow the grant prompt. An existing read-only grant requires a separate **Enable Nyra task controls** action before append or Stop; old grants do not upgrade automatically. Read-only status remains an option. Local interaction remains available when disconnected, with an honest connection status.

**End point:** the installed character displays and its controls work. You do not need to create or repeat a TWOS business task.

Advanced checksum verification: in the download folder, run `shasum -a 256 -c SHA256SUMS`. Keep the manifest and release receipt with the installer. No Terminal command is required for ordinary installation.

[简体中文](INSTALL.zh-CN.md) · [README](../../README.md)


## Controls and connection

Use the separate lower-right hover Stage arrow with a single click; resize with the wheel/trackpad or **+ / Larger / Smaller / Reset size**. Return, actions, pose, sound, hide and quit sit in the visible top safe area, accounting for Dock/menu placement. Existing transparent art, five outfits and desktop restoration remain unchanged.

The read-only status channel carries side (left/right/both), minimal state, opaque IDs and a bounded active conversation title. Any fresh active pane keeps working frames alive; one finishing does not idle the other. Unknown connection is neutral; merely reading a page or inspecting delivery is not work. Short input actions return to the real current base state. TWOS manages automatic exchange and all task dispatch. Nyra does not read whole conversations; its separate authenticated user-control channel forwards only the explicitly entered draft/action for the bound task.

A new standalone can explicitly connect through TWOS → Nyra status → Connect. Both socket peers and their exact signatures are checked. An old standalone may remain visibility-only until normally upgraded. Reconnect reads the current snapshot, without historical work/celebration playback. No browser credentials or business files are copied.


[Five outfits and bilingual action voice](AUTOSEND_AND_WARDROBE.en.md)
