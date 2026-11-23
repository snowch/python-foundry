import {loadPyodide} from 'pyodide';
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const course=JSON.parse(await readFile('.cache/verified-course.json','utf8'));
const py=await loadPyodide({indexURL:'node_modules/pyodide/'});
py.globals.set('_source',await readFile('content/kernel.py','utf8'));
py.runPython("import types,sys\n_kernel=types.ModuleType('_python_foundry_kernel')\nsys.modules['_python_foundry_kernel']=_kernel\nexec(compile(_source, 'runner_kernel.py', 'exec'), _kernel.__dict__)");
for(const lesson of course.lessons){
 for(const mode of ['starter','edit','practice']){
  const files=structuredClone(mode==='practice'?lesson.solutionFiles:lesson.files);
  if(mode==='edit')files[lesson.focusFile]=files[lesson.focusFile].replace(lesson.before,lesson.after);
  py.globals.set('_payload',JSON.stringify({files,fixtures:lesson.fixtures,entry:lesson.entry,stdin:lesson.stdin,args:lesson.args,check:mode==='practice'?{expected:lesson.practiceExpected,behaviour:lesson.practiceCases}:null}));
  const proxy=await py.runPythonAsync("await _kernel.execute(__import__('json').loads(_payload))");const result=proxy.toJs({dict_converter:Object.fromEntries});proxy.destroy();
  const error=mode==='starter'?lesson.expectedError:mode==='edit'?lesson.changedError:null;
  if(error)assert.equal(result.error_type,error,lesson.id+' '+mode);
  else{assert.equal(result.ok,true,lesson.id+' '+mode+' '+result.error);assert.equal(result.stdout,mode==='starter'?lesson.expected:mode==='edit'?lesson.changed:lesson.practiceExpected,lesson.id+' '+mode);if(mode==='practice')assert.equal(result.check.passed,true,lesson.id+' '+JSON.stringify(result.check));}
 }console.log('Wasm checked',lesson.id);
}
console.log('PASS all '+course.lessons.length+' real Pyodide starters, edits, and practice solutions including SQLite, local modules and async tasks');

py.FS.writeFile("tinydb.py",await readFile("content/tinydb.py"));
py.globals.set("_tinydb_test_source",await readFile("tests/tinydb-test.py","utf8"));
py.runPython("import unittest\n_test_namespace={'__name__':'_storage_tests','__file__':'tests/tinydb-test.py'}\nexec(compile(_tinydb_test_source,'tinydb-test.py','exec'),_test_namespace)\n_suite=unittest.TestLoader().loadTestsFromTestCase(_test_namespace['TinyDBTests'])\n_result=unittest.TextTestRunner().run(_suite)\nassert _result.wasSuccessful(), 'TinyDB browser storage engine checks failed'");
