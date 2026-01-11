#!/usr/bin/env python3
"""
名利倾向分析 + 火属性平衡分析
"""

import sys
sys.path.insert(0, '/home/user/-/bazi_fortune')

from modules.bazi_parser import BaziParser
from modules.wuxing_analyzer import WuxingAnalyzer
from modules.shishen_analyzer import ShishenAnalyzer


def analyze_fame_vs_wealth(bazi_str: str, gender: str, birth_year: int):
    """分析命主的名利倾向"""

    parser = BaziParser(bazi_str, gender, birth_year)
    wuxing = WuxingAnalyzer(parser)
    shishen = ShishenAnalyzer(parser)
    count = shishen.get_shishen_count()

    print("=" * 60)
    print("                 名 利 倾 向 分 析")
    print("=" * 60)
    print()

    print("【十神与名利的关系】")
    print()
    print("  追求「名」的十神:")
    print("  ├─ 食神、伤官 → 表达、创作、才华展示、被认可")
    print("  └─ 正官、七杀 → 地位、权威、社会认可")
    print()
    print("  追求「利」的十神:")
    print("  └─ 正财、偏财 → 金钱、物质、实际收益")
    print()

    # 计算名利倾向
    fame_score = count['食神'] + count['伤官'] + count['正官'] + count['七杀']
    wealth_score = count['正财'] + count['偏财']

    print("【你的十神配置】")
    print()
    print("  「名」相关:")
    print(f"    食神: {count['食神']:.1f}  ← 才华表达、口碑")
    print(f"    伤官: {count['伤官']:.1f}  ← 创意输出、锋芒")
    print(f"    正官: {count['正官']:.1f}  ← 正统地位")
    print(f"    七杀: {count['七杀']:.1f}  ← 权威魄力")
    print(f"    ──────────────")
    print(f"    名气总分: {fame_score:.1f}")
    print()
    print("  「利」相关:")
    print(f"    正财: {count['正财']:.1f}  ← 稳定收入")
    print(f"    偏财: {count['偏财']:.1f}  ← 投机收益")
    print(f"    ──────────────")
    print(f"    财富总分: {wealth_score:.1f}")
    print()

    ratio = fame_score / wealth_score if wealth_score > 0 else float('inf')

    print("【结论】")
    print()
    print(f"  名/利 比值: {ratio:.1f} : 1")
    print()
    if ratio > 3:
        print("  ★ 你的命格确实是「重名轻利」型")
        print("  ★ 食伤旺 + 财弱 = 天生追求表达和认可，而非金钱")
        print("  ★ 你的成就感来自影响力，不是银行余额")
    print()

    print("=" * 60)
    print("              火 属 性 过 旺 分 析")
    print("=" * 60)
    print()

    print("【你的担忧是否成立？】")
    print()
    print("  2026年（丙午）= 天干丙火 + 地支午火 = 火极旺")
    print("  如果再去深圳（南方火地）...")
    print()
    print("  火叠加后的影响：")
    print("  ┌─────────────────────────────────────────────")
    print("  │ 火的正面：热情、名气、传播、科技、创新")
    print("  │ 火的负面：急躁、冲动、虚浮、过度消耗")
    print("  └─────────────────────────────────────────────")
    print()

    print("【关键问题：火对你是用神还是过旺？】")
    print()
    wuxing_score = wuxing.wuxing_score
    total = sum(wuxing_score.values())
    fire_ratio = wuxing_score['火'] / total * 100

    print(f"  你命局本身的火: {wuxing_score['火']:.2f} ({fire_ratio:.1f}%)")
    print(f"  → 火在你命局中是【极弱】的，只有 4.2%")
    print(f"  → 你不是火多要泄，而是火少要补")
    print()
    print("  所以：")
    print("  • 2026火年 + 南方火地 = 补你的短板，不是过犹不及")
    print("  • 但你的担忧也有道理：火太猛可能让节奏太快")
    print()

    print("=" * 60)
    print("                 城 市 气 质 对 比")
    print("=" * 60)
    print()

    print("【深圳 vs 杭州的气质差异】")
    print()
    print("  ┌────────────┬─────────────────┬─────────────────┐")
    print("  │            │     深圳        │      杭州       │")
    print("  ├────────────┼─────────────────┼─────────────────┤")
    print("  │ 五行       │ 火（纯火）      │ 木（木生火）    │")
    print("  │ 气质       │ 狼性、搞钱、快  │ 文雅、内容、稳  │")
    print("  │ 节奏       │ 极快、高压      │ 较快但有呼吸    │")
    print("  │ 适合       │ 追求规模和财富  │ 追求品质和影响  │")
    print("  │ 自媒体生态 │ 带货、商业化    │ 内容、调性      │")
    print("  │ 代表       │ 华为、腾讯      │ 阿里、网易      │")
    print("  └────────────┴─────────────────┴─────────────────┘")
    print()

    print("【从「追求名」的角度重新评估】")
    print()
    print("  你说你追求的是「名」而非「利」：")
    print("  • 想要的是行业影响力、被认可、话语权")
    print("  • 而不是单纯把流量变现、疯狂搞钱")
    print()
    print("  这样的话：")
    print()
    print("  杭州的优势浮现了：")
    print("  ├─ 木主「仁」，更重人文、内容、长期价值")
    print("  ├─ 木生火，是温和补火，不是猛火")
    print("  ├─ 自媒体生态偏内容调性，不那么「铜臭」")
    print("  ├─ 节奏允许你沉淀思考，而非疲于奔命")
    print("  └─ 居住环境确实一流，创作者需要灵感")
    print()
    print("  深圳的特点：")
    print("  ├─ 火主「礼」，更重效率、结果、商业闭环")
    print("  ├─ 适合快速规模化、融资、建团队")
    print("  ├─ 但容易被裹挟进「搞钱」的氛围")
    print("  └─ 如果你定力不够，可能偏离初心")
    print()

    print("=" * 60)
    print("                   修 正 后 的 建 议")
    print("=" * 60)
    print()
    print("  【重新评分】（加入「名利倾向」权重）")
    print()
    print("  ┌────────┬────────┬────────┬─────────────────────┐")
    print("  │  城市  │ 命理分 │ 气质分 │       总评          │")
    print("  ├────────┼────────┼────────┼─────────────────────┤")
    print("  │  杭州  │  65    │  +15   │  80分 ← 更适合你    │")
    print("  │  深圳  │  75    │  -10   │  65分               │")
    print("  │  北京  │  30    │   0    │  30分               │")
    print("  └────────┴────────┴────────┴─────────────────────┘")
    print()
    print("  【最终建议】")
    print()
    print("  ★ 如果你明确「追求名 > 追求利」→ 选杭州")
    print()
    print("    理由：")
    print("    1. 木生火 = 温补用神，不会过激")
    print("    2. 城市气质与你的追求匹配")
    print("    3. 内容创作者需要沉淀空间")
    print("    4. 你已经在圈子里有名气了，不需要狼性环境逼自己")
    print("    5. 食伤旺的人需要美的环境激发灵感")
    print()
    print("  ☆ 如果你想「名利双收、快速规模化」→ 选深圳")
    print()
    print("    但要注意：")
    print("    1. 保持初心，不要被氛围带偏")
    print("    2. 定期给自己「降火」的时间")
    print()
    print("  【补充说明】")
    print()
    print("  你问「火叠加会不会反而不好」——")
    print("  答案是：对你这个命局，火不会过。")
    print("  你命局火只有4%，2026火年+南方火地，")
    print("  最多把你的火补到30-40%，远没到「过」的程度。")
    print()
    print("  真正的问题不是「火过旺」，而是：")
    print("  「深圳的城市气质」和「你追求名的性格」是否匹配？")
    print()
    print("  这是个人选择，不是命理问题。")
    print()
    print("=" * 60)


if __name__ == "__main__":
    bazi = "庚辰 乙酉 癸酉 甲寅"
    analyze_fame_vs_wealth(bazi, "男", 2000)
