"""
十神分析模块 - 分析十神配置、性格与事业
"""

from .base_data import *
from .bazi_parser import BaziParser


class ShishenAnalyzer:
    """十神分析器"""

    def __init__(self, parser: BaziParser):
        self.parser = parser
        self.shishen_mapping = self._calculate_shishen()

    def _get_shishen(self, tiangan: str) -> str:
        """根据天干获取十神"""
        day_master = self.parser.get_day_master()
        dm_wuxing = self.parser.get_day_master_wuxing()
        dm_yinyang = self.parser.get_day_master_yinyang()

        tg_wuxing = TIANGAN_WUXING[tiangan]
        tg_yinyang = TIANGAN_YINYANG[tiangan]

        # 判断五行关系
        if tg_wuxing == dm_wuxing:
            relation = '同'
        elif tg_wuxing == WUXING_SHENG[dm_wuxing]:
            relation = '生'
        elif tg_wuxing == WUXING_KE[dm_wuxing]:
            relation = '克'
        elif tg_wuxing == WUXING_BEI_KE[dm_wuxing]:
            relation = '被克'
        elif tg_wuxing == WUXING_BEI_SHENG[dm_wuxing]:
            relation = '被生'
        else:
            return '未知'

        # 判断阴阳异同
        if dm_yinyang == tg_yinyang:
            yinyang_type = '阳'  # 同性
        else:
            yinyang_type = '阴'  # 异性

        return SHISHEN_RELATION[relation][yinyang_type]

    def _calculate_shishen(self) -> dict:
        """计算四柱十神"""
        result = {
            '年柱': {'天干': None, '藏干': []},
            '月柱': {'天干': None, '藏干': []},
            '日柱': {'天干': '日主', '藏干': []},
            '时柱': {'天干': None, '藏干': []}
        }

        for pillar_name in ['年柱', '月柱', '日柱', '时柱']:
            pillar = self.parser.pillars[pillar_name]

            # 天干十神（日干为日主）
            if pillar_name != '日柱':
                result[pillar_name]['天干'] = self._get_shishen(pillar['天干'])

            # 藏干十神
            for cg in pillar['藏干']:
                result[pillar_name]['藏干'].append(self._get_shishen(cg))

        return result

    def get_shishen_count(self) -> dict:
        """统计十神数量"""
        count = {
            '比肩': 0, '劫财': 0,
            '食神': 0, '伤官': 0,
            '偏财': 0, '正财': 0,
            '七杀': 0, '正官': 0,
            '偏印': 0, '正印': 0
        }

        for pillar_name in ['年柱', '月柱', '日柱', '时柱']:
            # 天干
            tg_shishen = self.shishen_mapping[pillar_name]['天干']
            if tg_shishen and tg_shishen != '日主':
                count[tg_shishen] += 1

            # 藏干
            for cg_shishen in self.shishen_mapping[pillar_name]['藏干']:
                if cg_shishen != '日主':
                    count[cg_shishen] += 0.5  # 藏干权重较低

        return count

    def get_dominant_shishen(self) -> list:
        """获取主要十神"""
        count = self.get_shishen_count()
        sorted_shishen = sorted(count.items(), key=lambda x: x[1], reverse=True)
        dominant = []
        for ss, cnt in sorted_shishen:
            if cnt >= 1:
                dominant.append((ss, cnt))
        return dominant

    def analyze_personality(self) -> dict:
        """分析性格特点"""
        dominant = self.get_dominant_shishen()
        personality = {
            '主要性格': [],
            '优点': [],
            '缺点': [],
            '建议': []
        }

        shishen_traits = {
            '比肩': {
                '性格': '独立自主、坚强刚毅、自尊心强',
                '优点': '意志坚定，独立性强，有主见',
                '缺点': '固执己见，不善妥协，过于自我',
                '建议': '学会团队合作，倾听他人意见'
            },
            '劫财': {
                '性格': '争强好胜、敢于冒险、行动力强',
                '优点': '积极进取，胆识过人，果断干练',
                '缺点': '冲动急躁，容易与人争执，理财能力弱',
                '建议': '培养耐心，理性决策，注意理财'
            },
            '食神': {
                '性格': '温和善良、乐观开朗、追求享受',
                '优点': '才华横溢，口才好，人缘佳',
                '缺点': '容易安于现状，缺乏进取心',
                '建议': '设定目标，保持动力，避免懈怠'
            },
            '伤官': {
                '性格': '聪明伶俐、创意丰富、追求完美',
                '优点': '才思敏捷，创新能力强，表达能力佳',
                '缺点': '恃才傲物，口无遮拦，容易得罪人',
                '建议': '谦虚谨慎，注意言辞，尊重他人'
            },
            '偏财': {
                '性格': '慷慨大方、交游广阔、善于经营',
                '优点': '人脉广泛，商业头脑好，机遇多',
                '缺点': '花钱大手大脚，感情不专一',
                '建议': '理性消费，珍惜感情，稳健投资'
            },
            '正财': {
                '性格': '勤俭持家、踏实稳重、重视家庭',
                '优点': '理财有方，责任心强，为人可靠',
                '缺点': '过于保守，不敢冒险，缺乏魄力',
                '建议': '适当冒险，把握机会，平衡工作与生活'
            },
            '七杀': {
                '性格': '果敢刚毅、有魄力、敢于挑战',
                '优点': '领导力强，执行力佳，有威严',
                '缺点': '脾气急躁，容易树敌，压力大',
                '建议': '修身养性，以德服人，注意健康'
            },
            '正官': {
                '性格': '正直守信、有责任感、重视名誉',
                '优点': '品行端正，组织能力强，受人尊敬',
                '缺点': '过于拘谨，不够灵活，压抑自我',
                '建议': '适当放松，保持弹性，表达自我'
            },
            '偏印': {
                '性格': '思维独特、喜欢钻研、内向孤僻',
                '优点': '悟性高，专注力强，有特殊才能',
                '缺点': '想法偏激，不善交际，多愁善感',
                '建议': '多与人交流，保持乐观，走出舒适区'
            },
            '正印': {
                '性格': '仁慈宽厚、有涵养、重视精神',
                '优点': '学识渊博，有爱心，贵人运强',
                '缺点': '依赖性强，缺乏主见，优柔寡断',
                '建议': '培养独立性，勇于决断，行动起来'
            }
        }

        for ss, cnt in dominant[:3]:  # 取前三个主要十神
            if ss in shishen_traits:
                traits = shishen_traits[ss]
                personality['主要性格'].append(f"{ss}: {traits['性格']}")
                personality['优点'].append(traits['优点'])
                personality['缺点'].append(traits['缺点'])
                personality['建议'].append(traits['建议'])

        return personality

    def analyze_career(self) -> dict:
        """分析事业方向"""
        dominant = self.get_dominant_shishen()
        career = {
            '适合行业': [],
            '事业建议': [],
            '财运分析': ''
        }

        career_mapping = {
            '比肩': ['创业、独立经营', '体育竞技', '自由职业'],
            '劫财': ['投资理财', '销售业务', '体力劳动相关'],
            '食神': ['餐饮美食', '艺术创作', '教育培训', '娱乐行业'],
            '伤官': ['技术研发', '艺术设计', '咨询顾问', '律师'],
            '偏财': ['商业贸易', '投资理财', '房地产', '中介服务'],
            '正财': ['财务会计', '银行金融', '稳定企业工作'],
            '七杀': ['军警法律', '管理层', '外科医生', '运动员'],
            '正官': ['公务员', '企业管理', '教师', '大型企业'],
            '偏印': ['宗教哲学', '命理玄学', '医药研究', '技术钻研'],
            '正印': ['文化教育', '出版传媒', '学术研究', '慈善公益']
        }

        for ss, cnt in dominant[:3]:
            if ss in career_mapping:
                career['适合行业'].extend(career_mapping[ss])

        # 财运分析
        count = self.get_shishen_count()
        wealth = count['正财'] + count['偏财']
        if wealth >= 2:
            career['财运分析'] = '财星旺盛，财运较好，适合从事与钱财相关的工作'
        elif wealth >= 1:
            career['财运分析'] = '财运中等，通过努力可获得稳定收入'
        else:
            career['财运分析'] = '财星较弱，需要更多努力积累财富，宜稳健理财'

        # 事业建议
        if count['正官'] + count['七杀'] >= 1.5:
            career['事业建议'].append('官杀得力，适合从政或管理工作')
        if count['食神'] + count['伤官'] >= 1.5:
            career['事业建议'].append('食伤旺盛，适合技术或艺术创作领域')
        if count['正印'] + count['偏印'] >= 1.5:
            career['事业建议'].append('印星得力，适合文化教育或研究工作')

        return career

    def analyze_relationships(self) -> dict:
        """分析人际关系与婚姻"""
        count = self.get_shishen_count()
        gender = self.parser.gender

        relationships = {
            '婚姻感情': '',
            '人际关系': '',
            '家庭关系': ''
        }

        # 婚姻分析（男女不同）
        if gender == '男':
            # 男命以财为妻
            wealth = count['正财'] + count['偏财']
            if wealth >= 2:
                relationships['婚姻感情'] = '财星旺盛，异性缘好，婚姻机会多，但需注意专一'
            elif wealth >= 1:
                relationships['婚姻感情'] = '财星适中，婚姻运势中等，感情较为稳定'
            else:
                relationships['婚姻感情'] = '财星偏弱，婚姻缘分来得较晚，宜主动追求'
        else:
            # 女命以官杀为夫
            official = count['正官'] + count['七杀']
            if official >= 2:
                relationships['婚姻感情'] = '官杀旺盛，异性缘好，但官杀混杂需注意感情专一'
            elif official >= 1:
                relationships['婚姻感情'] = '官星适中，婚姻运势较好，能遇良配'
            else:
                relationships['婚姻感情'] = '官星偏弱，婚姻缘分需等待，宜耐心'

        # 人际关系
        if count['比肩'] + count['劫财'] >= 2:
            relationships['人际关系'] = '比劫旺盛，朋友多但竞争也多，注意合作共赢'
        elif count['食神'] + count['伤官'] >= 1.5:
            relationships['人际关系'] = '食伤旺盛，口才好人缘佳，但需注意言辞'
        else:
            relationships['人际关系'] = '人际关系适中，保持真诚即可获得良好人缘'

        # 家庭关系
        if count['正印'] + count['偏印'] >= 1.5:
            relationships['家庭关系'] = '印星得力，与长辈关系好，家庭温馨'
        else:
            relationships['家庭关系'] = '家庭关系一般，需主动维护与家人的感情'

        return relationships

    def display_analysis(self) -> str:
        """显示十神分析结果"""
        lines = []
        lines.append("=" * 60)
        lines.append("                    十 神 分 析")
        lines.append("=" * 60)
        lines.append("")

        # 四柱十神
        lines.append("【四柱十神配置】")
        lines.append(f"        年柱      月柱      日柱      时柱")
        lines.append(f"        ----      ----      ----      ----")

        tg_line = "天干:   "
        for p in ['年柱', '月柱', '日柱', '时柱']:
            ss = self.shishen_mapping[p]['天干']
            tg = self.parser.pillars[p]['天干']
            tg_line += f"{tg}({ss[:2] if ss else '??'})  "
        lines.append(tg_line)

        dz_line = "地支:   "
        for p in ['年柱', '月柱', '日柱', '时柱']:
            dz = self.parser.pillars[p]['地支']
            cg_ss = self.shishen_mapping[p]['藏干']
            main_ss = cg_ss[0][:2] if cg_ss else '??'
            dz_line += f"{dz}({main_ss})  "
        lines.append(dz_line)

        # 十神统计
        lines.append("")
        lines.append("【十神数量统计】")
        count = self.get_shishen_count()
        for category in [('比肩', '劫财'), ('食神', '伤官'), ('偏财', '正财'), ('七杀', '正官'), ('偏印', '正印')]:
            line = "  "
            for ss in category:
                line += f"{ss}: {count[ss]:.1f}  "
            lines.append(line)

        # 性格分析
        lines.append("")
        lines.append("【性格特点分析】")
        personality = self.analyze_personality()
        for trait in personality['主要性格']:
            lines.append(f"  • {trait}")

        lines.append("")
        lines.append("  优点:")
        for adv in personality['优点']:
            lines.append(f"    - {adv}")

        lines.append("")
        lines.append("  缺点:")
        for dis in personality['缺点']:
            lines.append(f"    - {dis}")

        lines.append("")
        lines.append("  建议:")
        for sug in personality['建议']:
            lines.append(f"    - {sug}")

        # 事业分析
        lines.append("")
        lines.append("【事业发展分析】")
        career = self.analyze_career()
        lines.append(f"  适合行业: {', '.join(set(career['适合行业'][:6]))}")
        lines.append(f"  财运分析: {career['财运分析']}")
        for advice in career['事业建议']:
            lines.append(f"  • {advice}")

        # 人际关系
        lines.append("")
        lines.append("【人际婚姻分析】")
        relationships = self.analyze_relationships()
        lines.append(f"  婚姻感情: {relationships['婚姻感情']}")
        lines.append(f"  人际关系: {relationships['人际关系']}")
        lines.append(f"  家庭关系: {relationships['家庭关系']}")

        lines.append("=" * 60)
        return "\n".join(lines)
