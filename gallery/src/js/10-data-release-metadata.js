const seasonStories={
 'demo:01':['A signal after midnight','The distant reply','Orbits and echoes','A quiet visitor','Paper constellations','A light from home','The hidden station','Messages at dawn','Across the signal','A map of stars','The last transmission','First light'],
 'demo:02':['The new constellation','Under the observatory','Through the telescope','Northern horizon','A fragment of light','The second star','Before sunrise']
};
/* Connected records simulate a cached, verified relationship graph.
   Titles and release grouping use genuine naming conventions, but provider episode
   coverage, source matches, tags and progress below are design-only sample data.
   In the real app, IDs are cross-referenced and user corrections are explicit. */
const connectedMetadata={
 'demo:quints':{
   seasons:[
     {id:'quints-s1',label:'Season 1',title:'The Quintessential Quintuplets',seasonNumber:1,total:12,year:'2019',status:'Completed',sub:12,dub:12,sourceMatched:true,watched:4,downloaded:1},
     {id:'quints-s2',label:'Season 2',title:'The Quintessential Quintuplets ∬',seasonNumber:2,total:12,year:'2021',status:'Completed',sub:12,dub:12,sourceMatched:true,watched:0,downloaded:0}
   ],
   related:[
     {id:'quints-movie',title:'The Quintessential Quintuplets Movie',kind:'Movie',year:'2022',note:'The 2022 feature film, shown separately from the numbered TV seasons.',sourceMatched:true,total:1,sub:1,dub:1,status:'Completed',watched:0,downloaded:0},
     {id:'quints-sp-2023',title:'The Quintessential Quintuplets ∽',kind:'Special',year:'2023',note:'2023 special: two episodes, kept separate from the seasons and 2024 special.',sourceMatched:true,total:2,sub:2,dub:2,status:'Completed',watched:0,downloaded:0},
     {id:'quints-sp-2024',title:'The Quintessential Quintuplets ＊',kind:'Special',year:'2024',note:'2024 special: two episodes, kept separate from the 2023 special.',sourceMatched:true,total:2,sub:2,dub:2,status:'Completed',watched:0,downloaded:0}
   ]
 },
 'demo:solo':{
   seasons:[
     {id:'solo-s1',label:'Season 1',title:'Solo Leveling',seasonNumber:1,total:12,year:'2024',status:'Completed',sub:12,dub:12,sourceMatched:true,watched:4,downloaded:1},
     {id:'solo-s2',label:'Season 2',title:'Arise from the Shadow',seasonNumber:2,total:13,year:'2025',status:'Completed',sub:13,dub:9,sourceMatched:true,watched:0,downloaded:0}
   ],related:[]
 },
 'demo:long':{
   seasons:Array.from({length:18},(_,i)=>({id:`long-s${i+1}`,label:`Season ${i+1}`,title:i===0?'The Endless Voyage':i%3===0?`The Endless Voyage: Arc ${i+1}`:`Voyage Arc ${i+1} — ${['Dawn','Eclipse','North Star','Beyond the Horizon'][i%4]}`,seasonNumber:i+1,total:12,year:String(2007+i),status:'Completed',sub:12,dub:i%5===0?0:12,sourceMatched:i!==11,watched:0,downloaded:0})),
   related:[...Array.from({length:5},(_,i)=>({id:`long-m${i+1}`,title:`The Endless Voyage — Feature Film ${i+1}`,kind:'Movie',year:String(2012+i*2),sourceMatched:false,total:1,sub:null,dub:null,status:'Completed',watched:0,downloaded:0})),...Array.from({length:11},(_,i)=>({id:`long-o${i+1}`,title:`Side Story ${i+1}: ${['The First Night','Reunion','Hidden Paths'][i%3]}`,kind:i%2?'OVA':'Special',year:String(2010+i),sourceMatched:false,total:1,sub:null,dub:null,status:'Completed',watched:0,downloaded:0}))]
 },
 'demo:aot':{
   seasons:[
     {id:'aot-s1',label:'Season 1',title:'Attack on Titan',seasonNumber:1,total:25,year:'2013',status:'Completed',sub:25,dub:25,sourceMatched:true,watched:10,downloaded:3},
     {id:'aot-s2',label:'Season 2',title:'Attack on Titan',seasonNumber:2,total:12,year:'2017',status:'Completed',sub:12,dub:12,sourceMatched:true,watched:2,downloaded:0},
{id:'aot-s3',label:'Season 3',title:'Attack on Titan',seasonNumber:3,total:22,year:'2018–2019',status:'Completed',sub:null,dub:null,sourceMatched:false,watched:0,downloaded:0},
     {id:'aot-s4a',label:'Season 4 · Part 1',title:'The Final Season · Part 1',seasonNumber:4,total:16,year:'2020–2021',status:'Completed',sub:16,dub:12,sourceMatched:true,watched:0,downloaded:0},
     {id:'aot-s4b',label:'Season 4 · Part 2',title:'The Final Season · Part 2',seasonNumber:4,total:12,year:'2022',status:'Completed',sub:12,dub:null,sourceMatched:true,watched:0,downloaded:0},
   ],related:[
     {id:'aot-finalchapters',title:'The Final Chapters',kind:'Special',year:'2023',note:'Finale specials · linked, not assigned a new season number',sourceMatched:false,total:2,sub:null,dub:null,watched:0,downloaded:0,status:'Completed'},
     {id:'aot-lastattack',title:'THE LAST ATTACK',kind:'Movie',year:'2024',note:'Film version of the finale · not Season 5',sourceMatched:false,total:1,sub:null,dub:null,watched:0,downloaded:0,status:'Completed'},
     {id:'aot-oad',title:'OAD Archive',kind:'OVA',year:'Various',note:'Original animation releases · separate from numbered seasons',sourceMatched:false,total:8,sub:null,dub:null,watched:0,downloaded:0,status:'Completed'}
   ]
 }
};
