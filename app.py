from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import anthropic
import os
import json
import base64
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

# 配置
UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# 确保目录存在
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(DATA_FOLDER).mkdir(exist_ok=True)

# Claude API 配置
CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY', '')

# 分析风格配置
ANALYSIS_STYLES = {
    'formal_tech': {
        'name': '正式-技术视角',
        'prompt': '请以正式专业的语气，从技术角度分析这些趋势图。重点关注数据指标、技术参数、性能表现等。'
    },
    'formal_business': {
        'name': '正式-业务视角',
        'prompt': '请以正式专业的语气，从业务角度分析这些趋势图。重点关注业务影响、增长趋势、关键指标等。'
    },
    'formal_management': {
        'name': '正式-管理视角',
        'prompt': '请以正式专业的语气，从管理角度分析这些趋势图。重点关注整体表现、风险评估、决策建议等。'
    },
    'concise_tech': {
        'name': '简洁-技术视角',
        'prompt': '请以简洁明了的方式，从技术角度总结这些趋势图的关键信息。只突出重点数据和技术指标。'
    },
    'concise_business': {
        'name': '简洁-业务视角',
        'prompt': '请以简洁明了的方式，从业务角度总结这些趋势图的关键信息。只突出业务核心数据。'
    },
    'concise_management': {
        'name': '简洁-管理视角',
        'prompt': '请以简洁明了的方式，从管理角度总结这些趋势图的关键信息。只突出管理决策要点。'
    },
    'detailed_tech': {
        'name': '详细-技术视角',
        'prompt': '请以详尽的方式，从技术角度深入分析这些趋势图。包括数据变化原因、技术细节、潜在问题等。'
    },
    'detailed_business': {
        'name': '详细-业务视角',
        'prompt': '请以详尽的方式，从业务角度深入分析这些趋势图。包括业务影响分析、市场洞察、增长机会等。'
    },
    'detailed_management': {
        'name': '详细-管理视角',
        'prompt': '请以详尽的方式，从管理角度深入分析这些趋势图。包括综合评估、风险机会、具体行动建议等。'
    },
    'daily_report': {
        'name': '日报格式',
        'prompt': '请以日报格式分析这些趋势图。包括：今日数据概况、关键指标、异常情况、明日关注点。使用简洁的格式。'
    },
    'weekly_report': {
        'name': '周报格式',
        'prompt': '请以周报格式分析这些趋势图。包括：本周概况、主要趋势、重点成果、下周计划。'
    },
    'monthly_report': {
        'name': '月报格式',
        'prompt': '请以月报格式分析这些趋势图。包括：月度总结、趋势分析、亮点与问题、下月重点。'
    }
}


def encode_image(image_path):
    """将图片编码为base64"""
    with open(image_path, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8')


def get_image_media_type(file_path):
    """根据文件扩展名获取媒体类型"""
    ext = file_path.lower().split('.')[-1]
    media_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    return media_types.get(ext, 'image/jpeg')


def analyze_with_claude(image_paths, style_key, user_context=''):
    """使用 Claude API 分析图片"""
    if not CLAUDE_API_KEY:
        return {'error': 'Claude API Key 未配置，请设置环境变量 CLAUDE_API_KEY'}

    try:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

        # 构建消息内容
        content = []

        # 添加图片
        for img_path in image_paths:
            image_data = encode_image(img_path)
            media_type = get_image_media_type(img_path)
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_data,
                },
            })

        # 添加分析提示词
        style_config = ANALYSIS_STYLES.get(style_key, ANALYSIS_STYLES['formal_tech'])
        prompt = style_config['prompt']

        if user_context:
            prompt += f"\n\n用户补充说明：{user_context}"

        prompt += "\n\n请用markdown格式输出分析结果。"

        content.append({
            "type": "text",
            "text": prompt
        })

        # 调用 Claude API
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

        return {
            'success': True,
            'analysis': message.content[0].text,
            'style': style_config['name']
        }

    except Exception as e:
        return {'error': str(e)}


def save_history(images, analyses, user_context, name=''):
    """保存分析历史"""
    history_file = os.path.join(DATA_FOLDER, 'history.json')

    # 读取现有历史
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

    # 添加新记录
    record = {
        'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'timestamp': datetime.now().isoformat(),
        'name': name or f"分析_{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        'images': images,
        'user_context': user_context,
        'analyses': analyses
    }

    history.insert(0, record)  # 最新的在前面

    # 保存历史
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    return record['id']


def get_history():
    """获取历史记录"""
    history_file = os.path.join(DATA_FOLDER, 'history.json')
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def delete_history(record_id):
    """删除历史记录"""
    history_file = os.path.join(DATA_FOLDER, 'history.json')
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)

        history = [h for h in history if h['id'] != record_id]

        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    return False


def update_history_name(record_id, new_name):
    """更新历史记录名称"""
    history_file = os.path.join(DATA_FOLDER, 'history.json')
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)

        for h in history:
            if h['id'] == record_id:
                h['name'] = new_name
                break

        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    return False


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/styles', methods=['GET'])
def get_styles():
    """获取所有分析风格"""
    styles = [{'key': k, 'name': v['name']} for k, v in ANALYSIS_STYLES.items()]
    return jsonify({'styles': styles})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """分析图片接口"""
    if 'images' not in request.files:
        return jsonify({'error': '没有上传图片'}), 400

    files = request.files.getlist('images')
    style_keys = request.form.getlist('styles')
    user_context = request.form.get('context', '')
    save_name = request.form.get('name', '')

    if not files or files[0].filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    if not style_keys:
        return jsonify({'error': '没有选择分析风格'}), 400

    # 保存上传的图片
    saved_images = []
    for file in files:
        if file:
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            saved_images.append(filepath)

    # 对每种风格进行分析
    analyses = []
    for style_key in style_keys:
        result = analyze_with_claude(saved_images, style_key, user_context)
        if 'error' in result:
            return jsonify(result), 500
        analyses.append(result)

    # 保存历史
    history_id = save_history(saved_images, analyses, user_context, save_name)

    return jsonify({
        'success': True,
        'analyses': analyses,
        'history_id': history_id
    })


@app.route('/api/history', methods=['GET'])
def history():
    """获取历史记录"""
    return jsonify({'history': get_history()})


@app.route('/api/history/<record_id>', methods=['DELETE'])
def delete_history_record(record_id):
    """删除历史记录"""
    if delete_history(record_id):
        return jsonify({'success': True})
    return jsonify({'error': '删除失败'}), 404


@app.route('/api/history/<record_id>/name', methods=['PUT'])
def update_history_record_name(record_id):
    """更新历史记录名称"""
    data = request.get_json()
    new_name = data.get('name', '')
    if update_history_name(record_id, new_name):
        return jsonify({'success': True})
    return jsonify({'error': '更新失败'}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
