# Use Nyra 1.0

**R2 verification scope.** The signed TWOS 1.0.2 / 101.50 candidate completed one explicitly started three-round-trip exchange between real ChatGPT and Claude webpages: six submissions and six matched complete replies, with no manual per-turn send or check. Reopening preserved the completed exchange without replay. TXT, PNG and simple text-layer PDF readability was observed in both directions; native/synthetic boundary checks are recorded separately. The matching complete main regression and new notarization are recorded in the release receipt; the linked GitHub Release records publication. These observations do not grant Owner acceptance.


Nyra is a local visual companion, not an execution agent. It cannot approve work, run commands, send messages, or infer success from conversation text.

## Desktop

Enter the visible character to trigger one jump; staying still does not continually retrigger it. Drag the character left or right to move it and play that direction's running frames. Release to settle and return to the real base state. The corner grip, mouse wheel and trackpad adjust size. The menu offers Reset position if the character is offscreen.

The control ring offers outfit, transparent stage, sound, Actions, smaller/larger, hide and quit. Actions are bounded **Manual preview** overrides: they do not change task truth or count as successful work. Unsupported optional actions are disabled for that outfit. After a preview, the current real state resumes. Reduce Motion follows the macOS preference.

## Three outfits and stage

Black & purple, Office and Gala each have standing and reclining runtime art. In the transparent stage, choose an outfit at the top and **Pose** in the top safe toolbar. Reclining supports blink, gaze, work, wait and a celebration preview. Running or jumping uses matching-outfit rise → action → lower frames. No standing image is rotated to impersonate a reclining pose.

The stage is a screen-sized transparent window, not a black macOS fullscreen Space. Blank areas pass pointer input through; the character and control buttons remain interactive. **Desktop**, **Stage/Back**, or Esc while the stage has focus returns to the saved desktop position, size and outfit. Hiding or quitting also restores that desktop configuration. There is no global keyboard listener.

## Task truth

| Status | Appearance and meaning |
|---|---|
| Connected, no active task | Idle |
| Queued / waiting for user | Waiting; approve or answer in TWOS, never in Nyra |
| Running | Working |
| Partial / failed / cancelled / ended unverified | Neutral idle with the actual result label; no success celebration |
| Verified success with linked evidence | Celebrate once, then return to the current base state |
| Disconnected / stale | Neutral appearance and unknown connection; no permanent fake work |

A manual celebration is labelled preview. A website finishing a reply does not verify a local file. Startup and reconnect read the current snapshot and do not replay an old celebration. Nyra cannot grant overall Owner acceptance.

## Audio and lifecycle

Sound controls provide mute, volume and explicit Chinese/English preview using installed system speech or your locally imported audio. Two original short UI chimes are included. No exclusive generated voice is claimed. Hidden Nyra stops frame and hover timers and audio; a connected read-only status check may remain active to keep connection truth current. Quit ends Nyra, not TWOS or any model task. Embedded and standalone production copies share preferences and allow one compatible active instance.

[简体中文](USER_GUIDE.zh-CN.md) · [README](../../README.md)


## R2 controls and connection

Use the separate lower-right hover Stage arrow with a single click; resize with the ruler grip/wheel. Return, actions, pose, sound, hide and quit sit in the visible top safe area, accounting for Dock/menu placement. Existing transparent art, three outfits and desktop restoration remain unchanged.

Nyra v2 receives only side (left/right/both), minimal state and opaque IDs. Any fresh active pane keeps working frames alive; one finishing does not idle the other. Unknown connection is neutral; merely reading a page or inspecting delivery is not work. Short input actions return to the real current base state. TWOS manages automatic exchange; Nyra cannot dispatch, approve or read the conversations.

A new standalone can explicitly connect through TWOS → Nyra status → Connect. Both socket peers and their exact signatures are checked. An old standalone may remain visibility-only until normally upgraded. Reconnect reads the current snapshot, without historical work/celebration playback. No browser credentials or business files are copied.

[Evidence coverage / 验证范围](R2_VERIFICATION.en.md)


[Actual R2 screenshots and recording scope](MEDIA.en.md)
