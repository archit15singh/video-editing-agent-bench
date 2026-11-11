import json,os
from bench import ROOT,run,save
out=ROOT/'results/remotion/media/remotion-warm.mp4'
run([ROOT/'node_modules/.bin/remotion','render','adapters/remotion/index.jsx','Benchmark',out,'--public-dir','fixtures/generated','--props',json.dumps({'title':'Verified, editable, ready'}),'--codec','h264','--concurrency','2','--log','error'],'warm-remotion',timeout=600)
env={**os.environ,'PATH':str(ROOT/'.tools/bin')+':'+os.environ['PATH'],'MAKEMYCLIP_WORKSPACE':str(ROOT/'results/makemyclip/media')}
run([ROOT/'node_modules/.bin/clip','timeline','export',ROOT/'results/makemyclip/media/makemyclip-warm.mp4'],'warm-makemyclip',env=env)
save('results/warm-timings.json',{name:json.loads((ROOT/f'results/logs/warm-{name}.json').read_text())['elapsed_seconds'] for name in ['remotion','makemyclip']})
