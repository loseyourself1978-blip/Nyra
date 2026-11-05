"""Checks the shipped native resources and action coverage, not simulated UI acceptance."""
import hashlib
import json
import sys
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from extend_wardrobe import NAMES, STANDING, RECLINING, make_set


class ExtendedWardrobeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runtime = json.loads((ROOT/"production-1.0/specs/runtime.json").read_text())
        cls.resources = json.loads((ROOT/"production-1.0/specs/resources.json").read_text())["files"]
        cls.wardrobe = json.loads((ROOT/"production-1.0/specs/outfits.json").read_text())

    def test_existing_selection_order_and_complete_pose_pairs(self):
        ids = [x["id"] for x in self.wardrobe["outfits"]]
        self.assertEqual(ids[:3], ["runtime-default", "runtime-office", "runtime-gala"])
        self.assertEqual(ids[3:], ["runtime-office_white", "runtime-gala_red"])
        self.assertEqual(len(self.runtime["sets"]), 10)
        for key in NAMES:
            self.assertIn(key, self.runtime["sets"])
            self.assertIn("recline_"+key, self.runtime["sets"])

    def test_new_frames_are_unique_native_transparent_files_with_matching_hashes(self):
        hashes = set()
        for outfit in NAMES:
            for reclining, frames in ((False, STANDING), (True, RECLINING)):
                folder = ("recline_" if reclining else "") + outfit
                prefix = "nyra_"+outfit+("_recline_" if reclining else "_")
                for frame in frames:
                    record = self.resources[folder+"/"+prefix+frame+".png"]
                    path = ROOT / record["source"]
                    digest = hashlib.sha256(path.read_bytes()).hexdigest()
                    self.assertEqual(digest, record["sha256"])
                    self.assertNotIn(digest, hashes)
                    hashes.add(digest)
                    with Image.open(path) as image:
                        self.assertEqual(image.mode, "RGBA")
                        self.assertEqual(image.size, (1536,1024) if reclining else (1024,1536))
                        histogram = image.getchannel("A").histogram()
                        self.assertGreater(histogram[0], image.width*image.height//10)
                        self.assertGreater(sum(histogram[250:]), image.width*image.height//10)
        self.assertEqual(len(hashes), 40)

    def test_action_frames_never_cross_outfit_or_pose(self):
        for outfit in NAMES:
            for reclining in (False, True):
                folder = ("recline_" if reclining else "") + outfit
                set_ = self.runtime["sets"][folder]
                expected = make_set(outfit, reclining)
                self.assertEqual(set_["sequences"], expected["sequences"])
                prefix = "nyra_"+outfit+("_recline_" if reclining else "_")
                for sequence in set_["sequences"].values():
                    self.assertEqual(len(sequence["asset_ids"]), len(sequence["durations_ms"]))
                    self.assertTrue(all(0 < ms <= 10000 for ms in sequence["durations_ms"]))
                    for frame in sequence["asset_ids"]:
                        self.assertTrue(frame.startswith(prefix))
                        self.assertIn(folder+"/"+frame+".png", self.resources)
                self.assertTrue(set_["sequences"]["working"]["loop"])
                self.assertFalse(set_["sequences"]["verified_success"]["loop"])

    def test_frame_scaling_and_hit_bounds_fit_native_canvas(self):
        for outfit in NAMES:
            for key in (outfit, "recline_"+outfit):
                set_ = self.runtime["sets"][key]
                x,y,w,h = set_["bbox"]
                self.assertGreater(w, 0); self.assertGreater(h, 0)
                self.assertGreaterEqual(x, 0); self.assertGreaterEqual(y, 0)
                self.assertLessEqual(x+w, set_["width"])
                self.assertLessEqual(y+h, set_["height"])
                self.assertTrue(all(0.25 <= scale <= 1 for scale in set_["frame_scales"].values()))


if __name__ == "__main__":
    unittest.main()
