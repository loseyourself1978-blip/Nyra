# Use Nyra 1.0

> **Current control-enabled version:** [Focus, compact task controls and shared Codex navigation](FOCUS_AND_TASK_CONTROLS.en.md). The status channel remains read-only; a separate authenticated channel carries only user-selected drafts/actions. Existing standalone status grants do not gain control permission automatically. Historical read-only-only descriptions do not describe this new control channel.

Nyra 1.0.7 / 107 · [This update](FOCUS_AND_TASK_CONTROLS.en.md)

Nyra is a local visual companion. A user can edit a draft, submit an authorized supplement or stop the exact bound task through TWOS. TWOS remains the sole execution and permission controller; Nyra cannot approve work, independently run commands or infer success from conversation text.

## Desktop

Enter the visible character to trigger one jump; staying still does not continually retrigger it. Drag the character left or right to move it and play that direction's running frames. Release to settle and return to the real base state. The mouse wheel and trackpad adjust size; **+ / Larger / Smaller / Reset size** provides explicit controls. The old ruler grip and its hit region are removed. The menu offers Reset position if the character is offscreen.

The control ring offers outfit, transparent stage, sound, Actions, smaller/larger, hide and quit. Actions are bounded **Manual preview** overrides: they do not change task truth or count as successful work. Unsupported optional actions are disabled for that outfit. After a preview, the current real state resumes. Reduce Motion follows the macOS preference.

## Five outfits and stage

Black & purple, Office, Gala, White blouse and Ruby gown each have standing and reclining runtime art. In the transparent stage, choose an outfit at the top and **Pose** in the top safe toolbar. Reclining supports blink, gaze, work, wait and a celebration preview. Running or jumping uses matching-outfit rise → action → lower frames. No standing image is rotated to impersonate a reclining pose.

The stage is a screen-sized transparent window, not a black macOS fullscreen Space. Blank areas pass pointer input through; the character and control buttons remain interactive. **Desktop**, **Stage/Back**, or Esc while the stage has focus returns to the saved desktop position, size and outfit. Hiding or quitting also restores that desktop configuration. There is no global keyboard listener.

## Task truth

| Status | Appearance and meaning |
|---|---|
| Connected, no active task | Idle |
| Queued / waiting for user | Waiting; approve or answer in TWOS, never in Nyra |
| Running | Working |
| Partial / failed / cancelled / ended unverified | Neutral idle with the actual result label; no success celebration |
| Verified success with linked evidence | Celebrate once, then return to the current base state |
| Transport disconnected | Neutral appearance and unknown connection; no permanent fake work |
| Connected but activity stale | Activity needs an update; no invented idle/success, task actions disabled until reconciled |

A manual celebration is labelled preview. A website finishing a reply does not verify a local file. Startup and reconnect read the current snapshot and do not replay an old celebration. Nyra cannot grant overall Owner acceptance.

## Audio and lifecycle

Nyra plays 13 short bundled Chinese Tian recordings or 13 corresponding English phrases with an installed local female voice. Eligible action transitions include idle, reading, work, rest and verified success; cooldown prevents repetitive speech. Sound starts muted. Unmute and enable Action voice in Sound; close the panel with Close, Escape or Sound again. Hiding Nyra stops audio; quitting Nyra does not stop TWOS tasks.

[简体中文](USER_GUIDE.zh-CN.md) · [README](../../README.md)


## Controls and connection

Use the separate lower-right hover Stage arrow with a single click; resize with the wheel/trackpad or **+ / Larger / Smaller / Reset size**. Return, actions, pose, sound, hide and quit sit in the visible top safe area, accounting for Dock/menu placement. Existing transparent art, five outfits and desktop restoration remain unchanged.

The read-only status channel carries side (left/right/both), minimal state, opaque IDs and a bounded active conversation title. Any fresh active pane keeps working frames alive; one finishing does not idle the other. Unknown connection is neutral; merely reading a page or inspecting delivery is not work. Short input actions return to the real current base state. TWOS manages automatic exchange and all task dispatch. Nyra does not read whole conversations; its separate authenticated user-control channel forwards only the explicitly entered draft/action for the bound task.

A new standalone can explicitly connect through TWOS → Nyra status → Connect. Both socket peers and their exact signatures are checked. An old standalone may remain visibility-only until normally upgraded. Reconnect reads the current snapshot, without historical work/celebration playback. No browser credentials or business files are copied.

[Current verification / 本版验证](DEEPSEEK_R1_VERIFICATION.en.md)


[Five outfits and bilingual action voice](AUTOSEND_AND_WARDROBE.en.md)


[Current delta](FOCUS_AND_TASK_CONTROLS.en.md)

## Direct task controls

Click the character once to restore the bound TWOS workbench. The compact task bubble has a direct pencil and Stop. The pencil opens a focused IME-capable editor; Enter sends, Shift+Enter inserts a line, Escape closes. Normal drafts are autosaved; a queued revision is saved only explicitly. A running owned Codex turn supports Steer; web tasks use send-after-completion. Target changes retain the input rather than redirecting it. Stop first fences future dispatch and then interrupts only the bound task. The display changes to Stopping immediately, and to Stopped only on confirmed cancellation. Failed confirmation remains visible. See the [incremental guide](FOCUS_AND_TASK_CONTROLS.en.md) for exact authority and recovery boundaries.
