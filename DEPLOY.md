# 趋势图分析工具 - Render 云端部署指南

## 一键部署到 Render（免费）

按照以下步骤操作，10 分钟内完成部署：

---

## 步骤 1：准备 GitHub 账号

1. 如果没有 GitHub 账号，去注册一个：https://github.com/signup
2. 登录 GitHub

---

## 步骤 2：创建 GitHub 仓库

### 方法 A：使用 GitHub Desktop（推荐，简单）

1. 下载安装 GitHub Desktop：https://desktop.github.com/
2. 打开 GitHub Desktop，登录你的 GitHub 账号
3. 点击 File → Add Local Repository
4. 选择文件夹：`C:\Users\pengzishan\trend-analyzer`
5. 如果提示"not a git repository"，点击"create a repository"
6. 填写：
   - Name: `trend-analyzer`
   - Description: 趋势图分析工具
   - 勾选 "Initialize this repository with a README"（取消勾选）
7. 点击 "Create Repository"
8. 点击 "Publish repository"
9. 取消勾选 "Keep this code private"（或保持私有也可以）
10. 点击 "Publish Repository"

### 方法 B：使用命令行

在 trend-analyzer 目录下打开命令行：

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/trend-analyzer.git
git push -u origin main
```

---

## 步骤 3：部署到 Render

1. 打开 Render 网站：https://render.com/
2. 点击右上角 "Get Started" 或 "Sign Up"
3. 选择 "GitHub" 登录（使用你的 GitHub 账号登录）
4. 授权 Render 访问你的 GitHub
5. 点击 "New +" → "Web Service"
6. 选择你刚才创建的 `trend-analyzer` 仓库
7. 配置如下：
   - **Name**: `trend-analyzer`（或其他你喜欢的名字）
   - **Region**: Singapore（或离你最近的）
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300`

8. 展开 "Advanced" 设置
9. 点击 "Add Environment Variable"
10. 添加环境变量：
    - Key: `CLAUDE_API_KEY`
    - Value: `你的Claude API密钥`

11. 选择 "Free" 计划
12. 点击 "Create Web Service"

---

## 步骤 4：等待部署完成

- Render 会自动开始构建和部署
- 等待 3-5 分钟（第一次部署会慢一些）
- 看到 "Live" 状态时，部署完成

---

## 步骤 5：访问你的应用

在 Render 页面顶部会显示你的应用 URL，格式类似：

```
https://trend-analyzer-xxxx.onrender.com
```

**复制这个链接，在浏览器中打开就可以使用了！**

---

## 获取 Claude API 密钥

如果还没有 API 密钥：

1. 访问：https://console.anthropic.com/
2. 注册/登录 Anthropic 账号
3. 进入 API Keys 页面
4. 点击 "Create Key"
5. 复制密钥（sk-ant-api03-开头的）

---

## 免费版限制

Render 免费版特点：
- ✅ 完全免费
- ✅ 自动 HTTPS
- ✅ 自动部署更新
- ⚠️ 15分钟不活动会休眠（首次访问需等待 30-60 秒唤醒）
- ⚠️ 每月 750 小时免费时长（够用）

如果需要保持常在线，可升级到付费版（$7/月）。

---

## 故障排查

### 部署失败
- 检查 GitHub 仓库代码是否完整上传
- 检查 Render 日志（Logs 标签）
- 确认 Python 版本为 3.11

### 访问出错
- 检查环境变量 `CLAUDE_API_KEY` 是否正确设置
- 查看 Render Logs 中的错误信息

### 首次访问很慢
- 正常现象，免费版会休眠，首次访问需要唤醒
- 等待 30-60 秒后刷新页面

---

## 完成！

现在你有一个在线的趋势图分析工具了！

- 链接可以分享给其他人使用
- 历史记录会保存在云端
- 随时随地都能访问
