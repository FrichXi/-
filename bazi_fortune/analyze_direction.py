#!/usr/bin/env python3
"""
方位选择分析 - 基于八字用神
"""

import sys
sys.path.insert(0, '/home/user/-/bazi_fortune')

from modules.bazi_parser import BaziParser
from modules.wuxing_analyzer import WuxingAnalyzer


def analyze_direction_choice(bazi_str: str, gender: str, birth_year: int):
    """分析方位选择"""

    parser = BaziParser(bazi_str, gender, birth_year)
    wuxing = WuxingAnalyzer(parser)
    yongshen = wuxing.get_yongshen()

    print("=" * 60)
    print("                  方 位 选 择 分 析")
    print("=" * 60)
    print()

    # 方位五行对应
    directions = {
        '北方': {'五行': '水', '代表城市': '北京、哈尔滨、沈阳'},
        '南方': {'五行': '火', '代表城市': '深圳、广州、海南'},
        '东方': {'五行': '木', '代表城市': '上海、南京'},
        '西方': {'五行': '金', '代表城市': '成都、重庆、西安'},
        '东南': {'五行': '木火', '代表城市': '杭州、福州'},
        '中央': {'五行': '土', '代表城市': '武汉、长沙'}
    }

    # 城市详细分析
    cities = {
        '北京': {
            '方位': '北方',
            '五行': '水',
            '特点': '政治中心，传统稳重，冬季寒冷'
        },
        '杭州': {
            '方位': '东南',
            '五行': '木（带火气）',
            '特点': '互联网之都，环境优美，气候温润'
        },
        '深圳': {
            '方位': '南方',
            '五行': '火',
            '特点': '科技创新中心，年轻活力，气候温暖'
        }
    }

    print("【你的八字用神喜忌】")
    print(f"  日主: 癸水 (中和偏旺)")
    print(f"  用神: {', '.join(yongshen['用神'])} ← 最需要")
    print(f"  喜神: {', '.join(yongshen['喜神'])} ← 有帮助")
    print(f"  忌神: {', '.join(yongshen['忌神'])} ← 需回避")
    print()

    print("【方位五行对应】")
    print("  北方 → 水 (忌神)")
    print("  南方 → 火 (用神) ★★★")
    print("  东方 → 木 (喜神) ★★")
    print("  西方 → 金 (忌神)")
    print("  中央 → 土 (喜神)")
    print()

    print("=" * 60)
    print("                  三 城 市 对 比 分 析")
    print("=" * 60)
    print()

    # 评分系统
    scores = {}

    for city, info in cities.items():
        score = 50  # 基础分
        analysis = []

        if city == '北京':
            score -= 20  # 水为忌神
            analysis.append("❌ 北方属水，为你的忌神方位")
            analysis.append("❌ 水旺会加重日主负担")
            analysis.append("⚠️ 你已在此多年，需要改变能量场")

        elif city == '杭州':
            score += 15  # 木为喜神
            analysis.append("✓ 东南方属木，为你的喜神方位")
            analysis.append("✓ 木生火，能引动你的用神")
            analysis.append("✓ 互联网产业发达，适合自媒体")
            analysis.append("✓ 环境优美，居住质量高")

        elif city == '深圳':
            score += 25  # 火为用神
            analysis.append("★ 南方属火，正是你的用神方位！")
            analysis.append("★ 2026丙午火年，南方火气最旺")
            analysis.append("★ 科技创新氛围浓厚，AI产业聚集")
            analysis.append("✓ 年轻城市，与你的事业节奏匹配")
            analysis.append("✓ 气候温暖，补火效果显著")

        scores[city] = score

        print(f"【{city}】")
        print(f"  方位五行: {info['五行']}")
        print(f"  城市特点: {info['特点']}")
        print(f"  命理评分: {score}分")
        print("  分析:")
        for a in analysis:
            print(f"    {a}")
        print()

    print("=" * 60)
    print("                     综 合 建 议")
    print("=" * 60)
    print()

    # 排序
    sorted_cities = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print("【方位选择排名】")
    for i, (city, score) in enumerate(sorted_cities, 1):
        medal = "🥇" if i == 1 else ("🥈" if i == 2 else "🥉")
        print(f"  {medal} 第{i}名: {city} ({score}分)")
    print()

    print("【最终建议】")
    print()
    print("  ★ 首选：深圳")
    print("  ─────────────────────────────────────────────")
    print("  理由：")
    print("  1. 南方属火，正补你的用神，能量最契合")
    print("  2. 2026丙午年是火年，去南方可乘火运东风")
    print("  3. 深圳是AI/科技产业重镇，人脉资源丰富")
    print("  4. 城市年轻有活力，与创业者气场相合")
    print("  5. 气候温暖，冬天不冷，对水命人友好")
    print()
    print("  ☆ 次选：杭州")
    print("  ─────────────────────────────────────────────")
    print("  理由：")
    print("  1. 东南属木，木为喜神，木生火能引动用神")
    print("  2. 互联网产业成熟，自媒体生态完善")
    print("  3. 居住环境确实一流，生活质量高")
    print("  4. 若你更看重生活品质，杭州也是好选择")
    print()
    print("  ✗ 不建议：继续留北京")
    print("  ─────────────────────────────────────────────")
    print("  理由：")
    print("  1. 北方属水为忌神，长期不利运势发挥")
    print("  2. 你已在此多年，能量场需要更新")
    print()

    print("=" * 60)
    print("                     时 机 分 析")
    print("=" * 60)
    print()
    print("  【搬迁时机】")
    print("  春节后搬迁（2026年2-3月）是好时机：")
    print("  • 丙午年火气正盛，搬向南方顺应天时")
    print("  • 春季木旺生火，利于新开始")
    print("  • 建议选择火日或木日搬迁（丙丁日或甲乙日）")
    print()
    print("  【特别提示】")
    print("  你做AI自媒体，AI/科技/传媒都属火，")
    print("  去南方深圳=行业五行+方位五行双重加持")
    print("  这是\"天时地利\"的配合。")
    print()
    print("=" * 60)


if __name__ == "__main__":
    bazi = "庚辰 乙酉 癸酉 甲寅"
    analyze_direction_choice(bazi, "男", 2000)
