# Python Foundry

[Open the course](https://snowch.github.io/python-foundry/)

A beginner-to-practical Python course with **122 lessons across 20 chapters, six application projects and a staged TinyDB project**. No previous programming experience is required. Each lesson provides a complete runnable example, an exact edit to try, a saved prediction, a separate practice task and references to official documentation.

The browser runs **real CPython 3.14.0 through Pyodide 314.0.2**, including the standard library and SQLite. There is no server executing learner code. Projects include editable multi-file modules, prepared data, streamed output, tracebacks and generated-file downloads. Source highlighting follows the code discussed in each lesson. Practice checks compare output and, where specified, additional function cases; a valid experiment is not graded against the starter.

The header manages one reusable Python worker per tab. It supports explicit startup, stopping, a 30-minute idle default and 5/15/30/60-minute preferences. Code, predictions and results survive navigation and guarded updates. App status saves a verified **approximately 16 MB** offline copy including the interpreter, exercises, fonts and downloads. An online visit gets live pages while open code remains pinned to its release. External documentation needs internet access.

## Curriculum

1. Your first programs: printing, names, arithmetic, text and input.
2. Choose and repeat: comparisons, Boolean logic, branches, loops, break and continue.
3. Collections: lists, slicing, mutation, tuples, dictionaries and sets.
4. Iteration: ranges, enumerate, zip, nested loops, comprehensions and sorting.
5. Functions: returns, arguments, defaults, scope, boundaries and recursion.
6. Structured text: normalization, Unicode/bytes, regular expressions, CSV and JSON.
7. Files and values: pathlib, text I/O, context managers, file errors, dates and Decimal.
8. Reliability: tracebacks, exceptions, validation boundaries, assertions and unittest.
9. Modules and tools: local imports, main guards, argparse, desktop environments, packaging and type hints.
10. Objects: classes, dataclasses, validated methods, properties, composition and protocols.
11. Language patterns: inheritance, custom exceptions, special methods, lambdas, dictionary comprehensions, argument unpacking and structural matching.
12. Deeper Python: identity/copying, mutable defaults, iterators, generators, decorators and context managers.
13. Applications: logging, configuration, SQLite queries, parameter binding, transactions and test doubles.
14. Async and performance: coroutine lifecycles, gather, cancellation, operation counts, measured timing and caching.
15. Application projects: text analysis, a decimal CSV ledger, a multi-file inventory, a CLI report, a SQLite catalog and an async transformation pipeline.
16. Algorithm cost, linear/binary search, insertion/merge sort and two-pointer scans.
17. Stacks, deque queues, linked nodes, collision-resolving hashing, heaps and search trees.
18. Graphs, BFS/DFS, topological ordering, Dijkstra and dynamic programming.
19. TinyDB rows, statement parsing, encoding, B+ lookup, splits and range scans.
20. TinyDB snapshots, transactions, rejected statements, journal recovery, backup restoration and a persistent workspace.

The [TinyDB implementation and format](docs/tinydb-design.md) are written in Python. Its saved workspace supports queries, edits, transactions, crash experiments, checked imports and database-file downloads. Whole-file-set saves use revision checks so stale tabs cannot overwrite newer work. The twelve TinyDB lessons follow eighteen dedicated data structures and algorithms lessons.

Desktop virtual environments, package builds, third-party installation and native processes are explicitly distinguished from browser capabilities. Async browser examples use a final top-level `await main()`; downloaded scripts use `asyncio.run(main())`. Prepared files are recreated for each run. Only generated files explicitly downloaded or retained in saved results outlive that run's temporary directory.

## Development and verification

Use Node 24 and Python 3.14 (the authoring and native checks also work on Python 3.12).

```sh
npm ci
npm run build
npm run check
npm test
node tests/wasm-course.mjs
npx playwright install chromium
npm run test:browser
npm run dev
```

`content/course.py` is the authoritative, readable curriculum. `content/kernel.py` is shared by native tests and the browser interpreter. The build verifies starters, guided edits and reference solutions, produces project ZIPs and creates the immutable release manifest. The Wasm suite runs the same programs in actual Pyodide. Browser tests exercise real controls, multiple source files, saved work, runtime failures, offline operation, updates, keyboard navigation, widths and themes.

Functional checks verify program and interface behaviour; they do not establish learning effectiveness. See the [learning design](docs/learning-design.md), [course style](docs/course-style.md), [runner design](docs/code-runner-design.md) and [offline/update contract](docs/offline-update-design.md).

Original content and application code: MIT. [Third-party notices](THIRD_PARTY.md).
