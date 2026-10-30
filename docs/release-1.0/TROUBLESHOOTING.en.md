# Nyra troubleshooting

**R2 verification scope.** The signed TWOS 1.0.2 / 101.50 candidate completed one explicitly started three-round-trip exchange between real ChatGPT and Claude webpages: six submissions and six matched complete replies, with no manual per-turn send or check. Reopening preserved the completed exchange without replay. TXT, PNG and simple text-layer PDF readability was observed in both directions; native/synthetic boundary checks are recorded separately. The matching complete main regression and new notarization are recorded in the release receipt; the linked GitHub Release records publication. These observations do not grant Owner acceptance.


- **Not visible:** use the ◈ 夜璃 menu → Show/Hide. If the app is already running, reopen it from Applications. Reset position restores a reachable location. Do not delete preferences as a first remedy.
- **A different version is running:** quit that Nyra normally from its own menu, then open the desired version. TWOS jobs continue. Do not use killall or launch several copies.
- **No task connection:** local animations still work. In TWOS use Show Nyra and inspect the read-only binding label. An independently started Nyra may require explicit endpoint selection. Opening the pet alone is not evidence of a task binding.
- **Working with no new output:** check TWOS's current task and connection. Nyra follows state, not elapsed time or hidden reasoning. A stale connection must become unknown; retain the minimal error rather than inventing success.
- **A preview returns to idle:** previews are intentionally bounded. A disabled action has no matching resource for the chosen outfit; supported core actions are listed in the guide.
- **Stage exit:** use Desktop/Back or focus the stage and press Esc. Controls remain visible. Blank regions are intentionally click-through.
- **No sound:** mute is the default. Open Sound, choose a language/source, and use an explicit preview. System voices vary by macOS installation; no voice is silently downloaded.
- **macOS blocks launch:** verify the exact release asset and receipt. Report the displayed error and version. Never disable system security or paste private credentials into a support report.

Send only the product version, relevant visible error and non-sensitive reproduction steps. Do not include model prompts, account data, reports, tokens or endpoint secrets.

[简体中文](TROUBLESHOOTING.zh-CN.md) · [README](../../README.md)


## R2 controls and connection

Use the separate lower-right hover Stage arrow with a single click; resize with the ruler grip/wheel. Return, actions, pose, sound, hide and quit sit in the visible top safe area, accounting for Dock/menu placement. Existing transparent art, three outfits and desktop restoration remain unchanged.

Nyra v2 receives only side (left/right/both), minimal state and opaque IDs. Any fresh active pane keeps working frames alive; one finishing does not idle the other. Unknown connection is neutral; merely reading a page or inspecting delivery is not work. Short input actions return to the real current base state. TWOS manages automatic exchange; Nyra cannot dispatch, approve or read the conversations.

A new standalone can explicitly connect through TWOS → Nyra status → Connect. Both socket peers and their exact signatures are checked. An old standalone may remain visibility-only until normally upgraded. Reconnect reads the current snapshot, without historical work/celebration playback. No browser credentials or business files are copied.


### App moved or macOS translocated it

The read-only link is bound to the exact signed producer, including its application path. Moving/replacing TWOS, or macOS running a quarantined copy from a different temporary path, can leave standalone Nyra at NOT_CONNECTED while Show/Hide still works. Install the verified app in Applications, open that version, then use **Nyra status → Connect** to explicitly renew the read-only association if needed. Do not delete preferences or disable Gatekeeper. In the final isolated installer check, a changed macOS translocation path correctly invalidated the old link; that case is not claimed as automatic reconnection.
