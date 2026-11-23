"""Algorithms taught through implementations, counted work and boundary cases."""

def populate(module, lesson):
    ref=[('Data structures in Python','https://docs.python.org/3/tutorial/datastructures.html')]
    module('dsa-search-sort','Algorithms: search, sorting and cost','Implement algorithms and state the assumptions behind their cost.')
    lesson('dsa-cost','Separate input size, work and extra space','Count operations for two input sizes before naming a growth class.',[
        'Big O describes a bound on growth as input size n increases. A full scan performs n visits, so its time is O(n). Comparing every distinct pair performs n(n−1)/2 comparisons, giving O(n²) time. These counts are not measured milliseconds.',
        'Auxiliary space counts additional storage beyond the input. The pair counter below keeps only counters, so it uses O(1) auxiliary space despite quadratic work. Changing n changes work; it does not add a stored list of all pairs.'
    ],'''def pair_count(n):
    count = 0
    for left in range(n):
        for right in range(left + 1, n):
            count += 1
    return count

for n in (4, 8):
    print(n, pair_count(n))''','(4, 8)','(4, 16)','4 6\n8 28\n','4 6\n16 120\n','Compare the ratio of input sizes with the ratio of comparisons. Why does doubling n not simply double pair_count?','Write pair_count(n) using loops and print pair_count(5). Do not build a list of the pairs.','def pair_count(n):\n    count = 0\n    for i in range(n):\n        for j in range(i + 1, n):\n            count += 1\n    return count\n\nprint(pair_count(5))','Five items have ten distinct unordered pairs.',refs=ref)
    lesson('dsa-linear-search','Stop a linear search when the answer is found','Distinguish the best case from the missing-item case.',[
        'Linear search inspects items in order until the target matches. The function returns the first matching index and the number of equality checks. A missing target returns None after checking the whole list.',
        'The best case takes one comparison; a missing value or a match at the end takes n comparisons. Worst-case time is O(n), and this implementation uses O(1) auxiliary space. The returned index is a position, not the matched value.'
    ],'''def find(values, target):
    checks = 0
    for index, value in enumerate(values):
        checks += 1
        if value == target:
            return index, checks
    return None, checks

print(find([4, 7, 4, 9], 4))''','], 4)','], 8)','(0, 1)\n','(None, 4)\n','Which run inspects the entire input? Why is index 0 returned when 4 appears twice?','Implement find_index(values, target), returning the first matching index or None. Print its result for [8, 3, 8] and target 3.','def find_index(values, target):\n    for index, value in enumerate(values):\n        if value == target:\n            return index\n    return None\n\nprint(find_index([8, 3, 8], 3))','Stopping at the first match preserves first-occurrence semantics.',refs=ref)
    lesson('dsa-binary-search','Halve a sorted search interval','Return the first possible matching position without skipping duplicates.',[
        'Binary search requires sorted input. The interval [low, high) contains every position still eligible for the answer; high itself is excluded. Comparing the middle value discards about half that interval.',
        'This lower_bound function returns the insertion position of the first value not less than target. Verify equality separately before claiming the target exists. Search takes O(log n) comparisons and O(1) auxiliary space; sorting an unsorted input first adds its own cost.'
    ],'''def lower_bound(values, target):
    low, high = 0, len(values)
    checks = 0
    while low < high:
        middle = (low + high) // 2
        checks += 1
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle
    return low, checks

values = [2, 4, 4, 6, 8, 10, 12, 14]
target = 4
position, checks = lower_bound(values, target)
print(position, checks)
print(position < len(values) and values[position] == target)''','target = 4','target = 5','1 4\nTrue\n','3 3\nFalse\n','Find the position and comparison count. Why does an insertion position not by itself prove that 5 is present?','Implement lower_bound(values, target) returning only the insertion index. Print the result for [1, 3, 3, 7] and target 3.','def lower_bound(values, target):\n    low, high = 0, len(values)\n    while low < high:\n        middle = (low + high) // 2\n        if values[middle] < target:\n            low = middle + 1\n        else:\n            high = middle\n    return low\n\nprint(lower_bound([1, 3, 3, 7], 3))','The first matching position is 1, including when equal values repeat.',diagram={'kind':'flow','question':'How does the eligible interval shrink for target 4?','parts':['[0, 8): middle 4 → 8','[0, 4): middle 2 → 4','[0, 2): middle 1 → 4','[0, 1): middle 0 → 2','low = high = 1']},refs=[('bisect: standard-library binary search','https://docs.python.org/3/library/bisect.html')])
    lesson('dsa-insertion-sort','Maintain a sorted prefix with insertion sort','Move greater values while preserving the order of equal values.',[
        'Insertion sort grows a sorted prefix one item at a time. Save the next key, shift larger preceding values one place right, then put the key in the gap. The key must be saved before shifting overwrites its original slot.',
        'Shifting strictly greater values keeps equal values in their original relative order: the sort is stable. Already sorted input needs O(n) comparisons; reverse order needs O(n²) shifts. The algorithm changes the list in place with O(1) auxiliary space.'
    ],'''def insertion_sort(values):
    shifts = 0
    for i in range(1, len(values)):
        key, j = values[i], i
        while j > 0 and values[j - 1] > key:
            values[j] = values[j - 1]
            j -= 1
            shifts += 1
        values[j] = key
    return shifts

values = [4, 3, 2, 1]
print("shifts", insertion_sort(values))
print(values)''','[4, 3, 2, 1]','[1, 2, 3, 4]','shifts 6\n[1, 2, 3, 4]\n','shifts 0\n[1, 2, 3, 4]\n','The final lists match. What does the shift count reveal that the final sorted output cannot?','Write an in-place insertion_sort(values) and print the sorted form of [3, -1, 3, 2].','def insertion_sort(values):\n    for i in range(1, len(values)):\n        key, j = values[i], i\n        while j > 0 and values[j - 1] > key:\n            values[j] = values[j - 1]\n            j -= 1\n        values[j] = key\n\nvalues = [3, -1, 3, 2]\ninsertion_sort(values)\nprint(values)','The duplicate remains present; the result is [-1, 2, 3, 3].',refs=[('Sorting stability','https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts')])
    lesson('dsa-merge-sort','Merge two sorted halves','Use divide and conquer while accounting for temporary storage.',[
        'Merge sort divides the list until each part contains at most one item, then merges sorted parts. During a merge, the smaller front item is the next output. Choosing the left item on equality preserves stability.',
        'There are O(log n) division levels and O(n) merging work per level, giving O(n log n) time. This list-based implementation allocates O(n) peak auxiliary storage, plus O(log n) call-stack depth. Python’s sorted is the usual application choice; this implementation exposes the mechanism.'
    ],'''def merge_sort(values):
    if len(values) < 2:
        return values[:]
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]

values = [7, 2, 5, 2]
print(merge_sort(values))
print(values)''','[7, 2, 5, 2]','[7, 2, -1, 2]','[2, 2, 5, 7]\n[7, 2, 5, 2]\n','[-1, 2, 2, 7]\n[7, 2, -1, 2]\n','Which printed list is a new result, and which shows that the input was preserved?','Merge the sorted lists [1, 4] and [2, 3] using two indexes and print the merged list. Do not call sorted.','left, right = [1, 4], [2, 3]\nresult, i, j = [], 0, 0\nwhile i < len(left) and j < len(right):\n    if left[i] <= right[j]:\n        result.append(left[i]); i += 1\n    else:\n        result.append(right[j]); j += 1\nprint(result + left[i:] + right[j:])','Each comparison consumes one input item; remaining suffixes are already sorted.',diagram={'kind':'flow','question':'Which sorted pieces combine to produce the final result?','parts':['[7, 2] and [5, 2]','Sort halves: [2, 7], [2, 5]','Merge fronts in order','[2, 2, 5, 7]']},refs=[('Sorting HOWTO','https://docs.python.org/3/howto/sorting.html')])
    lesson('dsa-two-pointers','Move two pointers toward a target sum','Use sorted order to choose which endpoint can be discarded.',[
        'For a sorted list, compare the sum at the two endpoints with a target. If the sum is too small, move the left endpoint right; every smaller left value would also be too small with the current right endpoint. If the sum is too large, move the right endpoint left.',
        'The pointers never move backward, so the scan takes O(n) time and O(1) auxiliary space after sorting. The function uses distinct positions even if equal values repeat. Applying the endpoint rule to unsorted input can miss an answer.'
    ],'''def pair_sum(values, target):
    left, right = 0, len(values) - 1
    while left < right:
        total = values[left] + values[right]
        if total == target:
            return values[left], values[right]
        if total < target:
            left += 1
        else:
            right -= 1
    return None

print(pair_sum([1, 3, 5, 8], 9))''','], 9)','], 7)','(1, 8)\n','None\n','Trace the pointer movement for target 7. Which sorted-order assumption justifies each move?','For sorted values [2, 4, 6, 9], use two pointers to find a pair summing to 10 and print the pair as a tuple.','values, target = [2, 4, 6, 9], 10\nleft, right = 0, len(values) - 1\nwhile left < right:\n    total = values[left] + values[right]\n    if total == target:\n        print((values[left], values[right])); break\n    if total < target:\n        left += 1\n    else:\n        right -= 1','After discarding 9, the endpoints 4 and 6 produce 10.',refs=ref)

    module('dsa-structures','Data structures: representation and operations','Implement links, hashing and trees; choose standard-library alternatives.')
    lesson('dsa-stack','Use a stack to match nested brackets','Choose last-in, first-out order for unfinished work.',[
        'A stack removes the most recently added item first: last in, first out, or LIFO. A Python list supports this with append and pop at its end. Opening parentheses go onto the stack; a closing parenthesis must remove one.',
        'Reject a closing parenthesis when the stack is empty, and reject leftover openings after the scan. The algorithm takes O(n) time and O(n) worst-case auxiliary space. End-appends are amortized O(1): occasional list resizing is spread across many appends.'
    ],'''def balanced(text):
    stack = []
    for char in text:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if not stack:
                return False
            stack.pop()
    return not stack

print(balanced("(()())"))''','"(()())"','"())("','True\n','False\n','The edited text has equal numbers of openings and closings. Why is counting alone insufficient?','Use a list as a stack: append "first", append "second", then print two pop results on separate lines.','stack = []\nstack.append("first")\nstack.append("second")\nprint(stack.pop())\nprint(stack.pop())','The last value added is the first removed.',refs=ref)
    lesson('dsa-queue','Keep arrival order with a deque','Use first-in, first-out order without shifting a whole list.',[
        'A queue removes the oldest pending item first: first in, first out, or FIFO. collections.deque provides append at the right and popleft at the left, each approximately O(1).',
        'A list’s pop(0) shifts the remaining items and takes O(n); repeated front-removal can therefore make a queue-based algorithm quadratic. The deque below changes its pending contents as each item is processed.'
    ],'''from collections import deque
pending = deque(["first", "second", "third"])
print(pending.popleft())
print(list(pending))''','pending.popleft()','pending.pop()','first\n[\'second\', \'third\']\n','third\n[\'first\', \'second\']\n','Which method processes the oldest item? Why does replacing popleft with pop change the scheduling rule?','Create a deque containing 2 and 4, append 6, then print each value by repeatedly using popleft.','from collections import deque\npending = deque([2, 4])\npending.append(6)\nwhile pending:\n    print(pending.popleft())','The queue preserves arrival order: 2, then 4, then 6.',refs=[('collections.deque','https://docs.python.org/3/library/collections.html#collections.deque')])
    lesson('dsa-linked-list','Follow links between nodes','Prepend a node and traverse the resulting chain.',[
        'A singly linked list stores each value in a node with a reference to the next node. head refers to the first node; None ends the chain. Prepending allocates one node whose next reference is the old head.',
        'Prepending takes O(1) time, but reaching a value by position takes O(n) traversal rather than a list’s O(1) indexing. Nodes add per-item memory overhead. Python lists and deques are usually simpler choices; this model makes links explicit for later trees.'
    ],'''from dataclasses import dataclass

@dataclass
class Node:
    value: int
    next: "Node | None" = None

head = Node(2, Node(3))
head = Node(1, head)
current = head
while current is not None:
    print(current.value)
    current = current.next''','Node(1, head)','Node(9, head)','1\n2\n3\n','9\n2\n3\n','Which link preserves access to the original two nodes after changing head?','Define a Node with value and next, connect 4 to 7, and traverse the chain to print both values.','from dataclasses import dataclass\n@dataclass\nclass Node:\n    value: int\n    next: "Node | None" = None\n\nhead = Node(4, Node(7))\nwhile head is not None:\n    print(head.value)\n    head = head.next','Following next reaches 7; None terminates traversal.',diagram={'kind':'flow','question':'Which references connect the nodes after prepending?','parts':['head → Node(1)','next → Node(2)','next → Node(3)','next → None']},refs=ref)
    lesson('dsa-hash-table','Resolve a collision in a hash table','Keep colliding keys distinct by checking equality within a bucket.',[
        'A hash table maps a key to a bucket, then compares keys within that bucket. This teaching implementation uses key % 4 for integer keys and a list of pairs per bucket. Keys 1 and 5 collide but remain separate records.',
        'With a well-distributed hash and controlled load, a lookup is expected O(1). A bucket containing every key gives O(n) worst-case lookup. The example exposes collision handling; Python’s dict has a different implementation and also resizes to control occupancy.'
    ],'''buckets = [[] for _ in range(4)]
def put(key, value):
    bucket = buckets[key % len(buckets)]
    for index, (existing, _) in enumerate(bucket):
        if existing == key:
            bucket[index] = (key, value)
            return
    bucket.append((key, value))

put(1, "Ada")
put(5, "Lin")
put(1, "Grace")
print(buckets[1])''','put(1, "Grace")','put(9, "Grace")',"[(1, 'Grace'), (5, 'Lin')]\n","[(1, 'Ada'), (5, 'Lin'), (9, 'Grace')]\n",'Why does the starter replace one pair while the edit adds a third pair to the same bucket?','Using buckets [[(0, "zero")], [(1, "one"), (5, "five")]], scan bucket key % 2 to find key 5 and print its value.','buckets = [[(0, "zero")], [(1, "one"), (5, "five")]]\nkey = 5\nfor stored, value in buckets[key % len(buckets)]:\n    if stored == key:\n        print(value)\n        break','The bucket narrows the search, but equality decides which colliding pair matches.',refs=[('Mapping types: dict','https://docs.python.org/3/library/stdtypes.html#mapping-types-dict')])
    lesson('dsa-heap','Retrieve the smallest priority from a heap','Distinguish a heap invariant from a fully sorted list.',[
        'A min-heap keeps the smallest item at index zero. Each parent is no greater than its children; the remaining array is not guaranteed to be sorted. heapq.heappush and heappop repair that invariant in O(log n) time.',
        'The tuple (priority, sequence, label) orders tasks first by priority and then arrival sequence. The explicit sequence gives equal-priority tasks a stable order without comparing their payloads. Building a heap with heapify takes O(n) time.'
    ],'''import heapq
pending = [(2, 0, "write"), (1, 1, "read"), (2, 2, "close")]
heapq.heapify(pending)
heapq.heappush(pending, (0, 3, "recover"))
while pending:
    print(heapq.heappop(pending)[2])''','(0, 3, "recover")','(3, 3, "recover")','recover\nread\nwrite\nclose\n','read\nwrite\nclose\nrecover\n','Which field breaks the tie between write and close? Does changing one priority change their relative order?','Build a heap from [7, 2, 5], then pop and print all three values in priority order.','import heapq\nvalues = [7, 2, 5]\nheapq.heapify(values)\nwhile values:\n    print(heapq.heappop(values))','The heap supplies 2, 5 and 7 without initially sorting the whole list.',refs=[('heapq','https://docs.python.org/3/library/heapq.html')])
    lesson('dsa-bst','Compare a search tree’s order with its height','Insert unique keys and observe why an unbalanced tree can become a chain.',[
        'A binary search tree places smaller keys in the left subtree and larger keys in the right. Searching or inserting follows one path, taking O(h) time where h is the tree’s height.',
        'Sorted insertion can make this unbalanced tree a chain of n nodes. Balanced insertion order can produce logarithmic height, but this implementation does not rebalance itself. In-order traversal visits left, node and right to recover sorted keys in either shape.'
    ],'''from dataclasses import dataclass
@dataclass
class Node:
    key: int
    left: "Node | None" = None
    right: "Node | None" = None

def insert(node, key):
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    return node

def height(node):
    return 0 if node is None else 1 + max(height(node.left), height(node.right))

def ordered(node):
    return [] if node is None else ordered(node.left) + [node.key] + ordered(node.right)

root = None
for key in [2, 1, 3]:
    root = insert(root, key)
print(ordered(root))
print("height", height(root))''','[2, 1, 3]','[1, 2, 3]','[1, 2, 3]\nheight 2\n','[1, 2, 3]\nheight 3\n','The sorted output is unchanged. Which output exposes the extra work a later search can require?','Given tree = (2, (1, None, None), (3, None, None)), write inorder(node) returning its sorted keys. Print the result.','def inorder(node):\n    if node is None:\n        return []\n    key, left, right = node\n    return inorder(left) + [key] + inorder(right)\n\ntree = (2, (1, None, None), (3, None, None))\nprint(inorder(tree))','Tree shape controls path length, while the ordering rule controls traversal order.',refs=ref)

    module('dsa-graphs','Graphs, paths and dynamic programming','Choose traversal order, enforce preconditions and reuse solved subproblems.')
    graph={'kind':'graph','question':'Which routes connect A to D?','nodes':[['A',90,65],['B',320,65],['C',90,205],['D',320,205]],'edges':[['A','B'],['A','C'],['B','D'],['C','D']]}
    lesson('dsa-graph-model','Represent vertices and edges explicitly','Distinguish a vertex’s neighbors from every reachable vertex.',[
        'A graph models vertices, such as places, connected by edges, such as routes. An adjacency list maps each vertex to its immediate neighbors. For an undirected edge, both endpoint lists include the other endpoint.',
        'The graph below is directed: A lists B and C, but B does not list A. A missing reverse edge therefore changes which routes can be followed. Storing adjacency lists takes O(V + E) space for V vertices and E directed entries.'
    ],'''graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
start = "A"
print(graph[start])
print(sum(len(neighbors) for neighbors in graph.values()))''','start = "A"','start = "B"',"['B', 'C']\n4\n","['D']\n4\n",'Which result depends on the chosen start vertex? Why does the edge count remain four?','Represent an undirected path A—B—C using adjacency lists. Print B’s neighbors as ["A", "C"].','graph = {"A": ["B"], "B": ["A", "C"], "C": ["B"]}\nprint(graph["B"])','Each undirected edge appears in the lists of both endpoints.',diagram=graph,refs=ref)
    lesson('dsa-bfs','Find shortest unweighted paths with a queue','Record discovery before enqueueing so cycles do not repeat work.',[
        'Breadth-first search, or BFS, explores vertices in increasing edge distance from a start. A deque processes the oldest discovery first. Set a neighbor’s distance when it is enqueued, so later edges cannot enqueue it again.',
        'For equal-cost edges, the first discovered distance is shortest. BFS takes O(V + E) time and O(V) auxiliary space. Weighted edges require a different algorithm; the distance here is a number of edges, not kilometers or travel time.'
    ],'''from collections import deque

def distances(graph, start):
    distance = {start: 0}
    pending = deque([start])
    while pending:
        node = pending.popleft()
        for neighbor in graph[node]:
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                pending.append(neighbor)
    return distance

graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
print(distances(graph, "A"))''','distances(graph, "A")','distances(graph, "B")',"{'A': 0, 'B': 1, 'C': 1, 'D': 2}\n","{'B': 0, 'D': 1}\n",'Why is D’s distance two from A but one from B? Why are unreachable vertices absent?','Use BFS to compute distances from 0 in graph = {0: [1], 1: [0, 2], 2: [1]}. Print the resulting dictionary.','from collections import deque\ngraph = {0: [1], 1: [0, 2], 2: [1]}\ndistance = {0: 0}\npending = deque([0])\nwhile pending:\n    node = pending.popleft()\n    for neighbor in graph[node]:\n        if neighbor not in distance:\n            distance[neighbor] = distance[node] + 1\n            pending.append(neighbor)\nprint(distance)','Marking 0 as discovered before scanning 1 prevents a cycle back to the start.',diagram=graph,refs=[('collections.deque','https://docs.python.org/3/library/collections.html#collections.deque')])
    lesson('dsa-dfs','Explore a graph with an explicit stack','Keep a visited set so cycles cannot cause an endless traversal.',[
        'Depth-first search, or DFS, follows one pending branch before returning to alternatives. An explicit list stack replaces recursive function calls. A visited set prevents a cycle from repeatedly processing the same vertex.',
        'The reversed neighbor list makes the first listed neighbor the next one popped. Traversal order depends on that scheduling choice. DFS reachability takes O(V + E) time; it does not guarantee the shortest unweighted path that BFS supplies.'
    ],'''def visit(graph, start):
    pending, seen, order = [start], set(), []
    while pending:
        node = pending.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        pending.extend(reversed(graph[node]))
    return order

graph = {"A": ["B", "C"], "B": ["A", "D"], "C": [], "D": []}
print(visit(graph, "A"))''','reversed(graph[node])','graph[node]',"['A', 'B', 'D', 'C']\n","['A', 'C', 'B', 'D']\n",'Both runs reach the same vertices. Why does stack insertion change their printed order?','Use a stack and a seen set to visit graph = {0: [1], 1: [0]} starting at 0. Print the visit order.','graph = {0: [1], 1: [0]}\npending, seen, order = [0], set(), []\nwhile pending:\n    node = pending.pop()\n    if node in seen:\n        continue\n    seen.add(node)\n    order.append(node)\n    pending.extend(graph[node])\nprint(order)','The seen set stops the two-way edge from revisiting 0 forever.',refs=ref)
    lesson('dsa-topological','Schedule tasks only after their dependencies','Detect a dependency cycle instead of returning an incomplete schedule.',[
        'A topological ordering puts each directed edge’s source before its destination. It exists only for a directed acyclic graph: a graph with no directed cycle. Indegree counts how many incoming dependencies each task still has.',
        'Start a queue with zero-indegree tasks. Removing a task decreases its neighbors’ indegrees; enqueue a neighbor when its count reaches zero. If fewer than V tasks are removed, a cycle blocks the remaining tasks. The algorithm takes O(V + E) time.'
    ],'''from collections import deque

def schedule(graph):
    indegree = dict.fromkeys(graph, 0)
    for neighbors in graph.values():
        for neighbor in neighbors:
            indegree[neighbor] += 1
    pending = deque(node for node, count in indegree.items() if count == 0)
    order = []
    while pending:
        node = pending.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                pending.append(neighbor)
    return order if len(order) == len(graph) else "cycle"

graph = {"read": ["transform"], "transform": ["write"], "write": []}
print(schedule(graph))''','"write": []','"write": ["read"]',"['read', 'transform', 'write']\n",'cycle\n','Which new edge closes the cycle? Why can no task in that cycle satisfy its prerequisites first?','For tasks ["read", "transform", "write"], print them in an order that keeps read before transform and transform before write. Then print whether that order contains all three distinct tasks.','order = ["read", "transform", "write"]\nprint(order)\nprint(len(order) == 3 and len(set(order)) == 3)','The ordering must satisfy every dependency, not just include the task names.',refs=[('graphlib.TopologicalSorter','https://docs.python.org/3/library/graphlib.html')])
    lesson('dsa-dijkstra','Find minimum total weight with a priority queue','Use nonnegative edge weights and discard stale heap entries.',[
        'Dijkstra’s algorithm chooses the smallest pending total distance from a min-heap. Relaxing an edge means replacing a neighbor’s distance when the new route has a smaller total weight.',
        'All edge weights must be nonnegative; reject negative weights before searching. A vertex may have older heap entries after an improvement, so skip an entry whose distance no longer matches the best known value. This heap-based implementation takes O((V + E) log V) time for a simple graph.'
    ],'''import heapq

def shortest(graph, start):
    if any(weight < 0 for edges in graph.values() for _, weight in edges):
        raise ValueError("weights must be nonnegative")
    distance, pending = {start: 0}, [(0, start)]
    while pending:
        cost, node = heapq.heappop(pending)
        if cost != distance[node]:
            continue
        for neighbor, weight in graph[node]:
            candidate = cost + weight
            if candidate < distance.get(neighbor, float("inf")):
                distance[neighbor] = candidate
                heapq.heappush(pending, (candidate, neighbor))
    return distance

graph = {"A": [("B", 5), ("C", 1)], "B": [], "C": [("B", 2)]}
print(shortest(graph, "A"))''','("C", 1)','("C", 4)',"{'A': 0, 'B': 3, 'C': 1}\n","{'A': 0, 'B': 5, 'C': 4}\n",'Which route reaches B more cheaply in each run? Why is fewest edges not the question this algorithm answers?','Use heapq to process route candidates [(5, "B"), (1, "C"), (3, "B")] in increasing cost order and print each tuple.','import heapq\npending = [(5, "B"), (1, "C"), (3, "B")]\nheapq.heapify(pending)\nwhile pending:\n    print(heapq.heappop(pending))','The improved cost 3 is processed before the stale cost 5; the algorithm must still identify stale entries.',refs=[('heapq','https://docs.python.org/3/library/heapq.html')])
    lesson('dsa-dynamic-programming','Reuse smaller solutions in a dynamic program','Find a minimum coin count where choosing the largest coin first fails.',[
        'Dynamic programming stores answers to overlapping subproblems. For each amount, best[amount] is one plus the smallest already solved count for amount minus an available coin. best[0] = 0 is the base case.',
        'With coins [1, 3, 4], greedily taking 4 for amount 6 leaves two ones, while two threes use fewer coins. The table method checks all allowed final coins. Coins must be positive integers and target must be a nonnegative integer. For target A and C denominations, this implementation takes O(A × C) time and O(A) space.'
    ],'''def minimum_coins(coins, target):
    best = [0] + [float("inf")] * target
    for amount in range(1, target + 1):
        for coin in coins:
            if coin <= amount:
                best[amount] = min(best[amount], 1 + best[amount - coin])
    return best[target]

print(minimum_coins([1, 3, 4], 6))''','[1, 3, 4], 6','[1, 4], 6','2\n','3\n','Which two coins explain the starter’s result? Why does removing denomination 3 change the optimum?','Compute a best table for coins [1, 3] and target 5, then print best[5].','coins, target = [1, 3], 5\nbest = [0] + [float("inf")] * target\nfor amount in range(1, target + 1):\n    for coin in coins:\n        if coin <= amount:\n            best[amount] = min(best[amount], 1 + best[amount - coin])\nprint(best[target])','One three and two ones give the minimum count of three. Positive integer coins and a nonnegative integer target are assumed.',refs=ref)
