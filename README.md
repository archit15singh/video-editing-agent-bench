# Autonomous video editing benchmark

**Live-tested:** MakeMyClip is the strongest fit here for editing recordings; Remotion gives better layout/motion control; NodeTool's standalone MCP preview works but its export jobs failed.

[Read the measured results and qualitative analysis](docs/RESULTS.md) · [Open the playable report](artifacts/comparison.html) · [Methodology](docs/METHODOLOGY.md) · [Primary sources](docs/SOURCES.md)

Three toolchains operated by the same Codex session against identical footage. No paid APIs or desktop mouse automation. This is a toolchain execution experiment, plus a separate transcript-driven MakeMyClip run; it is not a blind test of autonomous editorial judgment.

## Reproduce on Apple Silicon macOS

Tested with Node 26.12.0, Python 3.13, MakeMyClip 0.4.1, Remotion 4.0.543, NodeTool 0.8.10 and whisper.cpp v1.8.3. Exact packages, binaries, model hash and raw evidence are under `results/` and the lockfiles. Native `say` and system fonts make fixture generation macOS-specific.

After approving dependency installation in your environment:

```sh
bash scripts/setup_local.sh
python3 scripts/make_fixture.py
python3 scripts/run_remotion.py
python3 scripts/run_makemyclip.py
python3 scripts/polish_makemyclip.py
python3 scripts/run_nodetool.py  # exit 2 is the observed export failure
python3 scripts/run_ffmpeg_control.py
PATH="$PWD/.tools/bin:$PATH" .venv/bin/python scripts/transcribe_mlx.py
python3 scripts/makemyclip_auto.py
python3 scripts/finish_auto.py
python3 scripts/verify_speech.py
python3 scripts/warm_timing.py
```

`run_nodetool.py` creates fresh asset/timeline IDs. The runner exits 2 on a failed export. Inspect the summary's job `status`; a successful MCP call can contain a failed render job. In the tested version both renders fail with `getTimelineSequence is not configured`. The runner preserves that outcome rather than substituting another renderer.

`polish_makemyclip.py` resolves the current title ID and applies the visual correction through MCP, exporting both the polished MP4 and final FCPXML. Historical plans remain as evidence; use the script for fresh runs.

```sh
python3 scripts/bench.py verify results/remotion/media/remotion-revised.mp4
python3 scripts/verify_edit.py results/remotion/media/remotion-revised.mp4
python3 scripts/verify_edit.py fixtures/generated/source.mp4  # expected failure
python3 scripts/build_report.py
```

## Evidence and limits

- Input: 20.53 seconds; deterministic edit: 15.13 seconds; automatic speech/silence edit: 12.395 seconds.
- Successful MP4s pass decode, format and independent sampled-cut checks. Exported speech was re-transcribed and compared with the intended words.
- Rendered stills were inspected and layout defects corrected. No claim of listening-based audio review or full-motion aesthetic evaluation.
- Setup and run failures remain in logs. Early adapter mistakes are distinguished from product faults.
- Generated media, models, caches and dependencies remain local. The self-contained HTML report embeds final sample videos and previews so it is reviewable from a checkout without those local directories.
- MakeMyClip JSON/FCPXML and NodeTool timeline JSON are retained. FCPXML import into a pro editor is untested. Remotion source plus fixture manifest is the editable project.

The repository is private. Upstream software keeps its own licences; Remotion uses custom terms. This repo does not redistribute model files or vendor source snapshots.
