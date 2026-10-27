#!/usr/bin/env python3
"""Maintainer-only clean-source Developer ID notarization; no GitHub mutation."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
def run(args):subprocess.run(list(map(str,args)),check=True)
def digest(p):
    with p.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def submit(path,profile,receipt):
    r=subprocess.run(['xcrun','notarytool','submit',str(path),'--keychain-profile',profile,'--wait','--output-format','json'],text=True,capture_output=True)
    receipt.write_text(r.stdout)
    if r.returncode:raise RuntimeError('Notarization failed; preserved response: '+str(receipt)+' '+r.stderr)
    j=json.loads(r.stdout)
    if j.get('status')!='Accepted' or not j.get('id'):raise RuntimeError('Apple did not accept '+str(receipt))
    return j['id']
def main():
    p=argparse.ArgumentParser();p.add_argument('--app',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--identity',required=True);p.add_argument('--notary-profile',default='TWOS-NOTARY');a=p.parse_args()
    if not a.identity.startswith('Developer ID Application: '):p.error('Developer ID Application required')
    m=json.loads((a.app/'Contents/Resources/component-manifest.json').read_text())
    if m.get('source_clean') is not True or m.get('engineering') is not False:p.error('A clean production commit is required')
    if a.output.exists():p.error('Existing release directories are immutable')
    a.output.mkdir(parents=True);app=a.output/a.app.name;run(['ditto',a.app,app])
    for target in [app/'Contents/MacOS/Nyra',app]:run(['codesign','--force','--options','runtime','--timestamp','--sign',a.identity,target])
    run(['codesign','--verify','--deep','--strict',app])
    archive=a.output/'notarization.zip';run(['ditto','-c','-k','--keepParent',app,archive])
    app_id=submit(archive,a.notary_profile,a.output/'app-notarization.json')
    for command in ['staple','validate']:run(['xcrun','stapler',command,app])
    run(['spctl','--assess','--type','execute','--verbose=4',app])
    stage=a.output/'volume';stage.mkdir();run(['ditto',app,stage/app.name]);(stage/'Applications').symlink_to('/Applications',target_is_directory=True)
    dmg=a.output/('Nyra-'+m['version']+'-arm64.dmg');run(['hdiutil','create','-volname','Nyra','-srcfolder',stage,'-format','UDZO',dmg]);run(['codesign','--timestamp','--sign',a.identity,dmg])
    dmg_id=submit(dmg,a.notary_profile,a.output/'dmg-notarization.json')
    for command in ['staple','validate']:run(['xcrun','stapler',command,dmg])
    run(['spctl','--assess','--type','open','--context','context:primary-signature','--verbose=4',dmg])
    (a.output/'component-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    files={x.relative_to(app).as_posix():digest(x) for x in sorted(app.rglob('*')) if x.is_file() and not x.is_symlink()}
    (a.output/'installer-manifest.json').write_text(json.dumps({'source_commit':m['source_commit'],'files':files},indent=2)+'\n')
    (a.output/'release.json').write_text(json.dumps({'product':'Nyra','version':m['version'],'source_commit':m['source_commit'],'artifact':dmg.name,'bytes':dmg.stat().st_size,'sha256':digest(dmg),'app_notarization_id':app_id,'dmg_notarization_id':dmg_id,'gatekeeper':'PASS','architecture':'arm64','owner_differential_acceptance':'NOT_GRANTED_BY_ENGINEERING'},indent=2)+'\n')
    names=[dmg.name,'component-manifest.json','installer-manifest.json','release.json','app-notarization.json','dmg-notarization.json']
    (a.output/'SHA256SUMS').write_text(''.join(digest(a.output/x)+'  '+x+'\n' for x in names))
if __name__=='__main__':main()
