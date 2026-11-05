# Nyra 1.0.5 / 105 verification

Runtime source: `1b712de7110feded54775b522448fe6c61dbc164`. DMG SHA-256: `05b42e2e782146b41ce94e5b5543fc885e0b923b47013022ada7f1cfa2b0cde7`.

- Complete serial TWOS/macOS gate: 1827 PASS, 1 retained historical skip, 0 failures; 1828 collected. Frozen inputs and runtime unchanged.
- REAL_GUI: all 38 Safari geometry measurements began and ended visible in actual Safari. An earlier mixed-client bridge failure is preserved; browser identity binding was corrected and its four new simulated tests passed before this complete run.
- Historical gate02 failure is preserved: fixture preparation exceeded its historical20-second poll before any model execution. A separate unchanged-limit probe passed; the fixture-only wait was aligned to two existing30-second subprocess phases plus preparation. All30 migration checks passed before this full run. No production timeout or migration/authority assertion was weakened.
- REAL_GUI: exact signed/notarized DMGs launched read-only; bundled and standalone Nyra were observed, then normally quit. No installed Owner app replacement.
- REAL_PROTOCOL / REAL_GUI: both initiating providers exceeded five round trips, native Stop/partial reply/new composer were checked. The signed candidate completed 27 reconciled replies before Stop, with 28 sent; one stopped in-flight receipt remains explicitly unreconciled and was not resent.
- REAL_NATIVE / REAL_GUI: 13 Chinese recordings and 13 English phrases completed native playback callbacks; current panels showed start/end and closed. This does not certify subjective voice quality. Five outfits, including both new standing/reclining variants, were observed; two-frame directional loops are not eight-frame animation.
- Unchanged accepted business tasks were not replayed. New Owner acceptance and Mac App Store approval are NOT_GRANTED.

The original Owner first-round stop trigger was not reproduced in the tested baseline scenarios. Repairs address independently observed intent projection, native Stop, partial-response and composer-remount defects; the original incident is not relabelled as proven resolved by a single guessed cause.

The old isolated project launcher refused a changed installation path (`DESKTOP_INSTALLATION_MISMATCH`). The paired workbench remained usable through Window → ChatGPT + Codex. No cross-path legacy-environment migration is claimed.

Mac App Store remains NOT_SUBMITTED: sandbox folder persistence, external executable/helper architecture, provider distribution permissions, provisioning and reviewer access are unresolved. Developer ID notarization is not App Store acceptance.
