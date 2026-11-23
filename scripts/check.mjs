import assert from 'node:assert/strict';
import {readdir,readFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {loadCourse} from './curriculum.mjs';
import {validateRelease} from '../web/release-contract.mjs';
const {lessons,modules}=loadCourse();assert.equal(lessons.length,122);assert.equal(modules.length,20);
const seen=new Set();for(const lesson of lessons){assert(!seen.has(lesson.id));for(const id of lesson.prerequisites)assert(seen.has(id),'Prerequisite must point backward');seen.add(lesson.id);assert(lesson.explain.length>=2);assert(lesson.practice&&lesson.goal&&lesson.observe);assert(lesson.files[lesson.focusFile].includes(lesson.before));assert(lesson.refs.every(([,url])=>url.startsWith('https://')));}
for(const folder of ['web','scripts','src','tests'])for(const name of await readdir(folder))if(/\.(m?js|cjs)$/.test(name))execFileSync(process.execPath,['--check',folder+'/'+name]);
const release=validateRelease(JSON.parse(await readFile('dist/release.json')));
for(const file of release.files){const body=await readFile('dist/'+file.path);assert.equal(body.length,file.bytes);assert.equal(createHash('sha256').update(body).digest('hex'),file.sha256,file.path);}
assert(release.files.some(f=>f.path==='runtime/pyodide.asm.wasm'));assert(release.files.some(f=>f.path==='editor.mjs'));assert(!release.files.some(f=>/torch|\.whl$/.test(f.path)));
console.log('PASS 122 coherent lessons, backward prerequisites, all syntax and every offline file hash; standard-library runtime only.');
