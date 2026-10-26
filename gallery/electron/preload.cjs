'use strict';
const {contextBridge,ipcRenderer}=require('electron');
contextBridge.exposeInMainWorld('galleryDesktop',Object.freeze({
  getSettings:()=>ipcRenderer.invoke('gallery:settings:get'),
  saveSettings:settings=>ipcRenderer.invoke('gallery:settings:save',settings),
  openVideo:()=>ipcRenderer.invoke('gallery:file:pick'),
  locateVLC:()=>ipcRenderer.invoke('gallery:vlc:locate'),
  openInVLC:()=>ipcRenderer.invoke('gallery:vlc:launch')
}));
