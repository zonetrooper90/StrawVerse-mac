// On entering Sources, show installed extensions if there are any;
// otherwise lead with the Marketplace. Keep the tab order stable.
function preferredSourcesTab(){
 return SOURCES_PREVIEW_CATALOG.some(p=>!!sourceDemoState[p.id]?.installed)?'installed':'marketplace';
}
let sourcesTab='installed';
let sourcesExpanded=new Set();
let sourcesFeedback='';
let sourceDemoState={};
let sourceDemoRepos=[];
let sourceDemoBusy=null;
let sourceDemoBusyAction=null;
let sourceDemoPhase=-1;
let sourceDemoOpToken=0;
let sourceDemoTimer=null;
function cancelSourceOperationTimer(){
 const handle=sourceDemoTimer;
 sourceDemoTimer=null;
 if(handle!==null)clearTimeout(handle);
}
function scheduleSourceOperation(token,callback,delay){
 if(token!==sourceDemoOpToken)return;
 cancelSourceOperationTimer();
 const handle=setTimeout(()=>{
  if(sourceDemoTimer!==handle||token!==sourceDemoOpToken)return;
  sourceDemoTimer=null;
  callback();
 },delay);
 sourceDemoTimer=handle;
}
function resetSourcesPreview(){
 sourceDemoOpToken++;
 cancelSourceOperationTimer();
 sourceDemoState=Object.fromEntries(SOURCES_PREVIEW_CATALOG.map(p=>[p.id,{installed:p.initialVersion,health:p.initialHealth,nextOutcome:'working',notice:null,backup:null}]));
 sourceDemoRepos=[];sourceDemoBusy=null;sourceDemoBusyAction=null;sourceDemoPhase=-1;sourcesExpanded.clear();
 sourcesFeedback='Demo restored: sample source versions and states reset.';
 sourcesTab=preferredSourcesTab();
 renderSourcesPreview();
 refreshDiscoverFromSourcePreview();
}
// Initialise only the demonstration model, never touch source files or network.
sourceDemoState=Object.fromEntries(SOURCES_PREVIEW_CATALOG.map(p=>[p.id,{installed:p.initialVersion,health:p.initialHealth,nextOutcome:'working',notice:null,backup:null}]));

