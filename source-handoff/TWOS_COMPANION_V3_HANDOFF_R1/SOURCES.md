# 原始资料与实现依据

## 用户提供的视觉依据
- 本对话最后一张V2/V3对比图下半区；原文件名 a_wide_detailed_character_concept_sheet_compositi.png。
- 用户当前明确选择V3；本规范裁切该下半区保留来源，不根据早期红发第三版替换。

## 工程参考（检索日期：2026-10-22）
- Apple NSPanel: https://developer.apple.com/documentation/appkit/nspanel
- Nonactivating panel: https://developer.apple.com/documentation/appkit/nswindow/stylemask-swift.struct/nonactivatingpanel
- Mouse event passthrough: https://developer.apple.com/documentation/appkit/nswindow/ignoresmouseevents
- AVSpeechSynthesizer: https://developer.apple.com/documentation/avfaudio/avspeechsynthesizer
- AVSpeechSynthesisVoice: https://developer.apple.com/documentation/avfaudio/avspeechsynthesisvoice
- Speech synthesis overview: https://developer.apple.com/documentation/avfaudio/speech-synthesis

这些文档支持原生面板和语音能力选择，不保证本工程已实现，也不证明macOS第三方App有权未经许可读取TWOS私有数据。窗口命中、性能、声音可用性与版本兼容必须在实际机器验证。
