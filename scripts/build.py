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
    info = dict(CFBundleName='夜璃 · Nyra', CFBundleDisplayName='夜璃 · Nyra',
                CFBundleIdentifier='local.nyra.companion.preview', CFBundleExecutable='NyraPreview',
                CFBundlePackageType='APPL', CFBundleShortVersionString='0.1.0', CFBundleVersion='1',
                LSMinimumSystemVersion='13.0', LSUIElement=True, NSHighResolutionCapable=True,
                NSPrincipalClass='NSApplication', CFBundleDevelopmentRegion='zh_CN',
                LSMultipleInstancesProhibited=True)
    (contents / 'Info.plist').write_bytes(plistlib.dumps(info))
    sources = sorted((ROOT / 'Sources').glob('*.swift'))
    archs = ['arm64', 'x86_64']
    for arch in archs:
        run(['xcrun', 'swiftc', '-swift-version', '5', '-O', '-target', arch+'-apple-macos13.0',
             '-module-cache-path', BUILD / 'module-cache', '-framework', 'AppKit',
             *sources, '-o', BUILD / ('NyraPreview-'+arch)])
    run(['lipo', '-create', *(BUILD / ('NyraPreview-'+a) for a in archs),
         '-output', contents / 'MacOS/NyraPreview'])
    run(['codesign', '--force', '--sign', '-', APP])
    run(['codesign', '--verify', '--deep', '--strict', APP])
    print(APP)


if __name__ == '__main__':
    main()
