from Functions.CalculateSkill import apply_skill

def apply_character_skills(result, character_name, initial_variables):
    # 1. 在结果集中查找指定角色
    character_data = None
    for char in result:
        if char["角色名"] == character_name:
            character_data = char
            break
    if character_data is None:
        print(f"警告: 未找到角色 '{character_name}'")
        return initial_variables
    
    # 2. 创建变量集的副本（避免修改原始数据）
    variables = initial_variables.copy()
    
    # 3. 添加角色的基础属性到变量集
    attributes = ["身手", "体魄", "智力", "技术", "悟性", "魅力"]
    for attr in attributes:
        variables[attr] = character_data.get(attr, 0)
    
    # 4. 按优先级和顺序应用角色的所有技能
    # 首先按优先级分组
    priority_groups = {1: [], 2: [], 3: [], 4: [], 5: []}
    for skill in character_data.get("技能", []):
        priority = skill.get("优先级", 3)  # 默认优先级为3
        if priority not in priority_groups:
            priority = 3  # 如果优先级不在1-5范围内，使用默认值
        priority_groups[priority].append(skill)
    
    # 然后按优先级顺序应用，同一优先级内按序号从小到大排序
    for priority in sorted(priority_groups.keys()):
        # 对同一优先级内的技能按序号排序
        sorted_skills = sorted(priority_groups[priority], key=lambda x: x.get("序号", 0))
        for skill in sorted_skills:
            variables = apply_skill(skill, variables)
    
    # 5. 返回最终变量集
    return variables