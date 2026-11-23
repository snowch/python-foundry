# Python Foundry learning design

## Audience, gap and delivery

This is a self-directed, browser-based course for people who can use a browser and type text but have not programmed before. Their target is to read, change and build small Python programs that handle real input, structured data and files, with tests and clear failure handling. Prior programming, command-line and database knowledge are not prerequisites.

The gap is procedural as well as conceptual: newcomers need to connect statements to observable output, choose data structures, trace control flow and debug a program instead of only recognizing syntax. A course with editable examples, predictions, bounded experiments and independent applications addresses that gap. Browser execution removes initial installation work; desktop environment and packaging instructions are introduced later and clearly labelled.

Successful functional performance means the learner can explain a new program’s output, make a specified change, distinguish a valid experiment from a failed check, and build a small tested project from separate files. We have not measured learning transfer or retention in a learner study. Automated checks establish that examples, suggested edits and controls work, not that learners understand them.

## Sequence and coverage

The 122 lessons progress through 20 chapters from printing and names to decisions, collections, reusable functions, data parsing, files, reliability, project organization, objects, language patterns, lazy iteration, applications, async work, application projects, data structures and algorithms, and a staged TinyDB implementation. Prerequisites always refer backward. Necessary syntax is explained before it is relied on; later coverage deepens earlier uses such as file exceptions and context managers.

Six projects integrate earlier concepts: normalized word counts, a Decimal ledger, a multi-file inventory, an argument-driven report, a parameterized SQLite catalog and controlled async transformations. Eighteen further lessons implement and analyze search, sorting, stack/queue/link/hash/heap/tree representations, graph traversals, scheduling, weighted paths and dynamic programming. Twelve TinyDB lessons turn those structures into a checked snapshot engine with a B+ index, transactions, recovery and a persistent browser workspace. Browser activities use real standard-library operations and concrete fixtures, not precomputed output or a simulated Python evaluator. Desktop-only tools are separate instructions and never presented as actions inside the Python editor.

## Lesson and assessment contract

Each lesson owns an observable goal, two short explanatory passages, prepared state, a prediction, one complete program, one exact Find/Replace experiment and an evidence question. The practice program is independent: its instructions state the task and display the expected output. Reusable-function tasks also show additional calls and expected return values, and checks actually invoke those functions.

An edited example can produce any valid output without being called a failed assessment. Python exceptions retain their type, filename and source line. Practice mismatches are reported separately from program execution errors. Runtime asset failures open a recovery dialog instead of masquerading as errors in learner code. Reading completion is explicit and reversible; passing a practice check does not automatically mark a lesson complete.

Essential explanations and actions stay visible. Reference solutions are optional disclosures because revealing an answer after attempting practice has a clear benefit. References link directly to relevant official documentation. The outline, completion state, notebook-free project ZIPs, saved predictions and results support returning to a lesson without repeating setup.

## Diagrams and limits of claims

Use relationship diagrams where prose otherwise requires a mental reconstruction: bindings and rebinding, a function’s input/return path, mutually exclusive branches, nested loops, shared references versus a copied list, transaction commit/rollback, and async suspension/resumption. Branch diagrams branch rather than displaying alternatives as consecutive steps. The copy diagram explicitly describes the pre-append state; output is the evidence for the actual edited run.

Operation counts are labelled as counts, not measured speed. Timing examples keep deterministic correctness separate from elapsed time and explain repetition/variability. Async tasks demonstrate cooperative concurrency, not CPU parallelism. Decimal arithmetic, Unicode lengths, parameterized SQL and shallow copies retain their necessary conditions and caveats.

## Verification and future evaluation

Run every starter, its stated edit and every practice solution with CPython and Pyodide. Inspect real user paths on phones, tablets and wide screens in both themes. Test input, arguments, multi-file imports, generated exports, restored work, errors, cancellation, worker reuse, idle release and genuine network-off operation. Test interrupted updates and all-window restart veto/commit, not only one successful download.

A later learner evaluation should observe novices attempting selected tasks without coaching, note where they misinterpret a name/control/output, and check transfer with a new input or project. Manual completion rates and passing implementation tests are not evidence of that learning outcome.
