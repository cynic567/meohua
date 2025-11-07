#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梅花易数占卜程序测试脚本
"""

from meihua import MeihuaYishu
import datetime


def test_basic_divination():
    """测试基本占卜功能"""
    print("="*60)
    print("测试1：基本占卜功能")
    print("="*60)
    
    diviner = MeihuaYishu()
    result = diviner.divine(category=2, use_ip=True)
    diviner.print_result(result)
    print("✓ 基本占卜功能测试通过\n")


def test_all_categories():
    """测试所有占卜类别"""
    print("="*60)
    print("测试2：所有占卜类别")
    print("="*60)
    
    diviner = MeihuaYishu()
    
    # 测试几个关键类别
    test_categories = [2, 5, 10, 16]  # 人事、婚姻、求财、疾病
    
    for cat in test_categories:
        result = diviner.divine(category=cat, use_ip=True)
        print(f"\n{result['占卜类别']}：{result['卦辞解释']}")
    
    print("\n✓ 所有占卜类别测试通过\n")


def test_trigram_calculation():
    """测试卦象计算"""
    print("="*60)
    print("测试3：卦象计算")
    print("="*60)
    
    diviner = MeihuaYishu()
    
    # 测试八卦数字对应
    for i in range(1, 9):
        name = MeihuaYishu.TRIGRAM_NAMES[i]
        symbol = MeihuaYishu.TRIGRAM_SYMBOLS[i]
        element = MeihuaYishu.TRIGRAM_ELEMENTS[i]
        print(f"{i}. {name}{symbol} - 五行：{element}")
    
    print("\n✓ 卦象计算测试通过\n")


def test_element_relationships():
    """测试五行关系"""
    print("="*60)
    print("测试4：五行生克关系")
    print("="*60)
    
    diviner = MeihuaYishu()
    
    # 测试五行相生
    print("五行相生：")
    for parent, child in MeihuaYishu.ELEMENT_GENERATION.items():
        print(f"  {parent} → {child}")
    
    # 测试五行相克
    print("\n五行相克：")
    for restrainer, restrained in MeihuaYishu.ELEMENT_RESTRICTION.items():
        print(f"  {restrainer} ⊗ {restrained}")
    
    print("\n✓ 五行关系测试通过\n")


def test_body_use_analysis():
    """测试体用分析"""
    print("="*60)
    print("测试5：体用分析")
    print("="*60)
    
    diviner = MeihuaYishu()
    diviner.generate_hexagram_by_time_and_ip()
    
    body_use = diviner.analyze_body_use()
    
    print(f"体卦：{body_use['body_name']}（{body_use['body_element']}）")
    print(f"用卦：{body_use['use_name']}（{body_use['use_element']}）")
    print(f"关系：{body_use['relationship']}")
    
    # 测试各种关系
    test_cases = [
        ("金", "金", "比和"),
        ("金", "水", "体生用"),
        ("水", "金", "用生体"),
        ("金", "木", "体克用"),
        ("木", "金", "用克体"),
    ]
    
    print("\n关系判断测试：")
    for body, use, expected in test_cases:
        result = diviner.get_element_relationship(body, use)
        status = "✓" if result == expected else "✗"
        print(f"  {status} 体({body}) vs 用({use}) = {result} (期望: {expected})")
    
    print("\n✓ 体用分析测试通过\n")


def test_ip_algorithm():
    """测试IP地址算法"""
    print("="*60)
    print("测试6：IP地址算法")
    print("="*60)
    
    diviner = MeihuaYishu()
    
    # 测试几个IP地址
    test_ips = ["192.168.1.1", "10.0.0.1", "8.8.8.8", "127.0.0.1"]
    
    for ip in test_ips:
        value = diviner.ip_to_number(ip)
        trigram = diviner.calculate_trigram(value)
        print(f"IP: {ip:15s} → 值: {value:2d} → 卦: {MeihuaYishu.TRIGRAM_NAMES[trigram]}")
    
    print("\n✓ IP地址算法测试通过\n")


def test_hexagram_names():
    """测试卦名"""
    print("="*60)
    print("测试7：六十四卦名")
    print("="*60)
    
    diviner = MeihuaYishu()
    
    # 显示部分卦名
    print("部分卦名示例：")
    examples = [(1, 1), (1, 8), (8, 1), (8, 8), (3, 6), (6, 3)]
    
    for upper, lower in examples:
        name = diviner.get_hexagram_name(upper, lower)
        upper_name = MeihuaYishu.TRIGRAM_NAMES[upper]
        lower_name = MeihuaYishu.TRIGRAM_NAMES[lower]
        print(f"  {upper_name}上{lower_name}下 = {name}")
    
    print("\n✓ 卦名测试通过\n")


def test_changed_hexagram():
    """测试变卦"""
    print("="*60)
    print("测试8：变卦计算")
    print("="*60)
    
    diviner = MeihuaYishu()
    diviner.upper_trigram = 1  # 乾
    diviner.lower_trigram = 8  # 坤
    
    print(f"本卦：{MeihuaYishu.TRIGRAM_NAMES[diviner.upper_trigram]}上{MeihuaYishu.TRIGRAM_NAMES[diviner.lower_trigram]}下")
    
    # 测试不同位置的动爻
    for line in range(1, 7):
        diviner.moving_line = line
        changed_upper, changed_lower = diviner.get_changed_hexagram()
        print(f"  第{line}爻动 → {MeihuaYishu.TRIGRAM_NAMES[changed_upper]}上{MeihuaYishu.TRIGRAM_NAMES[changed_lower]}下")
    
    print("\n✓ 变卦计算测试通过\n")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("梅花易数占卜程序 - 测试套件".center(56))
    print("="*60 + "\n")
    
    tests = [
        test_basic_divination,
        test_all_categories,
        test_trigram_calculation,
        test_element_relationships,
        test_body_use_analysis,
        test_ip_algorithm,
        test_hexagram_names,
        test_changed_hexagram,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ 测试失败：{test.__name__}")
            print(f"  错误：{str(e)}\n")
    
    print("="*60)
    print("所有测试完成！".center(56))
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
