@echo off
echo ========================================
echo   趋势图分析工具 - Docker 启动脚本
echo ========================================
echo.

REM 检查 .env 文件是否存在
if not exist .env (
    echo [错误] 未找到 .env 文件
    echo.
    echo 请先创建 .env 文件并配置 Claude API 密钥：
    echo 1. 复制 .env.example 为 .env
    echo 2. 编辑 .env 填入你的 API 密钥
    echo.
    pause
    exit /b 1
)

REM 检查 Docker 是否运行
docker info >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker 未运行
    echo.
    echo 请先启动 Docker Desktop
    echo.
    pause
    exit /b 1
)

echo [1/3] 停止旧容器...
docker-compose down

echo.
echo [2/3] 构建并启动容器...
docker-compose up -d --build

if errorlevel 1 (
    echo.
    echo [错误] 启动失败
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] 启动成功！
echo.
echo ========================================
echo   应用已启动！
echo   访问地址：http://localhost:5000
echo ========================================
echo.
echo 查看日志：docker-compose logs -f
echo 停止应用：docker-compose down
echo.
pause
