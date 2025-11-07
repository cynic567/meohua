#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梅花易数占卜程序 (Meihua Yishu Divination Program)
依据梅花易数理论进行占卜
"""

import datetime
import socket
import hashlib
from typing import Tuple, Dict, Any


class MeihuaYishu:
    """梅花易数占卜系统"""
    
    # 先天八卦数 (Prior Heaven Trigram Numbers)
    # 乾一，兑二，离三，震四，巽五，坎六，艮七，坤八
    TRIGRAM_NAMES = {
        1: "乾", 2: "兑", 3: "离", 4: "震",
        5: "巽", 6: "坎", 7: "艮", 8: "坤"
    }
    
    # 八卦符号
    TRIGRAM_SYMBOLS = {
        1: "☰", 2: "☱", 3: "☲", 4: "☳",
        5: "☴", 6: "☵", 7: "☶", 8: "☷"
    }
    
    # 八卦五行属性
    TRIGRAM_ELEMENTS = {
        1: "金", 2: "金", 3: "火", 4: "木",
        5: "木", 6: "水", 7: "土", 8: "土"
    }
    
    # 八卦基本含义
    TRIGRAM_MEANINGS = {
        1: "乾为天，五行属金，代表天、金属",
        2: "兑为泽，五行属金，代表沼泽、水性物、金属",
        3: "离为火，五行属火，代表火、火性物",
        4: "震为雷，五行属木，代表雷、树木、大木",
        5: "巽为风，五行属木，代表风、草藤、小木",
        6: "坎为水，五行属水，代表水、流动性物",
        7: "艮为山，五行属土，代表山、土性物",
        8: "坤为地，五行属土，代表地、大地、土性物"
    }
    
    # 六十四卦名称 (上卦索引 * 10 + 下卦索引)
    HEXAGRAM_NAMES = {
        11: "乾为天", 12: "天泽履", 13: "天火同人", 14: "天雷无妄",
        15: "天风姤", 16: "天水讼", 17: "天山遯", 18: "天地否",
        21: "泽天夬", 22: "兑为泽", 23: "泽火革", 24: "泽雷随",
        25: "泽风大过", 26: "泽水困", 27: "泽山咸", 28: "泽地萃",
        31: "火天大有", 32: "火泽睽", 33: "离为火", 34: "火雷噬嗑",
        35: "火风鼎", 36: "火水未济", 37: "火山旅", 38: "火地晋",
        41: "雷天大壮", 42: "雷泽归妹", 43: "雷火丰", 44: "震为雷",
        45: "雷风恒", 46: "雷水解", 47: "雷山小过", 48: "雷地豫",
        51: "风天小畜", 52: "风泽中孚", 53: "风火家人", 54: "风雷益",
        55: "巽为风", 56: "风水涣", 57: "风山渐", 58: "风地观",
        61: "水天需", 62: "水泽节", 63: "水火既济", 64: "水雷屯",
        65: "水风井", 66: "坎为水", 67: "水山蹇", 68: "水地比",
        71: "山天大畜", 72: "山泽损", 73: "山火贲", 74: "山雷颐",
        75: "山风蛊", 76: "山水蒙", 77: "艮为山", 78: "山地剥",
        81: "地天泰", 82: "地泽临", 83: "地火明夷", 84: "地雷复",
        85: "地风升", 86: "地水师", 87: "地山谦", 88: "坤为地"
    }
    
    # 五行相生 (Element Generation)
    ELEMENT_GENERATION = {
        "金": "水", "水": "木", "木": "火", "火": "土", "土": "金"
    }
    
    # 五行相克 (Element Restriction)
    ELEMENT_RESTRICTION = {
        "金": "木", "木": "土", "土": "水", "水": "火", "火": "金"
    }
    
    # 占卜类别
    DIVINATION_CATEGORIES = {
        1: "天时占",
        2: "人事占",
        3: "家宅占",
        4: "屋舍占",
        5: "婚姻占",
        6: "生产占",
        7: "饮食占",
        8: "求谋占",
        9: "求名占",
        10: "求财占",
        11: "交易占",
        12: "出行占",
        13: "行人占",
        14: "谒见占",
        15: "失物占",
        16: "疾病占",
        17: "官讼占",
        18: "坟墓占"
    }

    def __init__(self):
        self.upper_trigram = 0
        self.lower_trigram = 0
        self.moving_line = 0
        self.main_hexagram = None
        self.changed_hexagram = None
        self.mutual_hexagram = None
        
    def get_current_time_value(self) -> Tuple[int, int, int, int, int]:
        """获取当前农历时间值（简化版使用公历）
        返回: (年, 月, 日, 时辰, 时辰数)
        """
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        
        # 地支时辰对应 (简化处理)
        # 子(23-1)1, 丑(1-3)2, 寅(3-5)3, 卯(5-7)4, 辰(7-9)5, 巳(9-11)6,
        # 午(11-13)7, 未(13-15)8, 申(15-17)9, 酉(17-19)10, 戌(19-21)11, 亥(21-23)12
        hour_branch = ((hour + 1) // 2) % 12
        if hour_branch == 0:
            hour_branch = 12
            
        return year, month, day, hour, hour_branch
    
    def ip_to_number(self, ip: str = None) -> int:
        """将IP地址转换为数值
        使用哈希算法处理，然后对32取模
        """
        if ip is None:
            # 获取本机IP地址
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.connect(("8.8.8.8", 80))
                    ip = s.getsockname()[0]
            except (OSError, socket.error):
                ip = "127.0.0.1"
        
        # 使用SHA256哈希算法
        hash_value = hashlib.sha256(ip.encode()).hexdigest()
        # 取哈希值的前16位转为整数
        number = int(hash_value[:16], 16)
        # 对32取模得到1-32范围的值
        result = (number % 32) + 1
        
        return result
    
    def calculate_trigram(self, value: int) -> int:
        """计算卦象（除以8取余数）
        余数0视为8
        """
        remainder = value % 8
        return remainder if remainder != 0 else 8
    
    def calculate_moving_line(self, value: int) -> int:
        """计算动爻（除以6取余数）
        余数0视为6
        """
        remainder = value % 6
        return remainder if remainder != 0 else 6
    
    def generate_hexagram_by_time(self):
        """根据时间起卦"""
        year, month, day, hour, hour_num = self.get_current_time_value()
        
        # 上卦 = (年 + 月 + 日) ÷ 8，取余数
        upper_sum = year + month + day
        self.upper_trigram = self.calculate_trigram(upper_sum)
        
        # 下卦 = (年 + 月 + 日 + 时) ÷ 8，取余数
        lower_sum = year + month + day + hour_num
        self.lower_trigram = self.calculate_trigram(lower_sum)
        
        # 动爻 = (年 + 月 + 日 + 时) ÷ 6，取余数
        self.moving_line = self.calculate_moving_line(lower_sum)
        
        return self.upper_trigram, self.lower_trigram, self.moving_line
    
    def generate_hexagram_by_time_and_ip(self):
        """根据时间和IP地址起卦"""
        year, month, day, hour, hour_num = self.get_current_time_value()
        
        # 上卦使用时间
        upper_sum = year + month + day
        self.upper_trigram = self.calculate_trigram(upper_sum)
        
        # 下卦使用IP地址算法值
        ip_value = self.ip_to_number()
        self.lower_trigram = self.calculate_trigram(ip_value)
        
        # 动爻使用时间和IP的组合
        total_sum = upper_sum + ip_value
        self.moving_line = self.calculate_moving_line(total_sum)
        
        return self.upper_trigram, self.lower_trigram, self.moving_line
    
    def get_hexagram_name(self, upper: int, lower: int) -> str:
        """获取卦名"""
        key = upper * 10 + lower
        return self.HEXAGRAM_NAMES.get(key, f"{self.TRIGRAM_NAMES[upper]}{self.TRIGRAM_NAMES[lower]}")
    
    def get_changed_hexagram(self) -> Tuple[int, int]:
        """获取变卦（动爻变化后的卦）"""
        # 上卦和下卦的爻序
        # 下卦: 初爻(1), 二爻(2), 三爻(3)
        # 上卦: 四爻(4), 五爻(5), 上爻(6)
        
        upper = self.upper_trigram
        lower = self.lower_trigram
        
        if self.moving_line <= 3:
            # 动爻在下卦，下卦变化
            lower = self.change_trigram_line(lower, self.moving_line)
        else:
            # 动爻在上卦，上卦变化
            upper = self.change_trigram_line(upper, self.moving_line - 3)
        
        return upper, lower
    
    def change_trigram_line(self, trigram: int, line: int) -> int:
        """改变卦的某一爻"""
        # 八卦二进制表示（从下到上）
        # 乾111, 兑011, 离101, 震001, 巽110, 坎010, 艮100, 坤000
        trigram_binary = {
            1: 0b111, 2: 0b011, 3: 0b101, 4: 0b001,
            5: 0b110, 6: 0b010, 7: 0b100, 8: 0b000
        }
        binary_to_trigram = {v: k for k, v in trigram_binary.items()}
        
        binary = trigram_binary[trigram]
        # 改变指定位（从1开始，从下往上）
        binary ^= (1 << (line - 1))
        
        return binary_to_trigram[binary]
    
    def get_mutual_hexagram(self) -> Tuple[int, int]:
        """获取互卦"""
        # 互卦取本卦的2、3、4爻为下卦，3、4、5爻为上卦
        # 这里简化处理，根据主卦的五行属性推导
        # 实际应该根据六爻的具体情况计算
        
        # 简化版本：使用主卦的变化
        upper_element = self.TRIGRAM_ELEMENTS[self.upper_trigram]
        lower_element = self.TRIGRAM_ELEMENTS[self.lower_trigram]
        
        # 根据五行生成关系推导互卦
        mutual_upper = self.upper_trigram
        mutual_lower = self.lower_trigram
        
        # 简化处理，这里可以根据更复杂的规则计算
        return mutual_upper, mutual_lower
    
    def analyze_body_use(self) -> Dict[str, Any]:
        """分析体用关系"""
        # 动爻所在的卦为用卦，另一卦为体卦
        if self.moving_line <= 3:
            body_trigram = self.upper_trigram
            use_trigram = self.lower_trigram
        else:
            body_trigram = self.lower_trigram
            use_trigram = self.upper_trigram
        
        body_element = self.TRIGRAM_ELEMENTS[body_trigram]
        use_element = self.TRIGRAM_ELEMENTS[use_trigram]
        
        # 判断五行关系
        relationship = self.get_element_relationship(body_element, use_element)
        
        return {
            "body_trigram": body_trigram,
            "body_name": self.TRIGRAM_NAMES[body_trigram],
            "body_element": body_element,
            "use_trigram": use_trigram,
            "use_name": self.TRIGRAM_NAMES[use_trigram],
            "use_element": use_element,
            "relationship": relationship
        }
    
    def get_element_relationship(self, body: str, use: str) -> str:
        """判断体用五行关系"""
        if body == use:
            return "比和"
        elif self.ELEMENT_GENERATION.get(use) == body:
            return "用生体"
        elif self.ELEMENT_GENERATION.get(body) == use:
            return "体生用"
        elif self.ELEMENT_RESTRICTION.get(body) == use:
            return "体克用"
        elif self.ELEMENT_RESTRICTION.get(use) == body:
            return "用克体"
        else:
            return "无关系"
    
    def interpret_divination(self, category: int) -> str:
        """根据类别解卦"""
        body_use = self.analyze_body_use()
        relationship = body_use["relationship"]
        
        # 基础解释
        interpretations = {
            "比和": "吉利，事情顺遂",
            "用生体": "大吉，有进益之喜",
            "体生用": "不利，有耗损之患",
            "体克用": "可成，但较迟缓",
            "用克体": "凶，不宜进行"
        }
        
        base_interpretation = interpretations.get(relationship, "需详细分析")
        
        # 根据不同类别添加具体解释
        category_name = self.DIVINATION_CATEGORIES.get(category, "未知")
        
        specific_interpretations = {
            2: {  # 人事占
                "比和": "谋为吉利，事情顺遂",
                "用生体": "有进益之喜，贵人相助",
                "体生用": "有耗失之患，需谨慎行事",
                "体克用": "事可成但需时日",
                "用克体": "诸事不宜，需等待时机"
            },
            5: {  # 婚姻占
                "比和": "婚姻吉利，良配佳偶",
                "用生体": "婚易成，因婚有得",
                "体生用": "婚难成，因婚有失",
                "体克用": "可成但成之迟",
                "用克体": "不可成，成亦有害"
            },
            10: {  # 求财占
                "比和": "求财顺利，利快意",
                "用生体": "有财，且有进益之喜",
                "体生用": "无财，且有损耗之忧",
                "体克用": "有财但得财较迟",
                "用克体": "无财，不宜求财"
            },
            16: {  # 疾病占
                "比和": "疾病易安",
                "用生体": "病即愈",
                "体生用": "病难愈，迁延难好",
                "体克用": "病易安，勿药有喜",
                "用克体": "虽药无功，需谨慎"
            }
        }
        
        if category in specific_interpretations:
            specific = specific_interpretations[category].get(relationship, base_interpretation)
        else:
            specific = base_interpretation
        
        return f"{category_name}：{specific}"
    
    def divine(self, category: int = 2, use_ip: bool = True) -> Dict:
        """执行占卜
        
        Args:
            category: 占卜类别
            use_ip: 是否使用IP算法（True使用IP，False仅使用时间）
        """
        if use_ip:
            self.generate_hexagram_by_time_and_ip()
        else:
            self.generate_hexagram_by_time()
        
        # 获取变卦
        changed_upper, changed_lower = self.get_changed_hexagram()
        
        # 获取互卦
        mutual_upper, mutual_lower = self.get_mutual_hexagram()
        
        # 体用分析
        body_use = self.analyze_body_use()
        
        # 解卦
        interpretation = self.interpret_divination(category)
        
        # 返回完整结果
        result = {
            "时间": datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S"),
            "占卜类别": self.DIVINATION_CATEGORIES.get(category, "未知"),
            "本卦": {
                "上卦": f"{self.TRIGRAM_NAMES[self.upper_trigram]}{self.TRIGRAM_SYMBOLS[self.upper_trigram]}",
                "下卦": f"{self.TRIGRAM_NAMES[self.lower_trigram]}{self.TRIGRAM_SYMBOLS[self.lower_trigram]}",
                "卦名": self.get_hexagram_name(self.upper_trigram, self.lower_trigram),
                "动爻": f"第{self.moving_line}爻"
            },
            "变卦": {
                "上卦": f"{self.TRIGRAM_NAMES[changed_upper]}{self.TRIGRAM_SYMBOLS[changed_upper]}",
                "下卦": f"{self.TRIGRAM_NAMES[changed_lower]}{self.TRIGRAM_SYMBOLS[changed_lower]}",
                "卦名": self.get_hexagram_name(changed_upper, changed_lower)
            },
            "体用": {
                "体卦": f"{body_use['body_name']}（{body_use['body_element']}）",
                "用卦": f"{body_use['use_name']}（{body_use['use_element']}）",
                "关系": body_use['relationship']
            },
            "卦辞解释": interpretation
        }
        
        return result
    
    def print_result(self, result: Dict):
        """打印占卜结果"""
        print("\n" + "="*50)
        print("梅花易数占卜结果".center(46))
        print("="*50)
        print(f"\n占卜时间：{result['时间']}")
        print(f"占卜类别：{result['占卜类别']}")
        print("\n【本卦】")
        print(f"  上卦：{result['本卦']['上卦']}")
        print(f"  下卦：{result['本卦']['下卦']}")
        print(f"  卦名：{result['本卦']['卦名']}")
        print(f"  动爻：{result['本卦']['动爻']}")
        print("\n【变卦】")
        print(f"  上卦：{result['变卦']['上卦']}")
        print(f"  下卦：{result['变卦']['下卦']}")
        print(f"  卦名：{result['变卦']['卦名']}")
        print("\n【体用分析】")
        print(f"  体卦：{result['体用']['体卦']}")
        print(f"  用卦：{result['体用']['用卦']}")
        print(f"  关系：{result['体用']['关系']}")
        print("\n【卦辞解释】")
        print(f"  {result['卦辞解释']}")
        print("\n" + "="*50 + "\n")


def main():
    """主程序"""
    print("="*50)
    print("梅花易数占卜程序".center(46))
    print("="*50)
    print("\n占卜类别：")
    
    categories = MeihuaYishu.DIVINATION_CATEGORIES
    for i in range(1, 19, 2):
        left = f"{i}. {categories[i]}"
        right = f"{i+1}. {categories.get(i+1, '')}" if i+1 in categories else ""
        print(f"  {left:20s}  {right}")
    
    print("\n请输入占卜类别编号 (1-18)，直接回车默认为人事占：", end="")
    try:
        choice = input().strip()
        category = int(choice) if choice else 2
        if category not in categories:
            print("无效的类别，使用默认类别：人事占")
            category = 2
    except ValueError:
        print("输入无效，使用默认类别：人事占")
        category = 2
    
    # 创建占卜实例并执行
    diviner = MeihuaYishu()
    result = diviner.divine(category=category, use_ip=True)
    diviner.print_result(result)


if __name__ == "__main__":
    main()
