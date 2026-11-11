#!/usr/bin/env python3
import sys,json,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bench import ROOT,run,save
from media_probe import probe
media=ROOT/'results/round-two/media';work=media/'makemyclip';work.mkdir(exist_ok=True)
env={**os.environ,'MAKEMYCLIP_WORKSPACE':str(work),'MAKEMYCLIP_WHISPER_PATH':str(ROOT/'.tools/whisper.cpp/build/bin/whisper-cli'),'MAKEMYCLIP_WHISPER_MODEL':str(ROOT/'.tools/models/ggml-base.en.bin'),'PATH':str(ROOT/'.tools/bin')+':'+os.environ['PATH']}
cli=ROOT/'node_modules/.bin/clip'
def clip(args,name):return json.loads(run([cli,'timeline',*args],'r2-cleanup-'+name,env=env))
clip(['new','--width','1280','--height','720','--fps','30'],'new')
added=clip(['add-media',str(media/'source.mp4')],'add');ident=added['clipId']
t=clip(['transcribe',ident,'--language','en'],'transcribe');save('results/round-two/raw-transcript.json',t)
# Detect the narrated rejection through observed ASR words, not fixture times.
words=t['words'];end=next(i for i,w in enumerate(words) if w['text'].lower().strip('.,')=='sentence')
clip(['cut-words',ident,'0',str(end)],'reject')
state=clip(['show'],'state')
for track in state['tracks']:
 for c in track['clips']:
  if c['kind']=='media':clip(['silence',c['id']],'silence-'+c['id'])
# Export the cleaned recording before captions, so both final renderers share it.
clip(['export',str(media/'clean.mp4')],'export')
clip(['captions','--words','5','--font','30','--anchor','bottom-center'],'captions')
clip(['export',str(media/'cleanup-captions.mp4')],'caption-export')
composition=json.loads((work/'composition.json').read_text());save('results/round-two/cleanup-project.json',composition)
state=clip(['show'],'final-state');save('results/round-two/cleanup-state.json',state)
captions=[]
for tr in composition['tracks']:
 for c in tr['clips']:
  if c['kind']=='text':captions.append({'text':c['text'],'start':c['startSec'],'end':c['startSec']+c['durationSec']})
save('fixtures/round-two/captions.json',captions)
print('Clean duration:',probe(media/'clean.mp4')['format']['duration'],'captions:',len(captions))
