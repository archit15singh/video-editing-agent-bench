#!/usr/bin/env python3
"""Re-transcribe the cleaned single clip to avoid source-boundary caption loss."""
import sys,json,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bench import ROOT,run,save
from media_probe import probe
media=ROOT/'results/round-two/media';workspace=media/'caption-project';workspace.mkdir(exist_ok=True)
env={**os.environ,'PATH':str(ROOT/'.tools/bin')+':'+os.environ['PATH'],'MAKEMYCLIP_WORKSPACE':str(workspace),'MAKEMYCLIP_WHISPER_PATH':str(ROOT/'.tools/whisper.cpp/build/bin/whisper-cli'),'MAKEMYCLIP_WHISPER_MODEL':str(ROOT/'.tools/models/ggml-base.en.bin')}
def clip(args,name):return json.loads(run([ROOT/'node_modules/.bin/clip','timeline',*args],'r2-caption-'+name,env=env))
clip(['new','--width','1280','--height','720','--fps','30'],'new')
a=clip(['add-media',str(media/'clean.mp4')],'add')
t=clip(['transcribe',a['clipId'],'--language','en'],'transcribe');save('results/round-two/clean-word-transcript.json',t)
clip(['captions','--words','7','--font','30','--anchor','bottom-center'],'generate')
# MakeMyClip's clipped transcript dropped the final three words because its
# timestamps exceeded the media duration. Local MLX word alignment retains them.
mlx_path=ROOT/'results/round-two/mlx-clean-transcript.json'
run([ROOT/'.venv/bin/python','-c',"import mlx_whisper,json;from pathlib import Path;r=mlx_whisper.transcribe('results/round-two/media/clean.mp4',path_or_hf_repo='mlx-community/whisper-base.en-mlx',word_timestamps=True,language='en');Path('results/round-two/mlx-clean-transcript.json').write_text(json.dumps(r,indent=2))"],'r2-caption-mlx',env={**env,'HF_HOME':str(ROOT/'.cache/huggingface')})
alignment=json.loads(mlx_path.read_text())
duration=float(probe(media/'clean.mp4')['format']['duration'])
words=[{'text':w['word'].strip(),'startSec':w['start'],'endSec':min(duration,w['end'])} for seg in alignment['segments'] for w in seg['words']]
# Group from cleaned word timings, ensuring <=7 words except a final merged tail.
# This is timing repair, not a supplied reference transcript.
c=[];group=[]
for w in words:
 group.append(w)
 if len(group)>=7 and group[-1]['endSec']-group[0]['startSec']>=1.4:
  c.append({'text':' '.join(x['text'] for x in group),'start':group[0]['startSec'],'end':group[-1]['endSec']});group=[]
if group:
 if c and group[-1]['endSec']-group[0]['startSec']<1.2:
  c[-1]['text']+=' '+' '.join(x['text'] for x in group);c[-1]['end']=group[-1]['endSec']
 else:c.append({'text':' '.join(x['text'] for x in group),'start':group[0]['startSec'],'end':group[-1]['endSec']})
if not (ROOT/'fixtures/round-two/captions-before-repair.json').exists():save('fixtures/round-two/captions-before-repair.json',json.loads((ROOT/'fixtures/round-two/captions.json').read_text()))
save('fixtures/round-two/captions.json',c);save('results/round-two/caption-project.json',json.loads((workspace/'composition.json').read_text()))
print(len(c),'caption groups, minimum duration',min(x['end']-x['start'] for x in c));print(t['text'])
