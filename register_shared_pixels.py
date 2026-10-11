"""Preserve the approved row-wide scale and jump displacement using pixel sampling."""
from pathlib import Path
import json
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parent
shutil.copytree(ROOT / 'frames', ROOT / 'qa/pre-registration-frames', dirs_exist_ok=True)
scale = 176 / 196
rows = []
for folder in (ROOT / 'frames').iterdir():
    if not folder.is_dir() or folder.name == 'jumping':
        continue
    bounds = []
    for file in sorted(folder.glob('*.png')):
        frame = Image.open(file).convert('RGBA')
        resized = frame.resize((round(192*scale), round(208*scale)), Image.Resampling.NEAREST)
        target = Image.new('RGBA', (192, 208))
        target.alpha_composite(resized, ((192-resized.width)//2, round(203-202*scale)))
        target.save(file)
        bounds.append(target.getchannel('A').point(lambda a: 255 if a > 16 else 0).getbbox())
    rows.append({'state': folder.name, 'bounds': bounds})
(ROOT / 'qa/shared-registration.json').write_text(json.dumps({
    'shared_scale': scale, 'nominal_baseline': 203,
    'sampling': 'NEAREST, no smoothing or painted corrections',
    'jumping': 'original source displacement retained, no row shrink', 'rows': rows
}, indent=2)+'\n')
print('Applied one shared nearest-pixel transform; jumping unchanged.')
