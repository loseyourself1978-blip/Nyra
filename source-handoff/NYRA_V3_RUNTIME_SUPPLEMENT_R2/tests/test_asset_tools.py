"""Synthetic infrastructure tests ONLY; never a character/animation acceptance."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('nyra_assets',ROOT/'tools/nyra_assets.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class AssetToolsTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name)
 def tearDown(self): self.tmp.cleanup()
 def image(self,name='a.png',mode='RGBA',solid=False):
  im=Image.new(mode,(1024,1536),(220,220,220,255) if solid else (0,0,0,0))
  if not solid: ImageDraw.Draw(im).ellipse((300,180,720,1430),fill=(90,45,120,255))
  p=self.d/name;im.save(p);return p
 def test_true_alpha_structural_only(self): self.assertTrue(m.inspect(self.image())['structural_pass'])
 def test_opaque_background_rejected(self): self.assertFalse(m.inspect(self.image(solid=True))['structural_pass'])
 def test_empty_rejected(self):
  p=self.d/'empty.png';Image.new('RGBA',(1024,1536)).save(p);self.assertIn('EMPTY_IMAGE',m.inspect(p)['errors'])
 def test_fake_translucent_poster_rejected(self):
  p=self.d/'poster.png';Image.new('RGBA',(1024,1536),(200,180,190,252)).save(p);r=m.inspect(p);self.assertIn('NO_ADEQUATE_OPAQUE_CHARACTER_CORE',r['errors'])
 def test_wrong_size_rejected(self):
  p=self.d/'small.png';Image.new('RGBA',(302,517)).save(p);self.assertIn('NATIVE_CANVAS_MISMATCH',m.inspect(p)['errors'])
 def test_edge_content_rejected(self):
  p=self.image();im=Image.open(p);im.putpixel((0,50),(1,2,3,255));im.save(p);self.assertIn('CANVAS_EDGE_NOT_CLEAR',m.inspect(p)['errors'])
 def test_unsafe_relative_path(self):
  with self.assertRaises(m.GateError): m.safe(self.d,'../outside.png')
 def test_unsafe_symlink(self):
  (self.d/'link').symlink_to('/tmp');
  with self.assertRaises(m.GateError): m.safe(self.d,'link/outside.png')
 def test_source_profiles_counts(self):
  p=m.load(ROOT/'specs/pets_layout_profiles.json')['profiles'];self.assertEqual(m.layout_check(p['pets_v2_attachment_provisional']),[]);self.assertEqual(m.layout_check(p['web_9row_candidate_unconfirmed']),[])
 def test_bad_layout(self):
  p=m.load(ROOT/'specs/pets_layout_profiles.json')['profiles']['pets_v2_attachment_provisional'];p['canvas'][1]=1872;self.assertTrue(m.layout_check(p))
 def test_missing_assets_are_blocked(self):
  r=m.run_audit(ROOT,m.p0_ids(ROOT));self.assertEqual(r['status'],'BLOCKED');self.assertEqual(r['present_assets'],0);self.assertEqual(r['required_unique_assets'],20)
 def test_no_installable_placeholder_generated(self):
  with self.assertRaises(m.GateError): m.build(ROOT,'pets_v2_attachment_provisional','runtime/SHOULD_NOT_EXIST.png')
  self.assertFalse((ROOT/'runtime/SHOULD_NOT_EXIST.png').exists())
 def test_cells_are_fixed_uniform_transform(self):
  p=m.load(ROOT/'specs/pets_layout_profiles.json')['profiles']['pets_v2_attachment_provisional'];t=m.render_cell(self.image(),p);self.assertEqual(t.size,(192,208));self.assertTrue(t.getchannel('A').getbbox());self.assertEqual(t.getpixel((0,0))[3],0)
 def test_file_decode_error_is_reported(self):
  p=self.d/'bad.png';p.write_text('not an image');self.assertTrue(any(e.startswith('DECODE_ERROR') for e in m.inspect(p)['errors']))
 def test_shared_neutral_frame_is_declared(self):
  p=m.load(ROOT/'specs/standalone_p0.json');self.assertEqual(p['required_frame_slots'],23);self.assertEqual(p['sequences']['verified_success']['asset_ids'][0],p['sequences']['verified_success']['asset_ids'][-1]);self.assertEqual(len(m.p0_ids(ROOT)),20)
if __name__=='__main__':unittest.main(verbosity=2)
