# Install Nyra 1.0

This is the standalone companion. TWOS includes its own pinned Nyra component: TWOS users do not need this second installer.

Currently supports macOS only. A Windows version is in development; no downloadable build is available yet. This installer contains arm64 code for Apple Silicon. The deployment target is macOS 13.0, but the actual tested platform is macOS 27.0.1; older systems and Intel are not verified by this release. See the [release receipt](release.json).

1. Download the **Nyra** DMG and its matching `SHA256SUMS` from this repository's release. The work-order ZIP and automatic GitHub source ZIP are not installers.
2. Open the DMG. Drag **Nyra** into **Applications**. Eject the DMG and open the installed app. Approve only the normal macOS launch prompt for this signed product. If macOS reports an invalid signature or blocks the app, stop and consult Troubleshooting; do not disable Gatekeeper or remove quarantine.
3. A transparent character and the **◈ 夜璃** menu-bar item appear. Audio is muted by default. Nyra requires no account, email registration, model subscription, Python, Node, Pets plugin, or first-run artwork download.
4. Hover over the visible character. Use **＋** to open the control ring. Choose Actions to play one bounded preview, or change outfits. The menu bar remains available if the character is hidden.
5. To view actual TWOS task state, prefer the copy bundled with TWOS. Standalone Nyra offers **Connect read-only status…**: choose the TWOS application's exact app and its documented local endpoint when requested. This connects only minimal status. Do not choose business reports, credentials, or arbitrary socket files. If no valid endpoint is available, local interaction remains usable and the status says not connected.

**End point:** the installed character displays and its controls work. You do not need to create or repeat a TWOS business task.

Advanced checksum verification: in the download folder, run `shasum -a 256 -c SHA256SUMS`. Keep the manifest and release receipt with the installer. No Terminal command is required for ordinary installation.

[简体中文](INSTALL.zh-CN.md) · [README](../../README.md)
