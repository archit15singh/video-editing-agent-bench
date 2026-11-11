import json,re,time
from bench import ROOT,run,binary,save
manifest=json.loads((ROOT/'fixtures/manifest.json').read_text())
expected=' '.join(s['text'] for s in manifest['scenes'] if s['keep'])
normalize=lambda s:re.findall(r'[a-z]+',s.lower())
def distance(a,b):
 prev=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  curr=[i]
  for j,y in enumerate(b,1):curr.append(min(curr[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
  prev=curr
 return prev[-1]
reports=[]
for name,path in [('remotion','results/remotion/media/remotion-revised.mp4'),('makemyclip','results/makemyclip/media/makemyclip-polished.mp4'),('makemyclip-auto','results/makemyclip-auto/media/makemyclip-auto.mp4')]:
 wav=ROOT/f'results/asr/media/{name}.wav';prefix=ROOT/f'results/asr/{name}'
 run([binary('ffmpeg'),'-y','-i',ROOT/path,'-ar','16000','-ac','1',wav],f'speech-extract-{name}')
 run([ROOT/'.tools/whisper.cpp/build/bin/whisper-cli','-m',ROOT/'.tools/models/ggml-base.en.bin','-f',wav,'-oj','-of',prefix],f'speech-asr-{name}')
 d=json.loads(prefix.with_suffix('.json').read_text());text=' '.join(s['text'].strip() for s in d['transcription']);wer=distance(normalize(expected),normalize(text))/len(normalize(expected))
 reports.append(dict(name=name,expected=expected,recognized=text,word_error_rate=wer,bad_take_present='wrong take' in text.lower(),content_coverage_pass=wer<0.1 and 'wrong take' not in text.lower()))
save('results/verification/speech.json',reports)
print(json.dumps(reports,indent=2))
