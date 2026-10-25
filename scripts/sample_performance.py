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
    parser.add_argument('--animation-playback', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--playback-state', type=Path)
    parser.add_argument('--expected-animation')
    parser.add_argument('--require-hidden', action='store_true')
    args = parser.parse_args()
    def observed_sample():
        row = sample(args.pid)
        if args.playback_state:
            row['playback'] = json.loads(args.playback_state.read_text())
            if row['playback']['pid'] != args.pid:
                raise ValueError('Playback evidence belongs to another process')
        return row
    rows = [observed_sample()]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    deadline = rows[0]['monotonic']+args.seconds
    while time.monotonic() < deadline:
        time.sleep(min(args.interval, max(0, deadline-time.monotonic())))
        rows.append(observed_sample())
    elapsed = rows[-1]['monotonic']-rows[0]['monotonic']
    result = dict(phase=args.phase, utc_start=started, elapsed_seconds=elapsed,
                  architecture=platform.machine(), os=platform.platform(),
                  cpu_percent_one_core=(rows[-1]['cpu_seconds']-rows[0]['cpu_seconds'])/elapsed*100,
                  max_rss_mib=max(r['rss_kib'] for r in rows)/1024,
                  method='ps cumulative user+system CPU time delta / monotonic wall time; RSS in KiB; 5s interval',
                  animation_playback=args.animation_playback, samples=rows)
    if args.playback_state:
        states = [r['playback'] for r in rows]
        result['observed_animations'] = sorted({s['animation'] for s in states})
        names = set(states[-1]['displayed_frames']) | set(states[0]['displayed_frames'])
        result['displayed_frame_deltas'] = {n: states[-1]['displayed_frames'].get(n,0)-states[0]['displayed_frames'].get(n,0) for n in names}
        result['playback_evidence_pass'] = True
        if args.expected_animation:
            result['playback_evidence_pass'] &= all(s['animation'] == args.expected_animation for s in states)
            result['playback_evidence_pass'] &= result['displayed_frame_deltas'].get(args.expected_animation,0) > 0
        if args.require_hidden:
            result['playback_evidence_pass'] &= all(not s['panel_visible'] and not s['stage_visible'] and not s['timer_scheduled'] for s in states)
            result['playback_evidence_pass'] &= all(v == 0 for v in result['displayed_frame_deltas'].values())
    out = args.output or Path(__file__).resolve().parents[1]/'reports'/('performance-'+args.phase+'.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'samples'}, indent=2))
    if result.get('playback_evidence_pass') is False:
        raise SystemExit('Playback state verification failed; preserve report for diagnosis')


if __name__ == '__main__':
    main()
