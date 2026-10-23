#!/usr/bin/env python3
"""Read-only GitHub verification of privacy, main commit and every tracked blob/mode."""
from pathlib import Path
import argparse
import datetime
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = 'loseyourself1978-blip/Nyra'


def output(args):
    return subprocess.check_output(args,cwd=ROOT)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record',action='store_true',help='Record this already verified source commit; then commit the receipt separately')
    args = parser.parse_args()
    repo = json.loads(output(['gh','api','repos/'+REPO]))
    assert repo['private'] is True and repo['full_name'].lower() == REPO.lower()
    head = output(['git','rev-parse','HEAD']).decode().strip()
    main_ref = json.loads(output(['gh','api','repos/'+REPO+'/git/ref/heads/main']))
    assert main_ref['object']['sha'] == head, 'remote main differs from local HEAD'
    tree = json.loads(output(['gh','api','repos/'+REPO+'/git/trees/'+head+'?recursive=1']))
    assert not tree.get('truncated',False)
    remote = {e['path']:(e['sha'],e['mode']) for e in tree['tree'] if e['type']=='blob'}
    local = {}
    for record in output(['git','ls-tree','-rz','HEAD']).split(b'\0'):
        if not record:
            continue
        meta,path = record.split(b'\t',1)
        mode,kind,sha = meta.decode().split()
        if kind == 'blob': local[path.decode()] = (sha,mode)
    assert local == remote, 'remote blob content or executable modes differ'
    result = dict(repository=REPO,url=repo['html_url'],is_private=repo['private'],
                  content_upload='VERIFIED',verified_source_commit=head,
                  exact_blob_and_mode_matches=len(local),remote_tree_truncated=False,
                  verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  public_release=False,tag_created=False,
                  receipt_scope='This records the source commit verified before the separate receipt/package follow-up commit. Rerun verify_remote.py for the latest main.')
    if args.record:
        (ROOT/'reports/github-upload.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
