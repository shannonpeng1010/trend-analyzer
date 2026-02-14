# 趋势图分析工具

一个基于 Claude AI 的智能趋势图分析工具，支持上传图片自动分析趋势，提供多种分析风格，协助完成日报、周报等工作汇报。

## 功能特点

- 📊 **智能分析**：使用 Claude Vision API 自动识别和分析趋势图
- 🎨 **多种风格**：支持多种分析风格组合
  - 语气风格：正式、简洁、详细
  - 视角维度：技术、业务、管理
  - 场景格式：日报、周报、月报
- 📸 **灵活上传**：支持单张或多张图片同时上传分析
- 💬 **可选说明**：可添加文字补充背景信息
- 📝 **结果展示**：网页显示分析结果，一键复制
- 📚 **历史管理**：保存分析历史，支持命名、分类、删除
- 🎯 **极简设计**：专业数据分析风格界面

## 技术栈

- **后端**：Python Flask
- **AI服务**：Claude API (Anthropic)
- **前端**：HTML + CSS + JavaScript
- **部署**：支持本地运行和云服务器部署

## 快速开始

### 1. 安装依赖

```bash
cd trend-analyzer
pip install -r requirements.txt
```

### 2. 配置 API 密钥

在项目根目录创建 `.env` 文件，添加你的 Claude API 密钥：

```env
CLAUDE_API_KEY=your_api_key_here
```

或者直接设置环境变量：

**Windows:**
```cmd
set CLAUDE_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export CLAUDE_API_KEY=your_api_key_here
```

### 3. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 使用说明

### 基本使用流程

1. **上传图片**
   - 点击或拖拽图片到上传区域
   - 支持 JPG、PNG、GIF、WebP 格式
   - 可同时上传多张图片

2. **添加说明**（可选）
   - 在"补充说明"区域添加背景信息
   - 帮助 AI 更准确地理解图片内容

3. **选择分析风格**
   - 至少选择一种分析风格
   - 可多选，同时生成多种风格的分析

4. **命名保存**（可选）
   - 为本次分析起个名字
   - 方便后续在历史记录中查找

5. **开始分析**
   - 点击"开始分析"按钮
   - 等待 AI 分析完成

6. **查看结果**
   - 查看不同风格的分析结果
   - 点击"复制"按钮复制内容
   - 直接粘贴到日报/周报文档

### 历史记录管理

- 点击右上角"历史记录"按钮打开侧边栏
- 点击任意记录查看详情
- 使用编辑按钮重命名记录
- 使用删除按钮删除不需要的记录

## 分析风格说明

### 语气风格

- **正式风格**：专业正式的表达，适合正式汇报
- **简洁风格**：简明扼要，突出重点，适合快速浏览
- **详细风格**：深入分析，包含详细解读，适合深度报告

### 视角维度

- **技术视角**：关注技术指标、性能参数、技术细节
- **业务视角**：关注业务影响、增长趋势、关键指标
- **管理视角**：关注整体表现、风险评估、决策建议

### 场景格式

- **日报格式**：今日概况、关键指标、异常情况、明日关注
- **周报格式**：本周概况、主要趋势、重点成果、下周计划
- **月报格式**：月度总结、趋势分析、亮点与问题、下月重点

## 项目结构

```
trend-analyzer/
├── app.py                 # Flask 应用主文件
├── requirements.txt       # Python 依赖
├── .env                   # 环境变量配置（需自行创建）
├── static/
│   ├── css/
│   │   └── style.css     # 样式文件
│   └── js/
│       └── script.js     # 前端逻辑
├── templates/
│   └── index.html        # 主页模板
├── uploads/              # 上传的图片（自动创建）
└── data/                 # 历史记录数据（自动创建）
    └── history.json      # 历史记录文件
```

## 云服务器部署

### 使用 Gunicorn（推荐）

```bash
# 安装 gunicorn
pip install gunicorn

# 运行
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 使用 Supervisor 守护进程

创建 `/etc/supervisor/conf.d/trend-analyzer.conf`：

```ini
[program:trend-analyzer]
directory=/path/to/trend-analyzer
command=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
user=your-user
autostart=true
autorestart=true
stderr_logfile=/var/log/trend-analyzer.err.log
stdout_logfile=/var/log/trend-analyzer.out.log
```

## 常见问题

### 1. API 调用失败

- 检查 `.env` 文件中的 API 密钥是否正确
- 确认网络连接正常
- 检查 API 额度是否充足

### 2. 图片上传失败

- 检查图片格式是否支持
- 确认图片大小不超过 16MB
- 检查 `uploads` 目录权限

### 3. 历史记录无法保存

- 检查 `data` 目录是否存在
- 确认目录有写入权限

## API 接口说明

### GET /api/styles
获取所有可用的分析风格

### POST /api/analyze
提交图片进行分析
- 参数：images (文件), styles (列表), context (字符串), name (字符串)

### GET /api/history
获取历史记录列表

### DELETE /api/history/<record_id>
删除指定历史记录

### PUT /api/history/<record_id>/name
更新历史记录名称

## 许可证

MIT License

## 获取 Claude API 密钥

访问 [Anthropic Console](https://console.anthropic.com/) 注册账号并获取 API 密钥。

## 支持

如有问题或建议，欢迎提 Issue。
