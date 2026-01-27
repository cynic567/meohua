#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梅花易数占卜程序 - Web界面版本
Meihua Yishu Divination Program - Web Interface
"""

from flask import Flask, render_template, request, jsonify
from meihua import MeihuaYishu
import os

app = Flask(__name__)
diviner = MeihuaYishu()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html', categories=diviner.DIVINATION_CATEGORIES)


@app.route('/divine', methods=['POST'])
def divine():
    """执行占卜"""
    try:
        data = request.get_json()
        category = int(data.get('category', 2))
        use_ip = data.get('use_ip', True)
        
        # 执行占卜
        result = diviner.divine(category=category, use_ip=use_ip)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # 确保templates目录存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 启动服务器
    print("梅花易数占卜程序 Web界面")
    print("访问 http://localhost:5000 使用程序")
    app.run(debug=False, host='0.0.0.0', port=5000)
