#!/usr/bin/env python3
"""Offline PNG header/hash audit. No image edits, no network, no automatic PASS.
Usage: python3 audit_assets.py /path/to/actual/runtime/assets
Pillow is optional: without it alpha coverage stays NOT_MEASURED.
"""
from pathlib import Path
import sys, json, struct, hashlib

def audit(p):
    b=p.read_bytes()
    if b[:8]!=b"\x89PNG\r\n\x1a\n" or len(b)<33:
        return {"file":str(p),"error":"NOT_A_VALID_PNG_HEADER"}
    w,h,depth,ct,compression,flt,interlace=struct.unpack(">IIBBBBB",b[16:29])
    out={"file":str(p),"sha256":hashlib.sha256(b).hexdigest(),
         "width":w,"height":h,"bit_depth":depth,"color_type":ct,
         "alpha_channel_in_header":ct in (4,6),"alpha_coverage":"NOT_MEASURED",
         "visual_identity_crop_anchor_review":"REQUIRED"}
    try:
        from PIL import Image
        with Image.open(p) as im:
            im.load()
            out["decoded"]=True
            alpha=im.convert("RGBA").getchannel("A")
            hist=alpha.histogram();total=w*h
            out["transparent_fraction"]=round(hist[0]/total,6)
            out["nonopaque_fraction"]=round(sum(hist[:-1])/total,6)
            out["alpha_coverage"]="MEASURED"
            out["fully_opaque_warning"]=hist[255]==total
    except ImportError:
        out["note"]="Pillow not installed; no dependencies installed by this script."
    except Exception as e:
        out["decode_error"]=str(e)
    return out

def main():
    if len(sys.argv)!=2:
        raise SystemExit("Usage: audit_assets.py DIRECTORY")
    root=Path(sys.argv[1]).resolve()
    if not root.is_dir(): raise SystemExit("Directory does not exist")
    results=[audit(p) for p in sorted(root.rglob("*.png")) if p.is_file()]
    print(json.dumps({"kind":"OFFLINE_ASSET_AUDIT_NOT_VISUAL_ACCEPTANCE", "assets":results},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
