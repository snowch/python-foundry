import {execFileSync} from 'node:child_process';
export function loadCourse(){return JSON.parse(execFileSync('python',['content/course.py'],{encoding:'utf8',maxBuffer:8*1024*1024}));}
