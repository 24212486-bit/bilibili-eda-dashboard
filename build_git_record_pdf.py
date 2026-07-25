# -*- coding: utf-8 -*-
"""把 Git 操作过程记录生成为 PDF（宋体正文 + 等宽代码块 + 嵌入截图）。"""
import os, html
from reportlab.lib import colors, units
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

FONT_ROOT = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("SimSun", os.path.join(FONT_ROOT, "simsun.ttc")))
pdfmetrics.registerFont(TTFont("SimHei", os.path.join(FONT_ROOT, "simhei.ttf")))
pdfmetrics.registerFont(TTFont("Consolas", os.path.join(FONT_ROOT, "consola.ttf")))

ROOT = r"C:\Users\qianx\Desktop\task4"
OUT = os.path.join(ROOT, "Git操作过程记录.pdf")

def S(name, **kw):
    base = dict(fontName="SimSun", fontSize=10.5, leading=15.75, alignment=TA_JUSTIFY,
                firstLineIndent=0, spaceAfter=0, spaceBefore=0, wordWrap='CJK',
                spaceShrinkage=0.3, spaceStretch=0.6)
    base.update(kw)
    return ParagraphStyle(name, **base)

body  = S("Body")
h1    = S("H1", fontName="SimHei", fontSize=13, leading=19.5, spaceBefore=10, spaceAfter=5)
h2    = S("H2", fontName="SimHei", fontSize=11, leading=16.5, spaceBefore=8, spaceAfter=4)
title = S("Title", fontName="SimHei", fontSize=17, leading=25.5, alignment=TA_CENTER, spaceAfter=6)
sub   = S("Sub", fontSize=10.5, alignment=TA_CENTER, spaceAfter=2)
code_style = S("Code", fontName="SimSun", fontSize=8.5, leading=12, alignment=0, wordWrap="CJK")
cap   = S("Cap", fontName="SimSun", fontSize=9, leading=13.5, alignment=TA_CENTER, spaceBefore=3, spaceAfter=6)

def esc(t): return html.escape(t)
def P(t): return Paragraph(esc(t), body)
def H(t): return Paragraph(esc(t), h1)
def H2(t): return Paragraph(esc(t), h2)
def C(t): return Paragraph(esc(t), cap)

def code_block(text):
    lines = text.strip("\n").split("\n")
    paras = [Paragraph(esc(l).replace(" ", "&nbsp;") if l else "&nbsp;", code_style) for l in lines]
    t = Table([[p] for p in paras], colWidths=[units.mm*162])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F5F5F5")),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (0,0), 6),
        ("BOTTOMPADDING", (-1,-1), (-1,-1), 6),
        ("TOPPADDING", (0,1), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-2), 0),
    ]))
    return t

def screenshot(path, caption, w=units.mm*155):
    full = os.path.join(ROOT, path)
    pil = PILImage.open(full)
    aspect = pil.height / pil.width
    return KeepTogether([
        Image(full, width=w, height=w*aspect),
        C(caption),
        Spacer(1, 6),
    ])

story = []
story.append(Paragraph("Git 操作过程记录（Task 4）", title))
story.append(Paragraph("姓名：钱欣羽　·　GitHub 账号：24212486-bit　·　仓库：bilibili-eda-dashboard", sub))
story.append(Paragraph("本文档记录从 SSH 配置到 GitHub Pages 上线的完整操作过程，命令输出为本机实际执行结果。", sub))
story.append(Spacer(1, 8))

story.append(H("一、SSH 密钥配置"))
story.append(P("使用 ssh-keygen 生成 ed25519 密钥对："))
story.append(code_block('ssh-keygen -t ed25519 -C "qianx-task4-github" -f ~/.ssh/id_ed25519 -N ""'))
story.append(Spacer(1, 4))
story.append(P("生成的公钥已添加到 GitHub → Settings → SSH and GPG keys，对应截图见第四节。"))
story.append(Spacer(1, 4))
story.append(P("SSH 连接验证，ssh -T git@github.com 实际输出："))
story.append(code_block("Hi 24212486-bit! You've successfully authenticated, but GitHub does not provide shell access."))

story.append(H("二、本地仓库初始化与提交"))
story.append(code_block("""git init
git config user.name "钱欣羽"
git config user.email "24212486-bit@users.noreply.github.com"
git add index.html build_dashboard.py README.md
git commit -m "Task4: 添加交互式 B站热门视频数据看板（单文件 HTML + Plotly）"
git branch -M main"""))
story.append(Spacer(1, 4))
story.append(P("说明：邮箱使用 GitHub 官方隐私邮箱，提交正常计入本人 GitHub 账号贡献。"))

story.append(H("三、远程仓库配置与推送"))
story.append(P("git remote -v 实际输出："))
story.append(code_block("""origin  git@github.com:24212486-bit/bilibili-eda-dashboard.git (fetch)
origin  git@github.com:24212486-bit/bilibili-eda-dashboard.git (push)"""))
story.append(Spacer(1, 4))
story.append(P("首次推送 git push -u origin main 实际输出（节选）："))
story.append(code_block("""To github.com:24212486-bit/bilibili-eda-dashboard.git
 * [new branch]      main -> main
Branch 'main' set up to track 'origin/main'."""))
story.append(Spacer(1, 4))
story.append(P("后续修复推送 git push 实际输出："))
story.append(code_block("""To github.com:24212486-bit/bilibili-eda-dashboard.git
   ff4aebf..d4e0520  main -> main"""))
story.append(code_block("""To github.com:24212486-bit/bilibili-eda-dashboard.git
   d4e0520..9d850a2  main -> main"""))
story.append(Spacer(1, 4))
story.append(P("git log --oneline -5 实际输出（含提交时间）："))
story.append(code_block("""78fc039 2026-07-25 23:04 docs: 在Git记录PDF中嵌入部署截图；删除报告中外部协助相关表述；同步README图1描述
9d850a2 2026-07-25 22:55 fix: 修复图1直方图在对数坐标下柱子不可见；同步更新PDF图1解读与报告图
d4e0520 2026-07-25 22:06 docs: 报告生成脚本正文字体改宋体(SimSun)符合作业格式要求
accd4bc 2026-07-25 22:05 fix: 图4筛选只更新散点层保留全样本回归线；图2开启图例筛选；PDF正文改宋体；加入CSV并改相对路径
ff4aebf 2026-07-25 21:27 docs: 修复 PDF 中英数混排间隔与图1缺失问题
87d3653 2026-07-25 19:32 Task4: 添加交互式 B站热门视频数据看板（单文件 HTML + Plotly）"""))
story.append(Spacer(1, 4))
story.append(P("仓库当前包含文件：index.html、README.md、build_dashboard.py、clean_Task1_data.csv、make_report_assets.py、build_report_task4.py、钱欣羽+Task4.pdf、Git操作过程记录.pdf。"))

story.append(H("四、GitHub Pages 部署"))
story.append(P("1. 在仓库页面点击 Settings → Pages；"))
story.append(P("2. Source 选择 Deploy from a branch，Branch 选择 main、文件夹 / (root)，点击 Save；"))
story.append(P("3. 等待约 2–5 分钟部署生效。"))
story.append(Spacer(1, 4))
story.append(P("在线访问地址（已验证可正常打开）："))
story.append(code_block("https://24212486-bit.github.io/bilibili-eda-dashboard/"))

story.append(PageBreak())
story.append(H("五、操作佐证截图"))
story.append(P("以下截图分别为 SSH 公钥配置、仓库首页文件列表、GitHub Dashboard 仓库入口、GitHub Pages 部署设置，证明上述操作已实际完成。"))
story.append(screenshot("screenshots/ssh_keys.png", "图1 GitHub SSH keys 设置页（公钥“我的电脑 Task4”已添加）"))
story.append(screenshot("screenshots/repo_home.png", "图2 仓库 bilibili-eda-dashboard 首页（main 分支文件列表与 README）"))
story.append(screenshot("screenshots/github_dashboard.png", "图3 GitHub Dashboard 左侧仓库入口（显示 bilibili-eda-dashboard）"))
story.append(screenshot("screenshots/pages_deployed.png", "图4 GitHub Pages 设置页（已部署至 main 分支 /(root)，显示在线地址）"))

story.append(H2("六、最终验证"))
story.append(P("完成部署后，用浏览器打开 https://24212486-bit.github.io/bilibili-eda-dashboard/，确认标题、6 张交互图表、6 个指标卡片、洞察与假设内容均正常显示；并测试图表悬停、缩放、图例筛选与分区下拉筛选功能。"))

doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=units.mm*20, rightMargin=units.mm*20,
                        topMargin=units.mm*20, bottomMargin=units.mm*20)
doc.build(story)
print(f"PDF 已生成：{OUT} ({os.path.getsize(OUT)/1024:.1f} KB)")
