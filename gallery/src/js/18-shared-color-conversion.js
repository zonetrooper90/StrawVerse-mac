function galleryHexToHSV(hex){
 const x=hex.replace('#','');const r=parseInt(x.slice(0,2),16)/255,g=parseInt(x.slice(2,4),16)/255,b=parseInt(x.slice(4,6),16)/255;
 const max=Math.max(r,g,b),min=Math.min(r,g,b),delta=max-min;
 let hue=0;
 if(delta){
  if(max===r)hue=((g-b)/delta)%6;
  else if(max===g)hue=(b-r)/delta+2;
  else hue=(r-g)/delta+4;
  hue=(hue*60+360)%360;
 }
 return {h:hue,s:max===0?0:delta/max*100,v:max*100};
}
function galleryHSVToHex(h,s,v){
 const sat=s/100,val=v/100,chroma=val*sat,x=chroma*(1-Math.abs(((h/60)%2)-1)),m=val-chroma;
 let rgb;
 if(h<60)rgb=[chroma,x,0];else if(h<120)rgb=[x,chroma,0];else if(h<180)rgb=[0,chroma,x];
 else if(h<240)rgb=[0,x,chroma];else if(h<300)rgb=[x,0,chroma];else rgb=[chroma,0,x];
 return '#'+rgb.map(n=>Math.round((n+m)*255).toString(16).padStart(2,'0')).join('');
}
