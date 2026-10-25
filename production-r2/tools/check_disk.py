"""Run before each image generation and archive job; never deletes user data."""
from pathlib import Path
import json, shutil, sys
root=Path(__file__).resolve().parents[1]
free=shutil.disk_usage(root).free
ok=free>=2*1024**3
print(json.dumps(dict(status='READY' if ok else 'PAUSED_LOW_DISK',free_bytes=free,minimum_free_bytes=2*1024**3)))
sys.exit(0 if ok else 2)
