let modalExitTimer=null;
function countTag(t){return t==='All Titles'?demo.length:demo.filter(x=>x.tags.includes(t)).length;}
// Browser-only sliding-tab and label-anchored cursor-follow hover-pill experiment.
// No changes have been applied to the Gallery macOS application.
const tabOrder=['discover','library','downloads'];
const tabPagesViewport=document.getElementById('tab-pages-viewport');
const tabPagesTrack=document.getElementById('tab-pages-track');
const tabPages=Object.fromEntries(tabOrder.map(view=>[view,tabPagesViewport.querySelector(`[data-tab-page="${view}"]`)]));

