'use strict';
/* Pure subtitle helpers used by the local-player test and its Node unit tests. */
(function (root) {
  function timestamp(seconds) {
    const ms=Math.max(0,Math.round(seconds*1000));
    const n=Math.floor(ms/1000);
    return String(Math.floor(n/3600)).padStart(2,'0')+':'+
      String(Math.floor(n%3600/60)).padStart(2,'0')+':'+
      String(n%60).padStart(2,'0')+'.'+String(ms%1000).padStart(3,'0');
  }
  function readTimestamp(input) {
    const m=String(input).trim().match(/^(?:(\d{1,3}):)?(\d{1,2}):(\d{2})[,.](\d{1,3})$/);
    if(!m)return null;
    const hours=Number(m[1]||0),minutes=Number(m[2]),seconds=Number(m[3]);
    if(minutes>59||seconds>59)return null;
    return hours*3600+minutes*60+seconds+Number(m[4].padEnd(3,'0'))/1000;
  }
  function toWebVtt(input) {
    if(typeof input!=='string')throw Error('Subtitle content must be text.');
    const text=input.replace(/^\uFEFF/,'').replace(/\r\n?/g,'\n').trim();
    if(/^WEBVTT(?:[ \t][^\n]*)?(?:\n|$)/.test(text))return text+'\n';
    const cues=[];
    for(const block of text.split(/\n[ \t]*\n/)) {
      const lines=block.split('\n');
      const i=lines.findIndex(line=>line.includes('-->'));
      if(i<0)continue;
      const match=lines[i].trim().match(/^(.+?)\s+-->\s+([^\s]+)(?:\s+.*)?$/);
      if(!match)continue;
      const start=readTimestamp(match[1]),end=readTimestamp(match[2]);
      const message=lines.slice(i+1).join('\n').trim();
      if(start===null||end===null||end<=start||!message)continue;
      cues.push(timestamp(start)+' --> '+timestamp(end)+'\n'+message);
    }
    if(!cues.length)throw Error('No usable subtitle cues found. Select a valid .srt or .vtt file.');
    return 'WEBVTT\n\n'+cues.join('\n\n')+'\n';
  }
  function sampleWebVtt(duration,currentTime) {
    if(!Number.isFinite(duration)||duration<=0)throw Error('Load a video before using sample subtitles.');
    const current=Number.isFinite(currentTime)?Math.max(0,currentTime):0;
    const first=Math.max(0,Math.min(Math.floor(current)-1,Math.floor(duration)-6));
    const messages=[
      'The quick brown fox jumps over the lazy dog.',
      'Gallery subtitle test — a second line for spacing.\nThis line checks two-line subtitle placement.',
      'These are sample captions, not dialogue from your video.',
      'Move the pointer to reveal the player controls.'
    ];
    const cues=[];
    for(let i=0;i<messages.length;i++){
      const start=first+i*7;
      const end=Math.min(duration,start+6.4);
      if(end<=start)break;
      cues.push(timestamp(start)+' --> '+timestamp(end)+'\n'+messages[i]);
    }
    if(!cues.length)throw Error('The video is too short for sample subtitles.');
    return 'WEBVTT\n\n'+cues.join('\n\n')+'\n';
  }
  const api=Object.freeze({toWebVtt,sampleWebVtt,timestamp});
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  if(root)root.GallerySubtitles=api;
})(typeof window!=='undefined'?window:null);
