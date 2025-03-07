## 说明

一个微信阅读阅读时长的热力图
之前是使用[Weread2Notion](https://github.com/malinkang/weread2notion-pro.git)进行生成，因去年转向Obsidian，Obsidian中的Weread插件也很好用，而且也搞了个[obsidian-readingcard](https://github.com/ZiGmaX809/obsidian-readingcard-template.git)的模板，用来展示微信阅读的进度
考虑到原来生成热力图的方式还需要链接Notion感觉麻烦，所以用了一天时间结合AI重构了热力图的生成的实现

## 使用
1. fork本项目
2. 获取微信阅读的`cookie`—— 获取方法请查询相关项目的手册，仅需其中的`wr_fp=123456789; wr_vid=12345678; wr_rt=XXXXXXXXXXXXXXXXX; wr_skey=XXXXXXXXXX`，`cookie`过期会尝试自动刷新
3. 点击Settings->Secrets and variables->New repository secret

| secret键       | 值   | 备注    |
| :------------ | :-- | ----- |
| WEREAD_COOKIE |     |     |

4. 在`Settings->Secrets and variables`中添加`variables`，以下按需自行修改值

| variables键       | 值         | 备注                      |
| ---------------- | --------- | ----------------------- |
| START_YEAR             | `2024`    | 开始年份                      |
| END_YEAR             | `2025`    | 结束年份                      |
| NAME             | `ZiGma's Read Time Heatmap`    | 卡片标题  |

5. 项目自动运行后会在根目录下生成`heatmap.svg`文件，直接在Obsidian中进行引用即可


## TIP

本项目灵感来自于[Weread2Notion](https://github.com/malinkang/weread2notion-pro.git)，在此表示衷心感谢


