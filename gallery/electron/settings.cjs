'use strict';
const fs = require('node:fs');
const path = require('node:path');

const DEFAULT_SETTINGS = Object.freeze({
  theme: 'neon',
  defaultPlayback: 'sub',
  defaultDownload: 'sub',
  defaultSubtitles: true,
  playerPreference: 'built-in',
  vlcPath: ''
});
function normalize(candidate) {
  const input = candidate && typeof candidate === 'object' && !Array.isArray(candidate) ? candidate : {};
  return {
    theme: ['neon','midnight','paper'].includes(input.theme) ? input.theme : DEFAULT_SETTINGS.theme,
    defaultPlayback: ['sub','dub'].includes(input.defaultPlayback) ? input.defaultPlayback : DEFAULT_SETTINGS.defaultPlayback,
    defaultDownload: ['sub','dub'].includes(input.defaultDownload) ? input.defaultDownload : DEFAULT_SETTINGS.defaultDownload,
    defaultSubtitles: typeof input.defaultSubtitles === 'boolean' ? input.defaultSubtitles : DEFAULT_SETTINGS.defaultSubtitles,
    playerPreference: ['built-in','vlc'].includes(input.playerPreference) ? input.playerPreference : DEFAULT_SETTINGS.playerPreference,
    vlcPath: typeof input.vlcPath === 'string' && input.vlcPath.length < 1024 ? input.vlcPath : ''
  };
}
function readSettings(filename) {
  try {
    if (fs.statSync(filename).size > 65536) return normalize();
    return normalize(JSON.parse(fs.readFileSync(filename, 'utf8')));
  } catch { return normalize(); }
}
function writeSettings(filename, value) {
  fs.mkdirSync(path.dirname(filename), {recursive: true, mode: 0o700});
  const next = normalize(value);
  const tmp = filename + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(next,null,2)+'\n',{mode:0o600});
  fs.renameSync(tmp,filename);
  return next;
}
module.exports={DEFAULT_SETTINGS,normalize,readSettings,writeSettings};
