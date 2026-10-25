"""Render existing artwork for review. Missing frames remain missing; no art synthesis."""
from pathlib import Path
import hashlib, json
from PIL import Image, ImageDraw
from nyra_assets import inspect, render_cell

ROOT = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    catalog_path = ROOT/'specs/assets_required.json'
    catalog = json.loads(catalog_path.read_text())
    assets = {a['id']: a for a in catalog['assets']}
    checks, missing = [], []
    for a in assets.values():
        p = ROOT/a['path']
        if not p.exists():
            missing.append(a['id'])
            continue
        c = inspect(p); c['asset_id'] = a['id']; checks.append(c)
        if a.get('status') != 'P0_REVIEWED':
            status = 'STATIC_OUTFIT_ONLY' if a.get('outfit') == 'office' else 'GENERATED_PENDING_VISUAL_GATE'
            a.update(status=status, sha256=sha(p),
                     native_resolution_provenance='RECORDED')
    catalog['generated_runtime_asset_count'] = len(checks)
    catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    profile = json.loads((ROOT/'specs/pets_layout_profiles.json').read_text())['profiles']['pets_v2_attachment_provisional']
    rows = profile['row_definitions']
    sequences = list(rows) + [dict(state='gaze_full_16',asset_ids=[a for r in rows[9:] for a in r['asset_ids']])]
    out = ROOT/'preview/rendered/extensions'; out.mkdir(parents=True,exist_ok=True)
    facts = {}
    for row in sequences:
        ids = row['asset_ids']; absent = [a for a in ids if not (ROOT/assets[a]['path']).exists()]
        if absent:
            facts[row['state']] = dict(status='INCOMPLETE_NOT_RENDERED',missing=absent)
            continue
        frames, cells, hashes = [], [], {}
        for aid in ids:
            p = ROOT/assets[aid]['path']; im=Image.open(p).convert('RGBA'); hashes[aid]=sha(p)
            bg=Image.new('RGBA',im.size,'#362c42');bg.alpha_composite(im)
            frames.append(bg.resize((384,576)).convert('RGB'))
            tile=render_cell(p,profile);cell=Image.new('RGBA',tile.size,'#362c42');cell.alpha_composite(tile);cells.append(cell.convert('RGB'))
        name=row['state']; once=name in ['waving','jumping']
        timings=[200 if 'gaze' in name else 150]*len(frames)
        opts=dict(save_all=True,append_images=frames[1:],duration=timings,disposal=2)
        if not once: opts['loop']=0
        frames[0].save(out/(name+'.gif'),**opts)
        smallopts=dict(opts);smallopts['append_images']=cells[1:];cells[0].save(out/(name+'-pet-size.gif'),**smallopts)
        sheet=Image.new('RGB',(len(cells)*192,234),'#362c42');draw=ImageDraw.Draw(sheet)
        for i,c in enumerate(cells):sheet.paste(c,(i*192,0));draw.text((i*192+3,211),ids[i].replace('nyra_',''),fill='white')
        sheet.save(out/(name+'-frames.png'))
        facts[name]=dict(status='RENDERED_REQUIRES_VISUAL_REVIEW',slots=len(ids),unique_hashes=len(set(hashes.values())),hashes=hashes,loop=not once,durations_ms=timings)
    (ROOT/'reports/extensions-pixel-and-source-checks.json').write_text(json.dumps(dict(actual_png=len(checks),missing=missing,checks=checks),indent=2)+'\n')
    (ROOT/'reports/extensions-sequence-facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    print(json.dumps(dict(actual_png=len(checks),missing=len(missing),all_present_structural_pass=all(c['structural_pass'] for c in checks),rendered=sum(x['status'].startswith('RENDERED') for x in facts.values()))))

if __name__ == '__main__':main()
