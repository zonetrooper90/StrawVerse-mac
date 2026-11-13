/* Gallery v100 · Watch History integrated from approved Layout Experiment 03.
 * UI demo records remain clearly labeled samples; local-video playback can additionally
 * produce local browser-preview records. No provider streams are fabricated. */
const whStorageKey='gallery.watchHistory.v100.preview';
function whMakeEpisodes(count, watchedCount=0, partialEpisode=null, partialSeconds=0, duration=1440){
 return Array.from({length:count},(_,i)=>{const n=i+1,watched=n<=watchedCount;return {n,watched,started:watched||n===partialEpisode,progressSeconds:watched?duration:(n===partialEpisode?partialSeconds:0),duration};});
}
const whSeed=[
 {id:'q2',library:true,group:'quints',galleryId:'demo:quints',installmentId:'quints-s2',title:'The Quintessential Quintuplets ∬',short:'Quints ∬',cover:'linear-gradient(145deg,#413759,#7e6694 48%,#cda1ba)',last:'2026-11-04',dates:['2026-11-04','2026-11-03'],episodes:whMakeEpisodes(12,7,8,872)},
 {id:'pkm',library:false,group:'pokemon',galleryId:null,installmentId:'pokemon-ind',title:'Pokémon — Indigo League',short:'Pokémon',cover:'linear-gradient(145deg,#285886,#5c8cc6 52%,#f4c36e)',last:'2026-11-03',dates:['2025-06-21','2026-11-03'],episodes:whMakeEpisodes(100,74,75,608,1320)},
 {id:'frieren',library:true,group:'frieren',galleryId:null,installmentId:'frieren-s1',title:"Frieren: Beyond Journey's End",short:'Frieren',cover:'linear-gradient(147deg,#3f6569,#8cbcb4 48%,#b9bd95)',last:'2026-10-30',dates:['2026-10-30'],episodes:whMakeEpisodes(28,16,17,914)},
 {id:'q1',library:true,group:'quints',galleryId:'demo:quints',installmentId:'quints-s1',title:'The Quintessential Quintuplets',short:'Quints',cover:'linear-gradient(145deg,#533a60,#b67f9b 52%,#ebbaa4)',last:'2026-10-28',dates:['2025-06-19','2026-10-28'],episodes:whMakeEpisodes(12,12)},
 {id:'solo',library:false,group:'solo',galleryId:'demo:solo',installmentId:'solo-s1',title:'Solo Leveling',short:'Solo',cover:'linear-gradient(148deg,#121b36,#49618e 49%,#8b6ab1)',last:'2026-09-12',dates:['2026-09-12'],episodes:whMakeEpisodes(12,8,9,430)},
 {id:'violet',library:true,group:'violet',galleryId:null,installmentId:'violet-s1',title:'Violet Evergarden',short:'Violet',cover:'linear-gradient(145deg,#465b8a,#7b99ba 51%,#cfb69b)',last:'2025-08-20',dates:['2025-08-20'],episodes:whMakeEpisodes(13,13)},
 {id:'moon',library:false,group:'moon',galleryId:'demo:01',installmentId:'moon-s1',title:'Moonlit Signals 2025',short:'Moonlit',cover:'linear-gradient(145deg,#322554,#74548f 51%,#c48b9c)',last:'2026-01-15',dates:['2026-01-15'],episodes:whMakeEpisodes(12,3,4,319)},
 {id:'aot',library:true,group:'aot',galleryId:'demo:aot',installmentId:'aot-final',title:'Attack on Titan: The Final Season',short:'AoT',cover:'linear-gradient(150deg,#334447,#697b77 50%,#958c76)',last:'2025-04-10',dates:['2025-04-10'],episodes:whMakeEpisodes(16,9,10,611)},
 {id:'astra',library:false,group:'astra',galleryId:'demo:02',installmentId:'astra-s1',title:'Astra Afterlight',short:'Astra',cover:'linear-gradient(145deg,#213654,#386e88 50%,#88c2c1)',last:'2024-12-16',dates:['2024-12-16'],episodes:whMakeEpisodes(12,12)}
];
