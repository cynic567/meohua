"""
LLM Desktop Client - Main Application
桌面大语言模型客户端
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
from typing import Dict, List, Optional
from openai_provider import OpenAIProvider
from anthropic_provider import AnthropicProvider
from custom_provider import CustomProvider


class LLMDesktopApp:
    """Desktop application for LLM API calls"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("大语言模型桌面客户端 - LLM Desktop Client")
        self.root.geometry("900x700")
        
        # Message history
        self.messages: List[Dict[str, str]] = []
        
        # Current provider
        self.current_provider = None
        
        # Load config
        self.config = self.load_config()
        
        # Create UI
        self.create_widgets()
        
    def load_config(self) -> Dict:
        """Load configuration from file"""
        config_file = 'config.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            'openai_api_key': '',
            'openai_base_url': 'https://api.openai.com/v1',
            'anthropic_api_key': '',
            'custom_api_key': '',
            'custom_base_url': '',
            'custom_model': 'default'
        }
    
    def save_config(self):
        """Save configuration to file"""
        config_file = 'config.json'
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("成功", "配置已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败：{str(e)}")
    
    def create_widgets(self):
        """Create UI widgets"""
        # Top frame for provider selection and settings
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        # Provider selection
        ttk.Label(top_frame, text="选择提供商:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.provider_var = tk.StringVar(value="OpenAI")
        provider_combo = ttk.Combobox(top_frame, textvariable=self.provider_var, 
                                     values=["OpenAI", "Anthropic", "Custom"], 
                                     state="readonly", width=15)
        provider_combo.grid(row=0, column=1, padx=5)
        provider_combo.bind("<<ComboboxSelected>>", self.on_provider_change)
        
        # Model selection
        ttk.Label(top_frame, text="模型:").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(top_frame, textvariable=self.model_var, 
                                       state="readonly", width=25)
        self.model_combo.grid(row=0, column=3, padx=5)
        
        # Settings button
        settings_btn = ttk.Button(top_frame, text="设置", command=self.open_settings)
        settings_btn.grid(row=0, column=4, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(top_frame, text="清空对话", command=self.clear_chat)
        clear_btn.grid(row=0, column=5, padx=5)
        
        # Chat display area
        chat_frame = ttk.Frame(self.root, padding="10")
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(chat_frame, text="对话历史:").pack(anchor=tk.W)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, 
                                                      height=20, font=("Arial", 10))
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input area
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="输入消息:").pack(anchor=tk.W)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, 
                                                    height=5, font=("Arial", 10))
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Send button
        send_frame = ttk.Frame(self.root, padding="10")
        send_frame.pack(fill=tk.X)
        
        self.send_btn = ttk.Button(send_frame, text="发送", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key
        self.input_text.bind("<Control-Return>", lambda e: self.send_message())
        
        # Initialize provider
        self.on_provider_change()
    
    def on_provider_change(self, event=None):
        """Handle provider selection change"""
        provider = self.provider_var.get()
        
        if provider == "OpenAI":
            models = ['gpt-4', 'gpt-4-turbo-preview', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k']
        elif provider == "Anthropic":
            models = ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 
                     'claude-3-haiku-20240307', 'claude-2.1', 'claude-2.0']
        else:  # Custom
            models = [self.config.get('custom_model', 'default')]
        
        self.model_combo['values'] = models
        if models:
            self.model_var.set(models[0])
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("600x500")
        
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # OpenAI settings
        openai_frame = ttk.Frame(notebook, padding="10")
        notebook.add(openai_frame, text="OpenAI")
        
        ttk.Label(openai_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        openai_key_entry = ttk.Entry(openai_frame, width=50, show="*")
        openai_key_entry.insert(0, self.config.get('openai_api_key', ''))
        openai_key_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(openai_frame, text="Base URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        openai_url_entry = ttk.Entry(openai_frame, width=50)
        openai_url_entry.insert(0, self.config.get('openai_base_url', 'https://api.openai.com/v1'))
        openai_url_entry.grid(row=1, column=1, pady=5)
        
        # Anthropic settings
        anthropic_frame = ttk.Frame(notebook, padding="10")
        notebook.add(anthropic_frame, text="Anthropic")
        
        ttk.Label(anthropic_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        anthropic_key_entry = ttk.Entry(anthropic_frame, width=50, show="*")
        anthropic_key_entry.insert(0, self.config.get('anthropic_api_key', ''))
        anthropic_key_entry.grid(row=0, column=1, pady=5)
        
        # Custom settings
        custom_frame = ttk.Frame(notebook, padding="10")
        notebook.add(custom_frame, text="自定义")
        
        ttk.Label(custom_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        custom_key_entry = ttk.Entry(custom_frame, width=50, show="*")
        custom_key_entry.insert(0, self.config.get('custom_api_key', ''))
        custom_key_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(custom_frame, text="Base URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        custom_url_entry = ttk.Entry(custom_frame, width=50)
        custom_url_entry.insert(0, self.config.get('custom_base_url', ''))
        custom_url_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(custom_frame, text="Model:").grid(row=2, column=0, sticky=tk.W, pady=5)
        custom_model_entry = ttk.Entry(custom_frame, width=50)
        custom_model_entry.insert(0, self.config.get('custom_model', 'default'))
        custom_model_entry.grid(row=2, column=1, pady=5)
        
        # Save button
        def save_settings():
            self.config['openai_api_key'] = openai_key_entry.get()
            self.config['openai_base_url'] = openai_url_entry.get()
            self.config['anthropic_api_key'] = anthropic_key_entry.get()
            self.config['custom_api_key'] = custom_key_entry.get()
            self.config['custom_base_url'] = custom_url_entry.get()
            self.config['custom_model'] = custom_model_entry.get()
            self.save_config()
            settings_window.destroy()
            self.on_provider_change()
        
        save_btn = ttk.Button(settings_window, text="保存", command=save_settings)
        save_btn.pack(pady=10)
    
    def get_provider(self):
        """Get current provider instance"""
        provider_name = self.provider_var.get()
        
        if provider_name == "OpenAI":
            api_key = self.config.get('openai_api_key', '')
            base_url = self.config.get('openai_base_url', 'https://api.openai.com/v1')
            if not api_key:
                messagebox.showerror("错误", "请先在设置中配置 OpenAI API Key")
                return None
            return OpenAIProvider(api_key, base_url)
        
        elif provider_name == "Anthropic":
            api_key = self.config.get('anthropic_api_key', '')
            if not api_key:
                messagebox.showerror("错误", "请先在设置中配置 Anthropic API Key")
                return None
            return AnthropicProvider(api_key)
        
        else:  # Custom
            api_key = self.config.get('custom_api_key', '')
            base_url = self.config.get('custom_base_url', '')
            model = self.config.get('custom_model', 'default')
            if not api_key or not base_url:
                messagebox.showerror("错误", "请先在设置中配置自定义 API 信息")
                return None
            return CustomProvider(api_key, base_url, model)
    
    def send_message(self):
        """Send message to LLM"""
        message = self.input_text.get("1.0", tk.END).strip()
        if not message:
            return
        
        # Get provider
        provider = self.get_provider()
        if not provider:
            return
        
        # Add user message to history
        self.messages.append({"role": "user", "content": message})
        
        # Display user message
        self.display_message("用户", message)
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Disable send button
        self.send_btn.config(state=tk.DISABLED)
        self.root.update()
        
        # Get model
        model = self.model_var.get()
        
        # Send to API
        try:
            response = provider.chat(self.messages, model=model)
            
            # Add assistant response to history
            self.messages.append({"role": "assistant", "content": response})
            
            # Display response
            self.display_message("助手", response)
        except Exception as e:
            messagebox.showerror("错误", f"API 调用失败：{str(e)}")
        finally:
            # Re-enable send button
            self.send_btn.config(state=tk.NORMAL)
    
    def display_message(self, role: str, content: str):
        """Display message in chat area"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{'='*80}\n")
        self.chat_display.insert(tk.END, f"{role}:\n", "bold")
        self.chat_display.insert(tk.END, f"{content}\n")
        self.chat_display.tag_config("bold", font=("Arial", 10, "bold"))
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def clear_chat(self):
        """Clear chat history"""
        if messagebox.askyesno("确认", "确定要清空对话历史吗？"):
            self.messages = []
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = LLMDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
