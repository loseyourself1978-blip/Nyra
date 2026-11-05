#!/usr/bin/env python3
"""Append two reviewed native frame sets without changing accepted wardrobe pixels."""
import argparse
import copy
import json
import shutil
from pathlib import Path
from prepare_release import measure, seq, sha

ROOT = Path(__file__).resolve().parents[1]
NAMES = {"office_white": "白衬衫 / White blouse", "gala_red": "红礼服 / Ruby gown"}
STANDING = ("neutral", "blink", "head", "left", "right", "work", "workblink",
            "crouch", "jump", "rise", "run_left_1", "run_left_2", "run_right_1", "run_right_2")
RECLINING = ("neutral", "blink", "work", "workblink", "gaze", "celebrate")


def make_set(outfit, reclining):
    folder = ("recline_" if reclining else "") + outfit
    prefix = "nyra_" + outfit + ("_recline_" if reclining else "_")
    def s(frames, ms, loop=False):
        return seq([prefix + f for f in frames], ms, loop)
    common = {
        "idle": s(["neutral", "blink", "neutral"], [3000, 160, 1800], True),
        "working": s(["work", "workblink", "work"], [2400, 160, 1400], True),
        "review": s(["work", "workblink", "work"], [2400, 160, 1400], True),
    }
    if reclining:
        common.update({
            "waiting": s(["gaze", "neutral"], [1800, 1400], True),
            "look_around": s(["neutral", "gaze", "neutral"], [200, 600, 200]),
            "verified_success": s(["neutral", "celebrate", "neutral"], [150, 1000, 350]),
            "settle": s(["blink", "neutral"], [160, 400]),
        })
        for name in ("head", "left", "right"):
            common["gaze_" + name] = s(["gaze", "neutral"], [700, 350])
    else:
        common.update({
            "waiting": s(["head", "neutral"], [1800, 1400], True),
            "look_around": s(["left", "neutral", "right", "neutral"], [300, 150, 300, 150]),
            "drag": s(["run_right_1", "run_right_2"], [180, 180], True),
            "settle": s(["crouch", "neutral"], [180, 400]),
            "rise": s(["rise", "neutral"], [280, 40]),
            "lower": s(["neutral", "rise"], [40, 280]),
            "jumping": s(["neutral", "crouch", "jump", "crouch", "neutral"], [100, 140, 280, 160, 160]),
            "verified_success": s(["neutral", "crouch", "jump", "neutral"], [100, 180, 440, 200]),
        })
        for direction in ("left", "right"):
            common["running_" + direction] = s(["run_" + direction + "_1", "run_" + direction + "_2"], [180, 180], True)
        for name in ("head", "left", "right"):
            common["gaze_" + name] = s([name, "neutral"], [700, 350])
    return dict(folder=folder, neutral=prefix+"neutral",
                width=1536 if reclining else 1024, height=1024 if reclining else 1536,
                bbox=[0, 0, 1, 1], sequences=common,
                frame_scales={} if reclining else {prefix+"rise": 0.72, prefix+"crouch": 0.72},
                capabilities="Native full-body RGBA animation; standing and reclining use the same outfit. No rotated standing-art substitute.")


def assemble(candidates, root=ROOT):
    candidates = Path(candidates)
    root = Path(root)
    specs = root / "production-1.0/specs"
    runtime = json.loads((specs / "runtime.json").read_text())
    resources = json.loads((specs / "resources.json").read_text())
    wardrobe = json.loads((specs / "outfits.json").read_text())
    if runtime["schemaVersion"] not in (5, 6):
        raise ValueError("Only the established three/five outfit manifest can be extended")
    original_sets = {k: copy.deepcopy(v) for k,v in runtime["sets"].items()
                     if k in {"default","office","gala","recline","recline_office","recline_gala"}}
    if len(original_sets) != 6:
        raise ValueError("Accepted wardrobe sets are incomplete")
    pending, records, new_sets = [], {}, {}
    # Validate all inputs before copying or changing any manifest. Never edit pixels.
    for outfit in NAMES:
        for reclining, frames in ((False, STANDING), (True, RECLINING)):
            set_ = make_set(outfit, reclining)
            boxes = []
            for frame in frames:
                source = candidates / outfit / (("recline_" if reclining else "") + frame + ".png")
                if source.is_symlink() or not source.is_file():
                    raise ValueError("Missing regular native frame: " + str(source))
                m = measure(source)
                if m["native_size"] != [set_["width"], set_["height"]]:
                    raise ValueError("Native dimensions differ: " + str(source))
                prefix = "nyra_" + outfit + ("_recline_" if reclining else "_")
                relative = set_["folder"] + "/" + prefix + frame + ".png"
                dest = root / "production-1.0/runtime" / relative
                records[relative] = dict(source=dest.relative_to(root).as_posix(),
                    sha256=sha(source), bytes=source.stat().st_size, **m)
                pending.append((source, dest))
                boxes.append(m["bbox_top_origin"])
            x, top = min(b[0] for b in boxes), min(b[1] for b in boxes)
            right, bottom = max(b[2] for b in boxes), max(b[3] for b in boxes)
            set_["bbox"] = [x, set_["height"]-bottom, right-x, bottom-top]
            new_sets[set_["folder"]] = set_
    for source, dest in pending:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    for outfit, name in NAMES.items():
        preview = root / "assets" / ("runtime-" + outfit + ".png")
        shutil.copy2(candidates / outfit / "neutral.png", preview)
        item = dict(id="runtime-"+outfit, name=name, file=preview.name,
                    note="Native animated wardrobe · standing and reclining",
                    width=1024, height=1536, runtimeReady=True,
                    classification="NATIVE_RUNTIME", sha256=sha(preview))
        index = next((i for i,x in enumerate(wardrobe["outfits"]) if x["id"] == item["id"]), None)
        if index is None:
            wardrobe["outfits"].append(item)
        else:
            wardrobe["outfits"][index] = item
    runtime["schemaVersion"] = 6
    runtime["sets"].update(new_sets)
    resources["files"].update(records)
    wardrobe["wardrobeStatus"] = "FIVE_OUTFIT_STANDING_AND_RECLINING"
    assert all(runtime["sets"][k] == v for k,v in original_sets.items())
    for name, data in (("runtime", runtime), ("resources", resources), ("outfits", wardrobe)):
        (specs / (name+".json")).write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n")
    return dict(new_native_frames=len(records), outfits=len(wardrobe["outfits"]),
                runtime_sets=len(runtime["sets"]), preserved_existing_sets=sorted(original_sets))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True)
    args = parser.parse_args()
    print(json.dumps(assemble(args.candidates)))
