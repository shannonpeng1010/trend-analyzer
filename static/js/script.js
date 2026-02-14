// 全局变量
let selectedFiles = [];
let availableStyles = [];

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 初始化应用
async function initializeApp() {
    // 加载分析风格
    await loadStyles();

    // 绑定上传区域事件
    setupUploadArea();

    // 加载历史记录
    loadHistory();
}

// 设置上传区域
function setupUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    // 点击上传
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // 文件选择
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });
}

// 处理文件
function handleFiles(files) {
    const fileArray = Array.from(files);
    const imageFiles = fileArray.filter(file => file.type.startsWith('image/'));

    if (imageFiles.length === 0) {
        alert('请选择图片文件');
        return;
    }

    selectedFiles = [...selectedFiles, ...imageFiles];
    displayPreview();
}

// 显示预览
function displayPreview() {
    const previewArea = document.getElementById('previewArea');
    previewArea.innerHTML = '';

    selectedFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewItem = document.createElement('div');
            previewItem.className = 'preview-item';
            previewItem.innerHTML = `
                <img src="${e.target.result}" alt="预览图">
                <button class="preview-remove" onclick="removeFile(${index})">
                    <i class="fas fa-times"></i>
                </button>
            `;
            previewArea.appendChild(previewItem);
        };
        reader.readAsDataURL(file);
    });
}

// 移除文件
function removeFile(index) {
    selectedFiles.splice(index, 1);
    displayPreview();
}

// 加载分析风格
async function loadStyles() {
    try {
        const response = await fetch('/api/styles');
        const data = await response.json();
        availableStyles = data.styles;
        displayStyles();
    } catch (error) {
        console.error('加载分析风格失败:', error);
        alert('加载分析风格失败，请刷新页面重试');
    }
}

// 显示分析风格
function displayStyles() {
    const styleGrid = document.getElementById('styleGrid');
    styleGrid.innerHTML = '';

    availableStyles.forEach(style => {
        const styleItem = document.createElement('div');
        styleItem.className = 'style-item';
        styleItem.innerHTML = `
            <input type="checkbox" id="style_${style.key}" value="${style.key}">
            <label for="style_${style.key}" class="style-label">${style.name}</label>
        `;
        styleGrid.appendChild(styleItem);
    });
}

// 开始分析
async function startAnalyze() {
    // 验证输入
    if (selectedFiles.length === 0) {
        alert('请先上传图片');
        return;
    }

    const selectedStyles = Array.from(document.querySelectorAll('.style-item input:checked'))
        .map(input => input.value);

    if (selectedStyles.length === 0) {
        alert('请至少选择一种分析风格');
        return;
    }

    // 准备表单数据
    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('images', file);
    });
    selectedStyles.forEach(style => {
        formData.append('styles', style);
    });
    formData.append('context', document.getElementById('userContext').value);
    formData.append('name', document.getElementById('saveName').value);

    // 显示加载提示
    showLoading(true);

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert('分析失败: ' + data.error);
            return;
        }

        // 显示结果
        displayResults(data.analyses);

        // 刷新历史记录
        loadHistory();

    } catch (error) {
        console.error('分析失败:', error);
        alert('分析失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 显示结果
function displayResults(analyses) {
    const resultSection = document.getElementById('resultSection');
    const resultContent = document.getElementById('resultContent');

    resultContent.innerHTML = '';

    analyses.forEach((analysis, index) => {
        const card = document.createElement('div');
        card.className = 'analysis-card';
        card.innerHTML = `
            <div class="analysis-header">
                <div class="analysis-title">${analysis.style}</div>
                <button class="btn-copy" onclick="copyAnalysis(${index})">
                    <i class="fas fa-copy"></i> 复制
                </button>
            </div>
            <div class="analysis-content" id="analysis_${index}">
                ${marked.parse(analysis.analysis)}
            </div>
        `;
        resultContent.appendChild(card);
    });

    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// 复制分析结果
function copyAnalysis(index) {
    const content = document.getElementById(`analysis_${index}`).innerText;
    navigator.clipboard.writeText(content).then(() => {
        const btn = event.target.closest('.btn-copy');
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> 已复制';
        setTimeout(() => {
            btn.innerHTML = originalHTML;
        }, 2000);
    }).catch(err => {
        alert('复制失败: ' + err.message);
    });
}

// 重置分析
function resetAnalysis() {
    selectedFiles = [];
    document.getElementById('previewArea').innerHTML = '';
    document.getElementById('userContext').value = '';
    document.getElementById('saveName').value = '';
    document.querySelectorAll('.style-item input').forEach(input => {
        input.checked = false;
    });
    document.getElementById('resultSection').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 显示/隐藏加载提示
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = show ? 'flex' : 'none';
}

// 切换历史记录侧边栏
function toggleHistory() {
    const sidebar = document.getElementById('historySidebar');
    sidebar.classList.toggle('open');
}

// 加载历史记录
async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        displayHistory(data.history);
    } catch (error) {
        console.error('加载历史记录失败:', error);
    }
}

// 显示历史记录
function displayHistory(history) {
    const historyList = document.getElementById('historyList');

    if (history.length === 0) {
        historyList.innerHTML = '<p style="text-align: center; color: #7f8c8d; padding: 20px;">暂无历史记录</p>';
        return;
    }

    historyList.innerHTML = '';

    history.forEach(record => {
        const item = document.createElement('div');
        item.className = 'history-item';

        const date = new Date(record.timestamp);
        const timeStr = `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2,'0')}-${date.getDate().toString().padStart(2,'0')} ${date.getHours().toString().padStart(2,'0')}:${date.getMinutes().toString().padStart(2,'0')}`;

        item.innerHTML = `
            <div class="history-item-header">
                <div class="history-item-name">${record.name}</div>
                <div class="history-item-actions">
                    <button onclick="renameHistory('${record.id}')" title="重命名">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-delete" onclick="deleteHistory('${record.id}')" title="删除">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="history-item-time">${timeStr}</div>
            <div class="history-item-context">${record.user_context || '无补充说明'}</div>
        `;

        item.addEventListener('click', (e) => {
            if (!e.target.closest('button')) {
                viewHistoryRecord(record);
            }
        });

        historyList.appendChild(item);
    });
}

// 查看历史记录
function viewHistoryRecord(record) {
    displayResults(record.analyses);
    toggleHistory();
}

// 重命名历史记录
async function renameHistory(recordId) {
    const newName = prompt('请输入新名称:');
    if (!newName) return;

    try {
        const response = await fetch(`/api/history/${recordId}/name`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: newName })
        });

        if (response.ok) {
            loadHistory();
        } else {
            alert('重命名失败');
        }
    } catch (error) {
        console.error('重命名失败:', error);
        alert('重命名失败: ' + error.message);
    }
}

// 删除历史记录
async function deleteHistory(recordId) {
    if (!confirm('确定要删除这条记录吗？')) return;

    try {
        const response = await fetch(`/api/history/${recordId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadHistory();
        } else {
            alert('删除失败');
        }
    } catch (error) {
        console.error('删除失败:', error);
        alert('删除失败: ' + error.message);
    }
}

// 简单的 Markdown 解析器（如果不想引入外部库）
const marked = {
    parse: function(markdown) {
        if (!markdown) return '';

        let html = markdown;

        // 标题
        html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

        // 粗体和斜体
        html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

        // 代码块
        html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        html = html.replace(/`(.+?)`/g, '<code>$1</code>');

        // 列表
        html = html.replace(/^\* (.+)$/gim, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        html = html.replace(/^\d+\. (.+)$/gim, '<li>$1</li>');

        // 链接
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

        // 换行
        html = html.replace(/\n\n/g, '</p><p>');
        html = html.replace(/\n/g, '<br>');
        html = '<p>' + html + '</p>';

        return html;
    }
};
