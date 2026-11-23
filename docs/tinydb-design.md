# Python Foundry TinyDB

## Learning path and implementation

The algorithms sequence precedes twelve TinyDB lessons. Those lessons connect validated records, statement parsing, deterministic encoding, B+ point lookups, leaf/branch splits and range links to snapshots, transactions, statement errors, interrupted commits, corruption handling and the saved workspace. All run the same `content/tinydb.py` engine that is supplied as an editable source tab. It uses Python's standard library, independently of SQLite and the unrelated third-party package named TinyDB.

The SQL subset accepts one complete statement per line. It supports one table, `people(id, name, score)`, inserts, id equality/range selection, score updates, deletion, BEGIN/COMMIT/ROLLBACK, `.schema`, `.stats`, `.check`, `.dump`, `.snapshot`, `.export`, and `.crash prepare|commit|install`. `.help` gives the exact grammar. Unsupported statements are rejected rather than silently interpreted as another command. A rejected statement leaves its prior candidate unchanged; earlier successful statements remain staged. Ending a script with an open transaction rolls it back.

Row constraints are explicit: an integer id in 0..2147483647, a name of 1..32 UTF-8 bytes, and an integer score in 0..100. Booleans are not accepted as integer fields. Duplicate ids and more than 4096 rows are rejected.

## Index and snapshot format

The B+ index has at most three keys per node. Branch separators repeat the minimum of each right subtree; separator equality routes right. Leaves carry rows and next-leaf links. Insertion splits overflowing leaves and branches and can create a new root. Validation checks sorted unique keys, capacities, child ranges, separators, equal leaf depth and leaf links.

The index is in memory. Snapshots contain sorted rows and rebuild the index on opening. Updates and deletes rebuild it for clarity; this is not an incremental page-cache or delete-rebalancing implementation. Lessons distinguish logical nodes visited from physical file I/O. The course also implements a separate unbalanced binary search tree so learners can compare its height with a balanced B+ index.

A `.pfdb` snapshot is UTF-8 JSON with exactly `payload` and `sha256`. The payload has exactly `format: "PYFDB1"`, nonnegative integer `generation`, and sorted unique `rows`. SHA-256 covers deterministic UTF-8 JSON of that payload with sorted field names and compact separators. Check the hash, marker, types, row bounds and ordering before accepting the file. A hash detects accidental corruption, not malicious replacement of both data and hash. These files are not binary-compatible with C or Rust Foundry databases; JSON row export is the interchange path.

## Commit and recovery boundaries

The journal, `<database>.journal`, contains `phase`, `base` generation and an `after` snapshot envelope. The target generation must be base + 1. Commit writes a prepared journal, marks it committed, installs the after-image by replacing a temporary file, then removes the journal. A prepared journal is discarded on reopen. A committed journal is redone, including when the same after-image was already installed. A conflicting generation or malformed journal is rejected without replacing the main file. A valid committed after-image can recover a damaged main file.

`.crash` deliberately ends the next commit after a protocol boundary. It is a controlled exit that returns both main and journal bytes to the browser. A real Stop, timeout or killed worker returns no candidate file set and leaves the previous browser snapshot. These are teaching failure models; the browser filesystem supplies no physical-disk fsync guarantee and the engine does not provide concurrent process locking.

## Saved workspace and safe restart

The standalone examples always have fresh files. Only the final Saved TinyDB workspace retains data. Run statements uses the current editable `tinydb.py`, replaces `main.py` with its statement driver, and mounts the saved data files. The Python kernel returns the complete resulting file set, including unchanged files and deletion of an old journal. Do not merge only modified files: that could resurrect a journal removed by recovery.

Publish that whole set in one IndexedDB read/write transaction with an expected workspace revision. A stale tab cannot overwrite newer files. It retains a downloadable candidate and offers Load latest saved files. Storage denial also retains the candidate. Displaying output or finishing Python execution does not imply the files were saved. Save success names the new workspace revision; that revision is separate from TinyDB's committed generation.

Import database runs the real Python decoder before replacing the main snapshot and removing its journal. Other saved backup/export files are retained. A failed validation preserves the saved workspace. Downloads include complete file sets so a deliberately interrupted commit keeps its journal with its main file. Generated-file bounds apply: 1 MB per file, 2 MB total, 12 files. An incomplete returned set cannot be published.

Guarded reload and course updates preserve source edits, statements, output, selected import bytes, saved revision/files and an unsaved candidate in a verified per-tab restart snapshot. The workspace remains busy through its asynchronous IndexedDB save, so an update cannot race that write. Freeing the Python worker leaves these records intact. Offline execution uses the same pinned Python runtime and engine source.

## Functional evidence

Native and real Pyodide tests exercise random insertion orders, deep splits, separator equality, duplicates, range boundaries, corruption, transaction failures, recovery at prepare/commit/install, idempotent reopen, malformed journals and SQL grammar. Browser tests add reload, a closed-tab fresh offline run, stale-tab conflict, candidate export/restore, validated import, learner engine edits, Stop and storage denial. Shared update tests verify all-window save veto/commit. These establish execution and persistence behavior, not learning effectiveness.
