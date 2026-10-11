# Failed row visual review

Built-in imagegen generated the selected strip from all four supplied references; no correction pass was needed.

- Eight separated, complete full-body poses; source green chroma; same outfit, hair, eye identity, slender proportions, and grounded shoes.
- Frames 1–4 progressively lower eyelids and bow head/shoulders; frame 4 has closed eyes and the deepest bow. Frames 5–8 protectively cup the glasses then recover. This reads as restrained disappointment rather than an idle prop pose.
- One amber-lensed, warm-brown framed spectacles pair remains attached to both cupped hands in every pose. No wearing, duplicates, book, tears, detached fragments, or decorative effects.
- Native 192x208 frames 00, 03, 04, 07 inspected visually; spectacles silhouette remains legible and connected. Head lowering is visibly preserved; clothing and shoe baseline stable with only 1 pixel source registration variation.
- Bundled component extraction and inspect_frames reports both returned ok:true, with zero errors and warnings. Chroma-adjacent edge pixels still require the parent workflow's final single despill pass.

Selected source: decoded/failed.png
Actual prompt: prompts/rows/failed-v3-actual.md
Official report: qa/rows/failed/review.json
Official frames: qa/rows/failed/frames/failed/
