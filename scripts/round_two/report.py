#!/usr/bin/env python3
import sys,json,base64,html,hashlib,mimetypes
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from bench import ROOT,save
media=ROOT/'results/round-two/media'
v=json.loads((ROOT/'results/round-two/verification.json').read_text())
if not v['passed']:raise SystemExit('Verification failed: report requires inspection before finalizing.')
times={e:{version:json.loads((ROOT/f'results/logs/r2-{e}-{version}.json').read_text())['elapsed_seconds'] for version in ['first','revised']} for e in ['remotion','hyperframes']}
manifest=json.loads((ROOT/'fixtures/round-two/manifest.json').read_text())
text=f'''# Round two: a complete narrated-demo pipeline

Measured on12 November2026. Public repository: https://github.com/archit15singh/video-editing-agent-bench

## Result

Both MakeMyClip → Remotion → FFmpeg and MakeMyClip → HyperFrames → FFmpeg exported first and rebranded videos. The46.921-second synthetic narrated recording became a38.400-second cleaned edit. Each implementation uses the same three fictitious product screenshots, three6-second graphics sequences, repaired captions, original music and effects. Source code, rendered review frames, raw logs and verification are retained.

**Practical ranking for this run:1 Remotion,2 HyperFrames. Visual result: effectively tied for this modest design.** Remotion required fewer renderer-specific repairs and retained explicit frame-driven React code. HyperFrames delivered the same visual idea with editable HTML/GSAP and stronger built-in layout/contrast diagnostics, but needed explicit FFmpeg paths and a header positioning repair. This is a workflow ranking by one operator, not intrinsic model or aesthetic superiority. MakeMyClip remains the shared cleanup component and is not a competing graphics renderer.

## Measured render time

| Renderer | First render | Branding revision |
|---|---:|---:|
| Remotion4.0.543 | {times['remotion']['first']:.3f}s | {times['remotion']['revised']:.3f}s |
| HyperFrames0.9.34 | {times['hyperframes']['first']:.3f}s | {times['hyperframes']['revised']:.3f}s |

Final runs were sequential with two workers each. These include renderer startup and visual encoding; shared FFmpeg audio mux has separate command logs. They exclude setup, authoring, downloads and reasoning. Different browser render paths and encoder defaults remain; one run per version gives no statistical performance guarantee. Earlier simultaneous/pre-polish renders remain in the evidence but are not these final timings.

## What changed in branding

FrameLab with a teal F monogram became SignalCut with a coral S monogram; product screens changed their logo and accent too. Narration, caption text, graphics timing, cuts, duration and source picture were intentionally preserved. The narrated product name still says Frame Lab: the revision tests visual rebranding without re-recording speech, not a complete linguistic rebrand.

## Self-verification and defects

- All four final files fully decode at1280×720/30fps and match the38.4s timeline within0.1s; all have audio.
- Decoded audio PCM hashes match across all four exports: the actual encoded narration/music/effects mix survived unchanged.
- Sampled source-picture and caption crops remain within2 RGB levels mean absolute difference after rebranding. Brand-accent pixel samples change from teal to coral. Final logo/name and animated sequence states are reviewed in rendered frames.
- Cleaned narration re-transcription recovered104/105 intended words, normalized word error rate{v['speech']['wer']:.4f}; rejected sentence absent. Opening A is absent in both recognizers. This may be ASR or cut-edge loss; no listening-based resolution is claimed.
- Initial raw-fragment captions lost words crossing edit boundaries. MakeMyClip's cleaned-clip word timing also extended past the end and dropped final words. Local MLX Whisper alignment repaired caption coverage and grouping. Final captions contain the observed104-word transcript, with a minimum1.7s group duration. This makes the transcript-repair stage necessary; successful export alone was insufficient.
- Initial source label crop, font parity, header position and caption group defects were corrected. HyperFrames runtime/contrast/layout checks passed after narrow annotations for intentionally covered background text; nested root-composition warnings remain as an editable-handoff weakness. The silent-film warning applies to pre-mux visuals; final files include the common audio mix.

The playable-report browser test initially failed because a generic text placeholder corrupted embedded base64 video bytes. Unique placeholders fixed it; all three embedded videos match their source MP4 bytes exactly. Brave paired-play and paired-pause controls were exercised successfully. This report-packaging defect is separate from either renderer.

The original shared mix peaks at-4.96dBFS with RMS-19.13dBFS; no listening-based assessment is claimed.

## Strengths and weaknesses

**Remotion:** predictable frame math; direct control of the three motion sequences; props cleanly switch branding. More verbose React code, and quality checks outside the renderer are largely our own scripts. No conventional timeline interchange was tested for these graphics.

**HyperFrames:** HTML and seekable GSAP are approachable for web authoring; snapshot/contact-sheet and layout/contrast diagnostics helped find defects. The installed compiler required explicit header positioning and local font definitions for closer parity. Our root contains nested graphics rather than separate scene files, so a future user can edit HTML but does not get the cleanest per-scene Studio handoff. Local render succeeded; no hosted credits or provider account needed.

**MakeMyClip:** actual transcript-based rejected-take removal and silence cleanup were useful. The retained editable project and decisions make recovery possible. Word timing/caption generation was the weakest seam in this trial; the separate cleaned-clip alignment repair restored coverage.

## Intervention, time and cost limits

See INTERVENTIONS.json for five shared correction categories and four HyperFrames-specific setup/layout categories; these are an operator's repair log, not timed human labor or independent agent success rates. User input covered source/installation decisions; no human visual scoring was collected. Both contenders were authored by the same Codex session using the same brief, not independently prompted competing agents.

No paid generation or hosted-render API calls were used. Incremental billed API spend for this run was0; Codex subscription allocation, tokens, electricity and total labor were not metered. Remotion's custom licence still governs use; system fonts are local assets and are not redistributed in the source repository. Synthesized music/effects demonstrate mixing and scheduled accents, not professional sound design or music selection.

This is a synthetic narrated demonstration, not real talking-head footage. It cannot establish face continuity, lip sync, emotional performance selection or fully unattended storytelling. Source screenshots are original code-native mock product screens. The shared pipeline is implemented and run; real-footage generalization remains untested.

## Reproduction

From repository root after existing setup: npm ci; run scripts/round_two/fixture.py, node scripts/round_two/screenshots.mjs, cleanup.py, captions.py, author.py; generate storyboard stills with render.py remotion --stills and HyperFrames snapshot. Review them, then render.py remotion and hyperframes for first/revised versions; verify.py; report.py; audit.py results/round-two/evidence.json. Python scripts use the root environment except MLX, which runs .venv/bin/python. See docs/round-two/README.md for the exact ordered commands.

Primary references: https://github.com/heygen-com/hyperframes/blob/main/packages/cli/README.md ; https://www.remotion.dev/docs/ai/coding-agents ; https://github.com/MakeMyClip/editor
'''
report=ROOT/'docs/round-two/RESULTS.md';report.write_text(text)
def data(p):return 'data:'+mimetypes.guess_type(p.name)[0]+';base64,'+base64.b64encode(p.read_bytes()).decode()
cards=''.join(f'<article><h2>{e.title()}</h2><video controls preload="metadata" src="{data(media/f"{e}-revised.mp4")}"></video><p>Final visual rebrand. First: {times[e]["first"]:.2f}s · revision: {times[e]["revised"]:.2f}s.</p></article>' for e in ['remotion','hyperframes'])
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Round two · Narration, motion and revision</title><style>:root{color-scheme:dark;background:#10191e;color:#edf0eb;font-family:Helvetica}*{box-sizing:border-box}body{margin:0}main{max-width:1300px;margin:auto;padding:48px 28px}h1{font:54px/1.1 Georgia;max-width:900px}h2{font:28px Georgia}p{color:#afbdc2;line-height:1.7}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}video{width:100%;background:black;border:1px solid #35434a}summary{cursor:pointer;padding:20px 0;color:#f27d62}pre{white-space:pre-wrap;font:15px/1.7 Helvetica;max-width:950px}button{padding:12px 18px;background:#f27d62;border:0;border-radius:6px;color:#10191e;cursor:pointer;margin:12px 8px 24px 0}button:focus-visible{outline:3px solid white}small{color:#f27d62}@media(max-width:800px){.grid{grid-template-columns:1fr}h1{font-size:38px}}</style><main><small>LIVE BENCHMARK / ROUND TWO / 12 NOVEMBER 2026</small><h1>One story.<br>Two graphics engines.<br>A checked branding revision.</h1><p>MakeMyClip cleanup → storyboarded Remotion or HyperFrames → identical music, effects and captions → rebrand → verify.</p><p>Both pipelines exported. Remotion ranks first for local workflow reliability in this run; the modest visual design is effectively tied. Synthetic narration limits the claim.</p><button id="play">Play both from start</button><button id="pause">Pause both</button><p id="state" role="status">Remotion supplies audio during paired playback.</p><div class="grid">__CARDS__</div><details><summary>Raw recording, before cleanup (46.92 seconds)</summary><video controls preload="metadata" src="__INPUT_VIDEO_DATA__"></video></details><details><summary>Full measured analysis and limitations</summary><pre>__REPORT_TEXT__</pre></details><p>Self-contained local report; no hosted media requests. Source repository: <a href="https://github.com/archit15singh/video-editing-agent-bench">video-editing-agent-bench</a>.</p></main><script>const pair=[...document.querySelectorAll('article video')];document.querySelector('#play').onclick=async()=>{pair.forEach((v,i)=>{v.pause();v.currentTime=0;v.muted=i===1});const r=await Promise.allSettled(pair.map(v=>v.play()));document.querySelector('#state').textContent=r.every(x=>x.status==='fulfilled')?'Both playing; HyperFrames muted to avoid doubled speech.':'Use the individual playback controls.'};document.querySelector('#pause').onclick=()=>{pair.forEach(v=>v.pause());document.querySelector('#state').textContent='Both paused.'};</script></html>'''
page=page.replace('__REPORT_TEXT__',html.escape(text)).replace('__INPUT_VIDEO_DATA__',data(media/'source.mp4')).replace('__CARDS__',cards)
(ROOT/'artifacts/round-two.html').write_text(page)
def ref(p):
 p=ROOT/p;return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
verification=ref('results/round-two/verification.json')
evidence={'input':{'duration_seconds':manifest['duration'],'provenance':'synthetic','source':ref('results/round-two/media/source.mp4'),'screenshots':[ref(f'results/round-two/media/first-screen-{i}.png') for i in range(3)]},'cleanup':{k:ref(p) for k,p in {'transcript':'results/round-two/raw-transcript.json','decisions':'results/round-two/cleanup-state.json','project':'results/round-two/cleanup-project.json','output':'results/round-two/media/clean.mp4','verification':'results/round-two/cleanup-speech-verification.json'}.items()},'shared':{k:ref(p) for k,p in {'captions':'fixtures/round-two/captions.json','music':'results/round-two/media/music.wav','sound_effects':'results/round-two/media/effect.wav'}.items()},'engines':{},'comparison':{'quality':'Comparable modest design; operator qualitative review','defects':'See REVIEW.md','intervention':'See INTERVENTIONS.json','time':times,'cost':'0 incremental paid API spend; subscription/labor unmetered'},'report':ref('docs/round-two/RESULTS.md')}
for e in ['remotion','hyperframes']:
 evidence['engines'][e]={'status':'verified','source':ref('adapters/round-two/remotion.jsx' if e=='remotion' else 'adapters/round-two/hyperframes-revised/index.html'),'storyboard':ref('docs/round-two/STORYBOARD.md'),'first_export':ref(f'results/round-two/media/{e}-first.mp4'),'revised_export':ref(f'results/round-two/media/{e}-revised.mp4'),'verification':verification,'revision_comparison':verification,'review':ref('docs/round-two/REVIEW.md'),'commands':ref(f'results/logs/r2-{e}-revised.json')}
save('results/round-two/evidence.json',evidence)
print('Report, playable artifact and hashed evidence manifest created.')
