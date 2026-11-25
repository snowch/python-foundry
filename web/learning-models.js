export const learningModels = {
  "copying": {
    "title": "Two names can reach one list",
    "question": "Why does alias.append(3) change original but leave copy unchanged?",
    "kind": "references",
    "states": [
      {
        "label": "Before append",
        "objects": [
          {
            "label": "List A",
            "value": "[1, 2]",
            "refs": [
              {
                "name": "original",
                "edge": "refers to A"
              },
              {
                "name": "alias",
                "edge": "refers to A"
              }
            ]
          },
          {
            "label": "List B",
            "value": "[1, 2]",
            "refs": [
              {
                "name": "copy",
                "edge": "refers to B"
              }
            ]
          }
        ]
      },
      {
        "label": "After alias.append(3)",
        "objects": [
          {
            "label": "Same list A",
            "value": "[1, 2, 3]",
            "refs": [
              {
                "name": "original",
                "edge": "still A"
              },
              {
                "name": "alias",
                "edge": "still A"
              }
            ]
          },
          {
            "label": "Same list B",
            "value": "[1, 2]",
            "refs": [
              {
                "name": "copy",
                "edge": "unchanged"
              }
            ]
          }
        ]
      }
    ],
    "note": "The printed lists differ, while original is alias is True. list.copy creates a separate outer list; it is a shallow copy, not a recursive copy of nested objects.",
    "description": "Why does alias.append(3) change original but leave copy unchanged? Before append: List A contains [1, 2]. original refers to A List A; alias refers to A List A; List B contains [1, 2]. copy refers to B List B. After alias.append(3): Same list A contains [1, 2, 3]. original still A Same list A; alias still A Same list A; Same list B contains [1, 2]. copy unchanged Same list B. The printed lists differ, while original is alias is True. list.copy creates a separate outer list; it is a shallow copy, not a recursive copy of nested objects."
  },
  "if": {
    "title": "One branch runs; both paths reach the final print",
    "question": "For score=7, why are pass and finished both printed?",
    "kind": "branch",
    "root": "score ≥ 6?",
    "paths": [
      {
        "when": "True · 7 ≥ 6",
        "result": "print pass",
        "detail": ""
      },
      {
        "when": "False · not selected",
        "result": "print retry",
        "detail": ""
      }
    ],
    "join": "After either branch: print finished",
    "note": "Only one indented branch executes. The final print is outside the conditional and runs after either path.",
    "description": "For score=7, why are pass and finished both printed? score ≥ 6?. True · 7 ≥ 6. print pass. ; False · not selected. print retry. . After either branch: print finished. Only one indented branch executes. The final print is outside the conditional and runs after either path."
  },
  "nested-loops": {
    "title": "Each row visits both columns",
    "question": "Why do two rows and two columns produce four pairs?",
    "kind": "table",
    "headings": [
      "Outer row",
      "Inner column a",
      "Inner column b"
    ],
    "rows": [
      [
        "1",
        "1: (1,a)",
        "2: (1,b)"
      ],
      [
        "2",
        "3: (2,a)",
        "4: (2,b)"
      ]
    ],
    "label": "Printed order: 1 → 2 → 3 → 4",
    "links": [],
    "note": "The inner loop starts again for each outer value. The grid counts combinations and their order; it is not a timing measurement.",
    "description": "Why do two rows and two columns produce four pairs? Outer row; Inner column a; Inner column b. 1; 1: (1,a); 2: (1,b); 2; 3: (2,a); 4: (2,b). Printed order: 1 → 2 → 3 → 4. . The inner loop starts again for each outer value. The grid counts combinations and their order; it is not a timing measurement."
  },
  "dsa-binary-search": {
    "title": "The original positions stay fixed",
    "question": "Why does lower bound for 4 return index 1 rather than index 2?",
    "kind": "slots",
    "rows": [
      {
        "label": "[0,8)",
        "values": [
          2,
          4,
          4,
          6,
          8,
          10,
          12,
          14
        ],
        "note": "8 ≥ 4 → hi=4",
        "active": [
          0,
          1,
          2,
          3,
          4,
          5,
          6,
          7
        ],
        "muted": [],
        "tags": {
          "4": "mid"
        }
      },
      {
        "label": "[0,4)",
        "values": [
          2,
          4,
          4,
          6,
          8,
          10,
          12,
          14
        ],
        "note": "4 ≥ 4 → hi=2",
        "active": [
          0,
          1,
          2,
          3
        ],
        "muted": [
          4,
          5,
          6,
          7
        ],
        "tags": {
          "2": "mid"
        }
      },
      {
        "label": "[0,2)",
        "values": [
          2,
          4,
          4,
          6,
          8,
          10,
          12,
          14
        ],
        "note": "4 ≥ 4 → hi=1",
        "active": [
          0,
          1
        ],
        "muted": [
          2,
          3,
          4,
          5,
          6,
          7
        ],
        "tags": {
          "1": "mid"
        }
      },
      {
        "label": "[0,1)",
        "values": [
          2,
          4,
          4,
          6,
          8,
          10,
          12,
          14
        ],
        "note": "2 < 4 → lo=1",
        "active": [
          0
        ],
        "muted": [
          1,
          2,
          3,
          4,
          5,
          6,
          7
        ],
        "tags": {
          "0": "mid"
        }
      },
      {
        "label": "[1,1) · stop",
        "values": [
          2,
          4,
          4,
          6,
          8,
          10,
          12,
          14
        ],
        "note": "The first not-less position is 1; the equality check succeeds.",
        "active": [],
        "muted": [
          0,
          1,
          2,
          3,
          4,
          5,
          6,
          7
        ]
      }
    ],
    "note": "The input must be sorted. lo is inclusive and hi exclusive. Lower bound returns an insertion position; check bounds and equality before claiming membership.",
    "description": "Why does lower bound for 4 return index 1 rather than index 2? [0,8): index 0 = 2, index 1 = 4, index 2 = 4, index 3 = 6, index 4 = 8, index 5 = 10, index 6 = 12, index 7 = 14. 8 ≥ 4 → hi=4. [0,4): index 0 = 2, index 1 = 4, index 2 = 4, index 3 = 6, index 4 = 8, index 5 = 10, index 6 = 12, index 7 = 14. 4 ≥ 4 → hi=2. [0,2): index 0 = 2, index 1 = 4, index 2 = 4, index 3 = 6, index 4 = 8, index 5 = 10, index 6 = 12, index 7 = 14. 4 ≥ 4 → hi=1. [0,1): index 0 = 2, index 1 = 4, index 2 = 4, index 3 = 6, index 4 = 8, index 5 = 10, index 6 = 12, index 7 = 14. 2 < 4 → lo=1. [1,1) · stop: index 0 = 2, index 1 = 4, index 2 = 4, index 3 = 6, index 4 = 8, index 5 = 10, index 6 = 12, index 7 = 14. The first not-less position is 1; the equality check succeeds.. The input must be sorted. lo is inclusive and hi exclusive. Lower bound returns an insertion position; check bounds and equality before claiming membership."
  },
  "async-gather": {
    "title": "Two coroutines yield independently",
    "question": "How can b start before a finishes while results remain [A,B]?",
    "kind": "table",
    "headings": [
      "Participant",
      "Start and suspend",
      "Resume and finish"
    ],
    "rows": [
      [
        "Task a",
        "print start a; await sleep(0)",
        "print finish a; return A"
      ],
      [
        "Task b",
        "print start b; await sleep(0)",
        "print finish b; return B"
      ],
      [
        "gather",
        "Schedules the two calls",
        "Returns [A,B] in call order"
      ]
    ],
    "label": "Dependencies, not a proportional time axis",
    "links": [
      "Each await permits the event loop to run another ready task.",
      "Result slot 0 belongs to call a; slot 1 belongs to call b, independently of completion order."
    ],
    "note": "The unchanged starter prints start a, start b, finish a, finish b. This illustrates cooperative scheduling, not measured timings or CPU parallelism.",
    "description": "How can b start before a finishes while results remain [A,B]? Participant; Start and suspend; Resume and finish. Task a; print start a; await sleep(0); print finish a; return A; Task b; print start b; await sleep(0); print finish b; return B; gather; Schedules the two calls; Returns [A,B] in call order. Dependencies, not a proportional time axis. Each await permits the event loop to run another ready task.; Result slot 0 belongs to call a; slot 1 belongs to call b, independently of completion order.. The unchanged starter prints start a, start b, finish a, finish b. This illustrates cooperative scheduling, not measured timings or CPU parallelism."
  },
  "dsa-linked-list": {
    "title": "Prepending reuses the old nodes",
    "question": "Which node is new, and which links remain?",
    "kind": "panels",
    "panels": [
      {
        "label": "Before prepend",
        "model": {
          "kind": "graph",
          "nodes": [
            {
              "id": "h",
              "label": "head",
              "x": 12,
              "y": 50
            },
            {
              "id": "2",
              "label": "2",
              "x": 44,
              "y": 50
            },
            {
              "id": "3",
              "label": "3",
              "x": 76,
              "y": 50
            }
          ],
          "edges": [
            {
              "from": "h",
              "to": "2",
              "label": ""
            },
            {
              "from": "2",
              "to": "3",
              "label": "next"
            }
          ],
          "legend": "Node 3.next is None.",
          "height": 160
        }
      },
      {
        "label": "After prepend",
        "model": {
          "kind": "graph",
          "nodes": [
            {
              "id": "h",
              "label": "head",
              "x": 9,
              "y": 50
            },
            {
              "id": "1",
              "label": "1",
              "x": 34,
              "y": 50
            },
            {
              "id": "2",
              "label": "2",
              "x": 59,
              "y": 50
            },
            {
              "id": "3",
              "label": "3",
              "x": 84,
              "y": 50
            }
          ],
          "edges": [
            {
              "from": "h",
              "to": "1",
              "label": ""
            },
            {
              "from": "1",
              "to": "2",
              "label": "next"
            },
            {
              "from": "2",
              "to": "3",
              "label": "next"
            }
          ],
          "legend": "Only node 1 is new. Nodes 2 and 3 retain their identity; the traversal prints 1,2,3.",
          "height": 160
        }
      }
    ],
    "note": "Positions preserve logical node identity, not physical addresses or adjacency. next is a Python reference.",
    "description": "Which node is new, and which links remain? Before prepend. Nodes: head, 2, 3. Connections: head leads to 2; 2 leads to 3 (next). Node 3.next is None.; After prepend. Nodes: head, 1, 2, 3. Connections: head leads to 1; 1 leads to 2 (next); 2 leads to 3 (next). Only node 1 is new. Nodes 2 and 3 retain their identity; the traversal prints 1,2,3.. Positions preserve logical node identity, not physical addresses or adjacency. next is a Python reference."
  },
  "dsa-merge-sort": {
    "title": "Two sorted fronts feed one output",
    "question": "Which next value should the merge consume?",
    "kind": "panels",
    "panels": [
      {
        "label": "Split and sort the starter halves",
        "model": {
          "kind": "table",
          "headings": [
            "Original half",
            "Sorted half"
          ],
          "rows": [
            [
              "[7,2]",
              "[2,7]"
            ],
            [
              "[5,2]",
              "[2,5]"
            ]
          ],
          "label": "",
          "links": []
        }
      },
      {
        "label": "Consume the next available front",
        "model": {
          "kind": "table",
          "headings": [
            "Choice",
            "Left remaining",
            "Right remaining",
            "Output"
          ],
          "rows": [
            [
              "Left 2",
              "[7]",
              "[2,5]",
              "[2]"
            ],
            [
              "Right 2",
              "[7]",
              "[5]",
              "[2,2]"
            ],
            [
              "Right 5",
              "[7]",
              "[]",
              "[2,2,5]"
            ],
            [
              "Left 7",
              "[]",
              "[]",
              "[2,2,5,7]"
            ]
          ],
          "label": "",
          "links": []
        }
      }
    ],
    "note": "The original [7,2,5,2] remains unchanged in this implementation. Consuming the left equal value first preserves equal-key order.",
    "description": "Which next value should the merge consume? Split and sort the starter halves. Original half; Sorted half. [7,2]; [2,7]; [5,2]; [2,5]. . ; Consume the next available front. Choice; Left remaining; Right remaining; Output. Left 2; [7]; [2,5]; [2]; Right 2; [7]; [5]; [2,2]; Right 5; [7]; []; [2,2,5]; Left 7; []; []; [2,2,5,7]. . . The original [7,2,5,2] remains unchanged in this implementation. Consuming the left equal value first preserves equal-key order."
  },
  "transactions": {
    "title": "A normal exit and an exception choose different outcomes",
    "question": "Why is the final row count 0 in the unchanged program?",
    "kind": "branch",
    "root": "Insert one row inside the transaction",
    "paths": [
      {
        "when": "Normal block exit · comparison case",
        "result": "Commit → count 1",
        "detail": ""
      },
      {
        "when": "ValueError · unchanged starter",
        "result": "Rollback → count 0",
        "detail": ""
      }
    ],
    "join": "Query the row count after leaving the block",
    "note": "The starter deliberately raises ValueError. The normal-exit branch is a comparison, not another action performed by that run.",
    "description": "Why is the final row count 0 in the unchanged program? Insert one row inside the transaction. Normal block exit · comparison case. Commit → count 1. ; ValueError · unchanged starter. Rollback → count 0. . Query the row count after leaving the block. The starter deliberately raises ValueError. The normal-exit branch is a comparison, not another action performed by that run."
  },
  "tdb-transactions": {
    "title": "Staged score and saved score are separate",
    "question": "Which score survives after reopening?",
    "kind": "branch",
    "root": "Committed score 42; staged UPDATE sets 73",
    "paths": [
      {
        "when": "COMMIT · starter",
        "result": "Saved score 73",
        "detail": "Reopen observes the new committed snapshot."
      },
      {
        "when": "ROLLBACK · edit variant",
        "result": "Saved score 42",
        "detail": "Discard the candidate; keep the previous snapshot."
      }
    ],
    "note": "Rollback is a deliberate transaction decision. It is different from reopening after an interrupted commit.",
    "description": "Which score survives after reopening? Committed score 42; staged UPDATE sets 73. COMMIT · starter. Saved score 73. Reopen observes the new committed snapshot.; ROLLBACK · edit variant. Saved score 42. Discard the candidate; keep the previous snapshot.. Rollback is a deliberate transaction decision. It is different from reopening after an interrupted commit."
  },
  "tdb-journal": {
    "title": "A committed marker changes the recovery decision",
    "question": "At which stopping point does recovery choose the new generation?",
    "kind": "table",
    "headings": [
      "Interrupted phase",
      "Journal decision",
      "On reopen"
    ],
    "rows": [
      [
        "prepare",
        "Candidate only; not committed",
        "Discard candidate; retain old rows"
      ],
      [
        "commit",
        "Committed marker present",
        "Replay candidate if necessary"
      ],
      [
        "install",
        "Committed data installed",
        "Replay/check safely; remove journal"
      ]
    ],
    "label": "Recovery boundaries",
    "links": [],
    "note": "Prepared and committed are distinct states in this teaching protocol. A recoverable committed decision is not proof of production flush ordering or physical-disk durability.",
    "description": "At which stopping point does recovery choose the new generation? Interrupted phase; Journal decision; On reopen. prepare; Candidate only; not committed; Discard candidate; retain old rows; commit; Committed marker present; Replay candidate if necessary; install; Committed data installed; Replay/check safely; remove journal. Recovery boundaries. . Prepared and committed are distinct states in this teaching protocol. A recoverable committed decision is not proof of production flush ordering or physical-disk durability."
  },
  "unicode-bytes": {
    "title": "One scalar value can use two UTF-8 bytes",
    "question": "Why is café length 4 as text but length 5 as bytes?",
    "kind": "bytes",
    "label": "Unicode scalar values aligned with UTF-8 bytes",
    "values": [
      "63",
      "61",
      "66",
      "C3",
      "A9"
    ],
    "groups": [
      {
        "label": "c",
        "size": 1
      },
      {
        "label": "a",
        "size": 1
      },
      {
        "label": "f",
        "size": 1
      },
      {
        "label": "é",
        "size": 2
      }
    ],
    "note": "len(text) counts code points in this example; len(data) counts bytes. A code point is not always a complete user-perceived character. Decoding the full byte sequence restores café.",
    "description": "Why is café length 4 as text but length 5 as bytes? Unicode scalar values aligned with UTF-8 bytes. c uses byte offsets 0: 63; a uses byte offsets 1: 61; f uses byte offsets 2: 66; é uses byte offsets 3 through 4: C3, A9. len(text) counts code points in this example; len(data) counts bytes. A code point is not always a complete user-perceived character. Decoding the full byte sequence restores café."
  },
  "index-slice": {
    "title": "A slice includes its start and excludes its stop",
    "question": "Why does values[1:3] produce [20,30]?",
    "kind": "slots",
    "rows": [
      {
        "label": "Original values",
        "values": [
          10,
          20,
          30,
          40
        ],
        "note": "Index 0 → 10; index -1 → 40. The slice includes indices 1 and 2.",
        "active": [
          1,
          2
        ],
        "muted": [
          0,
          3
        ],
        "tags": {
          "1": "start",
          "3": "stop excluded"
        }
      }
    ],
    "note": "A list slice creates a new outer list of the selected values. The stop boundary is not another included element.",
    "description": "Why does values[1:3] produce [20,30]? Original values: index 0 = 10, index 1 = 20, index 2 = 30, index 3 = 40. Index 0 → 10; index -1 → 40. The slice includes indices 1 and 2.. A list slice creates a new outer list of the selected values. The stop boundary is not another included element."
  },
  "range": {
    "title": "The stop value is excluded",
    "question": "Why does range(1,4) print 1,2,3?",
    "kind": "table",
    "headings": [
      "Range",
      "Produced values",
      "Excluded boundary"
    ],
    "rows": [
      [
        "range(1,4)",
        "1 → 2 → 3",
        "4"
      ],
      [
        "range(0,6,2)",
        "0 → 2 → 4",
        "6"
      ]
    ],
    "label": "",
    "links": [],
    "note": "These are the two ranges in the starter. range describes integer steps without storing a list of every value; list(...) materializes one for the second print.",
    "description": "Why does range(1,4) print 1,2,3? Range; Produced values; Excluded boundary. range(1,4); 1 → 2 → 3; 4; range(0,6,2); 0 → 2 → 4; 6. . . These are the two ranges in the starter. range describes integer steps without storing a list of every value; list(...) materializes one for the second print."
  },
  "zip": {
    "title": "zip stops at the shorter input",
    "question": "Why is score 5 not printed?",
    "kind": "table",
    "headings": [
      "Position",
      "names",
      "scores",
      "Paired output"
    ],
    "rows": [
      [
        "0",
        "Ada",
        "9",
        "Ada 9"
      ],
      [
        "1",
        "Lin",
        "7",
        "Lin 7"
      ],
      [
        "2",
        "No name",
        "5",
        "No pair"
      ]
    ],
    "label": "",
    "links": [],
    "note": "Default zip stops when one input ends. The extra score is not matched with a missing name. strict=True is a separate contract.",
    "description": "Why is score 5 not printed? Position; names; scores; Paired output. 0; Ada; 9; Ada 9; 1; Lin; 7; Lin 7; 2; No name; 5; No pair. . . Default zip stops when one input ends. The extra score is not matched with a missing name. strict=True is a separate contract."
  },
  "scope": {
    "title": "A function parameter is a local name",
    "question": "Why does the caller still print count as 3?",
    "kind": "table",
    "headings": [
      "Step",
      "Caller count",
      "Local parameter count"
    ],
    "rows": [
      [
        "Before call",
        "3",
        "not present"
      ],
      [
        "Inside next_count",
        "3",
        "3 → 4"
      ],
      [
        "After return",
        "3",
        "local call finished; result 4 returned"
      ]
    ],
    "label": "",
    "links": [],
    "note": "Rebinding the local parameter does not rebind the caller’s name. The first print uses the returned 4; the second reads caller count=3.",
    "description": "Why does the caller still print count as 3? Step; Caller count; Local parameter count. Before call; 3; not present; Inside next_count; 3; 3 → 4; After return; 3; local call finished; result 4 returned. . . Rebinding the local parameter does not rebind the caller’s name. The first print uses the returned 4; the second reads caller count=3."
  },
  "recursion": {
    "title": "Each call retains its own number",
    "question": "Why do 3,2,1 print before go?",
    "kind": "frames",
    "frames": [
      {
        "call": "countdown(3)",
        "pending": "print 3; call countdown(2)",
        "result": "Returns after the smaller call"
      },
      {
        "call": "countdown(2)",
        "pending": "print 2; call countdown(1)",
        "result": "Returns to countdown(3)"
      },
      {
        "call": "countdown(1)",
        "pending": "print 1; call countdown(0)",
        "result": "Returns to countdown(2)"
      },
      {
        "call": "countdown(0)",
        "pending": "Base case: print go",
        "result": "Return without another recursive call"
      }
    ],
    "note": "These are logical call frames. Each call has its own local number; a smaller argument is required for termination.",
    "description": "Why do 3,2,1 print before go? countdown(3). print 3; call countdown(2). Returns after the smaller call; countdown(2). print 2; call countdown(1). Returns to countdown(3); countdown(1). print 1; call countdown(0). Returns to countdown(2); countdown(0). Base case: print go. Return without another recursive call. These are logical call frames. Each call has its own local number; a smaller argument is required for termination."
  },
  "mutable-defaults": {
    "title": "Each omitted argument gets a fresh list here",
    "question": "Why do the calls print [a] and [b] rather than one accumulating list?",
    "kind": "references",
    "states": [
      {
        "label": "Two calls with items=None",
        "objects": [
          {
            "label": "First call’s new list",
            "value": "['a']",
            "refs": [
              {
                "name": "add_item(a)",
                "edge": "creates inside the function"
              }
            ]
          },
          {
            "label": "Second call’s new list",
            "value": "['b']",
            "refs": [
              {
                "name": "add_item(b)",
                "edge": "creates another list"
              }
            ]
          }
        ]
      }
    ],
    "note": "The default None is evaluated at definition time. items=[] runs separately inside each call. Using [] as the default would share one list across calls; that is a contrasting edit, not this starter.",
    "description": "Why do the calls print [a] and [b] rather than one accumulating list? Two calls with items=None: First call’s new list contains ['a']. add_item(a) creates inside the function First call’s new list; Second call’s new list contains ['b']. add_item(b) creates another list Second call’s new list. The default None is evaluated at definition time. items=[] runs separately inside each call. Using [] as the default would share one list across calls; that is a contrasting edit, not this starter."
  },
  "iterators": {
    "title": "Consumption advances one iterator",
    "question": "Where did 2 go when list(iterator) prints [4,6]?",
    "kind": "slots",
    "rows": [
      {
        "label": "Before next(iterator)",
        "values": [
          2,
          4,
          6
        ],
        "note": "Next position is index 0.",
        "active": [
          0
        ],
        "muted": []
      },
      {
        "label": "After next returns 2",
        "values": [
          2,
          4,
          6
        ],
        "note": "list(iterator) consumes only remaining values 4 and 6.",
        "active": [
          1,
          2
        ],
        "muted": [
          0
        ]
      },
      {
        "label": "After list(iterator)",
        "values": [
          2,
          4,
          6
        ],
        "note": "Iterator exhausted: another list(iterator) returns [].",
        "active": [],
        "muted": [
          0,
          1,
          2
        ]
      }
    ],
    "note": "The original list stays [2,4,6]. The iterator’s position changes; consuming it does not remove list elements.",
    "description": "Where did 2 go when list(iterator) prints [4,6]? Before next(iterator): index 0 = 2, index 1 = 4, index 2 = 6. Next position is index 0.. After next returns 2: index 0 = 2, index 1 = 4, index 2 = 6. list(iterator) consumes only remaining values 4 and 6.. After list(iterator): index 0 = 2, index 1 = 4, index 2 = 6. Iterator exhausted: another list(iterator) returns [].. The original list stays [2,4,6]. The iterator’s position changes; consuming it does not remove list elements."
  },
  "generators": {
    "title": "yield suspends a calculation with state retained",
    "question": "Why does next(result) return 4 before list(result) returns [9,16]?",
    "kind": "table",
    "headings": [
      "Request",
      "Generator work",
      "Returned evidence"
    ],
    "rows": [
      [
        "Create generator",
        "Body has not iterated yet",
        "No square calculated"
      ],
      [
        "next(result)",
        "Visit 2; yield 2*2; suspend",
        "4"
      ],
      [
        "list(result)",
        "Resume with 3, then 4; finish",
        "[9,16]"
      ]
    ],
    "label": "",
    "links": [],
    "note": "The generator resumes where it suspended. It does not rebuild the already yielded 4 or construct all three squares at creation.",
    "description": "Why does next(result) return 4 before list(result) returns [9,16]? Request; Generator work; Returned evidence. Create generator; Body has not iterated yet; No square calculated; next(result); Visit 2; yield 2*2; suspend; 4; list(result); Resume with 3, then 4; finish; [9,16]. . . The generator resumes where it suspended. It does not rebuild the already yielded 4 or construct all three squares at creation."
  },
  "context-managers": {
    "title": "Cleanup surrounds the with body",
    "question": "Why does close print even when the with body raises?",
    "kind": "flow",
    "steps": [
      {
        "label": "Enter resource",
        "detail": "Print open; yield ready."
      },
      {
        "label": "Run with body",
        "detail": "value is ready; the starter prints ready."
      },
      {
        "label": "Leave with body",
        "detail": "Normal exit or an exception resumes cleanup."
      },
      {
        "label": "finally",
        "detail": "Print close."
      }
    ],
    "note": "The unchanged starter uses normal exit. The finally cleanup also runs on exception exit; process termination is outside this demonstration.",
    "description": "Why does close print even when the with body raises? Enter resource. Print open; yield ready.; Run with body. value is ready; the starter prints ready.; Leave with body. Normal exit or an exception resumes cleanup.; finally. Print close.. The unchanged starter uses normal exit. The finally cleanup also runs on exception exit; process termination is outside this demonstration."
  },
  "async-cancel": {
    "title": "Request cancellation, then await cleanup",
    "question": "Why does cleanup print before cancelled?",
    "kind": "table",
    "headings": [
      "Order",
      "main task",
      "work task"
    ],
    "rows": [
      [
        "1",
        "create_task; await sleep(0)",
        "Starts and awaits sleep(10)"
      ],
      [
        "2",
        "task.cancel()",
        "Cancellation requested at an await"
      ],
      [
        "3",
        "await task",
        "finally prints cleanup"
      ],
      [
        "4",
        "catch CancelledError; print cancelled",
        "Task has finished"
      ]
    ],
    "label": "Completion dependencies, not measured time",
    "links": [],
    "note": "cancel requests cancellation; awaiting observes completion. The initial yield lets work begin, so its finally block is active before cancellation.",
    "description": "Why does cleanup print before cancelled? Order; main task; work task. 1; create_task; await sleep(0); Starts and awaits sleep(10); 2; task.cancel(); Cancellation requested at an await; 3; await task; finally prints cleanup; 4; catch CancelledError; print cancelled; Task has finished. Completion dependencies, not measured time. . cancel requests cancellation; awaiting observes completion. The initial yield lets work begin, so its finally block is active before cancellation."
  },
  "dsa-two-pointers": {
    "title": "Endpoints choose which region to discard",
    "question": "Why does the starter return (1,8) immediately?",
    "kind": "slots",
    "rows": [
      {
        "label": "Target 9",
        "values": [
          1,
          3,
          5,
          8
        ],
        "note": "left=0, right=3: 1+8=9, so return the two values.",
        "active": [
          0,
          3
        ],
        "muted": [],
        "tags": {
          "0": "left",
          "3": "right"
        }
      }
    ],
    "note": "On a later unequal sum, sorted order justifies moving left rightward if too small, or right leftward if too large. The unchanged starter does not perform either move.",
    "description": "Why does the starter return (1,8) immediately? Target 9: index 0 = 1, index 1 = 3, index 2 = 5, index 3 = 8. left=0, right=3: 1+8=9, so return the two values.. On a later unequal sum, sorted order justifies moving left rightward if too small, or right leftward if too large. The unchanged starter does not perform either move."
  },
  "dsa-insertion-sort": {
    "title": "Save the key while larger values move right",
    "question": "Which value would be lost without the separate key?",
    "kind": "slots",
    "rows": [
      {
        "label": "First insertion: save key=3",
        "values": [
          4,
          3,
          2,
          1
        ],
        "note": "The prefix [4] is sorted; key=3 is kept in a local variable.",
        "active": [
          0,
          1
        ],
        "muted": []
      },
      {
        "label": "Shift 4 to index 1",
        "values": [
          4,
          4,
          2,
          1
        ],
        "note": "Both slots contain 4 temporarily; key still holds 3.",
        "active": [
          1
        ],
        "muted": []
      },
      {
        "label": "Place key at index 0",
        "values": [
          3,
          4,
          2,
          1
        ],
        "note": "The sorted prefix is now [3,4]. Repeating yields [1,2,3,4] with 6 shifts.",
        "active": [
          0,
          1
        ],
        "muted": []
      }
    ],
    "note": "A logical gap does not mean an uninitialized Python list element. The saved key preserves the value during overlapping assignments.",
    "description": "Which value would be lost without the separate key? First insertion: save key=3: index 0 = 4, index 1 = 3, index 2 = 2, index 3 = 1. The prefix [4] is sorted; key=3 is kept in a local variable.. Shift 4 to index 1: index 0 = 4, index 1 = 4, index 2 = 2, index 3 = 1. Both slots contain 4 temporarily; key still holds 3.. Place key at index 0: index 0 = 3, index 1 = 4, index 2 = 2, index 3 = 1. The sorted prefix is now [3,4]. Repeating yields [1,2,3,4] with 6 shifts.. A logical gap does not mean an uninitialized Python list element. The saved key preserves the value during overlapping assignments."
  },
  "dsa-stack": {
    "title": "Only the most recent unmatched opening can close",
    "question": "How does the stack change for (()())?",
    "kind": "table",
    "headings": [
      "Input prefix",
      "Stack · bottom → top",
      "Action"
    ],
    "rows": [
      [
        "(",
        "(",
        "push"
      ],
      [
        "((",
        "( (",
        "push"
      ],
      [
        "(()",
        "(",
        "pop one opening"
      ],
      [
        "(()(",
        "( (",
        "push"
      ],
      [
        "(()()",
        "(",
        "pop"
      ],
      [
        "(()())",
        "empty",
        "pop; balanced=True"
      ]
    ],
    "label": "",
    "links": [],
    "note": "The starter handles parentheses only. An empty stack at a closing parenthesis rejects immediately; the final stack must also be empty.",
    "description": "How does the stack change for (()())? Input prefix; Stack · bottom → top; Action. (; (; push; ((; ( (; push; ((); (; pop one opening; (()(; ( (; push; (()(); (; pop; (()()); empty; pop; balanced=True. . . The starter handles parentheses only. An empty stack at a closing parenthesis rejects immediately; the final stack must also be empty."
  },
  "dsa-queue": {
    "title": "Remove the oldest pending item",
    "question": "Why does popleft return first while second and third remain?",
    "kind": "slots",
    "rows": [
      {
        "label": "Before popleft",
        "values": [
          "first",
          "second",
          "third"
        ],
        "note": "Front is index 0; back is index 2.",
        "active": [
          0
        ],
        "muted": [],
        "tags": {
          "0": "front",
          "2": "back"
        }
      },
      {
        "label": "After popleft",
        "values": [
          "removed",
          "second",
          "third"
        ],
        "note": "Logical queue is [second,third]. These stable positions illustrate identity, not deque internal storage.",
        "active": [
          1
        ],
        "muted": [
          0
        ],
        "tags": {
          "1": "new front"
        }
      }
    ],
    "note": "The deque’s physical representation is not specified by this illustration. The result is FIFO: first in, first out.",
    "description": "Why does popleft return first while second and third remain? Before popleft: index 0 = first, index 1 = second, index 2 = third. Front is index 0; back is index 2.. After popleft: index 0 = removed, index 1 = second, index 2 = third. Logical queue is [second,third]. These stable positions illustrate identity, not deque internal storage.. The deque’s physical representation is not specified by this illustration. The result is FIFO: first in, first out."
  },
  "dsa-hash-table": {
    "title": "A bucket can contain different keys",
    "question": "Why does updating key 1 leave key 5 in the same bucket?",
    "kind": "table",
    "headings": [
      "Operation",
      "Bucket calculation",
      "Bucket 1 afterward"
    ],
    "rows": [
      [
        "put(1,Ada)",
        "1 % 4 = 1",
        "[(1,Ada)]"
      ],
      [
        "put(5,Lin)",
        "5 % 4 = 1",
        "[(1,Ada),(5,Lin)]"
      ],
      [
        "put(1,Grace)",
        "Compare actual key 1",
        "[(1,Grace),(5,Lin)]"
      ]
    ],
    "label": "",
    "links": [],
    "note": "The modulo hash selects a bucket, not a unique identity. Equality distinguishes colliding keys; the update replaces the matching key’s value.",
    "description": "Why does updating key 1 leave key 5 in the same bucket? Operation; Bucket calculation; Bucket 1 afterward. put(1,Ada); 1 % 4 = 1; [(1,Ada)]; put(5,Lin); 5 % 4 = 1; [(1,Ada),(5,Lin)]; put(1,Grace); Compare actual key 1; [(1,Grace),(5,Lin)]. . . The modulo hash selects a bucket, not a unique identity. Equality distinguishes colliding keys; the update replaces the matching key’s value."
  },
  "dsa-heap": {
    "title": "Parent order is not a fully sorted array",
    "question": "Which pending item has the lowest priority?",
    "kind": "graph",
    "nodes": [
      {
        "id": "r",
        "label": "recover",
        "x": 50,
        "y": 15,
        "detail": "priority 0"
      },
      {
        "id": "a",
        "label": "read",
        "x": 25,
        "y": 50,
        "detail": "priority 1"
      },
      {
        "id": "b",
        "label": "close",
        "x": 78,
        "y": 50,
        "detail": "priority 2"
      },
      {
        "id": "c",
        "label": "write",
        "x": 16,
        "y": 85,
        "detail": "priority 2"
      }
    ],
    "edges": [
      {
        "from": "r",
        "to": "a",
        "label": "",
        "directed": false
      },
      {
        "from": "r",
        "to": "b",
        "label": "",
        "directed": false
      },
      {
        "from": "a",
        "to": "c",
        "label": "",
        "directed": false
      }
    ],
    "legend": "After the starter pushes recover: every parent tuple is ≤ its children. Pop order: recover, read, write, close.",
    "height": 350,
    "note": "Priority ties use the tuple’s sequence field: write has sequence 0, close has sequence 2. The heap array is not globally sorted; this is the actual small starter heap after the push.",
    "description": "Which pending item has the lowest priority? Nodes: recover (priority 0), read (priority 1), close (priority 2), write (priority 2). Connections: recover connects to read; recover connects to close; read connects to write. After the starter pushes recover: every parent tuple is ≤ its children. Pop order: recover, read, write, close.. Priority ties use the tuple’s sequence field: write has sequence 0, close has sequence 2. The heap array is not globally sorted; this is the actual small starter heap after the push."
  },
  "dsa-bst": {
    "title": "An ancestor bounds the whole subtree",
    "question": "Why is in-order traversal [1,2,3] with height 2?",
    "kind": "graph",
    "nodes": [
      {
        "id": "2",
        "label": "2",
        "x": 50,
        "y": 20
      },
      {
        "id": "1",
        "label": "1",
        "x": 22,
        "y": 80
      },
      {
        "id": "3",
        "label": "3",
        "x": 78,
        "y": 80
      }
    ],
    "edges": [
      {
        "from": "2",
        "to": "1",
        "label": "< 2"
      },
      {
        "from": "2",
        "to": "3",
        "label": "> 2"
      }
    ],
    "legend": "Left → node → right visits 1,2,3. Height counts the two occupied node levels.",
    "height": 300,
    "note": "These are the keys inserted by the starter: 2,1,3. Sorted insertion can create a taller chain; ordering alone does not guarantee balance.",
    "description": "Why is in-order traversal [1,2,3] with height 2? Nodes: 2, 1, 3. Connections: 2 leads to 1 (< 2); 2 leads to 3 (> 2). Left → node → right visits 1,2,3. Height counts the two occupied node levels.. These are the keys inserted by the starter: 2,1,3. Sorted insertion can create a taller chain; ordering alone does not guarantee balance."
  },
  "dsa-topological": {
    "title": "A task becomes ready after its prerequisites",
    "question": "Why must transform wait for read, and write for transform?",
    "kind": "graph",
    "nodes": [
      {
        "id": "r",
        "label": "read",
        "x": 16,
        "y": 50
      },
      {
        "id": "t",
        "label": "transform",
        "x": 50,
        "y": 50
      },
      {
        "id": "w",
        "label": "write",
        "x": 84,
        "y": 50
      }
    ],
    "edges": [
      {
        "from": "r",
        "to": "t",
        "label": "before"
      },
      {
        "from": "t",
        "to": "w",
        "label": "before"
      }
    ],
    "legend": "Initial indegrees: read=0, transform=1, write=1. Processing a predecessor decrements the next indegree.",
    "height": 200,
    "note": "A topological order exists only for a directed acyclic graph. If fewer tasks are emitted than graph vertices, the function reports cycle.",
    "description": "Why must transform wait for read, and write for transform? Nodes: read, transform, write. Connections: read leads to transform (before); transform leads to write (before). Initial indegrees: read=0, transform=1, write=1. Processing a predecessor decrements the next indegree.. A topological order exists only for a directed acyclic graph. If fewer tasks are emitted than graph vertices, the function reports cycle."
  },
  "dsa-dijkstra": {
    "title": "A cheaper indirect route can replace a direct route",
    "question": "Why is the final distance to B equal to 3 rather than 5?",
    "kind": "graph",
    "nodes": [
      {
        "id": "A",
        "label": "A",
        "x": 18,
        "y": 20
      },
      {
        "id": "B",
        "label": "B",
        "x": 82,
        "y": 20
      },
      {
        "id": "C",
        "label": "C",
        "x": 50,
        "y": 80
      }
    ],
    "edges": [
      {
        "from": "A",
        "to": "B",
        "label": "5"
      },
      {
        "from": "A",
        "to": "C",
        "label": "1"
      },
      {
        "from": "C",
        "to": "B",
        "label": "2"
      }
    ],
    "legend": "Direct A→B costs 5. A→C→B costs 1+2=3, so distance[B] changes 5→3.",
    "height": 300,
    "note": "All weights must be nonnegative. The priority queue chooses the smallest pending total distance; this picture is not a timing measurement.",
    "description": "Why is the final distance to B equal to 3 rather than 5? Nodes: A, B, C. Connections: A leads to B (5); A leads to C (1); C leads to B (2). Direct A→B costs 5. A→C→B costs 1+2=3, so distance[B] changes 5→3.. All weights must be nonnegative. The priority queue chooses the smallest pending total distance; this picture is not a timing measurement."
  },
  "dsa-dynamic-programming": {
    "title": "Earlier amounts feed best[6]",
    "question": "Which final coin gives the fewest coins for amount 6?",
    "kind": "graph",
    "nodes": [
      {
        "id": "5",
        "label": "best[5]=2",
        "x": 16,
        "y": 18
      },
      {
        "id": "3",
        "label": "best[3]=1",
        "x": 50,
        "y": 18
      },
      {
        "id": "2",
        "label": "best[2]=2",
        "x": 84,
        "y": 18
      },
      {
        "id": "6",
        "label": "best[6]=2",
        "x": 50,
        "y": 85
      }
    ],
    "edges": [
      {
        "from": "5",
        "to": "6",
        "label": "+1 coin → 3"
      },
      {
        "from": "3",
        "to": "6",
        "label": "+3 coin → 2"
      },
      {
        "from": "2",
        "to": "6",
        "label": "+4 coin → 3"
      }
    ],
    "legend": "Candidate totals count coins, not currency value. Choose min(3,2,3)=2: use 3+3.",
    "height": 320,
    "note": "The starter’s coin values are [1,3,4], and best[0]=0. The ascending amount order makes each predecessor answer available before amount 6.",
    "description": "Which final coin gives the fewest coins for amount 6? Nodes: best[5]=2, best[3]=1, best[2]=2, best[6]=2. Connections: best[5]=2 leads to best[6]=2 (+1 coin → 3); best[3]=1 leads to best[6]=2 (+3 coin → 2); best[2]=2 leads to best[6]=2 (+4 coin → 3). Candidate totals count coins, not currency value. Choose min(3,2,3)=2: use 3+3.. The starter’s coin values are [1,3,4], and best[0]=0. The ascending amount order makes each predecessor answer available before amount 6."
  },
  "tdb-index-split": {
    "title": "The fourth key creates a new level",
    "question": "Which insertion crosses the three-key leaf capacity?",
    "kind": "panels",
    "panels": [
      {
        "label": "Unchanged starter: keys 1..3",
        "model": {
          "kind": "slots",
          "rows": [
            {
              "label": "One leaf",
              "values": [
                1,
                2,
                3
              ],
              "note": "rows=3, height=1, leaves=1.",
              "active": [],
              "muted": []
            }
          ]
        }
      },
      {
        "label": "After the instructed edit range(1,5)",
        "model": {
          "kind": "graph",
          "nodes": [
            {
              "id": "root",
              "label": "3",
              "x": 50,
              "y": 18
            },
            {
              "id": "left",
              "label": "[1,2]",
              "x": 22,
              "y": 80
            },
            {
              "id": "right",
              "label": "[3,4]",
              "x": 78,
              "y": 80
            }
          ],
          "edges": [
            {
              "from": "root",
              "to": "left",
              "label": "< 3"
            },
            {
              "from": "root",
              "to": "right",
              "label": "≥ 3"
            }
          ],
          "legend": "rows=4, height=2, leaves=2. Separator 3 is copied into the parent and remains in the right leaf.",
          "height": 300
        }
      }
    ],
    "note": "The second panel is the instructed edit, not the original three-insertion output. These are logical nodes, not fixed-size on-disk pages.",
    "description": "Which insertion crosses the three-key leaf capacity? Unchanged starter: keys 1..3. One leaf: index 0 = 1, index 1 = 2, index 2 = 3. rows=3, height=1, leaves=1.; After the instructed edit range(1,5). Nodes: 3, [1,2], [3,4]. Connections: 3 leads to [1,2] (< 3); 3 leads to [3,4] (≥ 3). rows=4, height=2, leaves=2. Separator 3 is copied into the parent and remains in the right leaf.. The second panel is the instructed edit, not the original three-insertion output. These are logical nodes, not fixed-size on-disk pages."
  },
  "tdb-range": {
    "title": "Route once, then follow neighboring leaves",
    "question": "Why can between(2,5) continue without returning to the root?",
    "kind": "graph",
    "nodes": [
      {
        "id": "root",
        "label": "[3,5]",
        "x": 50,
        "y": 14
      },
      {
        "id": "a",
        "label": "[1,2]",
        "x": 16,
        "y": 68
      },
      {
        "id": "b",
        "label": "[3,4]",
        "x": 50,
        "y": 68
      },
      {
        "id": "c",
        "label": "[5,6]",
        "x": 84,
        "y": 68
      }
    ],
    "edges": [
      {
        "from": "root",
        "to": "a",
        "label": "< 3"
      },
      {
        "from": "root",
        "to": "b",
        "label": "3..4"
      },
      {
        "from": "root",
        "to": "c",
        "label": "≥ 5"
      },
      {
        "from": "a",
        "to": "b",
        "label": "next"
      },
      {
        "from": "b",
        "to": "c",
        "label": "next"
      }
    ],
    "legend": "Start in the first leaf at key 2; follow next links and emit 2,3,4,5. Stop at key 6.",
    "height": 320,
    "note": "Both bounds are inclusive in between. The displayed nodes follow insertion of keys 1 through 6 with leaf capacity 3. Root-routing edges and leaf-next edges have different labels.",
    "description": "Why can between(2,5) continue without returning to the root? Nodes: [3,5], [1,2], [3,4], [5,6]. Connections: [3,5] leads to [1,2] (< 3); [3,5] leads to [3,4] (3..4); [3,5] leads to [5,6] (≥ 5); [1,2] leads to [3,4] (next); [3,4] leads to [5,6] (next). Start in the first leaf at key 2; follow next links and emit 2,3,4,5. Stop at key 6.. Both bounds are inclusive in between. The displayed nodes follow insertion of keys 1 through 6 with leaf capacity 3. Root-routing edges and leaf-next edges have different labels."
  },
  "tdb-statement-errors": {
    "title": "A rejected statement does not erase earlier staged work",
    "question": "Why can COMMIT still save Ada after the duplicate insert fails?",
    "kind": "table",
    "headings": [
      "Statement",
      "Candidate result",
      "Active transaction"
    ],
    "rows": [
      [
        "BEGIN",
        "Start private transaction",
        "empty"
      ],
      [
        "INSERT ID 1/Ada/42",
        "Valid candidate replaces staged state",
        "Ada retained"
      ],
      [
        "INSERT ID 1/Lin/75",
        "Duplicate: discard this candidate",
        "Ada still retained"
      ],
      [
        "COMMIT",
        "Publish staged Ada row",
        "Ada visible to SELECT"
      ]
    ],
    "label": "",
    "links": [],
    "note": "Statement failure and transaction rollback are separate decisions in this engine. The duplicate statement must not leak partial changes or silently undo an earlier successful statement.",
    "description": "Why can COMMIT still save Ada after the duplicate insert fails? Statement; Candidate result; Active transaction. BEGIN; Start private transaction; empty; INSERT ID 1/Ada/42; Valid candidate replaces staged state; Ada retained; INSERT ID 1/Lin/75; Duplicate: discard this candidate; Ada still retained; COMMIT; Publish staged Ada row; Ada visible to SELECT. . . Statement failure and transaction rollback are separate decisions in this engine. The duplicate statement must not leak partial changes or silently undo an earlier successful statement."
  },
  "dsa-graph-model": {
    "title": "Two directed routes reach D",
    "question": "Why can D be reached from both B and C?",
    "kind": "graph",
    "nodes": [
      {
        "id": "A",
        "label": "A",
        "x": 50,
        "y": 15
      },
      {
        "id": "B",
        "label": "B",
        "x": 20,
        "y": 50
      },
      {
        "id": "C",
        "label": "C",
        "x": 80,
        "y": 50
      },
      {
        "id": "D",
        "label": "D",
        "x": 50,
        "y": 85
      }
    ],
    "edges": [
      {
        "from": "A",
        "to": "B",
        "label": ""
      },
      {
        "from": "A",
        "to": "C",
        "label": ""
      },
      {
        "from": "B",
        "to": "D",
        "label": ""
      },
      {
        "from": "C",
        "to": "D",
        "label": ""
      }
    ],
    "legend": "A has neighbors B,C. B and C each point to D; D has no outgoing edges. Distance layers from A are 0: A, 1: B/C, 2: D.",
    "height": 300,
    "note": "Edges are directed in the starter. BFS records D on first discovery so the second route does not enqueue it again. The graph-model lesson only inspects the neighbors and four edges.",
    "description": "Why can D be reached from both B and C? Nodes: A, B, C, D. Connections: A leads to B; A leads to C; B leads to D; C leads to D. A has neighbors B,C. B and C each point to D; D has no outgoing edges. Distance layers from A are 0: A, 1: B/C, 2: D.. Edges are directed in the starter. BFS records D on first discovery so the second route does not enqueue it again. The graph-model lesson only inspects the neighbors and four edges."
  },
  "dsa-bfs": {
    "title": "Two directed routes reach D",
    "question": "Why can D be reached from both B and C?",
    "kind": "graph",
    "nodes": [
      {
        "id": "A",
        "label": "A",
        "x": 50,
        "y": 15
      },
      {
        "id": "B",
        "label": "B",
        "x": 20,
        "y": 50
      },
      {
        "id": "C",
        "label": "C",
        "x": 80,
        "y": 50
      },
      {
        "id": "D",
        "label": "D",
        "x": 50,
        "y": 85
      }
    ],
    "edges": [
      {
        "from": "A",
        "to": "B",
        "label": ""
      },
      {
        "from": "A",
        "to": "C",
        "label": ""
      },
      {
        "from": "B",
        "to": "D",
        "label": ""
      },
      {
        "from": "C",
        "to": "D",
        "label": ""
      }
    ],
    "legend": "A has neighbors B,C. B and C each point to D; D has no outgoing edges. Distance layers from A are 0: A, 1: B/C, 2: D.",
    "height": 300,
    "note": "Edges are directed in the starter. BFS records D on first discovery so the second route does not enqueue it again. The graph-model lesson only inspects the neighbors and four edges.",
    "description": "Why can D be reached from both B and C? Nodes: A, B, C, D. Connections: A leads to B; A leads to C; B leads to D; C leads to D. A has neighbors B,C. B and C each point to D; D has no outgoing edges. Distance layers from A are 0: A, 1: B/C, 2: D.. Edges are directed in the starter. BFS records D on first discovery so the second route does not enqueue it again. The graph-model lesson only inspects the neighbors and four edges."
  },
  "tdb-index-search": {
    "title": "Equality follows the right-hand leaf",
    "question": "Where does key 3 go when the separator is 3?",
    "kind": "graph",
    "nodes": [
      {
        "id": "root",
        "label": "3",
        "x": 50,
        "y": 18
      },
      {
        "id": "left",
        "label": "[1,2]",
        "x": 22,
        "y": 80
      },
      {
        "id": "right",
        "label": "[3,4]",
        "x": 78,
        "y": 80
      }
    ],
    "edges": [
      {
        "from": "root",
        "to": "left",
        "label": "< 3"
      },
      {
        "from": "root",
        "to": "right",
        "label": "≥ 3"
      }
    ],
    "legend": "Searching for 3 visits the root and the right leaf, then finds the row.",
    "height": 300,
    "note": "Separators repeat the first key of a right subtree. Rows remain in leaves. This is the starter’s small logical index, not a general disk-page layout.",
    "description": "Where does key 3 go when the separator is 3? Nodes: 3, [1,2], [3,4]. Connections: 3 leads to [1,2] (< 3); 3 leads to [3,4] (≥ 3). Searching for 3 visits the root and the right leaf, then finds the row.. Separators repeat the first key of a right subtree. Rows remain in leaves. This is the starter’s small logical index, not a general disk-page layout."
  }
};
