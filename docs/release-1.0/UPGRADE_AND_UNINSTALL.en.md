# Upgrade and uninstall

## Upgrade

Finish any local manual preview and quit Nyra normally. Replace **Nyra.app** in Applications with the new signed app, then reopen. A TWOS update replaces its nested helper as part of the complete TWOS app; never replace files inside a running app bundle. Keep previous installers until the new version is accepted.

Preferences for standalone and embedded Nyra are shared under `~/Library/Application Support/Nyra` in production. Previous bundled preferences migrate only if no shared settings exist. A normal quit preserves the requested show/hide preference; explicit Hide changes it. Existing audio, outfit and size choices are retained. Engineering diagnostic roots are separate.

Only one compatible production Nyra should run. Opening another compatible copy targets the existing instance with a visibility-only request. An incompatible version asks for a normal exit instead of killing or silently downgrading it. TWOS closing must not kill an independently started Nyra.

## Uninstall

Quit the app and move the chosen Nyra application to Trash in Finder. Removing TWOS removes its bundled component but does not remove standalone Nyra or personal preferences. Removing Nyra does not remove TWOS projects or stop a running model task. Application Support data remains for reinstall; deleting it is an optional separate, explicit user action. No login item is installed automatically.

[简体中文](UPGRADE_AND_UNINSTALL.zh-CN.md) · [README](../../README.md)
