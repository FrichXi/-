"""
五行分析模块 - 分析五行强弱喜忌
"""

from .base_data import *
from .bazi_parser import BaziParser


class WuxingAnalyzer:
    """五行分析器"""

    def __init__(self, parser: BaziParser):
        self.parser = parser
        self.wuxing_count = self._calculate_wuxing_count()
        self.wuxing_score = self._calculate_wuxing_score()

    def _calculate_wuxing_count(self) -> dict:
        """计算五行数量"""
        count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}

        # 天干五行
        for tg in self.parser.get_all_tiangan():
            count[TIANGAN_WUXING[tg]] += 1

        # 地支五行（只计本气）
        for dz in self.parser.get_all_dizhi():
            count[DIZHI_WUXING[dz]] += 1

        return count

    def _calculate_wuxing_score(self) -> dict:
        """计算五行力量分数"""
        score = {'木': 0.0, '火': 0.0, '土': 0.0, '金': 0.0, '水': 0.0}

        # 天干力量
        for tg in self.parser.get_all_tiangan():
            score[TIANGAN_WUXING[tg]] += WUXING_WEIGHT['天干']

        # 地支藏干力量
        for pillar_name in ['年柱', '月柱', '日柱', '时柱']:
            canggan = self.parser.pillars[pillar_name]['藏干']
            for i, cg in enumerate(canggan):
                if i == 0:
                    score[TIANGAN_WUXING[cg]] += WUXING_WEIGHT['地支本气']
                elif i == 1:
                    score[TIANGAN_WUXING[cg]] += WUXING_WEIGHT['地支中气']
                else:
                    score[TIANGAN_WUXING[cg]] += WUXING_WEIGHT['地支余气']

        return score

    def get_day_master_strength(self) -> str:
        """判断日主强弱"""
        day_master = self.parser.get_day_master()
        dm_wuxing = self.parser.get_day_master_wuxing()

        # 帮扶力量：同类五行 + 生我五行
        help_score = self.wuxing_score[dm_wuxing]
        help_score += self.wuxing_score[WUXING_BEI_SHENG[dm_wuxing]]

        # 耗泄力量：我生 + 我克 + 克我
        consume_score = self.wuxing_score[WUXING_SHENG[dm_wuxing]]
        consume_score += self.wuxing_score[WUXING_KE[dm_wuxing]]
        consume_score += self.wuxing_score[WUXING_BEI_KE[dm_wuxing]]

        total = help_score + consume_score
        help_ratio = help_score / total if total > 0 else 0.5

        # 考虑月令（月支对日主的影响最大）
        month_dizhi = self.parser.pillars['月柱']['地支']
        month_canggan = DIZHI_CANGGAN[month_dizhi]
        month_main_wuxing = TIANGAN_WUXING[month_canggan[0]]

        # 月令得令判断
        is_deling = False
        if month_main_wuxing == dm_wuxing:
            is_deling = True
            help_ratio += 0.1
        elif month_main_wuxing == WUXING_BEI_SHENG[dm_wuxing]:
            is_deling = True
            help_ratio += 0.05

        if help_ratio >= 0.5:
            if help_ratio >= 0.65:
                return '日主极旺'
            elif help_ratio >= 0.55:
                return '日主偏旺'
            else:
                return '日主中和偏旺'
        else:
            if help_ratio <= 0.35:
                return '日主极弱'
            elif help_ratio <= 0.45:
                return '日主偏弱'
            else:
                return '日主中和偏弱'

    def get_yongshen(self) -> dict:
        """确定用神喜忌"""
        day_master = self.parser.get_day_master()
        dm_wuxing = self.parser.get_day_master_wuxing()
        strength = self.get_day_master_strength()

        result = {
            '用神': [],
            '喜神': [],
            '忌神': [],
            '仇神': [],
            '闲神': []
        }

        if '旺' in strength:
            # 日主旺，喜克泄耗
            result['用神'].append(WUXING_KE[dm_wuxing])  # 我克者为财
            result['喜神'].append(WUXING_SHENG[dm_wuxing])  # 我生者为食伤
            result['喜神'].append(WUXING_BEI_KE[dm_wuxing])  # 克我者为官杀
            result['忌神'].append(dm_wuxing)  # 同类为比劫
            result['忌神'].append(WUXING_BEI_SHENG[dm_wuxing])  # 生我者为印
        else:
            # 日主弱，喜生扶
            result['用神'].append(WUXING_BEI_SHENG[dm_wuxing])  # 生我者为印
            result['喜神'].append(dm_wuxing)  # 同类为比劫
            result['忌神'].append(WUXING_KE[dm_wuxing])  # 我克者为财
            result['忌神'].append(WUXING_BEI_KE[dm_wuxing])  # 克我者为官杀
            result['仇神'].append(WUXING_SHENG[dm_wuxing])  # 我生者为食伤

        return result

    def get_lacking_wuxing(self) -> list:
        """获取缺失的五行"""
        lacking = []
        for wx in WUXING:
            if self.wuxing_count[wx] == 0:
                lacking.append(wx)
        return lacking

    def get_excess_wuxing(self) -> list:
        """获取过旺的五行"""
        total = sum(self.wuxing_score.values())
        avg = total / 5
        excess = []
        for wx in WUXING:
            if self.wuxing_score[wx] > avg * 1.5:
                excess.append(wx)
        return excess

    def analyze_wuxing_balance(self) -> dict:
        """分析五行平衡"""
        total = sum(self.wuxing_score.values())
        result = {}

        for wx in WUXING:
            percentage = (self.wuxing_score[wx] / total * 100) if total > 0 else 20
            if percentage >= 30:
                status = '过旺'
            elif percentage >= 22:
                status = '偏旺'
            elif percentage <= 10:
                status = '偏弱'
            elif percentage <= 5:
                status = '极弱'
            else:
                status = '适中'

            result[wx] = {
                '分数': round(self.wuxing_score[wx], 2),
                '比例': f"{percentage:.1f}%",
                '状态': status
            }

        return result

    def display_analysis(self) -> str:
        """显示五行分析结果"""
        lines = []
        lines.append("=" * 60)
        lines.append("                    五 行 分 析")
        lines.append("=" * 60)
        lines.append("")

        # 五行统计
        lines.append("【五行数量统计】")
        count_str = "  "
        for wx in WUXING:
            count_str += f"{wx}: {self.wuxing_count[wx]}  "
        lines.append(count_str)

        # 五行力量
        lines.append("")
        lines.append("【五行力量评分】")
        balance = self.analyze_wuxing_balance()
        for wx in WUXING:
            info = balance[wx]
            bar_len = int(info['分数'] * 5)
            bar = "█" * bar_len
            lines.append(f"  {wx}: {info['分数']:.2f} ({info['比例']}) {bar} [{info['状态']}]")

        # 日主强弱
        lines.append("")
        lines.append("【日主强弱判断】")
        strength = self.get_day_master_strength()
        dm = self.parser.get_day_master()
        dm_wx = self.parser.get_day_master_wuxing()
        lines.append(f"  日主 {dm}({dm_wx}) - {strength}")

        # 用神喜忌
        lines.append("")
        lines.append("【用神喜忌分析】")
        yongshen = self.get_yongshen()
        for category, elements in yongshen.items():
            if elements:
                lines.append(f"  {category}: {', '.join(elements)}")

        # 缺失五行
        lacking = self.get_lacking_wuxing()
        if lacking:
            lines.append("")
            lines.append(f"【五行缺失】: {', '.join(lacking)}")
        else:
            lines.append("")
            lines.append("【五行缺失】: 无（五行俱全）")

        lines.append("=" * 60)
        return "\n".join(lines)
