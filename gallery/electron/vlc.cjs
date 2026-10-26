'use strict';
const fs = require('node:fs');
const path = require('node:path');
const {execFile} = require('node:child_process');
const {promisify} = require('node:util');
const execFileAsync=promisify(execFile);

function insideAppPath(input) {
  if(typeof input!=='string'||!path.isAbsolute(input)||!input.endsWith('.app'))return null;
  try {
    const real=fs.realpathSync(input);
    if(!fs.statSync(real).isDirectory())return null;
    return real;
  }catch{return null;}
}
async function infoPlistField(appPath,key) {
  const plist=path.join(appPath,'Contents','Info.plist');
  try {const {stdout}=await execFileAsync('/usr/bin/plutil',['-extract',key,'raw','-o','-',plist],{timeout:1500,maxBuffer:4096});return stdout.trim();}
  catch {return null;}
}
async function validateVLC(appPath) {
  const app=insideAppPath(appPath);if(!app)return null;
  if(process.platform!=='darwin')return null;
  const bundleId=await infoPlistField(app,'CFBundleIdentifier');
  if(bundleId!=='org.videolan.vlc')return null;
  const executableName=await infoPlistField(app,'CFBundleExecutable');
  if(!executableName||!/^[-\w.]+$/.test(executableName))return null;
  const binary=path.join(app,'Contents','MacOS',executableName);
  try {fs.accessSync(binary,fs.constants.X_OK);return {appPath:app,binary};}catch{return null;}
}
async function findVLC(preferred='') {
  const tried=new Set();
  let candidates=[preferred,'/Applications/VLC.app',path.join(process.env.HOME||'','Applications','VLC.app')];
  if(process.platform==='darwin'){
    try {
      // Indexed Spotlight metadata query, not a full filesystem crawl.
      const {stdout}=await execFileAsync('/usr/bin/mdfind',['kMDItemCFBundleIdentifier == "org.videolan.vlc"'],{timeout:2500,maxBuffer:32768});
      candidates.push(...stdout.split(/\r?\n/).filter(Boolean));
    }catch{}
  }
  for(const candidate of candidates){if(!candidate||tried.has(candidate))continue;tried.add(candidate);const result=await validateVLC(candidate);if(result)return result;}
  return null;
}
module.exports={validateVLC,findVLC};
