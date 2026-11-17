# Nyra troubleshooting

> **Current update: minimal activity bubble, independent host focus and offline English voice.** [Instructions](MINIMAL_STATUS_AND_FOCUS.en.md) · [Actual verification and limits](MINIMAL_STATUS_VERIFICATION.en.md). The default bubble closes when no work is active; task mutations still require their separate authorization.

> **Current control-enabled version:** [Focus, compact task controls and shared Codex navigation](MINIMAL_STATUS_AND_FOCUS.en.md). The status channel remains read-only; a separate authenticated channel carries only user-selected drafts/actions. Existing standalone status grants do not gain control permission automatically. Historical read-only-only descriptions do not describe this new control channel.

Nyra 1.0.8 / 108 · [This update](MINIMAL_STATUS_AND_FOCUS.en.md)

- **Not visible:** use the ◈ 夜璃 menu → Show/Hide. If the app is already running, reopen it from Applications. Reset position restores a reachable location. Do not delete preferences as a first remedy.
- **A different version is running:** quit that Nyra normally from its own menu, then open the desired version. TWOS jobs continue. Do not use killall or launch several copies.
- **No task connection:** local animations still work. Open TWOS → ⋯ More → Nyra status, verify the standalone instance and follow the connection prompt. Active task controls require their separate grant. Opening the pet alone is not evidence of a task binding.
- **Working with no new output:** check TWOS's current task and connection. Nyra follows state, not elapsed time or hidden reasoning. A stale connection must become unknown; retain the minimal error rather than inventing success.
- **A preview returns to idle:** previews are intentionally bounded. A disabled action has no matching resource for the chosen outfit; supported core actions are listed in the guide.
- **Stage exit:** use Desktop/Back or focus the stage and press Esc. Controls remain visible. Blank regions are intentionally click-through.
Nyra plays short, bundled Chinese recordings by Tian at action transitions: a rest reminder on reclining and a cheer on verified success. Sound starts muted. Unmute and enable Action voice in Sound; close the panel with Close, Escape or Sound again.
- **macOS blocks launch:** verify the exact release asset and receipt. Report the displayed error and version. Never disable system security or paste private credentials into a support report.

Send only the product version, relevant visible error and non-sensitive reproduction steps. Do not include model prompts, account data, reports, tokens or endpoint secrets.

[简体中文](TROUBLESHOOTING.zh-CN.md) · [README](../../README.md)


## Controls and connection

Use the separate lower-right hover Stage arrow with a single click; resize with the wheel/trackpad or **+ / Larger / Smaller / Reset size**. Return, actions, pose, sound, hide and quit sit in the visible top safe area, accounting for Dock/menu placement. Existing transparent art, five outfits and desktop restoration remain unchanged.

The read-only status channel carries side (left/right/both), minimal state, opaque IDs and a bounded active conversation title. Any fresh active pane keeps working frames alive; one finishing does not idle the other. Unknown connection is neutral; merely reading a page or inspecting delivery is not work. Short input actions return to the real current base state. TWOS manages automatic exchange and all task dispatch. Nyra does not read whole conversations; its separate authenticated user-control channel forwards only the explicitly entered draft/action for the bound task.

A new standalone can explicitly connect through TWOS → Nyra status → Connect. Both socket peers and their exact signatures are checked. An old standalone may remain visibility-only until normally upgraded. Reconnect reads the current snapshot, without historical work/celebration playback. No browser credentials or business files are copied.


### App moved or macOS translocated it

The read-only link is bound to the exact signed producer, including its application path. Moving/replacing TWOS, or macOS running a quarantined copy from a different temporary path, can leave standalone Nyra at NOT_CONNECTED while Show/Hide still works. Install the verified app in Applications, open that version, then use **Nyra status → Connect** to explicitly renew the read-only association if needed. Do not delete preferences or disable Gatekeeper. In the final isolated installer check, a changed macOS translocation path correctly invalidated the old link; that case is not claimed as automatic reconnection.


[Five outfits and bilingual action voice](AUTOSEND_AND_WARDROBE.en.md)


[Current delta](MINIMAL_STATUS_AND_FOCUS.en.md)


## English voice update

English uses 13 bundled tiny-voca F2 offline cues; Chinese Tian and explicit imports are preserved. See [voice details](ENGLISH_VOICE.en.md). No task text, synthesis service or model runtime is added.

## Current status / return troubleshooting

The bubble shows observed replying, execution, queueing or waiting-for-action work, then closes on confirmed idle or terminal state. An observation gap is briefly unconfirmed, never an indefinitely running old task. If an old engineering Nyra occupies the singleton, quit it through its own menu and use Show Nyra in the intended TWOS. Do not delete profiles or force-stop other apps. Character return needs no edit grant; unavailable edit/Stop actions require checking the exact task and current permission. Choose tiny-voca F2 for English; Chinese Tian is unchanged and sound still starts muted.
