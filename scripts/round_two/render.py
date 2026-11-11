#!/usr/bin/env python3
import sys,os,json,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bench import ROOT,run,binary,save
p=argparse.ArgumentParser();p.add_argument('engine',choices=['remotion','hyperframes']);p.add_argument('--stills',action='store_true');p.add_argument('--version',default='first',choices=['first','revised']);a=p.parse_args()
media=ROOT/'results/round-two/media';version=a.version
if a.engine=='remotion':
 if a.stills:
  out=media/'remotion-storyboard';out.mkdir(exist_ok=True)
  for t in [3.2,4.5,7,16.5,18,28.5]:
   run([ROOT/'node_modules/.bin/remotion','still','adapters/round-two/remotion.jsx','RoundTwo',out/f'{t}.png','--public-dir',media,'--frame',round(t*30),'--props',json.dumps({'version':version}),'--log','error'],f'r2-remotion-still-{t}',timeout=120)
 else:run([ROOT/'node_modules/.bin/remotion','render','adapters/round-two/remotion.jsx','RoundTwo',media/f'remotion-{version}-silent.mp4','--public-dir',media,'--props',json.dumps({'version':version}),'--concurrency','2','--log','error'],f'r2-remotion-{version}',timeout=600)
else:
 env={**os.environ,'HYPERFRAMES_NO_TELEMETRY':'1','HYPERFRAMES_FFMPEG_PATH':binary('ffmpeg'),'HYPERFRAMES_FFPROBE_PATH':binary('ffprobe'),'PATH':str(ROOT/'.tools/bin')+':'+os.environ['PATH'],'HYPERFRAMES_BROWSER_PATH':str(ROOT/'node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell')}
 run([ROOT/'node_modules/.bin/hyperframes','render',ROOT/f'adapters/round-two/hyperframes-{version}','--output',media/f'hyperframes-{version}-silent.mp4','--fps','30','--workers','2','--quality','standard'],f'r2-hyperframes-{version}',timeout=600,env=env)
if not a.stills:
 run([binary('ffmpeg'),'-y','-i',media/f'{a.engine}-{version}-silent.mp4','-i',media/'mix.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',media/f'{a.engine}-{version}.mp4'],f'r2-mux-{a.engine}-{version}')
