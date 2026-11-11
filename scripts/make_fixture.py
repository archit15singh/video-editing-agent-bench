#!/usr/bin/env python3
"""Create deterministic scenes and native macOS speech, retaining measured timings."""
import json
from pathlib import Path
from bench import ROOT, binary, probe, run, save

OUT=ROOT/'fixtures/generated'
OUT.mkdir(parents=True,exist_ok=True)
SCENES=[
 ('bad', 'red', 'This is the wrong take. Please discard it.', False),
 ('intro', '0x164e63', 'Welcome to the demo. We turn raw recordings into clear stories.', True),
 ('feature', '0x4c1d95', 'First, remove mistakes. Then add titles and readable captions.', True),
 ('close', '0x14532d', 'Finally, verify the export. Every edit should be easy to revise.', True),
]
manifest={'width':1280,'height':720,'fps':30,'scenes':[],'source':'fixtures/generated/source.mp4'}
source_time=0
edit_time=0
for index,(key,color,speech,keep) in enumerate(SCENES):
    aiff=OUT/f'{key}.aiff'
    run(['say','-v','Samantha','-r','175','-o',aiff,speech],f'fixture-speech-{key}')
    seconds=float(probe(aiff)['format']['duration'])
    frames=round((seconds+0.8)*30)
    duration=frames/30
    title=f'{index+1:02d}  {key.upper()}'
    clip=OUT/f'{key}.mp4'
    vf=(f"drawbox=x=80+mod(t*120\\,1000):y=300:w=60:h=60:color=white:t=fill,"
        f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='{title}':fontsize=54:fontcolor=white:x=80:y=80")
    run([binary('ffmpeg'),'-y','-f','lavfi','-i',f'color=c={color}:s=1280x720:r=30',
         '-i',aiff,'-vf',vf,'-af','apad','-t',str(duration),'-c:v','libx264','-preset','fast',
         '-crf','20','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-ac','2',clip],f'fixture-{key}')
    entry=dict(id=key,source_start=source_time,source_end=source_time+duration,
               duration=duration,frames=frames,keep=keep,text=speech,color=color,
               path=str(clip.relative_to(ROOT)),speech_duration=seconds)
    if keep:
        entry['edit_start']=edit_time
        edit_time+=duration
    manifest['scenes'].append(entry)
    source_time+=duration
    if index==1:
        pause=OUT/'pause.mp4'
        run([binary('ffmpeg'),'-y','-f','lavfi','-i','color=c=black:s=1280x720:r=30',
             '-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','2','-c:v','libx264',
             '-pix_fmt','yuv420p','-c:a','aac',pause],'fixture-pause')
        manifest['scenes'].append(dict(id='pause',source_start=source_time,
              source_end=source_time+2,duration=2,frames=60,keep=False,path='fixtures/generated/pause.mp4'))
        source_time+=2
concat=OUT/'concat.txt'
concat.write_text(''.join(f"file '{ROOT/s['path']}'\n" for s in manifest['scenes']))
run([binary('ffmpeg'),'-y','-f','concat','-safe','0','-i',concat,'-c','copy',OUT/'source.mp4'],'fixture-concat')
manifest.update(source_duration=source_time,expected_duration=edit_time,title='From raw to ready',revision_title='Verified, editable, ready')
save('fixtures/manifest.json',manifest)
print(json.dumps(manifest,indent=2))
