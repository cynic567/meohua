# 快速开始指南 / Quick Start Guide

## 安装步骤 / Installation Steps

### 1. 克隆仓库 / Clone Repository
```bash
git clone https://github.com/cynic567/meohua.git
cd meohua
```

### 2. 安装 Python 依赖 / Install Python Dependencies
```bash
pip install -r requirements.txt
```

或使用虚拟环境（推荐）/ Or use virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 / or
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. 配置 API Keys / Configure API Keys

创建配置文件 / Create config file:
```bash
cp config.json.example config.json
```

编辑 `config.json` 并填入您的 API Key / Edit `config.json` and add your API keys.

或者在应用程序中通过"设置"按钮配置 / Or configure through "Settings" button in the app.

### 4. 运行应用 / Run Application
```bash
python main.py
```

## 获取 API Keys / Getting API Keys

### OpenAI
1. 访问 / Visit: https://platform.openai.com/
2. 注册账号 / Sign up
3. 前往 API Keys 页面 / Go to API Keys page
4. 创建新的 API Key / Create new API Key

### Anthropic Claude
1. 访问 / Visit: https://console.anthropic.com/
2. 注册账号 / Sign up
3. 前往 API Keys 设置 / Go to API Keys settings
4. 创建新的 API Key / Create new API Key

### 自定义 API / Custom API
如果您使用兼容 OpenAI API 格式的服务（如 Azure OpenAI、本地模型等），只需要：
- API Key
- Base URL（API 端点地址）
- Model Name（模型名称）

If using OpenAI-compatible services (like Azure OpenAI, local models, etc.), you need:
- API Key
- Base URL (API endpoint)
- Model Name

## 使用技巧 / Usage Tips

1. **快捷键 / Shortcuts**: 使用 `Ctrl+Enter` 发送消息 / Use `Ctrl+Enter` to send messages

2. **对话历史 / Chat History**: 应用会保持完整的对话上下文 / The app maintains full conversation context

3. **切换模型 / Switch Models**: 可以随时切换不同的提供商和模型 / You can switch between providers and models anytime

4. **清空对话 / Clear Chat**: 点击"清空对话"按钮开始新的对话 / Click "Clear Chat" to start a new conversation

5. **API 费用 / API Costs**: 
   - 使用 API 会产生费用，请注意控制使用量
   - Using APIs incurs costs, please monitor your usage
   - 建议先使用较便宜的模型测试 / Start with cheaper models for testing

## 常见问题 / Troubleshooting

### 问题：无法启动应用 / Issue: Cannot start application
**解决方案 / Solution**:
- 确保已安装 Python 3.7+ / Ensure Python 3.7+ is installed
- 确保已安装所有依赖 / Ensure all dependencies are installed
- Linux 用户可能需要安装 `python3-tk`: `sudo apt-get install python3-tk`

### 问题：API 调用失败 / Issue: API call fails
**解决方案 / Solution**:
- 检查 API Key 是否正确 / Check if API key is correct
- 检查网络连接 / Check internet connection
- 检查 API 配额是否用尽 / Check if API quota is exhausted
- 查看错误消息获取详细信息 / Check error message for details

### 问题：中文显示乱码 / Issue: Chinese characters display incorrectly
**解决方案 / Solution**:
- 确保系统安装了中文字体 / Ensure Chinese fonts are installed
- Windows: 系统默认支持 / Supported by default
- Linux: `sudo apt-get install fonts-wqy-zenhei`
- macOS: 系统默认支持 / Supported by default

## 开发建议 / Development Tips

### 添加新的 LLM 提供商 / Adding New LLM Providers

1. 继承 `LLMProvider` 基类 / Inherit from `LLMProvider` base class
2. 实现 `chat()` 和 `get_models()` 方法 / Implement `chat()` and `get_models()` methods
3. 在 `main.py` 中添加到提供商列表 / Add to provider list in `main.py`

示例 / Example:
```python
from llm_provider import LLMProvider

class MyLLMProvider(LLMProvider):
    def chat(self, messages, **kwargs):
        # Your implementation
        pass
    
    def get_models(self):
        return ['model-1', 'model-2']
```

## 安全提示 / Security Notes

⚠️ **重要 / Important**:
- 不要分享您的 API Keys / Never share your API keys
- 不要将 `config.json` 提交到公共仓库 / Don't commit `config.json` to public repos
- 定期更换 API Keys / Rotate API keys regularly
- 注意 API 使用费用 / Monitor API usage and costs

## 获取帮助 / Getting Help

- 提交 Issue: https://github.com/cynic567/meohua/issues
- 查看文档: README.md
- 示例配置: config.json.example

## 许可证 / License

MIT License - 可自由使用和修改 / Free to use and modify
