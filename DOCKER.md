# Docker 运行指南

## 前提条件

确保已安装 Docker Desktop for Windows：
- 下载地址：https://www.docker.com/products/docker-desktop

## 快速启动

### 方法一：使用 docker-compose（推荐）

1. 配置 API 密钥

创建 `.env` 文件：
```bash
copy .env.example .env
```

编辑 `.env` 文件，填入你的 Claude API 密钥：
```
CLAUDE_API_KEY=你的API密钥
```

2. 启动应用

```bash
docker-compose up -d
```

3. 访问应用

打开浏览器访问：http://localhost:5000

4. 停止应用

```bash
docker-compose down
```

### 方法二：使用 docker 命令

1. 构建镜像

```bash
docker build -t trend-analyzer .
```

2. 运行容器

```bash
docker run -d ^
  --name trend-analyzer ^
  -p 5000:5000 ^
  -e CLAUDE_API_KEY=你的API密钥 ^
  -v "%cd%\uploads:/app/uploads" ^
  -v "%cd%\data:/app/data" ^
  trend-analyzer
```

3. 停止容器

```bash
docker stop trend-analyzer
docker rm trend-analyzer
```

## 常用命令

### 查看日志
```bash
docker-compose logs -f
```

### 重启应用
```bash
docker-compose restart
```

### 重新构建
```bash
docker-compose up -d --build
```

### 进入容器
```bash
docker exec -it trend-analyzer /bin/bash
```

## 数据持久化

- `uploads/` 目录：存储上传的图片
- `data/` 目录：存储历史记录

这两个目录会自动挂载到主机，即使容器删除数据也不会丢失。

## 更新应用

```bash
docker-compose down
docker-compose up -d --build
```

## 故障排查

### 端口被占用
修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "5001:5000"  # 改为其他端口
```

### 权限问题
Windows 上确保 Docker Desktop 有访问共享文件夹的权限。

### API 调用失败
检查 `.env` 文件中的 API 密钥是否正确。
