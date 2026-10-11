# Idle and waiting visual review

Built-in ImageGen produced both strips using all four requested references. Official strip extraction used the shared nearest-neighbor sampling wrapper; official inspection reported ok true with no errors or warnings for both rows.

Idle: exactly six complete separated poses; same icy-blue hair, red eyes, school uniform, dark socks, white shoes, slender full-body proportions. Feet stay planted. Visible distant gaze, one closed blink (the generator rendered a full blink rather than the requested half blink), direct eye contact, and return to distant gaze. Joined hands remain unchanged; no props or effects. First/last nearly identical. Calm semantics readable at native size. Native frames 00, 02, 03, 05 inspected.

Waiting: exactly six complete separated poses; same identity, proportions, planted feet. Head down -> lift -> direct eye contact -> held gaze -> small head tilt -> head down. Hands subtly tighten but their elevation change is limited; the head movement and expectant gaze carry state meaning. No bow touching, books, glasses, effects or extra objects. Native frames 00, 02, 03, 04, 05 inspected.

Selected sources: decoded/idle.png and decoded/waiting.png.
Prompts: prompts/rows/idle-v3-actual.md and prompts/rows/waiting-v3-actual.md.
QA: qa/rows/idle/review.json and qa/rows/waiting/review.json.
Frame roots: qa/rows/idle/frames and qa/rows/waiting/frames.

Final playback registration and cross-state scale review remain with the parent workflow.

