"""Validate the redistributable fixed-phrase voice pack before packaging."""
import hashlib
import json
import wave
from pathlib import Path

PHRASES = {
    'welcome': '嗨，我在这里，陪着你呢。',
    'rest': '累了吗？喝口水，休息一下吧。',
    'working': '开工啦，我陪你一起加油。',
    'waiting': '需要你确认一下哦，我在这里等你。',
    'success': '欧耶！你好棒！',
    'sad': '别着急，我们慢慢来。',
    'outfit': '换好啦，好看吗？',
    'wave': '嘿，我在呢。',
}


def validated_voice_files(root: Path, *, allow_test=False):
    directory = root / 'audio/tian-1413-zh'
    manifest_path = directory / 'manifest.json'
    if directory.resolve() != directory.absolute() or manifest_path.is_symlink():
        raise ValueError('Voice pack must be inside the source tree')
    if manifest_path.stat().st_size >= 32768:
        raise ValueError('Oversized voice manifest')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('test_only') and not allow_test:
        raise ValueError('TEST/FIXTURE voice pack cannot be shipped')
    if (manifest['schema'], manifest['voice_id'], manifest['language'], manifest['display_name']) != (
        1, 'ttsmaker:1413:default', 'zh', '小田 / Tian'
    ):
        raise ValueError('Unexpected voice identity')
    if set(manifest['clips']) != set(PHRASES):
        raise ValueError('Missing/extra action cues')
    files = [manifest_path]
    for cue, phrase in PHRASES.items():
        clip = manifest['clips'][cue]
        if clip['file'] != cue + '.wav' or clip['text'] != phrase:
            raise ValueError('Cue filename/text mismatch: ' + cue)
        path = directory / clip['file']
        if path.is_symlink() or not 0 < path.stat().st_size < 25 * 1024 * 1024:
            raise ValueError('Unsafe/oversized voice file: ' + cue)
        if hashlib.sha256(path.read_bytes()).hexdigest() != clip['sha256']:
            raise ValueError('Voice hash mismatch: ' + cue)
        try:
            with wave.open(str(path), 'rb') as sound:
                if sound.getcomptype() != 'NONE' or not 0 < sound.getnframes() / sound.getframerate() <= 120:
                    raise ValueError('Unsupported voice audio: ' + cue)
        except (wave.Error, EOFError) as error:
            raise ValueError('Undecodable voice audio: ' + cue) from error
        files.append(path)
    return files
