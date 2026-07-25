# -*- coding: utf-8 -*-
"""生成 Task4 单文件交互式看板 index.html（内联 Plotly.js，离线可直接打开）。"""
import os, json
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 相对路径：脚本与数据同目录，克隆仓库后可直接运行
ROOT = Path(__file__).resolve().parent
SRC  = ROOT / "clean_Task1_data.csv"
PLOTLY_JS = ROOT / "plotly.min.js"   # 已下载的离线库
OUT  = ROOT / "index.html"

df = pd.read_csv(SRC)
n = len(df)
ncols = 18

# ---------- 核心指标 ----------
mean_play   = df["播放量"].mean() / 1e4
median_play = df["播放量"].median() / 1e4
max_play    = df["播放量"].max() / 1e4
mean_like   = df["点赞数"].mean() / 1e4
mean_fav    = df["收藏数"].mean() / 1e4

cards = [
    ("样本量", f"{n}", "条已上榜热门视频"),
    ("字段数", f"{ncols}", "原始12 + 派生6"),
    ("平均播放量", f"{mean_play:,.1f} 万", "均值远高于中位数→长尾"),
    ("中位播放量", f"{median_play:,.1f} 万", "半数视频低于此值"),
    ("头部最高播放", f"{max_play:,.1f} 万", "少数爆款撑起流量"),
    ("平均点赞", f"{mean_like:,.1f} 万", "互动规模核心指标"),
]

# ---------- 颜色 ----------
ACCENT = "#FB7299"   # B站粉
PALETTE = ["#FB7299","#23ADE5","#FFB023","#7ED321","#9B59B6","#E74C3C"]

# ============ 图1：播放量分布直方图（可切换 对数/线性）============
fig1 = go.Figure(go.Histogram(
    x=df["播放量"], nbinsx=45, marker_color=ACCENT, opacity=0.85,
    hovertemplate="播放量区间: %{x}<br>视频数: %{y}<extra></extra>"))
fig1.update_layout(
    title="图1 播放量分布（默认对数坐标轴）",
    xaxis_title="播放量", yaxis_title="视频数量",
    xaxis_type="log",
    margin=dict(l=50,r=20,t=50,b=50), paper_bgcolor="white", plot_bgcolor="#fafafa")
fig1.update_traces(name="播放量")

# ============ 图2：分区大类播放量箱线图 ============
parts = ["知识/资讯","娱乐","游戏","动画/二次元","生活","其他"]
boxes = [go.Box(y=df.loc[df["分区大类"]==p,"播放量"], name=p,
                marker_color=PALETTE[i%len(PALETTE)], boxmean=True)
         for i,p in enumerate(parts)]
fig2 = go.Figure(boxes)
fig2.update_layout(
    title="图2 六大分区播放量分布对比（点击图例可隐藏/筛选分区）",
    yaxis_title="播放量", xaxis_title="分区大类",
    yaxis_type="log", showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    margin=dict(l=50,r=20,t=80,b=50), paper_bgcolor="white", plot_bgcolor="#fafafa")

# ============ 图3：变量相关性热力图 ============
num_cols = ["播放量","点赞数","收藏数","弹幕数","投币数","评论数","分享数","视频时长(秒)","标题长度"]
corr = df[num_cols].corr().round(2)
fig3 = go.Figure(go.Heatmap(
    z=corr.values, x=num_cols, y=num_cols,
    colorscale="RdBu", zmid=0, zmin=-1, zmax=1,
    text=corr.values, texttemplate="%{text}",
    colorbar=dict(title="相关系数"),
    hovertemplate="%{y} × %{x}<br>r=%{z}<extra></extra>"))
fig3.update_layout(
    title="图3 核心变量相关系数热力图",
    margin=dict(l=80,r=20,t=50,b=80), paper_bgcolor="white",
    height=520)

# ============ 图4：播放量 vs 点赞数 散点 + 回归（分区筛选）============
lp = np.log1p(df["播放量"].values)
ll = np.log1p(df["点赞数"].values)
b, a = np.polyfit(lp, ll, 1)
xs = np.linspace(lp.min(), lp.max(), 50)
ys = a + b*xs
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=df["播放量"], y=df["点赞数"], mode="markers",
    marker=dict(size=8, color=df["播放量"], colorscale="Viridis", showscale=False, opacity=0.8),
    name="视频",
    hovertemplate="播放量: %{x:,}<br>点赞数: %{y:,}<extra></extra>"))
fig4.add_trace(go.Scatter(
    x=np.expm1(xs), y=np.expm1(ys), mode="lines", name="全样本回归趋势线",
    line=dict(color="#E74C3C", width=3)))
fig4.update_layout(
    title="图4 播放量 vs 点赞数（双对数 + 回归线，可用下拉筛选分区）",
    xaxis_title="播放量", yaxis_title="点赞数",
    xaxis_type="log", yaxis_type="log",
    margin=dict(l=60,r=20,t=50,b=50), paper_bgcolor="white", plot_bgcolor="#fafafa")
# 供前端筛选用的原始数据
scatter_raw = {"play": df["播放量"].tolist(),
               "like": df["点赞数"].tolist(),
               "part": df["分区大类"].tolist()}

# ============ 图5：发布时段播放量中位数 + 样本量 ============
slot_order = ["早间(6-11)","午间(12-17)","晚间(18-23)","凌晨(0-5)"]
g = df.groupby("发布时段")["播放量"].agg(["median","count"]).reindex(slot_order)
fig5 = go.Figure(go.Bar(
    x=slot_order, y=g["median"].values/1e4,
    marker_color=["#23ADE5","#7ED321","#FB7299","#9B59B6"],
    text=[f"n={int(c)}" for c in g["count"].values],
    textposition="outside",
    hovertemplate="%{x}<br>中位数: %{y:.1f} 万<extra></extra>"))
fig5.update_layout(
    title="图5 不同发布时段播放量中位数（柱顶标注样本量）",
    yaxis_title="播放量中位数（万）", xaxis_title="发布时段",
    margin=dict(l=50,r=20,t=50,b=50), paper_bgcolor="white", plot_bgcolor="#fafafa")

# ============ 图6：标题长度 vs 平均播放量 折线 ============
tg = df.groupby("标题长度")["播放量"].mean()/1e4
fig6 = go.Figure(go.Scatter(
    x=tg.index.tolist(), y=tg.values.tolist(), mode="lines+markers",
    line=dict(color="#FFB023", width=3), marker=dict(size=8),
    hovertemplate="标题长度: %{x} 字<br>平均播放: %{y:.1f} 万<extra></extra>"))
fig6.update_layout(
    title="图6 标题长度与平均播放量关系",
    xaxis_title="标题长度（字）", yaxis_title="平均播放量（万）",
    margin=dict(l=50,r=20,t=50,b=50), paper_bgcolor="white", plot_bgcolor="#fafafa")

# ============ 组装 HTML ============
chart_defs = [
    ("chart1", fig1.to_plotly_json(), "图1 播放量分布直方图",
     "多数视频集中在较低播放量区间，少数头部视频极高，呈典型右偏长尾。点击上方按钮可在“对数/线性”坐标轴间切换，对数视图能更清楚地看清长尾结构。"),
    ("chart2", fig2.to_plotly_json(), "图2 六大分区播放量对比",
     "各分区播放量中位数与离散程度存在明显差异，动画/二次元及“其他”分区相对较高；但“其他”仅有 5 条样本，不能作为稳健结论。各分区均存在上方离群点（爆款）。点击图上方图例可隐藏/显示某一分区，实现维度筛选。"),
    ("chart3", fig3.to_plotly_json(), "图3 变量相关性热力图",
     "播放量与点赞数(r=0.86)、收藏数(r=0.70)强正相关；视频时长与播放量几乎无关(r≈-0.01)。想解释播放量差异，最该关注点赞与收藏。"),
    ("chart4", fig4.to_plotly_json(), "图4 播放量 vs 点赞数 散点",
     "双对数下散点沿红色回归线分布，二者共变关系稳健。二者为同期累计数据，只能说明共变，不能推断因果。可通过下拉框筛选不同分区的视频散点，红色趋势线代表全样本整体回归关系。"),
    ("chart5", fig5.to_plotly_json(), "图5 发布时段中位数",
     "早/中/晚中位数接近（约 80–100 万），差异有限；凌晨柱虽高但样本量 n=2，结论不可靠，已用柱顶标注提示。"),
    ("chart6", fig6.to_plotly_json(), "图6 标题长度 vs 平均播放量",
     "各标题长度区间平均播放量波动较大，无单调趋势，说明靠“堆字数”并不能稳定提升热度。"),
]

cards_html = "".join(
    f'<div class="metric"><div class="m-label">{l}</div><div class="m-value">{v}</div><div class="m-sub">{s}</div></div>'
    for l,v,s in cards)

charts_html = ""
charts_js = ""
for cid, spec, title, interp in chart_defs:
    charts_html += f'''
    <section class="card">
      <h2>{title}</h2>
      <div id="{cid}" class="plot"></div>
      <p class="insight"><b>解读：</b>{interp}</p>
    </section>'''
    charts_js += f"Plotly.newPlot('{cid}', {json.dumps(spec['data'])}, {json.dumps(spec['layout'])}, CONFIG);\n"

# 图1 对数/线性 切换按钮 + 图4 分区筛选下拉
controls_html = '''
    <div class="controls">
      <button id="btnLog" class="btn">切换 对数/线性 坐标轴（图1）</button>
      <label class="sel-label">图4 按分区筛选：
        <select id="selPart" class="sel">
          <option value="__all__">全部</option>
        </select>
      </label>
    </div>'''

controls_js = r'''
  // 图1 坐标轴切换
  let histLog = true;
  document.getElementById('btnLog').addEventListener('click', () => {
    histLog = !histLog;
    Plotly.relayout('chart1', {'xaxis.type': histLog ? 'log' : 'linear'});
  });
  // 图4 分区下拉
  const raw = __SCATTER_RAW__;
  const parts = Array.from(new Set(raw.part));
  const sel = document.getElementById('selPart');
  parts.forEach(p => { const o=document.createElement('option'); o.value=p; o.textContent=p; sel.appendChild(o); });
  sel.addEventListener('change', () => {
    const v = sel.value;
    let idx = raw.play.map((_,i)=>i);
    if (v !== '__all__') idx = idx.filter(i => raw.part[i] === v);
    const fx = idx.map(i=>raw.play[i]);
    const fy = idx.map(i=>raw.like[i]);
    // 只更新第0个图层（散点），第1个图层（全样本回归趋势线）保持不变
    Plotly.restyle('chart4', {x:[fx], y:[fy]}, [0]);
  });
'''.replace("__SCATTER_RAW__", json.dumps(scatter_raw))

with open(PLOTLY_JS, encoding="utf-8") as f:
    plotly_src = f.read()

CONFIG = json.dumps({"responsive": True, "displaylogo": False,
                     "modeBarButtonsToRemove": ["select2d","lasso2d"]})

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>B站热门视频 · 探索性数据分析看板（Task 4）</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB",sans-serif;
         background:#f5f7fa; color:#2c3e50; }}
  header {{ background:linear-gradient(135deg,#1f2a44,#2c3e6b); color:#fff; padding:28px 24px; }}
  header h1 {{ margin:0 0 6px; font-size:24px; }}
  header p {{ margin:0; opacity:.85; font-size:13px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .metrics {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:14px; margin:18px 0; }}
  .metric {{ background:#fff; border-radius:12px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,.06);
            border-left:4px solid {ACCENT}; }}
  .m-label {{ font-size:13px; color:#7f8c8d; }}
  .m-value {{ font-size:22px; font-weight:700; color:#2c3e6b; margin:4px 0; }}
  .m-sub {{ font-size:12px; color:#95a5a6; }}
  .card {{ background:#fff; border-radius:12px; padding:18px 20px; margin:18px 0;
          box-shadow:0 2px 10px rgba(0,0,0,.07); }}
  .card h2 {{ font-size:17px; margin:0 0 12px; color:#2c3e6b; border-bottom:2px solid #eee; padding-bottom:8px; }}
  .plot {{ width:100%; height:430px; }}
  .insight {{ font-size:13.5px; line-height:1.7; color:#34495e; background:#fafbfc;
             border-left:3px solid {ACCENT}; padding:10px 14px; margin:10px 0 0; border-radius:0 6px 6px 0; }}
  .controls {{ display:flex; flex-wrap:wrap; gap:16px; align-items:center; margin:6px 0 4px; }}
  .btn {{ background:{ACCENT}; color:#fff; border:none; padding:8px 14px; border-radius:8px;
         cursor:pointer; font-size:13px; }}
  .btn:hover {{ opacity:.9; }}
  .sel-label {{ font-size:13px; }}
  .sel {{ padding:6px 8px; border-radius:6px; border:1px solid #ccc; font-size:13px; }}
  .insights-box {{ background:#fff; border-radius:12px; padding:20px; margin:18px 0;
                  box-shadow:0 2px 10px rgba(0,0,0,.07); }}
  .insights-box h2 {{ color:#2c3e6b; }}
  .insights-box li {{ line-height:1.8; font-size:14px; margin:6px 0; }}
  footer {{ text-align:center; color:#95a5a6; font-size:12px; padding:24px; }}
  @media (max-width:600px) {{ .plot {{ height:340px; }} header h1 {{ font-size:20px; }} }}
</style>
</head>
<body>
<header>
  <h1>B站热门视频 · 探索性数据分析看板</h1>
  <p>Task 4 数据产品 · 钱欣羽 · 基于 120 条热门视频快照（2026）</p>
</header>
<div class="wrap">
  <div class="metrics">{cards_html}</div>

  <div class="card">
    <h2>交互式图表</h2>
    {controls_html}
    {charts_html}
  </div>

  <div class="insights-box">
    <h2>关键数据洞察</h2>
    <ol>
      <li><b>流量由少数头部视频主导：</b>播放量、点赞、收藏、弹幕均呈右偏长尾，均值远高于中位数，少数爆款贡献大部分流量。</li>
      <li><b>播放量与点赞、收藏强正相关（共变）：</b>r 分别约 0.86 / 0.70；但二者为同期累计数据，不能推断因果。</li>
      <li><b>视频时长与播放量几乎无关：</b>相关系数约 -0.01，靠“堆时长”提升热度缺乏证据。</li>
      <li><b>内容赛道差异显著：</b>分区中位数与离群点不同，应分赛道建立基准。</li>
      <li><b>发布时段差异有限且样本不均：</b>早/中/晚接近，凌晨 n=2 不可靠。</li>
      <li><b>UP主重复上榜数据不足：</b>“多次上榜”代理组仅 4 条，仅作方法示意。</li>
    </ol>
  </div>

  <div class="insights-box">
    <h2>面向 Task 4 看板的可验证假设</h2>
    <ul>
      <li>H1 互动规模指标可解释热门视频间的播放量差异（预测需避免数据泄漏）。</li>
      <li>H2 不同分区的互动转化率存在显著差异，可建对标基线。</li>
      <li>H3 早/中/晚时段对播放量中位数可能存在影响（Kruskal-Wallis 检验）。</li>
      <li>H4 标题长度落在某区间的视频平均播放量是否显著更高（分组中位数检验）。</li>
    </ul>
  </div>
</div>
<footer>数据看板由 Plotly.js 驱动 · 单文件离线可运行 · 部署于 GitHub Pages</footer>

<script>{plotly_src}</script>
<script>
  const CONFIG = {CONFIG};
  {charts_js}
  {controls_js}
</script>
</body>
</html>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"看板已生成：{OUT} ({os.path.getsize(OUT)/1024/1024:.2f} MB)")
