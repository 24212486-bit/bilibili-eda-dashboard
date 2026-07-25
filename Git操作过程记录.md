# Git 操作过程记录（Task 4）

> 本文件记录 Task 4 从 SSH 配置到 GitHub Pages 上线的完整真实操作过程，所有命令输出均为本机实际执行结果。
> 姓名：钱欣羽　GitHub 账号：24212486-bit　仓库：bilibili-eda-dashboard

## 1. SSH 密钥配置（已完成）

生成 ed25519 密钥对：

```
ssh-keygen -t ed25519 -C "qianx-task4-github" -f ~/.ssh/id_ed25519 -N ""
```

生成的公钥（已添加到 GitHub → Settings → SSH and GPG keys）：

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILVKo+qHi4nuMTynFXFaqvSMFTGlji5tkHIP5xH4NZda qianx-task4-github
```

私钥指纹：

```
256 SHA256:FHRs9/KeTnFpjgkZExR3s7Dd94mrxKoKkoKYIE96E3k qianx-task4-github (ED25519)
```

SSH 连接验证（`ssh -T git@github.com` 实际输出）：

```
Hi 24212486-bit! You've successfully authenticated, but GitHub does not provide shell access.
```

## 2. 本地仓库初始化与提交（已完成）

```
git init
git config user.name "钱欣羽"
git config user.email "24212486-bit@users.noreply.github.com"
git add index.html build_dashboard.py README.md
git commit -m "Task4: 添加交互式 B站热门视频数据看板（单文件 HTML + Plotly）"
git branch -M main
```

说明：邮箱使用 GitHub 官方隐私邮箱 `24212486-bit@users.noreply.github.com`，提交会正常计入本人 GitHub 账号贡献。

## 3. 远程仓库配置与推送（已完成）

`git remote -v` 实际输出：

```
origin	git@github.com:24212486-bit/bilibili-eda-dashboard.git (fetch)
origin	git@github.com:24212486-bit/bilibili-eda-dashboard.git (push)
```

首次推送 `git push -u origin main` 实际输出（节选）：

```
To github.com:24212486-bit/bilibili-eda-dashboard.git
 * [new branch]      main -> main
Branch 'main' set up to track 'origin/main'.
```

后续修复推送（`git push`）实际输出：

```
To github.com:24212486-bit/bilibili-eda-dashboard.git
   ff4aebf..d4e0520  main -> main
```

`git log --oneline -5` 实际输出（含提交时间）：

```
d4e0520 2026-07-25 22:06 docs: 报告生成脚本正文字体改宋体(SimSun)符合作业格式要求
accd4bc 2026-07-25 22:05 fix: 图4筛选只更新散点层保留全样本回归线；图2开启图例筛选；PDF正文改宋体；加入CSV并改相对路径
ff4aebf 2026-07-25 21:27 docs: 修复 PDF 中英数混排间隔与图1缺失问题
87d3653 2026-07-25 19:32 Task4: 添加交互式 B站热门视频数据看板（单文件 HTML + Plotly）
```

仓库当前包含文件：`index.html`、`README.md`、`build_dashboard.py`、`clean_Task1_data.csv`、`钱欣羽+Task4.pdf`。

## 4. GitHub Pages 部署（已完成）

1. 仓库 → Settings → Pages。
2. Source 选择 **Deploy from a branch**，Branch 选择 **main**、文件夹 **/ (root)**，点击 Save。
3. 等待约 2–5 分钟部署生效。

在线访问地址（已验证可正常打开，图表、指标卡、洞察内容显示完整）：

**https://24212486-bit.github.io/bilibili-eda-dashboard/**

## 5. 截图材料清单

以下命令输出已在本文档以文本形式完整记录；建议提交前再补充对应截图作为佐证：

- [x] `ssh -T git@github.com` 成功回显（见第 1 节文本记录）
- [x] `git remote -v` / `git log` 输出（见第 3 节文本记录）
- [x] `git push` 成功输出（见第 3 节文本记录）
- [ ] GitHub → Settings → SSH keys 页面截图（公钥已添加）
- [ ] GitHub 仓库首页截图（含 index.html 等文件）
- [ ] GitHub Pages 设置页截图（main / root 已保存）
- [ ] 浏览器打开在线看板的截图（含地址栏）

> 提交前最终验证建议：用浏览器无痕窗口（或退出 GitHub 账号后）打开上述在线链接，点击图表测试悬停、缩放与筛选功能，并保存一张包含浏览器地址栏的截图。
