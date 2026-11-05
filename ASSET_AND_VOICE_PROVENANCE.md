# Nyra 1.0 resource and voice provenance

The source manifests identify each runtime image by source path and SHA-256. `production-1.0/generated-assets.json` inventories the authorized missing-art additions. Existing R2/R4 character/runtime art is retained; black-purple, office and gala use complete transparent images, with matching-outfit reclining and rise/action/lower transitions. Office/gala runs contain two painted frames; they are not described as eight-frame gait animation. Generated content is not a claim of exclusive copyright.

Source, manifest and candidate media are distinct: an actual screenshot is not proof of frame progression, and a static image animation is not an installation recording. Public media uses only non-sensitive engineering examples.

## Tian action voice

Thirteen fixed Chinese phrases use the Owner-selected TTSMaker 1413 Tian voice. The original eight WAV clips are unchanged. Five additional phrases (idle, reading, movement, jumping and settling) were supplied by the Owner as an MP3 on November 5, 2026; the manifest records its source hash, decoded sample rate and exact phrase cut ranges. Only the inter-phrase gaps were trimmed; the source was decoded into mono PCM WAV for offline playback. The supplemental website generation settings were not independently observed. No voice is cloned.

The two procedural UI chimes remain. English maps every action to a corresponding fixed English phrase and uses an available installed female system voice; it does not silently replay the Chinese recording. On the engineering Mac, all thirteen English phrases completed native speech callbacks with the installed Samantha voice. This is playback-engine evidence, not an independent listening-quality assessment or proof that every other Mac has that voice. The player reports an unavailable voice and lets the user select an installed alternative. Private, per-action imports take precedence and are never distributed.

[Manifest](audio/tian-1413-zh/manifest.json) · [TTSMaker audio license](https://ttsmaker.com/copyright_and_commercial_license_terms/zh-cn)

## White blouse and ruby gown additions — development checkpoint

The existing three outfits and their 122 resource records remain unchanged. Two additional Owner-requested reference variants contain forty new native RGBA frames: fourteen standing frames and six reclining frames per outfit. These are independently generated full-size frames, not crops or rotations of the old low-resolution concept screenshots. The manifest records each source file, byte size, dimensions, alpha measurements and SHA-256. The source inventory records OpenAI image generation/editing; it does not assert exclusive rights.

The five-outfit manifest and its action coverage have passed local resource tests. Final packaged visual transitions and Owner acceptance are still pending at this checkpoint. Directional runs use two painted frames per direction. Resting work and blink use distinct supported reclining frames. The implementation does not claim continuous motion capture or eight-frame gait animation.

## 中文补充

新增五句“小田 1413”来自 Owner 下载的 MP3，原八句文件未改动；来源哈希和分句区间保存在音频清单中。中英文均有十三项动作台词，英文使用本机已安装女声，当前工程机的 Samantha 已完成逐句播放回调检查。这不等于已经完成主观听感验收。

白衬衫与红礼服各有十四张站姿帧和六张侧卧帧，完整透明素材经资源测试后接入现有动作系统。原三套服装不变。新服装的最终打包界面与动作衔接仍待验证，不把资源检查写成 Owner 接受。
