"""
八字解析模块 - 解析四柱信息
"""

from .base_data import *


class BaziParser:
    """八字解析器"""

    def __init__(self, bazi_str: str, gender: str = '男', birth_year: int = 2000):
        """
        初始化八字解析器

        Args:
            bazi_str: 八字字符串，格式如 "庚辰 乙酉 癸酉 甲寅"
            gender: 性别 "男" 或 "女"
            birth_year: 出生年份
        """
        self.bazi_str = bazi_str
        self.gender = gender
        self.birth_year = birth_year
        self.pillars = self._parse_bazi(bazi_str)

    def _parse_bazi(self, bazi_str: str) -> dict:
        """解析八字字符串"""
        parts = bazi_str.replace('　', ' ').split()
        if len(parts) != 4:
            raise ValueError("八字格式错误，应为四柱，如：庚辰 乙酉 癸酉 甲寅")

        pillars = {
            '年柱': {'天干': parts[0][0], '地支': parts[0][1]},
            '月柱': {'天干': parts[1][0], '地支': parts[1][1]},
            '日柱': {'天干': parts[2][0], '地支': parts[2][1]},
            '时柱': {'天干': parts[3][0], '地支': parts[3][1]}
        }

        # 添加五行和阴阳属性
        for pillar_name, pillar in pillars.items():
            pillar['天干五行'] = TIANGAN_WUXING[pillar['天干']]
            pillar['地支五行'] = DIZHI_WUXING[pillar['地支']]
            pillar['天干阴阳'] = TIANGAN_YINYANG[pillar['天干']]
            pillar['地支阴阳'] = DIZHI_YINYANG[pillar['地支']]
            pillar['藏干'] = DIZHI_CANGGAN[pillar['地支']]

        return pillars

    def get_day_master(self) -> str:
        """获取日主（日干）"""
        return self.pillars['日柱']['天干']

    def get_day_master_wuxing(self) -> str:
        """获取日主五行"""
        return TIANGAN_WUXING[self.get_day_master()]

    def get_day_master_yinyang(self) -> str:
        """获取日主阴阳"""
        return TIANGAN_YINYANG[self.get_day_master()]

    def get_all_tiangan(self) -> list:
        """获取所有天干"""
        return [self.pillars[p]['天干'] for p in ['年柱', '月柱', '日柱', '时柱']]

    def get_all_dizhi(self) -> list:
        """获取所有地支"""
        return [self.pillars[p]['地支'] for p in ['年柱', '月柱', '日柱', '时柱']]

    def get_all_canggan(self) -> list:
        """获取所有藏干"""
        canggan = []
        for p in ['年柱', '月柱', '日柱', '时柱']:
            canggan.extend(self.pillars[p]['藏干'])
        return canggan

    def get_nayin(self, pillar: str) -> str:
        """获取纳音五行"""
        nayin_table = {
            '甲子': '海中金', '乙丑': '海中金', '丙寅': '炉中火', '丁卯': '炉中火',
            '戊辰': '大林木', '己巳': '大林木', '庚午': '路旁土', '辛未': '路旁土',
            '壬申': '剑锋金', '癸酉': '剑锋金', '甲戌': '山头火', '乙亥': '山头火',
            '丙子': '涧下水', '丁丑': '涧下水', '戊寅': '城头土', '己卯': '城头土',
            '庚辰': '白蜡金', '辛巳': '白蜡金', '壬午': '杨柳木', '癸未': '杨柳木',
            '甲申': '泉中水', '乙酉': '泉中水', '丙戌': '屋上土', '丁亥': '屋上土',
            '戊子': '霹雳火', '己丑': '霹雳火', '庚寅': '松柏木', '辛卯': '松柏木',
            '壬辰': '长流水', '癸巳': '长流水', '甲午': '砂石金', '乙未': '砂石金',
            '丙申': '山下火', '丁酉': '山下火', '戊戌': '平地木', '己亥': '平地木',
            '庚子': '壁上土', '辛丑': '壁上土', '壬寅': '金箔金', '癸卯': '金箔金',
            '甲辰': '覆灯火', '乙巳': '覆灯火', '丙午': '天河水', '丁未': '天河水',
            '戊申': '大驿土', '己酉': '大驿土', '庚戌': '钗钏金', '辛亥': '钗钏金',
            '壬子': '桑柘木', '癸丑': '桑柘木', '甲寅': '大溪水', '乙卯': '大溪水',
            '丙辰': '沙中土', '丁巳': '沙中土', '戊午': '天上火', '己未': '天上火',
            '庚申': '石榴木', '辛酉': '石榴木', '壬戌': '大海水', '癸亥': '大海水'
        }
        pillar_data = self.pillars[pillar]
        ganzhi = pillar_data['天干'] + pillar_data['地支']
        return nayin_table.get(ganzhi, '未知')

    def get_changsheng(self, tiangan: str, dizhi: str) -> str:
        """获取天干在地支的十二长生状态"""
        start_dizhi = CHANGSHENG_START.get(tiangan)
        if not start_dizhi:
            return '未知'

        start_idx = DIZHI.index(start_dizhi)
        current_idx = DIZHI.index(dizhi)

        # 阳干顺行，阴干逆行
        if TIANGAN_YINYANG[tiangan] == '阳':
            diff = (current_idx - start_idx) % 12
        else:
            diff = (start_idx - current_idx) % 12

        return CHANGSHENG_ORDER[diff]

    def get_day_master_changsheng(self) -> dict:
        """获取日主在四柱地支的长生状态"""
        day_master = self.get_day_master()
        result = {}
        for pillar_name in ['年柱', '月柱', '日柱', '时柱']:
            dizhi = self.pillars[pillar_name]['地支']
            result[pillar_name] = self.get_changsheng(day_master, dizhi)
        return result

    def check_shensha(self) -> dict:
        """检查神煞"""
        result = {
            '天乙贵人': [],
            '文昌': [],
            '驿马': [],
            '桃花': []
        }

        day_master = self.get_day_master()
        all_dizhi = self.get_all_dizhi()
        year_dizhi = self.pillars['年柱']['地支']

        # 天乙贵人
        if day_master in SHENSHA['天乙贵人']:
            guiren_dizhi = SHENSHA['天乙贵人'][day_master]
            for dz in all_dizhi:
                if dz in guiren_dizhi:
                    result['天乙贵人'].append(dz)

        # 文昌
        if day_master in SHENSHA['文昌']:
            wenchang_dizhi = SHENSHA['文昌'][day_master]
            for dz in all_dizhi:
                if dz == wenchang_dizhi:
                    result['文昌'].append(dz)

        # 驿马和桃花（以年支查）
        for sanhe_group, yima_dizhi in SHENSHA['驿马'].items():
            if year_dizhi in sanhe_group:
                for dz in all_dizhi:
                    if dz == yima_dizhi:
                        result['驿马'].append(dz)
                break

        for sanhe_group, taohua_dizhi in SHENSHA['桃花'].items():
            if year_dizhi in sanhe_group:
                for dz in all_dizhi:
                    if dz == taohua_dizhi:
                        result['桃花'].append(dz)
                break

        return result

    def check_combinations(self) -> dict:
        """检查地支合冲刑害"""
        all_dizhi = self.get_all_dizhi()
        result = {
            '六合': [],
            '三合': [],
            '六冲': [],
            '六害': [],
            '三刑': []
        }

        # 检查六合
        for i, dz1 in enumerate(all_dizhi):
            for j, dz2 in enumerate(all_dizhi[i+1:], i+1):
                if LIUHE.get(dz1) == dz2:
                    result['六合'].append(f"{dz1}-{dz2}")

        # 检查三合
        for sanhe_group, element in SANHE.items():
            count = sum(1 for dz in all_dizhi if dz in sanhe_group)
            if count >= 3:
                result['三合'].append(f"{sanhe_group}合{element}")
            elif count == 2:
                # 半合
                present = [dz for dz in all_dizhi if dz in sanhe_group]
                result['三合'].append(f"{''.join(present)}半合{element}")

        # 检查六冲
        for i, dz1 in enumerate(all_dizhi):
            for j, dz2 in enumerate(all_dizhi[i+1:], i+1):
                if LIUCHONG.get(dz1) == dz2:
                    result['六冲'].append(f"{dz1}-{dz2}相冲")

        # 检查六害
        for i, dz1 in enumerate(all_dizhi):
            for j, dz2 in enumerate(all_dizhi[i+1:], i+1):
                if LIUHAI.get(dz1) == dz2:
                    result['六害'].append(f"{dz1}-{dz2}相害")

        # 检查三刑
        for dz in all_dizhi:
            if dz in ['辰', '午', '酉', '亥'] and all_dizhi.count(dz) >= 2:
                result['三刑'].append(f"{dz}自刑")

        return result

    def display_bazi(self) -> str:
        """显示八字排盘"""
        lines = []
        lines.append("=" * 60)
        lines.append("                    八 字 排 盘")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"        年柱      月柱      日柱      时柱")
        lines.append(f"        ----      ----      ----      ----")

        # 天干行
        tiangan_line = "天干:   "
        for p in ['年柱', '月柱', '日柱', '时柱']:
            tg = self.pillars[p]['天干']
            wx = self.pillars[p]['天干五行']
            yy = self.pillars[p]['天干阴阳']
            tiangan_line += f"{tg}({wx}{yy})  "
        lines.append(tiangan_line)

        # 地支行
        dizhi_line = "地支:   "
        for p in ['年柱', '月柱', '日柱', '时柱']:
            dz = self.pillars[p]['地支']
            wx = self.pillars[p]['地支五行']
            dizhi_line += f"{dz}({wx})    "
        lines.append(dizhi_line)

        # 藏干行
        lines.append("")
        lines.append("藏干:")
        for p in ['年柱', '月柱', '日柱', '时柱']:
            canggan = self.pillars[p]['藏干']
            canggan_str = ', '.join([f"{cg}({TIANGAN_WUXING[cg]})" for cg in canggan])
            lines.append(f"  {p}: {canggan_str}")

        # 纳音
        lines.append("")
        lines.append("纳音:")
        for p in ['年柱', '月柱', '日柱', '时柱']:
            lines.append(f"  {p}: {self.get_nayin(p)}")

        lines.append("")
        lines.append(f"日主: {self.get_day_master()} ({self.get_day_master_wuxing()}{self.get_day_master_yinyang()})")
        lines.append(f"性别: {self.gender}")
        lines.append(f"出生年: {self.birth_year}年")
        lines.append("=" * 60)

        return "\n".join(lines)
