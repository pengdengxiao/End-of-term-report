import os
import json
import http.client
import time
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

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

# ========== 新增：链式调用上下文管理器 ==========
class ChainedCallContext:
    """
    链式工具调用的上下文管理器，用于管理调用状态和中间变量。
    
    核心功能：
    - 记录每步工具调用（含工具名、参数、结果、时间戳）
    - 存储中间变量，支持跨步骤读取
    - 控制最大迭代次数，防止无限循环
    """
    
    def __init__(self, max_iterations: int = 5):
        """
        初始化上下文管理器。
        
        Args:
            max_iterations: 最大迭代次数，默认5次
        """
        self.steps: List[Dict] = []  # 记录每步工具调用
        self.variables: Dict[str, Any] = {}  # 存储中间变量
        self.max_iterations: int = max_iterations
    
    def add_step(self, tool_name: str, arguments: Dict, result: Dict) -> None:
        """
        添加步骤记录。
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            result: 工具执行结果
        """
        self.steps.append({
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        })
    
    def set_variable(self, key: str, value: Any) -> None:
        """
        存储中间变量。
        
        Args:
            key: 变量名
            value: 变量值
        """
        self.variables[key] = value
    
    def get_variable(self, key: str, default: Any = None) -> Any:
        """
        获取中间变量，变量不存在时返回默认值。
        
        Args:
            key: 变量名
            default: 默认值，默认为None
        
        Returns:
            变量值或默认值
        """
        return self.variables.get(key, default)
    
    def is_max_iterations_reached(self) -> bool:
        """
        判断是否达到最大迭代次数。
        
        Returns:
            True表示已达到最大迭代次数，False表示未达到
        """
        return len(self.steps) >= self.max_iterations
    
    def get_steps_summary(self) -> str:
        """
        获取步骤摘要，用于构建提示词。
        
        Returns:
            格式化的步骤摘要字符串
        """
        if not self.steps:
            return "暂无执行步骤"
        
        summary = "已执行步骤：\n"
        for i, step in enumerate(self.steps, 1):
            summary += f"{i}. [{step['timestamp']}] {step['tool_name']}({step['arguments']}) -> {'成功' if step['result'].get('status') == 'success' else '失败'}\n"
        
        return summary

# ========== 新增：构建分析提示词函数 ==========
def build_analysis_prompt(user_prompt: str, context: ChainedCallContext) -> str:
    """
    构建链式调用分析提示词。
    
    Args:
        user_prompt: 用户原始需求
        context: 链式调用上下文
    
    Returns:
        完整的分析提示词
    """
    # 获取已执行步骤
    steps_summary = context.get_steps_summary()
    
    # 获取可用变量列表
    variables_summary = "可用中间变量：\n"
    if context.variables:
        for key, value in context.variables.items():
            # 对长内容进行截断
            if isinstance(value, str) and len(value) > 50:
                value = value[:50] + "..."
            variables_summary += f"- {key}: {value}\n"
    else:
        variables_summary += "暂无中间变量\n"
    
    prompt = f"""
你是资深Python工程师，精通LLM工具调用和链式执行逻辑。请分析用户需求，决定下一步操作。

## 用户原始需求
{user_prompt}

## {steps_summary}

## {variables_summary}

## 决策规则
1. 优先使用 context.variables 中的中间变量进行决策
2. 工具调用失败时重试1次，重试失败则终止任务
3. 已有的工具执行结果存储在 context.steps 中，可以参考

## 链式调用示例
### 示例1：网页处理流程
步骤1: curl(url) -> 结果存入 web_content
步骤2: 分析 web_content 进行总结 -> 结果存入 summary
步骤3: create_file(directory, filename, summary)

### 示例2：多文件操作流程
步骤1: read_file(directory, "1.txt") -> 结果存入 num1
步骤2: read_file(directory, "2.txt") -> 结果存入 num2
步骤3: 计算 num1 + num2 -> 结果存入 sum_result
步骤4: create_file(directory, "result.txt", sum_result)

## 输出格式要求
请严格按照以下JSON格式输出，禁止任何额外内容：

### 任务完成
{{"done": true, "answer": "最终回答内容"}}

### 继续调用工具
{{"done": false, "tool_call": {{"name": "工具名", "arguments": {{"参数名": "值"}}}}}}

注意：
- 工具名必须是已定义的工具：list_files, rename_file, delete_file, create_file, read_file, curl, list_available_skills, load_skill_content
- 参数必须符合工具定义的要求
- 如果需要使用中间变量，请从 context.variables 中读取
"""
    
    return prompt.strip()

# ========== 新增：执行链式工具调用函数 ==========
def execute_chained_tool_call(user_prompt: str, max_iterations: int = 5) -> Dict:
    """
    执行链式工具调用，实现"前一个工具输出作为后一个工具输入"的自主决策流程。
    
    Args:
        user_prompt: 用户原始需求
        max_iterations: 最大迭代次数，默认5次
    
    Returns:
        执行结果字典，包含状态、答案和步骤记录
    """
    # 初始化上下文
    context = ChainedCallContext(max_iterations=max_iterations)
    
    print(f"\n=== 开始链式工具调用 ===")
    print(f"用户需求: {user_prompt}")
    print(f"最大迭代次数: {max_iterations}")
    
    # 循环执行
    while not context.is_max_iterations_reached():
        print(f"\n--- 迭代 {len(context.steps) + 1} ---")
        
        # 构建分析提示词
        analysis_prompt = build_analysis_prompt(user_prompt, context)
        
        # 调用LLM分析
        llm_response = _call_llm_for_chained(analysis_prompt)
        
        if llm_response is None:
            return {"status": "error", "message": "LLM调用失败", "steps": context.steps}
        
        # 解析LLM响应
        try:
            response_data = json.loads(llm_response)
        except json.JSONDecodeError:
            print(f"JSON解析失败，原始响应: {llm_response}")
            return {"status": "error", "message": f"LLM响应格式错误: {llm_response}", "steps": context.steps}
        
        # 检查是否完成
        if response_data.get("done"):
            print(f"任务完成: {response_data.get('answer')}")
            return {
                "status": "success",
                "answer": response_data.get("answer"),
                "steps": context.steps
            }
        
        # 执行工具调用
        tool_call = response_data.get("tool_call")
        if not tool_call:
            return {"status": "error", "message": "LLM响应缺少tool_call字段", "steps": context.steps}
        
        tool_name = tool_call.get("name")
        arguments = tool_call.get("arguments", {})
        
        print(f"执行工具: {tool_name}")
        print(f"工具参数: {arguments}")
        
        # 执行工具（支持重试1次）
        result = None
        for attempt in range(2):
            result = _execute_tool(tool_name, arguments)
            
            if result.get("status") == "success":
                break
            
            print(f"工具执行失败(尝试 {attempt + 1}/2): {result.get('message')}")
            if attempt == 0:
                print("正在重试...")
        
        # 记录步骤
        context.add_step(tool_name, arguments, result)
        
        # 如果工具执行失败，终止并返回错误
        if result.get("status") != "success":
            error_msg = f"工具调用失败: {result.get('message')}"
            print(f"终止任务: {error_msg}")
            return {"status": "error", "message": error_msg, "steps": context.steps}
        
        # 将工具结果存入中间变量
        _store_tool_result(context, tool_name, result)
        
        print(f"工具执行成功")
        print(f"当前中间变量: {context.variables.keys()}")
    
    # 达到最大迭代次数
    return {"status": "error", "message": f"达到最大迭代次数({max_iterations})，任务未完成", "steps": context.steps}

def _call_llm_for_chained(prompt: str) -> Optional[str]:
    """
    内部函数：调用LLM进行链式分析。
    
    Args:
        prompt: 分析提示词
    
    Returns:
        LLM响应内容，失败返回None
    """
    env_vars = load_env()
    base_url = env_vars.get('BASE_URL', 'https://api.openai.com/v1')
    model = env_vars.get('MODEL', 'gpt-3.5-turbo')
    api_key = env_vars.get('API_KEY', '')
    
    if not api_key:
        print("错误：API_KEY未设置")
        return None
    
    # 提取主机和路径
    if base_url.startswith('https://'):
        host = base_url[8:].split('/')[0]
        path_parts = base_url[8:].split('/')[1:]
        path = '/' + '/'.join(path_parts) + '/chat/completions' if path_parts else '/chat/completions'
        conn = http.client.HTTPSConnection(host)
    else:
        host = base_url[7:].split('/')[0]
        path_parts = base_url[7:].split('/')[1:]
        path = '/' + '/'.join(path_parts) + '/chat/completions' if path_parts else '/chat/completions'
        conn = http.client.HTTPConnection(host)
    
    # 系统提示词（简化版，仅专注于链式调用）
    system_prompt = """你是一个智能助手，专门用于分析和决策链式工具调用。
    你需要根据用户需求和已执行步骤，决定下一步操作。
    请严格按照指定的JSON格式输出，禁止任何额外内容。
    可用工具：list_files, rename_file, delete_file, create_file, read_file, curl, list_available_skills, load_skill_content"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,  # 降低随机性，确保决策一致性
        "max_tokens": 1000
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        conn.request('POST', path, json.dumps(data, ensure_ascii=False).encode('utf-8'), headers)
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        conn.close()
        
        result = json.loads(response_data)
        if 'error' in result:
            print(f"LLM错误: {result['error']['message']}")
            return None
        
        return result['choices'][0]['message']['content']
    
    except Exception as e:
        print(f"LLM调用异常: {str(e)}")
        return None

def _execute_tool(tool_name: str, arguments: Dict) -> Dict:
    """
    内部函数：执行工具调用。
    
    Args:
        tool_name: 工具名称
        arguments: 工具参数
    
    Returns:
        工具执行结果
    """
    try:
        if tool_name == 'list_files':
            return list_files(arguments['directory'])
        elif tool_name == 'rename_file':
            return rename_file(arguments['directory'], arguments['old_name'], arguments['new_name'])
        elif tool_name == 'delete_file':
            return delete_file(arguments['directory'], arguments['filename'])
        elif tool_name == 'create_file':
            return create_file(arguments['directory'], arguments['filename'], arguments['content'])
        elif tool_name == 'read_file':
            return read_file(arguments['directory'], arguments['filename'])
        elif tool_name == 'curl':
            return curl(arguments['url'])
        elif tool_name == 'list_available_skills':
            return list_available_skills()
        elif tool_name == 'load_skill_content':
            return load_skill_content(arguments['skill_name'])
        else:
            return {"status": "error", "message": f"未知工具: {tool_name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def _store_tool_result(context: ChainedCallContext, tool_name: str, result: Dict) -> None:
    """
    内部函数：将工具执行结果存入上下文变量。
    
    Args:
        context: 链式调用上下文
        tool_name: 工具名称
        result: 工具执行结果
    """
    if result.get("status") != "success":
        return
    
    # 根据不同工具类型存储不同的变量
    if tool_name == "curl":
        context.set_variable("web_content", result.get("content", ""))
        context.set_variable("last_url", result.get("url", ""))
    elif tool_name == "read_file":
        context.set_variable("file_content", result.get("content", ""))
        context.set_variable("last_file_path", result.get("file_path", ""))
    elif tool_name == "list_files":
        context.set_variable("file_list", result.get("files", []))
        context.set_variable("last_directory", result.get("directory", ""))
    elif tool_name == "create_file":
        context.set_variable("last_created_file", result.get("file_path", ""))
    elif tool_name == "list_available_skills":
        context.set_variable("available_skills", result.get("skills", []))
    elif tool_name == "load_skill_content":
        context.set_variable("skill_content", result.get("content", ""))
        context.set_variable("last_skill_name", result.get("skill_name", ""))
    
    # 通用变量：存储最后一次工具结果
    context.set_variable("last_result", result)

def call_llm_with_tools(prompt):
    """调用LLM并处理工具调用（原有函数，保持兼容）"""
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
    
    # 系统提示词（新增链式调用规则）
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

## 链式调用规则
1. 可基于中间变量（context.variables）决策下一步工具，无需用户干预
2. 步骤依赖示例：
   - 网页处理：curl获取内容（存web_content）→ 总结内容（读web_content）→ create_file保存
   - 多文件操作：read_file 1.txt（存num1）→ read_file 2.txt（存num2）→ 计算和 → create_file写入

## JSON输出要求
请严格按以下格式返回，禁止额外内容：
- 任务完成：{{"done": true, "answer": "最终回答内容"}}
- 继续调用：{{"done": false, "tool_call": {{"name": "工具名", "arguments": {{"参数名": "值"}}}}}}

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

# ========== 测试代码 ==========
def prepare_test_data():
    """准备测试数据（创建1.txt和2.txt文件）"""
    test_dir = os.path.dirname(__file__)
    
    # 创建1.txt
    with open(os.path.join(test_dir, "1.txt"), 'w', encoding='utf-8') as f:
        f.write("42")
    
    # 创建2.txt
    with open(os.path.join(test_dir, "2.txt"), 'w', encoding='utf-8') as f:
        f.write("18")
    
    print(f"测试数据已准备完成，目录: {test_dir}")

def test_chained_call_file_search():
    """测试1：文件搜索链式调用（查找practice06目录下含'def'的文件并总结）"""
    print("\n" + "="*60)
    print("测试1：文件搜索链式调用")
    print("="*60)
    
    user_prompt = "查找practice06目录下包含'def'关键字的Python文件，并总结这些文件的功能"
    
    try:
        result = execute_chained_tool_call(user_prompt, max_iterations=5)
        print(f"\n测试1执行结果:")
        print(f"状态: {result.get('status')}")
        print(f"答案: {result.get('answer')}")
        print(f"步骤记录:")
        for i, step in enumerate(result.get('steps', []), 1):
            print(f"  {i}. {step['tool_name']} -> {'成功' if step['result'].get('status') == 'success' else '失败'}")
    except Exception as e:
        print(f"测试1执行失败: {str(e)}")

def test_chained_call_multi_file():
    """测试2：多文件操作（读取1.txt和2.txt的正整数，相加写入result.txt）"""
    print("\n" + "="*60)
    print("测试2：多文件操作")
    print("="*60)
    
    # 准备测试数据
    prepare_test_data()
    
    current_dir = os.path.dirname(__file__)
    user_prompt = f"读取目录{current_dir}下的1.txt和2.txt文件，将两个文件中的数字相加，然后将结果写入result.txt文件"
    
    try:
        result = execute_chained_tool_call(user_prompt, max_iterations=5)
        print(f"\n测试2执行结果:")
        print(f"状态: {result.get('status')}")
        print(f"答案: {result.get('answer')}")
        print(f"步骤记录:")
        for i, step in enumerate(result.get('steps', []), 1):
            print(f"  {i}. {step['tool_name']} -> {'成功' if step['result'].get('status') == 'success' else '失败'}")
        
        # 验证结果
        result_file = os.path.join(current_dir, "result.txt")
        if os.path.exists(result_file):
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"\nresult.txt内容: {content}")
    except Exception as e:
        print(f"测试2执行失败: {str(e)}")

def test_chained_call_web_summary():
    """测试3：网页处理（访问网页，总结后保存到practice07/summary.txt）"""
    print("\n" + "="*60)
    print("测试3：网页处理")
    print("="*60)
    
    user_prompt = "访问网页https://www.nsu.edu.cn/HTML/news/2024/06/article_3974.html，获取内容后进行总结，然后将总结保存到practice07/summary.txt文件"
    
    try:
        result = execute_chained_tool_call(user_prompt, max_iterations=5)
        print(f"\n测试3执行结果:")
        print(f"状态: {result.get('status')}")
        print(f"答案: {result.get('answer')}")
        print(f"步骤记录:")
        for i, step in enumerate(result.get('steps', []), 1):
            print(f"  {i}. {step['tool_name']} -> {'成功' if step['result'].get('status') == 'success' else '失败'}")
        
        # 验证结果
        summary_file = os.path.join(os.path.dirname(__file__), "summary.txt")
        if os.path.exists(summary_file):
            with open(summary_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"\nsummary.txt内容: {content[:500]}..." if len(content) > 500 else f"\nsummary.txt内容: {content}")
    except Exception as e:
        print(f"测试3执行失败: {str(e)}")

if __name__ == "__main__":
    print("=== 链式工具调用测试 ===")
    
    # 测试1：文件搜索链式调用
    test_chained_call_file_search()
    
    # 测试2：多文件操作
    test_chained_call_multi_file()
    
    # 测试3：网页处理
    test_chained_call_web_summary()
    
    print("\n=== 测试完成 ===")
