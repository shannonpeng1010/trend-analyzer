# 网页修改指南

## 📁 项目文件结构说明

```
trend-analyzer/
├── app.py                    # 后端逻辑（Python）
├── templates/
│   └── index.html           # 页面结构和布局
├── static/
│   ├── css/
│   │   └── style.css        # 页面样式（颜色、字体、布局）
│   └── js/
│       └── script.js        # 前端交互逻辑
```

---

## 🎨 常见修改场景

### 1. 修改页面布局和内容

**文件：** `templates/index.html`

#### 修改标题
找到第 13 行：
```html
<h1><i class="fas fa-chart-line"></i> 趋势图分析工具</h1>
```
改成你想要的标题：
```html
<h1><i class="fas fa-chart-line"></i> 我的数据分析平台</h1>
```

#### 添加说明文字
在第 33 行 `<p class="upload-hint">` 后面添加：
```html
<p class="upload-hint">支持 JPG、PNG、GIF、WebP 格式</p>
<p class="upload-note" style="color: #e74c3c; margin-top: 10px;">
    💡 提示：这是演示版本，分析结果为预设内容
</p>
```

#### 添加页脚信息
在 `</main>` 标签前（约第 79 行）添加：
```html
<footer style="text-align: center; padding: 20px; color: #7f8c8d;">
    <p>© 2025 我的公司 | 联系邮箱: example@email.com</p>
</footer>
```

#### 修改上传区域提示文字
找到第 31-33 行：
```html
<p class="upload-text">点击或拖拽图片到此处上传</p>
<p class="upload-hint">支持 JPG、PNG、GIF、WebP 格式</p>
```
改成：
```html
<p class="upload-text">上传您的趋势图</p>
<p class="upload-hint">支持多种图片格式，单次最多上传10张</p>
```

---

### 2. 修改页面样式（颜色、字体、间距）

**文件：** `static/css/style.css`

#### 修改主题颜色
找到第 1-10 行的颜色变量：
```css
:root {
    --primary: #2c3e50;      /* 主色 - 深蓝灰 */
    --accent: #3498db;       /* 强调色 - 蓝色 */
    --success: #27ae60;      /* 成功色 - 绿色 */
}
```
改成你喜欢的颜色：
```css
:root {
    --primary: #1a1a2e;      /* 深色主题 */
    --accent: #0f3460;       /* 深蓝色 */
    --success: #16213e;      /* 深绿色 */
}
```

#### 修改标题字体大小
找到第 47 行：
```css
.header h1 {
    font-size: 24px;
}
```
改成：
```css
.header h1 {
    font-size: 28px;
    font-weight: bold;
}
```

#### 修改页面背景色
找到第 22 行：
```css
body {
    background: var(--lighter);  /* #f8f9fa */
}
```
改成：
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* 或纯色背景：background: #ffffff; */
}
```

#### 调整卡片圆角和阴影
找到第 126 行：
```css
.upload-section {
    border-radius: 8px;
    box-shadow: 0 2px 8px var(--shadow);
}
```
改成：
```css
.upload-section {
    border-radius: 16px;           /* 更圆润 */
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);  /* 更明显的阴影 */
}
```

---

### 3. 修改分析风格（添加/删除/修改）

**文件：** `app.py`

找到第 27-76 行的 `ANALYSIS_STYLES` 字典：

#### 添加新的分析风格
```python
ANALYSIS_STYLES = {
    # ... 现有风格 ...

    # 添加自定义风格
    'custom_style': {
        'name': '个性化报告',
        'prompt': '用轻松幽默的语气分析趋势图，适合团队内部分享。'
    }
}
```

#### 删除不需要的风格
直接删除或注释掉对应的项：
```python
# 'monthly_report': {
#     'name': '月报格式',
#     'prompt': '...'
# },
```

---

### 4. 修改演示分析结果

**文件：** `app.py`

找到第 104-331 行的 `demo_analyses` 字典：

#### 修改某个风格的分析结果
```python
demo_analyses = {
    'formal_tech': """# 我的自定义技术分析

## 核心指标
- 性能提升：20%
- 响应时间：150ms
- 用户满意度：95%

## 详细说明
这里写你想要的分析内容...
""",
    # ... 其他风格 ...
}
```

#### 添加公司信息到所有分析结果
在第 333-350 行，修改返回内容：
```python
# 在分析文本末尾添加公司信息
analysis_text += "\n\n---\n\n"
analysis_text += "**📊 报告生成**：我的公司数据分析团队\n"
analysis_text += "**📧 联系方式**：data@company.com\n"
analysis_text += "**🌐 官网**：www.company.com"
```

---

### 5. 修改上传限制

**文件：** `app.py`

找到第 15 行：
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```
改成：
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

---

## 🔄 修改后如何更新部署

### 方法 1：通过 Replit 直接修改（最简单）

1. 在 Replit 页面左侧直接编辑对应文件
2. 按 Ctrl+S 保存
3. 点击绿色 "Run" 按钮重启应用
4. 完成！

### 方法 2：本地修改后推送更新

1. 在本地编辑文件（用记事本或 VS Code）
2. 打开命令行，运行：
```bash
cd C:\Users\pengzishan\trend-analyzer
git add .
git commit -m "更新页面布局和样式"
git push
```
3. 在 Replit 页面点击：Shell → 运行 `git pull`
4. 点击 "Run" 按钮重启

### 方法 3：使用 GitHub 网页编辑

1. 访问：https://github.com/shannonpeng1010/trend-analyzer
2. 点击要修改的文件
3. 点击右上角铅笔图标 ✏️ 编辑
4. 修改完成后点击 "Commit changes"
5. 在 Replit 运行 `git pull` 更新
6. 重启应用

---

## 📝 推荐修改流程

1. **先在本地测试**：修改文件后在本地运行看效果
2. **确认无误后提交**：git commit 提交更改
3. **推送到 GitHub**：git push 上传
4. **更新线上版本**：在 Replit 拉取最新代码

---

## 🛠️ 推荐编辑工具

- **简单编辑**：Windows 记事本、Notepad++
- **专业开发**：Visual Studio Code（推荐）
  - 下载：https://code.visualstudio.com/
  - 支持语法高亮、自动补全

---

## 💡 修改提示

### 修改 HTML 时
- 保持标签配对（每个 `<div>` 都要有 `</div>`）
- 注意缩进，保持代码整洁
- 修改文字直接改就行，不要动标签

### 修改 CSS 时
- 一次改一个属性，测试效果
- 颜色可以用在线取色器：https://htmlcolorcodes.com/
- 不确定的话复制一份原样式做备份

### 修改 Python 时
- 注意缩进（Python 用空格缩进）
- 修改字符串内容最安全
- 不要删除关键的函数和变量

---

## ❓ 常见问题

**Q: 改错了怎么办？**
A: 如果用了 git，运行 `git checkout app.py` 恢复单个文件

**Q: Replit 上的改动会覆盖吗？**
A: 如果同时在两边改，以最后 git push 的为准

**Q: 怎么预览效果？**
A: 在 Replit 直接改完点 Run，或本地运行 `python app.py` 后访问 localhost:5000

---

需要修改具体的某个功能？告诉我，我可以直接帮你改好！
