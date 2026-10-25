"""Render genuine PNG sequences and record pixel facts; does not grant visual PASS."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw, ImageChops, ImageStat
from nyra_assets import inspect, p0_ids

ROOT=Path(__file__).resolve().parents[1]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    catalog=json.loads((ROOT/'specs/assets_required.json').read_text())
    plan=json.loads((ROOT/'specs/standalone_p0.json').read_text())
    records=[]
    for a in catalog['assets']:
        p=ROOT/a['path']
        if p.is_file():
            check=inspect(p);records.append(check)
            a.update(status='GENERATED_PENDING_VISUAL_GATE',sha256=check['sha256'],native_resolution_provenance='RECORDED')
    catalog['generated_runtime_asset_count']=len(records)
    (ROOT/'specs/assets_required.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    facts={}
    preview=ROOT/'preview/rendered';preview.mkdir(exist_ok=True)
    for name, seq in plan['sequences'].items():
        frames=[];anchors=[];hashes={}
        for aid in seq['asset_ids']:
            p=ROOT/'runtime/default'/(aid+'.png');im=Image.open(p).convert('RGBA');hashes[aid]=digest(p)
            # Restrict geometric evidence to opaque boots, not hair/tail or faint alpha noise.
            mask=im.getchannel('A').crop((350,1200,650,1536)).point(lambda a:255 if a>=128 else 0)
            bbox=mask.getbbox();anchors.append({'id':aid,'boot_bbox':None if bbox is None else [bbox[0]+350,bbox[1]+1200,bbox[2]+350,bbox[3]+1200]})
            bg=Image.new('RGBA',im.size,'#24202e');bg.alpha_composite(im)
            frames.append(bg.resize((384,576)).convert('RGB'))
        opts={'save_all':True,'append_images':frames[1:],'duration':seq['durations_ms'],'disposal':2}
        if seq['loop']:opts['loop']=0
        frames[0].save(preview/(name+'.gif'),**opts)
        sheet=Image.new('RGB',(len(frames)*192,316),'#24202e');draw=ImageDraw.Draw(sheet)
        for i,f in enumerate(frames):
            sheet.paste(f.resize((192,288)),(i*192,0));draw.text((i*192+5,292),f'{i+1} / {seq["durations_ms"][i]}ms',fill='white')
        sheet.save(preview/(name+'-frames.png'))
        facts[name]={'frame_slots':len(frames),'loop':seq['loop'],'duration_ms':sum(seq['durations_ms']),
            'hashes':hashes,'boot_geometry':anchors,'visual_acceptance':'NOT_AUTOMATIC',
            'adjacent_pixel_mean_difference':[ImageStat.Stat(ImageChops.difference(a,b)).mean for a,b in zip(frames,frames[1:])]}
    ids=p0_ids(ROOT);sheet=Image.new('RGB',(1000,1320),'#e5e1ec');draw=ImageDraw.Draw(sheet)
    for i,aid in enumerate(ids):
        im=Image.open(ROOT/'runtime/default'/(aid+'.png'));bg=Image.new('RGBA',im.size,'#e5e1ec');bg.alpha_composite(im)
        sheet.paste(bg.resize((200,300)).convert('RGB'),((i%5)*200,(i//5)*330));draw.text(((i%5)*200+5,(i//5)*330+303),aid,fill='#22172e')
    sheet.save(ROOT/'reports/p0-contact.png')
    (ROOT/'reports/p0-pixel-checks.json').write_text(json.dumps(records,indent=2)+'\n')
    (ROOT/'reports/p0-sequence-facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    print(json.dumps({'actual_runtime_png':len(records),'all_structural_pass':all(x['structural_pass'] for x in records),'unique_hashes':len(set(x['sha256'] for x in records))}))
if __name__=='__main__':main()
