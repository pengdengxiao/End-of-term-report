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

def list_available_skills():
    """读取所有可用的技能"""
    try:
        skills_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.agents', 'skills')
        skills = []
        
        if os.path.exists(skills_dir):
            # 遍历所有一级子目录
            for skill_dir in os.listdir(skills_dir):
                skill_path = os.path.join(skills_dir, skill_dir)
                if os.path.isdir(skill_path):
                    # 读取SKILL.md文件
                    skill_file = os.path.join(skill_path, 'SKILL.md')
                    if os.path.exists(skill_file):
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 提取YAML front matter
                        if content.startswith('---'):
                            front_matter_end = content.find('---', 3)
                            if front_matter_end != -1:
                                front_matter = content[3:front_matter_end].strip()
                                # 解析YAML front matter
                                name = skill_dir
                                description = ""
                                for line in front_matter.split('\n'):
                                    line = line.strip()
                                    if line.startswith('name:'):
                                        name = line[5:].strip().strip('"\'')
                                    elif line.startswith('description:'):
                                        description = line[12:].strip().strip('"\'')
                                if name:
                                    skills.append({"name": name, "description": description, "dir": skill_dir})
        
        return {
            "status": "success",
            "skills": skills
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def load_skill_content(skill_name):
    """加载技能的内容"""
    try:
        skills_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.agents', 'skills')
        
        # 先获取所有技能信息
        skills_result = list_available_skills()
        skill_dir = None
        
        for skill in skills_result.get("skills", []):
            if skill.get("name") == skill_name:
                skill_dir = skill.get("dir")
                break
        
        # 如果找不到技能，尝试直接使用skill_name作为目录名
        if not skill_dir:
            skill_dir = skill_name
        
        skill_path = os.path.join(skills_dir, skill_dir)
        
        if os.path.exists(skill_path) and os.path.isdir(skill_path):
            # 读取SKILL.md文件
            skill_file = os.path.join(skill_path, 'SKILL.md')
            if os.path.exists(skill_file):
                with open(skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取YAML front matter之后的内容
                if content.startswith('---'):
                    front_matter_end = content.find('---', 3)
                    if front_matter_end != -1:
                        content = content[front_matter_end + 3:].strip()
                
                return {
                    "status": "success",
                    "skill_name": skill_name,
                    "content": content
                }
            else:
                return {
                    "status": "error",
                    "message": "SKILL.md文件不存在"
                }
        else:
            return {
                "status": "error",
                "message": "技能不存在"
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
    },
    {
        "type": "function",
        "function": {
            "name": "list_available_skills",
            "description": "列出所有可用的技能",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "load_skill_content",
            "description": "加载指定技能的内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "技能名称"
                    }
                },
                "required": ["skill_name"]
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

def call_llm_with_tools(prompt):
    """调用LLM并处理工具调用"""
    # 加载环境变量
    env_vars = load_env()
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', '')
    temperature = float(env_vars.get('TEMPERATURE', '0.7'))
    max_tokens = int(env_vars.get('MAX_TOKENS', '4000'))
    
    if not api_key:
        print("错误：API_KEY未设置")
        return
    
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
    
    # 读取可用技能
    skills_result = list_available_skills()
    # 移除dir字段，只保留name和description
    skills_for_json = []
    for skill in skills_result.get("skills", []):
        skills_for_json.append({"name": skill.get("name"), "description": skill.get("description")})
    skills_json = json.dumps({"skills": skills_for_json}, ensure_ascii=False, indent=2)
    
    # 系统提示词
    system_prompt = f"""你是一个智能助手，拥有以下工具调用能力：

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

7. list_available_skills(): 列出所有可用的技能
   - 参数：无
   - 返回：包含技能列表的JSON对象

8. load_skill_content(skill_name): 加载指定技能的内容
   - 参数：
     - skill_name (string) - 技能名称
   - 返回：包含技能内容的JSON对象

可用技能列表：
```json
{skills_json}
```

重要指令：
1. 当用户请求加载某个技能的内容时，你必须：
   - 首先调用 list_available_skills() 获取可用技能列表
   - 然后调用 load_skill_content(skill_name) 加载该技能的详细内容
   - 最后根据加载的技能内容为用户提供响应

2. 当用户请求使用某个技能时，你必须：
   - 首先调用 list_available_skills() 获取可用技能列表
   - 然后调用 load_skill_content(skill_name) 加载该技能的详细内容
   - 最后根据加载的技能内容为用户提供相应的服务

3. 当用户的请求涉及技能时，你必须使用工具调用格式进行响应，不要直接猜测答案。

请严格按照上述步骤执行，确保正确使用技能管理工具。"""
    
    # 构建请求数据
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
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
    conn.request('POST', path, json.dumps(data, ensure_ascii=False).encode('utf-8'), headers)
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
            return
        
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
                    elif function_name == 'list_available_skills':
                        result = list_available_skills()
                    elif function_name == 'load_skill_content':
                        result = load_skill_content(arguments['skill_name'])
                    else:
                        result = {"status": "error", "message": "未知工具"}
                    
                    print(f"工具执行结果: {result}")
                    
                    # 添加工具响应到消息列表
                    tool_responses.append({
                        "role": "tool",
                        "tool_call_id": tool_call['id'],
                        "name": function_name,
                        "content": json.dumps(result, ensure_ascii=False)
                    })
                
                # 再次调用LLM，传入工具执行结果
                messages.extend(tool_responses)
                data['messages'] = messages
                
                # 发送第二次请求
                start_time2 = time.time()
                conn = http.client.HTTPSConnection(host) if base_url.startswith('https://') else http.client.HTTPConnection(host)
                conn.request('POST', path, json.dumps(data, ensure_ascii=False).encode('utf-8'), headers)
                response2 = conn.getresponse()
                end_time2 = time.time()
                
                # 读取响应
                response_data2 = response2.read().decode('utf-8')
                conn.close()
                
                # 解析第二次响应
                try:
                    result2 = json.loads(response_data2)
                    if 'error' in result2:
                        print(f"错误：{result2['error']['message']}")
                        return
                    
                    # 提取第二次token使用情况
                    usage2 = result2.get('usage', {})
                    total_tokens2 = usage2.get('total_tokens', 0)
                    elapsed_time2 = end_time2 - start_time2
                    
                    # 检查是否需要再次工具调用
                    choice2 = result2['choices'][0]
                    if choice2.get('finish_reason') == 'tool_calls':
                        # 处理嵌套工具调用
                        tool_calls2 = choice2.get('message', {}).get('tool_calls', [])
                        if tool_calls2:
                            # 执行工具调用
                            tool_responses2 = []
                            for tool_call2 in tool_calls2:
                                function_name2 = tool_call2['function']['name']
                                arguments2 = json.loads(tool_call2['function']['arguments'])
                                
                                print(f"\n执行工具调用: {function_name2}")
                                print(f"参数: {arguments2}")
                                
                                # 执行相应的工具函数
                                if function_name2 == 'list_files':
                                    result2 = list_files(arguments2['directory'])
                                elif function_name2 == 'rename_file':
                                    result2 = rename_file(arguments2['directory'], arguments2['old_name'], arguments2['new_name'])
                                elif function_name2 == 'delete_file':
                                    result2 = delete_file(arguments2['directory'], arguments2['filename'])
                                elif function_name2 == 'create_file':
                                    result2 = create_file(arguments2['directory'], arguments2['filename'], arguments2['content'])
                                elif function_name2 == 'read_file':
                                    result2 = read_file(arguments2['directory'], arguments2['filename'])
                                elif function_name2 == 'curl':
                                    result2 = curl(arguments2['url'])
                                elif function_name2 == 'list_available_skills':
                                    result2 = list_available_skills()
                                elif function_name2 == 'load_skill_content':
                                    result2 = load_skill_content(arguments2['skill_name'])
                                else:
                                    result2 = {"status": "error", "message": "未知工具"}
                                
                                print(f"工具执行结果: {result2}")
                                
                                # 添加工具响应到消息列表
                                tool_responses2.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call2['id'],
                                    "name": function_name2,
                                    "content": json.dumps(result2, ensure_ascii=False)
                                })
                            
                            # 再次调用LLM，传入工具执行结果
                            messages.extend(tool_responses2)
                            data['messages'] = messages
                            
                            # 发送第三次请求
                            start_time3 = time.time()
                            conn = http.client.HTTPSConnection(host) if base_url.startswith('https://') else http.client.HTTPConnection(host)
                            conn.request('POST', path, json.dumps(data, ensure_ascii=False).encode('utf-8'), headers)
                            response3 = conn.getresponse()
                            end_time3 = time.time()
                            
                            # 读取响应
                            response_data3 = response3.read().decode('utf-8')
                            conn.close()
                            
                            # 解析第三次响应
                            result3 = json.loads(response_data3)
                            if 'error' in result3:
                                print(f"错误：{result3['error']['message']}")
                                return
                            
                            # 提取第三次token使用情况
                            usage3 = result3.get('usage', {})
                            total_tokens3 = usage3.get('total_tokens', 0)
                            elapsed_time3 = end_time3 - start_time3
                            
                            # 打印结果
                            print("\n=== LLM调用结果 ===")
                            print(f"总令牌数: {total_tokens3}")
                            print(f"耗时: {elapsed_time3:.2f} 秒")
                            print(f"速度: {total_tokens3 / elapsed_time3:.2f} tokens/秒")
                            print("\n响应内容:")
                            print(result3['choices'][0]['message']['content'])
                        else:
                            # 直接打印结果
                            print("\n=== LLM调用结果 ===")
                            print(f"总令牌数: {total_tokens2}")
                            print(f"耗时: {elapsed_time2:.2f} 秒")
                            print(f"速度: {total_tokens2 / elapsed_time2:.2f} tokens/秒")
                            print("\n响应内容:")
                            print(choice2['message']['content'])
                    else:
                        # 直接打印结果
                        print("\n=== LLM调用结果 ===")
                        print(f"总令牌数: {total_tokens2}")
                        print(f"耗时: {elapsed_time2:.2f} 秒")
                        print(f"速度: {total_tokens2 / elapsed_time2:.2f} tokens/秒")
                        print("\n响应内容:")
                        print(choice2['message']['content'])
                except json.JSONDecodeError:
                    print("错误：响应解析失败")
                    print(f"原始响应: {response_data2}")
                except Exception as e:
                    print(f"错误：{str(e)}")
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
        
    except json.JSONDecodeError:
        print("错误：响应解析失败")
        print(f"原始响应: {response_data}")
    except Exception as e:
        print(f"错误：{str(e)}")

# if __name__ == "__main__":
#     print("=== 技能调用示例 ===")
    
#     # 测试列出可用技能
#     print("\n示例1: 列出可用技能")
#     call_llm_with_tools("请列出所有可用的技能")
    
#     # 测试加载技能内容
#     print("\n示例2: 加载通知管理技能内容")
#     call_llm_with_tools("请加载通知管理技能的详细内容")
    
#     # 测试使用通知管理技能
#     print("\n示例3: 使用通知管理技能")
#     call_llm_with_tools("请先加载通知管理技能的内容，然后根据技能内容生成一个会议通知，部门是人力资源部，标题是关于召开2026年第二季度工作会议的通知，内容是为了总结2026年第二季度工作情况，部署第三季度工作计划，现决定召开部门工作会议。会议时间：2026年7月15日 14:00，会议地点：公司会议室A，参会人员：全体部门成员，会议内容：1. 第二季度工作汇报 2. 第三季度工作计划 3. 团队建设讨论")
if __name__ == "__main__":
    print("=== LLM工具调用系统（输入 '退出' 结束）===")
    while True:
        # 接收你在终端输入的自然语言指令
        user_input = input("\n请输入你的指令：")
        # 输入“退出”则关闭程序
        if user_input.strip() == "退出":
            print("程序结束！")
            break
        # 调用核心函数，执行你的指令
        call_llm_with_tools(user_input)