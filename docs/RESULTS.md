# Live results — 12 November 2026

**For editing existing recordings with an agent, choose MakeMyClip first. Choose Remotion when custom visual design matters more. NodeTool's standalone MCP export was blocked in this environment.**

All rankings below concern the tested local workflow, not every version or deployment of these products. Codex in this interactive session authored and operated the adapters. This was not three independently prompted agents or a model benchmark.

## What actually ran

An Apple Silicon Mac generated a 20.53-second synthetic recording with native speech, a rejected opening take, a 2-second pause, three correct scenes, distinct colours and a moving marker. Each tool received the same source MP4 and retained ranges. The deterministic assignment produced a 15.13-second, 1280×720, 30 fps cut, three reference-text caption blocks, an opening title and a title revision.

The execution test deliberately supplies an edit manifest. It proves a specified edit can be implemented, not that an agent independently discovered an engaging story. A separate MakeMyClip transcript-driven test used local ASR, an agent decision to cut the explicitly rejected sentence, silence detection and automatically generated five-word captions. It produced a 12.395-second cut. It was not blind: the coordinating session had already seen the fixture and reference text.

## Ranking

| Rank for footage editing | Toolchain | Measured result | Best reason to choose it | Main weakness |
|---|---|---|---|---|
| 1 | Codex + MakeMyClip 0.4.1 + whisper.cpp | First, revised, polished and transcript-driven MP4s exported; JSON timeline and FCPXML retained | Small editing commands, local ASR, silence removal, undoable state and inexpensive iteration | Limited title placement/design surface; transcripts and word timings need review |
| 2 | Codex + Remotion 4.0.543 + local Whisper + FFmpeg verification | First and revised MP4s exported; editable React composition retained | Full layout and motion control; deterministic frame previews; natural fit for a coding agent | More code and slower rendering; no tested transcript-editing timeline/undo workflow |
| 3 | Codex + NodeTool 0.8.10 standalone MCP | Source imported, clips trimmed, title revised, saved state validated and contact sheet rendered; MP4 jobs failed | Rich structured timeline, snapshots, validation and composited preview | Extra packages and runtime setup, then a reproducible export integration failure |

For animated product promos or explainers I would reverse the top two. The fixture includes a modest Remotion title animation; it does not benchmark sophisticated motion design, colour grading, long-form editing, GPU performance or cinematic storytelling.

## Output and verification

An FFmpeg-only control also rendered the same retained ranges and reference-text overlays, and passed the format and independent edit checks. It is a control, not a fourth ranked agent editor.

Remotion and MakeMyClip passed full-file decoding, dimensions, frame rate, audio-track presence, intended duration, sampled scene order and samples immediately after both cut boundaries. Independent checks rejected the original unedited source as a negative control. These checks would catch an export that merely encoded successfully while retaining the bad take or pause.

Local whisper.cpp re-transcribed the two final deterministic exports and the automatic MakeMyClip export. All intended words were recovered after case/punctuation normalization (0 word error rate against the reference), with no rejected sentence. This is evidence of speech-content preservation, not a listening test or proof of perfect audio sync. The model was also used elsewhere in this workflow, so this is not independent model validation.

I inspected rendered images. MakeMyClip's initial top-centred title covered the source scene label. Through MCP I replaced it with a smaller top-right title, re-exported and inspected that exact output. Remotion's revised title and caption were readable and separated from the scene label. NodeTool's initial text positions were authored in the wrong units and its overlays shared a track; after reading actual state and API contracts, I moved captions to an overlay track and used pixel offsets. Its final contact sheet is readable and validation has no warnings. Those authoring mistakes are not counted as renderer bugs.

Scene-colour samples differed from nominal fixture RGB by at most 12 levels per channel in Remotion and 1 in MakeMyClip. The tolerance was 15. This suggests a small difference in the tested colour pipelines; it is not a colour-management benchmark.

## Iteration speed

| Measurement | MakeMyClip | Remotion |
|---|---:|---:|
| Initial full render, concurrent first runs | 1.383 s | 17.264 s |
| Title revision render, concurrent first runs | 1.248 s | 13.950 s |
| Sequential warm render, one run each | 1.404 s | 14.432 s |

Times include CLI startup and render, exclude dependency/model/browser downloads and fixture generation. Warm runs used the existing final compositions, ran sequentially, and were not a statistical sample. Designs, encoders and title animation differ; do not treat the ratio as a universal performance result. No model reasoning latency, token cost or end-to-end human editing time was measured.

## Strengths and weaknesses in practice

### MakeMyClip

**Observed strengths:** 8 MCP tools with structured editing verbs; inspectable JSON and an operation log; CLI edits and MCP corrections share the same timeline. It exported FCPXML, although importing that file into a professional editor was not tested. Its silence dry run found four silent regions and proposed removing 5.662 seconds from the full source. The agent then cut transcript words 0–7 and applied silence removal to the surviving media clips, followed by ASR-derived captions and export. All processing stayed local.

**Observed weaknesses:** the CLI resolves relative media paths against the working directory, whereas MCP documents workspace-relative resolution. An initial relative-path call failed until changed to an absolute path. Invalid anchor `bottom` was rejected with the supported values; the corrected value was `bottom-center`. Those were operator errors, and they are preserved in logs. The tested title controls expose nine anchors rather than the unrestricted positioning available in React. The original ASR text said “row recordings,” and some word timings stretched across a pause; the uncorrected automatic-caption sample retains that error. Retake detection returned no repeats, which is expected because the fixture has a rejected instruction rather than a repeated phrase; repeated-take performance remains untested.

### Remotion

**Observed strengths:** the composition makes timing, title position, animation, caption styling and retained source ranges explicit. A revised prop changes the title without rebuilding the edit logic. Its headless renderer produced a frame preview and successful MP4 exports. MLX Whisper transcribed the source locally as a separate preparation step.

**Observed weaknesses:** the deterministic output uses reference captions, not automatically consumed ASR output. The composition directly trims the original video in Remotion; FFmpeg prepares/verifies media here rather than making a separate destructive base cut. There is no tested automatic retake-removal pipeline or conventional editor handoff. Code changes can be versioned, but that is different from a user's timeline undo. Rendering requires a substantial browser download. Remotion has a custom licence; check eligibility before commercial deployment.

### NodeTool

**Observed strengths:** 14 direct MCP tools; discoverable editing functions through its code sandbox; persistent timeline documents; named snapshots; validators that detected overlapping overlays; composited frames and contact sheets without a desktop UI. It accepted the shared source, stored the correct source ranges, retained the title revision and produced a readable final preview.

**Observed blocker:** standalone `render_timeline` jobs repeatedly returned `Node "render" failed: ProcessingContext model interface 'getTimelineSequence' is not configured`, including a fresh-ID reproduction in `scripts/run_nodetool.py`. A valid document and complete preview did not imply a working export. I did not replace this with an FFmpeg render and call NodeTool successful.

**Setup friction:** native SQLite initially had a Node 26/24 ABI mismatch; matching Node 26 resolved MCP startup. Imaging/canvas and video packs were optional and had to be added before previews or render jobs could run. A nonexistent `timeline` pack was rejected; the actual `video` pack was installed. These dependencies live in the repository's isolated data directory. The desktop/server path, generated-media providers and paid APIs were not tested. This failure does not establish that NodeTool's desktop app cannot export.

## Recommendation

Start with **MakeMyClip + local Whisper for assembly and speech cleanup**. Add **Remotion for deliberate branded graphics** when the design justifies the extra code and render time. A hybrid is a recommendation, not an integrated pipeline tested here. Keep the edit plan, JSON/project state, exported media and verification results together. Human review remains useful for story, timing and listening; the current evidence supports technically checked short edits, not universal unattended video editing.

Primary references and licences: [sources](SOURCES.md). Reproduction and commands: [README](../README.md). Raw logs and checks: [results](../results/).
