"""Install the reviewed local pet package, refusing any different existing Nyra.

This copies two public character-package files only. It does not edit the host
database or selection preferences and does not assert host UI visibility.
"""
from pathlib import Path
import hashlib,json,os,shutil,tempfile
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'pets-ready/nyra'
destination=Path.home()/'.codex/pets/nyra'
expected='4be774c50035149374b1049f0a44ba548c0cfb68e473b1d867201900efebb34e'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((source/'pet.json').read_text())
if manifest['id']!='nyra' or manifest['spriteVersionNumber']!=2 or manifest['spritesheetPath']!='spritesheet.webp':
    raise ValueError('Unexpected package manifest')
if sha(source/'spritesheet.webp')!=expected:raise ValueError('Sprite changed since preflight')
for f in ['final/validation-extended.json','qa/pet-quality.json']:
    check=json.loads((ROOT/'bundled-run'/f).read_text())
    if check.get('ok') is not True or check.get('sha256')!=expected:raise ValueError('QA mismatch')
host=json.loads((ROOT/'bundled-run/qa/host-preflight.json').read_text())['structuredContent']
if host.get('valid') is not True or host.get('file_size_bytes')!=(source/'spritesheet.webp').stat().st_size:
    raise ValueError('Host preflight mismatch')
destination.parent.mkdir(parents=True,exist_ok=True)
if destination.exists():
    if set(p.name for p in destination.iterdir())!={'pet.json','spritesheet.webp'} or any(sha(source/f)!=sha(destination/f) for f in ['pet.json','spritesheet.webp']):
        raise FileExistsError('A different Nyra package already exists; refusing replacement')
    status='EXACT_PACKAGE_ALREADY_INSTALLED'
else:
    staging=Path(tempfile.mkdtemp(prefix='.nyra-install-',dir=destination.parent))
    try:
        for f in ['pet.json','spritesheet.webp']:shutil.copy2(source/f,staging/f)
        os.rename(staging,destination)
    finally:
        if staging.exists():shutil.rmtree(staging)
    status='INSTALLED_ONCE'
print(json.dumps({'status':status,'path':str(destination),'sha256':sha(destination/'spritesheet.webp'),
    'database_edited':False,'desktop_selection_changed_by_installer':False,'desktop_playback_verified_by_installer':False}))
