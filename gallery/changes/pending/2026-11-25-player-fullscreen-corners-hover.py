#!/usr/bin/env python3
"""Approved Gallery fullscreen four-corner hover motion, Version 2.

Scoped to Player fullscreen markup, Player-owned interaction handlers, and
Player-only CSS. The existing publisher exclusively owns generated HTML,
immutable checkpoints, and exact candidate/browser verification. The four
visible SVG paths are byte-for-byte the user's supplied rounded artwork.
"""
import hashlib
from pathlib import Path

def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

EXPECT = {
    'gallery/src/js/11b-player-page.js': 'bdd389447f4a2b0d09bb1f2e3160e7621aeb78a1',
    'gallery/src/js/11h-player-controls.js': 'b5bdbecfac32a57237119087c2f2feab8f46fde5',
    'gallery/src/styles/26-player-icons-and-timelines.css': '318f07fe457f6d6ef9096e7ae40f46d2aee0743d',
}
SVG = '''<svg class="icon g4-fullscreen-svg" width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><g class="g4-fullscreen-piece g4-fullscreen-tl"><path d="M4 8v-2a2 2 0 0 1 2 -2h2"/></g><g class="g4-fullscreen-piece g4-fullscreen-bl"><path d="M4 16v2a2 2 0 0 0 2 2h2"/></g><g class="g4-fullscreen-piece g4-fullscreen-tr"><path d="M16 4h2a2 2 0 0 1 2 2v2"/></g><g class="g4-fullscreen-piece g4-fullscreen-br"><path d="M16 20h2a2 2 0 0 0 2 -2v-2"/></g></svg>'''

JS = ''' const fullscreenButton=document.getElementById('fullscreen');
 // The current Player session owns exactly one icon pose. While hovered or
 // keyboard-focused, capture the direction on entry so click/fullscreenchange
 // cannot reset the four corners. Leaving returns to the actual fullscreen
 // resting pose; browser Escape and external OS exits use the same sync.
 let fullscreenPointerHover=false,fullscreenKeyboardFocus=false;
 let fullscreenPreviewWasActive=false,fullscreenPreviewExpanded=false;
 const refreshFullscreenIcon=()=>{
  if(!owns()||!fullscreenButton)return;
  const active=fullscreenPointerHover||fullscreenKeyboardFocus;
  const isFull=document.fullscreenElement===playerArea;
  if(active&&!fullscreenPreviewWasActive)fullscreenPreviewExpanded=!isFull;
  fullscreenButton.dataset.g4Expanded=String(active?fullscreenPreviewExpanded:isFull);
  fullscreenButton.dataset.g4Fullscreen=String(isFull);
  fullscreenPreviewWasActive=active;
 };
 on(fullscreenButton,'pointerenter',e=>{
  if(e.pointerType==='mouse'||e.pointerType==='pen'){
   fullscreenPointerHover=true;refreshFullscreenIcon();
  }
 });
 on(fullscreenButton,'pointerleave',()=>{
  fullscreenPointerHover=false;refreshFullscreenIcon();
 });
 on(fullscreenButton,'focus',()=>{
  if(fullscreenButton.matches(':focus-visible')){
   fullscreenKeyboardFocus=true;refreshFullscreenIcon();
  }
 });
 on(fullscreenButton,'blur',()=>{
  fullscreenKeyboardFocus=false;refreshFullscreenIcon();
 });
 refreshFullscreenIcon();
'''

CSS = '''
/* Scoped Player fullscreen icon: exact rounded four-corner SVG from the user.
   Windowed hover spreads corners, fullscreen hover contracts them. JS retains
   the current visual target through click/fullscreenchange, including Escape.
   Do not move the button itself or alter the surrounding Player control sizes. */
#fullscreen .g4-fullscreen-svg{display:block;overflow:visible;pointer-events:none}
#fullscreen .g4-fullscreen-piece{
 transform:translate(0,0);
 transition:transform 300ms cubic-bezier(.24,.68,.27,1);
}
#fullscreen[data-g4-expanded="true"] .g4-fullscreen-tl{transform:translate(-1.75px,-1.75px)}
#fullscreen[data-g4-expanded="true"] .g4-fullscreen-tr{transform:translate(1.75px,-1.75px)}
#fullscreen[data-g4-expanded="true"] .g4-fullscreen-bl{transform:translate(-1.75px,1.75px)}
#fullscreen[data-g4-expanded="true"] .g4-fullscreen-br{transform:translate(1.75px,1.75px)}
@media(prefers-reduced-motion:reduce){
 #fullscreen .g4-fullscreen-piece{transition:none!important}
}
'''

def replace_once(original,before,after,path):
    assert original.count(before)==1,(path,'nonunique or missing exact anchor',before[:100])
    return original.replace(before,after,1)

def patch():
    drafts={}
    for path,expected in EXPECT.items():
        raw=Path(path).read_bytes()
        assert blob(raw)==expected,(path,'baseline source drift',blob(raw),expected)
        txt=raw.decode('utf-8')
        if path.endswith('11b-player-page.js'):
            txt=replace_once(txt,"${icon('maximize',21)}",SVG,path)
        elif path.endswith('11h-player-controls.js'):
            txt=replace_once(txt," const playerArea=document.getElementById('player-area');\n",
                             " const playerArea=document.getElementById('player-area');\n"+JS,path)
            txt=replace_once(txt," on(document,'fullscreenchange',playerControlsWake);",
                             " on(document,'fullscreenchange',()=>{playerControlsWake();refreshFullscreenIcon();});",path)
        else:
            assert txt.endswith('\n')
            assert 'g4-fullscreen-' not in txt
            txt+=CSS
        result=txt.encode('utf-8')
        assert raw!=result and len(result)>len(raw),path
        drafts[path]=result
    for path,result in drafts.items():
        Path(path).write_bytes(result)
        assert Path(path).read_bytes()==result,path
        print('APPROVED fullscreen source patch',path,'git-blob',blob(result),flush=True)
    print('Player-only fullscreen corners source complete; publisher owns both generated HTMLs and immutable checkpoint.',flush=True)

if __name__=='__main__':
    patch()
