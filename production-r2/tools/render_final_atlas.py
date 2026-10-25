"""Render review media from the exact encoded atlas; never invent artwork."""
from pathlib import Path
import hashlib,json,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'bundled-run'
sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
from render_animation_previews import ROW_DURATIONS, save_preview
atlas_path=RUN/'final/spritesheet-extended.webp'
atlas=Image.open(atlas_path).convert('RGBA')
assert atlas.size==(1536,2288)
out=RUN/'previews';out.mkdir(exist_ok=True)
frames_root=RUN/'final-frames';frames_root.mkdir(exist_ok=True)
profile=json.loads((ROOT/'specs/pets_layout_profiles.json').read_text())['profiles']['pets_v2_attachment_provisional']
rows=profile['row_definitions'];cells={};timeline=[]
for ri,row in enumerate(rows):
    cells[row['state']]=[]
    for i in range(len(row['asset_ids'])):
        cell=atlas.crop((i*192,ri*208,(i+1)*192,(ri+1)*208))
        p=frames_root/row['state']/f'{i:02d}.png';p.parent.mkdir(exist_ok=True);cell.save(p)
        cells[row['state']].append(cell)
        tile=Image.new('RGB',(384,448),'#30283d');tile.paste(cell.resize((384,416)),(0,0),cell.resize((384,416)))
        ImageDraw.Draw(tile).text((8,423),f'{row["state"]}  {i+1}/{len(row["asset_ids"])}',fill='white')
        duration=ROW_DURATIONS.get(row['state'],[200]*8)[i]
        timeline.append((tile,duration))
gaze=cells[rows[9]['state']]+cells[rows[10]['state']]
save_preview(gaze,[200]*16,out/'look-loop.gif')
transition=cells['idle']+cells['jumping']+cells['idle']
save_preview(transition,ROW_DURATIONS['idle']+ROW_DURATIONS['jumping']+ROW_DURATIONS['idle'],out/'idle-jump-idle.gif')
timeline[0][0].save(out/'all-states.gif',save_all=True,append_images=[im for im,_ in timeline[1:]],duration=[t for _,t in timeline],loop=0,disposal=2)
still=Image.new('RGB',(4*384,448),'#30283d')
for j,idx in enumerate([0,10,34,57]):still.paste(timeline[idx][0],(384*j,0))
still.save(out/'four-stills.png')
proof=dict(atlas=str(atlas_path),sha256=hashlib.sha256(atlas_path.read_bytes()).hexdigest(),
           extraction='Exact 192x208 cells from final encoded atlas',populated_cells=len(timeline),
           generated_art=False,simulation=True,twos_connected=False,host_playback=False)
(out/'media-provenance.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof))
