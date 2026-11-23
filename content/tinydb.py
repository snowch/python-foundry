"""Python Foundry TinyDB: checked snapshots, a B+ index and redo recovery.

This educational engine is independent of sqlite3. Logical B+ nodes live in
memory; the disk format stores rows and rebuilds that index when opened.
"""
from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
import csv
import hashlib
import json
from pathlib import Path
import re

MAX_ROWS = 4096

@dataclass(frozen=True)
class Row:
    id: int
    name: str
    score: int
    def __post_init__(self):
        if type(self.id) is not int or not 0 <= self.id <= 2**31 - 1:
            raise ValueError('id must be an integer from 0 to 2147483647')
        if not isinstance(self.name, str) or not 1 <= len(self.name.encode('utf-8')) <= 32:
            raise ValueError('name must contain 1 to 32 UTF-8 bytes')
        if type(self.score) is not int or not 0 <= self.score <= 100:
            raise ValueError('score must be an integer from 0 to 100')
    def data(self):
        return {'id': self.id, 'name': self.name, 'score': self.score}

@dataclass
class Node:
    leaf: bool = True
    keys: list = field(default_factory=list)
    values: list = field(default_factory=list)
    children: list = field(default_factory=list)
    next: 'Node | None' = None

class BPlusTree:
    """At most three keys per node; separators repeat a right subtree minimum."""
    def __init__(self):
        self.root = Node()
        self.visits = 0
    def insert(self, row):
        split = self._insert(self.root, row)
        if split:
            separator, right = split
            self.root = Node(False, [separator], children=[self.root, right])
    def _insert(self, node, row):
        if node.leaf:
            position = bisect_left(node.keys, row.id)
            if position < len(node.keys) and node.keys[position] == row.id:
                raise ValueError('duplicate id')
            node.keys.insert(position, row.id)
            node.values.insert(position, row)
            if len(node.keys) <= 3:
                return None
            middle = len(node.keys) // 2
            right = Node(True, node.keys[middle:], node.values[middle:], next=node.next)
            node.keys, node.values, node.next = node.keys[:middle], node.values[:middle], right
            return right.keys[0], right
        position = bisect_right(node.keys, row.id)
        split = self._insert(node.children[position], row)
        if split:
            separator, right = split
            node.keys.insert(position, separator)
            node.children.insert(position + 1, right)
        if len(node.keys) <= 3:
            return None
        middle = len(node.keys) // 2
        separator = node.keys[middle]
        right = Node(False, node.keys[middle + 1:], children=node.children[middle + 1:])
        node.keys, node.children = node.keys[:middle], node.children[:middle + 1]
        return separator, right
    def _leaf(self, key):
        node, self.visits = self.root, 1
        while not node.leaf:
            node = node.children[bisect_right(node.keys, key)]
            self.visits += 1
        return node
    def get(self, key):
        leaf = self._leaf(key)
        position = bisect_left(leaf.keys, key)
        return leaf.values[position] if position < len(leaf.keys) and leaf.keys[position] == key else None
    def between(self, low=0, high=2**31 - 1):
        if low > high:
            return []
        leaf, result = self._leaf(low), []
        position = bisect_left(leaf.keys, low)
        while leaf is not None:
            for row in leaf.values[position:]:
                if row.id > high:
                    return result
                result.append(row)
            leaf, position = leaf.next, 0
            if leaf is not None:
                self.visits += 1
        return result
    def check(self):
        leaves, seen = [], set()
        def walk(node, depth):
            if id(node) in seen:
                raise ValueError('cycle or repeated child in index')
            seen.add(id(node))
            if node.keys != sorted(set(node.keys)) or len(node.keys) > 3:
                raise ValueError('invalid key order or capacity')
            if node.leaf:
                if node.children or node.keys != [row.id for row in node.values]:
                    raise ValueError('leaf keys and rows disagree')
                if node is not self.root and len(node.keys) < 2:
                    raise ValueError('underfilled non-root leaf')
                leaves.append(node)
                return node.keys, depth
            if node.values or len(node.children) != len(node.keys) + 1 or not node.keys:
                raise ValueError('invalid branch shape')
            parts = [walk(child, depth + 1) for child in node.children]
            if len({height for _, height in parts}) != 1:
                raise ValueError('leaves have unequal depths')
            if node.keys != [keys[0] for keys, _ in parts[1:]]:
                raise ValueError('separator is not a right subtree minimum')
            keys = [key for part, _ in parts for key in part]
            if keys != sorted(set(keys)):
                raise ValueError('overlapping child ranges')
            return keys, parts[0][1]
        keys, height = walk(self.root, 1)
        for position, leaf in enumerate(leaves):
            if leaf.next is not (leaves[position + 1] if position + 1 < len(leaves) else None):
                raise ValueError('invalid leaf link')
        return {'rows': len(keys), 'height': height, 'leaves': len(leaves)}

def index_for(rows):
    tree = BPlusTree()
    for key in sorted(rows):
        tree.insert(rows[key])
    tree.check()
    return tree

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def pack(rows, generation):
    payload = {'format': 'PYFDB1', 'generation': generation, 'rows': [rows[key].data() for key in sorted(rows)]}
    return canonical({'payload': payload, 'sha256': hashlib.sha256(canonical(payload)).hexdigest()})

def unpack(data):
    try:
        envelope = json.loads(data)
        if set(envelope) != {'payload', 'sha256'}:
            raise ValueError('invalid snapshot envelope')
        payload = envelope['payload']
        if hashlib.sha256(canonical(payload)).hexdigest() != envelope['sha256']:
            raise ValueError('snapshot checksum mismatch')
        if set(payload) != {'format', 'generation', 'rows'} or payload['format'] != 'PYFDB1':
            raise ValueError('unsupported snapshot format')
        generation = payload['generation']
        if type(generation) is not int or generation < 0 or not isinstance(payload['rows'], list) or len(payload['rows']) > MAX_ROWS:
            raise ValueError('invalid generation or row count')
        records = [Row(**row) for row in payload['rows']]
        keys = [row.id for row in records]
        if keys != sorted(set(keys)):
            raise ValueError('snapshot ids must be unique and sorted')
        return {row.id: row for row in records}, generation
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError('invalid snapshot structure') from error

class SimulatedCrash(RuntimeError):
    pass

class Database:
    def __init__(self, filename='people.pfdb'):
        self.path = Path(filename)
        self.journal = Path(filename + '.journal')
        self.staged = None
        self.crash_at = None
        self.recovered = self._recover()
        self.rows, self.generation = unpack(self.path.read_bytes()) if self.path.exists() else ({}, 0)
        self.index = index_for(self.rows)
    def _install(self, data):
        temporary = self.path.with_name(self.path.name + '.tmp')
        temporary.write_bytes(data)
        temporary.replace(self.path)
    def _recover(self):
        if not self.journal.exists():
            return 'none'
        try:
            record = json.loads(self.journal.read_bytes())
            if set(record) != {'phase', 'base', 'after'} or record['phase'] not in ('prepared', 'committed') or type(record['base']) is not int:
                raise ValueError('invalid journal structure')
            data = canonical(record['after'])
            _, target = unpack(data)
            if target != record['base'] + 1:
                raise ValueError('journal generation mismatch')
            try:
                current_rows, current = unpack(self.path.read_bytes()) if self.path.exists() else ({}, 0)
            except ValueError:
                if record['phase'] != 'committed':
                    raise
                current = record['base']
            if current not in (record['base'], target):
                raise ValueError('journal does not match the current database')
            if current == target and self.path.read_bytes() != data:
                raise ValueError('journal conflicts with installed generation')
            if record['phase'] == 'prepared':
                if current != record['base']:
                    raise ValueError('prepared journal cannot replace installed data')
                action = 'discarded prepared journal'
            else:
                self._install(data)
                action = 'replayed committed journal'
            self.journal.unlink()
            return action
        except (KeyError, TypeError, json.JSONDecodeError) as error:
            raise ValueError('invalid recovery journal') from error
    def _publish(self, candidate):
        index = index_for(candidate)
        data = pack(candidate, self.generation + 1)
        record = {'phase': 'prepared', 'base': self.generation, 'after': json.loads(data)}
        self.journal.write_bytes(canonical(record))
        self._crash('prepare')
        record['phase'] = 'committed'
        self.journal.write_bytes(canonical(record))
        self._crash('commit')
        self._install(data)
        self._crash('install')
        self.journal.unlink()
        self.rows, self.index = candidate, index
        self.generation += 1
    def _crash(self, phase):
        if self.crash_at == phase:
            self.crash_at = None
            raise SimulatedCrash('simulated crash after ' + phase)
    def begin(self):
        if self.staged is not None:
            raise ValueError('transaction already active')
        self.staged = dict(self.rows)
    def commit(self):
        if self.staged is None:
            raise ValueError('no active transaction')
        self._publish(dict(self.staged))
        self.staged = None
    def rollback(self):
        if self.staged is None:
            raise ValueError('no active transaction')
        self.staged = None
    def _change(self, operation):
        candidate = dict(self.rows if self.staged is None else self.staged)
        operation(candidate)
        if len(candidate) > MAX_ROWS:
            raise ValueError('row limit reached: 4096')
        if self.staged is not None:
            self.staged = candidate
        else:
            self._publish(candidate)
    def insert(self, row):
        def add(rows):
            if row.id in rows:
                raise ValueError('duplicate id')
            rows[row.id] = row
        self._change(add)
    def delete(self, key):
        def remove(rows):
            if key not in rows:
                raise ValueError('id not found')
            del rows[key]
        self._change(remove)
    def update(self, key, score):
        def replace(rows):
            if key not in rows:
                raise ValueError('id not found')
            row = rows[key]
            rows[key] = Row(row.id, row.name, score)
        self._change(replace)
    def select(self, low=0, high=2**31 - 1):
        index = self.index if self.staged is None else index_for(self.staged)
        return index.between(low, high)
    def check(self):
        index = self.index if self.staged is None else index_for(self.staged)
        report = index.check()
        if [row.id for row in index.between()] != sorted(self.rows if self.staged is None else self.staged):
            raise ValueError('index and stored rows disagree')
        return report

HELP = '''INSERT INTO people VALUES (1, 'Ada', 42);
SELECT * FROM people;
SELECT * FROM people WHERE id = 1;
SELECT * FROM people WHERE id >= 1 AND id <= 9;
UPDATE people SET score = 73 WHERE id = 1;
DELETE FROM people WHERE id = 1;
BEGIN; COMMIT; ROLLBACK;
.schema .stats .check .dump
.snapshot backup.pfdb
.export rows.json
.crash prepare|commit|install'''

def execute_statement(db, statement):
    statement = statement.strip().rstrip(';').strip()
    if not statement or statement.startswith('--'):
        return
    upper = statement.upper()
    if upper in ('BEGIN', 'COMMIT', 'ROLLBACK'):
        getattr(db, upper.lower())()
        print(upper.lower() + ' ok')
        return
    if statement == '.help':
        print(HELP); return
    if statement == '.schema':
        print('people(id INTEGER PRIMARY KEY, name TEXT 1..32 UTF-8 bytes, score INTEGER 0..100)'); return
    if statement == '.stats':
        report = db.check()
        print(f"generation {db.generation} rows {report['rows']} height {report['height']} leaves {report['leaves']}")
        print('transaction ' + ('active' if db.staged is not None else 'none')); return
    if statement == '.check':
        print('check ok', db.check()); return
    if statement == '.dump':
        print(json.dumps([row.data() for row in db.select()], ensure_ascii=False)); return
    match = re.fullmatch(r'\.(snapshot|export) ([A-Za-z0-9_-]+\.(?:pfdb|json))', statement)
    if match:
        kind, filename = match.groups()
        if filename in (str(db.path), str(db.journal)):
            raise ValueError('choose a different output filename')
        if kind == 'snapshot':
            Path(filename).write_bytes(pack(db.rows, db.generation))
        else:
            Path(filename).write_text(json.dumps([row.data() for row in db.select()], ensure_ascii=False), encoding='utf-8')
        print('saved', filename); return
    match = re.fullmatch(r'\.crash (prepare|commit|install)', statement)
    if match:
        db.crash_at = match[1]; print('next commit will stop after', match[1]); return
    match = re.fullmatch(r'INSERT INTO people VALUES\s*\((.*)\)', statement, re.I)
    if match:
        fields = next(csv.reader([match[1]], quotechar="'", skipinitialspace=True, strict=True))
        if len(fields) != 3:
            raise ValueError('INSERT needs id, name and score')
        db.insert(Row(int(fields[0]), fields[1], int(fields[2])))
        print('insert ok'); return
    match = re.fullmatch(r'UPDATE people SET score\s*=\s*(\d+) WHERE id\s*=\s*(\d+)', statement, re.I)
    if match:
        db.update(int(match[2]), int(match[1])); print('update ok'); return
    match = re.fullmatch(r'DELETE FROM people WHERE id\s*=\s*(\d+)', statement, re.I)
    if match:
        db.delete(int(match[1])); print('delete ok'); return
    match = re.fullmatch(r'SELECT \* FROM people(?: WHERE id\s*=\s*(\d+)| WHERE id\s*>=\s*(\d+) AND id\s*<=\s*(\d+))?', statement, re.I)
    if match:
        equal, low, high = match.groups()
        rows = db.select(int(equal), int(equal)) if equal else db.select(int(low), int(high)) if low else db.select()
        for row in rows:
            print(f'{row.id} | {row.name} | {row.score}')
        print(f'({len(rows)} rows)'); return
    raise ValueError('statement not supported; use .help for the exact grammar')

def run_script(script, filename='people.pfdb'):
    """One complete statement per line; an unfinished transaction rolls back."""
    db = Database(filename)
    if db.recovered != 'none':
        print('recovery:', db.recovered)
    for number, statement in enumerate(script.splitlines(), 1):
        try:
            execute_statement(db, statement)
        except SimulatedCrash as error:
            print(str(error)); return
        except (ValueError, csv.Error) as error:
            print(f'line {number}: {error}')
    if db.staged is not None:
        db.rollback()
        print('uncommitted transaction rolled back at end of script')
