# 趋势图分析工具 - PythonAnywhere 免费部署

## 完全免费，无需信用卡，只需邮箱！

---

## 一键部署步骤（5分钟）

### 步骤 1：注册 PythonAnywhere（1分钟）

1. 打开：https://www.pythonanywhere.com/registration/register/beginner/
2. 填写：
   - Username: 选一个用户名（记住它！）
   - Email: 你的邮箱
   - Password: 设置密码
3. 点击 "Register"
4. 去邮箱点击确认链接

### 步骤 2：上传代码（2分钟）

登录后，在 Dashboard 页面：

1. 点击顶部菜单 "Files"
2. 在 "Directories" 部分，输入：`/home/你的用户名/trend-analyzer`
3. 点击 "New directory"
4. 点击这个新文件夹进入

#### 上传文件（两种方式选一种）

**方式 A - 打包上传（推荐）：**

在你的电脑上：
1. 打开文件夹：`C:\Users\pengzishan\trend-analyzer`
2. 选中所有文件，右键 → 发送到 → 压缩文件夹
3. 回到 PythonAnywhere，点击 "Upload a file"
4. 上传 `trend-analyzer.zip`
5. 点击右边的 "Open Bash console here"
6. 运行：`unzip trend-analyzer.zip`

**方式 B - 使用 Git（如果熟悉 Git）：**

1. 点击顶部菜单 "Consoles"
2. 点击 "Bash"
3. 运行：
```bash
git clone https://github.com/你的GitHub用户名/trend-analyzer.git
cd trend-analyzer
```

### 步骤 3：安装依赖（1分钟）

在 Bash 控制台运行：

```bash
cd /home/你的用户名/trend-analyzer
pip3 install --user -r requirements.txt
```

等待安装完成（1-2分钟）

### 步骤 4：配置 Web App（1分钟）

1. 点击顶部菜单 "Web"
2. 点击 "Add a new web app"
3. 点击 "Next"
4. 选择 "Flask"
5. 选择 "Python 3.10"
6. Path 改为：`/home/你的用户名/trend-analyzer/app.py`
7. 点击 "Next"

### 步骤 5：设置环境变量

在 Web 页面往下滚动，找到 "Environment variables" 部分：

1. 点击 "Go to directory"（或者手动创建）
2. Name: `CLAUDE_API_KEY`
3. Value: `你的Claude API密钥`
4. 点击 "Add"

### 步骤 6：启动应用

1. 滚动到页面顶部
2. 点击绿色的 "Reload" 按钮
3. 等待几秒钟

### 步骤 7：获取链接

你的应用链接是：

```
https://你的用户名.pythonanywhere.com
```

**复制这个链接，在浏览器打开就能用了！**

---

## 免费版限制

- ✅ 完全免费
- ✅ 永久在线
- ✅ 不需要信用卡
- ⚠️ CPU 和流量有限制（日常使用够用）
- ⚠️ 每3个月需要手动点一次"续期"按钮

---

## 更简单的方案 - Replit（推荐！）

如果觉得上面的步骤还是麻烦，用 **Replit** 更简单：

### Replit 一键部署（2分钟）

1. 打开：https://replit.com/signup
2. 用 GitHub 账号登录（或邮箱注册）
3. 点击 "Create Repl"
4. 选择 "Import from GitHub"
5. 粘贴：`https://github.com/你的GitHub用户名/trend-analyzer`
6. 点击 "Import from GitHub"
7. 等待导入完成
8. 在左侧 "Secrets" 标签（锁图标）添加：
   - Key: `CLAUDE_API_KEY`
   - Value: `你的Claude API密钥`
9. 点击顶部大大的绿色 "Run" 按钮
10. 等待启动，右侧会出现你的应用链接

**链接格式：** `https://trend-analyzer.你的用户名.repl.co`

---

## 获取 Claude API 密钥

1. 访问：https://console.anthropic.com/
2. 注册/登录
3. 进入 API Keys
4. 创建新密钥
5. 复制（sk-ant-api03-开头）

注意：Claude API 可能需要绑定支付方式，但有免费额度。

---

## 哪个最简单？

**推荐顺序：**
1. **Replit** - 最简单，2分钟搞定
2. **PythonAnywhere** - 稍微复杂，但更稳定
3. **Render** - 需要信用卡验证（不扣费）

选哪个都可以，看你的偏好！
