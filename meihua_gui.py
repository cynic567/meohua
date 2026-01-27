#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梅花易数占卜程序 - 图形界面版本（桌面应用）
Meihua Yishu Divination Program - Desktop GUI Version

这个版本使用本地Web服务器 + 浏览器应用模式，提供完整的桌面应用体验。
无需安装tkinter或PyQt等GUI库，只需要Python标准库。
"""

import http.server
import socketserver
import webbrowser
import threading
import os
import sys
import time
from urllib.parse import parse_qs, urlparse
import json
from meihua import MeihuaYishu


class MeihuaRequestHandler(http.server.SimpleHTTPRequestHandler):
    """处理HTTP请求的处理器"""
    
    def __init__(self, *args, **kwargs):
        # 设置工作目录
        self.directory = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, directory=self.directory, **kwargs)
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/divine':
            try:
                # 读取请求数据
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # 执行占卜
                diviner = MeihuaYishu()
                category = int(data.get('category', 2))
                use_ip = data.get('use_ip', True)
                result = diviner.divine(category=category, use_ip=use_ip)
                
                # 返回结果
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'result': result
                }, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': str(e)
                }, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        """静默日志输出"""
        pass


class MeihuaGUI:
    """梅花易数桌面应用"""
    
    def __init__(self, port=8888):
        self.port = port
        self.server = None
        self.server_thread = None
        self.directory = os.path.dirname(os.path.abspath(__file__))
        
        # 创建梅花易数实例
        self.diviner = MeihuaYishu()
    
    def create_html_interface(self):
        """创建HTML界面文件"""
        html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>梅花易数占卜程序</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            overflow-y: auto;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 8px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header p {
            font-size: 1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 25px;
        }
        
        .section {
            margin-bottom: 25px;
        }
        
        .section-title {
            font-size: 1.2em;
            color: #667eea;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #667eea;
        }
        
        .category-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 15px;
        }
        
        .category-item {
            display: flex;
            align-items: center;
            padding: 8px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9em;
        }
        
        .category-item:hover {
            border-color: #667eea;
            background: #f5f7ff;
        }
        
        .category-item input[type="radio"] {
            margin-right: 8px;
            cursor: pointer;
        }
        
        .category-item label {
            cursor: pointer;
            user-select: none;
            flex: 1;
        }
        
        .category-item.selected {
            border-color: #667eea;
            background: #f5f7ff;
            font-weight: bold;
        }
        
        .method-options {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .method-item {
            display: flex;
            align-items: center;
            padding: 12px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            flex: 1;
        }
        
        .method-item:hover {
            border-color: #667eea;
            background: #f5f7ff;
        }
        
        .method-item.selected {
            border-color: #667eea;
            background: #f5f7ff;
            font-weight: bold;
        }
        
        .method-item input[type="radio"] {
            margin-right: 10px;
            cursor: pointer;
        }
        
        .method-item label {
            cursor: pointer;
            user-select: none;
        }
        
        .button-group {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
        }
        
        .btn {
            padding: 12px 35px;
            font-size: 1em;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            flex: 1;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .result-container {
            background: #f9f9f9;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            min-height: 300px;
            max-height: 500px;
            overflow-y: auto;
        }
        
        .result-content {
            font-family: "Courier New", monospace;
            white-space: pre-wrap;
            line-height: 1.6;
            font-size: 0.95em;
        }
        
        .result-header {
            font-size: 1.2em;
            color: #667eea;
            font-weight: bold;
            margin-bottom: 12px;
        }
        
        .result-section {
            margin-bottom: 18px;
        }
        
        .result-section-title {
            font-size: 1.05em;
            color: #764ba2;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        .trigram-symbol {
            font-size: 1.4em;
            color: #d63031;
        }
        
        .hexagram-name {
            font-size: 1.2em;
            color: #e17055;
            font-weight: bold;
        }
        
        .interpretation {
            background: #fff3cd;
            padding: 12px;
            border-left: 4px solid #ffc107;
            margin-top: 8px;
        }
        
        .loading {
            text-align: center;
            padding: 35px;
            color: #999;
        }
        
        .empty-result {
            text-align: center;
            padding: 50px 20px;
            color: #999;
            font-size: 1em;
        }
        
        .footer {
            text-align: center;
            padding: 15px;
            color: #999;
            font-size: 0.85em;
            border-top: 1px solid #e0e0e0;
        }
        
        @media (max-width: 768px) {
            .category-grid {
                grid-template-columns: 1fr;
            }
            
            .method-options {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>梅花易数占卜程序</h1>
            <p>Meihua Yishu Divination System - Desktop Version</p>
        </div>
        
        <div class="content">
            <!-- 占卜类别选择 -->
            <div class="section">
                <div class="section-title">选择占卜类别</div>
                <div class="category-grid" id="categoryGrid"></div>
            </div>
            
            <!-- 起卦方式选择 -->
            <div class="section">
                <div class="section-title">起卦方式</div>
                <div class="method-options">
                    <div class="method-item selected" onclick="selectMethod(true)">
                        <input type="radio" name="method" id="method1" value="true" checked>
                        <label for="method1">时间+IP地址（推荐）</label>
                    </div>
                    <div class="method-item" onclick="selectMethod(false)">
                        <input type="radio" name="method" id="method2" value="false">
                        <label for="method2">仅使用时间</label>
                    </div>
                </div>
            </div>
            
            <!-- 操作按钮 -->
            <div class="section">
                <div class="button-group">
                    <button class="btn btn-primary" onclick="performDivination()">🔮 开始占卜</button>
                    <button class="btn btn-secondary" onclick="clearResults()">🗑️ 清空结果</button>
                </div>
            </div>
            
            <!-- 结果显示 -->
            <div class="section">
                <div class="section-title">占卜结果</div>
                <div class="result-container" id="resultContainer">
                    <div class="empty-result">
                        请选择占卜类别后点击"开始占卜"按钮
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            梅花易数占卜程序 © 2025 | 仅供娱乐和学习传统文化之用
        </div>
    </div>
    
    <script>
        const DIVINATION_CATEGORIES = {
            1: "天时占", 2: "人事占", 3: "家宅占", 4: "屋舍占",
            5: "婚姻占", 6: "生产占", 7: "饮食占", 8: "求谋占",
            9: "求名占", 10: "求财占", 11: "交易占", 12: "出行占",
            13: "行人占", 14: "谒见占", 15: "失物占", 16: "疾病占",
            17: "官讼占", 18: "坟墓占"
        };
        
        // 初始化界面
        function initCategories() {
            const grid = document.getElementById('categoryGrid');
            for (let num in DIVINATION_CATEGORIES) {
                const div = document.createElement('div');
                div.className = 'category-item';
                if (num == 2) div.classList.add('selected');
                div.onclick = () => selectCategory(num);
                
                div.innerHTML = `
                    <input type="radio" name="category" id="cat${num}" value="${num}" ${num == 2 ? 'checked' : ''}>
                    <label for="cat${num}">${num}. ${DIVINATION_CATEGORIES[num]}</label>
                `;
                grid.appendChild(div);
            }
        }
        
        function selectCategory(num) {
            document.querySelectorAll('.category-item').forEach(item => {
                item.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
            document.getElementById('cat' + num).checked = true;
        }
        
        function selectMethod(useIp) {
            document.querySelectorAll('.method-item').forEach(item => {
                item.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
            
            if (useIp) {
                document.getElementById('method1').checked = true;
            } else {
                document.getElementById('method2').checked = true;
            }
        }
        
        function performDivination() {
            const category = parseInt(document.querySelector('input[name="category"]:checked').value);
            const useIp = document.getElementById('method1').checked;
            
            const resultContainer = document.getElementById('resultContainer');
            resultContainer.innerHTML = '<div class="loading">正在占卜中，请稍候...</div>';
            
            fetch('/divine', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category: category,
                    use_ip: useIp
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displayResult(data.result);
                } else {
                    resultContainer.innerHTML = '<div class="empty-result">占卜失败：' + data.error + '</div>';
                }
            })
            .catch(error => {
                resultContainer.innerHTML = '<div class="empty-result">占卜失败：' + error + '</div>';
            });
        }
        
        function displayResult(result) {
            const resultContainer = document.getElementById('resultContainer');
            
            let html = '<div class="result-content">';
            html += '<div class="result-header">════════════════════════════════════════</div>';
            html += '<div class="result-header" style="text-align: center;">梅花易数占卜结果</div>';
            html += '<div class="result-header">════════════════════════════════════════</div>';
            html += '<br>';
            
            html += '<div><strong>占卜时间：</strong>' + result['时间'] + '</div>';
            html += '<div><strong>占卜类别：</strong>' + result['占卜类别'] + '</div>';
            html += '<br>';
            
            // 本卦
            html += '<div class="result-section">';
            html += '<div class="result-section-title">【本卦】</div>';
            html += '<div>　上卦：<span class="trigram-symbol">' + result['本卦']['上卦'] + '</span></div>';
            html += '<div>　下卦：<span class="trigram-symbol">' + result['本卦']['下卦'] + '</span></div>';
            html += '<div>　卦名：<span class="hexagram-name">' + result['本卦']['卦名'] + '</span></div>';
            html += '<div>　动爻：' + result['本卦']['动爻'] + '</div>';
            html += '</div>';
            
            // 变卦
            html += '<div class="result-section">';
            html += '<div class="result-section-title">【变卦】</div>';
            html += '<div>　上卦：<span class="trigram-symbol">' + result['变卦']['上卦'] + '</span></div>';
            html += '<div>　下卦：<span class="trigram-symbol">' + result['变卦']['下卦'] + '</span></div>';
            html += '<div>　卦名：<span class="hexagram-name">' + result['变卦']['卦名'] + '</span></div>';
            html += '</div>';
            
            // 体用分析
            html += '<div class="result-section">';
            html += '<div class="result-section-title">【体用分析】</div>';
            html += '<div>　体卦：' + result['体用']['体卦'] + '</div>';
            html += '<div>　用卦：' + result['体用']['用卦'] + '</div>';
            html += '<div>　关系：<strong>' + result['体用']['关系'] + '</strong></div>';
            html += '</div>';
            
            // 卦辞解释
            html += '<div class="result-section">';
            html += '<div class="result-section-title">【卦辞解释】</div>';
            html += '<div class="interpretation">' + result['卦辞解释'] + '</div>';
            html += '</div>';
            
            html += '<div class="result-header">════════════════════════════════════════</div>';
            html += '</div>';
            
            resultContainer.innerHTML = html;
        }
        
        function clearResults() {
            const resultContainer = document.getElementById('resultContainer');
            resultContainer.innerHTML = '<div class="empty-result">请选择占卜类别后点击"开始占卜"按钮</div>';
        }
        
        // 页面加载时初始化
        window.addEventListener('DOMContentLoaded', function() {
            initCategories();
        });
    </script>
</body>
</html>'''
        
        # 保存HTML文件到临时目录
        gui_html_path = os.path.join(self.directory, 'gui_interface.html')
        with open(gui_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return gui_html_path
    
    def start_server(self):
        """启动HTTP服务器"""
        try:
            self.server = socketserver.TCPServer(("127.0.0.1", self.port), MeihuaRequestHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            print(f"✓ 服务器已启动在端口 {self.port}")
            return True
        except OSError as e:
            if e.errno == 48 or e.errno == 98:  # Address already in use
                print(f"✗ 端口 {self.port} 已被占用，尝试使用其他端口...")
                self.port += 1
                return self.start_server()
            else:
                print(f"✗ 启动服务器失败: {e}")
                return False
    
    def open_browser(self):
        """打开浏览器窗口"""
        url = f"http://127.0.0.1:{self.port}/gui_interface.html"
        
        # 尝试在应用模式打开浏览器（无地址栏、无工具栏）
        print(f"✓ 正在打开图形界面...")
        
        # 不同操作系统的应用模式启动方式
        if sys.platform == 'darwin':  # macOS
            try:
                os.system(f'open -a "Google Chrome" --args --app={url} --window-size=1000,800 2>/dev/null')
            except:
                webbrowser.open(url)
        elif sys.platform == 'win32':  # Windows
            try:
                os.system(f'start chrome --app={url} --window-size=1000,800')
            except:
                webbrowser.open(url)
        else:  # Linux
            try:
                os.system(f'google-chrome --app={url} --window-size=1000,800 2>/dev/null &')
            except:
                webbrowser.open(url)
    
    def run(self):
        """运行GUI应用"""
        print("="*60)
        print("梅花易数占卜程序 - 桌面GUI版本".center(54))
        print("="*60)
        print()
        
        # 创建HTML界面
        self.create_html_interface()
        
        # 启动服务器
        if not self.start_server():
            print("启动失败，请检查端口是否被占用")
            return
        
        # 打开浏览器
        time.sleep(0.5)  # 等待服务器启动
        self.open_browser()
        
        print()
        print(f"访问地址: http://127.0.0.1:{self.port}/gui_interface.html")
        print()
        print("提示:")
        print("  - 程序正在运行中")
        print("  - 请在打开的窗口中进行占卜")
        print("  - 按 Ctrl+C 退出程序")
        print("="*60)
        
        try:
            # 保持程序运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n正在关闭程序...")
            if self.server:
                self.server.shutdown()
            print("程序已关闭")


def main():
    """主程序入口"""
    try:
        app = MeihuaGUI(port=8888)
        app.run()
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

