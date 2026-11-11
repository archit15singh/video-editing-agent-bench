#!/usr/bin/env python3
import json
from bench import ROOT,binary,run,save
m=json.loads((ROOT/'fixtures/manifest.json').read_text());scenes=[s for s in m['scenes'] if s['keep']]
parts=[]
for i,s in enumerate(scenes):
 parts.extend([f"[0:v]trim=start={s['source_start']}:end={s['source_end']},setpts=PTS-STARTPTS[v{i}]",f"[0:a]atrim=start={s['source_start']}:end={s['source_end']},asetpts=PTS-STARTPTS[a{i}]"])
parts.append(''.join(f'[v{i}][a{i}]' for i in range(len(scenes)))+f'concat=n={len(scenes)}:v=1:a=1[v][a]')
filters=[]
for s in scenes:
 filters.append(f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='{s['text']}':fontsize=30:fontcolor=white:box=1:boxcolor=black:x=(w-tw)/2:y=h-th-40:enable='between(t,{s['edit_start']},{s['edit_start']+s['duration']})'")
filters.append("drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='Verified, editable, ready':fontsize=40:fontcolor=white:x=w-tw-30:y=30:enable='lt(t,3)'")
parts.append('[v]'+','.join(filters)+'[out]')
out=ROOT/'results/ffmpeg-control/media';out.mkdir(parents=True,exist_ok=True)
run([binary('ffmpeg'),'-y','-i',ROOT/'fixtures/generated/source.mp4','-filter_complex',';'.join(parts),'-map','[out]','-map','[a]','-r','30','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac',out/'ffmpeg-control.mp4'],'ffmpeg-control')
