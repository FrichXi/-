"""
命理报告模块 - 生成综合命理报告
"""

from .bazi_parser import BaziParser
from .wuxing_analyzer import WuxingAnalyzer
from .shishen_analyzer import ShishenAnalyzer
from .dayun_analyzer import DayunAnalyzer


class ReportGenerator:
    """命理报告生成器"""

    def __init__(self, parser: BaziParser, wuxing: WuxingAnalyzer,
                 shishen: ShishenAnalyzer, dayun: DayunAnalyzer):
        self.parser = parser
        self.wuxing = wuxing
        self.shishen = shishen
        self.dayun = dayun

    def generate_summary(self) -> str:
        """生成命理总结"""
        lines = []
        lines.append("=" * 60)
        lines.append("                    命 理 总 结")
        lines.append("=" * 60)
        lines.append("")

        # 基本信息
        dm = self.parser.get_day_master()
        dm_wx = self.parser.get_day_master_wuxing()
        dm_yy = self.parser.get_day_master_yinyang()
        strength = self.wuxing.get_day_master_strength()

        lines.append("【命主基本信息】")
        lines.append(f"  八字: {self.parser.bazi_str}")
        lines.append(f"  日主: {dm} ({dm_wx}{dm_yy})")
        lines.append(f"  日主强弱: {strength}")
        lines.append(f"  性别: {self.parser.gender}")
        lines.append(f"  出生年: {self.parser.birth_year}年")
        lines.append(f"  当前年龄: {self.dayun.current_year - self.parser.birth_year}岁")
        lines.append("")

        # 五行喜忌
        yongshen = self.wuxing.get_yongshen()
        lines.append("【五行喜忌】")
        lines.append(f"  用神: {', '.join(yongshen['用神'])}")
        lines.append(f"  喜神: {', '.join(yongshen['喜神'])}")
        lines.append(f"  忌神: {', '.join(yongshen['忌神'])}")
        lines.append("")

        # 命格特点
        lines.append("【命格特点】")
        self._add_mingge_analysis(lines)
        lines.append("")

        # 人生建议
        lines.append("【人生发展建议】")
        self._add_life_suggestions(lines)
        lines.append("")

        # 2026年运势
        lines.append("【2026年运势提要】")
        liunian = self.dayun.analyze_liunian(2026)
        lines.append(f"  流年干支: {liunian['流年']}")
        lines.append(f"  运势等级: {liunian['运势等级']} ({liunian['运势评分']}分)")
        aspects = liunian['各方面运势']
        lines.append(f"  事业运: {aspects['事业']}")
        lines.append(f"  财运: {aspects['财运']}")
        lines.append(f"  感情运: {aspects['感情']}")
        lines.append(f"  健康运: {aspects['健康']}")
        lines.append("")

        # 吉祥指南
        lines.append("【开运吉祥指南】")
        self._add_lucky_guide(lines)

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)

    def _add_mingge_analysis(self, lines: list):
        """添加命格分析"""
        strength = self.wuxing.get_day_master_strength()
        dominant = self.shishen.get_dominant_shishen()

        if '旺' in strength:
            lines.append("  • 日主偏旺，命中能量充足")
            lines.append("  • 适合走财官路线，可担当重任")
            lines.append("  • 性格偏强势，需注意谦逊待人")
        else:
            lines.append("  • 日主偏弱，需借助外力")
            lines.append("  • 适合借助贵人、团队之力发展")
            lines.append("  • 性格偏温和，需培养主见和魄力")

        # 根据主要十神分析
        if dominant:
            main_ss = dominant[0][0]
            if main_ss in ['正官', '七杀']:
                lines.append("  • 官杀明显，适合从政或管理")
            elif main_ss in ['正财', '偏财']:
                lines.append("  • 财星明显，经商理财有天赋")
            elif main_ss in ['食神', '伤官']:
                lines.append("  • 食伤明显，才华横溢，适合技艺")
            elif main_ss in ['正印', '偏印']:
                lines.append("  • 印星明显，学业运好，适合学术")

    def _add_life_suggestions(self, lines: list):
        """添加人生建议"""
        yongshen = self.wuxing.get_yongshen()
        career = self.shishen.analyze_career()
        relationships = self.shishen.analyze_relationships()

        lines.append("  【事业方面】")
        lines.append(f"    推荐行业: {', '.join(set(career['适合行业'][:4]))}")
        for advice in career['事业建议'][:2]:
            lines.append(f"    • {advice}")

        lines.append("")
        lines.append("  【感情方面】")
        lines.append(f"    • {relationships['婚姻感情']}")

        lines.append("")
        lines.append("  【财富方面】")
        lines.append(f"    • {career['财运分析']}")

        # 根据用神给出具体建议
        lines.append("")
        lines.append("  【发展方向】")
        for wx in yongshen['用神']:
            wx_advice = self._get_wuxing_advice(wx)
            lines.append(f"    • {wx_advice}")

    def _get_wuxing_advice(self, wuxing: str) -> str:
        """根据五行给出建议"""
        advice_map = {
            '木': '木主仁，宜从事教育、文化、环保、出版等行业，向东方发展有利',
            '火': '火主礼，宜从事科技、能源、餐饮、传媒等行业，向南方发展有利',
            '土': '土主信，宜从事房地产、农业、建筑、矿业等行业，在本地发展有利',
            '金': '金主义，宜从事金融、机械、科技、法律等行业，向西方发展有利',
            '水': '水主智，宜从事贸易、运输、旅游、水利等行业，向北方发展有利'
        }
        return advice_map.get(wuxing, '')

    def _add_lucky_guide(self, lines: list):
        """添加开运指南"""
        yongshen = self.wuxing.get_yongshen()

        lucky_info = {
            '木': {'颜色': '绿色、青色', '数字': '3、8', '方位': '东方', '物品': '植物、木制品'},
            '火': {'颜色': '红色、紫色', '数字': '2、7', '方位': '南方', '物品': '电子产品、灯饰'},
            '土': {'颜色': '黄色、棕色', '数字': '5、10', '方位': '中央', '物品': '陶瓷、水晶'},
            '金': {'颜色': '白色、金色', '数字': '4、9', '方位': '西方', '物品': '金属饰品'},
            '水': {'颜色': '黑色、蓝色', '数字': '1、6', '方位': '北方', '物品': '鱼缸、水景'}
        }

        main_yongshen = yongshen['用神'][0] if yongshen['用神'] else yongshen['喜神'][0]
        info = lucky_info.get(main_yongshen, {})

        lines.append(f"  幸运五行: {main_yongshen}")
        lines.append(f"  幸运颜色: {info.get('颜色', '无')}")
        lines.append(f"  幸运数字: {info.get('数字', '无')}")
        lines.append(f"  有利方位: {info.get('方位', '无')}")
        lines.append(f"  开运物品: {info.get('物品', '无')}")

    def generate_full_report(self) -> str:
        """生成完整命理报告"""
        sections = []

        # 标题
        sections.append("")
        sections.append("╔" + "═" * 58 + "╗")
        sections.append("║" + "八 字 命 理 详 细 分 析 报 告".center(50) + "║")
        sections.append("╚" + "═" * 58 + "╝")
        sections.append("")

        # 各部分分析
        sections.append(self.parser.display_bazi())
        sections.append("")
        sections.append(self.wuxing.display_analysis())
        sections.append("")
        sections.append(self.shishen.display_analysis())
        sections.append("")
        sections.append(self.dayun.display_analysis())
        sections.append("")
        sections.append(self.generate_summary())

        # 结尾
        sections.append("")
        sections.append("╔" + "═" * 58 + "╗")
        sections.append("║" + "报 告 结 束".center(52) + "║")
        sections.append("╚" + "═" * 58 + "╝")
        sections.append("")
        sections.append("注：命理分析仅供参考，人生命运掌握在自己手中。")
        sections.append("    积极进取、善待他人、努力奋斗才是改变命运的根本。")
        sections.append("")

        return "\n".join(sections)
