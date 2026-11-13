const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const origin='https://modularfriends.github.io';
(async()=>{
 let playlist;
 for(let i=0;i<40;i++){
  try { const r=await fetch(origin+'/radio/tracks.json?qa='+Date.now());if(r.ok){playlist=await r.json();if(playlist.tracks?.length>=20)break;} }catch{}
  await new Promise(r=>setTimeout(r,15000));
 }
 assert(playlist?.tracks?.length>=20,'published playlist contains recordings');
 const browser=await chromium.launch();const results=[];fs.mkdirSync('test-results',{recursive:true});
 try{
  for(const width of [1280,390]){
   const page=await browser.newPage({viewport:{width,height:900}});
   await page.goto(origin+'/?qa='+Date.now()+'#radio',{waitUntil:'domcontentloaded'});
   const button=page.locator('#radio .mf-radio-toggle');await button.waitFor();await page.waitForFunction(()=>!document.querySelector('#radio button').disabled);
   assert.equal(await page.locator('audio').count(),1);
   assert(await page.locator('audio').evaluate(a=>a.paused&&!a.currentSrc),'no audio request before Play');
   await button.click();
   await page.waitForFunction(()=>{const a=document.querySelector('audio');return !a.paused&&a.currentTime>1&&a.readyState>=3;},{},{timeout:90000});
   const first=await page.locator('audio').evaluate(a=>({src:a.currentSrc,duration:a.duration,time:a.currentTime}));
   assert(first.src.endsWith('.mp3'));
   assert((await page.locator('#radio .mf-radio-artist').textContent()).length>0);
   await page.locator('#radio [data-mf-radio]').screenshot({path:`test-results/radio-${width}.png`});
   const rect=await page.locator('#radio [data-mf-radio]').boundingBox();assert(rect.x>=0&&rect.x+rect.width<=width+1,'radio fits viewport');
   await page.locator('#artists .mf-radio-toggle').click();
   assert(await page.locator('audio').evaluate(a=>a.paused));
   const paused=await page.locator('audio').evaluate(a=>a.currentTime);await page.waitForTimeout(400);assert(Math.abs((await page.locator('audio').evaluate(a=>a.currentTime))-paused)<.1);
   await page.locator('#artists .mf-radio-toggle').click();await page.waitForFunction(()=>!document.querySelector('audio').paused);
   if(width===1280){
    await page.locator('audio').evaluate(a=>{a.currentTime=a.duration-.5;});
    await page.waitForFunction(src=>{const a=document.querySelector('audio');return a.currentSrc!==src&&!a.paused&&a.currentTime>1;},first.src,{timeout:90000});
   }
   await page.locator('#artists [data-mf-radio]').screenshot({path:`test-results/artists-${width}.png`});
   await page.locator('#artists .mf-radio-toggle').click();
   await page.goto(origin+'/shop.html?qa='+Date.now()+'#audio',{waitUntil:'domcontentloaded'});
   await page.waitForFunction(()=>{const b=document.querySelector('.mf-radio-toggle');return b&&!b.disabled;});
   await page.locator('.mf-radio-toggle').click();await page.waitForFunction(()=>document.querySelector('audio').currentTime>1,{},{timeout:90000});
   const box=await page.locator('[data-mf-radio]').boundingBox();assert(box.x>=0&&box.x+box.width<=width+1,'audio section fits viewport');
   await page.locator('[data-mf-radio]').screenshot({path:`test-results/audio-${width}.png`});
   results.push({width,playback:true,pauseResume:true,sharedControls:true,metadata:true,autoAdvance:width===1280?'real ended event':'covered on desktop',first});
   await page.close();
  }
  fs.writeFileSync('test-results/results.json',JSON.stringify({tracks:playlist.tracks.length,results},null,2));console.log(JSON.stringify(results));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
