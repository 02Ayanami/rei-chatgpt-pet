"""Render review media only from the encoded atlas; does not change artwork."""
from pathlib import Path
import json
import subprocess
import os
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / 'final/spritesheet-extended.png'
OUT = ROOT / 'previews'
OUT.mkdir(exist_ok=True)
sheet = Image.open(ATLAS).convert('RGBA')
states = [('idle', 6), ('running-right', 8), ('running-left', 8),
          ('waving', 4), ('jumping', 5), ('failed', 8),
          ('waiting', 6), ('running', 6), ('review', 6)]

def cell(row, col):
    return sheet.crop((col * 192, row * 208, (col+1) * 192, (row+1) * 208))

def labeled(frame, label):
    canvas = Image.new('RGB', (384, 448), '#263044')
    canvas.paste(frame.resize((384, 416), Image.Resampling.NEAREST), (0, 0),
                 frame.resize((384, 416), Image.Resampling.NEAREST).getchannel('A'))
    ImageDraw.Draw(canvas).text((12, 426), label, fill='white')
    return canvas

def gif(frames, path, duration):
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=duration, loop=0, disposal=2, optimize=False)

all_frames, durations = [], []
native_root = ROOT / 'final/frames'
for row, (state, count) in enumerate(states):
    folder = native_root / state
    folder.mkdir(parents=True, exist_ok=True)
    for col in range(count):
        frame = cell(row, col)
        frame.save(folder / f'{col:02d}.png')
        all_frames.append(labeled(frame, f'{state} / {col+1}'))
        durations.append(180 if state != 'idle' else 300)
gif(all_frames, OUT / 'all-states.gif', durations)
personality_frames = []
for row, state, count in [(0, 'distant gaze / eye contact', 6),
                          (6, 'waiting for you', 6),
                          (7, 'focused reading', 6),
                          (8, 'checking / faint smile', 6),
                          (5, 'treasured spectacles / disappointment', 8)]:
    for column in range(count):
        personality_frames.append(labeled(cell(row, column), f'{state} / {column+1}'))
gif(personality_frames, OUT / 'personality-focus.gif', 240)
personality_stills = Image.new('RGB', (5*384, 448), '#263044')
for index, (row, col, label) in enumerate([(0, 3, 'eye contact'), (6, 3, 'waiting'),
                                         (7, 3, 'reading'), (8, 4, 'review / smile'),
                                         (5, 3, 'spectacles')]):
    personality_stills.paste(labeled(cell(row, col), label), (index*384, 0))
personality_stills.save(OUT / 'personality-stills.png')
transition = [cell(0, i) for i in range(6)] + [cell(4, i) for i in range(5)] + [cell(0, i) for i in range(6)]
gif(transition, OUT / 'idle-jump-idle.gif', [300]*6 + [150]*5 + [300]*6)
looks = [cell(9+i//8, i%8) for i in range(16)]
gif(looks, OUT / 'look-loop.gif', 180)
stills = Image.new('RGB', (4*384, 448), '#263044')
for index, (row, col, label) in enumerate([(0, 0, 'idle'), (3, 2, 'waving'), (4, 2, 'jumping'), (7, 2, 'working')]):
    stills.paste(labeled(cell(row, col), label), (index*384, 0))
stills.save(OUT / 'four-stills.png')
frames_dir = OUT / 'video-frames'
frames_dir.mkdir(exist_ok=True)
sequence_index = 0
for frame, duration in zip(all_frames, durations, strict=True):
    for _ in range(round(duration / 50)):
        frame.save(frames_dir / f'{sequence_index:04d}.png')
        sequence_index += 1
ffmpeg = os.environ.get('REI_FFMPEG', 'ffmpeg')
subprocess.run([str(ffmpeg), '-y', '-loglevel', 'error', '-framerate', '20',
                '-i', str(frames_dir / '%04d.png'), '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                str(OUT / 'all-states.mp4')], check=True)
(OUT / 'media-report.json').write_text(json.dumps({
    'ok': True, 'source': str(ATLAS), 'standard_frames': len(all_frames),
    'look_frames': len(looks), 'video_frames': sequence_index,
    'artifacts': ['all-states.gif', 'all-states.mp4', 'idle-jump-idle.gif', 'look-loop.gif', 'four-stills.png', 'personality-focus.gif', 'personality-stills.png']
}, indent=2) + '\n')
print('Rendered encoded-atlas previews, stills and MP4.')
