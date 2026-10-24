// Independent oracle: no imports from candidate, reference or visible tests.
import fs from 'node:fs'
import assert from 'node:assert/strict'
import { chromium, expect as baseExpect } from '@playwright/test'
const expect=baseExpect.configure({timeout:2500})
const fixtures=JSON.parse(fs.readFileSync('/inputs/quests.json','utf8'))
const selected=JSON.parse(process.env.CRITERIA || '[]')
const results=[]; const definitions=[]
const ordered=[...fixtures].sort((a,b)=>a.title.toLowerCase().localeCompare(b.title.toLowerCase(),'en') || a.id.localeCompare(b.id,'en'))
const ids=rows=>rows.map(q=>q.id)
const test=(id,requirements,description,fn)=>definitions.push({id,requirements,description,fn})
async function api(path,options){const r=await fetch('http://guild:8000'+path,{...options,signal:AbortSignal.timeout(5000)});return {status:r.status,body:await r.json()}}
function error(result,status,code){assert.equal(result.status,status);assert.equal(result.body.error.code,code);assert.equal(typeof result.body.error.message,'string');assert.ok(result.body.error.message.trim())}
const eqList=(r,rows)=>{assert.equal(r.status,200);assert.deepEqual(r.body.quests,rows)}

test('A01',['R01'],'List contains complete canonical objects',async()=>{
 const r=await api('/api/quests');assert.equal(r.status,200);assert.equal(r.body.quests.length,fixtures.length)
 assert.deepEqual([...r.body.quests].sort((a,b)=>a.id.localeCompare(b.id)),[...fixtures].sort((a,b)=>a.id.localeCompare(b.id)))
})
test('A02',['R03'],'Stable title ordering on canonical fixture',async()=>{eqList(await api('/api/quests'),ordered);eqList(await api('/api/quests'),ordered)})
test('A03',['R04'],'Every difficulty enum filters correctly',async()=>{for(const value of ['easy','medium','hard'])eqList(await api('/api/quests?difficulty='+value),ordered.filter(q=>q.difficulty===value))})
test('A04',['R05'],'Trimmed case-insensitive literal title search and empty query',async()=>{
 for(const [query,rows] of [['  bEACON  ',ordered.filter(q=>q.id==='q-beacon')],['',ordered],['  ',ordered],['[',[]],['.',[]],['not-a-real-title',[]]])eqList(await api('/api/quests?q='+encodeURIComponent(query)),rows)
})
test('A05',['R06'],'Status and combined filters use AND',async()=>{
 for(const value of ['open','closed'])eqList(await api('/api/quests?status='+value),ordered.filter(q=>q.status===value))
 eqList(await api('/api/quests?status=open&difficulty=easy'),ordered.filter(q=>q.status==='open'&&q.difficulty==='easy'))
 eqList(await api('/api/quests?q=beacon&status=closed&difficulty=medium'),[])
 eqList(await api('/api/quests?q=beacon&status=open&difficulty=medium'),ordered.filter(q=>q.id==='q-beacon'))
})
test('A06',['R07'],'Invalid and explicitly empty enums return exact domain errors',async()=>{
 for(const query of ['difficulty=','status=','difficulty=legendary','status=retired','difficulty=Easy','status=OPEN'])error(await api('/api/quests?'+query),400,'INVALID_REQUEST')
})
test('A07',['R07'],'Repeated supported keys are rejected even if values agree',async()=>{
 for(const query of ['q=ash&q=beacon','q=&q=','difficulty=easy&difficulty=easy','status=open&status=closed'])error(await api('/api/quests?'+query),400,'INVALID_REQUEST')
})
test('A08',['R07'],'Unknown query keys are ignored',async()=>{eqList(await api('/api/quests?unknown=x&unknown=y'),ordered);eqList(await api('/api/quests?difficulty=hard&surprise=1'),ordered.filter(q=>q.difficulty==='hard'))})
test('A09',['R02'],'All details equal complete canonical objects',async()=>{for(const q of fixtures){const r=await api('/api/quests/'+q.id);assert.equal(r.status,200);assert.deepEqual(r.body,q)}})
test('A10',['R08'],'Unknown ID returns NOT_FOUND with message',async()=>{error(await api('/api/quests/unknown-quest'),404,'NOT_FOUND')})
test('A11',['R13'],'Both service health endpoints preserved',async()=>{
 assert.deepEqual(await api('/health'),{status:200,body:{status:'ok',service:'guild'}})
 const r=await fetch('http://armory:8001/health');assert.equal(r.status,200);assert.deepEqual(await r.json(),{status:'ok',service:'armory'})
})
test('A12',['R13'],'Documented quest routes are read-only',async()=>{
 for(const path of ['/api/quests','/api/quests/q-ash'])for(const method of ['POST','PUT','PATCH','DELETE']){
  const r=await api(path,{method,headers:{'Content-Type':'application/json'},body:'{}'})
  assert.ok([404,405].includes(r.status),'Quest writes are outside T01')
 }
})
test('A13',['R01'],'Filters, errors and details do not change list data',async()=>{
 await api('/api/quests?difficulty=easy');await api('/api/quests/q-cairn');await api('/api/quests?difficulty=invalid');eqList(await api('/api/quests'),ordered)
})
let browser
async function withPage(fn){
 const context=await browser.newContext({viewport:{width:1280,height:900},serviceWorkers:'block'})
 const page=await context.newPage();page.setDefaultTimeout(2500)
 try{await fn(page)}finally{await context.close()}
}
const go=p=>p.goto('http://web:5173',{waitUntil:'domcontentloaded',timeout:10000})
const views=p=>p.getByRole('button',{name:/^View /})
async function choose(control,value){
 const tag=await control.evaluate(el=>el.tagName)
 if(tag==='SELECT')await control.selectOption(value)
 else if(tag==='INPUT')await control.fill(value)
 else{await control.click();await control.page().getByRole('option',{name:new RegExp(value,'i')}).click()}
}
async function selectedValue(control,value){if(['SELECT','INPUT'].includes(await control.evaluate(el=>el.tagName)))await expect(control).toHaveValue(value);else await expect(control).toContainText(new RegExp(value,'i'))}
const view=p=>p.getByRole('button',{name:'View Cairn Echo',exact:true})
async function initial(p){await go(p);await expect(views(p)).toHaveCount(4)}
const nonempty=async locator=>{const message=locator.filter({hasText:/\S/}).first();await expect(message).toBeVisible();assert.ok((await message.innerText()).trim(),'Feedback must be nonempty')}
async function settle(p){await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))))}
async function finishResponse(route){try{await route.request().response().then(r=>r?.finished())}catch{/* An aborted superseded request is valid. */}}

test('U01',['R09'],'Initial browser list contains all canonical quests',()=>withPage(async p=>{
 await initial(p);for(const q of ordered)await expect(p.getByRole('button',{name:'View '+q.title,exact:true})).toBeVisible()
}))
test('U02',['R11','R06'],'Labeled native controls and keyboard Apply filter through real API',()=>withPage(async p=>{
 await initial(p)
 const search=p.getByLabel(/search/i),difficulty=p.getByLabel(/difficulty/i),status=p.getByLabel(/status/i),apply=p.getByRole('button',{name:/apply/i})
 await search.focus();await p.keyboard.type('beacon')
 await choose(difficulty,'medium');await choose(status,'open')
 // Check reachability without prescribing a DOM/tab order.
 const controls=[search,difficulty,status,apply];const reached=new Set()
 await search.focus()
 for(let i=0;i<30&&reached.size<4;i++){
  for(let n=0;n<controls.length;n++)if(await controls[n].evaluate(el=>el===document.activeElement))reached.add(n)
  await p.keyboard.press('Tab')
 }
 assert.equal(reached.size,4,'All filter controls must participate in native focus traversal')
 await apply.focus();await p.keyboard.press('Enter')
 await expect(views(p)).toHaveCount(1);await expect(p.getByRole('button',{name:'View Beacon Road',exact:true})).toBeVisible()
 await p.getByRole('button',{name:'View Beacon Road',exact:true}).focus();await p.keyboard.press('Enter')
 await expect(p.getByText('Relight the mountain beacon.',{exact:true})).toBeVisible()
}))
test('U03',['R11','R12'],'Details show all field values and preserve filters/list',()=>withPage(async p=>{
 await initial(p);await choose(p.getByLabel(/difficulty/i),'hard');await choose(p.getByLabel(/status/i),'open');await p.getByRole('button',{name:/apply/i}).click()
 await expect(views(p)).toHaveCount(1);await view(p).click();await expect(p.getByText('Survey the silent cairn.',{exact:true})).toBeVisible()
 await selectedValue(p.getByLabel(/difficulty/i),'hard');await selectedValue(p.getByLabel(/status/i),'open');await expect(views(p)).toHaveCount(1)
 const text=await p.evaluate(()=>{const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const parts=[];while(walker.nextNode()){const parent=walker.currentNode.parentElement;if(parent&&!parent.closest('script,style,select,input,button,label')&&parent.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))parts.push(walker.currentNode.textContent)}return parts.join(' ')})
 for(const value of ['Cairn Echo','Survey the silent cairn.','hard','open'])assert.ok(text.includes(value),'Missing detail field: '+value)
 for(const value of ['1','4','5','30'])assert.match(text,new RegExp('\\b'+value+'\\b'))
}))
test('U04',['R10'],'Pending list request exposes nonempty live status',()=>withPage(async p=>{
 let held;await p.route('**/api/quests*',route=>{held=route})
 await go(p);await expect.poll(()=>!!held).toBe(true);await nonempty(p.getByRole('status'))
 await held.fulfill({json:{quests:ordered}});await expect(views(p)).toHaveCount(4)
}))
test('U05',['R10'],'Successful empty list has nonempty status and no quest controls',()=>withPage(async p=>{
 await initial(p);await p.getByLabel(/search/i).fill('no-such-quest');const done=p.waitForResponse(r=>r.url().includes('no-such-quest'));await p.getByRole('button',{name:/apply/i}).click();await (await done).finished();await settle(p)
 await expect(views(p)).toHaveCount(0);await nonempty(p.getByRole('status'))
}))
for(const [id,failure] of [['U06','network'],['U07','http']])test(id,['R09'],'List '+failure+' failure exposes nonempty alert',()=>withPage(async p=>{
 await p.route('**/api/quests*',r=>failure==='network'?r.abort('failed'):r.fulfill({status:503,json:{quests:ordered,error:{code:'UNAVAILABLE',message:'fixture'}}}))
 await go(p);await nonempty(p.getByRole('alert'))
}))
test('U08',['R12'],'Detail failure preserves list and reports accessible error',()=>withPage(async p=>{
 await initial(p);await p.route('**/api/quests/q-cairn',r=>r.fulfill({status:404,json:{error:{code:'NOT_FOUND',message:'fixture'}}}))
 await view(p).click();await nonempty(p.getByRole('alert'));await expect(views(p)).toHaveCount(4)
}))
test('U09',['R12'],'An older list response cannot overwrite a newer result',()=>withPage(async p=>{
 await initial(p);let oldRoute
 await p.route('**/api/quests?*',async r=>{const q=new URL(r.request().url()).searchParams.get('q');if(q==='old'){oldRoute=r;return}if(q==='new'){await r.fulfill({json:{quests:ordered.filter(q=>q.id==='q-beacon')}});return}await r.continue()})
 await p.getByLabel(/search/i).fill('old');await p.getByRole('button',{name:/apply/i}).click();await expect.poll(()=>!!oldRoute).toBe(true)
 if(await p.getByRole('button',{name:/apply/i}).isDisabled() || await p.getByLabel(/search/i).isDisabled()){await oldRoute.fulfill({json:{quests:ordered.filter(q=>q.id==='q-ash')}});await finishResponse(oldRoute);oldRoute=null;await expect(p.getByRole('button',{name:/apply/i})).toBeEnabled()}
 await p.getByLabel(/search/i).fill('new');await p.getByRole('button',{name:/apply/i}).click();await expect(p.getByRole('button',{name:'View Beacon Road',exact:true})).toBeVisible();await expect(views(p)).toHaveCount(1)
 if(oldRoute)try{await oldRoute.fulfill({json:{quests:ordered.filter(q=>q.id==='q-ash')}})}catch{/* cancellation is valid */}
 if(oldRoute)await finishResponse(oldRoute);await settle(p);await expect(p.getByRole('button',{name:'View Beacon Road',exact:true})).toBeVisible();await expect(views(p)).toHaveCount(1)
}))
test('U10',['R12'],'An older detail response cannot replace the newer selection',()=>withPage(async p=>{
 await initial(p);let oldRoute
 await p.route('**/api/quests/q-ash',r=>{oldRoute=r})
 await p.getByRole('button',{name:'View Ash Orchard',exact:true}).click();await expect.poll(()=>!!oldRoute).toBe(true)
 if(!await view(p).isVisible() || await view(p).isDisabled()){await oldRoute.fulfill({json:fixtures.find(q=>q.id==='q-ash')});await finishResponse(oldRoute);oldRoute=null;await expect(view(p)).toBeEnabled()}
 await view(p).click();await expect(p.getByText('Survey the silent cairn.',{exact:true})).toBeVisible()
 if(oldRoute)try{await oldRoute.fulfill({json:fixtures.find(q=>q.id==='q-ash')})}catch{/* cancellation is valid */}
 if(oldRoute)await finishResponse(oldRoute);await settle(p);await expect(p.getByText('Survey the silent cairn.',{exact:true})).toBeVisible()
 await expect(p.getByText('Recover the orchard bells.',{exact:true})).toHaveCount(0)
}))

try {
 if(selected.some(id=>!definitions.some(d=>d.id===id)))throw new Error('Unknown criterion selection')
 if(definitions.some(d=>d.id.startsWith('U')&&(!selected.length||selected.includes(d.id))))browser=await chromium.launch({headless:true,args:['--disable-dev-shm-usage']})
 for(const d of definitions.filter(d=>!selected.length||selected.includes(d.id))){
  const started=Date.now()
  try{await d.fn();results.push({...d,fn:undefined,status:'pass',seconds:(Date.now()-started)/1000})}
  catch(e){results.push({...d,fn:undefined,status:'fail',seconds:(Date.now()-started)/1000,evidence:String(e.stack||e)})}
 }
 console.log(JSON.stringify({schema:'guild-ledger.t01-acceptance-observations/v1',status:'completed',browser:browser?.version()||null,results}))
} catch(e){console.log(JSON.stringify({schema:'guild-ledger.t01-acceptance-observations/v1',status:'evaluator_error',error:String(e.stack||e),results}));process.exitCode=2}
finally{if(browser)await browser.close()}
