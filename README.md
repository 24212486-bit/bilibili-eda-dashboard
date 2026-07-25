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
  4. 播放量 vs 点赞数 散点 + 回归（按分区筛选）
  5. 发布时段播放量中位数（标注样本量）
  6. 标题长度 vs 平均播放量
- 关键数据洞察 + 面向 Task 4 的可验证假设。

## 本地预览
直接双击 `index.html`，或用浏览器打开 `file:///.../task4/index.html`。

## 部署到 GitHub Pages（需在 GitHub 网页端手动完成）
1. 登录 GitHub，新建仓库（如 `bilibili-eda-dashboard`）。
2. 在 **Settings → SSH and GPG keys** 添加本机公钥（`id_ed25519.pub` 内容）。
3. 本地执行：
   ```bash
   git remote add origin git@github.com:<你的用户名>/<仓库名>.git
   git branch -M main
   git push -u origin main
   ```
4. 仓库 **Settings → Pages**，Source 选择 `main` 分支 `/ (root)`，保存。
5. 等待 2–5 分钟，访问 `https://<你的用户名>.github.io/<仓库名>/`。
