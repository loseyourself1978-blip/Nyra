"""One-shot offline generation of Nyra's existing fixed English cues."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, sys, time, wave
from voice_assets import ENGLISH_PHRASES

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--materials', required=True, type=Path, help='Pinned weights, dizione source, source-pins.json and model-download.json')
parser.add_argument('--output', required=True, type=Path, help='A new directory; never overwrite recordings')
args = parser.parse_args()
ROOT = args.materials.resolve()
os.environ['DIZIONE_DATA'] = str(ROOT / 'weights/phonemizer')
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ.pop('DIZIONE_OVERRIDES', None)
sys.path.insert(0, str(ROOT / 'dizione/src'))
import numpy as np
import onnxruntime as ort
import dizione
from dizione.symbols import SYMBOL_TO_ID

phrases = ENGLISH_PHRASES
assert len(phrases) == 13
config = json.loads((ROOT / 'weights/config.json').read_text())
assert config['vocab'] == SYMBOL_TO_ID
assert config['phonemizer']['version'] == dizione.VERSION
download = json.loads((ROOT / 'model-download.json').read_text())
assert download['revision'] == 'd94d2a0338fd1e0eab7dd896ec0ad23d8cdf7c14'
assert hashlib.sha256((ROOT/'weights/onnx/model.onnx').read_bytes()).hexdigest() == 'fe6d918791a15b82e37465981d7f27a070e46b46635e5a3482fc8dff87a1ae46'
pins = json.loads((ROOT / 'source-pins.json').read_text())
output = args.output.resolve()
output.mkdir(exist_ok=False)
options = ort.SessionOptions()
options.intra_op_num_threads = 1
options.inter_op_num_threads = 1
options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
ort.set_seed(20261117)
session = ort.InferenceSession(str(ROOT / 'weights/onnx/model.onnx'), sess_options=options, providers=['CPUExecutionProvider'])
one = lambda value: np.array([value], dtype=np.float32)
clips = {}
checks = []
for cue, phrase in phrases.items():
    start = time.monotonic()
    phones = dizione.phonemize(phrase)
    assert not phones.unknown and len(phones.ids) < 512
    audio, durations = session.run(None, {
        'tokens': np.array([phones.ids], dtype=np.int64),
        'stress': np.array([phones.stress], dtype=np.int64),
        'voice': np.array([0], dtype=np.int64),
        'speed': one(0.95), 'pitch_shift': one(0), 'pitch_range': one(1),
    })
    samples = audio[0]
    assert np.isfinite(samples).all() and 0.25 <= len(samples)/24000 < 20
    peak = float(np.max(np.abs(samples)))
    assert peak > .01
    gain = min(1., .97/peak)
    pcm = np.rint(samples*gain*32767).astype('<i2')
    path = output / (cue + '.wav')
    with wave.open(str(path), 'wb') as wav:
        wav.setparams((1, 2, 24000, len(pcm), 'NONE', 'not compressed'))
        wav.writeframes(pcm.tobytes())
    clips[cue] = {'file': path.name, 'text': phrase, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'duration_seconds':len(samples)/24000}
    check = {'cue':cue,'text':phrase,'seconds':len(samples)/24000,'generation_seconds':time.monotonic()-start,'tokens':len(phones.ids),'peak_before':peak,'gain':gain,'peak_after':float(np.max(np.abs(pcm.astype(np.float32))))/32767,'rms':float(np.sqrt(np.mean((pcm.astype(np.float32)/32767)**2))),'clipped_samples':int(np.sum(np.abs(pcm.astype(np.int32))>=32767))}
    checks.append(check)
    print(json.dumps(check),flush=True)
manifest = {'schema':1,'voice_id':'tiny-voca:F2:en-US','display_name':'tiny-voca F2','language':'en','locale':'en-US','source':'Locally generated fixed English action cues; no user task text','source_url':'https://huggingface.co/n4ze3m/tiny-voca','license':'Apache-2.0','license_url':'https://huggingface.co/n4ze3m/tiny-voca/blob/'+download['revision']+'/LICENSE','model_revision':download['revision'],'model_sha256':'fe6d918791a15b82e37465981d7f27a070e46b46635e5a3482fc8dff87a1ae46','source_commits':pins,'phonemizer_identity':dizione.identity(),'generation_settings':{'voice':'F2','speed':0.95,'pitch_shift':0,'pitch_range':1,'sample_rate':24000,'channels':1,'pcm_bits':16,'runtime':'onnxruntime '+ort.__version__,'numpy':np.__version__,'seed':20261117,'peak_limit':0.97},'generated_at':datetime.datetime.now().astimezone().isoformat(),'test_only':False,'clips':clips}
manifest['licenses'] = {}
for name, source in [('LICENSE', ROOT/'weights/LICENSE'), ('LICENSE.cmudict', ROOT/'weights/phonemizer/LICENSE.cmudict'), ('LICENSE.homograph-data', ROOT/'weights/phonemizer/LICENSE.homograph-data')]:
    data = source.read_bytes(); (output/name).write_bytes(data)
    manifest['licenses'][name] = hashlib.sha256(data).hexdigest()
(output/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(output.parent/(output.name+'-checks.json')).write_text(json.dumps({'signal_checks':checks,'auditory_review':'PENDING_NOT_INFERRED_FROM_SIGNAL_CHECKS'},indent=2)+'\n')
