#!/usr/bin/env python3
import sys,json,math,wave,struct,html
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bench import ROOT,run,binary,save
from media_probe import probe
OUT=ROOT/'results/round-two/media';OUT.mkdir(parents=True,exist_ok=True)
texts=[
('reject','This is a rejected take. Please discard this sentence.',False),
('organize','A useful video starts with a clear story. Frame Lab brings your recordings, notes, and screenshots into one place. Start by organizing the material you actually need, so every scene has a purpose.',True),
('review','Next, review the cut. Remove the mistakes and long pauses, then check the words that remain. Give each visual one job. Highlight a decision, explain a change, or show the product in action.',True),
('deliver','Finally, deliver a video that is easy to revise. Keep the narration clear, the captions readable, and the graphics consistent. When your brand changes, update the design without rebuilding the story. That is the workflow we are testing today.',True)]
manifest={'provenance':'synthetic','fps':30,'width':1280,'height':720,'scenes':[]}
cursor=0
for name,text,keep in texts:
 speech=OUT/f'{name}.aiff';run(['say','-v','Samantha','-r','166','-o',speech,text],f'r2-speech-{name}')
 seconds=float(probe(speech)['format']['duration']);duration=math.ceil((seconds+0.8)*30)/30
 # The raw source is a narrated demonstration, not a simulated human face.
 vf=f"drawtext=fontfile=/System/Library/Fonts/Georgia.ttf:text='{name.upper()}':fontcolor=white:fontsize=48:x=70:y=80,drawbox=x=70+mod(t*80\\,950):y=300:w=40:h=6:color=0x25b9a5:t=fill"
 target=OUT/f'raw-{name}.mp4'
 run([binary('ffmpeg'),'-y','-f','lavfi','-i','color=c=0x17252c:s=1280x720:r=30','-i',speech,'-vf',vf,'-af','apad','-t',duration,'-c:v','libx264','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-ar','48000',target],f'r2-scene-{name}')
 manifest['scenes'].append({'id':name,'text':text,'keep':keep,'start':cursor,'end':cursor+duration,'duration':duration,'path':str(target.relative_to(ROOT))});cursor+=duration
 if name=='organize':
  pause=OUT/'pause.mp4';run([binary('ffmpeg'),'-y','-f','lavfi','-i','color=c=0x17252c:s=1280x720:r=30','-f','lavfi','-i','anullsrc=r=48000:cl=mono','-t','1.6','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',pause],'r2-pause')
  manifest['scenes'].append({'id':'pause','keep':False,'start':cursor,'end':cursor+1.6,'duration':1.6,'path':str(pause.relative_to(ROOT))});cursor+=1.6
concat=OUT/'source-concat.txt';concat.write_text(''.join(f"file '{ROOT/s['path']}'\n" for s in manifest['scenes']))
run([binary('ffmpeg'),'-y','-f','concat','-safe','0','-i',concat,'-c','copy',OUT/'source.mp4'],'r2-source')
manifest['duration']=float(probe(OUT/'source.mp4')['format']['duration']);save('fixtures/round-two/manifest.json',manifest)
print('Source duration:',manifest['duration'])
# Original deterministic musical bed and short rising effects, no licensed samples.
rate=48000;length=65
for kind in ['music','effect']:
 seconds=length if kind=='music' else .35
 with wave.open(str(OUT/f'{kind}.wav'),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
  samples=[]
  for n in range(int(seconds*rate)):
   t=n/rate
   if kind=='music':
    notes=[130.8128,164.8138,195.9977,164.8138];hz=notes[int(t/2)%4];envelope=min(1,t/2,(seconds-t)/2);value=.055*envelope*(math.sin(2*math.pi*hz*t)+.4*math.sin(2*math.pi*hz*2*t))
   else:value=.14*math.sin(math.pi*t/seconds)**2*math.sin(2*math.pi*(420*t+1000*t*t))
   samples.append(struct.pack('<h',int(max(-1,min(1,value))*32767)))
  f.writeframes(b''.join(samples))
# Code-native product UI screens, not externally sourced screenshots.
for version,brand,accent in [('first','FrameLab','#25b9a5'),('revised','SignalCut','#f27d62')]:
 for i,title in enumerate(['Organize your material','Review every decision','Ready for delivery']):
  rows=''
  for j,(label,status) in enumerate([('Product overview','Ready'),('Workflow walkthrough','Reviewed'),('Launch sequence','Approved')]):
   y=245+j*100;rows+=f'<rect x="240" y="{y}" width="870" height="80" rx="10" fill="#202e35"/><text x="265" y="{y+32}" fill="#ecf0ed" font-size="23">{label}</text><text x="265" y="{y+60}" fill="#99a9ad" font-size="16">DEMO PROJECT / SCENE 0{j+1}</text><text x="965" y="{y+47}" fill="{accent}" font-size="19">{status}</text>'
  svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700"><rect width="1200" height="700" fill="#101b21"/><rect width="195" height="700" fill="#18272e"/><rect x="30" y="40" width="32" height="32" rx="8" fill="{accent}"/><text x="77" y="65" fill="white" font-family="Georgia" font-size="24">{brand}</text><g font-family="Helvetica"><text x="30" y="150" fill="{accent}" font-size="18">Workspace</text><text x="30" y="205" fill="#99a9ad" font-size="18">Library</text><text x="30" y="260" fill="#99a9ad" font-size="18">Review</text><text x="240" y="75" fill="#99a9ad" font-size="16">FICTITIOUS PRODUCT / LOCAL DEMO</text><text x="240" y="135" fill="white" font-size="37">{title}</text><text x="240" y="185" fill="#99a9ad" font-size="20">One story. Clear decisions. Editable output.</text>{rows}<text x="240" y="625" fill="{accent}" font-size="19">{['3 scenes organized','All decisions checked','100% ready'][i]}</text></g></svg>'''
  (OUT/f'{version}-screen-{i}.svg').write_text(svg)
