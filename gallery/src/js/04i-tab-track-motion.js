function measuredTrackX(){
 const transform=getComputedStyle(tabPagesTrack).transform;
 return transform==='none'?0:new DOMMatrixReadOnly(transform).m41;
}
/* v13 — The track travels in % of the *current* viewport width, rather
   than pixels captured when a tab was clicked. Percentage transforms are
   automatically recomputed by the browser on window/container resize,
   including while a WAAPI slide is running. */
function tabTrackPercent(x){
 const width=tabPagesViewport.clientWidth;
 return width>0?x/width*100:0;
}
function tabTrackTransform(percent){return `translate3d(${percent}%,0,0)`;}
function freezeTabTrack(){
 if(!tabTrackAnimation)return measuredTrackX();
 const current=measuredTrackX();
 const transform=tabTrackTransform(tabTrackPercent(current));
 tabTrackAnimation.onfinish=null;
 tabTrackAnimation.cancel();
 tabTrackAnimation=null;
 tabPagesTrack.style.transform=transform;
 return current;
}
function snapTabTrack(view){
 freezeTabTrack();
 tabTrackTarget=view;
 tabPagesTrack.style.transform=tabTrackTransform(-tabOrder.indexOf(view)*100);
}
function animateTabTrack(view){
 const width=tabPagesViewport.clientWidth;
 if(width<=0)return;
 const from=freezeTabTrack();
 const fromPercent=tabTrackPercent(from);
 const destinationPercent=-tabOrder.indexOf(view)*100;
 tabTrackTarget=view;
 const toTransform=tabTrackTransform(destinationPercent);
 if(window.matchMedia('(prefers-reduced-motion: reduce)').matches||Math.abs(fromPercent-destinationPercent)<.05){
  tabPagesTrack.style.transform=toTransform;
  return;
 }
 // A single uninterrupted trajectory through intermediate pages; both
 // keyframes remain relative to the viewport width even during resizing.
 const pages=Math.abs(destinationPercent-fromPercent)/100;
 const duration=Math.round(Math.max(160,Math.min(520,310*Math.pow(pages,.68))));
 const fromTransform=tabTrackTransform(fromPercent);
 tabPagesTrack.style.transform=toTransform;
 const running=tabPagesTrack.animate(
  [{transform:fromTransform},{transform:toTransform}],
  {duration,easing:'cubic-bezier(.32,.08,.22,1)',fill:'both'}
 );
 tabTrackAnimation=running;
 running.onfinish=()=>{
  if(tabTrackAnimation!==running)return;
  tabPagesTrack.style.transform=toTransform;
  tabTrackAnimation=null;
  running.cancel();
 };
}
