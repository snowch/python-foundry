"""The real Python storage engine: invariants, transactions and failure boundaries."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import random
import tempfile
import unittest

# This loader also works inside the browser interpreter's virtual filesystem.
engine = Path(__file__).resolve().parent.parent / 'content/tinydb.py'
if not engine.exists():
    engine = Path('tinydb.py')
spec = importlib.util.spec_from_file_location('tinydb_under_test', engine)
tinydb = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = tinydb
spec.loader.exec_module(tinydb)
Row, Database, BPlusTree = tinydb.Row, tinydb.Database, tinydb.BPlusTree

class TinyDBTests(unittest.TestCase):
    def setUp(self):
        self.previous = os.getcwd()
        self.directory = tempfile.TemporaryDirectory()
        os.chdir(self.directory.name)
    def tearDown(self):
        os.chdir(self.previous)
        self.directory.cleanup()
    def test_row_boundaries(self):
        Row(0, 'é' * 16, 100)
        for args in [(-1, 'Ada', 50), (True, 'Ada', 50), (1, '', 50), (1, 'é' * 17, 50), (1, 'Ada', 101), (1, 'Ada', False)]:
            with self.subTest(args=args), self.assertRaises(ValueError):Row(*args)
    def test_bplus_random_splits_and_separator_equality(self):
        for seed in range(4):
            keys=list(range(140));random.Random(seed).shuffle(keys)
            index=BPlusTree()
            for key in keys:
                index.insert(Row(key, str(key), key % 101));index.check()
            for key in keys:self.assertEqual(index.get(key).id,key)
            self.assertIsNone(index.get(141))
            self.assertEqual([row.id for row in index.between(17,83)],list(range(17,84)))
            self.assertEqual(index.between(9,1),[])
            with self.assertRaises(ValueError):index.insert(Row(12,'duplicate',50))
            self.assertEqual(index.check()['rows'],140)
    def test_leaf_link_cycle_rejected(self):
        index=BPlusTree()
        for key in range(10):index.insert(Row(key,'person',50))
        leaf=index._leaf(0);leaf.next=leaf
        with self.assertRaises(ValueError):index.check()
    def test_codec_rejects_changed_and_rechecksummed_invalid_rows(self):
        data=tinydb.pack({1:Row(1,'Ada',42)},3)
        self.assertEqual(tinydb.unpack(data)[1],3)
        with self.assertRaises(ValueError):tinydb.unpack(data.replace(b'"score":42',b'"score":43'))
        envelope=json.loads(data);envelope['payload']['rows'][0]['score']=101
        import hashlib
        envelope['sha256']=hashlib.sha256(tinydb.canonical(envelope['payload'])).hexdigest()
        with self.assertRaises(ValueError):tinydb.unpack(tinydb.canonical(envelope))
    def test_reopen_commit_update_delete(self):
        db=Database();db.begin()
        for key in range(40):db.insert(Row(key,'person',50))
        db.commit();self.assertEqual(db.generation,1)
        db.begin();db.update(2,73);db.delete(3);db.commit()
        reopened=Database();self.assertEqual(reopened.generation,2)
        self.assertEqual(reopened.select(2,2)[0].score,73)
        self.assertEqual(reopened.select(3,3),[]);self.assertEqual(reopened.check()['rows'],39)
    def test_rollback_and_statement_atomicity(self):
        db=Database();db.insert(Row(1,'Ada',42));before=db.path.read_bytes();db.begin();db.update(1,73)
        with self.assertRaises(ValueError):db.insert(Row(1,'Lin',50))
        with self.assertRaises(ValueError):db.update(1,101)
        self.assertEqual(db.select()[0].score,73)
        self.assertEqual(Database().select()[0].score,42)
        db.rollback();self.assertEqual(db.path.read_bytes(),before)
    def test_unfinished_script_transaction_is_not_saved(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            tinydb.run_script("BEGIN;\nINSERT INTO people VALUES (1, 'Ada', 42);")
        self.assertIn('rolled back',output.getvalue());self.assertEqual(Database().select(),[])
    def test_each_recovery_boundary(self):
        for phase,expected in [('prepare',42),('commit',73),('install',73)]:
            with self.subTest(phase=phase):
                db=Database(phase+'.pfdb');db.insert(Row(1,'Ada',42));db.crash_at=phase
                with self.assertRaises(tinydb.SimulatedCrash):db.update(1,73)
                reopened=Database(phase+'.pfdb')
                self.assertEqual(reopened.select()[0].score,expected)
                self.assertFalse(reopened.journal.exists())
                self.assertEqual(Database(phase+'.pfdb').select()[0].score,expected)
    def test_corrupt_main_can_recover_committed_afterimage(self):
        db=Database();db.insert(Row(1,'Ada',42));db.crash_at='commit'
        with self.assertRaises(tinydb.SimulatedCrash):db.update(1,73)
        db.path.write_bytes(b'partial main file')
        self.assertEqual(Database().select()[0].score,73)
    def test_mismatched_journal_does_not_overwrite(self):
        db=Database();db.insert(Row(1,'Ada',42));before=db.path.read_bytes()
        db.journal.write_bytes(tinydb.canonical({'phase':'committed','base':7,'after':json.loads(tinydb.pack({2:Row(2,'Lin',50)},8))}))
        with self.assertRaises(ValueError):Database()
        self.assertEqual(db.path.read_bytes(),before)
    def test_corruption_is_not_reset_to_empty(self):
        Path('people.pfdb').write_bytes(b'bad snapshot')
        with self.assertRaises(ValueError):Database()
        self.assertEqual(Path('people.pfdb').read_bytes(),b'bad snapshot')
    def test_sql_boundaries_and_quoted_name(self):
        script="INSERT INTO people VALUES (1, 'Ada, Lovelace', 42);\nINSERT INTO people VALUES (2, 'O''Brien', 75);\nSELECT * FROM people WHERE id >= 1 AND id <= 2;\nSELECT * FROM people WHERE id = 99;\nDROP TABLE people;"
        with contextlib.redirect_stdout(io.StringIO()) as output:tinydb.run_script(script)
        text=output.getvalue();self.assertIn("O'Brien",text);self.assertIn('Ada, Lovelace',text);self.assertIn('(0 rows)',text);self.assertIn('statement not supported',text)
        self.assertEqual(len(Database().select()),2)
    def test_snapshot_and_export_are_separate_files(self):
        with contextlib.redirect_stdout(io.StringIO()):tinydb.run_script("INSERT INTO people VALUES (1, 'Ada', 42);\n.snapshot backup.pfdb\n.export rows.json")
        self.assertEqual(tinydb.unpack(Path('backup.pfdb').read_bytes())[1],1)
        self.assertEqual(json.loads(Path('rows.json').read_text())[0]['name'],'Ada')

if __name__=='__main__':unittest.main()
