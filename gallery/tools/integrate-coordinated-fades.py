#!/usr/bin/env python3
"""Repair Gallery page transition layout/provenance against the exact GitHub checkpoint.

Only transform the checksum-verified committed 2026-11-10 sequential-fade
checkpoint. Does not touch the working Anime ↔ Player snapshot animation.
"""
import argparse
from pathlib import Path
import hashlib

SOURCE_SHA = '5b81d793f474fcf94bc1cd719f8a848cad66e63129b937fbd20450aa5c2d094f'

def replace_once(text, old, new):
    n=text.count(old)
    if n != 1:
        raise RuntimeError(f'Expected one exact replacement, found {n}: {old[:130]!r}')
    return text.replace(old,new,1)

def patch(raw):
    baseline=hashlib.sha256(raw).hexdigest()
    if baseline!=SOURCE_SHA:
        raise RuntimeError(f'Unsafe baseline: {baseline} (expected {SOURCE_SHA})')
    s=raw.decode('utf-8')

    # Keep existing ::view-transition CSS and function for Anime ↔ Player:
    # only other routes receive the two-phase, DOM-committed fade.
    old_header='''let galleryStageTransition=null;
let galleryStageMutating=false;
const galleryReducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
function clearGallerySurfaceEntrance(){screen.classList.remove('surface-enter');}
function transitionGalleryStage(mutator){'''
    new_header='''let galleryStageTransition=null;
let galleryStageMutating=false;
let galleryStageFadeInProgress=false;
let galleryStagePending=null;
const galleryReducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
function clearGallerySurfaceEntrance(){screen.classList.remove('surface-enter');}
// Preserve this browser snapshot transition exclusively for Anime Details ↔ Player.
// The user confirmed that route looks correct and it must not be redesigned.
function transitionGalleryPlayer(mutator){'''
    s=replace_once(s,old_header,new_header)

    marker='''// A disabled CSS animation does not fire animationend. Clean up after the
// normal animation, and when the motion preference changes in either direction.'''
    fader='''// All non-Player routes now fade actual DOM in a deliberate two-phase sequence.
// Until outgoing content *and* main navigation are fully invisible, neither
// application state nor the header/tab layout is allowed to change.
// This avoids ghosting and visible header-height jumps when tabs appear/vanish.
function transitionGalleryStage(mutator){
 if(galleryStageMutating){mutator();return;}
 if(galleryStageFadeInProgress){galleryStagePending=mutator;return;}
 if(galleryStageTransition){galleryStageTransition.skipTransition();galleryStageTransition=null;workspace.style.viewTransitionName='';}
 clearGallerySurfaceEntrance();
 if(galleryReducedMotion.matches||!Element.prototype.animate){
  galleryStageMutating=true;
  try{mutator();}finally{galleryStageMutating=false;}
  return;
 }
 galleryStageFadeInProgress=true;
 const app=document.querySelector('.app');
 const tabs=document.querySelector('.top .tabs');
 const header=document.querySelector('.top');
 const oldBorder=getComputedStyle(header).borderBottomColor;
 app.setAttribute('aria-busy','true');
 app.classList.add('gallery-route-transitioning');
 // Pause current live input; keyboard events and clicks must not mutate routes
 // during the invisible midpoint (including Settings Escape or tab hotkeys).
 let oldWorkspace=null,oldTabs=null,oldBorderAnim=null,newWorkspace=null,newTabs=null,newBorderAnim=null;
 const animate=(node,frames,timing)=>node.animate(frames,{...timing,fill:'forwards'});
 const fadeTiming={duration:150,easing:'ease-in'};
 const showTiming={duration:150,easing:'ease-out'};
 const visible=node=>Boolean(node&&node.getClientRects().length&&getComputedStyle(node).display!=='none');
 const finish=()=>{
  for(const anim of [oldWorkspace,oldTabs,oldBorderAnim,newWorkspace,newTabs,newBorderAnim])anim?.cancel();
  workspace.style.opacity='';tabs.style.opacity='';header.style.borderBottomColor='';
  app.removeAttribute('aria-busy');app.classList.remove('gallery-route-transitioning');
  galleryStageFadeInProgress=false;
  if(galleryStagePending){const next=galleryStagePending;galleryStagePending=null;queueMicrotask(()=>transitionGalleryStage(next));}
 };
 try{
  oldWorkspace=animate(workspace,[{opacity:1},{opacity:0}],fadeTiming);
  if(visible(tabs))oldTabs=animate(tabs,[{opacity:1},{opacity:0}],fadeTiming);
  oldBorderAnim=animate(header,[{borderBottomColor:oldBorder},{borderBottomColor:'transparent'}],fadeTiming);
 }catch(error){finish();galleryStageMutating=true;try{mutator();}finally{galleryStageMutating=false;}return;}
 oldWorkspace.finished.then(()=>{
  // Make the midpoint state opaque-to-input and transparent-to-view *before*
  // canceling the outgoing animations. The correct new page is mounted here.
  workspace.style.opacity='0';tabs.style.opacity='0';header.style.borderBottomColor='transparent';
  oldWorkspace.cancel();oldTabs?.cancel();oldBorderAnim?.cancel();
  galleryStageMutating=true;
  try{mutator();}finally{galleryStageMutating=false;}
  // Reading layout ensures that the new tab/header geometry is in effect
  // before either incoming opacity starts. Shared branding never moves.
  void workspace.offsetWidth;
  newWorkspace=animate(workspace,[{opacity:0},{opacity:1}],showTiming);
  if(visible(tabs))newTabs=animate(tabs,[{opacity:0},{opacity:1}],showTiming);
  header.style.borderBottomColor='';
  const incomingBorder=getComputedStyle(header).borderBottomColor;
  header.style.borderBottomColor='transparent';
  newBorderAnim=animate(header,[{borderBottomColor:'transparent'},{borderBottomColor:incomingBorder}],showTiming);
  return newWorkspace.finished;
 }).then(finish).catch(error=>{
  console.error('Gallery coordinated page fade failed',error);
  finish();
 });
}
// A route mutation must not happen while the old layout is still fading.
// Guard pointer/keyboard navigation, but retain focus and settings semantics.
function galleryRouteInputGate(event){
 if(!galleryStageFadeInProgress||galleryStageMutating)return;
 if(event.type==='click'||event.type==='keydown'){
  event.preventDefault();event.stopImmediatePropagation();
 }
}
document.querySelector('.app').addEventListener('click',galleryRouteInputGate,true);
document.querySelector('.app').addEventListener('keydown',galleryRouteInputGate,true);
'''
    s=replace_once(s,marker,fader+marker)

    # Keep existing anime<->player CSS snapshot path unchanged in these two callers.
    s=replace_once(s,''' transitionGalleryStage(()=>{
  state.playbackReturnScroll=workspace.scrollTop;''', ''' transitionGalleryPlayer(()=>{
  state.playbackReturnScroll=workspace.scrollTop;''')
    s=replace_once(s,''' transitionGalleryStage(()=>{
  state.playback=null;render();workspace.scrollTop=state.playbackReturnScroll;''', ''' transitionGalleryPlayer(()=>{
  state.playback=null;render();workspace.scrollTop=state.playbackReturnScroll;''')

    # Fix recently-watched routing. Only the full Watch History page should
    # set detailReturnHistory and suspend its DOM state.
    old_recent=""" for(const button of content.querySelectorAll('[data-wh-recent]'))button.addEventListener('click',()=>{const r=whRecords.find(r=>r.id===button.dataset.whRecent);if(!r)return;whEnter();whOpenTitle(r);});"""
    new_recent=""" for(const button of content.querySelectorAll('[data-wh-recent]'))button.addEventListener('click',()=>{
  const r=whRecords.find(r=>r.id===button.dataset.whRecent);
  if(!r)return;
  if(!r.galleryId||!demo.some(x=>x.id===r.galleryId)){
   modal('Sample Recently Watched entry','<p class="description">This preview record has no matching anime detail page yet.</p>','<button class="btn primary" id="wh-sample-okay">Got it</button>');
   document.getElementById('wh-sample-okay')?.addEventListener('click',closeModal);
   return;
  }
  // This card is on Discover, not inside Watch History. Back must return to Discover.
  showDetail(r.galleryId,false,r.installmentId);
 });"""
    s=replace_once(s,old_recent,new_recent)
    s=replace_once(s,'''function showDetail(id,fromHistory=false){''','''function showDetail(id,fromHistory=false,installmentId=null){''')
    old_season="""  state.detailId=id;state.detailSeason=0;state.detailRelated=null;
  state.detailEpisodeFilter='all';state.detailEpisode=1;state.detailAudio=null;"""
    new_season="""  state.detailId=id;state.detailSeason=0;state.detailRelated=null;
  if(installmentId){const index=getSeasons(x).findIndex(season=>season.id===installmentId);if(index>=0)state.detailSeason=index;}
  state.detailEpisodeFilter='all';state.detailEpisode=1;state.detailAudio=null;"""
    s=replace_once(s,old_season,new_season)

    # setView is the only remaining route setter that changed state *before*
    # starting its fade. Put the state changes inside the midpoint mutator.
    old_set=""" state.playback=null;state.view=view;state.detailId=null;state.query='';
 updateActiveTab(view);
 searchToggle.setAttribute('aria-label',view==='library'?'Search your library':view==='downloads'?'Search downloads':'Search anime');
 if(!wasTop){
  transitionGalleryStage(()=>render()); // Detail/player → main tabs, with an outgoing capture.
 }else{
  if(!tabPages[view].dataset.initialized)renderTabPage(view);
  syncTabPanelAccessibility();
  animateTabTrack(view); // Interruptions immediately redirect from the current position.
 }"""
    new_set=""" const changeView=()=>{
  state.playback=null;state.view=view;state.detailId=null;state.query='';
  updateActiveTab(view);
  searchToggle.setAttribute('aria-label',view==='library'?'Search your library':view==='downloads'?'Search downloads':'Search anime');
 };
 if(!wasTop){
  transitionGalleryStage(()=>{changeView();render();}); // State and navigation switch at the invisible midpoint.
 }else{
  changeView();
  if(!tabPages[view].dataset.initialized)renderTabPage(view);
  syncTabPanelAccessibility();
  animateTabTrack(view); // Approved main-tab slide remains untouched.
 }"""
    s=replace_once(s,old_set,new_set)

    # Don't expose the old snapshot mode for other pages; the only use of
    # startViewTransition is inside transitionGalleryPlayer.
    assert s.count('document.startViewTransition(')==1
    assert s.count('function transitionGalleryPlayer(')==1
    assert s.count('function transitionGalleryStage(')==1
    assert 'whEnter();whOpenTitle(r);' not in s
    return s.encode('utf-8')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    b=patch(args.input.read_bytes())
    args.output.parent.mkdir(exist_ok=True,parents=True)
    args.output.write_bytes(b)
    print('Coordinated fade SHA-256:',hashlib.sha256(b).hexdigest(),'bytes:',len(b))

if __name__=='__main__': main()
