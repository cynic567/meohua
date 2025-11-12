#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梅花易数占卜程序 - 图形界面版本
Meihua Yishu Divination Program - GUI Version
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from meihua import MeihuaYishu
import datetime


class MeihuaGUI:
    """梅花易数图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("梅花易数占卜程序")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 创建梅花易数实例
        self.diviner = MeihuaYishu()
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        
        # 标题框架
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame,
            text="梅花易数占卜程序",
            font=("Arial", 20, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Meihua Yishu Divination System",
            font=("Arial", 10)
        )
        subtitle_label.pack()
        
        # 分隔线
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # 占卜类别选择框架
        category_frame = ttk.LabelFrame(self.root, text="选择占卜类别", padding="10")
        category_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 创建占卜类别单选按钮
        self.category_var = tk.IntVar(value=2)
        
        # 分三列显示
        categories = self.diviner.DIVINATION_CATEGORIES
        col_frame1 = ttk.Frame(category_frame)
        col_frame1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        col_frame2 = ttk.Frame(category_frame)
        col_frame2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        col_frame3 = ttk.Frame(category_frame)
        col_frame3.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        for i, (num, name) in enumerate(sorted(categories.items())):
            if i < 6:
                frame = col_frame1
            elif i < 12:
                frame = col_frame2
            else:
                frame = col_frame3
                
            rb = ttk.Radiobutton(
                frame,
                text=f"{num}. {name}",
                variable=self.category_var,
                value=num
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # 起卦方式选择框架
        method_frame = ttk.LabelFrame(self.root, text="起卦方式", padding="10")
        method_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.method_var = tk.BooleanVar(value=True)
        
        rb1 = ttk.Radiobutton(
            method_frame,
            text="时间+IP地址（推荐）",
            variable=self.method_var,
            value=True
        )
        rb1.pack(anchor=tk.W)
        
        rb2 = ttk.Radiobutton(
            method_frame,
            text="仅使用时间",
            variable=self.method_var,
            value=False
        )
        rb2.pack(anchor=tk.W)
        
        # 占卜按钮
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        divine_btn = ttk.Button(
            button_frame,
            text="开始占卜",
            command=self.perform_divination,
            style="Accent.TButton"
        )
        divine_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="清空结果",
            command=self.clear_results
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 结果显示框架
        result_frame = ttk.LabelFrame(self.root, text="占卜结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 使用滚动文本框显示结果
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Courier New", 10)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置文本标签样式
        self.result_text.tag_config("title", font=("Arial", 14, "bold"), foreground="blue")
        self.result_text.tag_config("header", font=("Arial", 12, "bold"), foreground="darkgreen")
        self.result_text.tag_config("label", font=("Arial", 10, "bold"))
        self.result_text.tag_config("symbol", font=("Arial", 16), foreground="red")
        
        # 状态栏
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(
            status_frame,
            text="就绪",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
        
    def perform_divination(self):
        """执行占卜"""
        try:
            # 更新状态
            self.status_label.config(text="正在占卜...")
            self.root.update()
            
            # 获取选择的类别和方式
            category = self.category_var.get()
            use_ip = self.method_var.get()
            
            # 执行占卜
            result = self.diviner.divine(category=category, use_ip=use_ip)
            
            # 显示结果
            self.display_result(result)
            
            # 更新状态
            self.status_label.config(text=f"占卜完成 - {result['时间']}")
            
        except Exception as e:
            messagebox.showerror("错误", f"占卜过程出错：{str(e)}")
            self.status_label.config(text="占卜失败")
    
    def display_result(self, result):
        """显示占卜结果"""
        # 清空现有内容
        self.result_text.delete(1.0, tk.END)
        
        # 标题
        self.result_text.insert(tk.END, "="*70 + "\n")
        self.result_text.insert(tk.END, "梅花易数占卜结果\n", "title")
        self.result_text.insert(tk.END, "="*70 + "\n\n")
        
        # 基本信息
        self.result_text.insert(tk.END, f"占卜时间：{result['时间']}\n")
        self.result_text.insert(tk.END, f"占卜类别：{result['占卜类别']}\n\n")
        
        # 本卦
        self.result_text.insert(tk.END, "【本卦】\n", "header")
        self.result_text.insert(tk.END, f"  上卦：{result['本卦']['上卦']}\n", "symbol")
        self.result_text.insert(tk.END, f"  下卦：{result['本卦']['下卦']}\n", "symbol")
        self.result_text.insert(tk.END, f"  卦名：", "label")
        self.result_text.insert(tk.END, f"{result['本卦']['卦名']}\n", "symbol")
        self.result_text.insert(tk.END, f"  动爻：{result['本卦']['动爻']}\n\n")
        
        # 变卦
        self.result_text.insert(tk.END, "【变卦】\n", "header")
        self.result_text.insert(tk.END, f"  上卦：{result['变卦']['上卦']}\n", "symbol")
        self.result_text.insert(tk.END, f"  下卦：{result['变卦']['下卦']}\n", "symbol")
        self.result_text.insert(tk.END, f"  卦名：", "label")
        self.result_text.insert(tk.END, f"{result['变卦']['卦名']}\n\n", "symbol")
        
        # 体用分析
        self.result_text.insert(tk.END, "【体用分析】\n", "header")
        self.result_text.insert(tk.END, f"  体卦：{result['体用']['体卦']}\n")
        self.result_text.insert(tk.END, f"  用卦：{result['体用']['用卦']}\n")
        self.result_text.insert(tk.END, f"  关系：", "label")
        self.result_text.insert(tk.END, f"{result['体用']['关系']}\n\n")
        
        # 卦辞解释
        self.result_text.insert(tk.END, "【卦辞解释】\n", "header")
        self.result_text.insert(tk.END, f"  {result['卦辞解释']}\n\n")
        
        self.result_text.insert(tk.END, "="*70 + "\n")
        
        # 滚动到顶部
        self.result_text.see(1.0)
    
    def clear_results(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        self.status_label.config(text="已清空结果")


def main():
    """主程序"""
    root = tk.Tk()
    app = MeihuaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
