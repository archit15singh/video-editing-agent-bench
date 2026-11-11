# Live benchmark protocol

Compare three toolchains operated by the same Codex session:
1. FFmpeg + local Whisper + Remotion.
2. MakeMyClip CLI/MCP (FFmpeg + whisper.cpp internally).
3. NodeTool MCP with local editing tools; no paid generation.

A fourth FFmpeg-only output is a control, not one of the three contenders.

## Two separate questions

- Execution: can the tool implement a known edit, render it and expose enough state to verify it?
- Editorial autonomy: can an agent infer the right cuts from raw footage and a natural-language brief?

A deterministic fixture with a supplied edit decision list measures execution only. Do not present it as a test of unsupervised editorial judgment. Transcription, semantic retake detection and automatic silence removal need separate observed results.

## Common assignment

Produce a 1280×720, 30 fps MP4 from the same source. Remove a deliberate bad take and pause, retain three correct sections in order, add an opening title and captions, preserve speech, then revise the title and render again. Retain an editable project.

Use synthetic speech with known text, a moving marker, distinct scene colours, scene IDs, and known boundaries. Record actual generated timings in the fixture manifest. Ground truth must not substitute for ASR in the transcription trial.

## Evidence

Record package/source versions, exact commands, exit codes, wall time, errors and recoveries. Preserve raw logs. Check full-file decoding, duration, dimensions, frame rate, audio presence, cut order from colour samples, audio continuity, title/caption visibility and revision persistence. Inspect frames at cuts and within each scene. Stills cannot validate temporal rhythm, lip sync or music; do not claim those were verified without actual evidence.

Report installation/setup separately from render time. Exclude dependency downloads and shared fixture generation from render time. A failed attempt is evidence; do not silently replace a broken toolchain with FFmpeg and credit the contender.

## Ranking rubric

Qualitative judgments use explicit evidence for output correctness, agent control and recoverability, verification support, iteration speed, visual flexibility, editable handoff, setup burden and licensing/privacy. Separate measured results, source-documented capabilities and untested hypotheses. No precise aggregate score from a single synthetic clip. A blocked tool is ranked on local readiness, not claimed intrinsic video quality.
