"""Run the unchanged bundled pipeline with the approved nearest-pixel sampling.

Only the resampling filter changes. Geometry, connected-group extraction,
registration, assembly, validation and artwork remain owned by bundled tools.
"""
import runpy
import sys
from PIL import Image

target = sys.argv[1]
sys.argv = sys.argv[1:]
original_resize = Image.Image.resize

def nearest_resize(self, size, resample=None, box=None, reducing_gap=None):
    return original_resize(self, size, Image.Resampling.NEAREST, box=box,
                           reducing_gap=reducing_gap)

Image.Image.resize = nearest_resize
try:
    runpy.run_path(target, run_name='__main__')
finally:
    Image.Image.resize = original_resize
