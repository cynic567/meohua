#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梅花易数程序使用示例
Examples of using the Meihua Yishu divination program
"""

from meihua import MeihuaYishu


def example_1_basic_usage():
    """示例1：基本使用"""
    print("\n示例1：基本使用 - 人事占卜")
    print("-" * 50)
    
    diviner = MeihuaYishu()
    result = diviner.divine(category=2, use_ip=True)
    diviner.print_result(result)


def example_2_marriage_divination():
    """示例2：婚姻占卜"""
    print("\n示例2：婚姻占卜")
    print("-" * 50)
    
    diviner = MeihuaYishu()
    result = diviner.divine(category=5, use_ip=True)
    diviner.print_result(result)


def example_3_wealth_divination():
    """示例3：求财占卜"""
    print("\n示例3：求财占卜")
    print("-" * 50)
    
    diviner = MeihuaYishu()
    result = diviner.divine(category=10, use_ip=True)
    diviner.print_result(result)


def example_4_access_result_data():
    """示例4：访问占卜结果数据"""
    print("\n示例4：程序化访问占卜结果")
    print("-" * 50)
    
    diviner = MeihuaYishu()
    result = diviner.divine(category=2, use_ip=True)
    
    # 访问结果的各个部分
    print(f"占卜时间：{result['时间']}")
    print(f"占卜类别：{result['占卜类别']}")
    print(f"\n本卦信息：")
    print(f"  卦名：{result['本卦']['卦名']}")
    print(f"  上卦：{result['本卦']['上卦']}")
    print(f"  下卦：{result['本卦']['下卦']}")
    print(f"  动爻：{result['本卦']['动爻']}")
    print(f"\n体用关系：")
    print(f"  体卦：{result['体用']['体卦']}")
    print(f"  用卦：{result['体用']['用卦']}")
    print(f"  关系：{result['体用']['关系']}")
    print(f"\n解释：{result['卦辞解释']}")


def example_5_manual_hexagram():
    """示例5：手动设置卦象进行分析"""
    print("\n示例5：手动设置卦象")
    print("-" * 50)
    
    diviner = MeihuaYishu()
    
    # 手动设置上卦、下卦、动爻
    diviner.upper_trigram = 1  # 乾
    diviner.lower_trigram = 8  # 坤
    diviner.moving_line = 3    # 第3爻动
    
    # 分析体用
    body_use = diviner.analyze_body_use()
    print(f"本卦：{MeihuaYishu.TRIGRAM_NAMES[diviner.upper_trigram]}上{MeihuaYishu.TRIGRAM_NAMES[diviner.lower_trigram]}下")
    print(f"动爻：第{diviner.moving_line}爻")
    print(f"体卦：{body_use['body_name']}（{body_use['body_element']}）")
    print(f"用卦：{body_use['use_name']}（{body_use['use_element']}）")
    print(f"关系：{body_use['relationship']}")
    
    # 获取变卦
    changed_upper, changed_lower = diviner.get_changed_hexagram()
    changed_name = diviner.get_hexagram_name(changed_upper, changed_lower)
    print(f"变卦：{changed_name}")


def example_6_batch_divination():
    """示例6：批量占卜"""
    print("\n示例6：批量占卜多个类别")
    print("-" * 50)
    
    diviner = MeihuaYishu()
    
    # 对多个类别进行占卜
    categories = [
        (2, "人事"),
        (5, "婚姻"),
        (10, "求财"),
        (12, "出行"),
        (16, "疾病")
    ]
    
    for cat_num, cat_name in categories:
        result = diviner.divine(category=cat_num, use_ip=True)
        print(f"\n{cat_name}占：")
        print(f"  本卦：{result['本卦']['卦名']}")
        print(f"  体用：{result['体用']['关系']}")
        print(f"  解释：{result['卦辞解释']}")


def example_7_element_analysis():
    """示例7：五行分析"""
    print("\n示例7：五行生克分析")
    print("-" * 50)
    
    diviner = MeihuaYishu()
    
    # 显示五行相生
    print("五行相生：")
    for parent, child in MeihuaYishu.ELEMENT_GENERATION.items():
        print(f"  {parent}生{child}")
    
    # 显示五行相克
    print("\n五行相克：")
    for restrainer, restrained in MeihuaYishu.ELEMENT_RESTRICTION.items():
        print(f"  {restrainer}克{restrained}")
    
    # 分析特定五行关系
    print("\n体用关系判断示例：")
    test_pairs = [
        ("金", "水", "体生用"),
        ("水", "火", "体克用"),
        ("火", "金", "体克用"),
        ("木", "金", "用克体"),
        ("土", "土", "比和"),
    ]
    
    for body, use, expected in test_pairs:
        result = diviner.get_element_relationship(body, use)
        print(f"  体卦({body}) vs 用卦({use}) → {result}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("梅花易数占卜程序使用示例".center(56))
    print("=" * 60)
    
    examples = [
        example_1_basic_usage,
        example_2_marriage_divination,
        example_3_wealth_divination,
        example_4_access_result_data,
        example_5_manual_hexagram,
        example_6_batch_divination,
        example_7_element_analysis,
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            example()
            print()
        except Exception as e:
            print(f"\n示例{i}执行失败：{str(e)}\n")
    
    print("=" * 60)
    print("所有示例运行完成".center(56))
    print("=" * 60)


if __name__ == "__main__":
    main()
