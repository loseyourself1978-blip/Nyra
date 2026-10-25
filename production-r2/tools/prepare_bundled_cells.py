"""Adapt real per-frame art to bundled Pets tools without per-frame registration.

The user requires native individual PNGs, shared canvas/anchor and no strip
generation. This adapter only calls the existing fixed transform, then the
installed bundled atlas functions; it neither synthesizes art nor grants QA.
"""
from pathlib import Path
import argparse, hashlib, json, sys
from PIL import Image
from nyra_assets import render_cell

ROOT = Path(__file__).resolve().parents[1]
LABELS = ['000','022.5','045','067.5','090','112.5','135','157.5',
          '180','202.5','225','247.5','270','292.5','315','337.5']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save_json(p, data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scripts',type=Path,required=True)
    ap.add_argument('--assemble',action='store_true');args=ap.parse_args()
    scripts=args.scripts.resolve();run=ROOT/'bundled-run'
    sys.path.insert(0,str(scripts))
    from assemble_extended_atlas import (load_base_rows, paste_look_cells,
        clear_transparent_rgb, validate_normalized_look_cells)
    profile=json.loads((ROOT/'specs/pets_layout_profiles.json').read_text())['profiles']['pets_v2_attachment_provisional']
    if (profile['canvas'],profile['cell']) != ([1536,2288],[192,208]):
        raise ValueError('Unexpected frozen target geometry')
    rows=profile['row_definitions']
    if args.assemble:
        atlas=load_base_rows(run/'final/standard.png')
        cells=[Image.open(run/'look-cells'/f'{a}.png').convert('RGBA') for a in LABELS]
        validate_normalized_look_cells(cells,0,2,24)
        paste_look_cells(atlas,cells)
        out=run/'final/extended-raw.png';clear_transparent_rgb(atlas).save(out)
        save_json(run/'qa/assembly-receipt.json',{
            'method':'bundled load_base_rows + validate_normalized_look_cells + paste_look_cells + clear_transparent_rgb',
            'extra_per_frame_scale_or_translation':False,
            'bundled_module_sha256':sha(scripts/'assemble_extended_atlas.py'),
            'candidate_sha256':sha(out),'visual_acceptance':'PENDING_FINAL_REVIEW'})
        print('Assembled candidate with bundled functions; no acceptance asserted')
        return
    catalog=json.loads((ROOT/'specs/assets_required.json').read_text())
    assets={a['id']:a for a in catalog['assets']}
    req=json.loads((run/'pet_request.json').read_text())
    records=[]
    for row_index,row in enumerate(rows):
        for slot,aid in enumerate(row['asset_ids']):
            source=ROOT/assets[aid]['path']
            with Image.open(source) as im:
                if im.size!=(1024,1536) or im.mode!='RGBA':raise ValueError(source)
            cell=clear_transparent_rgb(render_cell(source,profile))
            dest=(run/'frames'/row['state']/f'{slot:02d}.png') if row_index<9 else (run/'look-cells'/f'{LABELS[(row_index-9)*8+slot]}.png')
            dest.parent.mkdir(parents=True,exist_ok=True);cell.save(dest)
            records.append(dict(asset_id=aid,source=str(source.relative_to(ROOT)),
                source_sha256=sha(source),cell=str(dest.relative_to(run)),cell_sha256=sha(dest)))
    if len(records)!=73:raise ValueError('Expected 73 populated cells')
    manifest=dict(chroma_key=req['chroma_key'],
        rows=[dict(state=r['state'],method='independent-png-fixed-transform') for r in rows[:9]],
        transform=dict(scale=200/1536,translate_x=96-512*200/1536,translate_y=196-1444*200/1536),
        source_canvas=[1024,1536],source_anchor=[512,1444],target_anchor=[96,196],
        per_frame_autofit=False,art_synthesized=False,records=records)
    save_json(run/'frames/frames-manifest.json',manifest)
    save_json(run/'workflow-adaptation.json',{
        'authority':'User R2: native individual PNGs, fixed canvas/anchor; prompts explicitly include work tablet and review blank card',
        'per_frame_generation':'Existing actual image_gen outputs and provenance; generated strips not claimed',
        'generated_job_graph':'prepare_pet_run planning only; no duplicate image jobs dispatched',
        'look_registration':'Bypass CLI auto-registration; call bundled composition functions on existing fixed-transform cells',
        'preserved_checks':'All bundled frame, atlas, chroma, continuity, semantics and quality gates remain required',
        'library':'No direct Library-folder upload capability exposed; local artifacts retained; no cloud Library save claimed',
        'owner_acceptance':False})
    print(json.dumps({'cells':len(records),'standard':57,'look':16,'generated_art':False}))

if __name__=='__main__':main()
