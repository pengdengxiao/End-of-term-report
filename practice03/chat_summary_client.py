import os
import json
import http.client
import time
import urllib.request
import urllib.error

# 工具函数
def list_files(directory):
    """列出某个目录下有哪些文件（包括文件的基本属性、大小等信息）"""
    try:
        files = []
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                files.append({
                    "name": filename,
                    "size": stat.st_size,
                    "mtime": time.ctime(stat.st_mtime),
                    "mode": stat.st_mode
                })
            elif os.path.isdir(file_path):
                files.append({
                    "name": filename + "/",
                    "type": "directory"
                })
        return {
            "status": "success",
            "files": files,
            "directory": directory
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def rename_file(directory, old_name, new_name):
    """修改某个目录下某个文件的名字"""
    try:
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            return {
                "status": "success",
                "old_path": old_path,
                "new_path": new_path
            }
        else:
            return {
                "status": "error",
                "message": "文件不存在"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def delete_file(directory, filename):
    """删除某个目录下的某个文件"""
    try:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            return {
                "status": "success",
                "file_path": file_path
            }
        else:
            return {
                "status": "error",
                "message": "文件不存在或不是文件"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def create_file(directory, filename, content):
    """在某个目录下新建1个文件，并且写入内容"""
    try:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {
            "status": "success",
            "file_path": file_path
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def read_file(directory, filename):
    """读取某个目录下的某个文件的内容"""
    try:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "status": "success",
                "file_path": file_path,
                "content": content
            }
        else:
            return {
                "status": "error",
                "message": "文件不存在或不是文件"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def curl(url):
    """通过curl访问网页并返回网页内容"""
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
            return {
                "status": "success",
                "url": url,
                "content": content
            }
    except urllib.error.URLError as e:
        return {
            "status": "error",
            "message": f"URL错误: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "列出某个目录下有哪些文件（包括文件的基本属性、大小等信息）",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "要列出文件的目录路径"
                    }
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rename_file",
            "description": "修改某个目录下某个文件的名字",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "文件所在的目录路径"
                    },
                    "old_name": {
                        "type": "string",
                        "description": "原文件名"
                    },
                    "new_name": {
                        "type": "string",
                        "description": "新文件名"
                    }
                },
                "required": ["directory", "old_name", "new_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "删除某个目录下的某个文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "文件所在的目录路径"
                    },
                    "filename": {
                        "type": "string",
                        "description": "要删除的文件名"
                    }
                },
                "required": ["directory", "filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "在某个目录下新建1个文件，并且写入内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "要创建文件的目录路径"
                    },
                    "filename": {
                        "type": "string",
                        "description": "要创建的文件名"
                    },
                    "content": {
                        "type": "string",
                        "description": "要写入文件的内容"
                    }
                },
                "required": ["directory", "filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取某个目录下的某个文件的内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "文件所在的目录路径"
                    },
                    "filename": {
                        "type": "string",
                        "description": "要读取的文件名"
                    }
                },
                "required": ["directory", "filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "curl",
            "description": "通过curl访问网页并返回网页内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要访问的网页URL"
                    }
                },
                "required": ["url"]
            }
        }
    }
]

def load_env():
    """加载.env文件中的环境变量"""
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

def calculate_tokens(text):
    """简单估算文本的token数量"""
    # 粗略估算：1个token约等于4个字符
    return len(text) // 4

def summarize_chat_history(chat_history, env_vars):
    """总结聊天历史记录"""
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', '')
    temperature = float(env_vars.get('TEMPERATURE', '0.7'))
    max_tokens = int(env_vars.get('MAX_TOKENS', '1000'))
    
    if not api_key:
        print("错误：API_KEY未设置")
        return chat_history
    
    # 提取主机和路径
    if base_url.startswith('https://'):
        host = base_url[8:].split('/')[0]
        path_parts = base_url[8:].split('/')[1:]
        if path_parts:
            path = '/' + '/'.join(path_parts) + '/chat/completions'
        else:
            path = '/chat/completions'
        conn = http.client.HTTPSConnection(host)
    else:
        host = base_url[7:].split('/')[0]
        path_parts = base_url[7:].split('/')[1:]
        if path_parts:
            path = '/' + '/'.join(path_parts) + '/chat/completions'
        else:
            path = '/chat/completions'
        conn = http.client.HTTPConnection(host)
    
    # 构建总结提示词
    summary_prompt = """请对以下聊天历史进行简要总结，提取关键信息和主题：

{chat_history}

总结要求：
1. 简洁明了，抓住核心内容
2. 保留重要的信息点
3. 忽略无关细节
4. 使用列表格式呈现主要内容"""
    
    # 构建聊天历史文本
    chat_history_text = ""
    for msg in chat_history:
        if msg.get('content'):
            if msg['role'] == 'user':
                chat_history_text += f"用户: {msg['content']}\n"
            elif msg['role'] == 'assistant':
                chat_history_text += f"助手: {msg['content']}\n"
    
    # 构建请求数据
    messages = [
        {"role": "system", "content": "你是一个专业的聊天记录总结助手，擅长提取关键信息并进行简洁总结。"},
        {"role": "user", "content": summary_prompt.format(chat_history=chat_history_text)}
    ]
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    # 构建请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # 发送请求
    try:
        conn.request('POST', path, json.dumps(data), headers)
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        conn.close()
        
        result = json.loads(response_data)
        if 'error' in result:
            print(f"总结错误：{result['error']['message']}")
            return chat_history
        
        summary = result['choices'][0]['message']['content']
        
        # 构建新的聊天历史
        new_chat_history = [
            {"role": "system", "content": f"聊天历史总结：\n{summary}"}
        ]
        
        # 保留最后30%的聊天记录
        total_messages = len(chat_history)
        if total_messages > 0:
            keep_count = max(1, int(total_messages * 0.3))
            new_chat_history.extend(chat_history[-keep_count:])
        
        return new_chat_history
        
    except Exception as e:
        print(f"总结失败：{str(e)}")
        return chat_history

def call_llm_with_tools(prompt, chat_history=None):
    """调用LLM并处理工具调用，支持聊天历史管理"""
    # 加载环境变量
    env_vars = load_env()
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', '')
    temperature = float(env_vars.get('TEMPERATURE', '0.7'))
    max_tokens = int(env_vars.get('MAX_TOKENS', '4000'))
    
    if not api_key:
        print("错误：API_KEY未设置")
        return chat_history
    
    # 初始化聊天历史
    if chat_history is None:
        chat_history = []
    
    # 添加用户消息
    chat_history.append({"role": "user", "content": prompt})
    
    # 检查是否需要总结聊天历史
    # 条件1：聊天轮数超过5轮
    # 条件2：聊天上下文长度超过3k tokens
    user_message_count = sum(1 for msg in chat_history if msg['role'] == 'user')
    
    # 计算上下文长度
    context_text = ""
    for msg in chat_history:
        if msg.get('content'):
            context_text += msg['content'] + "\n"
    context_tokens = calculate_tokens(context_text)
    
    if user_message_count > 5 or context_tokens > 3000:
        print("\n=== 检测到聊天历史过长，开始总结 ===")
        print(f"当前聊天轮数: {user_message_count}")
        print(f"当前上下文长度: {context_tokens} tokens")
        chat_history = summarize_chat_history(chat_history, env_vars)
        print("=== 聊天历史总结完成 ===\n")
    
    # 提取主机和路径
    if base_url.startswith('https://'):
        host = base_url[8:].split('/')[0]
        path_parts = base_url[8:].split('/')[1:]
        if path_parts:
            path = '/' + '/'.join(path_parts) + '/chat/completions'
        else:
            path = '/chat/completions'
        conn = http.client.HTTPSConnection(host)
    else:
        host = base_url[7:].split('/')[0]
        path_parts = base_url[7:].split('/')[1:]
        if path_parts:
            path = '/' + '/'.join(path_parts) + '/chat/completions'
        else:
            path = '/chat/completions'
        conn = http.client.HTTPConnection(host)
    
    # 系统提示词
    system_prompt = """你是一个智能助手，拥有以下工具调用能力：

1. list_files(directory): 列出某个目录下有哪些文件（包括文件的基本属性、大小等信息）
   - 参数：directory (string) - 要列出文件的目录路径
   - 返回：包含文件列表和状态的JSON对象

2. rename_file(directory, old_name, new_name): 修改某个目录下某个文件的名字
   - 参数：
     - directory (string) - 文件所在的目录路径
     - old_name (string) - 原文件名
     - new_name (string) - 新文件名
   - 返回：包含操作状态和路径信息的JSON对象

3. delete_file(directory, filename): 删除某个目录下的某个文件
   - 参数：
     - directory (string) - 文件所在的目录路径
     - filename (string) - 要删除的文件名
   - 返回：包含操作状态和文件路径的JSON对象

4. create_file(directory, filename, content): 在某个目录下新建1个文件，并且写入内容
   - 参数：
     - directory (string) - 要创建文件的目录路径
     - filename (string) - 要创建的文件名
     - content (string) - 要写入文件的内容
   - 返回：包含操作状态和文件路径的JSON对象

5. read_file(directory, filename): 读取某个目录下的某个文件的内容
   - 参数：
     - directory (string) - 文件所在的目录路径
     - filename (string) - 要读取的文件名
   - 返回：包含操作状态、文件路径和内容的JSON对象

6. curl(url): 通过curl访问网页并返回网页内容
   - 参数：
     - url (string) - 要访问的网页URL
   - 返回：包含操作状态、URL和网页内容的JSON对象

当用户请求需要使用这些工具时，请使用工具调用格式进行响应，不要直接猜测答案。"""
    
    # 构建请求数据
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    messages.extend(chat_history)
    
    data = {
        "model": model,
        "messages": messages,
        "tools": tools,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    # 构建请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # 发送请求并计时
    start_time = time.time()
    conn.request('POST', path, json.dumps(data), headers)
    response = conn.getresponse()
    end_time = time.time()
    
    # 计算耗时
    elapsed_time = end_time - start_time
    
    # 读取响应
    response_data = response.read().decode('utf-8')
    conn.close()
    
    # 解析响应
    try:
        result = json.loads(response_data)
        if 'error' in result:
            print(f"错误：{result['error']['message']}")
            return chat_history
        
        # 提取token使用情况
        usage = result.get('usage', {})
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        total_tokens = usage.get('total_tokens', 0)
        
        # 计算速度
        if elapsed_time > 0:
            tokens_per_second = total_tokens / elapsed_time
        else:
            tokens_per_second = 0
        
        # 检查是否需要工具调用
        choice = result['choices'][0]
        if choice.get('finish_reason') == 'tool_calls':
            # 处理工具调用
            tool_calls = choice.get('message', {}).get('tool_calls', [])
            if tool_calls:
                # 执行工具调用
                tool_responses = []
                for tool_call in tool_calls:
                    function_name = tool_call['function']['name']
                    arguments = json.loads(tool_call['function']['arguments'])
                    
                    print(f"\n执行工具调用: {function_name}")
                    print(f"参数: {arguments}")
                    
                    # 执行相应的工具函数
                    if function_name == 'list_files':
                        result = list_files(arguments['directory'])
                    elif function_name == 'rename_file':
                        result = rename_file(arguments['directory'], arguments['old_name'], arguments['new_name'])
                    elif function_name == 'delete_file':
                        result = delete_file(arguments['directory'], arguments['filename'])
                    elif function_name == 'create_file':
                        result = create_file(arguments['directory'], arguments['filename'], arguments['content'])
                    elif function_name == 'read_file':
                        result = read_file(arguments['directory'], arguments['filename'])
                    elif function_name == 'curl':
                        result = curl(arguments['url'])
                    else:
                        result = {"status": "error", "message": "未知工具"}
                    
                    print(f"工具执行结果: {result}")
                    
                    # 添加工具响应到消息列表
                    tool_responses.append({
                        "role": "tool",
                        "tool_call_id": tool_call['id'],
                        "name": function_name,
                        "content": json.dumps(result)
                    })
                
                # 添加助手消息（工具调用）
                chat_history.append(choice['message'])
                
                # 添加工具响应
                chat_history.extend(tool_responses)
                
                # 再次调用LLM，传入工具执行结果
                messages.extend(tool_responses)
                data['messages'] = messages
                
                # 发送第二次请求
                start_time2 = time.time()
                conn = http.client.HTTPSConnection(host) if base_url.startswith('https://') else http.client.HTTPConnection(host)
                conn.request('POST', path, json.dumps(data), headers)
                response2 = conn.getresponse()
                end_time2 = time.time()
                
                # 读取响应
                response_data2 = response2.read().decode('utf-8')
                conn.close()
                
                # 解析第二次响应
                result2 = json.loads(response_data2)
                if 'error' in result2:
                    print(f"错误：{result2['error']['message']}")
                    return chat_history
                
                # 提取第二次token使用情况
                usage2 = result2.get('usage', {})
                total_tokens2 = usage2.get('total_tokens', 0)
                elapsed_time2 = end_time2 - start_time2
                
                # 打印结果
                print("\n=== LLM调用结果 ===")
                print(f"总令牌数: {total_tokens2}")
                print(f"耗时: {elapsed_time2:.2f} 秒")
                print(f"速度: {total_tokens2 / elapsed_time2:.2f} tokens/秒")
                print("\n响应内容:")
                print(result2['choices'][0]['message']['content'])
                
                # 添加助手最终响应
                chat_history.append(result2['choices'][0]['message'])
        else:
            # 直接打印结果
            print("\n=== LLM调用结果 ===")
            print(f"提示词令牌数: {prompt_tokens}")
            print(f"完成令牌数: {completion_tokens}")
            print(f"总令牌数: {total_tokens}")
            print(f"耗时: {elapsed_time:.2f} 秒")
            print(f"速度: {tokens_per_second:.2f} tokens/秒")
            print("\n响应内容:")
            print(choice['message']['content'])
            
            # 添加助手响应
            chat_history.append(choice['message'])
        
    except json.JSONDecodeError:
        print("错误：响应解析失败")
        print(f"原始响应: {response_data}")
    except Exception as e:
        print(f"错误：{str(e)}")
    
    return chat_history

if __name__ == "__main__":
    print("=== 聊天记录总结示例 ===")
    
    # 初始化聊天历史
    chat_history = []
    
    # 模拟多轮对话
    print("\n=== 第1轮对话 ===")
    chat_history = call_llm_with_tools("你好，我想了解一下天气情况", chat_history)
    
    print("\n=== 第2轮对话 ===")
    chat_history = call_llm_with_tools("请帮我查询北京今天的天气", chat_history)
    
    print("\n=== 第3轮对话 ===")
    chat_history = call_llm_with_tools("那上海呢？", chat_history)
    
    print("\n=== 第4轮对话 ===")
    chat_history = call_llm_with_tools("广州的天气怎么样？", chat_history)
    
    print("\n=== 第5轮对话 ===")
    chat_history = call_llm_with_tools("深圳的天气如何？", chat_history)
    
    print("\n=== 第6轮对话（应该触发总结） ===")
    chat_history = call_llm_with_tools("杭州的天气怎么样？", chat_history)
    
    print("\n=== 第7轮对话 ===")
    chat_history = call_llm_with_tools("成都的天气如何？", chat_history)
    
    print("\n=== 对话结束 ===")
    print(f"最终聊天历史长度: {len(chat_history)} 条消息")