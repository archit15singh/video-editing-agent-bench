#!/usr/bin/env python3
"""Local video benchmark orchestration. No third-party Python dependencies."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]

def save(path, value):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

def run(args, name, timeout=300, env=None):
    start = time.monotonic()
    try:
        result = subprocess.run([str(x) for x in args], cwd=ROOT, capture_output=True,
                                text=True, timeout=timeout, env=env)
        record = dict(command=[str(x) for x in args], returncode=result.returncode,
                      stdout=result.stdout, stderr=result.stderr)
    except subprocess.TimeoutExpired as exc:
        record = dict(command=[str(x) for x in args], returncode=None, timeout=True,
                      stdout=str(exc.stdout or ''), stderr=str(exc.stderr or ''))
    record.update(elapsed_seconds=round(time.monotonic()-start, 3),
                  observed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    save(f'results/logs/{name}.json', record)
    if record['returncode'] != 0:
        raise RuntimeError(f'{name} failed: see results/logs/{name}.json')
    return record['stdout']

def binary(name):
    local = ROOT / '.tools' / 'bin' / name
    found = str(local) if local.exists() else shutil.which(name)
    if not found:
        raise RuntimeError(f'{name} missing; run the approved dependency setup first')
    return found

def probe(path):
    return json.loads(run([binary('ffprobe'), '-v', 'error', '-show_format', '-show_streams',
                           '-of', 'json', path], f'probe-{Path(path).stem}'))

def doctor():
    report = {}
    for name in ['node', 'npm', 'ffmpeg', 'ffprobe', 'say']:
        try:
            report[name] = binary(name)
        except RuntimeError:
            report[name] = None
    report['platform'] = os.uname().sysname + ' ' + os.uname().machine
    report['ready'] = all(report[k] for k in ['node', 'npm', 'ffmpeg', 'ffprobe'])
    save('results/doctor.json', report)
    print(json.dumps(report, indent=2))

def verify(paths):
    for source in paths:
        path = Path(source).resolve()
        info = probe(path)
        streams = info['streams']
        video = next((s for s in streams if s['codec_type']=='video'), {})
        checks = dict(video_present=bool(video), audio_present=any(s['codec_type']=='audio' for s in streams),
                      dimensions=video.get('width')==1280 and video.get('height')==720,
                      fps=video.get('r_frame_rate')=='30/1', nonempty=path.stat().st_size>1000)
        run([binary('ffmpeg'), '-v', 'error', '-i', path, '-f', 'null', '-'], f'decode-{path.stem}')
        checks['full_decode'] = True
        save(f'results/verification/{path.stem}.json', dict(path=str(path),
             sha256=hashlib.sha256(path.read_bytes()).hexdigest(), checks=checks,
             duration=float(info['format']['duration']), streams=streams,
             passed=all(checks.values())))
        print(path.name, checks)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command', choices=['doctor','verify'])
    parser.add_argument('paths', nargs='*')
    args=parser.parse_args()
    if args.command=='doctor': doctor()
    else: verify(args.paths)
