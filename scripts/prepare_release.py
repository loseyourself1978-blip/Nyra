"""Assemble Nyra 1.0 manifests from native RGBA originals; never edits pixels."""
from pathlib import Path
import copy,hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'production-1.0'
def seq(ids,durations,loop=False): return dict(asset_ids=ids,durations_ms=durations,loop=loop)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def measure(p):
    with Image.open(p) as im:
        assert im.mode=='RGBA',p
        a=im.getchannel('A');box=a.point(lambda x:255 if x>32 else 0).getbbox();hist=a.histogram()
        assert box and hist[0]>0 and sum(hist[250:])>0,p
        return dict(native_size=list(im.size),bbox_top_origin=list(box),alpha_min=a.getextrema()[0],alpha_max=a.getextrema()[1],zero_alpha_pixels=hist[0],alpha_ge_250_pixels=sum(hist[250:]))
def main():
    old=json.loads((ROOT/'production-r4/specs/r4.json').read_text());sets=copy.deepcopy(old['sets']);sets.pop('recline')
    sources={}
    for key,set_ in sets.items():
        for id_ in {i for s in set_['sequences'].values() for i in s['asset_ids']}:
            source=ROOT/('production-r2/runtime/default' if key=='default' else 'production-r4/runtime/'+key)/(id_+'.png')
            sources[key+'/'+id_+'.png']=source
    for p in (OUT/'runtime').rglob('*.png'): sources[p.relative_to(OUT/'runtime').as_posix()]=p
    for outfit in ['default','office','gala']:
        pre='nyra_'+outfit+'_';set_=sets[outfit];neutral=set_['neutral'];rise=pre+'rise'
        set_['sequences']['rise']=seq([rise,neutral],[280,40])
        set_['sequences']['lower']=seq([neutral,rise],[40,280])
        if outfit!='default':
            q=set_['sequences'];crouch=pre+'crouch';jump=pre+'jump'
            for d in ['left','right']:q['running_'+d]=seq([pre+'run_'+d+'_1',pre+'run_'+d+'_2'],[180,180],True)
            q['jumping']=seq([neutral,crouch,jump,crouch,neutral],[100,140,280,160,160])
            q['verified_success']=seq([neutral,crouch,jump,neutral],[100,180,440,200])
            q['settle']=seq([crouch,neutral],[180,400])
            q['review']=q['working'];q['look_around']=seq([pre+'left',neutral,pre+'right',neutral],[300,150,300,150])
        set_['capabilities']='Native standing animation; same-outfit rise/lower and directional run/jump. Unsupported menu actions disabled.'
        set_['frame_scales']={rise:0.72}
        folder='recline_'+outfit;pre='nyra_'+outfit+'_recline_'
        if outfit=='default':
            for kind in ['neutral','blink']:sources[folder+'/'+pre+kind+'.png']=ROOT/'production-r4/runtime/stage'/('nyra_recline_'+kind+'.png')
        neutral=pre+'neutral';blink=pre+'blink';work=pre+'work';workblink=pre+'workblink';gaze=pre+'gaze';celebrate=pre+'celebrate'
        sets['recline' if outfit=='default' else folder]=dict(folder=folder,neutral=neutral,width=1536,height=1024,bbox=[0,0,1,1],frame_scales={},capabilities='Full native reclining art: idle/blink, gaze, working/reading, waiting and once-only celebration; run/jump use same-outfit rise/action/lower.',sequences={
            'idle':seq([neutral,blink,neutral],[3000,160,1800],True),
            'working':seq([work,workblink,work],[2400,160,1400],True),
            'review':seq([work,workblink,work],[2400,160,1400],True),
            'waiting':seq([gaze,neutral],[1800,1400],True),
            'gaze_head':seq([gaze,neutral],[700,350]),
            'gaze_left':seq([gaze,neutral],[700,350]),
            'gaze_right':seq([gaze,neutral],[700,350]),
            'look_around':seq([neutral,gaze,neutral],[200,600,200]),
            'verified_success':seq([neutral,celebrate,neutral],[150,1000,350]),
            'settle':seq([blink,neutral],[160,400])})
    records={}
    for key,set_ in sets.items():
        ids={i for q in set_['sequences'].values() for i in q['asset_ids']}
        boxes=[]
        for i in sorted(ids):
            rel=set_['folder']+'/'+i+'.png';p=sources[rel];assert p.is_file(),p
            m=measure(p);assert m['native_size']==[set_['width'],set_['height']],(p,m['native_size'])
            boxes.append(m['bbox_top_origin']);records[rel]=dict(source=p.relative_to(ROOT).as_posix(),sha256=sha(p),bytes=p.stat().st_size,**m)
        x=min(b[0] for b in boxes);top=min(b[1] for b in boxes);right=max(b[2] for b in boxes);bottom=max(b[3] for b in boxes)
        set_['bbox']=[x,set_['height']-bottom,right-x,bottom-top]
    (OUT/'specs').mkdir(parents=True,exist_ok=True)
    (OUT/'specs/runtime.json').write_text(json.dumps(dict(schemaVersion=5,sets=sets),ensure_ascii=False,indent=2))
    (OUT/'specs/resources.json').write_text(json.dumps(dict(schema=1,files=records),indent=2))
    wardrobe=json.loads((ROOT/'assets/outfits.json').read_text());wardrobe['mode']='NYRA_1_0_REACTIVE';wardrobe['wardrobeStatus']='THREE_OUTFIT_STANDING_AND_RECLINING'
    for outfit in wardrobe['outfits']:outfit['name']={'runtime-default':'黑紫 / Black & purple','runtime-office':'职场 / Office','runtime-gala':'晚礼服 / Gala'}[outfit['id']];outfit['note']='Native animated wardrobe · standing and reclining';outfit['classification']='NATIVE_RUNTIME';outfit['runtimeReady']=True
    (OUT/'specs/outfits.json').write_text(json.dumps(wardrobe,ensure_ascii=False,indent=2))
    print('Runtime sets:',len(sets),'native files:',len(records),'bytes:',sum(x['bytes'] for x in records.values()))
if __name__=='__main__':main()
