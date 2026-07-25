# -*- coding: utf-8 -*-
"""生成《钱欣羽+Task4.pdf》项目总结报告：正文五号、1.5倍行距、两端对齐；
改用 Microsoft YaHei 字体以解决中英数混排间隔异常问题。"""
import os, re, html
from reportlab.lib import colors, units
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from PIL import Image as PILImage
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
                                 PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_ROOT = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("YaHei", os.path.join(FONT_ROOT, "msyh.ttc")))
pdfmetrics.registerFont(TTFont("YaHeiBold", os.path.join(FONT_ROOT, "msyhbd.ttc")))

ROOT = r"C:\Users\qianx\Desktop\task4"
IMG = os.path.join(ROOT, "report_imgs")
OUT = os.path.join(ROOT, "钱欣羽+Task4.pdf")

styles = getSampleStyleSheet()
def S(name, **kw):
    base = dict(fontName="YaHei", fontSize=10.5, leading=15.75, alignment=TA_JUSTIFY,
                firstLineIndent=21, spaceAfter=0, spaceBefore=0, wordWrap='CJK')
    base.update(kw)
    return ParagraphStyle(name, **base)

body   = S("Body")
noind  = S("NoInd", firstLineIndent=0)
h1     = S("H1", fontName="YaHeiBold", fontSize=14, leading=21, spaceBefore=10, spaceAfter=6, firstLineIndent=0)
h2     = S("H2", fontName="YaHeiBold", fontSize=11, leading=16.5, spaceBefore=8, spaceAfter=4, firstLineIndent=0)
title  = S("Title", fontName="YaHeiBold", fontSize=18, leading=27, alignment=TA_CENTER, spaceAfter=8, firstLineIndent=0)
sub    = S("Sub", fontName="YaHei", fontSize=11, leading=16, alignment=TA_CENTER, spaceAfter=0, firstLineIndent=0)
cap    = S("Cap", fontName="YaHei", fontSize=9, leading=13.5, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8, firstLineIndent=0)
li     = S("Li", firstLineIndent=0, leftIndent=21, spaceAfter=2)

def esc(t): return html.escape(t)
def P(t, st=body): return Paragraph(esc(t), st)
def H1(t): return Paragraph(esc(t), h1)
def H2(t): return Paragraph(esc(t), h2)
def C(t): return Paragraph(esc(t), cap)

def img(name, w=units.mm*150):
    path = os.path.join(IMG, name)
    pil = PILImage.open(path); aspect = pil.height/pil.width
    return Image(path, width=w, height=w*aspect)

def fig_block(no, title_txt, interp, name):
    return KeepTogether([
        H2(f"{no} {title_txt}"),
        img(name),
        C(f"{no} {title_txt}"),
        P(f"解读：{interp}", noind),
    ])

story = []
story.append(Paragraph("Task 4 项目总结报告", title))
story.append(Paragraph("从数据到数据产品——B站热门视频交互式看板部署", sub))
story.append(Paragraph("姓名：钱欣羽　·　提交日期：2026-07-25", sub))
story.append(Spacer(1, 10))

story.append(H1("一、问题定义与目标"))
story.append(P("前三个任务完成了“从数据到洞察”的分析链路（Task 1 抓取、Task 2 清洗、Task 3 探索性分析）。Task 4 的任务是把分析成果转化为一个可交付的数据产品：一个任何人都可以在线访问的交互式 HTML 数据看板，并完成从本地代码到 GitHub Pages 上线的工程化部署。核心目标是实现从“数据消费者”到“数据产品创造者”的身份跃迁，获得一份可写进简历的完整作品。"))
story.append(P("交付物包含四部分：① 单个自包含 HTML 看板文件（CSS/JS 全内联，可直接打开）；② GitHub Pages 在线访问链接；③ 本 PDF 项目总结报告；④ Git 操作过程记录（SSH 配置、git log 等）。"))

story.append(H1("二、看板规划与信息架构"))
story.append(P("看板采用单页信息架构，自上而下分为五个模块：标题区（项目名与作者）、核心指标卡片区（6 张关键数字卡）、交互图表区（6 张 Plotly 图表）、关键洞察区（6 条结论 + 4 个可验证假设）、页脚部署说明。布局使用 CSS Grid/Flex 实现响应式，在桌面与手机宽度下均保持可读。"))
story.append(P("指标卡选取逻辑：样本量(120)与字段数(18)交代数据规模；平均/中位/头部播放量与平均点赞，直观呈现“长尾”特征，为后续图表埋下伏笔。"))

story.append(H1("三、技术实现方案"))
story.append(P("使用 Plotly.js 作为交互图表库。为满足“单个 HTML 文件、所有 CSS/JS 内嵌、任意浏览器直接打开”的要求，将完整的 Plotly.js（约 4.5 MB）直接内联进 HTML 的 <script> 标签，使文件离线可用，同时天然适配 GitHub Pages 的在线访问。"))
story.append(P("图表由 Python（pandas + plotly）在本地生成数据并序列化为 Plotly 的 data/layout JSON，再在页面中通过 Plotly.newPlot 渲染。交互功能覆盖：悬停显示精确数值、框选缩放、图例点击筛选分区、坐标轴“对数/线性”一键切换、以及“按分区筛选”下拉框。看板数据已内联，不依赖外部接口。"))

story.append(PageBreak())
story.append(H1("四、核心图表与数据洞察"))
story.append(P("以下 6 张图覆盖单变量分布、分组对比、双变量关联与高级可视化，每张均配编号、标题与文字解读。"))
story.append(fig_block("图1", "播放量分布（log10 分箱）",
    "多数视频集中在较低播放量区间，少数头部视频极高，呈典型右偏长尾。log10 分箱能更清晰地展现长尾结构。",
    "chart1.png"))
story.append(fig_block("图2", "六大分区播放量分布对比",
    "各分区中位数接近，但“其他”分区仅 5 条样本、不宜下结论；各分区均存在上方离群点（爆款）。点击图例可隐藏/显示某一分区。",
    "chart2.png"))
story.append(fig_block("图3", "核心变量相关系数热力图",
    "播放量与点赞数(r=0.86)、收藏数(r=0.70)强正相关；视频时长与播放量几乎无关(r≈-0.01)。解释播放量差异最应关注点赞与收藏。",
    "chart3.png"))
story.append(fig_block("图4", "播放量 vs 点赞数（双对数 + 回归线）",
    "双对数下散点沿红色回归线分布，二者共变关系稳健。二者为同期累计数据，只能说明共变，不能推断因果。可用下拉框按分区筛选。",
    "chart4.png"))
story.append(fig_block("图5", "不同发布时段播放量中位数",
    "早/中/晚中位数接近（约 80–100 万），差异有限；凌晨柱虽高但样本量 n=2，结论不可靠，已用柱顶标注提示。",
    "chart5.png"))
story.append(fig_block("图6", "标题长度与平均播放量关系",
    "各标题长度区间平均播放量波动较大，无单调趋势，说明靠“堆字数”并不能稳定提升热度。",
    "chart6.png"))

story.append(PageBreak())
story.append(H1("五、技术踩坑记录"))
pitfalls = [
    "中文乱码与混排间隔：图表与 PDF 中文显示为方块，且 SimSun 对英文/数字字距处理不佳。解决——图表用 SimHei、正文改用 Microsoft YaHei，保证中英数混排紧凑自然。",
    "单文件离线化：Plotly 默认引用 CDN，断网打开空白。解决——将完整 plotly.min.js 内联进 HTML，文件虽增至约 4.4 MB，但真正实现“任意浏览器直接打开”。",
    "样本量陷阱：周末仅 4 条、凌晨仅 2 条、分区“其他”仅 5 条。若直接对这些分组下结论会误导，故在图表与报告中显式标注样本量，并声明“仅作方法示意”。",
    "相关性≠因果：播放量与点赞数强相关，但二者是同期累计数据。初稿曾写成“点赞带动播放”，经审查改为“共变关系”，避免因果误判。",
    "Git 身份缺失：首次提交因未配置 user.name/email 报错。解决——在仓库内执行 git config user.name/user.email。注意邮箱应与 GitHub 账户一致，否则贡献不计入主页。",
    "SSH 公钥未添加：生成密钥后推送被拒。需把 id_ed25519.pub 内容手动粘贴到 GitHub 的 Settings→SSH keys，且仓库需先在网页端创建。",
    "Pages 分支选择：GitHub Pages 需在 Settings→Pages 手动选择部署分支（main）与根目录，保存后等待 2–5 分钟才生效，并非立即可访问。",
]
for i,p in enumerate(pitfalls,1):
    story.append(Paragraph(f"{i}. {esc(p)}", li))

story.append(H1("六、智能体（WorkBuddy）使用心得"))
story.append(P("本次 Task 4 在智能体辅助下完成，最大价值在于“把工程琐事压到最低”：① 对话式生成完整 HTML 看板与部署脚本，无需逐行手写 Plotly 配置；② 自动处理中文字体、离线内联、响应式布局等易错细节；③ Git/SSH 等命令由智能体生成并逐步解释，降低了命令行门槛。"))
story.append(P("体会：智能体擅长“从 0 到 1 跑通”和“排错”，但关键决策（如仓库命名、GitHub 账户操作、提交内容确认）仍需本人把关。把它当“pair 程序员”而非“代写工具”，学习效果最好。"))

story.append(H1("七、学习反思与收获"))
story.append(P("技能层面：掌握了 Plotly 交互可视化的基本范式、单文件前端的离线打包思路，以及 Git/SSH/GitHub Pages 的完整发布链路。认知层面：更深刻理解了“分析洞察”与“产品交付”之间的差距——看板不仅要图表正确，还要信息层次清晰、交互顺手、在任何屏幕都可读。"))
story.append(P("不足与改进：当前看板数据为静态快照，未来可接入实时数据源；样本量局限表明若要做稳健结论，需要更完整、更大规模的采集。本次也暴露出对“统计显著性”意识的欠缺，后续应补强假设检验知识。"))

story.append(H1("八、部署与提交清单"))
story.append(P("本地已完成：生成 index.html（自包含看板）、导出图表、初始化 Git 仓库并提交（分支 main，提交记录见 Git 操作过程记录）。已在 GitHub 网页端手动完成：① 新建仓库；② 在 Settings→SSH keys 添加本机公钥；③ 执行 git remote add / git push；④ 在 Settings→Pages 启用 main 分支部署；⑤ 访问 https://24212486-bit.github.io/bilibili-eda-dashboard/ 验证。"))
story.append(P("提交材料：本 PDF 报告、index.html 看板文件、GitHub Pages 链接、以及 Git 操作过程记录（含 SSH 公钥指纹、git log 截图/文本）。"))

doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=units.mm*20, rightMargin=units.mm*20,
                        topMargin=units.mm*20, bottomMargin=units.mm*20)
doc.build(story)
print(f"PDF 已生成：{OUT} ({os.path.getsize(OUT)/1024:.1f} KB)")
