'use strict';
const {app,BrowserWindow,dialog,ipcMain,Menu} = require('electron');
const {pathToFileURL} = require('node:url');
const path=require('node:path');
const fs=require('node:fs');
const {spawn}=require('node:child_process');
const {normalize,readSettings,writeSettings}=require('./settings.cjs');
const {validateVLC,findVLC}=require('./vlc.cjs');

// This application is intentionally isolated from StrawVerse Mac's installation
// and userData path. The product name/app ID can be renamed later.
app.setName('Gallery');
let mainWindow=null, currentVideoPath=null, currentSettings=null,settingsPath=null;
app.on('window-all-closed',()=>{if(process.platform!=='darwin')app.quit();});
app.on('activate',()=>{if(BrowserWindow.getAllWindows().length===0)createWindow();});

function assertMainWindow(event){if(!mainWindow || event.sender!==mainWindow.webContents)throw Error('Untrusted renderer');}
function createMenu(){
 const template=[
  {label:app.name,submenu:[{role:'about'},{type:'separator'},{role:'services'},{type:'separator'},{role:'hide'},{role:'hideOthers'},{role:'unhide'},{type:'separator'},{role:'quit'}]},
  {label:'Edit',submenu:[{role:'undo'},{role:'redo'},{type:'separator'},{role:'cut'},{role:'copy'},{role:'paste'},{role:'selectAll'}]},
  {label:'View',submenu:[{role:'togglefullscreen'}]},
  {label:'Window',submenu:[{role:'minimize'},{role:'zoom'},{role:'front'}]}
 ];Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}
function createWindow(){
 mainWindow=new BrowserWindow({
  width:1260,height:870,minWidth:680,minHeight:520,
  title:'Gallery',backgroundColor:'#171221',
  titleBarStyle:process.platform==='darwin'?'hiddenInset':'default',
  show:false,
  webPreferences:{
   preload:path.join(__dirname,'preload.cjs'),
   contextIsolation:true,nodeIntegration:false,sandbox:true,
   webSecurity:true,allowRunningInsecureContent:false
  }
 });
 mainWindow.webContents.setWindowOpenHandler(()=>({action:'deny'}));
 mainWindow.webContents.on('will-navigate',e=>e.preventDefault());
 mainWindow.webContents.on('context-menu',e=>e.preventDefault());
 mainWindow.webContents.on('will-attach-webview',e=>e.preventDefault());
 mainWindow.loadFile(path.join(__dirname,'..','app','index.html'));
 mainWindow.once('ready-to-show',()=>mainWindow?.show());
}
function registerHandlers(){
 ipcMain.handle('gallery:settings:get',event=>{assertMainWindow(event);return currentSettings;});
 ipcMain.handle('gallery:settings:save',(event,prefs)=>{
  assertMainWindow(event);
  const updated=normalize({...currentSettings,...prefs,vlcPath:currentSettings.vlcPath});
  currentSettings=writeSettings(settingsPath,updated);
  return currentSettings;
 });
 ipcMain.handle('gallery:file:pick',async event=>{
  assertMainWindow(event);
  const result=await dialog.showOpenDialog(mainWindow,{
   title:'Open a video file',properties:['openFile'],
   filters:[{name:'Video files',extensions:['mp4','m4v','mov','webm','mkv','ogg','avi']},{name:'All files',extensions:['*']}]
  });
  if(result.canceled||!result.filePaths?.[0])return null;
  const chosen=path.resolve(result.filePaths[0]);
  if(!fs.statSync(chosen).isFile())throw Error('Not a regular file');
  currentVideoPath=chosen;
  return {name:path.basename(chosen),fileURL:pathToFileURL(chosen).href};
 });
 ipcMain.handle('gallery:vlc:locate',async event=>{
  assertMainWindow(event);
  const choice=await dialog.showOpenDialog(mainWindow,{title:'Select VLC.app',message:'Locate your VLC installation',properties:['openFile','openDirectory'],defaultPath:'/Applications'});
  if(choice.canceled||!choice.filePaths?.[0])return {ok:false,message:'No application selected.'};
  const validated=await validateVLC(choice.filePaths[0]);
  if(!validated)return {ok:false,message:'The selected application does not identify as VLC or has no valid executable.'};
  currentSettings=writeSettings(settingsPath,{...currentSettings,vlcPath:validated.appPath});
  return {ok:true,path:validated.appPath};
 });
 ipcMain.handle('gallery:vlc:launch',async event=>{
  assertMainWindow(event);
  if(!currentVideoPath||!fs.existsSync(currentVideoPath))return {ok:false,message:'Choose a local video file first.'};
  const found=await findVLC(currentSettings.vlcPath);
  if(!found)return {ok:false,message:'VLC was not detected.'};
  try {
   const child=spawn(found.binary,[currentVideoPath],{detached:true,stdio:'ignore'});
   await new Promise((resolve,reject)=>{child.once('spawn',resolve);child.once('error',reject);});
   child.unref();return {ok:true};
  }catch(err){return {ok:false,message:'VLC could not be launched: '+String(err.message)};}
 });
}
app.whenReady().then(()=>{
 const userDataDir=path.join(app.getPath('appData'),'GalleryAnime');
 app.setPath('userData',userDataDir);
 settingsPath=path.join(userDataDir,'settings.json');
 currentSettings=readSettings(settingsPath);
 registerHandlers();createMenu();createWindow();
}).catch(error=>{console.error(error);app.quit();});
