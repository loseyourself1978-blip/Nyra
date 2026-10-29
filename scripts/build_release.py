#!/usr/bin/env python3
"""Build the pinned native companion offline. No installs, downloads or publication."""
from pathlib import Path
import argparse,hashlib,json,plistlib,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
def run(args):subprocess.run(list(map(str,args)),check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(destination,cache,architectures,signing,engineering):
    destination=Path(destination);cache=Path(cache);assert not destination.exists(),'Use a new output; preserve previous candidates'
    contents=destination/'Contents';resources=contents/'Resources';(contents/'MacOS').mkdir(parents=True);resources.mkdir();cache.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/'production-1.0/specs/resources.json').read_text())
    for relative,entry in manifest['files'].items():
        source=ROOT/entry['source'];assert sha(source)==entry['sha256'];target=resources/'runtime'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    for source,target in [(ROOT/'production-1.0/specs/runtime.json',resources/'runtime/r4.json'),(ROOT/'production-r3/specs/standalone_r3.json',resources/'runtime/standalone_r3.json'),(ROOT/'production-1.0/specs/outfits.json',resources/'assets/outfits.json')]:
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    outfits=json.loads((resources/'assets/outfits.json').read_text())
    for outfit in outfits['outfits']:shutil.copy2(ROOT/'assets'/outfit['file'],resources/'assets'/outfit['file'])
    for name in ['open.wav','outfit.wav','provenance.json']:
        (resources/'audio').mkdir(exist_ok=True);shutil.copy2(ROOT/'audio'/name,resources/'audio'/name)
    contract=ROOT/'production-r4/contracts/nyra_event_contract.json'
    shutil.copy2(contract,resources/'event-contract.json')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    clean=not subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=ROOT,text=True).strip()
    input_paths=set((ROOT/'Sources').glob('*.swift'))
    input_paths.update(ROOT/v['source'] for v in manifest['files'].values())
    input_paths.update(ROOT/'assets'/outfit['file'] for outfit in outfits['outfits'])
    input_paths.update(ROOT/'audio'/name for name in ['open.wav','outfit.wav','provenance.json'])
    input_paths.update([ROOT/'scripts/build_release.py',ROOT/'scripts/prepare_release.py',
        ROOT/'production-1.0/specs/runtime.json',ROOT/'production-1.0/specs/resources.json',
        ROOT/'production-1.0/specs/outfits.json',ROOT/'production-r3/specs/standalone_r3.json',contract])
    inputs={str(p.relative_to(ROOT)):sha(p) for p in sorted(input_paths)}
    snapshot=hashlib.sha256(json.dumps(inputs,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    payload={p.relative_to(resources).as_posix():sha(p) for p in sorted(resources.rglob('*')) if p.is_file()}
    (resources/'component-manifest.json').write_text(json.dumps(dict(product='Nyra',version='1.0.1',build='101',source_commit=head,source_clean=clean,source_snapshot=snapshot,event_schema='twos.nyra.status.v2',event_schema_sha256=sha(contract),files=inputs,bundle_files=payload,engineering=engineering),indent=2)+'\n')
    info=dict(CFBundleName='Nyra Engineering' if engineering else 'Nyra',CFBundleDisplayName='Nyra Engineering' if engineering else '夜璃 · Nyra',CFBundleIdentifier='com.tianma.nyra.joint.engineering' if engineering else 'com.tianma.nyra',CFBundleExecutable='Nyra',CFBundlePackageType='APPL',CFBundleShortVersionString='1.0.1',CFBundleVersion='101',LSMinimumSystemVersion='13.0',LSUIElement=True,NSHighResolutionCapable=True,NSPrincipalClass='NSApplication',CFBundleDevelopmentRegion='en',LSMultipleInstancesProhibited=True,NyraVisibilityProtocol=2,CFBundleURLTypes=[dict(CFBundleURLName='Nyra visibility only',CFBundleURLSchemes=['nyra','twos-nyra'])])
    (contents/'Info.plist').write_bytes(plistlib.dumps(info))
    binaries=[]
    for arch in architectures:
        binary=cache/('Nyra-'+arch);binaries.append(binary)
        run(['xcrun','swiftc','-swift-version','5','-O','-target',arch+'-apple-macos13.0','-module-cache-path',cache/'module-cache','-framework','AppKit','-framework','AVFoundation',*sorted((ROOT/'Sources').glob('*.swift')),'-o',binary])
    if len(binaries)==1:shutil.copy2(binaries[0],contents/'MacOS/Nyra')
    else:run(['lipo','-create',*binaries,'-output',contents/'MacOS/Nyra'])
    args=['codesign','--force','--sign',signing]
    if signing!='-':args+=['--options','runtime','--timestamp']
    run([*args,destination]);run(['codesign','--verify','--deep','--strict',destination]);print(json.dumps(dict(app=str(destination),source=head,snapshot=snapshot,architectures=architectures,signature=signing,notarization='NOT_SUBMITTED')))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--cache',required=True);p.add_argument('--architectures',nargs='+',choices=['arm64','x86_64'],default=['arm64','x86_64']);p.add_argument('--sign',default='-');p.add_argument('--engineering',action='store_true');a=p.parse_args();build(a.output,a.cache,a.architectures,a.sign,a.engineering)
