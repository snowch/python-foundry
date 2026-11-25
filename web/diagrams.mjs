import {learningModels} from './learning-models.js';
import {learningFigure} from './learning-model.js';
const ns='http://www.w3.org/2000/svg';
const node=(tag,attributes={},text)=>{const value=document.createElementNS(ns,tag);for(const[key,item]of Object.entries(attributes))value.setAttribute(key,item);if(text!==undefined)value.textContent=text;return value;};
function box(svg,x,y,w,h,label){svg.append(node('rect',{x,y,width:w,height:h,rx:8,fill:'var(--light-blue)',stroke:'var(--line)'}),node('text',{x:x+w/2,y:y+h/2+6,'text-anchor':'middle',fill:'var(--ink)','font-size':18},label));}
function arrow(svg,d){svg.append(node('path',{d,fill:'none',stroke:'var(--muted)','stroke-width':2,'marker-end':'url(#diagram-arrow)'}));}
function card(text){const item=document.createElement('div');item.className='concept-card';item.textContent=text;return item;}
export function renderConcept(figure,diagram,id){
 const model=learningModels[id];
 figure.className='';figure.removeAttribute('data-model');figure.removeAttribute('aria-labelledby');
 if(model){
  const template=document.createElement('template');template.innerHTML=learningFigure(model,id);
  const rendered=template.content.firstElementChild;
  for(const attribute of rendered.attributes)figure.setAttribute(attribute.name,attribute.value);
  figure.replaceChildren(...rendered.childNodes);figure.hidden=false;return;
 }

 figure.hidden=!diagram;if(!diagram)return;figure.dataset.kind=diagram.kind;figure.replaceChildren();const caption=document.createElement('figcaption');caption.textContent=diagram.question;figure.append(caption);
 if(diagram.kind==='graph'||diagram.kind==='index'){
  const svg=node('svg',{viewBox:'0 0 450 275',role:'img','aria-label':diagram.question+' '+diagram.edges.map(([a,b])=>a+' leads to '+b).join('; ')}),positions=new Map(diagram.nodes.map(([name,x,y])=>[name,{x,y}])),defs=node('defs'),marker=node('marker',{id:'diagram-arrow',viewBox:'0 0 10 10',refX:8,refY:5,markerWidth:7,markerHeight:7,orient:'auto'});marker.append(node('path',{d:'M0 0 L10 5 L0 10 z',fill:'var(--muted)'}));defs.append(marker);svg.append(defs);
  for(const[from,to]of diagram.edges){const a=positions.get(from),b=positions.get(to);if(diagram.kind==='graph'){const length=Math.hypot(b.x-a.x,b.y-a.y),dx=(b.x-a.x)/length,dy=(b.y-a.y)/length;arrow(svg,`M${a.x+26*dx} ${a.y+26*dy} L${b.x-29*dx} ${b.y-29*dy}`);}else{arrow(svg,`M${a.x} ${a.y+25} L${b.x} ${b.y-29}`);svg.append(node('text',{x:(a.x+b.x)/2+(b.x<a.x?-25:20),y:(a.y+b.y)/2,fill:'var(--ink)','font-size':18},b.x<a.x?'< 3':'≥ 3'));}}
  for(const[name,x,y]of diagram.nodes)if(diagram.kind==='graph'){svg.append(node('circle',{cx:x,cy:y,r:24,fill:'var(--light-blue)',stroke:'var(--line)'}),node('text',{x,y:y+6,'text-anchor':'middle',fill:'var(--ink)','font-size':18},name));}else box(svg,x-77,y-24,154,48,name);
  const viewport=document.createElement('div');viewport.className='concept-viewport';viewport.tabIndex=0;viewport.setAttribute('aria-label','Diagram; scroll horizontally if needed');viewport.append(svg);figure.append(viewport);
 }else if(diagram.kind==='branch'){
  const layout=document.createElement('div');layout.className='concept-branch';layout.append(card(diagram.parts[0]));const title=document.createElement('p');title.className='branch-choice';title.textContent='Choose one path';const choices=document.createElement('div');choices.className='concept-alternatives';choices.append(card(diagram.parts[1]),card(diagram.parts[2]));layout.append(title,choices,card(diagram.parts[3]));figure.append(layout);
 }else if(diagram.kind==='references'){
  const layout=document.createElement('div');layout.className='concept-references';for(const[names,value]of[['original and alias','share one list [1, 2]'],['copy','refers to a new list [1, 2]']]){const row=document.createElement('div');row.append(card(names),card(value));layout.append(row);}figure.append(layout);const note=document.createElement('p');note.className='small';note.textContent='Before the append: original and alias refer to the same list; copy refers to a different outer list.';figure.append(note);
 }else{const list=document.createElement('ol');list.className='concept-steps';for(const part of diagram.parts){const item=document.createElement('li');item.textContent=part;list.append(item);}figure.append(list);}
}
