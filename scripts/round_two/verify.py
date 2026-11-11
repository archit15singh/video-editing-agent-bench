#!/usr/bin/env python3
import sys,json,subprocess,re,hashlib,array,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bench import ROOT,run,binary,save
from media_probe import probe
media=ROOT/'results/round-two/media';config=json.loads((ROOT/'fixtures/round-two/composition.json').read_text())

def frame(path,time,crop=None):
 args=[binary('ffmpeg'),'-v','error','-ss',str(time),'-i',path,'-frames:v','1']
 if crop:args+=['-vf',crop]
 return subprocess.check_output([str(x) for x in args+['-pix_fmt','rgb24','-f','rawvideo','-']])

def speech():
 run([binary('ffmpeg'),'-y','-i',media/'clean.mp4','-ar','16000','-ac','1',media/'verify.wav'],'r2-verify-extract')
 prefix=ROOT/'results/round-two/clean-asr'
 run([ROOT/'.tools/whisper.cpp/build/bin/whisper-cli','-m',ROOT/'.tools/models/ggml-base.en.bin','-f',media/'verify.wav','-oj','-of',prefix],'r2-verify-asr')
 recognized=' '.join(s['text'].strip() for s in json.loads(prefix.with_suffix('.json').read_text())['transcription'])
 expected=' '.join(s['text'] for s in json.loads((ROOT/'fixtures/round-two/manifest.json').read_text())['scenes'] if s['keep'])
 norm=lambda s:re.findall('[a-z]+',s.lower());a,b=norm(expected),norm(recognized);prev=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  curr=[i]
  for j,y in enumerate(b,1):curr.append(min(curr[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
  prev=curr
 return {'expected':expected,'recognized':recognized,'wer':prev[-1]/len(a),'rejected_take_absent':'rejected take' not in recognized.lower()}

if __name__=='__main__':
 reports={};audio_hashes=[]
 for engine in ['remotion','hyperframes']:
  versions={}
  for version,color in [('first',(37,185,165)),('revised',(242,125,98))]:
   name=f'{engine}-{version}';path=media/f'{name}.mp4';info=probe(path);v=next(s for s in info['streams'] if s['codec_type']=='video')
   run([binary('ffmpeg'),'-v','error','-i',path,'-f','null','-'],f'r2-decode-{name}')
   rgb=list(frame(path,1,'crop=2:2:56:50,scale=1:1')[:3]);accent=max(abs(x-y) for x,y in zip(rgb,color))<20
   pcm=subprocess.check_output([binary('ffmpeg'),'-v','error','-i',str(path),'-vn','-f','s16le','-ac','1','-ar','48000','-']);h=hashlib.sha256(pcm).hexdigest();audio_hashes.append(h)
   stilldir=media/'verification'/name;stilldir.mkdir(parents=True,exist_ok=True)
   for t in [0.1,3.2,4.5,7,9.1,12.19,12.29,15.2,18,21.1,24.11,24.22,27.2,28.5,33.1,38]:
    run([binary('ffmpeg'),'-y','-ss',t,'-i',path,'-frames:v','1',stilldir/f'{t}.png'],f'r2-frame-{name}-{t}')
   versions[version]={'dimensions':v['width']==1280 and v['height']==720,'fps':v['r_frame_rate']=='30/1','duration':abs(float(info['format']['duration'])-config['duration'])<.1,'full_decode':True,'audio_present':any(s['codec_type']=='audio' for s in info['streams']),'brand_rgb':rgb,'accent_pass':accent,'audio_pcm_sha256':h}
  # Same source pixels/captions must survive rebranding; compare decoded crops.
  unchanged=[]
  for t in [1,4.5,16.5,28.5,36]:
   for region in ['crop=300:360:60:170','crop=1024:70:128:615']:
    a=frame(media/f'{engine}-first.mp4',t,region);b=frame(media/f'{engine}-revised.mp4',t,region)
    mae=sum(abs(x-y) for x,y in zip(a,b))/len(a);unchanged.append({'time':t,'region':region,'mae':mae,'pass':mae<2})
  reports[engine]={'versions':versions,'revision_preserves_picture_and_captions':unchanged}
 speech_report=speech()
 # Audio hashes across four exports prove the actual encoded speech/music/effects mix is unchanged.
 report={'negative_control_wrong_brand_rejected':all(max(abs(x-y) for x,y in zip(e['versions']['first']['brand_rgb'],(242,125,98)))>=20 for e in reports.values()),'engines':reports,'shared_audio_identical':len(set(audio_hashes))==1,'speech':speech_report}
 report['passed']=report['negative_control_wrong_brand_rejected'] and report['shared_audio_identical'] and speech_report['wer']<.08 and speech_report['rejected_take_absent'] and all(all(v[k] for k in ['dimensions','fps','duration','full_decode','audio_present','accent_pass']) for e in reports.values() for v in e['versions'].values()) and all(x['pass'] for e in reports.values() for x in e['revision_preserves_picture_and_captions'])
 save('results/round-two/verification.json',report);print(json.dumps(report,indent=2));raise SystemExit(0 if report['passed'] else 1)
