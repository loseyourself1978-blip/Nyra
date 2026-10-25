#!/usr/bin/env python3
"""Offline checks and atlas packing. Never generates art, calls models, or installs Pets.
Requires Python 3.10+ and Pillow in the execution environment.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path
from collections import defaultdict
from PIL import Image, ImageChops

class GateError(Exception):
    pass

def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def safe(root: Path, value: str) -> Path:
    root=root.resolve()
    p=Path(value)
    if p.is_absolute() or '..' in p.parts: raise GateError(f'Unsafe relative path: {value}')
    result=(root/p).resolve()
    if not result.is_relative_to(root): raise GateError(f'Path outside package: {value}')
    return result

def profile_hash(profile: dict) -> str:
    return hashlib.sha256(json.dumps(profile,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def layout_check(p: dict) -> list[str]:
    errors=[]
    w,h=p['canvas'];cw,ch=p['cell'];cols=p['columns'];rows=p['rows']
    if w!=cols*cw or h!=rows*ch: errors.append('Canvas/grid dimensions disagree')
    if len(p['row_definitions'])!=rows: errors.append('Row count disagrees')
    count=0
    for i,r in enumerate(p['row_definitions']):
        n=len(r['asset_ids']);count+=n
        if r['row']!=i or n!=r['required_frames'] or not 0<n<=cols: errors.append(f'Invalid row {i}')
    if count!=p['required_slots']: errors.append('Required slot count disagrees')
    if rows*cols-count!=p['transparent_empty_slots']: errors.append('Empty slot count disagrees')
    return errors

def inspect(path: Path, expected_size=(1024,1536)) -> dict:
    result={'file':str(path),'exists':path.is_file(),'errors':[]}
    if not path.is_file():
        result['errors'].append('MISSING_FILE');return result
    try:
        with Image.open(path) as raw:
            raw.load()
            result.update(width=raw.width,height=raw.height,mode=raw.mode,sha256=digest(path))
            if raw.mode!='RGBA': result['errors'].append('RGBA_REQUIRED')
            if expected_size and raw.size!=expected_size: result['errors'].append('NATIVE_CANVAS_MISMATCH')
            im=raw.convert('RGBA');a=im.getchannel('A');hist=a.histogram();total=im.width*im.height
            result.update(alpha_min=a.getextrema()[0],alpha_max=a.getextrema()[1],transparent_fraction=hist[0]/total,opaque_fraction=hist[255]/total,semtransparent_fraction=sum(hist[1:255])/total,alpha_bbox=a.getbbox())
            corners=[a.getpixel(xy) for xy in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]]
            if any(corners): result['errors'].append('NONTRANSPARENT_CORNER')
            edge=[a.crop((0,0,im.width,1)).getextrema()[1],a.crop((0,im.height-1,im.width,im.height)).getextrema()[1],a.crop((0,0,1,im.height)).getextrema()[1],a.crop((im.width-1,0,im.width,im.height)).getextrema()[1]]
            if any(edge): result['errors'].append('CANVAS_EDGE_NOT_CLEAR')
            if hist[0]/total<.25: result['errors'].append('INSUFFICIENT_REAL_CLEAR_BACKGROUND')
            if hist[255]/total<.025: result['errors'].append('NO_ADEQUATE_OPAQUE_CHARACTER_CORE')
            if a.getbbox() is None: result['errors'].append('EMPTY_IMAGE')
            # Structural alpha checks only. They do not recognize anatomy, identity or art quality.
    except Exception as ex:
        result['errors'].append('DECODE_ERROR:'+type(ex).__name__)
    result['structural_pass']=not result['errors']
    return result

def p0_ids(root: Path) -> list[str]:
    p=load(root/'specs/standalone_p0.json')
    return list(dict.fromkeys(a for s in p['sequences'].values() for a in s['asset_ids']))

def run_audit(root: Path, ids: list[str], require_visual=False) -> dict:
    catalog=load(root/'specs/assets_required.json');assets={a['id']:a for a in catalog['assets']}
    review=load(root/'specs/visual_review.json');records=[];errors=[];hash_groups=defaultdict(list)
    for aid in dict.fromkeys(ids):
        if aid not in assets:
            errors.append(f'{aid}: NOT_IN_CATALOG');continue
        entry=assets[aid]
        try: rec=inspect(safe(root,entry['path']),(entry['native_width'],entry['native_height']))
        except GateError as ex: rec={'errors':[str(ex)],'exists':False}
        rec['asset_id']=aid
        if entry.get('reference_only') or entry.get('test_fixture'): rec['errors'].append('REFERENCE_OR_FIXTURE_NOT_PRODUCTION')
        if rec.get('exists'):
            sha=rec.get('sha256');hash_groups[sha].append(aid)
            if not entry.get('sha256') or sha!=entry['sha256']: rec['errors'].append('MISSING_OR_MISMATCHED_DECLARED_HASH')
            if entry.get('native_resolution_provenance')!='RECORDED': rec['errors'].append('NATIVE_SOURCE_PROVENANCE_NOT_RECORDED')
            if require_visual:
                v=review.get('assets',{}).get(aid,{})
                if v.get('sha256')!=sha: rec['errors'].append('VISUAL_REVIEW_NOT_BOUND_TO_CURRENT_HASH')
                for key in ('identity','anatomy','coverage','alpha_edges','anchor','source_provenance'):
                    if v.get(key)!='PASS': rec['errors'].append('VISUAL_'+key.upper()+'_NOT_PASS')
        rec['structural_pass']=not rec['errors'];records.append(rec)
        errors.extend(f'{aid}: {s}' for s in rec['errors'])
    for sha,group in hash_groups.items():
        if sha and len(group)>1: errors.append('UNDECLARED_DUPLICATE_DISTINCT_ASSETS: '+','.join(group))
    return {'status':'PASS_STRUCTURAL_AND_DECLARED_GATES' if not errors else 'BLOCKED','generated_by':'nyra_assets.py','art_generation_performed':False,'required_unique_assets':len(set(ids)),'present_assets':sum(r.get('exists',False) for r in records),'require_visual':require_visual,'errors':errors,'assets':records}

def render_cell(path: Path, p: dict) -> Image.Image:
    # One uniform affine for the whole family: no per-frame bounding-box auto fit.
    cw,ch=p['cell'];w,h=1024,1536
    scale=min((cw-8)/w,(ch-8)/h)
    tx=cw/2-512*scale;ty=(ch-12)-1444*scale
    with Image.open(path) as im:
        premul=im.convert('RGBA').convert('RGBa')
        tile=premul.transform((cw,ch),Image.Transform.AFFINE,(1/scale,0,-tx/scale,0,1/scale,-ty/scale),Image.Resampling.BICUBIC,fillcolor=(0,0,0,0)).convert('RGBA')
    return tile

def build(root: Path, name: str, output_rel: str):
    profiles=load(root/'specs/pets_layout_profiles.json')['profiles']
    if name not in profiles: raise GateError('Unknown target profile')
    p=profiles[name];err=layout_check(p)
    if err: raise GateError('; '.join(err))
    t=load(root/'specs/target_environment.json')
    if t.get('selected_profile')!=name or not t.get('row_mapping_confirmed') or not t.get('profile_sha256')==profile_hash(p):
        raise GateError('TARGET_LAYOUT_UNCONFIRMED: read actual installed Pets skill/schema and bind profile hash first')
    if p['rows']==11 and not t.get('gaze_order_confirmed'): raise GateError('TARGET_GAZE_ORDER_UNCONFIRMED')
    if not t.get('app_version') or not t.get('skill_version_or_hash'): raise GateError('TARGET_VERSION_EVIDENCE_MISSING')
    evidence=t.get('target_evidence_file')
    if not evidence: raise GateError('TARGET_EVIDENCE_FILE_MISSING')
    ev=safe(root,evidence)
    if not ev.is_file() or digest(ev)!=t.get('target_evidence_sha256'): raise GateError('TARGET_EVIDENCE_HASH_MISMATCH')
    ids=[aid for r in p['row_definitions'] for aid in r['asset_ids']]
    audit=run_audit(root,ids,True)
    if audit['status']=='BLOCKED': raise GateError('ART_ASSET_GATE_BLOCKED: '+'; '.join(audit['errors'][:8]))
    catalog={a['id']:a for a in load(root/'specs/assets_required.json')['assets']}
    v=load(root/'specs/visual_review.json')
    for r in p['row_definitions']:
        s=v.get('sequences',{}).get(r['state'],{})
        for key in ('loop_or_transition','local_body_motion','identity_continuity','no_whole_sprite_fake_motion'):
            if s.get(key)!='PASS': raise GateError(f'SEQUENCE_REVIEW_PENDING: {r["state"]}/{key}')
        if not s.get('reviewed_by'): raise GateError('SEQUENCE_REVIEWER_MISSING')
        for aid in r['asset_ids']:
            if s.get('reviewed_asset_hashes',{}).get(aid)!=catalog[aid]['sha256']: raise GateError('SEQUENCE_REVIEW_HASH_MISMATCH:'+aid)
    if p['rows']==11 and v.get('gaze_cycle_16',{}).get('continuity')!='PASS': raise GateError('FULL_16_GAZE_CYCLE_REVIEW_PENDING')
    image=Image.new('RGBA',tuple(p['canvas']),(0,0,0,0));cw,ch=p['cell']
    for r in p['row_definitions']:
        for col,aid in enumerate(r['asset_ids']):
            image.alpha_composite(render_cell(safe(root,catalog[aid]['path']),p),(col*cw,r['row']*ch))
    output=safe(root,output_rel)
    if output.exists(): raise GateError('OUTPUT_EXISTS_NO_OVERWRITE')
    output.parent.mkdir(parents=True,exist_ok=True)
    image.save(output,optimize=True)
    if output.stat().st_size>p['max_bytes']:
        output.unlink();raise GateError('ATLAS_EXCEEDS_TARGET_SIZE_LIMIT')
    receipt={'status':'ATLAS_COMPILED_NOT_INSTALLED','profile':name,'profile_sha256':profile_hash(p),'path':output_rel,'sha256':digest(output),'bytes':output.stat().st_size,'canvas':p['canvas'],'required_slots':p['required_slots'],'transparent_empty_slots':p['transparent_empty_slots'],'pets_preflight':'NOT_RUN','pets_created':False,'pet_selected':False,'custom_voice':False,'twos_connected':False}
    output.with_suffix('.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    return receipt

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    sub=parser.add_subparsers(dest='command',required=True)
    i=sub.add_parser('inspect');i.add_argument('image',type=Path)
    a=sub.add_parser('audit');a.add_argument('--subset',choices=['p0','all'],default='p0');a.add_argument('--require-visual',action='store_true');a.add_argument('--report',type=Path)
    s=sub.add_parser('profile');s.add_argument('name')
    b=sub.add_parser('build');b.add_argument('--profile',required=True);b.add_argument('--output',required=True,help='Relative package path; never overwrites')
    args=parser.parse_args();root=args.root.resolve()
    try:
        if args.command=='inspect': result=inspect(args.image);code=0 if result['structural_pass'] else 2
        elif args.command=='audit':
            ids=p0_ids(root) if args.subset=='p0' else [a['id'] for a in load(root/'specs/assets_required.json')['assets']]
            result=run_audit(root,ids,args.require_visual);code=0 if result['status']!='BLOCKED' else 2
            if args.report:
                # Explicit report path is a caller-selected local output, never implicitly in the source repo.
                args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        elif args.command=='profile':
            p=load(root/'specs/pets_layout_profiles.json')['profiles'][args.name];result={'profile':p,'profile_sha256':profile_hash(p),'layout_errors':layout_check(p)};code=0 if not result['layout_errors'] else 2
        else: result=build(root,args.profile,args.output);code=0
        print(json.dumps(result,ensure_ascii=False,indent=2));return code
    except (GateError,KeyError,ValueError,OSError) as ex:
        print(json.dumps({'status':'BLOCKED','reason':str(ex)},ensure_ascii=False,indent=2));return 2

if __name__=='__main__': sys.exit(main())
