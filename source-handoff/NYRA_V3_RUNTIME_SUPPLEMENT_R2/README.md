# 夜璃 · Nyra V3｜运行素材生产补充包 R2

**本包等级：PRODUCTION_SPEC_AND_QA_TOOLKIT；不是 RUNTIME_ASSETS_COMPLETE。**

这是对《ASSET_AUDIT》《DELIVERY_REPORT》《MINIMUM_ASSETS》《SCOPE_AND_AUTHORIZATION》的逐项补充。沿用已选 V3、原独立预览 App 及私有 Nyra 项目；不重新选人设，不修改 TWOS 主产品。

## 本轮真实完成

- 复核上传 ZIP：66 个文件条目、CRC 通过，65 项 RELEASE_MANIFEST 内容全部 SHA-256 匹配。原仓库“68 文件”是用户回传的远端清单，未在本轮实时验证，不与 ZIP 统计混同。
- 保留 V3 选定参考与主综合图，明确二者仍是参考，不是透明动画。
- 补齐 78 个唯一目标画稿的逐文件双语生产提示词：其中默认服装 77 张、职场中立换装 1 张；当前新生成运行画稿 **0**。
- 首阶段独立桌宠使用 **20 张唯一画稿、23 个播放/姿态槽位**：1 张中立母版由多个状态显式引用。母版及四套动作目前均缺。
- 按附件保存 73 帧槽位/15 空格的 Pets v2 图集方案，并另列当前公开文档的网页上传尺寸，二者不混用。
- 提供真实可运行的离线图片检查、固定变换图集编译器、15 项工具自测，以及本地动画审片页面。
- 提供服装、嘴形、配音、状态语义、Pet 创建/选中、权限与交接说明。

## 没有完成的东西

未生成新的高清透明母版或动作图、未制作 PSD/骨骼/Live2D/3D、未制作原创音频、未安装/创建/选中 Pets、未连接 TWOS、未上传/修改 GitHub。

当前会话的原生图像生成不可调用；已连接 Runway 的只读核验显示可用积分 0，未发送参考图、未启动生成、未购买。不能把本包的提示词、网格示意、合成测试或旧图抠裁称为新运行素材。

## 最短实际接续路线

在**官方 Codex 原「夜璃 / Nyra」独立会话**中读取 `CODEX_CONTINUE.md`，不是 TWOS 研发会话或 LDD 业务会话。

1. 读取本机可用的正式图像生成能力及已安装 Pets 创建 skill，确认目标版本，不猜路径/命令。
2. 先产出并检查 `runtime/default/nyra_neutral.png`，再扩展 P0 20 张；不要再画综合海报。
3. 真实播放四套动作，检查身份、锚点、alpha、过渡和局部动作。
4. 根据已核实的目标宿主选择图集 profile；补齐所需动作后编译、走宿主预检。
5. Pet 文件生成、预检通过、已创建、出现在列表、已选中、真正动画分别留回执。无合格素材时不上传空白/占位图。

第一次调用模型不被本包自动触发。下达 Codex 续接指令后，在既有授权额度内制作素材；新订阅、充值、公开发布不获授权。

## 文件导航

- `docs/SOURCE_AND_TARGET_RECONCILIATION.md`：附件事实、外部规格及本轮设计决策。
- `docs/PRODUCTION_PLAN.md`：P0 / Pets / 换装 / 表情 / 音频的完成条件。
- `docs/ART_LOCK_AND_ALPHA.md`：身份、坐标、透明度及补画标准。
- `prompts/`：78 份逐目标画稿指令，另有 `specs/prompt_catalog.json`。
- `specs/standalone_p0.json`：四动作播放关系与时长。
- `specs/pets_layout_profiles.json`：候选图集格式，默认未确认目标。
- `specs/assets_required.json`：所有运行图均为 `MISSING_NOT_RENDERED`。
- `preview/animation_review.html`：加载真正 PNG 后审片，不默认展示假动画。
- `tools/nyra_assets.py`：检查/打包，缺素材或目标规范即失败关闭。
- `reports/`：本轮实际审计和工具测试，不是动画验收。
- `voice/`：原台词及语音规范；没有 WAV 或专属音色。

运行工具需要已有 Python 3.10+ 与 Pillow。缺依赖时报告，不偷偷安装或付费。
