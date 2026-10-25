"""Preserve a real imagegen output and its prompt; never invent missing frames."""
from pathlib import Path
import argparse, datetime, json, re, shutil
from normalize_runtime import normalize, ROOT

def record(job):
    asset_id = job['id']
    if not re.fullmatch(r'nyra_[a-z0-9_]+', asset_id):
        raise ValueError('Invalid asset ID')
    source = Path(job['source']).resolve()
    destination = ROOT/'sources'/f'{asset_id}.png'
    if destination.exists():
        raise FileExistsError(destination)
    shutil.copy2(source, destination)
    destination.with_suffix('.prompt.txt').write_text(job['prompt'])
    normalize(destination, asset_id, already_registered=job.get('already_registered', False))
    state_path = ROOT/'reports/run-state.json'
    state = json.loads(state_path.read_text())
    count = len(list((ROOT/'runtime').rglob('*.png')))
    state.update(actual_runtime_png_count=count, runtime_png_created=count,
                 last_generated_asset=asset_id,
                 updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 free_disk_bytes=shutil.disk_usage(ROOT).free)
    temporary = state_path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n')
    temporary.replace(state_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('jobs_json')
    args = parser.parse_args()
    for job in json.loads(args.jobs_json):
        record(job)
