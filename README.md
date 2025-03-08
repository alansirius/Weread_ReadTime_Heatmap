# 微信阅读阅读时长的热力图生成

## 展示
<img src="https://raw.githubusercontent.com/ZiGmaX809/Weread_ReadTime_Heatmap/main/heatmap.svg">

## 说明

之前阅读的热力图使用的是[Weread2NotionPro](https://github.com/malinkang/weread2notion-pro.git)项目进行生成。

考虑到从Notion全面转向Obsidian，而且Obsidian中的Weread插件相比之下更加友好并能够使用`dataviewjs`自定义展示方式，而我也因此搞了个[obsidian-readingcard](https://github.com/ZiGmaX809/obsidian-readingcard-template.git)的模板用以展示微信阅读的各项进度。

基于上述原因，用了一天时间研究了一下相关Api和绘制脚本逻辑并使用AI（吹一波Claude的代码能力），重构了热力图生成脚本。

## 使用
1. fork本项目。
2. 获取微信阅读的`cookie`—— 获取方法请查询相关项目的手册，仅需其中的`wr_fp=123456789; wr_vid=12345678; wr_rt=XXXXXXXXXXXXXXXXX; wr_skey=XXXXXXXXXX`，`cookie`过期会尝试自动刷新。
3. 点击`Settings->Secrets and variables->New repository secret`中添加`SecretS`。

| Secrets键     | 值   | 备注    |
| ------------ | -- | ----- |
| WEREAD_COOKIE |  wr_fp=123456789; wr_vid=12345678; wr_rt=XXXXXXXXXXXXXXXXX; wr_skey=XXXXXXXXXX   |     |

4. 在`Settings->Secrets and variables`中添加`Variables`，以下按需自行修改值。

| Variables键      | （默认）值        | 备注              |
| ---------------- | --------- | -----------------------|
| START_YEAR       | `2024`    | 开始年份                 |
| END_YEAR         | `2025`    | 结束年份                 |
| NAME             | 微信阅读热力图    | 卡片标题  |
| TEXT_COLOR       | #2D3436   |  默认文字颜色            |
| TITLE_COLOR      | #2D3436   |  标题颜色               |
| YEAR_TXT_COLOR   | #2D3436   |  年度阅读时间颜色         |
| MONTH_TXT_COLOR  | #2D3436   |  月份标签颜色            |
| TRACK_COLOR      | #EBEDF0   |  无阅读颜色              |
| TRACK_SPECIAL1_COLOR | #9BE9A8 |  一级颜色              |
| TRACK_SPECIAL2_COLOR | #40C463 |  二级颜色              |
| TRACK_SPECIAL3_COLOR | #30A14E |  三级颜色              |
| TRACK_SPECIAL4_COLOR | #216E39 |  四级颜色              |
| DEFAULT_DOM_COLOR | #EBEDF0 | 默认格子颜色                  |

5. 项目自动运行后会在根目录下生成`heatmap.svg`文件，直接在Obsidian中进行引用即可。

## 配色参考

自行逐个替换`TRACK_SPECIAL1_COLOR`至 `TRACK_SPECIAL4_COLOR`的值

### 默认配色

| 颜色值       | 预览                               |
|--------------|-----------------------------------|
| `#9BE9A8` | ![9BE9A8](./assets/9BE9A8.svg) |
| `#40C463` | ![40C463](./assets/40C463.svg) |
| `#30A14E` | ![30A14E](./assets/30A14E.svg) |
| `#216E39` | ![FFF7B2](./assets/216E39.svg) |

### 秋天

| 颜色值       | 预览                               |
|--------------|-----------------------------------|
| `#FFF7B2` | ![FFF7B2](./assets/FFF7B2.svg) |
| `#FFEE4A` | ![FFEE4A](./assets/FFEE4A.svg) |
| `#FFD700` | ![FFD700](./assets/FFD700.svg) |
| `#FFA500` | ![B5E1FF](./assets/FFA500.svg) |

### 天空

| 颜色值       | 预览                               |
|--------------|-----------------------------------|
| `#B5E1FF` | ![B5E1FF](./assets/B5E1FF.svg) |
| `#5AB6FD` | ![5AB6FD](./assets/5AB6FD.svg) |
| `#34A7FF` | ![34A7FF](./assets/34A7FF.svg) |
| `#0077CC` | ![0077CC](./assets/0077CC.svg) |

## TIP

本项目灵感来自于[Weread2NotionPro](https://github.com/malinkang/weread2notion-pro.git)，在此再次表示衷心感谢！


