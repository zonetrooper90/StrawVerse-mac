const SOFT_FUTURISTIC_THEMES=['ocean','twilight','ember','slate','glacier','verdant'];
function readSoftFuturisticTheme(){
 try{const t=localStorage.getItem('gallery.softFuturistic.theme');if(SOFT_FUTURISTIC_THEMES.includes(t))return t;}catch{}
 return 'ocean';
}
const state={playback:null,playbackReturnScroll:0,view:'discover',theme:readSoftFuturisticTheme(),tag:'All Titles',filterStatus:'All',filterAudio:'All',downloadStatus:'All',query:'',tags:['Watching','Downloads','Plan to Watch','Comfort Picks','Weekend Queue'],kind:{'Watching':'system','Downloads':'system','Plan to Watch':'system','Comfort Picks':'custom','Weekend Queue':'custom'},importDoc:null,detailId:null,detailSeason:0,detailEpisode:1,detailReturnHistory:false,detailReturnView:'discover',detailReturnScroll:0,detailAudio:null,detailRelated:null,detailEpisodeFilter:'all',seasonTags:{},defaultPlayback:'sub',defaultDownload:'sub',defaultSubtitles:true,autoplayNextEpisode:readAutoplayNextEpisode()};
