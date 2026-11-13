// One fictional transfer is controllable to test the completion moment.
// The existing completed download starts with its percentage hidden.
const DOWNLOAD_ACTION_SVG={"cancel": '<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon download-action-icon" aria-hidden="true" focusable="false"><path d="M18 6l-12 12" /><path d="M6 6l12 12" /></svg>', "dismiss": '<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon download-action-icon" aria-hidden="true" focusable="false"><path d="M18 6l-12 12" /><path d="M6 6l12 12" /></svg>', "retry": '<svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon download-action-icon" aria-hidden="true" focusable="false"><path d="M19.933 13.041a8 8 0 1 1 -9.925 -8.788c3.899 -1 7.935 1.007 9.425 4.747" /><path d="M20 4v5h-5" /></svg>'};
function downloadActionIcon(action){return DOWNLOAD_ACTION_SVG[action]||'';}
const DEMO_COMPLETION_HOLD_MS=3000;
// Browser-only illustration of grouped downloads. No real transfers, files, or path reads.
function makeDemoDownloadEntries(){
 const items=[];
 for(let ep=1;ep<=10;ep++)items.push({id:`quints-${ep}`,animeId:'demo:quints',release:'Season 1',episode:ep,audio:'Sub',totalBytes:350+ep*13,status:ep<=8?'Completed':'Downloading',progress:ep<=8?100:ep===9?61:36});
 items.push(
  {id:'astra-01',animeId:'demo:02',release:'Season 1',episode:1,audio:'Sub',totalBytes:420,status:'Completed',progress:100},
  {id:'astra-02',animeId:'demo:02',release:'Season 1',episode:2,audio:'Sub',totalBytes:460,status:'Downloading',progress:55},
  {id:'astra-03',animeId:'demo:02',release:'Season 1',episode:3,audio:'Sub',totalBytes:440,status:'Queued',progress:0},
  {id:'astra-04',animeId:'demo:02',release:'Season 1',episode:4,audio:'Dub',totalBytes:480,status:'Failed',progress:24},
  {id:'astra-05',animeId:'demo:02',release:'Season 1',episode:5,audio:'Sub',totalBytes:410,status:'Canceled',progress:12},
  {id:'neon-01',animeId:'demo:06',release:'Season 1',episode:1,audio:'Dub',totalBytes:320,status:'Completed',progress:100},
  {id:'neon-02',animeId:'demo:06',release:'Season 1',episode:2,audio:'Dub',totalBytes:390,status:'Completed',progress:100}
 );
 return items;
}
const downloadDemo={entries:makeDemoDownloadEntries(),expanded:new Set(),dismissed:new Set(),fullAt:new Map(),timers:new Map()};
const downloadTerminalStates=new Set(['Completed','Failed','Canceled']);
function visibleDownloadEntries(){return downloadDemo.entries.filter(entry=>!downloadDemo.dismissed.has(entry.id));}
function animeDownloadEntries(id){return visibleDownloadEntries().filter(entry=>entry.animeId===id);}
function allAnimeDownloadEntries(id){return downloadDemo.entries.filter(entry=>entry.animeId===id);}
function downloadProgress(entries){
 const total=entries.reduce((sum,e)=>sum+e.totalBytes,0);
 return total?Math.round(entries.reduce((sum,e)=>sum+e.totalBytes*e.progress/100,0)/total*100):0;
}
function downloadStatusSummary(entries){
 return ['Completed','Downloading','Paused','Queued','Failed','Canceled'].map(status=>{
  const n=entries.filter(entry=>entry.status===status).length;
  return n?`${n} ${status.toLowerCase()}`:'';
 }).filter(Boolean).join(' · ');
}
function downloadGroupStatus(entries){
 if(entries.some(entry=>entry.status==='Downloading'))return ['Downloading','In progress'];
 if(entries.some(entry=>entry.status==='Paused'))return ['Paused','Paused'];
 if(entries.some(entry=>entry.status==='Failed'))return ['Failed','Needs attention'];
 if(entries.some(entry=>entry.status==='Queued'))return ['Queued','Queued'];
 if(entries.every(entry=>entry.status==='Completed'))return ['Completed','Complete'];
 return ['Completed','Finished'];
}
function sfDownloadControlIcon(kind){
 if(kind==='pause')return '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg>';
 return '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="m8 5 11 7-11 7z"/></svg>';
}
