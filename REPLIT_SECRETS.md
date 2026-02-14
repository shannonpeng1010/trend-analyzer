# Replit 添加密钥详细教程

## 方法 1：使用 Secrets（推荐）

### 找到 Secrets 入口（3种可能的位置）

**位置 A - 左侧工具栏：**
1. 看左边的侧边栏（文件列表上方）
2. 找到一个 🔒 锁图标，或者写着 "Secrets" 的按钮
3. 点击它

**位置 B - Tools 菜单：**
1. 点击左下角或顶部的 "Tools" 菜单
2. 在下拉菜单中找到 "Secrets"
3. 点击进入

**位置 C - 直接在 .replit 配置：**
如果实在找不到，可以用备用方案（见下面）

### 添加密钥步骤

找到 Secrets 页面后：

1. 看到一个输入框，上面写着 "key" 或 "Key"
2. 在这个框里输入：`CLAUDE_API_KEY`（注意大小写，全部大写）
3. 下面有个 "value" 或 "Value" 框
4. 在这个框里粘贴你的 Claude API 密钥（sk-ant-api03 开头的那串）
5. 点击 "Add new secret" 或 "Save" 按钮

---

## 方法 2：使用 .env 文件（备用方案）

如果找不到 Secrets，用这个方法：

1. 在 Replit 左侧文件列表中
2. 找到并点击 `.env` 文件（如果没有就创建一个）
3. 在文件中输入：
   ```
   CLAUDE_API_KEY=你的密钥粘贴在这里
   ```
4. 按 Ctrl+S 保存

---

## 方法 3：直接修改 app.py（最简单，但不安全）

如果上面两个都不行：

1. 打开 `app.py` 文件
2. 找到第 19 行：`CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY', '')`
3. 改成：`CLAUDE_API_KEY = 'sk-ant-api03-你的密钥粘贴在这里'`
4. 保存

⚠️ 注意：这个方法会把密钥暴露在代码中，不太安全，但可以先用来测试。

---

## 获取 Claude API 密钥

如果你还没有密钥：

1. 打开：https://console.anthropic.com/
2. 注册或登录
3. 点击左侧 "API Keys"
4. 点击 "Create Key"
5. 给密钥起个名字（比如：trend-analyzer）
6. 点击 "Create Key"
7. 复制密钥（sk-ant-api03 开头）

注意：密钥只显示一次，要保存好！

---

## 测试是否成功

添加密钥后：

1. 点击 Replit 顶部的绿色 "Run" 按钮
2. 等待 30-60 秒
3. 如果右侧出现网页，说明成功了！
4. 如果报错，检查密钥是否正确粘贴

---

需要帮助？告诉我你看到什么界面，我继续指导你！
