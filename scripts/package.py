#!/usr/bin/env python3
"""Pack complete deliverables, never local preferences, Git internals or build caches."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OMIT = {'.git', '.build', '.local', '__pycache__', 'dist'}


def included(path):
    relative = path.relative_to(ROOT)
    return path.is_file() and not any(part in OMIT for part in relative.parts) and path.name != '.DS_Store'


def main():
    manifest = ROOT/'RELEASE_MANIFEST.sha256'
    files = sorted(p for p in ROOT.rglob('*') if included(p) and p != manifest)
    manifest.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
    files.append(manifest)
    dist = ROOT/'dist'
    dist.mkdir(exist_ok=True)
    target = dist/'Nyra-R1.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for p in files:
            archive.write(p, Path('Nyra')/p.relative_to(ROOT))
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(files)
        executable = archive.getinfo('Nyra/夜璃 Nyra Preview.app/Contents/MacOS/NyraPreview')
        assert (executable.external_attr >> 16) & 0o111
        assert not any('/.local/' in name or '/.git/' in name or '/.build/' in name for name in archive.namelist())
    delivery = ROOT.parent/'夜璃-Nyra-R1.zip'
    shutil.copy2(target, delivery)
    checksum = hashlib.sha256(target.read_bytes()).hexdigest()
    (dist/'Nyra-R1.zip.sha256').write_text(checksum+'  Nyra-R1.zip\n')
    delivery.with_suffix('.zip.sha256').write_text(checksum+'  '+delivery.name+'\n')
    result = dict(file=str(delivery), project_archive='dist/Nyra-R1.zip', files=len(files),
                  bytes=target.stat().st_size, sha256=checksum)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
