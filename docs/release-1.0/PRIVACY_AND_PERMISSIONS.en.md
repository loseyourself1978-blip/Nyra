# Privacy and permissions

> Unreleased candidate amendment: [minimal activity display and independent host focus](MINIMAL_STATUS_AND_FOCUS.en.md). Verification and publication are pending; published-version guidance below is retained for reference.

> **Current control-enabled version:** [Focus, compact task controls and shared Codex navigation](FOCUS_AND_TASK_CONTROLS.en.md). The status channel remains read-only; a separate authenticated channel carries only user-selected drafts/actions. Existing standalone status grants do not gain control permission automatically. Historical read-only-only descriptions do not describe this new control channel.

Nyra 1.0.7 / 107 · [This update](FOCUS_AND_TASK_CONTROLS.en.md)

Nyra draws local bundled assets. It needs no browser cookies, model token, cloud account or business document. The read-only TWOS connection accepts only the versioned minimal event contract: producer/session/task IDs, sequence/event ID, timestamp, state, source, simulation marker, optional opaque evidence reference and bounded current conversation titles. It must not contain prompts, code, account identity, private paths, trading or medical content.

The local transport authenticates the selected peer. Nyra cannot write tasks, grant approvals, execute commands, or send model requests through it. Unexpected fields and invalid messages are rejected. Duplicate/reconnected terminal snapshots cannot repeatedly celebrate. The visibility URL handles show/hide/status only; it cannot choose an arbitrary endpoint or execute text.

Mouse handling is limited to the character/window hit region; there is no global keyboard recorder or screen recognition. Imported audio remains local. System speech uses installed voices. Local preferences and minimal engineering metadata are not business logs and must not include private message bodies. A separate engineering build uses an isolated root even when launched without diagnostic arguments.

Any file-selection dialog authorizes only the chosen file or endpoint. No full-disk access is required. Recording a walkthrough requires normal macOS permission and is optional. Nyra does not alter browser security, buy subscriptions or enable system login items.

[简体中文](PRIVACY_AND_PERMISSIONS.zh-CN.md) · [README](../../README.md)


## Controls and connection

Use the separate lower-right hover Stage arrow with a single click; resize with the wheel/trackpad or **+ / Larger / Smaller / Reset size**. Return, actions, pose, sound, hide and quit sit in the visible top safe area, accounting for Dock/menu placement. Existing transparent art, five outfits and desktop restoration remain unchanged.

The read-only status channel carries side (left/right/both), minimal state, opaque IDs and a bounded active conversation title. Any fresh active pane keeps working frames alive; one finishing does not idle the other. Unknown connection is neutral; merely reading a page or inspecting delivery is not work. Short input actions return to the real current base state. TWOS manages automatic exchange and all task dispatch. Nyra does not read whole conversations; its separate authenticated user-control channel forwards only the explicitly entered draft/action for the bound task.

A new standalone can explicitly connect through TWOS → Nyra status → Connect. Both socket peers and their exact signatures are checked. An old standalone may remain visibility-only until normally upgraded. Reconnect reads the current snapshot, without historical work/celebration playback. No browser credentials or business files are copied.


[Five outfits and bilingual action voice](AUTOSEND_AND_WARDROBE.en.md)


[Current delta](FOCUS_AND_TASK_CONTROLS.en.md)

## Authenticated user-control channel

The status socket remains read-only. This version separately carries the one draft or supplement explicitly edited by the user to the authenticated TWOS instance. TWOS alone checks the exact task, turn, revision and permission before saving, sending or stopping. Normal drafts and receipts use the existing local TWOS profile. An unconfirmed send is not automatically retried; unconfirmed input is retained in the editor and in the single bounded owner-only recovery record described below. The user can hide the bounded task title before screen sharing. No new file, shell, approval or recipient permissions are granted. See the [current delta](FOCUS_AND_TASK_CONTROLS.en.md).

Nyra’s task editor additionally keeps at most one local `task-input-recovery.json` in its application state directory before transmitting a draft/control operation. It contains only the explicitly entered text, a bounded task title/provider and opaque target identity; no attachments or credentials. The file is owner-only (0600), its directory is 0700, and a matching acknowledged save/delivery clears it. Retained recovery is displayed copy-only after reopening; it is never automatically sent. Discard requires an explicit local confirmation.

The authenticated control channel also returns up to two bound task summaries: provider, side, a title of at most 90 characters, state/freshness, available actions and opaque correlation IDs. A summary may retain an ended or stale task for result inspection or draft recovery. It does not return raw workspace paths, accounts, complete conversations or attachment contents.
