#!/usr/bin/env python3
"""Publishable source/art bundle and easy-to-open macOS bundle, verified after extraction."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,zipfile

ROOT=Path(__file__).resolve().parents[1]
OMIT={'.git','.build','.local','__pycache__','dist'}
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def public_files():
    candidates=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and not any(x in OMIT for x in p.relative_to(ROOT).parts)]
    names=[p.relative_to(ROOT).as_posix() for p in candidates]
    ignored=subprocess.run(['git','check-ignore','--no-index','--stdin','-z'],input=('\0'.join(names)+'\0').encode(),cwd=ROOT,capture_output=True)
    if ignored.returncode not in (0,1):raise RuntimeError(ignored.stderr.decode())
    exclusions=set(ignored.stdout.decode().split('\0'))
    return [p for p in candidates if p.relative_to(ROOT).as_posix() not in exclusions]
def main():
    if shutil.disk_usage(ROOT).free<2*1024**3:raise RuntimeError('At least 2GiB free required')
    report=json.loads((ROOT/'production-r3/reports/build-verification.json').read_text())
    assert report['status']=='PASS_SCOPED_RELEASE_CHECKS'
    app=ROOT/'夜璃 Nyra Preview.app'
    assert sha(app/'Contents/MacOS/NyraPreview')==report['executable_sha256']
    dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    targets=[dist/'Nyra-R3-macOS.zip',dist/'Nyra-R3-Complete.zip']
    if any(p.exists() for p in targets):raise FileExistsError('Existing R3 delivery; refuse duplicate packaging')
    manifest=ROOT/'RELEASE_MANIFEST_R3.sha256'
    files=[p for p in public_files() if p!=manifest]
    manifest.write_text(''.join(sha(p)+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
    files.append(manifest)
    app_files=[p for p in files if p.is_relative_to(app) or p.name in ['README.md','R3_DELIVERY.md','启动夜璃.command'] and p.parent==ROOT]
    receipts=[]
    for target,entries in zip(targets,[app_files,files]):
        with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in entries:z.write(p,Path('Nyra')/p.relative_to(ROOT))
        with zipfile.ZipFile(target) as z:
            assert z.testzip() is None
            assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
            assert len(z.namelist())==len(entries)
        with tempfile.TemporaryDirectory(prefix='nyra-r3-check-',dir=ROOT.parent) as tmp:
            subprocess.run(['ditto','-x','-k',str(target),tmp],check=True)
            extracted=Path(tmp)/'Nyra'
            for p in entries:assert sha(p)==sha(extracted/p.relative_to(ROOT)),p
            executable=extracted/'夜璃 Nyra Preview.app/Contents/MacOS/NyraPreview'
            subprocess.run(['codesign','--verify','--deep','--strict',str(executable.parents[2])],check=True)
            result=subprocess.run([str(executable),'--self-test'],text=True,capture_output=True,check=True)
        digest=sha(target);target.with_suffix('.zip.sha256').write_text(digest+'  '+target.name+'\n')
        receipts.append(dict(file=target.name,bytes=target.stat().st_size,sha256=digest,entries=len(entries),
            exact_extracted_hashes='PASS',signature='PASS',self_test=result.stdout.strip()))
    result=dict(status='PASS_R3_ARCHIVES',app_sha256=report['executable_sha256'],archives=receipts,
        omitted=['local preferences and imported voice','account-specific Pets receipts','build caches and Git metadata','historical dist archives'],
        custom_ai_voice='DEFERRED_BY_USER',office='STATIC_OUTFIT_ONLY',twos='NOT_CONNECTED')
    (dist/'Nyra-R3-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
