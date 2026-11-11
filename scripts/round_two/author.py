#!/usr/bin/env python3
import sys,json,shutil,html
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bench import ROOT,save,run,binary
from media_probe import probe
media=ROOT/'results/round-two/media';duration=float(probe(media/'clean.mp4')['format']['duration'])
captions=json.loads((ROOT/'fixtures/round-two/captions.json').read_text())
config={'duration':duration,'frames':round(duration*30),'beats':[3,15,27],'titles':['Organize your material','Review every decision','Ready for delivery'],'captions':captions}
save('fixtures/round-two/composition.json',config)
# One original audio mix used verbatim for all renderer/revision outputs.
filters=['[0:a]volume=1[voice]','[1:a]volume=0.22,afade=t=in:d=1,afade=t=out:st='+str(duration-1)+':d=1[bed]']
for i,beat in enumerate(config['beats']):filters.append(f'[{i+2}:a]volume=0.35,adelay={round((beat+.5)*1000)}:all=1[fx{i}]')
filters.append('[voice][bed][fx0][fx1][fx2]amix=inputs=5:duration=first:normalize=0,alimiter=limit=0.95:level=0[mix]')
args=[binary('ffmpeg'),'-y','-i',media/'clean.mp4','-i',media/'music.wav']
for _ in range(3):args+=['-i',media/'effect.wav']
run([*args,'-filter_complex',';'.join(filters),'-map','[mix]','-ar','48000',media/'mix.wav'],'r2-audio-mix')
for version,brand,accent in [('first','FrameLab','#25b9a5'),('revised','SignalCut','#f27d62')]:
 out=ROOT/f'adapters/round-two/hyperframes-{version}';assets=out/'assets';assets.mkdir(parents=True,exist_ok=True)
 for f in ['clean.mp4',*[f'{version}-screen-{i}.png' for i in range(3)]]:shutil.copy2(media/f,assets/f)
 shutil.copy2(ROOT/'node_modules/gsap/dist/gsap.min.js',assets/'gsap.min.js')
 for name in ['Georgia.ttf','Arial.ttf']:shutil.copyfile('/System/Library/Fonts/Supplemental/'+name,assets/name)
 body=f'<header class="brand" style="position:absolute;left:52px;top:34px"><b class="mark">{brand[0]}</b>{brand}<span>STORY → SCREEN → DELIVERY</span></header><h1 data-layout-allow-occlusion>Make the story<br>easy to follow.</h1><p class="sub" data-layout-allow-occlusion>A reproducible editing experiment.<br>Fictitious product. Real pipeline.</p>'
 body+=f'<video id="narration-picture" class="clip source" data-start="0" data-duration="{duration}" data-track-index="0" src="assets/clean.mp4" muted playsinline></video>'
 animations=[]
 for i,beat in enumerate(config['beats']):
  body+=f'<section id="plate-{i}" class="clip plate" data-start="{beat}" data-duration="6" data-track-index="{i+1}"><div class="moving" id="moving-{i}"><img src="assets/{version}-screen-{i}.png"/><div class="focus" id="focus-{i}"></div></div><div class="label" id="label-{i}">0{i+1} / {config["titles"][i]}</div><div class="bars" id="bars-{i}"><i></i><i></i><i></i></div></section>'
  animations += [f'tl.fromTo("#moving-{i}",{{scale:.94,x:0,opacity:0}},{{scale:1,x:0,opacity:1,duration:.5,ease:"power3.out"}},{beat});',f'tl.fromTo("#focus-{i}",{{opacity:0}},{{opacity:1,duration:.4}},{beat+.5});',f'tl.fromTo("#label-{i}",{{y:20,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"power3.out"}},{beat+.2});',f'tl.fromTo("#bars-{i} i",{{scaleX:0}},{{scaleX:1,duration:.8,stagger:.2,ease:"power2.out"}},{beat+1});']
 animations += ['tl.to("#focus-0",{y:66,duration:.4,ease:"power2.inOut"},5);','tl.to("#focus-0",{y:133,duration:.4,ease:"power2.inOut"},6.5);','tl.to("#moving-1",{scale:1.04,x:-16,duration:2,ease:"power2.inOut"},16.5);']
 for i,c in enumerate(captions):body+=f'<div id="caption-{i}" class="clip caption" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]}" data-track-index="8">{html.escape(c["text"])}</div>'
 css=f'''@font-face{{font-family:R2Serif;src:url(assets/Georgia.ttf)}}@font-face{{font-family:R2Sans;src:url(assets/Arial.ttf)}}*{{box-sizing:border-box}}body{{margin:0;background:#0d161c;color:#edf0eb;font-family:R2Sans}}#root{{position:relative;width:1280px;height:720px;overflow:hidden;background:#0d161c}}.brand{{position:absolute;left:52px;top:34px;font-family:R2Serif;font-size:27px;display:flex;align-items:center;gap:12px}}.mark{{background:{accent};color:#0d161c;padding:5px 12px;border-radius:8px}}.brand span{{font:19px R2Sans;letter-spacing:2px;color:#91a3a8;margin-left:260px}}h1{{position:absolute;left:440px;top:180px;font:62px/1.1 R2Serif;margin:0}}.sub{{position:absolute;left:444px;top:345px;color:#91a3a8;font-size:23px;line-height:1.6}}.source{{position:absolute;left:52px;top:160px;width:340px;height:380px;object-fit:cover;object-position:left center;border:1px solid #34434a;border-radius:14px}}.plate{{position:absolute;left:425px;top:145px;width:800px;height:450px;background:#0d161c;z-index:2}}.moving{{position:absolute;inset:0;transform-origin:50% 50%}}.moving img{{width:800px;height:467px;border:1px solid #34434a;border-radius:12px}}.focus{{position:absolute;left:158px;top:162px;width:580px;height:55px;border:3px solid {accent};border-radius:8px}}.label{{position:absolute;left:0;top:-45px;font:24px R2Serif;color:{accent}}}.bars{{position:absolute;left:162px;top:370px;display:flex;gap:12px}}.bars i{{width:90px;height:8px;background:{accent};transform-origin:left}}.bars i:nth-child(2){{width:150px}}.bars i:nth-child(3){{width:210px}}.caption{{position:absolute;z-index:20;bottom:38px;left:128px;width:1024px;text-align:center;font-size:30px;font-weight:500;background:#080d11;padding:13px 20px;border-radius:8px}}'''
 doc=f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div id="root" data-composition-id="main" data-width="1280" data-height="720" data-start="0" data-duration="{duration}">{body}</div><script src="assets/gsap.min.js"></script><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});'+''.join(animations)+'window.__timelines.main=tl;</script></body></html>'
 (out/'index.html').write_text(doc)
print('Authored HyperFrames projects; duration',duration)
