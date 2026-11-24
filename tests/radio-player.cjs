const {strict:assert}=require('node:assert');
const fs=require('node:fs'),vm=require('node:vm');
const flush=()=>new Promise(r=>setImmediate(r));
async function setup(count,broken=false){
 const elements=()=>{const v=Object.fromEntries(['.mf-radio-title','.mf-radio-artist','.mf-radio-status','.mf-radio-toggle','.mf-radio-next'].map(s=>[s,{textContent:'',disabled:false,setAttribute(){},addEventListener(e,fn){this[e]=fn;}}]));v.button=v['.mf-radio-toggle'];v.classes=new Set();return v;};
 const views=[elements(),elements()];const slots=views.map(v=>({classList:{add(c){v.classes.add(c)},toggle(c,on){on?v.classes.add(c):v.classes.delete(c)}},querySelector:s=>v[s]}));
 let audio;class Audio{constructor(){audio=this;this.handlers={};this.paused=true;this.ended=false;this.readyState=4;this.history=[];}setAttribute(){}addEventListener(e,f){this.handlers[e]=f;}set src(s){this._src=s;this.error=null;this.ended=false;}get src(){return this._src;}play(){this.paused=false;this.history.push(this.src);return broken?Promise.reject(new Error('bad media')):Promise.resolve();}pause(){this.paused=true;}}
 const tracks=Array.from({length:count},(_,i)=>({id:String(i),src:`media/${i}.mp3`,artist:`Artist ${i}`,title:`Track ${i}`}));
 vm.runInNewContext(fs.readFileSync('radio/player.js','utf8'),{document:{querySelectorAll:()=>slots,currentScript:{src:'https://example.com/radio/player.js'},body:{append(){}}},Audio,URL,Math,Set,setTimeout,clearTimeout,fetch:async()=>({ok:true,json:async()=>({tracks})})});
 await flush();return {audio,views,tracks};
}
(async()=>{
 const {audio,views}=await setup(5);assert.equal(audio.history.length,0,'no preload/autoplay');
 views[0].button.click();await flush();assert.equal(views[1].button.textContent,'PAUSE');assert.match(views[0]['.mf-radio-artist'].textContent,/Artist/);
 assert(views.every(v=>v.classes.has('is-playing')),'all record logos rotate during playback');
 for(let i=0;i<14;i++){audio.ended=true;audio.handlers.ended();await flush();}
 for(let i=0;i<15;i+=5)assert.equal(new Set(audio.history.slice(i,i+5)).size,5,'no repeat within cycle');
 assert.notEqual(audio.history[4],audio.history[5]);assert.notEqual(audio.history[9],audio.history[10]);
 views[1].button.click();assert.equal(audio.paused,true);const before=audio.src;views[0].button.click();await flush();assert.equal(audio.src,before,'pause resumes same recording');views[0].button.click();
 assert(views.every(v=>!v.classes.has('is-playing')),'all logos stop on pause');
 views[1]['.mf-radio-next'].click();await flush();assert.notEqual(audio.src,before,'Next from paused starts another recording');assert.equal(views[0].button.textContent,'PAUSE');
 const nextCycle=[audio.src];for(let i=0;i<4;i++){views[i%2]['.mf-radio-next'].click();await flush();nextCycle.push(audio.src);}assert.equal(new Set(nextCycle).size,5,'manual Next preserves the shuffle cycle');
 assert(!/\d+ recordings/.test(views[0]['.mf-radio-status'].textContent),'no track count displayed');
 views[0].button.click();
 const broken=await setup(3,true);broken.views[0].button.click();for(let i=0;i<8;i++)await flush();assert.equal(broken.audio.history.length,3,'failures bounded to playlist length');assert.match(broken.views[0]['.mf-radio-status'].textContent,/unavailable/);
 const empty=await setup(0);assert.equal(empty.views[0].button.disabled,true);
 assert.equal(empty.views[0]['.mf-radio-next'].disabled,true);
 const single=await setup(1);single.views[0]['.mf-radio-next'].click();await flush();assert.equal(single.audio.history.length,1);single.views[0].button.click();
 console.log('PASS: no autoplay; shared Play/Next; rotating/paused state; metadata; shuffle cycles without repeats; pause/resume; Next from pause; bounded failures; empty and single-track playlists');
})();
