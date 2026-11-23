import {loadPyodide} from './runtime/pyodide.mjs';
export async function startRuntime(){
 const py=await loadPyodide({indexURL:new URL('./runtime/',import.meta.url).href,packageBaseUrl:new URL('./runtime/',import.meta.url).href});
 const response=await fetch(new URL('./kernel.py',import.meta.url));if(!response.ok)throw Error('Could not load the Python runner kernel (HTTP '+response.status+').');
 const source=await response.text();
 py.globals.set('_kernel_source',source);
 py.runPython("import types, sys\n_foundry_kernel = types.ModuleType('_python_foundry_kernel')\nsys.modules['_python_foundry_kernel'] = _foundry_kernel\nexec(compile(_kernel_source, 'runner_kernel.py', 'exec'), _foundry_kernel.__dict__)\ndel _kernel_source");
 return py;
}
export async function runProject(py,payload,emit){
 const kernel=py.globals.get('_foundry_kernel');
 const send=(kind,text)=>emit({type:'output',kind,text});kernel._foundry_emit=send;
 const serialized=JSON.stringify(payload);py.globals.set('_foundry_payload',serialized);
 try{const result=await py.runPythonAsync("await _foundry_kernel.execute(__import__('json').loads(_foundry_payload))");try{return result.toJs({dict_converter:Object.fromEntries});}finally{result.destroy();}}
 finally{kernel._foundry_emit=null;kernel.destroy();py.globals.delete('_foundry_payload');}
}
