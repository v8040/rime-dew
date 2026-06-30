# 寒露拼音方案  (Ice + Frost + LMDG)

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3.0--only-blue.svg)](https://spdx.org/licenses/GPL-3.0-only.html)

寒露拼音方案是开箱即用专注于拼音的 [RIME](https://github.com/rime/librime) 输入法的融合方案 --
整合雾凇拼音框架, 白霜词库, 万象 LMDG 语法模型

**冰霜万象融合** (Ice + Frost + LMDG) 故命名为`寒露 rime-dew`

## 介绍

三源融合: 雾凇拼音框架 ([rime-ice](https://github.com/iDvel/rime-ice)) +
白霜词库 ([rime-frost](https://github.com/gaboolic/rime-frost)) +
万象语法模型 ([RIME-LMDG](https://github.com/amzxyz/RIME-LMDG))

仅暴露全拼与九键方案
预设配置, CI 自动化重组框架与词库

## 方案理念

沉浸式打字, 杜绝快捷键误触和全角符号污染代码与文档
- 无方案切换快捷键, `Shift_R` 中英切换, `Tab` 翻页
- 桌面端默认英文, 移动端默认中文, 强制半角标点
- `v` 模式 (如: 全角标点输入 `vdh`, 特殊符号输入 `vfh`) 无需切换
- Lua 扩展 (如: 拆字反查输入 `uU`, 计算输入 `cC`, 大写金额输入 `R`, 日期时间输入 `sj/rq/nl`) 即打即得

## 使用指南

已测试客户端:
- macOS: [鼠须管](https://github.com/rime/squirrel)
- Windows: [小狼毫](https://github.com/rime/weasel)
- iOS: [元书输入法](https://ihsiao.com/apps/hamster/v3/docs)

推荐直接使用 [Plum](https://github.com/rime/plum) 部署, 开箱即用
> [!TIP]
> `grammar` 为可选配置, 会自动下载语法模型 (400MB+)

```bash
git clone --depth=1 https://github.com/rime/plum.git plum && cd plum

# 桌面端
bash rime-install v8040/rime-dew
bash rime-install v8040/rime-dew:others/recipes/desktop
# (可选)
bash rime-install v8040/rime-dew:others/recipes/grammar

# 移动端 无法直接使用 Plum
# 建议在电脑端通过 rime_dir 指向同步目录后
# 通过 iCloud/Wi-Fi 同步到移动端
rime_dir="<dir>" bash rime-install v8040/rime-dew
rime_dir="<dir>" bash rime-install v8040/rime-dew:others/recipes/mobile
# (可选)
rime_dir="<dir>" bash rime-install v8040/rime-dew:others/recipes/grammar
rime_dir="<dir>" bash rime-install v8040/rime-dew:others/recipes/grammar:schema=t9

# Plum 支持 Multi-target
rime_dir="<dir>" bash rime-install \
  v8040/rime-dew \
  v8040/rime-dew:others/recipes/mobile \
  v8040/rime-dew:others/recipes/grammar \
  v8040/rime-dew:others/recipes/grammar:schema=t9
```

也可以直接从 [Releases](https://github.com/v8040/rime-dew/releases/latest) 下载预打包的 `.7z` 配置包:

| 包名 | 内容 |
|------|------|
| [desktop.7z](https://github.com/v8040/rime-dew/releases/latest/download/desktop.7z) | 桌面端 (全拼, 无语法模型) |
| [desktop-grammar.7z](https://github.com/v8040/rime-dew/releases/latest/download/desktop-grammar.7z) | 桌面端 (全拼 + 万象语法模型) |
| [mobile.7z](https://github.com/v8040/rime-dew/releases/latest/download/mobile.7z) | 移动端 (全拼 + 九宫格, 无语法模型) |
| [mobile-grammar.7z](https://github.com/v8040/rime-dew/releases/latest/download/mobile-grammar.7z) | 移动端 (全拼 + 九宫格 + 万象语法模型) |

> [!TIP]
> - 首次: 清空并解压至 `RIME 用户目录`, 重新部署即可
> - 更新: 再次执行部署命令`增量更新`或下载压缩包解压覆盖,
> 增量更新的自定义配置 (`*.custom.yaml`) 将保留与合并
> - 生效: `RIME 菜单` -> `重新部署`

> [!WARNING]
> - 本方案仅使用 `patch` 方式打补丁和替换词库 ([rime_frost.dict.yaml](./others/presets/rime_frost.dict.yaml)),
> 此外未修改任何上游文件
> - 任何使用问题请参考 [Wiki](https://dvel.me/posts/rime-ice),
> Issues 请反馈到对应的上游仓库

## 预设说明

预设配置通过 [others/presets](./others/presets/) 独立维护,
桌面端与移动端通过多级 `__include` 引用公共配置

> [!WARNING]
> 请勿直接修改
> - 若需自定义预设, Fork 本仓库后自行修改
> - 若需自定义配置, 修改 `RIME 用户目录` 下的 `*.custom.yaml` 覆盖预设即可
>
> <details><summary>自定义配置示例 (点击展开)</summary>
>
> ```YAML
> __patch:
> # Rx: v8040/rime-dew:others/recipes/desktop: {
>   - patch/+:
>       __include: others/presets/desktop_weasel:/patch
> # }
>   # 请勿删除以上动态生成配置
>   # 追加自定义配置以覆盖预设 (需缩进严格一致)
>   - patch/+:
>       style/horizontal: false
>       style/color_scheme: google
>       style/color_scheme_dark: purity_of_form_custom
> ```
>
> </details>

### common_*.yaml

- `common_algebra.yaml` 拼写派生规则 (简拼 + 模糊音纠错)
- `common_rime_ice.yaml` 追加派生规则, 引用 `common_algebra.yaml`
- `common_switches.yaml` 开关状态 (`@1` 半角标点, `@3` 简体, 其余关闭)

### desktop_*.yaml

- `desktop_default.yaml` 禁用方案选单, 默认为 `rime_ice`, `Shift_R` 中英切换, `Tab` 翻页, 小键盘映射
- `desktop_rime_ice.yaml` 桌面端入口, 串联公共规则与专属开关
- `desktop_squirrel.yaml` [鼠须管](https://github.com/rime/squirrel)横向候选框, `PingFangSC` + `Monaco` 字体
- `desktop_switches.yaml` 继承公共开关, 覆写 `@0` 为默认英文
- `desktop_weasel.yaml` [小狼毫](https://github.com/rime/weasel)横向候选框, `Microsoft YaHei` + `Consolas` 字体

### mobile_*.yaml

- `mobile_melt_eng.yaml` 英文字母映射为九键数字 `2-9`
- `mobile_rime_ice.yaml` 移动端入口, 串联公共规则与专属开关
- `mobile_switches.yaml` 继承公共开关, 覆写 `@0` 为默认中文
- `mobile_t9.yaml` 九宫格入口, 挂载 `melt_eng` 翻译器, 注入九键拼写映射

### 主词库

- `rime_frost.dict.yaml` -> `rime_ice.dict.yaml` 导入白霜词库, 去除低频词

## 鸣谢

- [iDvel/rime-ice](https://github.com/iDvel/rime-ice) (GPL-3.0) -- 雾凇框架
- [gaboolic/rime-frost](https://github.com/gaboolic/rime-frost) (GPL-3.0) -- 白霜词库
- [amzxyz/RIME-LMDG](https://github.com/amzxyz/RIME-LMDG) (CC-BY-4.0) -- 万象语法模型

## [LICENSE](./LICENSE)

本项目代码与框架部分采用 **[GPL-3.0-only](https://spdx.org/licenses/GPL-3.0-only.html)** 协议开源

基于本项目"三源融合"的特性, 各组件的知识产权与授权细则如下:

- **输入法框架与配置** (源自 [iDvel/rime-ice](https://github.com/iDvel/rime-ice) & [gaboolic/rime-frost](https://github.com/gaboolic/rime-frost)): 基于 **[GPL-3.0-only](https://spdx.org/licenses/GPL-3.0-only.html)** 协议分发
- **万象语法模型** (源自 [amzxyz/RIME-LMDG](https://github.com/amzxyz/RIME-LMDG)): 基于 **[CC-BY-4.0](https://spdx.org/licenses/CC-BY-4.0.html)** 协议分发
