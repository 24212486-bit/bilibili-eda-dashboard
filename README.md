# B站热门视频 · 探索性数据分析看板（Task 4）

基于 Task 1–3 的成果，将 EDA 洞察转化为一个可在线访问的交互式数据看板。

## 文件说明
- `index.html`：**交付物（单文件）**。所有 CSS/JS 已内联，包含完整 Plotly.js，可直接双击用浏览器打开，离线可用。
- `build_dashboard.py`：看板生成脚本（读取 `clean_Task1_data.csv`，用 Plotly 生成图表并内联）。
- `clean_Task1_data.csv`：Task 2 清洗后的 120 条 × 18 列数据（看板数据已内联进 HTML，此文件仅作溯源）。

## 看板内容
- 核心指标卡片：样本量、字段数、平均/中位/头部播放量、平均点赞。
- 6 张交互图表（悬停看数值、框选缩放、图例筛选、坐标轴切换、分区下拉）：
  1. 播放量分布（对数/线性切换）
  2. 六大分区播放量对比（点击图例筛选）
  3. 变量相关性热力图
  4. 播放量 vs 点赞数 散点 + 回归（下拉框筛选分区散点，红色趋势线为全样本整体回归关系）
  5. 发布时段播放量中位数（标注样本量）
  6. 标题长度 vs 平均播放量
- 关键数据洞察 + 面向 Task 4 的可验证假设。

## 本地预览
直接双击 `index.html`，或用浏览器打开 `file:///.../task4/index.html`。

## 在线访问（已部署）
本项目已通过 GitHub Pages 部署上线：

**https://24212486-bit.github.io/bilibili-eda-dashboard/**

## 部署方式（记录）
1. GitHub 新建仓库 `bilibili-eda-dashboard`，Settings → SSH and GPG keys 添加本机公钥。
2. 本地执行：
   ```bash
   git remote add origin git@github.com:24212486-bit/bilibili-eda-dashboard.git
   git branch -M main
   git push -u origin main
   ```
3. 仓库 **Settings → Pages**，Source 选择 `main` 分支 `/ (root)`，保存，等待 2–5 分钟生效。
