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

| secret键       | 值   | 备注    |
| :------------ | :-- | ----- |
| WEREAD_COOKIE |  wr_fp=123456789; wr_vid=12345678; wr_rt=XXXXXXXXXXXXXXXXX; wr_skey=XXXXXXXXXX   |     |

4. 在`Settings->Secrets and variables`中添加`Variables`，以下按需自行修改值。

| variables键      | （默认）值        | 备注              |
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
### 默认配色

| 颜色值       | 说明                  | 预览                               |
|--------------|-----------------------|-----------------------------------|
| `#9BE9A8` | 最浅色（低活跃度）     | [HTMLColorCodes](https://htmlcolorcodes.com/#9BE9A8) |
| `#40C463` | 中等偏浅（原色 1）     | <div style="background:#40C463; width: 60px; height: 20px;"></div> |
| `#30A14E` | 中等偏深（过渡色）     | <div style="background:#30A14E; width: 60px; height: 20px;"></div> |
| `#216E39` | 最深色（高活跃度）     | <div style="background:#216E39; width: 60px; height: 20px;"></div> |

### 秋天

| 颜色值       | 说明                  | 预览                               |
|--------------|-----------------------|-----------------------------------|
| `#FFF7B2` | 最浅色（低活跃度）     | <div style="background:#FFF7B2; width: 60px; height: 20px;"></div> |
| `#FFEE4A` | 中等偏浅（原色 1）     | <div style="background:#FFEE4A; width: 60px; height: 20px;"></div> |
| `#FFD700` | 中等偏深（过渡色）     | <div style="background:#FFD700; width: 60px; height: 20px;"></div> |
| `#FFA500` | 最深色（高活跃度）     | <div style="background:#FFA500; width: 60px; height: 20px;"></div> |


## TIP

本项目灵感来自于[Weread2NotionPro](https://github.com/malinkang/weread2notion-pro.git)，在此再次表示衷心感谢！


