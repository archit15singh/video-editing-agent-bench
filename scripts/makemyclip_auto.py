import json,os,shutil,sys
from bench import ROOT,run,save
media=ROOT/'results/makemyclip-auto/media';media.mkdir(parents=True,exist_ok=True)
shutil.copy2(ROOT/'fixtures/generated/source.mp4',media/'source.mp4')
env={**os.environ,'PATH':str(ROOT/'.tools/bin')+':'+os.environ['PATH'],'MAKEMYCLIP_WORKSPACE':str(media),'MAKEMYCLIP_WHISPER_PATH':str(ROOT/'.tools/whisper.cpp/build/bin/whisper-cli'),'MAKEMYCLIP_WHISPER_MODEL':str(ROOT/'.tools/models/ggml-base.en.bin')}
cli=ROOT/'node_modules/.bin/clip'
def clip(args,name):return json.loads(run([cli,'timeline',*args],name,env=env))
clip(['new','--width','1280','--height','720','--fps','30'],'auto-new')
a=clip(['add-media',str(media/'source.mp4')],'auto-add-media')
save('results/makemyclip-auto/clip.json',a)
t=clip(['transcribe',a['clipId'],'--language','en'],'auto-transcribe')
save('results/makemyclip-auto/transcript.json',t)
s=clip(['silence',a['clipId'],'--dry-run'],'auto-silence-dry-run')
r=clip(['remove-retakes',a['clipId'],'--dry-run'],'auto-retakes-dry-run')
save('results/makemyclip-auto/analysis.json',dict(silence=s,retakes=r))
print(json.dumps(t,indent=2)[:10000])
