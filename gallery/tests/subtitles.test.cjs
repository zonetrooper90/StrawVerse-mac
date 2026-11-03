'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const {toWebVtt,sampleWebVtt,timestamp}=require('../app/subtitles.js');
test('converts Windows SRT with BOM, cue numbers, and decimal commas',()=>{
 const input='\uFEFF1\r\n00:01:12,682 --> 00:01:15,301\r\nHello world\r\n\r\n2\r\n00:01:16,500 --> 00:01:21,000\r\nLine one\r\nLine two\r\n';
 const converted=toWebVtt(input);
 assert.match(converted,/WEBVTT\n\n00:01:12\.682 --> 00:01:15\.301\nHello world/);
 assert.match(converted,/00:01:16\.500 --> 00:01:21\.000\nLine one\nLine two/);
});
test('keeps an existing WebVTT file usable',()=>{
 assert.equal(toWebVtt('WEBVTT\n\n00:00:02.000 --> 00:00:03.000\nHi'), 'WEBVTT\n\n00:00:02.000 --> 00:00:03.000\nHi\n');
});
test('rejects invalid subtitle files',()=>{
 assert.throws(()=>toWebVtt('plain text'),/No usable subtitle cues/);
 assert.throws(()=>toWebVtt('1\n00:00:02,000 --> 00:00:01,000\nBad'),/No usable subtitle cues/);
});
test('sample captions work at the current position and never exceed duration',()=>{
 const vtt=sampleWebVtt(120,47);
 assert.match(vtt,/00:00:46\.000 --> 00:00:52\.400/);
 assert.match(vtt,/two-line subtitle placement/);
 assert.match(sampleWebVtt(4,3),/00:00:00\.000 --> 00:00:04\.000/);
});
test('timestamp emits whole hours, minutes and milliseconds',()=>{
 assert.equal(timestamp(754.682),'00:12:34.682');
});
