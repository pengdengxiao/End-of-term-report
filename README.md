# 项目说明

## 项目结构

```
project/
├── practice01/           # 练习1：基础LLM客户端
│   └── llm_client.py     # 基础LLM调用示例
├── practice02/           # 练习2：工具调用示例
│   ├── tool_client.py    # 工具调用客户端
│   └── tool_chat_client.py # 带curl功能的工具调用客户端
├── practice03/           # 练习3：聊天记录总结示例
│   └── chat_summary_client.py # 带聊天记录总结功能的客户端
├── .gitignore            # Git忽略文件配置
├── README.md             # 项目说明文件
└── env.example           # 环境变量示例文件
```

## 功能说明

### practice01 - 基础LLM客户端
- 实现了基础的LLM API调用功能
- 支持设置模型、温度、最大令牌数等参数

### practice02 - 工具调用示例
- **tool_client.py**: 实现了文件操作相关的工具调用功能
  - `list_files`: 列出目录下的文件和目录
  - `rename_file`: 重命名文件
  - `delete_file`: 删除文件
  - `create_file`: 创建文件并写入内容
  - `read_file`: 读取文件内容
  - `curl`: 通过curl访问网页并返回网页内容（新增）

- **tool_chat_client.py**: 包含与tool_client.py相同的功能，是完整的工具调用客户端

### practice03 - 聊天记录总结示例
- **chat_summary_client.py**: 实现了聊天记录自动总结功能
  - 聊天历史检测：当聊天轮数超过5轮或上下文长度超过3k tokens时触发总结
  - 聊天记录压缩：对前70%的内容进行总结压缩，保留最后30%的原文
  - 自动调用LLM进行总结，保持对话的连贯性

## 环境配置

1. 复制 `env.example` 文件为 `.env`
2. 在 `.env` 文件中配置以下环境变量：
   - `API_KEY`: LLM API密钥
   - `BASE_URL`: API基础URL（默认：https://api.openai.com/v1）
   - `MODEL`: 使用的模型（默认：gpt-3.5-turbo）
   - `TEMPERATURE`: 温度参数（默认：0.7）
   - `MAX_TOKENS`: 最大令牌数（默认：1000）

## 使用示例

### 运行工具调用示例

```bash
# 运行tool_client.py示例
python practice02/tool_client.py

# 运行tool_chat_client.py示例
python practice02/tool_chat_client.py

# 运行chat_summary_client.py示例
python practice03/chat_summary_client.py
```

### 工具调用示例

1. **列出文件**: 请列出当前目录下的文件
2. **创建文件**: 请在当前目录下创建一个名为test.txt的文件，内容为'Hello, World!'
3. **读取文件**: 请读取当前目录下的test.txt文件内容
4. **重命名文件**: 请将当前目录下的test.txt重命名为example.txt
5. **删除文件**: 请删除当前目录下的example.txt文件
6. **访问网页**: 请访问百度首页并返回内容

## 新增功能

### curl网络访问功能
- 实现了通过`curl`函数访问网页并返回网页内容的功能
- 支持处理URL错误和其他异常
- 返回包含状态、URL和网页内容的JSON对象

## 依赖

- Python 3.x
- 标准库：os, json, http.client, time, urllib.request, urllib.error

## 注意事项

- 请确保在`.env`文件中正确配置API密钥
- 网络访问功能可能受到网络环境和目标网站的限制
- 工具调用功能仅在LLM支持工具调用的情况下生效