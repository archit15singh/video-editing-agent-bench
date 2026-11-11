"""Correct the observed title overlap through the actual MCP interface."""
import json,subprocess,shutil
from bench import ROOT
composition=json.loads((ROOT/'results/makemyclip/media/composition.json').read_text())
title=next(t for t in composition['tracks'] if t['id']=='titles')['clips'][0]
plan=[{'name':'timeline_show','arguments':{}},{'name':'timeline_edit','arguments':{'verbs':[
 {'verb':'remove','clipId':title['id']},{'verb':'add_text','text':'Verified, editable, ready','durationSec':3,'startSec':0,'track':'titles','fontSize':40,'anchor':'top-right','background':'black'}]}},
 {'name':'timeline_export','arguments':{'output':'makemyclip-polished.mp4'}},
 {'name':'timeline_export','arguments':{'output':'makemyclip-final.fcpxml','format':'fcpxml'}}]
p=ROOT/'adapters/makemyclip/polish-current.json';p.write_text(json.dumps(plan,indent=2))
with (ROOT/'results/makemyclip-polish-current.log').open('w') as log:
 subprocess.run(['node',str(ROOT/'scripts/mcp.mjs'),'makemyclip',str(p)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
for f in ['composition.json','composition-ops.json','makemyclip-final.fcpxml']:
 shutil.copy2(ROOT/'results/makemyclip/media'/f,ROOT/'results/makemyclip'/f)
