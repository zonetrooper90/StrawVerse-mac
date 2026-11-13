/* All Gallery split timelines share one rule: the moving 5px gap is ALWAYS
   present. At 0% it occupies the leading edge; at 100%, the trailing edge.
   The completed and remaining segments divide the rest of the track. */
function galleryTimelineFill(percent){
 const amount=Math.max(0,Math.min(100,Number(percent)||0));
 return `calc((100% - var(--gallery-timeline-gap)) * ${(amount/100).toFixed(6)})`;
}
