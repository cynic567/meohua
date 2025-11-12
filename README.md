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