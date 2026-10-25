"""Normalize generated pixels only; never draw or synthesize anatomy/motion.

The one fixed transform is derived from the neutral source and shared by all
standing frames. Keep raw sources and per-file processing receipts.
"""
from pathlib import Path
import argparse, hashlib, json
from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]
SCALE = (1444 - 123) / (1504 - 26)
TX = 512 - 489 * SCALE
TY = 1444 - 1504 * SCALE

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def normalize(source, asset_id, already_registered=False):
    source = Path(source).resolve()
    output = ROOT / 'runtime/default' / (asset_id + '.png')
    if output.exists(): raise RuntimeError('Refusing to overwrite ' + str(output))
    with Image.open(source) as raw:
        if raw.size != (1024, 1536) or raw.mode != 'RGBA':
            raise RuntimeError('Unexpected native source size/mode')
        im = raw.copy()
    # The generator encoded opaque interiors predominantly as 252/253/254.
    # Restore those near-opaque values; preserve ordinary antialiased edges.
    alpha = im.getchannel('A').point(lambda a: 0 if a <= 3 else 255 if a >= 252 else a)
    im.putalpha(alpha)
    if not already_registered:
        im = im.convert('RGBa').transform((1024, 1536), Image.Transform.AFFINE,
            (1/SCALE, 0, -TX/SCALE, 0, 1/SCALE, -TY/SCALE),
            Image.Resampling.BICUBIC, fillcolor=(0,0,0,0)).convert('RGBA')
    pixels = list(im.getdata())
    im.putdata([(0,0,0,0) if p[3] == 0 else p for p in pixels])
    output.parent.mkdir(parents=True, exist_ok=True)
    icc = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
    im.save(output, icc_profile=icc)
    receipt = dict(asset_id=asset_id, source=str(source.relative_to(ROOT)),
        source_sha256=sha(source), source_native_size=[1024,1536],
        output=str(output.relative_to(ROOT)), output_sha256=sha(output),
        output_size=[1024,1536], generator='built-in image_gen',
        source_pixels_upscaled=False, source_native_resolution_verified=True,
        operations=['alpha <=3 cleared; alpha >=252 restored to255',
                    'already registered imagegen repair: no geometric transform' if already_registered else 'single shared premultiplied affine; bicubic downscale',
                    'zero hidden RGB under alpha0; attach sRGB profile'],
        shared_transform=dict(scale=SCALE, translate_x=TX, translate_y=TY,
            source_support=[489,1504], target_support=[512,1444]),
        already_registered=already_registered,
        applied_transform=dict(scale=1.0, translate_x=0.0, translate_y=0.0) if already_registered else dict(scale=SCALE, translate_x=TX, translate_y=TY),
        art_invented_by_processing=False)
    (ROOT/'reports'/(asset_id+'.provenance.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('asset_id');a=p.parse_args()
    normalize(a.source,a.asset_id)
