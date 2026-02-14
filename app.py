from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
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
    """使用 Claude API 分析图片 - 演示版本"""
    # 演示版本：返回预设的分析结果
    style_config = ANALYSIS_STYLES.get(style_key, ANALYSIS_STYLES['formal_tech'])

    # 根据不同风格返回不同的演示分析
    demo_analyses = {
        'formal_tech': """# 技术指标分析报告

## 核心数据概览
根据趋势图数据显示，关键技术指标呈现以下特征：

### 1. 性能指标趋势
- **响应时间**：平均响应时间从上周的 245ms 降低至 198ms，优化幅度达 19.2%
- **并发处理能力**：峰值 QPS 稳定在 8500-9200 区间，较基准值提升 15%
- **系统稳定性**：可用性维持在 99.95%，符合 SLA 要求

### 2. 资源使用情况
- CPU 使用率波动范围：45%-72%，平均值 58%
- 内存占用趋于稳定，峰值 4.2GB，较上期下降 8%
- 网络带宽使用平稳，未出现明显瓶颈

### 3. 异常监测
- 监测到 3 次轻微性能抖动，已定位到数据库查询优化问题
- 错误率保持在 0.02% 以下，处于正常范围

## 技术建议
1. 持续优化数据库查询性能
2. 关注 CPU 峰值时段的负载分布
3. 建议增加缓存预热机制""",

        'formal_business': """# 业务指标分析报告

## 数据概况
本期业务数据呈现积极增长态势，核心指标表现优秀：

### 1. 用户增长情况
- **新增用户**：较上期增长 23.5%，DAU 达到 45,800
- **用户留存率**：次日留存 68%，7日留存 42%，均高于行业平均水平
- **用户活跃度**：人均使用时长 28 分钟，环比提升 12%

### 2. 转化漏斗分析
- 访问→注册转化率：12.3%（↑ 2.1%）
- 注册→付费转化率：8.7%（↑ 0.9%）
- 整体转化效率提升显著

### 3. 营收表现
- GMV 同比增长 34%，环比增长 18%
- 客单价稳定在 ¥128，略有上升趋势
- 付费用户数突破 5,000 人

## 业务洞察
1. 营销活动效果显著，建议持续投入
2. 产品粘性增强，用户价值不断提升
3. 需关注高价值用户的精细化运营""",

        'concise_tech': """# 技术指标速览

**性能提升**
- 响应时间 ↓ 19.2%（245ms → 198ms）
- QPS 峰值稳定在 8500-9200

**资源状态**
- CPU 平均 58%，峰值 72%
- 内存占用 ↓ 8%，稳定在 4.2GB

**问题**
- 3 次性能抖动，已定位数据库优化点
- 错误率 0.02%，正常范围

**建议**
优化数据库查询 | 关注 CPU 峰值 | 增加缓存预热""",

        'detailed_management': """# 综合运营分析报告

## 一、整体表现评估

### 战略目标达成情况
本期各项核心指标均达到预期目标，整体运营健康度良好：
- 用户规模目标达成率：112%（目标 40K，实际 45.8K）
- 营收目标达成率：108%（目标 520W，实际 562W）
- 技术稳定性目标达成率：100%（SLA 99.95%）

### 关键成果亮点
1. **用户增长引擎启动成功**：新用户获取成本下降 15%，获客效率显著提升
2. **产品体验优化见效**：用户满意度从 4.2 提升至 4.6，NPS 值达到 52
3. **技术架构升级完成**：系统性能提升 20%，为业务扩展奠定基础

## 二、风险与机会

### 主要风险
- **竞争加剧**：同类产品陆续上线，需加强差异化竞争
- **成本控制**：随着规模扩大，单位成本需持续优化
- **团队扩张**：人才缺口逐渐显现，需提前布局

### 机会窗口
- 市场需求持续旺盛，用户痛点清晰
- 技术优势明显，可拓展高端市场
- 品牌认知度快速提升，口碑传播效应显现

## 三、下阶段重点

### 战略优先级
1. **用户规模翻番**：Q2 目标 DAU 突破 10 万
2. **营收结构优化**：提升高价值用户占比至 25%
3. **组织能力建设**：完成核心团队扩充 30%

### 具体行动计划
- 启动大规模市场推广计划，预算增加 40%
- 推出差异化功能，建立竞争壁垒
- 优化运营流程，提升人效 20%

### 资源需求
- 预算追加：营销 200W，技术 100W
- 人员增编：产品 3 人，技术 5 人，运营 4 人
- 外部合作：寻求战略合作伙伴 2-3 家""",

        'daily_report': """# 今日数据日报

**📅 日期**：2025-02-14

## 今日概况
- 访问量：12,340（↑ 8.2%）
- 新增用户：856（↑ 12%）
- 活跃用户：8,945
- 订单数：342（↑ 5.3%）

## 关键指标
✅ 转化率：8.7%（持平）
✅ 客单价：¥135（↑ 5.6%）
⚠️ 页面加载时间：2.3s（略慢）

## 异常情况
1. 14:20-14:35 服务器响应变慢，已处理
2. 支付成功率下降 2%，正在排查

## 明日关注
- 监控支付系统稳定性
- 优化页面加载速度
- 跟进新功能上线效果""",

        'weekly_report': """# 本周工作周报

**📅 周期**：2025-02-10 至 2025-02-16

## 本周概况
本周各项指标平稳增长，重点项目按计划推进：

### 数据表现
- 周活跃用户：45,800（↑ 18%）
- 周新增用户：5,240（↑ 23%）
- 周订单量：2,156（↑ 15%）
- 周营收：¥28.6W（↑ 19%）

### 主要成果
1. ✅ 新版本功能上线，用户反馈积极
2. ✅ 营销活动效果超预期，ROI 达 3.2
3. ✅ 技术性能优化完成，响应速度提升 20%

### 遇到的问题
1. 客服压力增大，响应时间延长
2. 部分用户反馈新功能学习成本高
3. 服务器负载接近预警值

## 下周计划
1. 扩充客服团队 2 人
2. 制作功能使用教程
3. 评估服务器扩容方案
4. 启动新一轮推广活动

## 需要支持
- 技术：申请服务器扩容预算
- 人力：加急招聘客服人员""",

        'monthly_report': """# 2月份月度总结报告

**📅 报告周期**：2025-02-01 至 2025-02-28

## 月度总结

### 核心数据
- 月活用户：156,000（同比 ↑ 45%，环比 ↑ 12%）
- 新增用户：18,500（同比 ↑ 52%）
- 月订单量：9,840（同比 ↑ 38%）
- 月营收：¥124W（同比 ↑ 42%，环比 ↑ 8%）

### 重大里程碑
1. 🎉 用户规模突破 15 万大关
2. 🎉 月营收首次突破 100 万
3. 🎉 产品功能迭代 5 次，用户满意度达 4.6/5.0
4. 🎉 技术架构升级完成，支撑 10 倍规模扩展

## 趋势分析

### 增长引擎
- **渠道效率**：信息流广告 ROI 3.8，短视频 ROI 4.2
- **用户裂变**：老用户推荐占新增 28%，裂变系数 1.6
- **产品留存**：30日留存率达 35%，超行业均值 15%

### 亮点与问题

**🌟 本月亮点**
- 春节营销活动大获成功，带来 5000+ 精准用户
- 产品口碑快速提升，应用市场评分 4.7
- 团队协作效率提升，项目交付准时率 95%

**⚠️ 存在问题**
- 高价值用户占比仅 18%，低于目标 25%
- 部分地区服务器延迟较高，影响用户体验
- 客户成功团队人手不足，服务响应时间偏长

## 3月重点

### 战略目标
1. 用户规模突破 20 万
2. 月营收达到 150 万
3. 高价值用户占比提升至 22%

### 关键举措
- **产品**：上线 VIP 会员体系，提升付费转化
- **技术**：部署 CDN，优化全国访问速度
- **运营**：启动品牌升级计划，加大市场投入
- **团队**：招聘 8 人，重点补充技术和客服

### 预算需求
- 营销预算：300 万（↑ 50%）
- 技术投入：120 万（服务器 + CDN）
- 人力成本：80 万（新增人员）

---

**报告人**：运营团队
**审核人**：管理层"""
    }

    # 返回对应风格的分析，如果没有则返回通用版本
    analysis_text = demo_analyses.get(style_key, demo_analyses['formal_tech'])

    # 如果用户提供了补充说明，加入到分析中
    if user_context:
        analysis_text = f"""## 用户补充说明
{user_context}

---

{analysis_text}

---

*💡 这是演示版本，显示的是预设的分析结果。实际使用时，AI 会根据您上传的图片进行真实分析。*"""
    else:
        analysis_text += "\n\n---\n\n*💡 这是演示版本，显示的是预设的分析结果。*"

    return {
        'success': True,
        'analysis': analysis_text,
        'style': style_config['name']
    }


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
