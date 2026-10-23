#!/usr/bin/env python3
"""Extract to a task-owned temporary folder and verify the delivered signed app."""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    package = ROOT/'dist/Nyra-R1.zip'
    with zipfile.ZipFile(package) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            assert not Path(name).is_absolute() and '..' not in Path(name).parts
    # ditto preserves executable mode on macOS, as the delivered archive requires.
    with tempfile.TemporaryDirectory(prefix='nyra-package-', dir=ROOT.parent.parent/'work') as folder:
        subprocess.run(['ditto','-x','-k',str(package),folder],check=True)
        extracted = Path(folder)/'Nyra'
        count = 0
        for line in (extracted/'RELEASE_MANIFEST.sha256').read_text().splitlines():
            expected, relative = line.split('  ',1)
            assert hashlib.sha256((extracted/relative).read_bytes()).hexdigest() == expected, relative
            count += 1
        app = extracted/'夜璃 Nyra Preview.app'
        subprocess.run(['codesign','--verify','--deep','--strict',str(app)],check=True)
        p = subprocess.run([str(app/'Contents/MacOS/NyraPreview'),'--self-test'],capture_output=True,text=True,check=True)
        print(json.dumps(dict(status='PASS',manifest_files=count,exact_archive_sha256=hashlib.sha256(package.read_bytes()).hexdigest(),
                              extracted_signature='PASS',executable_permission='PASS',core_checks=p.stdout.strip()),ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
