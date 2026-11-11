import json,os
from bench import ROOT,run,save
media=ROOT/'results/makemyclip-auto/media'
env={**os.environ,'PATH':str(ROOT/'.tools/bin')+':'+os.environ['PATH'],'MAKEMYCLIP_WORKSPACE':str(media),'MAKEMYCLIP_WHISPER_PATH':str(ROOT/'.tools/whisper.cpp/build/bin/whisper-cli'),'MAKEMYCLIP_WHISPER_MODEL':str(ROOT/'.tools/models/ggml-base.en.bin')}
cli=ROOT/'node_modules/.bin/clip'
def clip(args,name):return json.loads(run([cli,'timeline',*args],name,env=env))
first=json.loads((ROOT/'results/makemyclip-auto/clip.json').read_text())['clipId']
# Agent decision from observed transcript: reject words 0..7, explicit bad-take instruction.
clip(['cut-words',first,'0','7'],'auto-cut-bad-take')
show=clip(['show'],'auto-show-after-words')
for track in show['tracks']:
 for item in track['clips']:
  if item['kind']=='media':clip(['silence',item['id']],'auto-silence-'+item['id'])
clip(['captions','--words','5','--font','36','--anchor','bottom-center'],'auto-captions')
clip(['check','--sheet',str(media/'cuts.jpg')],'auto-check')
clip(['export',str(media/'makemyclip-auto.mp4')],'auto-export')
clip(['show'],'auto-final-state')
