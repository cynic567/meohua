# 大语言模型桌面客户端 - LLM Desktop Client

一个简单易用的桌面应用程序，可以通过 API 调用各种大语言模型服务。

A simple desktop application for calling various Large Language Model (LLM) APIs.

## 功能特性 / Features

- ✅ 支持多个 LLM 提供商 / Support multiple LLM providers
  - OpenAI (GPT-4, GPT-3.5 等)
  - Anthropic (Claude 系列)
  - 自定义 API 端点 / Custom API endpoints
- 🖥️ 简洁的图形界面 / Simple GUI interface
- 💬 完整的对话历史管理 / Full conversation history
- ⚙️ 灵活的配置系统 / Flexible configuration
- 🔐 本地存储 API 密钥 / Local API key storage

## 安装 / Installation

### 前提条件 / Prerequisites

- Python 3.7 或更高版本 / Python 3.7+
- pip 包管理器 / pip package manager

### 安装步骤 / Steps

1. 克隆仓库 / Clone the repository:
```bash
git clone https://github.com/cynic567/meohua.git
cd meohua
```

2. 安装依赖 / Install dependencies:
```bash
pip install -r requirements.txt
```

## 使用方法 / Usage

### 启动应用 / Start the application

```bash
python main.py
```

### 配置 API / Configure API

1. 点击 "设置" 按钮 / Click "Settings" button
2. 选择对应的提供商标签页 / Select provider tab
3. 输入您的 API Key / Enter your API key
4. (可选) 修改 Base URL / (Optional) Modify Base URL
5. 点击 "保存" / Click "Save"

### 使用聊天功能 / Using Chat

1. 在顶部选择 LLM 提供商 / Select LLM provider at top
2. 选择要使用的模型 / Select model to use
3. 在输入框中输入消息 / Enter message in input box
4. 点击 "发送" 或按 Ctrl+Enter / Click "Send" or press Ctrl+Enter
5. 等待 AI 响应 / Wait for AI response

## 支持的提供商 / Supported Providers

### OpenAI

**需要的信息 / Required:**
- API Key: 从 https://platform.openai.com/ 获取
- Base URL: 默认 `https://api.openai.com/v1`

**支持的模型 / Supported models:**
- GPT-4
- GPT-4 Turbo
- GPT-3.5 Turbo
- GPT-3.5 Turbo 16K

### Anthropic Claude

**需要的信息 / Required:**
- API Key: 从 https://console.anthropic.com/ 获取

**支持的模型 / Supported models:**
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku
- Claude 2.1
- Claude 2.0

### 自定义 API / Custom API

支持任何与 OpenAI API 格式兼容的服务，例如：
- Azure OpenAI
- 本地部署的模型
- 其他兼容服务

**需要的信息 / Required:**
- API Key
- Base URL (API 端点地址)
- Model Name (模型名称)

## 项目结构 / Project Structure

```
meohua/
├── main.py                 # 主应用程序 / Main application
├── llm_provider.py        # LLM 提供商基类 / Base provider class
├── openai_provider.py     # OpenAI 提供商 / OpenAI provider
├── anthropic_provider.py  # Anthropic 提供商 / Anthropic provider
├── custom_provider.py     # 自定义提供商 / Custom provider
├── requirements.txt       # Python 依赖 / Dependencies
├── .gitignore            # Git 忽略文件 / Git ignore
└── README.md             # 项目说明 / Documentation
```

## 配置文件 / Configuration

应用程序会在当前目录创建 `config.json` 文件来保存配置。
此文件包含 API 密钥，请勿分享或提交到版本控制系统。

The application creates a `config.json` file to store configuration.
This file contains API keys, do not share or commit to version control.

## 安全提示 / Security Notes

- ⚠️ API 密钥保存在本地 `config.json` 文件中
- ⚠️ 不要将 `config.json` 文件上传到公共仓库
- ⚠️ 定期更换您的 API 密钥

- ⚠️ API keys are stored locally in `config.json`
- ⚠️ Do not upload `config.json` to public repositories
- ⚠️ Rotate your API keys regularly

## 常见问题 / FAQ

**Q: 如何获取 API Key?**  
A: 访问对应提供商的官网注册账号并创建 API Key。

**Q: 支持哪些操作系统?**  
A: 支持 Windows、macOS 和 Linux。

**Q: 如何添加更多 LLM 提供商?**  
A: 可以继承 `LLMProvider` 基类创建新的提供商类。

**Q: API 调用会产生费用吗?**  
A: 是的，根据各提供商的定价策略收费。

## 许可证 / License

MIT License

## 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

Welcome to submit Issues and Pull Requests!
# 梅花易数占卜程序 (Meihua Yishu Divination Program)

基于梅花易数理论的占卜程序，使用Python实现。

## 简介

《梅花易数》是中国古代占卜法之一，相传为宋代易学家邵雍所著。本程序依据梅花易数理论，结合现代计算方法，实现了自动化占卜功能。

## 功能特点

- **18种占卜类别**：包括天时、人事、家宅、婚姻、求财、疾病等
- **智能起卦**：使用当前时间和IP地址算法自动起卦
- **体用分析**：基于五行生克关系进行体用分析
- **卦象解释**：根据不同占卜类别提供针对性解释
- **可视化界面**：提供美观的Web图形界面，操作简便直观

## 安装和运行

### 环境要求
- Python 3.6 或更高版本
- Flask（仅Web界面需要）

### 运行方法

#### 方法一：命令行版本

```bash
python3 meihua.py
```

#### 方法二：Web可视化界面（推荐）

**选项1：独立HTML版本（无需安装任何依赖）**

直接在浏览器中打开 `meihua_standalone.html` 文件即可使用。

**选项2：Flask Web服务器版本**

```bash
# 安装依赖
pip install -r requirements.txt

# 启动Web服务器
python3 meihua_web.py

# 在浏览器中访问 http://localhost:5000
```

#### 方法三：桌面GUI版本（推荐，完整功能）

**无需安装任何GUI库，只使用Python标准库！**

```bash
python3 meihua_gui.py
```

程序会自动启动本地服务器并在浏览器中打开应用界面。
- 自动管理服务器启动和关闭
- 类似桌面应用的使用体验
- 支持所有平台（Windows/Mac/Linux）
- 按 Ctrl+C 退出程序

### 使用方法

**命令行版本：**
1. 运行程序后，会显示18种占卜类别
2. 输入对应的编号（1-18）选择占卜类别
3. 直接回车使用默认类别（人事占）
4. 程序将自动计算并显示占卜结果

**Web界面版本：**
1. 在界面上选择占卜类别（单选按钮）
2. 选择起卦方式（时间起卦或随机起卦）
3. 点击"开始占卜"按钮
4. 查看占卜结果，包括本卦、变卦、体用分析和卦辞解释

![Web界面截图](https://github.com/user-attachments/assets/b8d0422e-d7be-47cb-a87b-402fece009c3)

![占卜结果示例](https://github.com/user-attachments/assets/e37ae526-67e1-4273-8a9f-829891f552bd)

## 占卜类别

1. 天时占 - 占卜天气时令
2. 人事占 - 占卜人事吉凶
3. 家宅占 - 占卜家宅情况
4. 屋舍占 - 占卜房屋居所
5. 婚姻占 - 占卜婚姻状况
6. 生产占 - 占卜生育事宜
7. 饮食占 - 占卜饮食情况
8. 求谋占 - 占卜谋事成败
9. 求名占 - 占卜功名利禄
10. 求财占 - 占卜财运状况
11. 交易占 - 占卜交易买卖
12. 出行占 - 占卜出行吉凶
13. 行人占 - 占卜行人归期
14. 谒见占 - 占卜见面拜访
15. 失物占 - 占卜失物寻找
16. 疾病占 - 占卜疾病状况
17. 官讼占 - 占卜官司诉讼
18. 坟墓占 - 占卜墓地风水

## 技术实现

### 起卦方法

- **上卦**：使用当前时间（年+月+日）除以8取余数
- **下卦**：使用IP地址通过SHA256哈希算法处理后对32取模，再除以8取余数
- **动爻**：使用时间和IP值的组合除以6取余数

### 八卦数理

基于先天八卦数：
- 乾☰ = 1（金）
- 兑☱ = 2（金）
- 离☲ = 3（火）
- 震☳ = 4（木）
- 巽☴ = 5（木）
- 坎☵ = 6（水）
- 艮☶ = 7（土）
- 坤☷ = 8（土）

### 五行关系

**相生关系**：金生水，水生木，木生火，火生土，土生金

**相克关系**：金克木，木克土，土克水，水克火，火克金

### 体用论

- 动爻所在的卦为用卦，另一卦为体卦
- 分析五行关系：
  - **比和**：体用五行相同，吉利
  - **用生体**：用卦五行生体卦五行，大吉
  - **体生用**：体卦五行生用卦五行，耗损
  - **体克用**：体卦五行克用卦五行，可成但慢
  - **用克体**：用卦五行克体卦五行，凶

## 示例输出

```
                   梅花易数占卜结果                   

占卜时间：2025年11月07日 10:25:04
占卜类别：人事占

【本卦】
  上卦：离☲
  下卦：巽☴
  卦名：火风鼎
  动爻：第6爻

【变卦】
  上卦：震☳
  下卦：巽☴
  卦名：雷风恒

【体用分析】
  体卦：巽（木）
  用卦：离（火）
  关系：体生用

【卦辞解释】
  人事占：有耗失之患，需谨慎行事

```

## 注意事项

1. 本程序仅供娱乐和学习传统文化之用
2. 占卜结果仅供参考，不应作为决策的唯一依据
3. 程序使用简化的农历计算，实际应用中可配合真实农历
4. IP地址获取可能因网络环境而异，本地测试时可能使用127.0.0.1

## 许可证

MIT License

## 贡献

欢迎提交问题和改进建议！
