#!/usr/bin/env python3
"""Meaningful release checks against the exact app and supplied source bytes."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT/'夜璃 Nyra Preview.app'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    checks = []
    audit = json.loads((ROOT/'reports/asset-audit.json').read_text())
    source = ROOT/'source-handoff/TWOS_COMPANION_V3_HANDOFF_R1'
    for entry in audit['assets']:
        assert digest(source/entry['file']) == entry['sha256'], entry['file']
    checks.append('12 supplied image hashes unchanged')
    for check in audit['handoff_manifest_checks']:
        assert check['matches']
    checks.append('26 supplied manifest checks recorded successful')
    manifest = json.loads((ROOT/'assets/outfits.json').read_text())
    assert manifest['mode'] == 'STATIC_PREVIEW'
    for entry in manifest['outfits']:
        p = ROOT/'assets'/entry['file']
        assert digest(p) == entry['sha256']
        assert p.read_bytes() == (APP/'Contents/Resources/assets'/entry['file']).read_bytes()
        assert not entry['runtimeReady'] and entry['anchor'] is None
    assert (ROOT/'assets/outfits.json').read_bytes() == (APP/'Contents/Resources/assets/outfits.json').read_bytes()
    checks.append('3 reference outfits match the exact packaged bytes; none falsely runtime-ready')
    for args, title in [
        (['codesign','--verify','--deep','--strict',str(APP)], 'exact application signature verifies'),
        ([str(APP/'Contents/MacOS/NyraPreview'),'--self-test'], '7 native core checks'),
    ]:
        p = subprocess.run(args,capture_output=True,text=True,check=True)
        checks.append(title+(': '+p.stdout.strip() if p.stdout.strip() else ''))
    arch = subprocess.run(['lipo','-archs',str(APP/'Contents/MacOS/NyraPreview')], capture_output=True,text=True,check=True).stdout.split()
    assert set(arch) == {'arm64','x86_64'}
    checks.append('universal binary contains arm64 and x86_64')
    result = dict(status='PASS_SCOPED_RELEASE_CHECKS', checks=checks,
                  executable_sha256=digest(APP/'Contents/MacOS/NyraPreview'),
                  not_claimed=['full animated pet','silhouette alpha hit testing','Live TWOS integration',
                               'custom voice','Owner Acceptance','Intel runtime validation'])
    (ROOT/'reports/build-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
