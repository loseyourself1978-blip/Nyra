"""SIMULATED packaging fixtures; not evidence of generated voice quality."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import wave

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('voice_assets', ROOT / 'scripts/voice_assets.py')
assets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assets)


class VoiceAssetsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nyra-voice-TEST-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.pack = self.root / 'audio/tian-1413-zh'
        self.pack.mkdir(parents=True)
        clips = {}
        for cue, phrase in assets.PHRASES.items():
            path = self.pack / (cue + '.wav')
            with wave.open(str(path), 'wb') as sound:
                sound.setparams((1, 2, 16000, 1600, 'NONE', 'not compressed'))
                sound.writeframes(bytes(3200))
            clips[cue] = {'file':path.name, 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'text':phrase}
        self.manifest = {'schema':1, 'voice_id':'ttsmaker:1413:default', 'display_name':'小田 / Tian', 'language':'zh', 'clips':clips, 'test_only':True}
        self.save()

    def save(self):
        (self.pack / 'manifest.json').write_text(json.dumps(self.manifest, ensure_ascii=False))

    def test_complete_exact_pack(self):
        self.assertEqual(len(assets.validated_voice_files(self.root, allow_test=True)), len(assets.PHRASES) + 1)

    def test_fixture_cannot_ship(self):
        with self.assertRaisesRegex(ValueError, 'cannot be shipped'):
            assets.validated_voice_files(self.root)

    def test_missing_clip(self):
        (self.pack / 'rest.wav').unlink()
        with self.assertRaises(FileNotFoundError): assets.validated_voice_files(self.root, allow_test=True)

    def test_wrong_identity(self):
        self.manifest['voice_id'] = 'unselected:voice'
        self.save()
        with self.assertRaises(ValueError): assets.validated_voice_files(self.root, allow_test=True)

    def test_wrong_phrase(self):
        self.manifest['clips']['rest']['text'] = 'different action'
        self.save()
        with self.assertRaises(ValueError): assets.validated_voice_files(self.root, allow_test=True)

    def test_corrupt_bytes(self):
        (self.pack / 'rest.wav').write_bytes(b'not the same recording')
        with self.assertRaises(ValueError): assets.validated_voice_files(self.root, allow_test=True)

    def test_outside_path(self):
        self.manifest['clips']['rest']['file'] = '../other.wav'
        self.save()
        with self.assertRaises(ValueError): assets.validated_voice_files(self.root, allow_test=True)

    def test_symlink(self):
        path = self.pack / 'rest.wav'
        path.unlink(); path.symlink_to(self.pack / 'working.wav')
        with self.assertRaises(ValueError): assets.validated_voice_files(self.root, allow_test=True)

    def test_undecodable_even_with_matching_hash(self):
        data = b'not WAV'
        (self.pack / 'rest.wav').write_bytes(data)
        self.manifest['clips']['rest']['sha256'] = hashlib.sha256(data).hexdigest()
        self.save()
        with self.assertRaisesRegex(ValueError, 'Undecodable voice audio'): assets.validated_voice_files(self.root, allow_test=True)


if __name__ == '__main__': unittest.main()
