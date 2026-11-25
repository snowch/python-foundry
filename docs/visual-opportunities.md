# Visual opportunities across the whole course

Reviewed on 25 November 2026 against `dbac5923f2fc5b7026d265e92481004fc761184e`. This extends the review beyond existing diagrams: 122 lessons have coverage records, including 24 newly illustrated lessons and 13 revised models.

Follow the [shared course-design guide](https://github.com/snowch/cuda-python-lab/blob/main/docs/course-design-guide.md). No dedicated UX or learning skill was available; this records equivalent design and learning reviews.

## Learning review

Look for references to shared objects, changing slots, exclusive bounds, call/return state, alternative branches, dependency edges, occupancy thresholds and publication/retention boundaries. Add a model when it answers a named question more directly than code/output alone. Keep simple syntax, API lookup and one-step results concise. The JSON companion quotes the passage, pins the starter source, and records each selected question, parts, connections, values, units and assumptions. Keep prerequisite definitions visible. Static models explicitly describe the supplied example, not arbitrary source edits.

## Presentation review

Before: spatial relationships were sometimes encoded in prose cards, small labels or a differently sized example. After: stable indexed cells for storage/ranges, converging name-to-object edges for aliases, actual graph/tree links, explicit alternatives, and labelled dependency tables. Essential model labels use live text at 16px or larger. Use theme roles and text/shape cues as well as color. Retain local scroll only where needed; never shrink the whole model to conceal small type.

## Reading order and scope

Keep the course’s existing reading order and compact lesson navigation. Put models next to the worked explanation/result without moving the editor into another page. Models never execute code, modify source/Input, write storage or mark completion. Keep the existing fgets interaction in C. A model can replace repeated relationship narration; it does not replace preconditions, definitions or caveats.

## Curated additions and revisions

| Lesson | Decision | Question answered |
| --- | --- | --- |
| [Choose whether a block runs](https://snowch.github.io/python-foundry/?lesson=if) | Revised | For score=7, why are pass and finished both printed? |
| [Select an item or a slice](https://snowch.github.io/python-foundry/?lesson=index-slice) | Added | Why does values[1:3] produce [20,30]? |
| [Choose a numeric loop boundary](https://snowch.github.io/python-foundry/?lesson=range) | Added | Why does range(1,4) print 1,2,3? |
| [Pair corresponding values](https://snowch.github.io/python-foundry/?lesson=zip) | Added | Why is score 5 not printed? |
| [Trace a loop inside a loop](https://snowch.github.io/python-foundry/?lesson=nested-loops) | Revised | Why do two rows and two columns produce four pairs? |
| [Keep a function’s local names local](https://snowch.github.io/python-foundry/?lesson=scope) | Added | Why does the caller still print count as 3? |
| [Make a smaller recursive call](https://snowch.github.io/python-foundry/?lesson=recursion) | Added | Why do 3,2,1 print before go? |
| [Distinguish characters from encoded bytes](https://snowch.github.io/python-foundry/?lesson=unicode-bytes) | Added | Why is café length 4 as text but length 5 as bytes? |
| [Distinguish a shared object from a shallow copy](https://snowch.github.io/python-foundry/?lesson=copying) | Revised | Why does alias.append(3) change original but leave copy unchanged? |
| [Avoid sharing a default list between calls](https://snowch.github.io/python-foundry/?lesson=mutable-defaults) | Added | Why do the calls print [a] and [b] rather than one accumulating list? |
| [Consume an iterator one item at a time](https://snowch.github.io/python-foundry/?lesson=iterators) | Added | Where did 2 go when list(iterator) prints [4,6]? |
| [Yield values without building the whole result](https://snowch.github.io/python-foundry/?lesson=generators) | Added | Why does next(result) return 4 before list(result) returns [9,16]? |
| [Guarantee cleanup with a context manager](https://snowch.github.io/python-foundry/?lesson=context-managers) | Added | Why does close print even when the with body raises? |
| [Commit or roll back a group of changes](https://snowch.github.io/python-foundry/?lesson=transactions) | Revised | Why is the final row count 0 in the unchanged program? |
| [Coordinate two async operations](https://snowch.github.io/python-foundry/?lesson=async-gather) | Revised | How can b start before a finishes while results remain [A,B]? |
| [Cancel a task and observe cleanup](https://snowch.github.io/python-foundry/?lesson=async-cancel) | Added | Why does cleanup print before cancelled? |
| [Halve a sorted search interval](https://snowch.github.io/python-foundry/?lesson=dsa-binary-search) | Revised | Why does lower bound for 4 return index 1 rather than index 2? |
| [Maintain a sorted prefix with insertion sort](https://snowch.github.io/python-foundry/?lesson=dsa-insertion-sort) | Added | Which value would be lost without the separate key? |
| [Merge two sorted halves](https://snowch.github.io/python-foundry/?lesson=dsa-merge-sort) | Revised | Which next value should the merge consume? |
| [Move two pointers toward a target sum](https://snowch.github.io/python-foundry/?lesson=dsa-two-pointers) | Added | Why does the starter return (1,8) immediately? |
| [Use a stack to match nested brackets](https://snowch.github.io/python-foundry/?lesson=dsa-stack) | Added | How does the stack change for (()())? |
| [Keep arrival order with a deque](https://snowch.github.io/python-foundry/?lesson=dsa-queue) | Added | Why does popleft return first while second and third remain? |
| [Follow links between nodes](https://snowch.github.io/python-foundry/?lesson=dsa-linked-list) | Revised | Which node is new, and which links remain? |
| [Resolve a collision in a hash table](https://snowch.github.io/python-foundry/?lesson=dsa-hash-table) | Added | Why does updating key 1 leave key 5 in the same bucket? |
| [Retrieve the smallest priority from a heap](https://snowch.github.io/python-foundry/?lesson=dsa-heap) | Added | Which pending item has the lowest priority? |
| [Compare a search tree’s order with its height](https://snowch.github.io/python-foundry/?lesson=dsa-bst) | Added | Why is in-order traversal [1,2,3] with height 2? |
| [Represent vertices and edges explicitly](https://snowch.github.io/python-foundry/?lesson=dsa-graph-model) | Revised | Why can D be reached from both B and C? |
| [Find shortest unweighted paths with a queue](https://snowch.github.io/python-foundry/?lesson=dsa-bfs) | Revised | Why can D be reached from both B and C? |
| [Schedule tasks only after their dependencies](https://snowch.github.io/python-foundry/?lesson=dsa-topological) | Added | Why must transform wait for read, and write for transform? |
| [Find minimum total weight with a priority queue](https://snowch.github.io/python-foundry/?lesson=dsa-dijkstra) | Added | Why is the final distance to B equal to 3 rather than 5? |
| [Reuse smaller solutions in a dynamic program](https://snowch.github.io/python-foundry/?lesson=dsa-dynamic-programming) | Added | Which final coin gives the fewest coins for amount 6? |
| [TinyDB: route a lookup through B+ separators](https://snowch.github.io/python-foundry/?lesson=tdb-index-search) | Revised | Where does key 3 go when the separator is 3? |
| [TinyDB: split an overflowing leaf](https://snowch.github.io/python-foundry/?lesson=tdb-index-split) | Added | Which insertion crosses the three-key leaf capacity? |
| [TinyDB: continue a range scan across leaves](https://snowch.github.io/python-foundry/?lesson=tdb-range) | Added | Why can between(2,5) continue without returning to the root? |
| [TinyDB: stage several changes before committing](https://snowch.github.io/python-foundry/?lesson=tdb-transactions) | Revised | Which score survives after reopening? |
| [TinyDB: retain a transaction after a statement error](https://snowch.github.io/python-foundry/?lesson=tdb-statement-errors) | Added | Why can COMMIT still save Ada after the duplicate insert fails? |
| [TinyDB: recover after a simulated interrupted commit](https://snowch.github.io/python-foundry/?lesson=tdb-journal) | Revised | At which stopping point does recovery choose the new generation? |

## Complete coverage

See [all per-lesson decisions, passages and model specifications](visual-opportunities.json). “Keep prose” means no additional visual is selected for that focused objective in this pass; it is not a claim that no possible illustration could help. Existing figures outside the changed set remain available.

## Verification

Build, static/offline checks, the full native/unit suite, real Python browser execution, multi-file editing, saved work, update/offline/recovery journeys, persistent TinyDB and navigation checks passed. The dedicated figure check passed for 37 models across 222 viewport/theme states, including readable essential labels, expanded text alternatives, byte-group consistency, graph-node overlap, page overflow and no compiler startup on navigation. These checks do not measure learning effectiveness.
