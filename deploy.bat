@echo off
echo ========================================
echo   自动上传到 GitHub
echo ========================================
echo.

REM 检查是否已登录 GitHub
git config user.name >nul 2>&1
if errorlevel 1 (
    echo 首次使用，请设置 GitHub 信息：
    echo.
    set /p username="输入你的 GitHub 用户名: "
    set /p email="输入你的 GitHub 邮箱: "

    git config --global user.name "%username%"
    git config --global user.email "%email%"
)

echo.
echo 请输入你的 GitHub 用户名（如果刚才输入过就输入同一个）：
set /p github_user="GitHub 用户名: "

echo.
echo [1/4] 检查 GitHub 仓库是否存在...
echo.
echo 请手动完成以下步骤：
echo 1. 打开浏览器访问：https://github.com/new
echo 2. Repository name 填写：trend-analyzer
echo 3. 选择 Public（公开）
echo 4. 不要勾选任何选项
echo 5. 点击 Create repository
echo.
pause

echo.
echo [2/4] 关联远程仓库...
cd C:\Users\pengzishan\trend-analyzer
git remote remove origin 2>nul
git remote add origin https://github.com/%github_user%/trend-analyzer.git

echo.
echo [3/4] 推送代码...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo 推送失败！可能需要 GitHub 访问令牌。
    echo.
    echo 请访问：https://github.com/settings/tokens/new
    echo 1. Note 填写：trend-analyzer
    echo 2. Expiration 选择：90 days
    echo 3. 勾选 repo（完整权限）
    echo 4. 点击页面底部 Generate token
    echo 5. 复制生成的 token（ghp_开头）
    echo.
    set /p token="粘贴你的 GitHub Token: "

    git remote set-url origin https://%token%@github.com/%github_user%/trend-analyzer.git
    git push -u origin main
)

echo.
echo [4/4] 完成！
echo.
echo ========================================
echo 代码已上传到 GitHub！
echo 仓库地址：https://github.com/%github_user%/trend-analyzer
echo ========================================
echo.
echo 下一步：部署到 Replit
echo 1. 打开：https://replit.com/github/%github_user%/trend-analyzer
echo 2. 直接会打开导入页面，点击 Import
echo 3. 等待导入完成
echo 4. 点击左侧 Secrets（锁图标）
echo 5. 添加：CLAUDE_API_KEY = 你的API密钥
echo 6. 点击顶部绿色 Run 按钮
echo 7. 完成！链接会显示在右侧
echo.
pause
