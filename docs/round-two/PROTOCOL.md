# Round two: speech cleanup and storyboarded product graphics

Status: live runs in progress. User selected generated demo and approved isolated HyperFrames dependencies with “do both” (2026-11-12).

## Acceptance evidence

1. One shared 45–60-second narrated recording and at least three product screenshots, with source hashes and provenance. Record whether synthetic or real; synthetic footage cannot establish talking-head lip sync or natural performance editing.
2. MakeMyClip cleans deliberate mistakes/pauses. Preserve raw transcript, edit decisions, cleaned audio/video, captions and editable state. Verify retained speech by re-transcription; inspect cut boundaries.
3. HyperFrames and Remotion implement the same three storyboarded motion sequences from the same screenshots, timing and design brief. Save contact sheets before full render and record corrections. Keep renderer-specific code independently editable.
4. Composite each contender with the same cleaned recording, captions, music and effects. Use original locally synthesized audio to avoid licensing ambiguity. Preserve speech intelligibility with conservative mix levels; measure peaks/loudness and inspect timing.
5. Apply the same branding revision (name, palette and logo), render both again, and verify intended changes plus unchanged speech/cut timing. Record revisions, failures, command wall times and output hashes.
6. Rank qualitative visual quality, defects, intervention and maintainability alongside measured execution time. Subscription agent cost is unmeasured unless usage evidence exists; local paid-service spend must be reported separately. Do not invent token or monetary costs.

## Controls

Keep the initial benchmark intact. New assets/results use round-two namespaces. No paid APIs, global MCP configuration edits or external footage uploads. The repository is public; generated demo data must be fictitious, and real footage must remain local unless explicitly authorized for publication.

Review both animation endpoints and intermediate frames. Decode entire exports, check dimensions/frame rate/duration/audio, sample every cut and each graphic sequence, compare revision frames and transcript coverage. Use negative controls to establish that verifiers reject meaningful defects. Frame review cannot establish a full listening or aesthetic review.

## Current independent findings

HyperFrames official CLI documentation describes local HTML compositions, FFmpeg and Node >=22, snapshot/check/render commands. Registry observed 2026-11-12: hyperframes 0.9.34. Installed locally for this round; gsap3.14.2 added for seekable animation.

Sources:
- https://github.com/heygen-com/hyperframes/blob/main/packages/cli/README.md
- https://github.com/heygen-com/hyperframes/blob/main/docs/developers/cli.mdx

Shared raw recording46.921s; MakeMyClip cleanup38.400s. Final outputs and verification still pending.
