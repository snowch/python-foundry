import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);const{start}=require('../tests/server.cjs');const{url}=await start({root:new URL('../dist',import.meta.url).pathname});console.log(url);
