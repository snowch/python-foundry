"""Execute every starter, guided edit and practice solution with real CPython."""
import asyncio
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parent.parent
catalog=json.loads(subprocess.check_output([sys.executable,str(root/'content/course.py')],text=True))
spec=importlib.util.spec_from_file_location('foundry_kernel',root/'content/kernel.py');kernel=importlib.util.module_from_spec(spec);spec.loader.exec_module(kernel)
async def verify():
 failures=[]
 for lesson in catalog['lessons']:
  for mode in ['starter','edit','practice']:
   files=dict(lesson['solutionFiles'] if mode=='practice' else lesson['files'])
   if mode=='edit':files[lesson['focusFile']]=files[lesson['focusFile']].replace(lesson['before'],lesson['after'],1)
   payload={'files':files,'fixtures':lesson['fixtures'],'entry':lesson['entry'],'stdin':lesson['stdin'],'args':lesson['args']}
   result=await kernel.execute(payload)
   error=lesson.get('expectedError') if mode=='starter' else lesson.get('changedError') if mode=='edit' else None
   expected=lesson['expected'] if mode=='starter' else lesson['changed'] if mode=='edit' else None
   if error:
    if result['error_type']!=error:failures.append((lesson['id'],mode,error,result))
   elif not result['ok'] or (expected is not None and result['stdout']!=expected):failures.append((lesson['id'],mode,expected,result))
   if mode=='practice' and result['ok']:
    lesson['practiceExpected']=result['stdout']
    payload['check']={'expected':result['stdout'],'behaviour':lesson.get('practiceCases')}
    checked=await kernel.execute(payload)
    if not checked['check']['passed']:failures.append((lesson['id'],'practice behaviour',checked))
  print('checked',lesson['id'],flush=True)
 if failures:
  print(json.dumps(failures,indent=2,ensure_ascii=False));raise SystemExit(1)
 print(f"PASS {len(catalog['lessons'])} starters, guided edits and practice solutions; reusable-function cases also pass")
 if '--catalog' in sys.argv:
  Path(sys.argv[sys.argv.index('--catalog')+1]).write_text(json.dumps(catalog,ensure_ascii=False))
asyncio.run(verify())
