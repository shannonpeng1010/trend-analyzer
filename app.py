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


def analyze_with_claude(image_paths, style_key, user_context='', custom_template=''):
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

        'formal_management': """# 综合运营分析报告

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

        'concise_business': """# 业务指标速览

**用户增长**
- 新增用户 ↑ 23.5%，DAU 45,800
- 次日留存 68%，7日留存 42%

**转化效率**
- 访问→注册 12.3%（↑ 2.1%）
- 注册→付费 8.7%（↑ 0.9%）

**营收表现**
- GMV ↑ 34%（同比）、↑ 18%（环比）
- 客单价 ¥128，付费用户 5,000+

**建议**
持续营销投入 | 提升用户价值 | 精细化运营""",

        'concise_management': """# 管理视角速览

**目标达成**
- 用户目标 112%（45.8K/40K）
- 营收目标 108%（562W/520W）
- 技术稳定性 100%

**关键成果**
✅ 获客成本 ↓ 15%
✅ 用户满意度 4.2 → 4.6
✅ 系统性能 ↑ 20%

**风险**
⚠️ 竞争加剧
⚠️ 成本控制压力
⚠️ 人才缺口

**下步重点**
用户规模翻番 | 营收结构优化 | 团队扩充 30%""",

        'detailed_tech': """# 技术深度分析报告

## 一、性能指标详细分析

### 1.1 响应时间优化成果
**数据对比**：
- 上周平均：245ms
- 本周平均：198ms
- 优化幅度：19.2%

**优化措施**：
1. 数据库查询优化：减少了 30% 的慢查询
2. 缓存命中率提升：从 65% 提升至 82%
3. 代码层面优化：减少不必要的循环和递归

**效果分析**：
响应时间的显著降低直接提升了用户体验，用户投诉率下降 15%。

### 1.2 并发处理能力评估
**峰值 QPS 分析**：
- 稳定区间：8500-9200
- 较基准值提升：15%
- 瓶颈识别：数据库连接池在高峰时段接近上限

**压力测试结果**：
- 10000 QPS 场景：系统可正常运行，但响应时间增加至 350ms
- 12000 QPS 场景：部分请求超时，建议扩容

### 1.3 系统稳定性保障
**SLA 达成情况**：
- 目标：99.95%
- 实际：99.96%
- 计划外停机：0 次
- 计划内维护：2 次（共 30 分钟）

## 二、资源使用深度分析

### 2.1 CPU 使用模式
**波动分析**：
- 日常范围：45%-60%
- 峰值时段：09:00-11:00 和 14:00-16:00
- 峰值水平：72%

**优化建议**：
1. 考虑引入自动扩缩容机制
2. 将非关键任务调度至低峰时段
3. 优化高 CPU 占用的算法逻辑

### 2.2 内存管理
**内存占用趋势**：
- 峰值：4.2GB（较上期 ↓ 8%）
- 平均：3.5GB
- 内存泄漏：未检测到

**优化成果**：
通过代码审查发现并修复了 3 处潜在内存泄漏点。

### 2.3 网络带宽
**使用情况**：
- 平均带宽：120 Mbps
- 峰值带宽：280 Mbps
- 总容量：1 Gbps
- 使用率：28%

**评估**：带宽充足，短期无扩容需求。

## 三、异常监测与处理

### 3.1 性能抖动分析
**3 次抖动详情**：
1. 周二 10:35：数据库主从切换，持续 15 秒
2. 周四 14:20：慢查询导致，持续 8 秒
3. 周五 16:48：突发流量，持续 12 秒

**根因分析**：
- 第 1 次：数据库架构问题，已优化切换策略
- 第 2 次：查询语句未加索引，已修复
- 第 3 次：营销活动流量预估不足，已调整容量规划

### 3.2 错误率监控
**错误统计**：
- 总请求数：8,500,000
- 错误数：1,700
- 错误率：0.02%

**错误分类**：
- 4xx 错误：65%（主要是用户输入问题）
- 5xx 错误：35%（主要是第三方 API 超时）

## 四、技术债务与改进建议

### 4.1 技术债务清单
1. **数据库层**：部分表结构设计不合理，查询效率低
2. **代码质量**：单元测试覆盖率仅 45%，需提升至 80%
3. **监控体系**：缺少业务级别监控，只有系统级监控

### 4.2 改进优先级
**P0（本周）**：
- 优化数据库慢查询
- 完善监控告警机制

**P1（本月）**：
- 提升单元测试覆盖率
- 重构核心模块代码

**P2（本季度）**：
- 数据库表结构优化
- 引入自动化性能测试

### 4.3 长期技术规划
1. **微服务化**：将单体应用拆分为微服务架构
2. **容器化**：全面容器化部署，提升资源利用率
3. **智能运维**：引入 AIOps，实现智能故障预测

## 五、总结与展望

### 5.1 本周亮点
✨ 性能优化效果显著，用户体验明显提升
✨ 系统稳定性保持高水平，SLA 超额完成
✨ 技术团队快速响应，问题解决及时

### 5.2 下周重点
🎯 持续优化数据库性能
🎯 提升监控覆盖面和准确性
🎯 推进技术债务偿还计划

### 5.3 风险提示
⚠️ 用户增长可能导致系统压力增大，需提前规划扩容
⚠️ 第三方 API 稳定性存在风险，需增加容错机制""",

        'detailed_business': """# 业务深度分析报告

## 一、用户增长深度剖析

### 1.1 新增用户分析
**增长数据**：
- 本期新增：10,820 人
- 上期新增：8,780 人
- 增长率：23.5%

**渠道分布**：
- 自然流量：35%（3,787 人）
- 信息流广告：40%（4,328 人）
- 社交媒体：15%（1,623 人）
- 用户推荐：10%（1,082 人）

**获客成本**：
- 平均 CAC：¥45/人（↓ 12%）
- 信息流 CAC：¥38/人
- 社交媒体 CAC：¥52/人

**质量评估**：
新增用户中高价值用户占比 18%，较上期提升 3 个百分点。

### 1.2 留存率深度分析
**留存数据对比**：
| 留存周期 | 本期 | 上期 | 行业均值 |
|---------|------|------|---------|
| 次日留存 | 68% | 65% | 55% |
| 7日留存 | 42% | 39% | 30% |
| 30日留存| 28% | 25% | 18% |

**留存曲线分析**：
用户留存曲线呈健康的指数衰减，第7天后趋于稳定，说明产品粘性良好。

**流失原因分析**：
通过用户访谈，主要流失原因为：
1. 功能不满足需求（35%）
2. 竞品吸引（28%）
3. 价格因素（22%）
4. 其他原因（15%）

### 1.3 活跃度提升分析
**使用时长**：
- 人均：28 分钟/天（↑ 12%）
- 高频用户：45 分钟/天
- 中频用户：20 分钟/天
- 低频用户：8 分钟/天

**使用频次**：
- 日均启动：3.2 次（↑ 0.4 次）
- 周活跃天数：4.8 天

**功能使用分布**：
- 核心功能 A：78% 用户使用
- 功能 B：52% 用户使用
- 功能 C：31% 用户使用

## 二、转化漏斗优化成果

### 2.1 访问→注册转化
**转化数据**：
- 转化率：12.3%（↑ 2.1%）
- 访问量：88,000
- 注册量：10,824

**优化措施**：
1. 简化注册流程：从 5 步缩减至 3 步
2. 优化注册页文案：突出价值主张
3. A/B 测试优化：找到最佳注册按钮颜色和位置

**各渠道转化对比**：
- 自然流量：15.2%
- 广告流量：10.8%
- 社交媒体：13.5%

### 2.2 注册→付费转化
**转化数据**：
- 转化率：8.7%（↑ 0.9%）
- 注册用户：10,824
- 付费用户：942

**转化周期**：
- 平均转化周期：12 天
- 快速转化（3天内）：25%
- 中速转化（3-14天）：45%
- 慢速转化（14天以上）：30%

**转化驱动因素**：
1. 产品试用体验好：68%
2. 促销活动吸引：42%
3. 功能刚需：35%
4. 朋友推荐：18%

### 2.3 整体漏斗效率
**漏斗转化全景**：
访问 → 注册（12.3%）→ 首次体验（85%）→ 深度使用（45%）→ 付费（8.7%）

**整体效率提升**：
相比上期，整体转化效率提升 18%，主要得益于注册流程优化和产品体验改善。

## 三、营收表现深度解析

### 3.1 GMV 增长分析
**增长数据**：
- GMV：¥1,245W
- 同比增长：34%
- 环比增长：18%

**增长驱动力**：
1. 用户规模增长贡献：60%
2. 客单价提升贡献：25%
3. 购买频次增加贡献：15%

**营收结构**：
- 新用户贡献：45%
- 老用户贡献：55%

### 3.2 客单价分析
**客单价趋势**：
- 当前：¥128
- 上期：¥125
- 增长：2.4%

**价格段分布**：
- 低价段（<¥50）：15%
- 中价段（¥50-200）：65%
- 高价段（>¥200）：20%

**提升策略**：
1. 推出组合套餐：提升 12% 客单价
2. 会员升级引导：高价值用户占比提升
3. 交叉销售：关联推荐转化率 8%

### 3.3 付费用户运营
**用户规模**：
- 总付费用户：5,120 人
- 新增付费：942 人
- 复购用户：3,850 人（75%）

**用户分层**：
- 高价值用户（LTV>¥500）：18%
- 中价值用户（LTV ¥200-500）：45%
- 低价值用户（LTV<¥200）：37%

**运营策略**：
- 高价值用户：VIP 服务 + 专属权益
- 中价值用户：会员升级引导
- 低价值用户：活跃度提升计划

## 四、营销活动效果评估

### 4.1 活动概览
**本期活动**：
1. 新春促销（2/1-2/7）
2. 情人节特惠（2/14）
3. 老用户回馈（2/20-2/22）

### 4.2 活动效果
**新春促销**：
- 参与用户：15,200 人
- 转化率：15.2%
- ROI：3.8
- 带来营收：¥342W

**情人节特惠**：
- 参与用户：8,500 人
- 转化率：12.8%
- ROI：3.2
- 带来营收：¥128W

### 4.3 营销渠道 ROI
| 渠道 | 投入 | 产出 | ROI |
|------|------|------|-----|
| 信息流广告 | ¥85W | ¥323W | 3.8 |
| 社交媒体 | ¥42W | ¥134W | 3.2 |
| KOL 合作 | ¥38W | ¥152W | 4.0 |
| SEO/SEM | ¥25W | ¥88W | 3.5 |

## 五、竞争分析与市场定位

### 5.1 竞争格局
**主要竞品**：
- 竞品 A：市场份额 35%，用户规模最大
- 竞品 B：市场份额 28%，价格优势明显
- 我们：市场份额 12%，功能体验领先

### 5.2 差异化优势
1. **产品体验**：用户满意度 4.6，高于竞品平均 4.2
2. **功能创新**：独家功能吸引精准用户
3. **服务质量**：响应速度快，问题解决率高

### 5.3 市场机会
- 细分市场需求未被满足
- 用户对品质的追求提升
- 行业整体增长红利期

## 六、业务洞察与建议

### 6.1 关键洞察
💡 **洞察 1**：营销活动 ROI 优秀，建议持续加大投入
💡 **洞察 2**：产品粘性强，但需关注功能流失用户反馈
💡 **洞察 3**：高价值用户占比偏低，需优化用户结构

### 6.2 行动建议
**短期（本月）**：
1. 启动高价值用户增长计划
2. 优化核心功能，降低流失
3. 加大高 ROI 渠道投放

**中期（本季度）**：
1. 推出会员体系 2.0
2. 建立用户成长激励机制
3. 拓展新的营销渠道

**长期（今年）**：
1. 品牌升级，提升市场认知
2. 产品矩阵化，满足多层次需求
3. 建立行业生态，巩固竞争壁垒

### 6.3 风险提示
⚠️ **竞争风险**：竞品降价促销可能影响用户增长
⚠️ **成本风险**：获客成本有上升趋势，需控制
⚠️ **市场风险**：宏观经济波动影响用户付费意愿

## 七、下期目标

### 7.1 增长目标
- DAU 目标：52,000（↑ 13.5%）
- 新增用户：12,000（↑ 11%）
- 付费用户：6,000（↑ 17%）

### 7.2 营收目标
- GMV 目标：¥1,450W（↑ 16.5%）
- 客单价目标：¥132（↑ 3%）

### 7.3 关键举措
1. 推出春季大促活动
2. 上线新功能吸引用户
3. 优化转化漏斗各环节
4. 加强高价值用户运营""",

        'detailed_management': """（此处已省略，使用之前的管理视角内容）""",

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

        'weekly_report': """（使用之前的周报内容）""",

        'monthly_report': """（使用之前的月报内容）"""
    }

    # 如果有自定义模板，使用模板格式
    if custom_template:
        # 在演示版本中，我们仍返回预设内容，但提示使用了模板
        analysis_text = f"""## 📋 使用自定义模板格式

{custom_template}

---

## 📊 根据模板生成的分析

{demo_analyses.get(style_key, demo_analyses['formal_tech'])}

---

*💡 演示版本：实际使用时，AI 将根据您的模板格式和上传的图片生成相应分析。*"""
    else:
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
        # 检查是否有对应的自定义模板
        template_key = style_key.replace('_report', '')
        custom_template = request.form.get(f'template_{template_key}', '')

        result = analyze_with_claude(saved_images, style_key, user_context, custom_template)
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
