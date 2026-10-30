# Upgrade and uninstall

R3 candidate: normal-reply handoff, explicit stop and separate Nyra transport/activity/rendering. Final package and release evidence pending. [R3 incremental guide / R3 差量指南](OWNER_REGRESSION_R3.en.md).


**R2 verification scope.** The signed TWOS 1.0.2 / 101.50 candidate completed one explicitly started three-round-trip exchange between real ChatGPT and Claude webpages: six submissions and six matched complete replies, with no manual per-turn send or check. Reopening preserved the completed exchange without replay. TXT, PNG and simple text-layer PDF readability was observed in both directions; native/synthetic boundary checks are recorded separately. The matching complete main regression and new notarization are recorded in the release receipt; the linked GitHub Release records publication. These observations do not grant Owner acceptance.


## Upgrade

Finish any local manual preview and quit Nyra normally. Replace **Nyra.app** in Applications with the new signed app, then reopen. A TWOS update replaces its nested helper as part of the complete TWOS app; never replace files inside a running app bundle. Keep previous installers until the new version is accepted.

Preferences for standalone and embedded Nyra are shared under `~/Library/Application Support/Nyra` in production. Previous bundled preferences migrate only if no shared settings exist. A normal quit preserves the requested show/hide preference; explicit Hide changes it. Existing audio, outfit and size choices are retained. Engineering diagnostic roots are separate.

Only one compatible production Nyra should run. Opening another compatible copy targets the existing instance with a visibility-only request. An incompatible version asks for a normal exit instead of killing or silently downgrading it. TWOS closing must not kill an independently started Nyra.

## Uninstall

Quit the app and move the chosen Nyra application to Trash in Finder. Removing TWOS removes its bundled component but does not remove standalone Nyra or personal preferences. Removing Nyra does not remove TWOS projects or stop a running model task. Application Support data remains for reinstall; deleting it is an optional separate, explicit user action. No login item is installed automatically.

[简体中文](UPGRADE_AND_UNINSTALL.zh-CN.md) · [README](../../README.md)


## R2 controls and connection

Use the separate lower-right hover Stage arrow with a single click; resize with the ruler grip/wheel. Return, actions, pose, sound, hide and quit sit in the visible top safe area, accounting for Dock/menu placement. Existing transparent art, three outfits and desktop restoration remain unchanged.

Nyra v2 receives only side (left/right/both), minimal state and opaque IDs. Any fresh active pane keeps working frames alive; one finishing does not idle the other. Unknown connection is neutral; merely reading a page or inspecting delivery is not work. Short input actions return to the real current base state. TWOS manages automatic exchange; Nyra cannot dispatch, approve or read the conversations.

A new standalone can explicitly connect through TWOS → Nyra status → Connect. Both socket peers and their exact signatures are checked. An old standalone may remain visibility-only until normally upgraded. Reconnect reads the current snapshot, without historical work/celebration playback. No browser credentials or business files are copied.
