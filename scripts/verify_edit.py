#!/usr/bin/env python3
"""Independent expected-cut checks, not renderer implementation checks."""
import argparse
import array
import hashlib
import json
import math
import subprocess
from pathlib import Path
from bench import ROOT, binary, probe, run, save

COLORS={'intro':(22,78,99),'feature':(76,29,149),'close':(20,83,45)}

def rgb_at(path,seconds,x=5,y=5):
    result=subprocess.run([binary('ffmpeg'),'-v','error','-ss',str(seconds),'-i',str(path),
          '-frames:v','1','-vf',f'crop=2:2:{x}:{y},scale=1:1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True)
    return list(result.stdout[:3])

def rms(path,start,duration):
    result=subprocess.run([binary('ffmpeg'),'-v','error','-ss',str(start),'-i',str(path),'-t',str(duration),
          '-vn','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True,check=True)
    samples=array.array('f'); samples.frombytes(result.stdout)
    return math.sqrt(sum(x*x for x in samples)/len(samples)) if samples else 0

def verify(path):
    manifest=json.loads((ROOT/'fixtures/manifest.json').read_text())
    info=probe(path)
    kept=[s for s in manifest['scenes'] if s['keep']]
    details=[]
    for s in kept:
        observed=rgb_at(path,s['edit_start']+s['duration']/2)
        expected=COLORS[s['id']]
        error=max(abs(a-b) for a,b in zip(observed,expected)) if len(observed)==3 else 999
        details.append(dict(scene=s['id'],observed_rgb=observed,expected_rgb=expected,max_error=error,passed=error<15,
                    speech_rms=rms(path,s['edit_start']+0.3,min(2,s['speech_duration']-0.3))))
    # Boundary samples catch stale take/pause insertion and timestamp drift.
    boundaries=[]
    for s in kept[1:]:
        t=s['edit_start']
        after=rgb_at(path,t+0.1)
        error=max(abs(a-b) for a,b in zip(after,COLORS[s['id']])) if len(after)==3 else 999
        boundaries.append(dict(time=t,after_rgb=after,passed=error<15))
    checks=dict(duration=abs(float(info['format']['duration'])-manifest['expected_duration'])<0.2,
                correct_scenes=all(s['passed'] for s in details),
                correct_boundaries=all(s['passed'] for s in boundaries),
                audible_sections=all(s['speech_rms']>0.003 for s in details))
    report=dict(file=str(path),checks=checks,passed=all(checks.values()),scenes=details,boundaries=boundaries,
                limitations=['RMS proves signal presence, not speech intelligibility or sync.',
                             'Corner colours prove scene identity at sampled times, not every frame.',
                             'Caption/title readability requires visual inspection.'])
    save(f'results/verification/{path.stem}-edit.json',report)
    print(json.dumps(report,indent=2))
    return report['passed']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('video',type=Path)
    args=parser.parse_args();raise SystemExit(0 if verify(args.video.resolve()) else 1)
