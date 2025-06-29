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
    
    # 4. 按顺序应用角色的所有技能
    for skill in character_data.get("技能", []):
        # 应用技能并更新变量集
        variables = apply_skill(skill, variables)
    
    # 5. 返回最终变量集
    return variables