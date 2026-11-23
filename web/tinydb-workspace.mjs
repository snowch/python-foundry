import {execute,runnerBusy,stopRunner} from './course-controls.mjs';
import {zipFiles} from './archive.js';
const key='python-foundry:tinydb-statements',snapshotKey='tinydb-workspace';
const initial="INSERT INTO people VALUES (1, 'Ada', 42);\nSELECT * FROM people;\n.check";
const bytes=base64=>Uint8Array.from(atob(base64),c=>c.charCodeAt(0));
const database=()=>new Promise((resolve,reject)=>{const request=indexedDB.open('python-foundry-tinydb-v1',1);request.onupgradeneeded=()=>request.result.createObjectStore('workspaces');request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);});
async function read(){const db=await database();try{return await new Promise((resolve,reject)=>{const request=db.transaction('workspaces').objectStore('workspaces').get(snapshotKey);request.onsuccess=()=>resolve(request.result||{revision:0,files:{}});request.onerror=()=>reject(request.error);});}finally{db.close();}}
async function publish(expected,files){const db=await database();try{return await new Promise((resolve,reject)=>{const tx=db.transaction('workspaces','readwrite'),store=tx.objectStore('workspaces');let revision;const request=store.get(snapshotKey);request.onsuccess=()=>{const current=request.result||{revision:0};if(current.revision!==expected){tx.abort();return;}revision=expected+1;store.put({revision,files},snapshotKey);};tx.oncomplete=()=>resolve(revision);tx.onabort=tx.onerror=()=>reject(tx.error||Error('Another tab saved this workspace first. Your candidate is kept for download. Load the latest saved files before trying again.'));});}finally{db.close();}}
export function mountTinyDB({host,sourceFiles,download,onChange}){
 let revision=0,saved={},candidate=null,busy=false,ready=false,output='',status='Loading saved files…',job=0,draft=initial,imported=null,loadSequence=0,saving=false;
 try{draft=localStorage.getItem(key)||initial;}catch{}
 host.innerHTML=`<h2>Saved TinyDB workspace</h2><p><strong>Run statements</strong> uses <code>tinydb.py</code> from the source editor and the database files saved below. It does not run <code>main.py</code>. Keep one complete statement per line. Put BEGIN and its COMMIT or ROLLBACK in the same script.</p><p>Your first saved workspace is empty. After the prepared insert, replace Statements with <code>SELECT * FROM people;</code> to query the saved row without inserting it again.</p><label for="database-statements">Statements</label><textarea id="database-statements" rows="7" spellcheck="false" autocapitalize="off"></textarea><div class="buttons"><button id="database-run" class="primary" type="button">Run statements</button><button id="database-stop" type="button" hidden>Stop</button></div><p id="database-state" role="status"></p><pre id="database-output" tabindex="0"></pre><p id="database-files"></p><details id="database-tools"><summary>Database files and tools</summary><p>Download workspace exports the currently saved files. An interrupted commit can leave both a main snapshot and its recovery journal; keep them together. Download candidate exports a result that could not be saved.</p><div class="buttons"><button id="database-export" type="button">Download workspace</button><button id="database-candidate" type="button" hidden>Download candidate</button><button id="database-latest" type="button">Load latest saved files</button></div><p>Import database validates one PYFDB1 snapshot using Python before replacing the saved main file and removing its previous journal. It does not import a C or Rust Foundry database format. Export your current files first.</p><label for="database-import">Choose a .pfdb database snapshot</label><input id="database-import" type="file" accept=".pfdb"><button id="database-install" type="button" disabled>Validate and replace database</button><p>Only this browser’s saved files persist. Download important files before clearing browser storage. Simulated crashes test the journal protocol; a forced Stop or actual tab termination keeps the previously saved whole file set.</p></details>`;
 const $=id=>host.querySelector('#'+id),statements=$('database-statements');statements.value=draft;
 function render(){
  $('database-run').disabled=!ready||busy||runnerBusy();$('database-stop').hidden=!busy;$('database-stop').disabled=saving;statements.readOnly=busy;$('database-output').textContent=output;$('database-state').textContent=status;
  $('database-files').textContent='Saved workspace revision '+revision+' · '+Object.keys(saved).length+' files'+(Object.keys(saved).length?': '+Object.keys(saved).join(', '):'.');$('database-candidate').hidden=!candidate;
  for(const id of ['database-export','database-latest','database-import'])$(id).disabled=busy;$('database-install').disabled=busy||!ready||!imported||runnerBusy();onChange();
 }
 function exportFiles(files,name){download(name,zipFiles(Object.entries(files).map(([name,data])=>[name,bytes(data)])),'application/zip');}
 statements.oninput=()=>{try{localStorage.setItem(key,statements.value);}catch{status='Statements are kept in this tab only. Export important work before closing it.';}render();};
 statements.onkeydown=event=>{if((event.ctrlKey||event.metaKey)&&event.key==='Enter'){event.preventDefault();run();}};
 async function load(){if(busy)return;const token=++loadSequence;try{const value=await read();if(token!==loadSequence)return;revision=value.revision;saved=value.files;status='Saved files loaded. Run statements to open the database.';}catch(error){status='Browser storage is unavailable. Runs can produce a downloadable candidate, but cannot be marked saved. '+error.message;}finally{if(token===loadSequence){ready=true;render();}}}
 async function run(replacement=null){
  if(busy||runnerBusy()||!ready)return;
  if(candidate){status='This tab has an unsaved candidate. Download it if needed, then choose Load latest saved files before another run.';render();return;}
  const selected=sourceFiles();if(typeof selected['tinydb.py']!=='string'){status='Restore the starter’s tinydb.py source before running statements.';render();return;}
  const sequence=++job,script=statements.value;let stream='';busy=true;status=replacement?'Validating imported database…':'Preparing statements…';render();
  const main=replacement?"from pathlib import Path\nfrom tinydb import unpack\ndata = Path('import.pfdb').read_bytes()\nrows, generation = unpack(data)\nPath('people.pfdb').write_bytes(data)\nPath('people.pfdb.journal').unlink(missing_ok=True)\nprint('validated', len(rows), 'rows at generation', generation)\n":"from tinydb import run_script\nrun_script("+JSON.stringify(script)+")\n";
  const fixtures=replacement?{...saved,'import.pfdb':replacement}:saved;
  try{await execute({type:'run',actionLabel:replacement?'Validate and replace database':'Run statements',payload:{files:{'main.py':main,'tinydb.py':selected['tinydb.py']},binaryFixtures:fixtures,captureWorkspace:true}},async data=>{
   if(sequence!==job)return;
   if(data.type==='status'){status=data.text;render();}
   if(data.type==='output'&&data.kind==='stdout'){stream+=data.text;output=stream;render();}
   if(data.type==='done'){
    const result=data.result;output=result.stdout+(result.error?'\n'+result.error:'');
    if(!result.ok||result.workspaceIncomplete){status=result.workspaceIncomplete?'The result exceeds the workspace limits and was not saved. Previous saved files are kept.':'Python stopped with an error. Previous saved files are kept.';busy=false;render();return;}
    const proposed=Object.fromEntries(result.workspaceFiles.filter(file=>!replacement||file.name!=='import.pfdb').map(file=>[file.name,file.base64]));
    candidate=proposed;saving=true;status='Saving complete file set…';render();
    try{revision=await publish(revision,proposed);saved=proposed;candidate=null;status='Saved workspace revision '+revision+'. Download important files as a backup.';try{navigator.storage?.persist?.().catch(()=>{});}catch{}}
    catch(error){status='Not saved: '+error.message;}
    saving=false;busy=false;render();
   }
   if(data.type==='error'||data.type==='cancelled'){status=data.type==='cancelled'?'Stopped. The previous saved file set is kept.':data.startup?'Python could not start. The previous saved file set is kept.':'Execution could not finish: '+(data.text||data.message||'unknown error')+'. Previous saved files are kept.';busy=false;render();}
  });}catch(error){status=error.message;busy=false;render();}
 }
 $('database-run').onclick=()=>run();$('database-stop').onclick=()=>stopRunner('Statements stopped. Saved files are kept.');
 $('database-export').onclick=()=>exportFiles(saved,'tinydb-workspace.zip');$('database-candidate').onclick=()=>exportFiles(candidate,'tinydb-unsaved-candidate.zip');
 $('database-latest').onclick=()=>{candidate=null;load();};
 $('database-import').onchange=async()=>{const file=$('database-import').files[0];imported=null;if(file){if(file.size>1000000)status='The imported snapshot exceeds the 1 MB file limit.';else{const data=new Uint8Array(await file.arrayBuffer());let text='';for(const byte of data)text+=String.fromCharCode(byte);imported=btoa(text);status='Snapshot selected. Validate and replace database will check its format before saving.';}}render();};
 $('database-install').onclick=()=>imported&&run(imported);
 addEventListener('code-runner-state',render);load();
 return{get ready(){return ready;},get busy(){return busy;},snapshot:()=>({revision,saved,candidate,statements:statements.value,output,status,imported}),restore(value){if(!value)return;loadSequence++;revision=value.revision;saved=value.saved;candidate=value.candidate;statements.value=value.statements;output=value.output;status=value.status;imported=value.imported;ready=true;render();},refresh:render};
}
