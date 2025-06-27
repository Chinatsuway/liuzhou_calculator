import csv
import json
import os

def StructureCharacter():
    """
    构建角色数据结构
    
    返回:
        list: 包含所有角色数据的列表，每个角色是一个字典
    """
    # 定义文件路径 - 注意路径已调整为相对位置
    csv_path = './liuzhou_calculator/Files/Characters.csv'
    skills_json_path = './liuzhou_calculator/Files/Skills.json'
    stats_json_path = './liuzhou_calculator/Files/Stats.json'
    
    # 确保文件存在
    if not os.path.exists(csv_path):
        print(f"错误：CSV文件路径 {csv_path} 不存在")
        return []
    if not os.path.exists(skills_json_path):
        print(f"错误：技能JSON文件路径 {skills_json_path} 不存在")
        return []
    if not os.path.exists(stats_json_path):
        print(f"错误：属性JSON文件路径 {stats_json_path} 不存在")
        return []
    
    # 读取角色-技能CSV文件
    characters_skills = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) < 2:
                    continue
                character, skill = row[0].strip(), row[1].strip()
                if character not in characters_skills:
                    characters_skills[character] = []
                characters_skills[character].append(skill)
    except Exception as e:
        print(f"读取CSV文件失败: {e}")
        return []

    # 读取技能JSON文件
    skills_data = []
    try:
        with open(skills_json_path, 'r', encoding='utf-8') as json_file:
            skills_data = json.load(json_file)
    except Exception as e:
        print(f"读取技能JSON文件失败: {e}")
        return []

    # 读取属性JSON文件
    stats_data = []
    try:
        with open(stats_json_path, 'r', encoding='utf-8') as json_file:
            stats_data = json.load(json_file)
    except Exception as e:
        print(f"读取属性JSON文件失败: {e}")
        return []

    # 创建技能名称到技能数据的映射
    skill_dict = {}
    for skill in skills_data:
        if "技能名称" in skill:
            skill_dict[skill["技能名称"]] = skill
        else:
            print(f"警告: 跳过无效技能数据 (缺少'技能名称'字段): {skill}")

    # 创建角色名称到属性数据的映射
    stats_dict = {}
    for stat in stats_data:
        if "角色名称" in stat:
            stats_dict[stat["角色名称"]] = stat
        else:
            print(f"警告: 跳过无效属性数据 (缺少'角色名称'字段): {stat}")

    # 构建最终结果数组
    result = []
    for character, skills in characters_skills.items():
        # 获取角色属性
        character_stats = stats_dict.get(character, {})
        
        # 构建技能数组
        character_skills_array = []
        for skill_name in skills:
            if skill_name in skill_dict:
                skill_info = skill_dict[skill_name]
                character_skills_array.append({
                    "技能名": skill_info.get("技能名称", "未知"),
                    "生效回合": skill_info.get("生效回合", "未知"),
                    "条件": skill_info.get("条件", "无"),
                    "效果": skill_info.get("效果", "无")
                })
            else:
                print(f"警告: 角色 '{character}' 的技能 '{skill_name}' 未在JSON文件中找到")
        
        # 添加角色到结果数组
        result.append({
            "角色名": character,
            "身手": character_stats.get("身手", 0),
            "体魄": character_stats.get("体魄", 0),
            "智力": character_stats.get("智力", 0),
            "技术": character_stats.get("技术", 0),
            "悟性": character_stats.get("悟性", 0),
            "魅力": character_stats.get("魅力", 0),
            "技能": character_skills_array
        })

    # 返回结果数组
    return result