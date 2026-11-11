# Reproduce round two

Apple Silicon macOS. First install the earlier benchmark environment with scripts/setup_local.sh. Root npm lockfile includes HyperFrames0.9.34 and GSAP3.14.2. Fonts come from the local macOS installation; fonts are not redistributed. No provider keys or account sign-in are used. HyperFrames CLI telemetry is disabled by the runner. Keep the Remotion browser installed by the earlier setup.

From repository root:

```sh
npm ci --no-audit --no-fund
python3 scripts/round_two/fixture.py
node scripts/round_two/screenshots.mjs
python3 scripts/round_two/cleanup.py
python3 scripts/round_two/captions.py
python3 scripts/round_two/author.py
python3 scripts/round_two/render.py remotion --stills
```

Generate a HyperFrames storyboard with the actual CLI (its FFmpeg probe needs explicit overrides here):

```sh
HYPERFRAMES_NO_TELEMETRY=1 \
HYPERFRAMES_FFMPEG_PATH="$PWD/.tools/bin/ffmpeg" \
HYPERFRAMES_FFPROBE_PATH="$PWD/.tools/bin/ffprobe" \
HYPERFRAMES_BROWSER_PATH="$PWD/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell" \
node_modules/.bin/hyperframes snapshot adapters/round-two/hyperframes-first \
  --at 3.2,4.5,7,16.5,18,28.5 --no-end \
  --output "$PWD/results/round-two/media/hyperframes-storyboard-final"
```

Inspect both storyboards before final rendering. Run the four final renders sequentially for less contention:

```sh
python3 scripts/round_two/render.py remotion
python3 scripts/round_two/render.py remotion --version revised
python3 scripts/round_two/render.py hyperframes
python3 scripts/round_two/render.py hyperframes --version revised
python3 scripts/round_two/verify.py
python3 scripts/round_two/report.py
python3 scripts/round_two/audit.py results/round-two/evidence.json
```

The report's reviewed status reflects the captured run. A fresh operator should inspect their own exported frames and update REVIEW.md before claiming visual review. The file/hash audit is a completeness gate, not an aesthetic judge. A freshly generated voice may differ if macOS changes its voice assets. Recorded durations and system-font availability should be checked; current voice fixture raw46.921s, clean38.400s. The caption alignment uses local MLX Whisper as a repair after observed MakeMyClip timing/coverage failures.

Generated assets stay under ignored results/round-two/media; author.py copies task-local source/screenshots/fonts into ignored HyperFrames assets. The final self-contained artifacts/round-two.html embeds the final videos for review without those asset directories. Do not copy local font files into Git. No live service or personal data is used.
