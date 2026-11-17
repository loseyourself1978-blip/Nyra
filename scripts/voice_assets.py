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
    'idle': '我在这里，随时陪着你。',
    'reading': '我陪你安静读一会儿。',
    'moving': '出发啦，我跟着你。',
    'jumping': '嘿咻，伸个懒腰。',
    'settling': '站稳啦，慢慢来。',
}


ENGLISH_PHRASES = {
    "welcome": "Hi! I'm right here with you.",
    "rest": "Feeling tired? Have a sip of water and take a little break.",
    "working": "Let's get started! I'm cheering you on.",
    "waiting": "Your confirmation is needed. I'll wait right here.",
    "success": "Yay! You did great!",
    "sad": "Don't worry. Let's take it one step at a time.",
    "outfit": "All dressed up! How do I look?",
    "wave": "Hey! I'm here.",
    "idle": "I'm right here, whenever you need me.",
    "reading": "Let's enjoy a little quiet reading together.",
    "moving": "Let's go! I'm right with you.",
    "jumping": "Up we go! Time for a little stretch.",
    "settling": "There we are. Nice and steady."
}
ENGLISH_LICENSES = ('LICENSE', 'LICENSE.cmudict', 'LICENSE.homograph-data')


def validated_voice_files(root: Path, *, allow_test=False, language='zh'):
    if language not in ('zh', 'en'):
        raise ValueError('Unsupported bundled language')
    directory = root / ('audio/tian-1413-zh' if language == 'zh' else 'audio/tiny-voca-f2-en')
    phrases = PHRASES if language == 'zh' else ENGLISH_PHRASES
    identity = (1, 'ttsmaker:1413:default', 'zh', '小田 / Tian') if language == 'zh' else (1, 'tiny-voca:F2:en-US', 'en', 'tiny-voca F2')
    manifest_path = directory / 'manifest.json'
    if directory.resolve() != directory.absolute() or manifest_path.is_symlink():
        raise ValueError('Voice pack must be inside the source tree')
    if manifest_path.stat().st_size >= 32768:
        raise ValueError('Oversized voice manifest')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('test_only') and not allow_test:
        raise ValueError('TEST/FIXTURE voice pack cannot be shipped')
    if (manifest['schema'], manifest['voice_id'], manifest['language'], manifest['display_name']) != identity:
        raise ValueError('Unexpected voice identity')
    if set(manifest['clips']) != set(phrases):
        raise ValueError('Missing/extra action cues')
    files = [manifest_path]
    for cue, phrase in phrases.items():
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
    if language == 'en':
        if set(manifest.get('licenses', {})) != set(ENGLISH_LICENSES):
            raise ValueError('Missing English voice license inventory')
        for name in ENGLISH_LICENSES:
            path = directory / name
            if path.is_symlink() or not 0 < path.stat().st_size < 65536:
                raise ValueError('Invalid English license: ' + name)
            if hashlib.sha256(path.read_bytes()).hexdigest() != manifest['licenses'][name]:
                raise ValueError('English license hash mismatch: ' + name)
            files.append(path)
    return files
