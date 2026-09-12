#!/usr/bin/env python3
"""
八字命理推算系统 - 主程序
"""

import sys
sys.path.insert(0, '/home/user/-/bazi_fortune')

from modules.bazi_parser import BaziParser
from modules.wuxing_analyzer import WuxingAnalyzer
from modules.shishen_analyzer import ShishenAnalyzer
from modules.dayun_analyzer import DayunAnalyzer
from modules.report_generator import ReportGenerator


def analyze_bazi(bazi_str: str, gender: str, birth_year: int, current_year: int = 2026):
    """
    分析八字命理

    Args:
        bazi_str: 八字字符串，如 "庚辰 乙酉 癸酉 甲寅"
        gender: 性别 "男" 或 "女"
        birth_year: 出生年份
        current_year: 当前年份
    """
    print(f"\n正在分析八字: {bazi_str}")
    print(f"性别: {gender}, 出生年: {birth_year}年, 当前年: {current_year}年")
    print("-" * 60)

    # 1. 解析八字
    parser = BaziParser(bazi_str, gender, birth_year)

    # 2. 五行分析
    wuxing = WuxingAnalyzer(parser)

    # 3. 十神分析
    shishen = ShishenAnalyzer(parser)

    # 4. 大运流年分析
    dayun = DayunAnalyzer(parser, wuxing, current_year)

    # 5. 生成报告
    report = ReportGenerator(parser, wuxing, shishen, dayun)

    # 输出完整报告
    full_report = report.generate_full_report()
    print(full_report)

    return {
        'parser': parser,
        'wuxing': wuxing,
        'shishen': shishen,
        'dayun': dayun,
        'report': report
    }


if __name__ == "__main__":
    # 用户的八字信息
    # 庚辰 乙酉 癸酉 甲寅 男 2000年出生
    bazi = "庚辰 乙酉 癸酉 甲寅"
    gender = "男"
    birth_year = 2000
    current_year = 2026

    # 运行分析
    result = analyze_bazi(bazi, gender, birth_year, current_year)
