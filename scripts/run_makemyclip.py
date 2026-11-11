#!/usr/bin/env python3
import json
import os
import shutil
import time
from bench import ROOT, run, save

manifest=json.loads((ROOT/'fixtures/manifest.json').read_text())
media=ROOT/'results/makemyclip/media';media.mkdir(parents=True,exist_ok=True)
shutil.copy2(ROOT/manifest['source'],media/'source.mp4')
env={**os.environ,'PATH':f'{ROOT}/.tools/bin:'+os.environ['PATH'],
     'MAKEMYCLIP_WORKSPACE':str(media),'MAKEMYCLIP_WHISPER_PATH':str(ROOT/'.tools/whisper.cpp/build/bin/whisper-cli'),
     'MAKEMYCLIP_WHISPER_MODEL':str(ROOT/'.tools/models/ggml-base.en.bin')}
cli=ROOT/'node_modules/.bin/clip'
count=0

def clip(*args):
 global count
 count+=1
 return json.loads(run([cli,'timeline',*args],f'makemyclip-final-{count:02d}-{args[0]}',env=env))

clip('new','--width','1280','--height','720','--fps','30')
for s in manifest['scenes']:
 if s['keep']:
  clip('add-media',str(media/'source.mp4'),str(s['source_start']),str(s['source_end']),'--start',str(s['edit_start']),'--track','picture')
  clip('add-text',s['text'],str(s['duration']),'--start',str(s['edit_start']),'--track','captions','--font','30','--anchor','bottom-center','--background','black')
title=clip('add-text',manifest['title'],'3','--start','0','--track','titles','--font','58','--anchor','top-center','--background','black')
clip('show')
clip('check','--sheet',str(media/'cuts.jpg'))
first=time.monotonic();clip('export',str(media/'makemyclip-first.mp4'));first=time.monotonic()-first
clip('export',str(media/'makemyclip.fcpxml'),'--format','fcpxml')
clip('remove',title['clipId'])
clip('add-text',manifest['revision_title'],'3','--start','0','--track','titles','--font','58','--anchor','top-center','--background','black')
revised=time.monotonic();clip('export',str(media/'makemyclip-revised.mp4'));revised=time.monotonic()-revised
clip('frame','1',str(media/'preview.jpg'))
clip('show')
save('results/makemyclip/timings.json',dict(first_render_seconds=first,revision_render_seconds=revised,cli_calls=count))
