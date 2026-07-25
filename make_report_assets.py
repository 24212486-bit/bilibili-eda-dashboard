# -*- coding: utf-8 -*-
"""复刻看板中的 6 张图，导出 PNG 供 Task4 总结报告使用。"""
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go

ROOT = r"C:\Users\qianx\Desktop\task4"
SRC  = r"C:\Users\qianx\Desktop\task3\clean_Task1_data.csv"
OUTD = os.path.join(ROOT, "report_imgs")
os.makedirs(OUTD, exist_ok=True)

df = pd.read_csv(SRC)
ACCENT = "#FB7299"
PALETTE = ["#FB7299","#23ADE5","#FFB023","#7ED321","#9B59B6","#E74C3C"]

# 图1：改用 log10 分箱直方图，柱状更清楚，PDF 打印友好
f1 = go.Figure(go.Histogram(
    x=np.log10(df["播放量"].values),
    nbinsx=25,
    marker_color=ACCENT,
    marker_line_color="#333333",
    marker_line_width=1.2,
    opacity=0.95
))
f1.update_layout(
    title="图1 播放量分布（log10 分箱）",
    xaxis_title="log10(播放量)",
    yaxis_title="视频数量",
    bargap=0.15,
    margin=dict(l=50, r=20, t=50, b=50),
    paper_bgcolor="white",
    plot_bgcolor="#fafafa"
)

# 图2
parts = ["知识/资讯","娱乐","游戏","动画/二次元","生活","其他"]
f2 = go.Figure([go.Box(y=df.loc[df["分区大类"]==p,"播放量"], name=p,
                        marker_color=PALETTE[i%len(PALETTE)], boxmean=True) for i,p in enumerate(parts)])
f2.update_layout(title="图2 六大分区播放量分布对比", yaxis_title="播放量", xaxis_title="分区大类",
                yaxis_type="log", showlegend=False, margin=dict(l=50,r=20,t=50,b=50), paper_bgcolor="white", plot_bgcolor="#fafafa")

# 图3
num_cols = ["播放量","点赞数","收藏数","弹幕数","投币数","评论数","分享数","视频时长(秒)","标题长度"]
corr = df[num_cols].corr().round(2)
f3 = go.Figure(go.Heatmap(z=corr.values, x=num_cols, y=num_cols, colorscale="RdBu", zmid=0, zmin=-1, zmax=1,
                          text=corr.values, texttemplate="%{text}", colorbar=dict(title="相关系数")))
f3.update_layout(title="图3 核心变量相关系数热力图", margin=dict(l=80,r=20,t=50,b=80), paper_bgcolor="white", height=520)

# 图4
lp = np.log1p(df["播放量"].values); ll = np.log1p(df["点赞数"].values)
b,a = np.polyfit(lp, ll, 1); xs = np.linspace(lp.min(), lp.max(), 50); ys = a + b*xs
f4 = go.Figure()
f4.add_trace(go.Scatter(x=df["播放量"], y=df["点赞数"], mode="markers",
                        marker=dict(size=8, color=df["播放量"], colorscale="Viridis", opacity=0.8), name="视频"))
f4.add_trace(go.Scatter(x=np.expm1(xs), y=np.expm1(ys), mode="lines", name="回归趋势线", line=dict(color="#E74C3C", width=3)))
f4.update_layout(title="图4 播放量 vs 点赞数（双对数 + 回归线）", xaxis_title="播放量", yaxis_title="点赞数",
                 xaxis_type="log", yaxis_type="log", margin=dict(l=60,r=20,t=50,b=50), paper_bgcolor="white", plot_bgcolor="#fafafa")

# 图5
slot_order = ["早间(6-11)","午间(12-17)","晚间(18-23)","凌晨(0-5)"]
g = df.groupby("发布时段")["播放量"].agg(["median","count"]).reindex(slot_order)
f5 = go.Figure(go.Bar(x=slot_order, y=g["median"].values/1e4,
                      marker_color=["#23ADE5","#7ED321","#FB7299","#9B59B6"],
                      text=[f"n={int(c)}" for c in g["count"].values], textposition="outside"))
f5.update_layout(title="图5 不同发布时段播放量中位数", yaxis_title="播放量中位数（万）", xaxis_title="发布时段",
                 margin=dict(l=50,r=20,t=50,b=50), paper_bgcolor="white", plot_bgcolor="#fafafa")

# 图6
tg = df.groupby("标题长度")["播放量"].mean()/1e4
f6 = go.Figure(go.Scatter(x=tg.index.tolist(), y=tg.values.tolist(), mode="lines+markers",
                          line=dict(color="#FFB023", width=3), marker=dict(size=8)))
f6.update_layout(title="图6 标题长度与平均播放量关系", xaxis_title="标题长度（字）", yaxis_title="平均播放量（万）",
                 margin=dict(l=50,r=20,t=50,b=50), paper_bgcolor="white", plot_bgcolor="#fafafa")

for name, fig in [("chart1",f1),("chart2",f2),("chart3",f3),("chart4",f4),("chart5",f5),("chart6",f6)]:
    fig.write_image(os.path.join(OUTD, f"{name}.png"), width=720, height=430, scale=2)
    print("saved", name)
print("done")
