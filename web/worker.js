import {startRuntime,runProject} from './engine.js';
let runtime,running=false;
async function prepare(){
 const original=self.fetch;let reject;const failure=new Promise((_,no)=>reject=no);
 self.fetch=async(...args)=>{try{const response=await original.apply(self,args);if(!response.ok)throw Error('Could not load '+new URL(typeof args[0]==='string'?args[0]:args[0].url||String(args[0]),self.location.href).pathname.split('/').pop()+' (HTTP '+response.status+').');return response;}catch(error){reject(error);throw error;}};
 try{return await Promise.race([startRuntime(),failure]);}finally{self.fetch=original;}
}
self.onmessage=async({data})=>{
 if(running)return;running=true;
 try{
  if(!runtime){self.postMessage({type:'status',stage:'loading',text:'Loading Python…'});runtime=await prepare();}
  if(data.type==='prepare'){self.postMessage({type:'ready'});return;}
  self.postMessage({type:'status',stage:'running',text:'Running Python…'});
  const result=await runProject(runtime,data.payload,value=>self.postMessage(value));
  self.postMessage({type:'done',result});
 }catch(error){self.postMessage({type:'error',text:error.message,startup:!runtime});}
 finally{running=false;}
};
