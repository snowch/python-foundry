"""Progressive TinyDB projects use the same Python engine as the saved workspace."""
from pathlib import Path
ENGINE = Path(__file__).with_name('tinydb.py').read_text(encoding='utf-8')

def populate(module, lesson):
    references=[('bisect and ordered indexes','https://docs.python.org/3/library/bisect.html'),('dataclasses','https://docs.python.org/3/library/dataclasses.html'),('JSON encoding','https://docs.python.org/3/library/json.html')]
    def lab(id,title,goal,explain,source,before,after,expected,changed,observe,practice,solution,answer,**options):
        item=lesson(id,title,goal,explain,source,before,after,expected,changed,observe,'The practice program also has the supplied tinydb.py module. '+practice,solution,answer,files={'main.py':source.strip()+'\n','tinydb.py':ENGINE},refs=references,**options)
        item['practiceFiles']['tinydb.py']=ENGINE
        item['solutionFiles']['tinydb.py']=ENGINE
        return item
    module('tinydb-index','TinyDB: rows, encoding and a B+ index','Connect earlier structures to a small database implemented in Python.')
    lab('tdb-schema','TinyDB: define and validate a row','Reject an invalid row before it can change stored data.',[
        'TinyDB stores one table, people, with id, name and score fields. A schema defines which values are allowed: a unique integer id from 0 to 2147483647, a name occupying 1 to 32 UTF-8 bytes, and an integer score from 0 to 100. The supplied Row dataclass validates field types and bounds when constructed. Database insertion separately rejects duplicate ids.',
        'This engine is Python code, not a wrapper around SQLite or the third-party package named TinyDB. Every source tab is editable. The standalone examples start with fresh files; the final Saved TinyDB workspace explicitly retains database files between runs.'
    ],'''from tinydb import Row
try:
    row = Row(1, "Ada", 42)
    print(row.data())
except ValueError as error:
    print(error)''','Row(1, "Ada", 42)','Row(1, "Ada", 142)',"{'id': 1, 'name': 'Ada', 'score': 42}\n",'score must be an integer from 0 to 100\n','Which constructor rule prevents 142 from becoming a stored score? A Python object existing in memory is not yet a committed database record.','Construct Row(7, "Lin", 90) and print its id and score on one line.','from tinydb import Row\nrow = Row(7, "Lin", 90)\nprint(row.id, row.score)','Schema checks happen before insertion.')
    lab('tdb-statements','TinyDB: parse a bounded statement language','Distinguish parsing a command from applying its storage operation.',[
        'run_script accepts one complete statement per line. The supported SQL subset includes INSERT, SELECT by id or id range, UPDATE score, DELETE, BEGIN, COMMIT and ROLLBACK. Dot commands provide inspection; .help lists the exact grammar. This is a deliberately bounded language, not all of SQL.',
        'The parser converts the three INSERT fields into a validated Row, then calls the database operation. A statement error prints its line number and allows later statements to run. It does not cancel earlier successful commits or automatically roll back an active transaction.'
    ],'''from tinydb import run_script
run_script("""INSERT INTO people VALUES (1, 'Ada', 42);
SELECT * FROM people WHERE id = 1;
""")''','WHERE id = 1','WHERE id = 2','insert ok\n1 | Ada | 42\n(1 rows)\n','insert ok\n(0 rows)\n','Did the edit change the inserted row or only the selection condition?','Run a two-line script inserting id 2, name Lin, score 75, then SELECT * FROM people.','from tinydb import run_script\nrun_script("INSERT INTO people VALUES (2, \'Lin\', 75);\\nSELECT * FROM people;")','The selection reads the row accepted by the insert.')
    lab('tdb-codec','TinyDB: encode rows and verify a checksum','Separate file integrity checking from user authentication.',[
        'A snapshot contains a PYFDB1 format marker, generation number, sorted rows and SHA-256 checksum. canonical converts values to a deterministic UTF-8 JSON representation; unpack recomputes the checksum before accepting row values and ordering.',
        'The checksum detects accidental byte changes. It does not authenticate a file: someone able to replace both payload and checksum can create another valid snapshot. Keep row validation and format checks even when the checksum matches.'
    ],'''from tinydb import Row, pack, unpack
rows = {1: Row(1, "Ada", 42)}
data = pack(rows, 3)
data = data.replace(b'"score":42', b'"score":42')
try:
    reopened, generation = unpack(data)
    print(generation, reopened[1].name)
except ValueError as error:
    print(error)''',"b'\"score\":42', b'\"score\":42'","b'\"score\":42', b'\"score\":43'",'3 Ada\n','snapshot checksum mismatch\n','Why can changing a valid numeric score still make the snapshot unreadable?','Pack {2: Row(2, "Lin", 75)} at generation 1, unpack it, then print the generation and recovered score.','from tinydb import Row, pack, unpack\nrows, generation = unpack(pack({2: Row(2, "Lin", 75)}, 1))\nprint(generation, rows[2].score)','Round-trip decoding checks both the representation and schema.',diagram={'kind':'flow','question':'Which checks stand between bytes and accepted rows?','parts':['UTF-8 JSON bytes','Envelope and SHA-256','Format, generation and row rules','Unique sorted rows']})
    lab('tdb-index-search','TinyDB: route a lookup through B+ separators','Send a separator-equal key into its right subtree.',[
        'A B+ tree stores rows only in leaves. Branch keys are separators: each repeats the smallest key in its right subtree. bisect_right chooses the child for a lookup, so a key equal to a separator follows that right subtree.',
        'With at most three keys per node, a small example already has a branch and two leaves. get returns a Row or None. visits counts nodes inspected by the last lookup, not file reads; the index is in memory and is rebuilt when the database opens.'
    ],'''from tinydb import BPlusTree, Row
index = BPlusTree()
for key in [1, 2, 3, 4]:
    index.insert(Row(key, f"person{key}", 50))
row = index.get(3)
print(row.id if row else None)
print("nodes", index.visits)''','index.get(3)','index.get(9)','3\nnodes 2\n','None\nnodes 2\n','Both lookups visit two nodes. Why does that count not establish whether a row was found?','Build a BPlusTree with rows 2 and 5, then print whether get(5) returns a row and get(9) returns None.','from tinydb import BPlusTree, Row\nindex = BPlusTree()\nfor key in [2, 5]:\n    index.insert(Row(key, "person", 50))\nprint(index.get(5) is not None)\nprint(index.get(9) is None)','A missing lookup is an ordinary result, not a storage error.',diagram={'kind':'index','question':'Where does key 3 go when the branch separator is 3?','nodes':[['separator 3',210,45],['leaf [1, 2]',90,175],['leaf [3, 4]',330,175]],'edges':[['separator 3','leaf [1, 2]'],['separator 3','leaf [3, 4]']]})
    lab('tdb-index-split','TinyDB: split an overflowing leaf','Copy the right leaf’s first key into a new branch.',[
        'Inserting a fourth key overflows a three-key leaf. Split the four sorted rows into two leaves and copy the first right key into a parent separator. The separator remains in the right leaf because rows live in leaves, not branches.',
        'A split root creates a new level. A split child can overflow its parent, causing another split upward. check validates capacity, order, child ranges, equal leaf depth and the leaf chain. These are logical nodes, not fixed-size disk pages.'
    ],'''from tinydb import BPlusTree, Row
index = BPlusTree()
for key in range(1, 4):
    index.insert(Row(key, "person", 50))
print(index.check())''','range(1, 4)','range(1, 5)',"{'rows': 3, 'height': 1, 'leaves': 1}\n","{'rows': 4, 'height': 2, 'leaves': 2}\n",'Which insertion crosses the capacity threshold? Compare height and leaves rather than only the row count.','Insert ids 1 through 8 into a BPlusTree, call check, then print the ids returned by between(3, 6).','from tinydb import BPlusTree, Row\nindex = BPlusTree()\nfor key in range(1, 9):\n    index.insert(Row(key, "person", 50))\nindex.check()\nprint([row.id for row in index.between(3, 6)])','Repeated splits preserve ordered range lookup.')
    lab('tdb-range','TinyDB: continue a range scan across leaves','Find the first eligible leaf, then follow its next links.',[
        'A range scan first descends to the leaf containing the lower bound. It then follows next links across neighboring leaves until a key exceeds the upper bound. Both bounds are inclusive in between(low, high).',
        'The index locates the beginning in O(log n) time and visits the matching rows sequentially, giving O(log n + k) work for k results in a bounded-capacity tree. That describes index operations, not disk I/O or elapsed time.'
    ],'''from tinydb import BPlusTree, Row
index = BPlusTree()
for key in range(1, 7):
    index.insert(Row(key, "person", 50))
print([row.id for row in index.between(2, 5)])
print("nodes", index.visits)''','between(2, 5)','between(3, 3)','[2, 3, 4, 5]\nnodes 4\n','[3]\nnodes 2\n','Which run follows leaf links? Why can a narrow range need fewer node visits?','Insert ids 1 through 5 into a BPlusTree, then print all ids returned by between(2, 4).','from tinydb import BPlusTree, Row\nindex = BPlusTree()\nfor key in range(1, 6):\n    index.insert(Row(key, "person", 50))\nprint([row.id for row in index.between(2, 4)])','The endpoints 2 and 4 are both included.')

    module('tinydb-storage','TinyDB: persistence, transactions and recovery','Save a complete database, stage changes and test recovery boundaries.')
    lab('tdb-snapshots','TinyDB: reopen a checksummed snapshot','Distinguish persisted rows from an index reconstructed in memory.',[
        'Database.insert commits automatically when no transaction is active. A commit writes a new whole-file snapshot with a generation one greater than the previous generation. Reopening decodes the rows and rebuilds the B+ index.',
        'This teaching format favors a readable implementation: opening rebuilds the index, and updates and deletes rebuild it too. It is not an incremental disk-page engine. Each ordinary lesson run recreates its files; Generated files lets you download a snapshot before moving to the saved workspace.'
    ],'''from tinydb import Database, Row
db = Database()
db.insert(Row(1, "Ada", 42))
db.update(1, 73)
reopened = Database()
print("generation", reopened.generation)
print(reopened.select()[0].score)''','db.update(1, 73)','db.update(1, 90)','generation 2\n73\n','generation 2\n90\n','Which two commits account for generation 2? What would be lost if only the in-memory row changed?','Insert Row(4, "Lin", 80), reopen Database(), and print the saved row’s name.','from tinydb import Database, Row\ndb = Database()\ndb.insert(Row(4, "Lin", 80))\nprint(Database().select()[0].name)','Reopening reads the committed snapshot rather than the old Python instance.')
    lab('tdb-transactions','TinyDB: stage several changes before committing','Keep a candidate separate from the last committed state.',[
        'BEGIN clones the committed row mapping into a staged candidate. Reads through that Database instance see staged changes. Another instance opened before COMMIT still sees the last saved snapshot.',
        'COMMIT publishes the candidate as one new generation; ROLLBACK discards it. The engine supports one active transaction per instance and the browser workspace runs statements sequentially. It does not implement concurrent database sessions or multi-process locking.'
    ],'''from tinydb import Database, Row
db = Database()
db.insert(Row(1, "Ada", 42))
db.begin()
db.update(1, 73)
print("staged", db.select()[0].score)
print("saved", Database().select()[0].score)
db.commit()
print("reopened", Database().select()[0].score)''','db.commit()','db.rollback()','staged 73\nsaved 42\nreopened 73\n','staged 73\nsaved 42\nreopened 42\n','Which read observes the candidate? Which operation determines what the final reopen sees?','Begin a transaction, insert Row(2, "Lin", 50), roll it back, then print len(Database().select()).','from tinydb import Database, Row\ndb = Database()\ndb.begin()\ndb.insert(Row(2, "Lin", 50))\ndb.rollback()\nprint(len(Database().select()))','No snapshot was committed, so reopening gives zero rows.',diagram={'kind':'branch','question':'Which transaction decision becomes visible on reopen?','parts':['committed score 42 → staged 73','COMMIT → save score 73','ROLLBACK → keep score 42','Reopen saved snapshot']})
    lab('tdb-statement-errors','TinyDB: retain a transaction after a statement error','Choose commit or rollback explicitly after a rejected change.',[
        'Each modifying statement applies to a separate candidate copy. A duplicate-id insert is rejected before the active transaction changes. Earlier successful statements in that transaction remain staged.',
        'run_script reports the failing line and continues. The learner must choose COMMIT or ROLLBACK. An unfinished transaction is rolled back when the script ends, so BEGIN and its final decision must appear in the same Run statements script.'
    ],'''from tinydb import run_script
run_script("""BEGIN;
INSERT INTO people VALUES (1, 'Ada', 42);
INSERT INTO people VALUES (1, 'Lin', 75);
COMMIT;
SELECT * FROM people;
""")''','COMMIT;','ROLLBACK;','begin ok\ninsert ok\nline 3: duplicate id\ncommit ok\n1 | Ada | 42\n(1 rows)\n','begin ok\ninsert ok\nline 3: duplicate id\nrollback ok\n(0 rows)\n','Why does the rejected duplicate not remove Ada? What does the final transaction decision change?','Run a script beginning a transaction, inserting id 3, then ending without COMMIT. Open a new Database and print its row count.','from tinydb import run_script, Database\nrun_script("BEGIN;\\nINSERT INTO people VALUES (3, \'Ada\', 40);")\nprint(len(Database().select()))','End-of-script rollback prevents an accidental open transaction from being mistaken for saved data.')
    lab('tdb-journal','TinyDB: recover after a simulated interrupted commit','Use the journal’s decision marker to distinguish undo from redo.',[
        'A commit writes a prepared journal containing the complete next snapshot, then writes a committed marker, installs that snapshot and removes the journal. A prepared journal alone has not committed the change. Recovery discards it; a committed journal is replayed.',
        'The crash_at control deliberately interrupts one commit at a named boundary. The example reopens inside the same run to expose the recovery decision. In the saved workspace, .crash commit ends the script and the next Run statements reopens the saved main file and journal. This models protocol boundaries, not a physical power-loss guarantee.'
    ],'''from tinydb import Database, Row, SimulatedCrash
db = Database()
db.insert(Row(1, "Ada", 42))
db.crash_at = "commit"
try:
    db.update(1, 73)
except SimulatedCrash as error:
    print(error)
reopened = Database()
print(reopened.recovered)
print(reopened.select()[0].score)''','crash_at = "commit"','crash_at = "prepare"','simulated crash after commit\nreplayed committed journal\n73\n','simulated crash after prepare\ndiscarded prepared journal\n42\n','Which persistent marker makes 73 recoverable? Why does merely writing a candidate into a journal not commit it?','Commit Row(1, "Ada", 42), interrupt an update to 90 at install, catch SimulatedCrash, then reopen and print the recovered score.','from tinydb import Database, Row, SimulatedCrash\ndb = Database()\ndb.insert(Row(1, "Ada", 42))\ndb.crash_at = "install"\ntry:\n    db.update(1, 90)\nexcept SimulatedCrash:\n    pass\nprint(Database().select()[0].score)','A committed journal makes replay safe even if its snapshot was already installed.',diagram={'kind':'flow','question':'At which boundary has the candidate become a committed decision?','parts':['Prepared journal: old state wins','Committed marker: new state wins','Install next snapshot','Remove journal']})
    lab('tdb-corruption','TinyDB: reject corruption and restore a checked backup','Keep invalid bytes intact until an explicit restore replaces them.',[
        'A checksum failure stops opening the database; it must not silently create an empty replacement. A backup is a separate snapshot that can be verified before being used to replace damaged data.',
        'The example deliberately changes one score byte after making a backup. It catches the failure, explicitly restores the backup bytes and reopens. In the saved workspace, download a backup before experiments, and use Import database to validate and replace the current database deliberately.'
    ],'''from pathlib import Path
from tinydb import Database, Row
db = Database()
db.insert(Row(1, "Ada", 42))
original = Path("people.pfdb").read_bytes()
Path("backup.pfdb").write_bytes(original)
Path("people.pfdb").write_bytes(original.replace(b'"score":42', b'"score":43'))
try:
    Database()
    print("opened")
except ValueError as error:
    print(error)
Path("people.pfdb").write_bytes(Path("backup.pfdb").read_bytes())
print("restored", Database().select()[0].score)''',"b'\"score\":42', b'\"score\":43'","b'\"score\":42', b'\"score\":42'",'snapshot checksum mismatch\nrestored 42\n','opened\nrestored 42\n','Which bytes were changed in the first run, and which explicit operation restores the saved score?','Call unpack on b"not json". Catch ValueError and print "rejected". Do not create a replacement database.','from tinydb import unpack\ntry:\n    unpack(b"not json")\nexcept ValueError:\n    print("rejected")','Rejecting a bad file preserves the distinction between damaged data and an intentionally empty database.')
    lab('tdb-workspace','TinyDB: keep a database between runs','Use the saved workspace while preserving another tab’s changes.',[
        'The source editor contains the complete engine in tinydb.py and a fresh demonstration in main.py. Run code executes that demonstration with temporary files. The Saved TinyDB workspace below uses tinydb.py from the source editor but runs its own Statements field against files kept in this browser.',
        'Run statements opens the saved files, executes one statement per line, then saves the whole returned file set in one browser storage transaction. A workspace revision counts browser saves; the database generation counts TinyDB commits. If another tab saved first, your candidate stays downloadable and cannot overwrite its newer files. Stop or a timeout keeps the previously saved files.'
    ],'''from tinydb import run_script
run_script("""INSERT INTO people VALUES (1, 'Ada', 42);
SELECT * FROM people;
.check
""")''',"(1, 'Ada', 42)","(1, 'Ada', 73)","insert ok\n1 | Ada | 42\n(1 rows)\ncheck ok {'rows': 1, 'height': 1, 'leaves': 1}\n","insert ok\n1 | Ada | 73\n(1 rows)\ncheck ok {'rows': 1, 'height': 1, 'leaves': 1}\n",'In the saved workspace, run the prepared insert and SELECT. Replace Statements with SELECT * FROM people; and run again. Then reload the lesson and run the SELECT once more. Does the row survive without repeating INSERT?','Build a Database containing ids 1, 2 and 3 in one explicit transaction. Delete id 2 in a second transaction and commit. Reopen, validate the index and print the remaining ids.','from tinydb import Database, Row\ndb = Database()\ndb.begin()\nfor key in [1, 2, 3]:\n    db.insert(Row(key, "person", 50))\ndb.commit()\ndb.begin()\ndb.delete(2)\ndb.commit()\nreopened = Database()\nreopened.check()\nprint([row.id for row in reopened.select()])','Database generation and browser workspace revision measure different boundaries. Download important database files; a browser can deny storage or evict it.')
