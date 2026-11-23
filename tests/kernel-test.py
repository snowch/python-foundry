"""Checks of the execution boundary shared by native Python and Pyodide."""
import base64
import importlib.util
import pathlib
import sys
import unittest
spec=importlib.util.spec_from_file_location('tested_kernel',pathlib.Path(__file__).resolve().parent.parent/'content/kernel.py')
kernel=importlib.util.module_from_spec(spec);spec.loader.exec_module(kernel)
class KernelTests(unittest.IsolatedAsyncioTestCase):
    async def test_input_and_real_stdin_share_one_stream(self):
        previous=sys.stdin
        result=await kernel.execute({'files':{'main.py':'import sys\nprint(input())\nprint(sys.stdin.read(), end="")'},'stdin':'first\nsecond\nthird\n'})
        self.assertTrue(result['ok']);self.assertEqual(result['stdout'],'first\nsecond\nthird\n');self.assertIs(sys.stdin,previous)
    async def test_complete_workspace_preserves_unchanged_and_removes_deleted(self):
        encode=lambda value:base64.b64encode(value).decode()
        result=await kernel.execute({'files':{'main.py':'from pathlib import Path\nPath("old.journal").unlink()\nPath("new.txt").write_text("hello", encoding="utf-8")'},'binaryFixtures':{'main.pfdb':encode(b'unchanged'),'old.journal':encode(b'remove')},'captureWorkspace':True})
        self.assertTrue(result['ok']);self.assertEqual({f['name'] for f in result['workspaceFiles']},{'main.pfdb','new.txt'})
        self.assertEqual({f['name'] for f in result['files']},{'new.txt'})
    async def test_incomplete_workspace_cannot_claim_a_complete_file_set(self):
        result=await kernel.execute({'files':{'main.py':'from pathlib import Path\nPath("large.bin").write_bytes(b"x" * 1000001)'},'captureWorkspace':True})
        self.assertTrue(result['ok']);self.assertTrue(result['workspaceIncomplete']);self.assertEqual(result['workspaceFiles'],[])
    async def test_an_execution_failure_returns_no_successful_practice_check(self):
        result=await kernel.execute({'files':{'main.py':'raise ValueError("invalid")'},'check':{'expected':'','behaviour':None}})
        self.assertFalse(result['ok']);self.assertIsNone(result['check']);self.assertEqual(result['error_type'],'ValueError');self.assertIn('main.py',result['error'])
if __name__=='__main__':unittest.main()
