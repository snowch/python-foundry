const marker='python-foundry:reading-snapshot';let composing=false,restoring=false,saving=false,lock,timer;
const scope=()=>[document.querySelector('.site-header'),document.querySelector('.course-layout')];
const request=value=>new Promise((yes,no)=>{value.onsuccess=()=>yes(value.result);value.onerror=()=>no(value.error);});
async function database(){const opening=indexedDB.open('python-foundry-restart-v1',1);opening.onupgradeneeded=()=>opening.result.createObjectStore('snapshots');return request(opening);}
async function remove(token){if(!token)return;const db=await database();try{const tx=db.transaction('snapshots','readwrite');tx.objectStore('snapshots').delete(token);}finally{db.close();}}
export async function saveReadingState(){
 if(composing||restoring||saving||document.readyState!=='complete'||!window.pythonApp||window.pythonApp.busy())throw Error('Wait for the current run to finish and finish typing before reloading.');
 saving=true;const nodes=scope(),prior=nodes.map(n=>n.inert);nodes.forEach(n=>n.inert=true);let token;
 try{
  token=crypto.randomUUID();const record={token,url:location.pathname+location.search,scroll:[scrollX,scrollY],snapshot:window.pythonApp.snapshot(),details:[...document.querySelectorAll('main details')].map((n,i)=>[i,n.open])};
  const db=await database();try{await new Promise((yes,no)=>{const tx=db.transaction('snapshots','readwrite');tx.objectStore('snapshots').put(record,token);tx.oncomplete=yes;tx.onerror=tx.onabort=()=>no(tx.error||Error('Could not save this window’s work.'));});const read=await request(db.transaction('snapshots').objectStore('snapshots').get(token));if(read?.token!==token)throw Error('The browser did not retain this window’s snapshot.');}finally{db.close();}
  sessionStorage.setItem(marker,token);if(sessionStorage.getItem(marker)!==token)throw Error('Allow browser storage or export your work before reloading.');return token;
 }catch(error){if(token)remove(token).catch(()=>{});throw error;}finally{saving=false;nodes.forEach((n,i)=>n.inert=prior[i]);}
}
export async function restoreReadingState(){
 let token;try{token=sessionStorage.getItem(marker);}catch{return;}if(!token)return;restoring=true;const nodes=scope();nodes.forEach(n=>n.inert=true);
 try{
  const db=await database();let record;try{record=await request(db.transaction('snapshots').objectStore('snapshots').get(token));}finally{db.close();}
  if(record?.url===location.pathname+location.search){window.pythonApp.restore(record.snapshot);const details=[...document.querySelectorAll('main details')];for(const[i,open]of record.details||[])if(details[i])details[i].open=open;requestAnimationFrame(()=>scrollTo(...record.scroll));}
  sessionStorage.removeItem(marker);await remove(token);
 }finally{restoring=false;nodes.forEach(n=>n.inert=false);}
}
function unlock(discard=false){if(discard){let token;try{token=sessionStorage.getItem(marker);sessionStorage.removeItem(marker);}catch{}remove(token).catch(()=>{});}clearTimeout(timer);lock=null;scope().forEach(n=>n.inert=false);}
document.addEventListener('compositionstart',()=>composing=true);document.addEventListener('compositionend',()=>composing=false);
navigator.serviceWorker?.addEventListener('message',async({data,ports})=>{
 if(data?.type==='PREPARE_RESTART')try{if(lock)throw Error('This window is already restarting.');lock=data.token;scope().forEach(n=>n.inert=true);const token=await saveReadingState();if(lock!==data.token){if(sessionStorage.getItem(marker)===token)sessionStorage.removeItem(marker);throw Error('The restart request expired; try again.');}timer=setTimeout(()=>unlock(true),12000);ports[0].postMessage({ready:true});}catch(error){unlock(true);ports[0].postMessage({ready:false,error:error.message});}
 if(data?.type==='ABORT_RESTART'&&data.token===lock)unlock(true);
 if(data?.type==='COMMIT_RESTART'&&data.token===lock)location.reload();
});
