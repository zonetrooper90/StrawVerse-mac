'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');const os=require('node:os');const path=require('node:path');
const {normalize,readSettings,writeSettings}=require('../electron/settings.cjs');
test('safe defaults and invalid values',()=>{
 assert.equal(normalize({theme:'invented'}).theme,'neon');
 assert.equal(normalize({defaultPlayback:'dub',defaultDownload:'sub'}).defaultPlayback,'dub');
 assert.equal(normalize({defaultPlayback:'dub',defaultDownload:'sub'}).defaultDownload,'sub');
 assert.equal(normalize({defaultSubtitles:false}).defaultSubtitles,false);
 assert.equal(normalize({playerPreference:'unauthorized'}).playerPreference,'built-in');
});
test('settings are persisted independently of StrawVerse',()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'gallery-020-test-'));
 try{const file=path.join(dir,'settings.json');
  assert.equal(readSettings(file).theme,'neon');
  writeSettings(file,{theme:'paper',defaultPlayback:'dub',defaultDownload:'sub',defaultSubtitles:false,playerPreference:'vlc'});
  assert.deepEqual(readSettings(file),{theme:'paper',defaultPlayback:'dub',defaultDownload:'sub',defaultSubtitles:false,playerPreference:'vlc',vlcPath:''});
  assert.equal(fs.existsSync(file+'.tmp'),false);
 }finally{fs.rmSync(dir,{force:true,recursive:true});}
});
