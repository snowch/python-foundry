"""Verify ZIP integrity and run the exported desktop programs, not reconstructed source."""
import json,pathlib,subprocess,sys,tempfile,zipfile
root=pathlib.Path(__file__).resolve().parent.parent
course=json.loads((root/'.cache/verified-course.json').read_text())
for lesson in course['lessons']:
 with tempfile.TemporaryDirectory(prefix='python-foundry-export-') as folder:
  with zipfile.ZipFile(root/'dist/downloads'/f"{lesson['id']}.zip") as archive:
   assert archive.testzip() is None
   assert set(archive.namelist())=={*lesson['files'],*lesson['fixtures'],'README.md'}
   archive.extractall(folder)
  result=subprocess.run([sys.executable,lesson['entry'],*lesson['args']],cwd=folder,input=lesson['stdin'],text=True,capture_output=True,timeout=10)
  if lesson['expectedError']:
   assert result.returncode!=0 and lesson['expectedError'] in result.stderr,lesson['id']
  else:
   assert result.returncode==0,(lesson['id'],result.stderr)
   assert result.stdout==lesson['expected'],(lesson['id'],result.stdout,lesson['expected'])
print(f"PASS all {len(course['lessons'])} desktop project ZIPs, Unicode filenames/CRC, prepared files and async entry conversion")
