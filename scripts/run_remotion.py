#!/usr/bin/env python3
import json
from pathlib import Path
from bench import ROOT, run, save
manifest=json.loads((ROOT/'fixtures/manifest.json').read_text())
out=ROOT/'results/remotion/media';out.mkdir(parents=True,exist_ok=True)
cli=ROOT/'node_modules/.bin/remotion'
base=[cli,'render','adapters/remotion/index.jsx','Benchmark']
metrics={}
for version,title in [('first',manifest['title']),('revised',manifest['revision_title'])]:
 name=f'remotion-{version}'
 run([*base,out/f'{name}.mp4','--public-dir','fixtures/generated','--props',json.dumps({'title':title}),
      '--codec','h264','--concurrency','2','--log','error'],name,timeout=600)
 metrics[version]=json.loads((ROOT/f'results/logs/{name}.json').read_text())['elapsed_seconds']
run([cli,'still','adapters/remotion/index.jsx','Benchmark',out/'preview.jpg','--public-dir','fixtures/generated',
     '--frame','30','--props',json.dumps({'title':manifest['revision_title']})],'remotion-preview',timeout=120)
save('results/remotion/timings.json',metrics)
