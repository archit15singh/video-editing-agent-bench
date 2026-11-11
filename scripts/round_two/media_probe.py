"""Namespace round-two probe logs so earlier benchmark evidence stays intact."""
import json
from pathlib import Path
from bench import run,binary

def probe(path):
    return json.loads(run([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',path],f'r2-probe-{Path(path).stem}'))
