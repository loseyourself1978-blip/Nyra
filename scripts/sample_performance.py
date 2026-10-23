#!/usr/bin/env python3
"""Sample only a named NyraPreview PID. No broad process inventory or event capture."""
import argparse
import datetime
import json
import platform
import subprocess
import time
from pathlib import Path


def cpu_seconds(value):
    parts = value.split(':')
    return sum(float(p)*60**i for i, p in enumerate(reversed(parts)))


def sample(pid):
    p = subprocess.run(['ps', '-p', str(pid), '-o', 'ucomm=,time=,rss='],
                       capture_output=True, text=True, check=True)
    command, cpu, rss = p.stdout.strip().rsplit(None, 2)
    if command != 'NyraPreview':
        raise ValueError('Refusing to sample a different process')
    return dict(monotonic=time.monotonic(), cpu_seconds=cpu_seconds(cpu), rss_kib=int(rss))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', type=int)
    parser.add_argument('--phase', required=True)
    parser.add_argument('--seconds', type=int, required=True)
    parser.add_argument('--interval', type=float, default=5)
    args = parser.parse_args()
    rows = [sample(args.pid)]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    deadline = rows[0]['monotonic']+args.seconds
    while time.monotonic() < deadline:
        time.sleep(min(args.interval, max(0, deadline-time.monotonic())))
        rows.append(sample(args.pid))
    elapsed = rows[-1]['monotonic']-rows[0]['monotonic']
    result = dict(phase=args.phase, utc_start=started, elapsed_seconds=elapsed,
                  architecture=platform.machine(), os=platform.platform(),
                  cpu_percent_one_core=(rows[-1]['cpu_seconds']-rows[0]['cpu_seconds'])/elapsed*100,
                  max_rss_mib=max(r['rss_kib'] for r in rows)/1024,
                  method='ps cumulative user+system CPU time delta / monotonic wall time; RSS in KiB; 5s interval',
                  animation_playback=False, samples=rows)
    out = Path(__file__).resolve().parents[1]/'reports'/('performance-'+args.phase+'.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'samples'}, indent=2))


if __name__ == '__main__':
    main()
