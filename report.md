# AI Agent 开发入门教程讲义

---

## 前言

欢迎来到「AI Agent 开发入门」课程！这门课程将带你从零开始，通过**实际项目驱动**的方式，学会构建一个能自主工作的 AI 助手。

**课程特色**：
- 🎯 **入门友好**：无需复杂理论，跟着做就能学会
- 📦 **项目驱动**：所有内容围绕实际项目展开
-  **逻辑闭环**：从基础到实战，形成完整知识体系
- 🚀 **实操落地**：学完就能独立复现项目并拓展功能

---

## 目录

1. [开篇破题——AI Agent 是什么？](#第 1 章 - 开篇破题 ai-agent 是什么)
2. [入门必备基础](#第 2 章 - 入门必备基础)
3. [教学项目拆解](#第 3 章 - 教学项目拆解)
4. [感知模块开发](#第 4 章 - 感知模块开发)
5. [记忆模块开发](#第 5 章 - 记忆模块开发)
6. [规划与执行模块开发](#第 6 章 - 规划与执行模块开发)
7. [整合与输出模块开发](#第 7 章 - 整合与输出模块开发)
8. [项目测试、部署与拓展](#第 8 章 - 项目测试部署与拓展)
9. [附录：实用工具包](#附录实用工具包)

---

# 第 1 章：开篇破题——AI Agent 是什么？

## 1.1 通俗定义

你可以把 AI Agent 理解为一个**有自主能力的数字助手**。它能：
- ✅ 自己理解你的需求
- ✅ 自己规划做事步骤
- ✅ 自己调用工具完成任务
- ✅ 自己总结并输出结果

**简单说**：就是一个能"自己干活"的智能程序！

## 1.2 应用场景举例

| 场景 | Agent 功能 | 类比理解 |
|------|----------|----------|
| 📝 **自动写报告** | 读取数据 → 分析内容 → 生成报告 | 像个自动写稿的秘书 |
| 💬 **智能客服** | 理解问题 → 查询知识 → 解答用户 | 像个专业客服人员 |
| 🔧 **代码调试** | 读取代码 → 分析问题 → 给出修复方案 | 像个资深程序员 |

**我们的教学项目**：开发一个「智能工具助手 Agent」，它能帮你完成文件操作、网页访问、技能调用等任务！

## 1.3 Agent 的核心特征

1. **自主决策**：不需要人一步步指挥，能自己决定下一步做什么
2. **能交互**：可以调用外部工具（如文件操作、API）获取信息
3. **可迭代**：能记住历史对话，持续优化回答

## 1.4 本章小目标

✅ 知道 AI Agent 是什么，能做什么  
✅ 明确我们要开发的「智能工具助手」项目目标  
✅ 激发学习兴趣，准备开始实战！

---

# 第 2 章：入门必备基础

## 2.1 技术栈清单

### 必须掌握的技能
| 技能 | 用途 | 掌握程度 |
|------|------|----------|
| Python 基础 | 编写 Agent 代码 | 熟悉变量、函数、条件判断 |
| HTTP 请求 | 调用 LLM API | 了解 POST/GET 请求 |
| JSON 处理 | 解析 API 响应 | 会用 json 库 |

### 可选技能
| 技能 | 用途 | 说明 |
|------|------|------|
| Docker | 部署项目 | 后续部署章节会讲 |
| Git | 版本控制 | 管理代码用 |

## 2.2 核心工具/库速通

### 1) LLM API 调用
我们使用标准 HTTP 请求调用 LLM 接口，无需额外安装复杂库。

### 2) 环境变量配置
使用`.env`文件存储敏感信息：
```bash
# .env 文件内容示例
API_KEY=your_api_key_here
BASE_URL=https://api.openai.com/v1
MODEL=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=1000
```

### 工具安装步骤
```bash
# 检查 Python 版本（需要 3.x）
python --version

# 复制环境变量模板
copy env.example .env

# 编辑.env 文件，填入你的 API 密钥
notepad .env
```

## 2.3 关键概念速记

| 概念 | 一句话定义 | 类比 |
|------|-----------|------|
| **LLM** | 大语言模型，能理解和生成人类语言 | 聪明的大脑 |
| **工具调用** | Agent 调用外部程序完成特定任务 | 大脑指挥手去做事 |
| **API 密钥** | 访问 LLM 服务的凭证 | 像一把钥匙 |
| **令牌 (Token)** | LLM 处理文本的基本单位 | 像文字的"积木" |

## 2.4 小练习：跑通第一个 LLM 调用

打开 `practice01/llm_client.py` 文件，运行：

```bash
python practice01/llm_client.py
```

**预期输出**：
```
=== LLM 调用结果 ===
提示词令牌数：12
完成令牌数：45
总令牌数：57
耗时：1.23 秒
速度：46.34 tokens/秒

响应内容:
人工智能是...
```

**如果报错**：检查 `.env` 文件中的 API 密钥是否正确！

---

# 第 3 章：教学项目拆解

## 3.1 项目目标

**输入**：用户的自然语言指令，如"帮我创建一个文件"  
**输出**：任务执行结果或回答

**项目名称**：智能工具助手 Agent

**核心功能**：
1. 文件操作（创建、读取、修改、删除）
2. 网页访问（通过 curl 获取内容）
3. 技能管理（加载和使用预设技能）

## 3.2 项目架构图

```
用户输入 → [感知模块] → [记忆模块] → [规划与执行模块] → [输出模块] → 结果
              ↓              ↓               ↓
           解析需求       存储历史        调用工具/LLM
```

## 3.3 模块分工表

| 模块 | 作用 | 对应练习文件 |
|------|------|-------------|
| **感知模块** | 接收输入、解析用户需求 | practice01 |
| **记忆模块** | 存储历史对话、管理上下文 | practice03 |
| **规划与执行模块** | 决策步骤、调用工具 | practice02 |
| **技能模块** | 加载和使用预设技能 | practice06 |

## 3.4 技术选型说明

| 选择 | 原因 |
|------|------|
| **原生 Python** | 避免过多依赖，入门更简单 |
| **HTTP 调用** | 直接调用 API，理解底层原理 |
| **工具调用框架** | 标准化工具定义，易于扩展 |

**为什么不选 LangChain？**  
对于入门者来说，先理解底层原理更重要。等你掌握了核心逻辑，再用框架会更得心应手！

---

# 第 4 章：感知模块开发

## 4.1 模块目标

让 Agent 能"听懂"用户的需求，解析输入的意图。

## 4.2 核心逻辑

```
用户输入 → 文本预处理 → LLM 分类 → 输出需求类型
```

## 4.3 手把手实操

### 步骤 1：代码编写

打开 `practice01/llm_client.py`，核心代码如下：

```python
import os
import json
import http.client
import time

def load_env():
    """加载.env 文件中的环境变量"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def call_llm(prompt):
    """调用 LLM 并统计相关指标"""
    # 加载环境变量（关键！）
    env_vars = load_env()
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    api_key = env_vars.get('API_KEY', '')
    
    if not api_key:
        print("错误：API_KEY 未设置")  # ❗ 常见报错点
        return
    
    # 提取主机和路径
    if base_url.startswith('https://'):
        host = base_url[8:].split('/')[0]
        path = '/' + '/'.join(base_url[8:].split('/')[1:]) + '/chat/completions'
        conn = http.client.HTTPSConnection(host)
    else:
        host = base_url[7:].split('/')[0]
        path = '/' + '/'.join(base_url[7:].split('/')[1:]) + '/chat/completions'
        conn = http.client.HTTPConnection(host)
    
    # 构建请求数据
    data = {
        "model": env_vars.get('MODEL', 'gpt-3.5-turbo'),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": float(env_vars.get('TEMPERATURE', '0.7')),
        "max_tokens": int(env_vars.get('MAX_TOKENS', '1000'))
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'  # 🔑 认证关键
    }
    
    # 发送请求
    conn.request('POST', path, json.dumps(data), headers)
    response = conn.getresponse()
    response_data = response.read().decode('utf-8')
    conn.close()
    
    # 解析响应
    result = json.loads(response_data)
    if 'error' in result:
        print(f"错误：{result['error']['message']}")
        return
    
    print(result['choices'][0]['message']['content'])

if __name__ == "__main__":
    prompt = "请解释什么是人工智能"
    call_llm(prompt)
```

### 步骤 2：环境配置

1. 复制 `env.example` 为 `.env`
2. 在 `.env` 中填入你的 API 密钥：
   ```
   API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 步骤 3：运行测试

```bash
python practice01/llm_client.py
```

**预期输出**：
```
=== LLM 调用结果 ===
提示词令牌数：12
完成令牌数：45
总令牌数：57
耗时：1.23 秒
速度：46.34 tokens/秒

响应内容:
人工智能是...
```

## 4.4 易错点提醒

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `API_KEY 未设置` | .env 文件不存在或 API_KEY 为空 | 创建.env 文件并填入密钥 |
| `认证失败` | API 密钥错误 | 检查密钥是否正确 |
| `响应解析失败` | API 返回非 JSON 格式 | 检查网络和 API 地址 |

## 4.5 小拓展

尝试修改 `prompt` 变量，让 Agent 分析用户意图：
```python
prompt = "分析以下用户输入的意图：'帮我创建一个文件'"
call_llm(prompt)
```

---

# 第 5 章：记忆模块开发

## 5.1 模块目标

让 Agent 能记住历史对话，实现多轮对话功能。

## 5.2 核心逻辑

```
新对话 → 检查历史长度 → 超过阈值则总结 → 存储上下文 → 传入下一轮
```

## 5.3 手把手实操

### 步骤 1：代码编写

查看 `practice03/chat_summary_client.py`，关键代码：

```python
def summarize_chat(history):
    """总结聊天记录"""
    # 只总结前 70% 的内容，保留最后 30%
    total_messages = len(history)
    if total_messages <= 3:
        return history  # 消息太少，不需要总结
    
    # 计算总结点
    summarize_up_to = int(total_messages * 0.7)
    messages_to_summarize = history[:summarize_up_to]
    messages_to_keep = history[summarize_up_to:]
    
    # 构建总结提示词
    summary_prompt = "请总结以下对话内容：\n"
    for msg in messages_to_summarize:
        summary_prompt += f"{msg['role']}: {msg['content']}\n"
    
    # 调用 LLM 进行总结
    summary = call_llm(summary_prompt)
    
    # 返回：[总结] + [保留的消息]
    return [{"role": "system", "content": f"对话总结：{summary}"}] + messages_to_keep
```

### 步骤 2：运行测试

```bash
python practice03/chat_summary_client.py
```

### 步骤 3：观察效果

当对话轮数超过 5 轮时，系统会自动总结历史内容，保持上下文窗口在合理范围内。

## 5.4 易错点提醒

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 内存溢出 | 历史记录无限增长 | 设置总结阈值 |
| 总结丢失信息 | 总结逻辑不合理 | 调整保留比例 |

---

# 第 6 章：规划与执行模块开发

## 6.1 模块目标

这是 Agent 的**核心模块**！让 Agent 能：
1. 判断是否需要调用工具
2. 选择合适的工具
3. 执行工具并获取结果
4. 根据结果生成最终回答

## 6.2 核心逻辑

```
用户需求 → LLM 判断是否调用工具 → 调用工具 → 获取结果 → LLM 总结回答
                              ↓
                         直接回答
```

## 6.3 手把手实操

### 步骤 1：代码编写

查看 `practice02/tool_client.py`，核心工具定义：

```python
# 工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "在某个目录下新建 1 个文件，并且写入内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "要创建文件的目录路径"},
                    "filename": {"type": "string", "description": "要创建的文件名"},
                    "content": {"type": "string", "description": "要写入文件的内容"}
                },
                "required": ["directory", "filename", "content"]
            }
        }
    },
    # ... 更多工具定义
]
```

工具执行函数：

```python
def create_file(directory, filename, content):
    """在某个目录下新建 1 个文件，并且写入内容"""
    try:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"status": "success", "file_path": file_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### 步骤 2：工具调用流程

```python
def call_llm_with_tools(prompt):
    # 1. 构建包含工具信息的系统提示词
    system_prompt = """你是一个智能助手，拥有以下工具调用能力：
    1. create_file(directory, filename, content): 创建文件
    2. read_file(directory, filename): 读取文件
    ...
    """
    
    # 2. 调用 LLM，传入工具列表
    data = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt}, 
                     {"role": "user", "content": prompt}],
        "tools": tools  # 关键：告诉 LLM 有哪些工具可用
    }
    
    # 3. 解析响应，检查是否需要工具调用
    response = conn.request('POST', path, json.dumps(data), headers)
    result = json.loads(response.read().decode('utf-8'))
    
    # 4. 如果需要工具调用，执行相应工具
    if result['choices'][0].get('finish_reason') == 'tool_calls':
        tool_calls = result['choices'][0]['message'].get('tool_calls', [])
        for tool_call in tool_calls:
            function_name = tool_call['function']['name']
            arguments = json.loads(tool_call['function']['arguments'])
            
            # 执行工具
            if function_name == 'create_file':
                tool_result = create_file(arguments['directory'], 
                                        arguments['filename'], 
                                        arguments['content'])
    
    # 5. 将工具结果返回给 LLM，生成最终回答
```

### 步骤 3：运行测试

```bash
python practice02/tool_client.py
```

**预期输出**：
```
=== 工具调用示例 ===
示例 1: 列出当前目录下的文件

执行工具调用：list_files
参数：{"directory": "."}
工具执行结果：{"status": "success", "files": [...], "directory": "."}

=== LLM 调用结果 ===
总令牌数：120
耗时：0.85 秒
速度：141.18 tokens/秒

响应内容:
当前目录下有以下文件：
- llm_client.py
- tool_client.py
- ...
```

## 6.4 易错点提醒

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 工具名称错误 | tools 列表中的 name 与函数名不一致 | 检查名称拼写 |
| 参数缺失 | required 参数未提供 | 检查工具调用参数 |
| 权限不足 | 文件操作没有权限 | 检查目录权限 |

## 6.5 小拓展

尝试添加新工具！比如添加一个计算工具：

```python
def calculate(expression):
    """计算数学表达式"""
    try:
        result = eval(expression)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

# 第 7 章：整合与输出模块开发

## 7.1 模块目标

将前面所有模块整合起来，形成完整的 Agent 系统，并生成友好的输出。

## 7.2 核心逻辑

```
感知模块 → 记忆模块 → 规划执行模块 → 格式化输出
    ↓           ↓           ↓
   解析需求    管理上下文   执行任务
```

## 7.3 手把手实操

### 步骤 1：查看整合代码

打开 `practice06/skill_client.py`，这是整合了所有功能的完整版本。

### 步骤 2：运行完整系统

```bash
python practice06/skill_client.py
```

**交互示例**：
```
=== LLM 工具调用系统（输入 '退出' 结束）===

请输入你的指令：帮我创建一个名为 hello.txt 的文件
执行工具调用：create_file
参数：{"directory": ".", "filename": "hello.txt", "content": ""}
工具执行结果：{"status": "success", "file_path": "./hello.txt"}

=== LLM 调用结果 ===
总令牌数：89
耗时：0.62 秒
速度：143.55 tokens/秒

响应内容:
已成功创建文件 hello.txt！

请输入你的指令：退出
程序结束！
```

## 7.4 易错点提醒

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 模块间数据传递错误 | 数据格式不一致 | 统一 JSON 格式 |
| 循环调用 | 工具调用逻辑有误 | 添加递归深度限制 |

---

# 第 8 章：项目测试、部署与拓展

## 8.1 测试方法

### 测试用例表

| 测试场景 | 输入 | 预期输出 |
|----------|------|----------|
| 创建文件 | "创建 test.txt 文件" | 文件创建成功提示 |
| 读取文件 | "读取 test.txt" | 文件内容 |
| 重命名文件 | "把 test.txt 改名为 demo.txt" | 重命名成功提示 |
| 删除文件 | "删除 demo.txt" | 删除成功提示 |
| 网页访问 | "访问百度首页" | 返回网页内容 |

### 运行测试

```bash
# 运行所有测试
python practice02/tool_client.py
```

## 8.2 部署步骤

### 本地运行（开发模式）
```bash
# 确保安装了 Python
python --version

# 运行主程序
python practice06/skill_client.py
```

### 打包成可执行文件（可选）
```bash
# 安装 pyinstaller
pip install pyinstaller

# 打包
pyinstaller --onefile practice06/skill_client.py

# 运行生成的 exe
dist/skill_client.exe
```

## 8.3 项目拓展方向

### 拓展 1：多轮对话优化
- 添加对话历史管理
- 实现话题追踪功能

### 拓展 2：替换成本地化 LLM
- 集成 Llama 3
- 部署本地推理服务

### 拓展 3：增加更多工具
- 添加 Excel 操作工具
- 添加邮件发送工具
- 添加数据库查询工具

## 8.4 资源推荐

-  **官方文档**：OpenAI API 文档、HTTP 客户端文档
- 🛠️ **工具**：Postman（API 测试）、ngrok（内网穿透）
- 📖 **进阶学习**：LangChain 官方教程、LLM Agent 论文

---

# 附录：实用工具包

## A.1 常用命令清单

```bash
# 运行基础 LLM 调用
python practice01/llm_client.py

# 运行工具调用示例
python practice02/tool_client.py

# 运行聊天总结示例
python practice03/chat_summary_client.py

# 运行完整技能调用系统
python practice06/skill_client.py

# 复制环境变量模板
copy env.example .env

# 查看目录结构
dir
```

## A.2 常见报错排查指南

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `API_KEY 未设置` | .env 文件不存在或为空 | 创建并配置.env 文件 |
| `认证失败` | API 密钥错误或过期 | 检查并更新密钥 |
| `网络连接失败` | 网络不通或代理问题 | 检查网络设置 |
| `文件不存在` | 文件路径错误 | 检查目录和文件名 |
| `权限不足` | 没有文件操作权限 | 以管理员身份运行 |

## A.3 核心代码速查表

### LLM 调用
```python
conn.request('POST', path, json.dumps(data), headers)
response = conn.getresponse()
result = json.loads(response.read().decode('utf-8'))
```

### 工具定义
```python
{
    "type": "function",
    "function": {
        "name": "工具名",
        "description": "工具描述",
        "parameters": {"类型定义"}
    }
}
```

### 环境变量加载
```python
env_vars = load_env()
api_key = env_vars.get('API_KEY', '')
```

## A.4 空白批注区

---

## Q&A

### Q1：为什么运行时报错"API_KEY 未设置"？

**A**：请检查项目根目录是否有 `.env` 文件，并且文件中是否正确设置了 `API_KEY`。

### Q2：Agent 决策不符合预期怎么办？

**A**：可以尝试：
1. 调整 `TEMPERATURE` 参数（越小越确定性）
2. 优化系统提示词，更明确地指导 Agent 行为
3. 检查工具描述是否清晰

### Q3：如何添加新工具？

**A**：按照以下步骤：
1. 编写工具函数
2. 在 `tools` 列表中添加工具定义
3. 在工具执行逻辑中添加对应的调用分支

---

## 项目源码链接

GitHub 仓库：https://github.com/pengdengxiao/End-of-term-report.git

---

**恭喜你完成 AI Agent 开发入门教程！** 🎉

现在你已经掌握了：
1. ✅ LLM API 调用基础
2. ✅ 工具调用机制
3. ✅ 记忆模块开发
4. ✅ 完整 Agent 系统整合

继续探索，你可以创建更强大的 AI Agent 应用！