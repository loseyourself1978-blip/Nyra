# Nyra V3 R2 — Pets交付记录

本轮为原工程意外关机后的续接。原P0 App、V3母版、既有素材和R1/R2历史包保留，没有重新做静态App或启动重复图像作业。

## 实际图片与来源

REAL_IMAGE_GENERATION_CHANNEL_AND_COST_BOUNDARY: 内置image_gen；使用现有能力，不调用收费API后备、不购买额度。剩余额度数值未向代理显示。

ACTUAL_NEW_NATIVE_RUNTIME_PNG_COUNT: 本次新增13张运行PNG，全部原生1024×1536 RGBA/sRGB；图像工具实际生成15份原始输出，另2份为腿部层和制作中间稿。当前runtime共78张、78个不同SHA-256；Pets使用其中73张，另外4张为P0成功动作、1张为职场中立换装。

P0_FOUR_ANIMATIONS_AND_PLAYBACK: 20张唯一画稿/23槽；idle6、working6、gaze/head5、verified_success6。中立图共享明确记录，成功动作只播一次后回到idle。既有浏览器/原生程序播放证据与性能实测保留。

REFERENCE_VS_RUNTIME_ASSETS: 原3张综合设定图与8张裁片仍是参考。sources现有126个PNG文件、113个不同哈希，含失败稿、处理副本、中间稿及重复归档；不能作为126张合格运行画稿计数。每份被使用画稿的原图、提示词和.provenance.json均保留。

## Alpha、身份、锚点与动画

ALPHA_ANCHOR_AND_IDENTITY_REVIEW:
- 78张通过尺寸、RGBA、四角和全画布边界透明、足够透明背景/不透明核心及源哈希检查；人工审片确认成年身份、服装内衬、完整肢体和左侧饰物。细发边缘存在抗锯齿，不声称每个内部像素都为255。
- 初期画稿按母版固定矩阵归一；后期以已注册画稿为参考，记录already_registered，不逐帧裁紧铺满。导出73个cell统一使用同一affine，(512,1444)映射到(96,196)。
- 右跑00/04与左跑00/04均真实交换近/远支撑腿。左跑由新画稿生成，花饰仍在解剖左侧。只读审查与主代理均确认可读步态；中段过渡略急、03/04等邻帧有短暂停顿感，未称为精修运动捕捉质量。
- 真实图集质量检查：跳跃最高离地12px，最终落地相对idle偏差0px；16向中心最大偏移0.5px，宽度最大比1.023。157.5°/247.5°较细微，157.5→180存在变化量警告，四主方向没有反转。
- 两名既有只读审查员分别对随机A/B轴图判断，两个真实脚本结果均ok:true。部分斜向有ambiguous提示。严格记录这不是3名全新隔离审查员的多数盲审；用户限制最多两名自动审查员，没有伪造第三票或修改脚本门槛。
- 所有帧都有真实身体局部动作；没有海报摇摆、复制静帧或代码几何人物补位。最终WebP全部73槽在浏览器实际完成15个循环/1166次帧推进后暂停。宿主全动作覆盖另记。

## 目标和实际预检

TARGET_PETS_APP_SKILL_VERSION_AND_LAYOUT:
宿主com.openai.codex，26.1016.61520/build21421，已核实的本机路径为/Applications/ChatGPT.app。Pets create-pet插件0.1.6与本地hatch-pet使用v2：1536×2288，8列11行，每格192×208；73有效槽、15透明空槽；末两行从UP开始每22.5°顺时针。9行1536×1872按v1历史目标另列，没有混用或裁行。

ATLAS_VALIDATION_AND_SPRITE_VERSION:
- 补充包原编译器真实通过，原始图集与bundled函数生成的原始图集RGBA逐像素一致。
- 实际运行bundled prepare、inspect_frames、compose_atlas、extended函数、单次despill、validate_atlas、direction/continuity、axis verdict和validate_pet_quality。
- 用户要求独立原生PNG与固定画布，覆盖skill默认生成整条strip的路线。薄适配器调用bundled合成函数，保留统一transform；没有假称component-extracted，也未用自制尺寸检查替代正式验收。组件提取偏好警告保留。
- blank review card与working tablet来自用户要求执行的完整补充包prompts；不把它们说成默认skill自行引入的道具。
- 最终文件：production-r2/bundled-run/final/spritesheet-extended.webp
- 大小：1,375,620字节；SHA-256：4be774c50035149374b1049f0a44ba548c0cfb68e473b1d867201900efebb34e
- 真实Pets MCP预检valid:true，sprite_version:2，errors:[]。以上检查均绑定这份实际文件。
- 没有可用的独立Library文件夹上传工具；没有声称已存入云Library。全部持久工件保存在独立Nyra工程与最新交付包。

## 创建、列表、选中和播放分别记录

PET_CREATED_LIST_VISIBLE_SELECTED:

| 阶段 | 实际状态 |
|---|---|
| 图片生成 | 78张运行PNG，计划内缺图0 |
| 文件预检 | 本机与实际Pets宿主均通过 |
| Pets创建 | CREATED，唯一ID [本机私有创建回执中的稳定 ID] |
| Pets接口列表 | 完整分页查询中可见唯一夜璃·Nyra |
| Pets接口选中 | active_pet_id等于上述ID |
| Codex本地包 | 已安装~/.codex/pets/nyra，图集哈希与预检文件一致 |
| Codex本地列表/选中 | Owner回复“已出现并选中”确认 |
| 最终图集浏览器实播 | 73槽、15个循环，证据已保存 |
| Codex宿主各动作实播 | NOT_AUTOMATION_VERIFIED；工具安全限制禁止访问Codex自身UI，未绕过 |

云Pet记录与桌面本地包分开留证。创建前两次去重查询没有Nyra；云端仅创建一次；本地此前仅Max，安装一次且拒绝覆盖不同已有包。没有修改内部Pets数据库，没有宣称Owner Acceptance。

## 程序、换装与范围

原独立App为macOS13+通用arm64/x86_64、ad-hoc签名。实际Apple Silicon设备验证；无Intel实机声明或Apple公证。P0资源20张/23槽与已保存性能证据一致：idle300秒约1.75%单核CPU，working120秒约1.89%，隐藏60秒0%且计时器停止，峰值RSS约143MiB。原拖动、缩放、全屏、隐藏恢复、退出和换装检查保留；本轮没有重构程序。

OUTFIT_ANIMATION_COVERAGE: 默认服装P0与Pets动作；职场仅一张中立图STATIC_OUTFIT_ONLY。独立App另外保留3张R1明确标注的概念参考。Pets内未实现整套动态换装。
ORIGINAL_VOICE_STATUS: NOT_PRODUCED，默认静音。
TWOS_READONLY_INTEGRATION_STATUS: NOT_CONNECTED，所有演示事件标SIMULATION。
OWNER_TWOS_PRESERVATION: 未读取TWOS私人资料或业务库，未修改主应用。
PURCHASES_AND_PUBLICATION: NONE；未自动Commit/Push/Tag/Release。

## 打包与后续

唯一最新交付：dist/Nyra-R2-Pets.zip，含原始参考/补充包、真实PNG、原始生成稿、提示词、源与输出哈希、代码、原独立App、最终图集、可安装本地包、GIF/MP4和真实回执。排除.git/.build/.local/缓存。旧Nyra-R2.zip与R1保留为历史检查点；旧说明保存在docs/R2_PRE_PETS_*。

MISSING_ITEMS_AND_ONE_NEXT_ACTION: 核心计划内运行素材已无缺项，Nyra已出现并选中，可直接使用。若继续精修，优先平滑左右跑中段与两处斜向视线；动态职场全动作、原创声音与真实TWOS接入均属未完成范围。代理未能覆盖宿主每种动作的实播，不以用户的“出现并选中”替代全动作验收。

磁盘曾最低约200MB是用户提供的线索，卡死/关机根因未被证明；本轮出图/打包均采用至少2GiB可用空间保护，没有删除用户资料。
