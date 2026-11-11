# Visual review record

The same coordinating Codex session authored and reviewed both contenders. No external human ratings or blind judgments were collected.

## Before full rendering

Inspected HyperFrames storyboard contact sheet at3.2,4.5,16.5,28.5s and Remotion4.5s frame. Found source label cropped by centered cover positioning. Corrected both video panes to left-center cropping. Inspected updated7s frames from both: source label readable, third row highlighted, captions separate from screenshot.

Matched the three animation intentions to the storyboard: sequential row highlights for organize; slight screenshot scale/pan for review; progressive bars for deliver. These are deliberately modest overlays, not a claim of high-end motion design.

HyperFrames compiled Georgia/Helvetica to downloaded fallback fonts. Switched both implementations to explicit local R2Serif/R2Sans font-face files. Fonts are copied from the user's macOS install only for local rendering; they are not redistributed in Git.

HyperFrames check reported intentionally covered background headline/subtitle while graphic plates are on screen. Marked only those two background text elements as allowing occlusion. Increased top supporting label from12px to19px in both. Retained warnings about nested root graphics (editable but not split into subcomposition files); report them as a handoff limitation rather than a render failure.

## Setup repairs

- HyperFrames snapshot failed to find FFmpeg despite the task-local PATH. Passing its documented HYPERFRAMES_FFMPEG_PATH/HYPERFRAMES_FFPROBE_PATH overrides resolved the snapshot.
- Copying system fonts with shutil.copy2 failed while copying macOS file flags. copyfile copied bytes without that metadata and resolved setup.
- HyperFrames used its default user font cache before fonts were pinned; no global agent or service configuration was changed. CLI telemetry is disabled for benchmark runs.

HyperFrames positioned the brand32px too high when relying on the class selector. An explicit inline header position resolved it; the4.5s frame was inspected after this correction.

Final export/rebranding inspection remains to be recorded after the four exports complete. The checked-in results must distinguish those outcomes from this preparatory review.

## Caption repair

MakeMyClip's captions derived from raw-source fragments omitted words crossing edit boundaries, and some groups lasted0.21–0.35s. Re-transcribing the cleaned single clip restored internal boundaries, but its word-timing path omitted the final three words (timings exceeded the38.4s media). Local MLX word alignment retained the closing words. Final caption groups use those observed timestamps, not the fixture script. The opening article A remains absent in both recognizers; retained as an unresolved ASR/cut discrepancy.

## Final export inspection — completed

Inspected actual revised-export contact sheets from both engines at3.2,7,12.19,12.29,18,24.11,24.22,28.5,38s. Inspected full-size28.5s frames from both, HyperFrames18s/12.29s, and Remotion38s. SignalCut name, S monogram and coral palette appear in header and screenshot. The three visual sequences appear, source labels switch correctly across cuts, captions occupy their reserved band, and closing caption includes testing today. The early entrance differs slightly in opacity between engines; the result is similar, not pixel-identical cross-engine motion.

Both versions' retained picture/caption crops pass the automated revision comparison. Shared audio PCM is identical after export. The final mix peaks at-4.96dBFS with RMS-19.13dBFS, measured on the original mix WAV; this is not an integrated-LUFS or listening assessment. Original synthesized music and three scheduled effect inputs are preserved in the FFmpeg mix command evidence.

Unresolved quality limits: one opening article absent in recognizers/captions, synthetic narration rather than a real performance, and no listening-based judgment or lip-sync test. Root-graphics nesting warnings remain in HyperFrames. These are disclosed in the final ranking.
