"""通知管理 Skill 实现

这个文件实现了通知管理Skill的核心功能，包括生成不同类型的通知。
"""

from typing import Dict, Any
import datetime

def generate_notice(department: str = None, title: str = "", content: str = "", 
                   notice_type: str = "other", effective_date: str = None, 
                   contact_person: str = "", contact_phone: str = "") -> Dict[str, Any]:
    """生成标准格式的通知
    
    Args:
        department: 部门名称，如果未提供则使用"xx部门"
        title: 通知标题
        content: 通知内容
        notice_type: 通知类型（meeting: 会议通知, activity: 活动通知, announcement: 公告通知, other: 其他）
        effective_date: 生效日期，格式为YYYY-MM-DD
        contact_person: 联系人
        contact_phone: 联系电话
    
    Returns:
        Dict[str, Any]: 包含生成的通知内容的字典
    """
    try:
        # 处理部门名称
        if not department:
            department = "xx部门"
        
        # 处理日期
        if effective_date:
            try:
                date_obj = datetime.datetime.strptime(effective_date, "%Y-%m-%d")
                date_str = date_obj.strftime("%Y年%m月%d日")
                date_short = effective_date
            except ValueError:
                # 如果日期格式错误，使用当前日期
                date_obj = datetime.datetime.now()
                date_str = date_obj.strftime("%Y年%m月%d日")
                date_short = date_obj.strftime("%Y-%m-%d")
        else:
            # 如果未提供日期，使用当前日期
            date_obj = datetime.datetime.now()
            date_str = date_obj.strftime("%Y年%m月%d日")
            date_short = date_obj.strftime("%Y-%m-%d")
        
        # 根据通知类型生成不同格式的通知
        if notice_type == "meeting":
            notice = generate_meeting_notice(department, title, content, date_str, contact_person, contact_phone)
        elif notice_type == "activity":
            notice = generate_activity_notice(department, title, content, date_str, contact_person, contact_phone)
        elif notice_type == "announcement":
            notice = generate_announcement_notice(department, title, content, date_str, contact_person, contact_phone)
        else:
            notice = generate_general_notice(department, title, content, date_str, contact_person, contact_phone)
        
        return {
            "status": "success",
            "notice": notice,
            "department": department,
            "title": title,
            "notice_type": notice_type,
            "effective_date": date_short
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def generate_general_notice(department: str, title: str, content: str, 
                           date_str: str, contact_person: str, contact_phone: str) -> str:
    """生成通用格式的通知
    
    Args:
        department: 部门名称
        title: 通知标题
        content: 通知内容
        date_str: 日期字符串
        contact_person: 联系人
        contact_phone: 联系电话
    
    Returns:
        str: 生成的通知内容
    """
    notice = f"【{department}】{title}\n\n"
    notice += f"{content}\n\n"
    
    if contact_person:
        notice += f"联系人：{contact_person}\n"
    if contact_phone:
        notice += f"联系电话：{contact_phone}\n"
    
    notice += f"日期：{date_str}"
    
    return notice

def generate_meeting_notice(department: str, title: str, content: str, 
                           date_str: str, contact_person: str, contact_phone: str) -> str:
    """生成会议通知
    
    Args:
        department: 部门名称
        title: 通知标题
        content: 通知内容
        date_str: 日期字符串
        contact_person: 联系人
        contact_phone: 联系电话
    
    Returns:
        str: 生成的通知内容
    """
    notice = f"【{department}】{title}\n\n"
    notice += "各相关单位：\n\n"
    notice += f"{content}\n\n"
    
    if contact_person:
        notice += f"联系人：{contact_person}\n"
    if contact_phone:
        notice += f"联系电话：{contact_phone}\n"
    
    notice += f"{department}\n"
    notice += f"{date_str}"
    
    return notice

def generate_activity_notice(department: str, title: str, content: str, 
                           date_str: str, contact_person: str, contact_phone: str) -> str:
    """生成活动通知
    
    Args:
        department: 部门名称
        title: 通知标题
        content: 通知内容
        date_str: 日期字符串
        contact_person: 联系人
        contact_phone: 联系电话
    
    Returns:
        str: 生成的通知内容
    """
    notice = f"【{department}】{title}\n\n"
    notice += "全体员工：\n\n"
    notice += f"{content}\n\n"
    
    if contact_person:
        notice += f"联系人：{contact_person}\n"
    if contact_phone:
        notice += f"联系电话：{contact_phone}\n"
    
    notice += f"{department}\n"
    notice += f"{date_str}"
    
    return notice

def generate_announcement_notice(department: str, title: str, content: str, 
                           date_str: str, contact_person: str, contact_phone: str) -> str:
    """生成公告通知
    
    Args:
        department: 部门名称
        title: 通知标题
        content: 通知内容
        date_str: 日期字符串
        contact_person: 联系人
        contact_phone: 联系电话
    
    Returns:
        str: 生成的通知内容
    """
    notice = f"【{department}】{title}\n\n"
    notice += "全体员工：\n\n"
    notice += f"{content}\n\n"
    notice += "特此公告。\n\n"
    
    if contact_person:
        notice += f"联系人：{contact_person}\n"
    if contact_phone:
        notice += f"联系电话：{contact_phone}\n"
    
    notice += f"{department}\n"
    notice += f"{date_str}"
    
    return notice

# 工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_notice",
            "description": "生成标准格式的通知",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "部门名称，如果未提供则使用\"xx部门\""
                    },
                    "title": {
                        "type": "string",
                        "description": "通知标题"
                    },
                    "content": {
                        "type": "string",
                        "description": "通知内容"
                    },
                    "notice_type": {
                        "type": "string",
                        "description": "通知类型（meeting: 会议通知, activity: 活动通知, announcement: 公告通知, other: 其他）",
                        "enum": ["meeting", "activity", "announcement", "other"]
                    },
                    "effective_date": {
                        "type": "string",
                        "description": "生效日期，格式为YYYY-MM-DD"
                    },
                    "contact_person": {
                        "type": "string",
                        "description": "联系人"
                    },
                    "contact_phone": {
                        "type": "string",
                        "description": "联系电话"
                    }
                },
                "required": ["title", "content", "notice_type"]
            }
        }
    }
]

if __name__ == "__main__":
    # 测试代码
    print("=== 测试通知管理Skill ===")
    
    # 测试1：生成会议通知（指定部门）
    print("\n1. 测试生成会议通知（指定部门）：")
    result1 = generate_notice(
        department="人力资源部",
        title="关于召开2026年第二季度工作会议的通知",
        content="为了总结2026年第二季度工作情况，部署第三季度工作计划，现决定召开部门工作会议。会议时间：2026年7月15日 14:00，会议地点：公司会议室A，参会人员：全体部门成员，会议内容：1. 第二季度工作汇报 2. 第三季度工作计划 3. 团队建设讨论",
        notice_type="meeting",
        effective_date="2026-07-10",
        contact_person="张三",
        contact_phone="13800138000"
    )
    print(f"状态: {result1.get('status')}")
    if 'notice' in result1:
        print(result1['notice'])
    else:
        print(f"错误: {result1.get('message', '未知错误')}")
    
    # 测试2：生成活动通知（未指定部门）
    print("\n2. 测试生成活动通知（未指定部门）：")
    result2 = generate_notice(
        title="关于举办公司年度团建活动的通知",
        content="为了增强团队凝聚力，促进员工之间的交流，现决定举办公司年度团建活动。活动时间：2026年8月1日 9:00-17:00，活动地点：郊外拓展基地，参与人员：全体员工，活动内容：拓展训练、团队游戏、烧烤晚会，报名方式：各部门负责人统一报名",
        notice_type="activity",
        effective_date="2026-07-20",
        contact_person="李四",
        contact_phone="13900139000"
    )
    print(f"状态: {result2.get('status')}")
    if 'notice' in result2:
        print(result2['notice'])
    else:
        print(f"错误: {result2.get('message', '未知错误')}")
    
    # 测试3：生成公告通知
    print("\n3. 测试生成公告通知：")
    result3 = generate_notice(
        department="行政部",
        title="关于公司作息时间调整的公告",
        content="为了适应季节变化，提高工作效率，公司决定从2026年5月1日起调整作息时间。调整后的工作时间为：上午9:00-12:00，下午13:30-17:30。请全体员工知悉并遵守。",
        notice_type="announcement",
        effective_date="2026-04-20"
    )
    print(f"状态: {result3.get('status')}")
    if 'notice' in result3:
        print(result3['notice'])
    else:
        print(f"错误: {result3.get('message', '未知错误')}")
    
    # 测试4：生成其他类型通知
    print("\n4. 测试生成其他类型通知：")
    result4 = generate_notice(
        department="技术部",
        title="关于系统升级的通知",
        content="为了提供更好的服务，我们将于2026年4月30日凌晨进行系统升级，届时系统将暂时无法访问，请各位用户提前做好准备。",
        notice_type="other",
        effective_date="2026-04-25",
        contact_person="王五",
        contact_phone="13700137000"
    )
    print(f"状态: {result4.get('status')}")
    if 'notice' in result4:
        print(result4['notice'])
    else:
        print(f"错误: {result4.get('message', '未知错误')}")
    
    print("\n=== 测试完成 ===")
