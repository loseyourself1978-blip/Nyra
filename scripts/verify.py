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
    assert manifest['mode'] == 'R3_INTERACTIVE_COMPANION'
    for entry in manifest['outfits']:
        p = ROOT/'assets'/entry['file']
        assert digest(p) == entry['sha256']
        assert p.read_bytes() == (APP/'Contents/Resources/assets'/entry['file']).read_bytes()
        if entry['id'] == 'runtime-default':
            assert entry['runtimeReady'] and entry['anchor'] == [512,1444]
        elif entry['id'] == 'runtime-office':
            assert not entry['runtimeReady'] and entry['classification'] == 'STATIC_OUTFIT_ONLY'
            assert entry['anchor'] == [512,1444]
        else:
            assert not entry['runtimeReady'] and entry['anchor'] is None
    assert (ROOT/'assets/outfits.json').read_bytes() == (APP/'Contents/Resources/assets/outfits.json').read_bytes()
    checks.append('3 unchanged reference outfits, 1 true P0 runtime outfit, 1 static office outfit match packaged bytes')
    production = ROOT/'production-r2'
    plan = json.loads((production/'specs/standalone_p0.json').read_text())
    ids = {x for s in plan['sequences'].values() for x in s['asset_ids']}
    assert len(ids) == 20
    assert sum(len(s['asset_ids']) for s in plan['sequences'].values()) == 23
    assert (production/'specs/standalone_p0.json').read_bytes() == (APP/'Contents/Resources/runtime/standalone_p0.json').read_bytes()
    for asset_id in ids:
        assert (production/'runtime/default'/f'{asset_id}.png').read_bytes() == (APP/'Contents/Resources/runtime/default'/f'{asset_id}.png').read_bytes()
    checks.append('20 real P0 PNGs and 23-slot frame plan match exact application resources')
    extended = json.loads((ROOT/'production-r3/specs/standalone_r3.json').read_text())
    extended_ids = {x for seq in extended['sequences'].values() for x in seq['asset_ids']}
    assert len(extended_ids) == 77 and len(extended['sequences']) == 12
    assert sum(len(seq['asset_ids']) for seq in extended['sequences'].values()) == 84
    assert (ROOT/'production-r3/specs/standalone_r3.json').read_bytes() == (APP/'Contents/Resources/runtime/standalone_r3.json').read_bytes()
    for asset_id in extended_ids:
        assert (production/'runtime/default'/f'{asset_id}.png').read_bytes() == (APP/'Contents/Resources/runtime/default'/f'{asset_id}.png').read_bytes()
    checks.append('All 77 default native art frames / 84 slots / 12 sequences match packaged resources')
    audio = json.loads((ROOT/'audio/provenance.json').read_text())
    for row in audio['files']:
        assert digest(ROOT/'audio'/row['file']) == row['sha256']
        assert digest(APP/'Contents/Resources/audio'/row['file']) == row['sha256']
    checks.append('Two original procedural chimes match packaged audio hashes')
    for args, title in [
        (['codesign','--verify','--deep','--strict',str(APP)], 'exact application signature verifies'),
        ([str(APP/'Contents/MacOS/NyraPreview'),'--self-test'], 'native window and runtime sequence checks'),
    ]:
        p = subprocess.run(args,capture_output=True,text=True,check=True)
        checks.append(title+(': '+p.stdout.strip() if p.stdout.strip() else ''))
    arch = subprocess.run(['lipo','-archs',str(APP/'Contents/MacOS/NyraPreview')], capture_output=True,text=True,check=True).stdout.split()
    assert set(arch) == {'arm64','x86_64'}
    checks.append('universal binary contains arm64 and x86_64')
    result = dict(status='PASS_SCOPED_RELEASE_CHECKS', checks=checks,
                  executable_sha256=digest(APP/'Contents/MacOS/NyraPreview'),
                  not_claimed=['animated office wardrobe','pixel-perfect silhouette hit testing (64x96 sampled alpha is tested)','Live TWOS integration',
                               'custom AI voice (deferred by user)','Owner Acceptance','Intel runtime validation'])
    (ROOT/'production-r3/reports/build-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
