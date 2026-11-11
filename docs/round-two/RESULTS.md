# Round two: a complete narrated-demo pipeline

Measured on12 November2026. Public repository: https://github.com/archit15singh/video-editing-agent-bench

## Result

Both MakeMyClip → Remotion → FFmpeg and MakeMyClip → HyperFrames → FFmpeg exported first and rebranded videos. The46.921-second synthetic narrated recording became a38.400-second cleaned edit. Each implementation uses the same three fictitious product screenshots, three6-second graphics sequences, repaired captions, original music and effects. Source code, rendered review frames, raw logs and verification are retained.

**Practical ranking for this run:1 Remotion,2 HyperFrames. Visual result: effectively tied for this modest design.** Remotion required fewer renderer-specific repairs and retained explicit frame-driven React code. HyperFrames delivered the same visual idea with editable HTML/GSAP and stronger built-in layout/contrast diagnostics, but needed explicit FFmpeg paths and a header positioning repair. This is a workflow ranking by one operator, not intrinsic model or aesthetic superiority. MakeMyClip remains the shared cleanup component and is not a competing graphics renderer.

## Measured render time

| Renderer | First render | Branding revision |
|---|---:|---:|
| Remotion4.0.543 | 31.473s | 31.909s |
| HyperFrames0.9.34 | 25.583s | 25.359s |

Final runs were sequential with two workers each. These include renderer startup and visual encoding; shared FFmpeg audio mux has separate command logs. They exclude setup, authoring, downloads and reasoning. Different browser render paths and encoder defaults remain; one run per version gives no statistical performance guarantee. Earlier simultaneous/pre-polish renders remain in the evidence but are not these final timings.

## What changed in branding

FrameLab with a teal F monogram became SignalCut with a coral S monogram; product screens changed their logo and accent too. Narration, caption text, graphics timing, cuts, duration and source picture were intentionally preserved. The narrated product name still says Frame Lab: the revision tests visual rebranding without re-recording speech, not a complete linguistic rebrand.

## Self-verification and defects

- All four final files fully decode at1280×720/30fps and match the38.4s timeline within0.1s; all have audio.
- Decoded audio PCM hashes match across all four exports: the actual encoded narration/music/effects mix survived unchanged.
- Sampled source-picture and caption crops remain within2 RGB levels mean absolute difference after rebranding. Brand-accent pixel samples change from teal to coral. Final logo/name and animated sequence states are reviewed in rendered frames.
- Cleaned narration re-transcription recovered104/105 intended words, normalized word error rate0.0095; rejected sentence absent. Opening A is absent in both recognizers. This may be ASR or cut-edge loss; no listening-based resolution is claimed.
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
