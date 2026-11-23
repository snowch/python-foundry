# Offline copies and safe updates

This course follows the shared [course guide](https://github.com/snowch/cuda-python-lab/blob/main/docs/course-design-guide.md) and the [Rust Foundry findings](https://github.com/snowch/rust-foundry/blob/main/docs/offline-update-design.md), including the distinction between live pages, pinned executable assets and a verified complete offline copy. Python’s unthreaded worker needs no separate isolation service worker.

The build fingerprints the complete site, creates a SHA-256 file contract and places immutable files in `releases/<id>/`. HTML and its module graph are pinned to that release. Runtime requests resolve relative to the pinned worker/engine URLs. All lessons, interpreter files, editor code, fonts, icons, source archives and project downloads are included. External documentation and desktop installation tools are excluded and named as such.

Online navigation fetches the live page. Offline navigation serves the complete saved release. Automatic checks fetch metadata without downloading the whole course. App status offers Save offline copy, Update offline copy or Repair offline copy according to the same verified state used for its status. Staged updates offer Restart to update. No completion claim is based on a percentage, commit equality or an old marker.

Verify each file and mark completion last. An interrupted update preserves the earlier complete copy and can resume verified bytes. Manual checks demand a fresh scan, waiting for earlier scans; older workers require sequential replies. Missing or corrupted files clear readiness and offer repair. Unknown unpinned root assets retain their original URL, while declared and pinned files must match their own release. Publishing retains two prior immutable trees for open tabs; first publication has no pre-release app graph to migrate.

Restart uses PREPARE_RESTART, unanimous window confirmation and COMMIT_RESTART. Lock working controls before the asynchronous snapshot write. Composition, an active job, failed storage or an unresponsive older window vetoes the transaction. An expired request cannot authorize a late restart. Abort unlocks and discards its marker/snapshot. Never silently reload another tab or overwrite its current editor.

Snapshots use per-tab IndexedDB records with read-back verification and a small sessionStorage marker. They preserve active source tab, all edited source/practice files, restore backups, input/arguments, prediction, results, generated files, completion and in-tab fallback records. Restore the editor before reopening its optional disclosures and returning to the saved reading position. Per-key lesson saves avoid overwriting independent edits in other windows.

HTTP503, integrity failures and missing interpreter files can occur after the page has opened. Show a native recovery dialog, retain earlier results, save before reload and name the actual Run control that failed. Python errors and practice checks do not request an offline repair. Preserve learner work when removing downloaded course files.

Browser storage can be evicted by the platform; request persistent storage where supported and verify before claiming readiness. Android can suspend transfers, so keep durable progress and resume rather than promise uninterrupted background execution. A repair error page is a last-resort path, not a successful offline journey.

Verification covers first save, genuine network-off navigation/reload/new tab with real execution, reopened pages, interrupted/cancelled updates, corruption and fresh repair, old-page first Run after publication, all-window restart refusal and commit, storage failures, runtime recovery, project files and every stable lesson URL. Functional results do not establish teaching effectiveness.

TinyDB data is separate from downloaded course assets. Repairing or removing the offline copy never clears the TinyDB IndexedDB database. Restart snapshots retain the statements, selected import, saved file revision and any unsaved candidate; an in-progress workspace save vetoes restart. A fresh offline tab is tested opening and running the saved database with a cold Python worker.
