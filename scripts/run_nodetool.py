#!/usr/bin/env python3
"""Repeat the headless MCP trial with fresh assets/timeline IDs on every run."""
import json,subprocess
from pathlib import Path
from bench import ROOT,save

def mcp(plan,name):
 p=ROOT/f'adapters/nodetool/{name}.json';p.write_text(json.dumps(plan,indent=2))
 out=ROOT/f'results/nodetool-{name}.log'
 with out.open('w') as log:
  subprocess.run(['node',str(ROOT/'scripts/mcp.mjs'),'nodetool',str(p)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
 records=json.loads((ROOT/f'results/nodetool/mcp-run-{name}.json').read_text())
 return records

upload=mcp([{'name':'upload_asset','arguments':{'file_path':str(ROOT/'fixtures/generated/source.mp4'),'name':'benchmark-source.mp4','content_type':'video/mp4'}}],'repeat-upload')
value=upload[0]['result'].get('structuredContent') or json.loads(upload[0]['result']['content'][0]['text'])
asset=value['asset_uri']
manifest=json.loads((ROOT/'fixtures/manifest.json').read_text());kept=[s for s in manifest['scenes'] if s['keep']]
code='''import {create_timeline,get_timeline,edit_timeline,validate_timeline,preview_timeline_frame,render_timeline,create_timeline_version} from "@nodetool-ai/sandbox-nodetool/timelines";
const made=await create_timeline({name:"Reproducible synthetic comparison",width:1280,height:720,fps:30});const id=made.timeline_id;
await get_timeline({timeline_id:id});await edit_timeline({timeline_id:id,ops:[{op:"add_track",type:"overlay",name:"Titles"},{op:"add_track",type:"overlay",name:"Caption overlays"},{op:"add_track",type:"video",name:"Picture"}]});
const state=await get_timeline({timeline_id:id});const track=n=>state.timeline.tracks.find(t=>t.name===n).id;
const ops=[{op:"add_text_clip",trackId:track("Titles"),name:"Title",text:"From raw to ready",startMs:0,durationMs:3000,fontSizePx:58,color:"#ffffff",background:{color:"#000000",paddingPx:14,radiusPx:8},transform:{position:{x:0,y:-160}}}];
for(const s of SCENES){ops.push({op:"add_text_clip",trackId:track("Caption overlays"),name:"Caption "+s.id,text:s.text,startMs:Math.round(s.edit_start*1000),durationMs:Math.round(s.duration*1000),fontSizePx:30,color:"#ffffff",background:{color:"#000000",paddingPx:16,radiusPx:8},transform:{position:{x:0,y:270}}});ops.push({op:"add_media_clip",trackId:track("Picture"),asset:ASSET,name:s.id,startMs:Math.round(s.edit_start*1000),durationMs:Math.round(s.duration*1000)});ops.push({op:"trim_clip",target:s.id,inPointMs:Math.round(s.source_start*1000),outPointMs:Math.round(s.source_end*1000),durationMs:Math.round(s.duration*1000)});}
await edit_timeline({timeline_id:id,ops});const validation=await validate_timeline({timeline_id:id});const first=await render_timeline({timeline_id:id,wait:true,timeout_ms:120000});
await create_timeline_version({timeline_id:id,name:"Before title revision"});await get_timeline({timeline_id:id});await edit_timeline({timeline_id:id,ops:[{op:"set_clip_params",target:"Title",textStyle:{text:"Verified, editable, ready"}}]});
const preview=await preview_timeline_frame({timeline_id:id,times_ms:[1000,6500,12000],sheet:true,width:640});const finalState=await get_timeline({timeline_id:id});const second=await render_timeline({timeline_id:id,wait:true,timeout_ms:120000});return {id,validation,first,second,preview,finalState};'''.replace('SCENES',json.dumps(kept)).replace('ASSET',json.dumps(asset))
records=mcp([{'name':'execute_code','arguments':{'title':'Run reproducible editing and revision','risk':'low','description':'','code':code}}],'repeat-trial')
result=json.loads(records[0]['result']['content'][0]['text'])
save('results/nodetool/repeat-trial-summary.json',result)
print(json.dumps(result.get('result',{}).get('second',result),indent=2))

trial=result.get("result",{})
raise SystemExit(0 if trial.get("first",{}).get("status")=="completed" and trial.get("second",{}).get("status")=="completed" else 2)
