#!/usr/bin/env python3
"""One local R2 archive; preserve R1, omit caches/preferences, verify extracted bytes."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess, tempfile, zipfile

ROOT = Path(__file__).resolve().parents[1]
OMIT = {'.git', '.build', '.local', '__pycache__', 'dist'}
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def included(p):
    return p.is_file() and not any(x in OMIT for x in p.relative_to(ROOT).parts) and p.name!='.DS_Store'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',default='R2',help='New immutable delivery label; never overwrites an archive')
    args=parser.parse_args()
    if not re.fullmatch(r'R2(?:-[A-Za-z0-9]+)*',args.label):raise ValueError('Invalid delivery label')
    if shutil.disk_usage(ROOT).free < 2*1024**3:raise RuntimeError('LOW_DISK: need at least2GiB before packaging')
    dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    target=dist/f'Nyra-{args.label}.zip'
    if target.exists():raise FileExistsError('R2 archive already exists; inspect its receipt instead of duplicating job')
    r=ROOT/'production-r2'
    inventory=[]
    for base in ['sources','runtime','prompts','references/pose-guides']:
        for p in sorted((r/base).rglob('*')):
            if p.is_file():inventory.append(dict(path=str(p.relative_to(r)),bytes=p.stat().st_size,sha256=sha(p)))
    (r/'reports/artifact-hashes.json').write_text(json.dumps(dict(algorithm='SHA-256',files=inventory),ensure_ascii=False,indent=2)+'\n')
    manifest=ROOT/f'RELEASE_MANIFEST_{args.label}.sha256'
    files=sorted(p for p in ROOT.rglob('*') if included(p) and p!=manifest)
    manifest.write_text(''.join(sha(p)+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
    files.append(manifest)
    with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:z.write(p,Path('Nyra')/p.relative_to(ROOT))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(files)
        assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
        assert not any(any(x in OMIT for x in Path(n).parts) for n in z.namelist())
        assert (z.getinfo('Nyra/夜璃 Nyra Preview.app/Contents/MacOS/NyraPreview').external_attr>>16)&0o111
    with tempfile.TemporaryDirectory(prefix='nyra-r2-extract-',dir=ROOT.parent) as tmp:
        subprocess.run(['ditto','-x','-k',str(target),tmp],check=True)
        extracted=Path(tmp)/'Nyra';count=0
        for line in (extracted/manifest.name).read_text().splitlines():
            expected,relative=line.split('  ',1)
            assert sha(extracted/relative)==expected,relative
            count+=1
        app=extracted/'夜璃 Nyra Preview.app'
        subprocess.run(['codesign','--verify','--deep','--strict',str(app)],check=True)
        check=subprocess.run([str(app/'Contents/MacOS/NyraPreview'),'--self-test'],capture_output=True,text=True,check=True)
    digest=sha(target)
    target.with_suffix('.zip.sha256').write_text(digest+'  '+target.name+'\n')
    lifecycle=json.loads((r/'reports/pets-readiness-final.json').read_text())
    receipt=dict(status='PASS_ARCHIVE_INTEGRITY_AND_EXTRACTED_APP',archive=str(target),bytes=target.stat().st_size,
                 sha256=digest,manifest_files=count,archive_entries=len(files),extracted_signature='PASS',
                 executable_permission='PASS',extracted_self_test=check.stdout.strip(),
                 full_pets_complete=False,remote_push=False,
                 pet_created=lifecycle.get('pet_created',False),
                 pet_selected=lifecycle.get('selected_nyra',False),
                 desktop_owner_confirmed=lifecycle.get('desktop_owner_confirmed',False),
                 host_all_actions_playback_verified=False)
    (dist/f'Nyra-{args.label}-verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
