#!/usr/bin/env python3
"""Offline universal macOS app build; uses only the installed Apple toolchain."""
from pathlib import Path
import json
import os
import plistlib
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / '夜璃 Nyra Preview.app'
BUILD = ROOT / '.build'


def run(args):
    subprocess.run([str(x) for x in args], check=True, cwd=ROOT)


def main():
    BUILD.mkdir(exist_ok=True)
    contents = APP / 'Contents'
    (contents / 'MacOS').mkdir(parents=True, exist_ok=True)
    resources = contents / 'Resources'
    resources.mkdir(exist_ok=True)
    for p in (ROOT / 'assets').glob('*'):
        if p.is_file():
            (resources / 'assets').mkdir(exist_ok=True)
            shutil.copy2(p, resources / 'assets' / p.name)
    runtime = resources / 'runtime'
    runtime.mkdir(exist_ok=True)
    plan = json.loads((ROOT / 'production-r3/specs/standalone_r3.json').read_text())
    ids = {i for s in plan['sequences'].values() for i in s['asset_ids']}
    packaged_frames = runtime / 'default'
    packaged_frames.mkdir(exist_ok=True)
    for old in packaged_frames.glob('*.png'):
        if old.stem not in ids:
            old.unlink()  # disposable bundled copy only; preserve original artwork
    for asset_id in ids:
        if not asset_id.replace('_', '').isalnum():
            raise ValueError('Invalid frame ID')
        shutil.copy2(ROOT / 'production-r2/runtime/default' / f'{asset_id}.png', packaged_frames / f'{asset_id}.png')
    shutil.copy2(ROOT / 'production-r3/specs/standalone_r3.json', runtime / 'standalone_r3.json')
    shutil.copy2(ROOT / 'production-r2/specs/standalone_p0.json', runtime / 'standalone_p0.json')
    shutil.copytree(ROOT / 'audio', resources / 'audio', dirs_exist_ok=True)
    info = dict(CFBundleName='夜璃 · Nyra', CFBundleDisplayName='夜璃 · Nyra',
                CFBundleIdentifier='local.nyra.companion.preview', CFBundleExecutable='NyraPreview',
                CFBundlePackageType='APPL', CFBundleShortVersionString='0.3.0', CFBundleVersion='3',
                LSMinimumSystemVersion='13.0', LSUIElement=True, NSHighResolutionCapable=True,
                NSPrincipalClass='NSApplication', CFBundleDevelopmentRegion='zh_CN',
                LSMultipleInstancesProhibited=True)
    (contents / 'Info.plist').write_bytes(plistlib.dumps(info))
    sources = sorted((ROOT / 'Sources').glob('*.swift'))
    archs = ['arm64', 'x86_64']
    for arch in archs:
        run(['xcrun', 'swiftc', '-swift-version', '5', '-O', '-target', arch+'-apple-macos13.0',
             '-module-cache-path', BUILD / 'module-cache', '-framework', 'AppKit', '-framework', 'AVFoundation',
             *sources, '-o', BUILD / ('NyraPreview-'+arch)])
    run(['lipo', '-create', *(BUILD / ('NyraPreview-'+a) for a in archs),
         '-output', contents / 'MacOS/NyraPreview'])
    run(['codesign', '--force', '--sign', '-', APP])
    run(['codesign', '--verify', '--deep', '--strict', APP])
    print(APP)


if __name__ == '__main__':
    main()
