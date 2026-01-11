"""
大运流年模块 - 计算大运流年运势
"""

from .base_data import *
from .bazi_parser import BaziParser
from .wuxing_analyzer import WuxingAnalyzer


class DayunAnalyzer:
    """大运流年分析器"""

    def __init__(self, parser: BaziParser, wuxing_analyzer: WuxingAnalyzer, current_year: int = 2026):
        self.parser = parser
        self.wuxing_analyzer = wuxing_analyzer
        self.current_year = current_year
        self.dayun_list = self._calculate_dayun()

    def _get_dayun_direction(self) -> int:
        """确定大运排列方向（顺排还是逆排）"""
        year_tiangan = self.parser.pillars['年柱']['天干']
        gender = self.parser.gender

        # 阳年男命、阴年女命顺排
        # 阴年男命、阳年女命逆排
        year_yinyang = TIANGAN_YINYANG[year_tiangan]

        if (year_yinyang == '阳' and gender == '男') or (year_yinyang == '阴' and gender == '女'):
            return 1  # 顺排
        else:
            return -1  # 逆排

    def _calculate_dayun(self) -> list:
        """计算大运"""
        month_tiangan = self.parser.pillars['月柱']['天干']
        month_dizhi = self.parser.pillars['月柱']['地支']

        direction = self._get_dayun_direction()
        dayun_list = []

        tg_idx = TIANGAN.index(month_tiangan)
        dz_idx = DIZHI.index(month_dizhi)

        # 起运年龄（简化计算，假设为3岁起运）
        start_age = 3

        for i in range(10):  # 计算10步大运
            new_tg_idx = (tg_idx + direction * (i + 1)) % 10
            new_dz_idx = (dz_idx + direction * (i + 1)) % 12

            new_tiangan = TIANGAN[new_tg_idx]
            new_dizhi = DIZHI[new_dz_idx]

            start_year = self.parser.birth_year + start_age + i * 10
            end_year = start_year + 9

            dayun_list.append({
                '序号': i + 1,
                '天干': new_tiangan,
                '地支': new_dizhi,
                '干支': new_tiangan + new_dizhi,
                '起始年龄': start_age + i * 10,
                '结束年龄': start_age + (i + 1) * 10 - 1,
                '起始年份': start_year,
                '结束年份': end_year,
                '天干五行': TIANGAN_WUXING[new_tiangan],
                '地支五行': DIZHI_WUXING[new_dizhi]
            })

        return dayun_list

    def get_current_dayun(self) -> dict:
        """获取当前大运"""
        age = self.current_year - self.parser.birth_year
        for dayun in self.dayun_list:
            if dayun['起始年龄'] <= age <= dayun['结束年龄']:
                return dayun
        return self.dayun_list[-1] if self.dayun_list else None

    def _get_shishen(self, tiangan: str) -> str:
        """根据天干获取十神"""
        day_master = self.parser.get_day_master()
        dm_wuxing = self.parser.get_day_master_wuxing()
        dm_yinyang = self.parser.get_day_master_yinyang()

        tg_wuxing = TIANGAN_WUXING[tiangan]
        tg_yinyang = TIANGAN_YINYANG[tiangan]

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

        if dm_yinyang == tg_yinyang:
            yinyang_type = '阳'
        else:
            yinyang_type = '阴'

        return SHISHEN_RELATION[relation][yinyang_type]

    def analyze_dayun(self, dayun: dict) -> dict:
        """分析单步大运"""
        yongshen = self.wuxing_analyzer.get_yongshen()
        tg_wuxing = dayun['天干五行']
        dz_wuxing = dayun['地支五行']

        # 计算运势评分
        score = 50  # 基础分

        # 检查天干五行是否为用神/喜神/忌神
        if tg_wuxing in yongshen['用神']:
            score += 20
        elif tg_wuxing in yongshen['喜神']:
            score += 10
        elif tg_wuxing in yongshen['忌神']:
            score -= 15
        elif tg_wuxing in yongshen['仇神']:
            score -= 10

        # 检查地支五行
        if dz_wuxing in yongshen['用神']:
            score += 15
        elif dz_wuxing in yongshen['喜神']:
            score += 8
        elif dz_wuxing in yongshen['忌神']:
            score -= 12
        elif dz_wuxing in yongshen['仇神']:
            score -= 8

        # 确定运势等级
        if score >= 70:
            level = '大吉'
            description = '此运大吉，诸事顺遂，可积极进取'
        elif score >= 60:
            level = '中吉'
            description = '此运中吉，整体顺利，宜把握机会'
        elif score >= 50:
            level = '平运'
            description = '此运平稳，无大起落，宜稳中求进'
        elif score >= 40:
            level = '小凶'
            description = '此运略有波折，需谨慎行事'
        else:
            level = '凶运'
            description = '此运多有阻碍，宜守不宜攻'

        # 获取十神
        tg_shishen = self._get_shishen(dayun['天干'])

        return {
            '大运': dayun['干支'],
            '年龄范围': f"{dayun['起始年龄']}-{dayun['结束年龄']}岁",
            '年份范围': f"{dayun['起始年份']}-{dayun['结束年份']}年",
            '天干十神': tg_shishen,
            '运势评分': score,
            '运势等级': level,
            '运势描述': description
        }

    def get_liunian(self, year: int) -> dict:
        """获取流年信息"""
        # 计算流年干支
        # 以1984年甲子年为基准
        base_year = 1984
        diff = year - base_year
        tg_idx = diff % 10
        dz_idx = diff % 12

        tiangan = TIANGAN[tg_idx]
        dizhi = DIZHI[dz_idx]

        return {
            '年份': year,
            '天干': tiangan,
            '地支': dizhi,
            '干支': tiangan + dizhi,
            '天干五行': TIANGAN_WUXING[tiangan],
            '地支五行': DIZHI_WUXING[dizhi],
            '年龄': year - self.parser.birth_year
        }

    def analyze_liunian(self, year: int) -> dict:
        """分析流年运势"""
        liunian = self.get_liunian(year)
        yongshen = self.wuxing_analyzer.get_yongshen()

        tg_wuxing = liunian['天干五行']
        dz_wuxing = liunian['地支五行']

        # 计算运势评分
        score = 50

        if tg_wuxing in yongshen['用神']:
            score += 20
        elif tg_wuxing in yongshen['喜神']:
            score += 10
        elif tg_wuxing in yongshen['忌神']:
            score -= 15

        if dz_wuxing in yongshen['用神']:
            score += 15
        elif dz_wuxing in yongshen['喜神']:
            score += 8
        elif dz_wuxing in yongshen['忌神']:
            score -= 12

        # 检查与命局地支的冲合
        liunian_dizhi = liunian['地支']
        bazi_dizhi = self.parser.get_all_dizhi()

        special_notes = []

        # 六冲
        for dz in bazi_dizhi:
            if LIUCHONG.get(liunian_dizhi) == dz:
                score -= 5
                special_notes.append(f"流年{liunian_dizhi}冲命局{dz}")

        # 六合
        for dz in bazi_dizhi:
            if LIUHE.get(liunian_dizhi) == dz:
                score += 5
                special_notes.append(f"流年{liunian_dizhi}合命局{dz}")

        # 确定运势等级
        if score >= 70:
            level = '大吉'
        elif score >= 60:
            level = '中吉'
        elif score >= 50:
            level = '平运'
        elif score >= 40:
            level = '小凶'
        else:
            level = '凶运'

        # 获取十神
        tg_shishen = self._get_shishen(liunian['天干'])

        # 各方面运势
        aspects = self._analyze_liunian_aspects(liunian, yongshen)

        return {
            '流年': liunian['干支'],
            '年份': year,
            '年龄': liunian['年龄'],
            '天干十神': tg_shishen,
            '运势评分': score,
            '运势等级': level,
            '特殊注意': special_notes,
            '各方面运势': aspects
        }

    def _analyze_liunian_aspects(self, liunian: dict, yongshen: dict) -> dict:
        """分析流年各方面运势"""
        tg_wuxing = liunian['天干五行']
        tg_shishen = self._get_shishen(liunian['天干'])

        aspects = {
            '事业': '平稳',
            '财运': '平稳',
            '感情': '平稳',
            '健康': '平稳'
        }

        # 事业运（看官杀印）
        if tg_shishen in ['正官', '七杀']:
            if tg_wuxing in yongshen['用神'] + yongshen['喜神']:
                aspects['事业'] = '有升迁机会，事业发展顺利'
            else:
                aspects['事业'] = '工作压力大，注意职场人际'

        # 财运（看财星）
        if tg_shishen in ['正财', '偏财']:
            if tg_wuxing in yongshen['用神'] + yongshen['喜神']:
                aspects['财运'] = '财运亨通，可有意外收获'
            else:
                aspects['财运'] = '财运一般，不宜大额投资'

        # 感情运（男看财，女看官）
        if self.parser.gender == '男':
            if tg_shishen in ['正财', '偏财']:
                aspects['感情'] = '桃花运旺，感情有进展'
        else:
            if tg_shishen in ['正官', '七杀']:
                aspects['感情'] = '桃花运旺，可能遇到心仪对象'

        # 健康（看忌神和冲克）
        if tg_wuxing in yongshen['忌神']:
            aspects['健康'] = '注意身体健康，避免过度劳累'

        return aspects

    def display_analysis(self) -> str:
        """显示大运流年分析结果"""
        lines = []
        lines.append("=" * 60)
        lines.append("                  大 运 流 年 分 析")
        lines.append("=" * 60)
        lines.append("")

        # 大运排列方向
        direction = self._get_dayun_direction()
        dir_str = "顺排" if direction == 1 else "逆排"
        lines.append(f"【排运方向】: {dir_str}")
        lines.append("")

        # 大运列表
        lines.append("【十年大运一览】")
        lines.append("-" * 60)
        lines.append(f"{'序号':<4} {'大运':<6} {'年龄':<10} {'年份':<14} {'运势':<6} {'评分':<4}")
        lines.append("-" * 60)

        current_dayun = self.get_current_dayun()

        for dayun in self.dayun_list:
            analysis = self.analyze_dayun(dayun)
            is_current = dayun == current_dayun
            marker = ">>>" if is_current else "   "
            lines.append(
                f"{marker}{dayun['序号']:<3} {dayun['干支']:<6} "
                f"{analysis['年龄范围']:<10} {analysis['年份范围']:<14} "
                f"{analysis['运势等级']:<6} {analysis['运势评分']:<4}"
            )

        lines.append("-" * 60)

        # 当前大运详解
        if current_dayun:
            lines.append("")
            lines.append("【当前大运详解】")
            current_analysis = self.analyze_dayun(current_dayun)
            lines.append(f"  大运: {current_analysis['大运']}")
            lines.append(f"  年龄: {current_analysis['年龄范围']}")
            lines.append(f"  年份: {current_analysis['年份范围']}")
            lines.append(f"  天干十神: {current_analysis['天干十神']}")
            lines.append(f"  运势评分: {current_analysis['运势评分']}分")
            lines.append(f"  运势等级: {current_analysis['运势等级']}")
            lines.append(f"  运势描述: {current_analysis['运势描述']}")

        # 近几年流年分析
        lines.append("")
        lines.append("【近年流年运势】")
        lines.append("-" * 60)

        for year in range(self.current_year - 1, self.current_year + 5):
            liunian_analysis = self.analyze_liunian(year)
            is_current = year == self.current_year
            marker = ">>>" if is_current else "   "
            lines.append(
                f"{marker}{year}年({liunian_analysis['流年']}) "
                f"{liunian_analysis['年龄']}岁 - "
                f"{liunian_analysis['运势等级']} ({liunian_analysis['运势评分']}分)"
            )

            # 当前年份详细分析
            if is_current:
                lines.append(f"      天干十神: {liunian_analysis['天干十神']}")
                aspects = liunian_analysis['各方面运势']
                lines.append(f"      事业: {aspects['事业']}")
                lines.append(f"      财运: {aspects['财运']}")
                lines.append(f"      感情: {aspects['感情']}")
                lines.append(f"      健康: {aspects['健康']}")
                if liunian_analysis['特殊注意']:
                    lines.append(f"      注意: {', '.join(liunian_analysis['特殊注意'])}")

        lines.append("-" * 60)
        lines.append("=" * 60)
        return "\n".join(lines)
