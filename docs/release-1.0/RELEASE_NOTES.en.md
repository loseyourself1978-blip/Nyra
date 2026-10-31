# Nyra 1.0.2 / 102 — R3 release notes

Signed, notarized patch with 1791 passing tests, 1 explicitly retained historical skip and 38 actual Safari measurements in one matched complete gate. [Exact artifact receipt](release.json) · [Verification and limits](R3_VERIFICATION.en.md) · [Incremental guide](OWNER_REGRESSION_R3.en.md). Publication is recorded by the linked GitHub Release; engineering does not grant Owner acceptance.

Changes: ordinary complete replies retain message-level target actions; canonical composer/message detection preserves truthful unknown states; automatic exchange starts from the selected first complete reply, stops future dispatch from either native Stop or host Stop, and retains stopped state across restart. Nyra separates authenticated connection, per-pane activity/freshness and actual clip/frame progress. Old snapshots after producer changes are labelled stale.

The failed Owner retest is preserved. New isolated ChatGPT/Claude work verified three real round trips, both native stops, late replies, direct left/right/both activity and advancing Nyra frames. No old Owner debate or accepted business artifact was replayed.

Current distribution: macOS arm64 only. Windows is in development with no downloadable version. Existing outfits, transparent stage and audio scope are retained. New Owner differential acceptance remains pending.

---

## Historical R2 release record (unchanged)

# Nyra 1.0.1 / 101 — R2 release notes

The matching complete main gate passed 1782 tests, skipped 1 retained historical-installer case and had zero failures, including 38 actual Safari measurements. App and DMG are newly notarized bytes; see the [release receipt](release.json) for signatures and hashes. Owner differential acceptance remains PENDING; original failures and PARTIAL receipts are preserved.

**R2 verification scope.** The signed TWOS 1.0.2 / 101.50 candidate completed one explicitly started three-round-trip exchange between real ChatGPT and Claude webpages: six submissions and six matched complete replies, with no manual per-turn send or check. Reopening preserved the completed exchange without replay. TXT, PNG and simple text-layer PDF readability was observed in both directions; native/synthetic boundary checks are recorded separately. The matching complete main regression and new notarization are recorded in the release receipt; the linked GitHub Release records publication. These observations do not grant Owner acceptance.


Status: signed, notarized and engineering-validated R2 distribution; final Owner differential acceptance remains separate. Use the matching release receipt and GitHub Release for exact distribution facts.

Changes: event-driven idle/work/wait truth; bounded manual playback; edge/cooldown hover; screen-coordinate directional drag with common-mode frame scheduling; same-outfit reclining and rise/action/lower transitions for Black & purple, Office and Gala; transparent screen-sized stage with reachable controls; shared production preferences and a single-instance guard; a pinned TWOS helper and standalone distribution.

The release includes original UI chimes and installed-system/user-imported speech support. It does not include an exclusive generated voice, Windows installer, model access credentials, or an agent with task-execution authority.

Evidence remains separate: native unit/simulation tests, engineering GUI, real transport, Owner product acceptance and public distribution. Old PARTIAL/business receipts are not rewritten. Final supported-system, asset hash, signing, notarization and test details belong in the release receipt. Optional video is not yet recorded; only actual final-candidate captures may be published.

[简体中文](RELEASE_NOTES.zh-CN.md) · [README](../../README.md)


## R2 controls and connection

Use the separate lower-right hover Stage arrow with a single click; resize with the ruler grip/wheel. Return, actions, pose, sound, hide and quit sit in the visible top safe area, accounting for Dock/menu placement. Existing transparent art, three outfits and desktop restoration remain unchanged.

Nyra v2 receives only side (left/right/both), minimal state and opaque IDs. Any fresh active pane keeps working frames alive; one finishing does not idle the other. Unknown connection is neutral; merely reading a page or inspecting delivery is not work. Short input actions return to the real current base state. TWOS manages automatic exchange; Nyra cannot dispatch, approve or read the conversations.

A new standalone can explicitly connect through TWOS → Nyra status → Connect. Both socket peers and their exact signatures are checked. An old standalone may remain visibility-only until normally upgraded. Reconnect reads the current snapshot, without historical work/celebration playback. No browser credentials or business files are copied.


R3 additionally fixes editing a selected first reply: stale seed identity is revoked while active exchange scope stays frozen. Final binaries and validation are identified in the matching release receipt.
