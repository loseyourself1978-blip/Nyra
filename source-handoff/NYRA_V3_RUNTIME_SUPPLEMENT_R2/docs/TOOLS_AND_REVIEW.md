# 工具使用与真实验收

本包工具只处理本地素材，不生成图片、不联网、不安装Pet、不上传仓库。需要执行环境已有Python3.10+、Pillow；不自动安装依赖。

## 检查当前缺口

```sh
python tools/nyra_assets.py audit --subset p0 --report reports/p0_asset_gate.json
python tools/nyra_assets.py audit --subset all --report reports/all_asset_gate.json
```

当前返回BLOCKED/exit2是正确结果：没有运行画稿。不要改成空白占位PNG绕过。

## 新图登记

真实画稿按catalog路径放入runtime，再执行：

```sh
python tools/nyra_assets.py inspect runtime/default/nyra_neutral.png
```

保留原始生成文件、实际工具/尺寸、参考母版hash、处理记录；在assets_required.json写入实际sha256和native_resolution_provenance=RECORDED。不要填虚构ID或生成时间。

打开preview/animation_review.html，选择补充包目录；仅加载本机文件、不发网络。逐动作播放/逐帧、检查透明底和脚锚点。填写visual_review.json的真实结果及hash；填PASS需要真的看过，数值检查不能代填。没有PNG时审片器显示缺图，不会用海报自动顶替。

## 编译前

读取本机真实Pets skill与预检器，固定selected_profile、版本/skill hash及row/gaze映射，保存脱敏的目标证据文件和hash。方向顺序如不同，先显式更改profile的asset_ids映射，再重新计算profile hash，不拉伸图片。

```sh
python tools/nyra_assets.py profile pets_v2_attachment_provisional
python tools/nyra_assets.py audit --subset all --require-visual
python tools/nyra_assets.py build --profile pets_v2_attachment_provisional --output exports/nyra-pets-v2.png
```

编译器使用全组同一等比变换，不按逐帧bbox缩放；无视觉审核、source provenance、target确认会拒绝。未用格透明。输出“ATLAS_COMPILED_NOT_INSTALLED”不是Pets预检、创建或选中成功。

网页9行profile默认映射未确认，同样拒绝正式编译。不要简单裁掉最后两行就声称任何目标都兼容。

## 自测

```sh
python -m unittest discover -s tests -v
```

测试使用临时抽象几何形状，验证拒绝坏alpha、错尺寸、越界路径、空图、布局计数和未确认目标；不使用它们当角色图。15项自测PASS不是角色画稿PASS。

## 最小人工验收

- 同一成年脸、发饰位置和服装覆盖；无多指、断手、截尾。
- 黑白/棋盘格底上无光晕；背景确实消失而人物核心不半透明。
- P0首尾与过渡自然；能指出每套动作的局部关节变化。
- 16向完整一周无人物自转、眼睛扭曲或首尾突变。
- 独立App和Pets各自真实播放，安装路径和结果分别记录。
- 禁止用动态缩放海报、重复静帧或删除失败记录冒充动画通过。
