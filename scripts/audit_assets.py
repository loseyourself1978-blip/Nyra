#!/usr/bin/env python3
"""Audit supplied bytes and extract explicit reference-only crops; never invent pixels."""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source-handoff/TWOS_COMPANION_V3_HANDOFF_R1'
ASSETS = ROOT / 'assets'
REPORTS = ROOT / 'reports'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def measure(path):
    with Image.open(path) as im:
        im.load()
        alpha = im.convert('RGBA').getchannel('A')
        hist = alpha.histogram()
        count = im.width * im.height
        return dict(width=im.width, height=im.height, mode=im.mode,
                    sha256=sha(path), bytes=path.stat().st_size,
                    alpha_min=min(i for i, n in enumerate(hist) if n),
                    alpha_max=max(i for i, n in enumerate(hist) if n),
                    transparent_pixels=hist[0], opaque_pixels=hist[255],
                    nonopaque_fraction=sum(hist[:-1]) / count,
                    transparent_fraction=hist[0] / count)


def main():
    ASSETS.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    catalog = json.loads((SOURCE / 'specs/asset_catalog.json').read_text())
    declared = {a['file']: a for a in catalog['design_sheets']}
    declared.update({a['file']: a for a in catalog['generation_receipt']['source_files']})
    assets = []
    primary = Image.open(SOURCE / 'generated/V3_PRIMARY_COMPOSITE.png')
    for p in sorted(SOURCE.rglob('*.png')):
        relative = p.relative_to(SOURCE).as_posix()
        entry = dict(file=relative, **measure(p), classification='DISPLAY_REFERENCE_ONLY',
                     runtime_ready=False, silhouette_alpha_approved=False)
        if relative in declared:
            d = declared[relative]
            entry['catalog_hash_matches'] = entry['sha256'] == d['sha256']
            if 'crop_rect' in d:
                entry['source'] = d['source_file']
                entry['crop_rect_xyxy'] = d['crop_rect']
                with Image.open(p) as crop:
                    expected = primary.crop(d['crop_rect'])
                    entry['pixels_equal_source_crop'] = (
                        expected.size == crop.size and expected.tobytes() == crop.tobytes())
        assets.append(entry)
    checks = []
    for line in (SOURCE / 'MANIFEST.sha256').read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        path = SOURCE / name
        checks.append(dict(file=name, exists=path.is_file(),
                           matches=path.is_file() and sha(path) == digest))
    report = dict(kind='ACTUAL_BYTE_AND_REFERENCE_AUDIT',
                  phase='ASSET_AUDIT_AND_STANDALONE_PREVIEW',
                  source_composites=3, derived_section_references=8,
                  selected_source_reference=1, runtime_assets_ready=0,
                  real_animation_loops_ready=0, custom_voice='NOT_PRODUCED',
                  live_integration='BLOCKED_NO_AUTHORIZED_INTERFACE_CONNECTED',
                  alpha_receipt_correction=(
                      'The receipt says RGB, but 11 generated PNGs decode as RGBA. '
                      'Their nonuniform alpha is not a clean silhouette matte; '
                      'printed backgrounds, labels and panel content remain. '
                      'Having an alpha channel does not make these runtime sprites.'),
                  assets=assets, handoff_manifest_checks=checks)
    (REPORTS / 'asset-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    # Exact source panels and deliberately bounded outfit reference crops.
    specs = [
        ('v3-master', '黑紫 V3 · 主造型', 'generated/sheets/02_fullbody_master.png', None,
         '主造型参考；302×517；原图板含标题与背景；非透明动画素材'),
        ('office-reference', '职场 · 概念换装', 'reference/V3_SELECTED_REFERENCE.png', [1118, 41, 1204, 253],
         '服装参考裁片；86×212；半身、低分辨率；缺同姿态全身运行素材'),
        ('gala-reference', '晚礼服 · 概念换装', 'reference/V3_SELECTED_REFERENCE.png', [1207, 41, 1293, 253],
         '服装参考裁片；86×212；半身、低分辨率；缺同姿态全身运行素材'),
    ]
    outfits = []
    for identity, name, source, rect, note in specs:
        p = SOURCE / source
        output = ASSETS / (identity + '.png')
        if rect:
            with Image.open(p) as im:
                im.crop(rect).save(output)
        else:
            shutil.copyfile(p, output)
        info = measure(output)
        outfits.append(dict(id=identity, name=name, file=output.name, note=note,
                            source=source, source_sha256=sha(p),
                            crop_rect_xyxy=rect or [0, 0, info['width'], info['height']],
                            anchor=None, anchor_status='NOT_RUNTIME_ALIGNED',
                            classification='STATIC_CONCEPT_REFERENCE', runtimeReady=False,
                            **info))
    manifest = dict(schemaVersion=1, character='夜璃 · Nyra', mode='STATIC_PREVIEW',
                    defaultOutfit='v3-master', outfits=outfits,
                    wardrobeStatus='REFERENCE_SWITCHING_ONLY_RUNTIME_OUTFITS_MISSING')
    (ASSETS / 'outfits.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    # Audit contact sheet contains only resized supplied pixels and neutral labels.
    contact = Image.new('RGB', (1200, 820), '#ececf1')
    draw = ImageDraw.Draw(contact)
    for i, p in enumerate(sorted((SOURCE / 'generated/sheets').glob('*.png'))):
        with Image.open(p) as im:
            thumb = Image.new('RGB', im.size, 'white')
            thumb.paste(im, mask=im.getchannel('A'))
            thumb.thumbnail((280, 350))
            x, y = (i % 4)*300, (i // 4)*410
            contact.paste(thumb, (x+(300-thumb.width)//2, y+38))
            draw.text((x+8, y+10), p.stem, fill='black')
    contact.save(REPORTS / 'reference-contact.png')
    if not all(x['matches'] for x in checks):
        raise SystemExit('Source manifest mismatch: inspect report')
    if not all(x.get('catalog_hash_matches', True) and x.get('pixels_equal_source_crop', True) for x in assets):
        raise SystemExit('Source crop or catalog mismatch: inspect report')
    print(f'Audited {len(assets)} images; {len(checks)} source hashes match; runtime_ready=0')


if __name__ == '__main__':
    main()
