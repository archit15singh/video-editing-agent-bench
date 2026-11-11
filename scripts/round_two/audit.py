#!/usr/bin/env python3
"""Audit round-two evidence. Missing evidence is never a successful run.

This checks evidence integrity and required coverage, not aesthetic quality or
truthfulness of manually recorded observations. Actual media checks belong to
render/verification runners; their logs and hashed outputs must be retained.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = {
    'input': {'duration_seconds', 'provenance', 'source', 'screenshots'},
    'cleanup': {'transcript', 'decisions', 'project', 'output', 'verification'},
    'comparison': {'quality', 'defects', 'intervention', 'time', 'cost'},
}
ENGINE_ARTIFACTS = ('source', 'storyboard', 'first_export', 'revised_export',
                    'verification', 'revision_comparison', 'review', 'commands')


def audit(manifest, root=ROOT):
    issues = []

    def artifact(ref, label):
        if not isinstance(ref, dict):
            issues.append(f'{label}: missing artifact reference')
            return
        name, expected = ref.get('path'), ref.get('sha256')
        if not isinstance(name, str) or not isinstance(expected, str):
            issues.append(f'{label}: path and sha256 required')
            return
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            issues.append(f'{label}: path escapes project')
        elif not path.is_file():
            issues.append(f'{label}: file missing: {name}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            issues.append(f'{label}: content hash mismatch')

    for section, keys in REQUIRED.items():
        obj = manifest.get(section)
        if not isinstance(obj, dict):
            issues.append(f'{section}: missing section')
            continue
        for key in sorted(keys):
            if key not in obj:
                issues.append(f'{section}.{key}: missing')
    source = manifest.get('input', {})
    duration = source.get('duration_seconds')
    if not isinstance(duration, (int, float)) or not 45 <= duration <= 60:
        issues.append('input: recording must be 45–60 seconds')
    if source.get('provenance') not in ('synthetic', 'user-recording'):
        issues.append('input: explicit provenance required')
    artifact(source.get('source'), 'input.source')
    shots = source.get('screenshots', [])
    if not isinstance(shots, list) or len(shots) < 3:
        issues.append('input: at least three screenshots required')
    else:
        for index, shot in enumerate(shots):
            artifact(shot, f'input.screenshots[{index}]')
    cleanup = manifest.get('cleanup', {})
    for key in REQUIRED['cleanup']:
        artifact(cleanup.get(key), f'cleanup.{key}')
    for engine in ('hyperframes', 'remotion'):
        result = manifest.get('engines', {}).get(engine, {})
        for key in ENGINE_ARTIFACTS:
            artifact(result.get(key), f'{engine}.{key}')
        if result.get('status') != 'verified':
            issues.append(f'{engine}: export and revision remain unverified')
    for key in ('captions', 'music', 'sound_effects'):
        artifact(manifest.get('shared', {}).get(key), f'shared.{key}')
    artifact(manifest.get('report'), 'report')
    return {'complete': not issues, 'issues': issues,
            'limitations': ['Hash and coverage audit does not judge aesthetics or validate manual assertions.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    if args.manifest.exists():
        report = audit(json.loads(args.manifest.read_text()))
    else:
        report = {'complete': False, 'issues': ['Evidence manifest does not exist; live runs incomplete.']}
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['complete'] else 1)
