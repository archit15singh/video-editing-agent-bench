#!/usr/bin/env bash
set -euo pipefail
BENCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BENCH_ROOT"
# Tested on Apple Silicon macOS, Python 3.13, Node 26.12.0.
# Explicit setup only: no global npm/pip installs or MCP client configuration writes.
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm ci --no-audit --no-fund
npm ci --prefix adapters/nodetool --no-audit --no-fund
mkdir -p .tools/bin .tools/models results
.venv/bin/python - <<'PY'
import imageio_ffmpeg,pathlib
p=pathlib.Path('.tools/bin/ffmpeg')
if not p.exists():p.symlink_to(imageio_ffmpeg.get_ffmpeg_exe())
PY
node --input-type=module - <<'JS'
import ffprobe from '@ffprobe-installer/ffprobe';import fs from 'node:fs';
fs.chmodSync(ffprobe.path,0o755);if(!fs.existsSync('.tools/bin/ffprobe'))fs.symlinkSync(ffprobe.path,'.tools/bin/ffprobe');
JS
if [ ! -d .tools/whisper.cpp ]; then
  git clone --depth 1 --branch v1.8.3 https://github.com/ggml-org/whisper.cpp.git .tools/whisper.cpp
fi
.venv/bin/cmake -S .tools/whisper.cpp -B .tools/whisper.cpp/build -DCMAKE_BUILD_TYPE=Release -DGGML_METAL=OFF -DWHISPER_BUILD_TESTS=OFF
.venv/bin/cmake --build .tools/whisper.cpp/build --config Release -j 4
if [ ! -f .tools/models/ggml-base.en.bin ]; then
  curl -L --fail -o .tools/models/ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
fi
node_modules/.bin/remotion browser ensure
XDG_DATA_HOME="$BENCH_ROOT/.cache/nodetool-data" XDG_CACHE_HOME="$BENCH_ROOT/.cache" PATH="$BENCH_ROOT/.tools/bin:$PATH" adapters/nodetool/node_modules/.bin/nodetool packs add video imaging media-codecs --yes
python3 scripts/bench.py doctor
