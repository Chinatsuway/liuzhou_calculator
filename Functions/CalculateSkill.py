import re
import random

def evaluate_condition(condition_str, variables):
    """
    评估条件字符串的真假值
    
    参数:
        condition_str (str): 条件表达式字符串
        variables (dict): 包含所有变量的字典
        
    返回:
        bool: 条件表达式的结果
    """
    if condition_str == "无":
        return True
    
    # 分割逻辑运算符
    tokens = re.split(r'\s+(与|或)\s+', condition_str)
    if len(tokens) == 1:
        # 单个条件
        return _evaluate_single_condition(tokens[0], variables)
    
    # 处理多个条件组合
    result = _evaluate_single_condition(tokens[0], variables)
    for i in range(1, len(tokens), 2):
        operator = tokens[i]
        next_condition = tokens[i+1]
        next_result = _evaluate_single_condition(next_condition, variables)
        
        if operator == "与":
            result = result and next_result
        elif operator == "或":
            result = result or next_result
    
    return result

def _evaluate_single_condition(condition, variables):
    """
    评估单个条件表达式
    
    参数:
        condition (str): 单个条件表达式
        variables (dict): 变量字典
        
    返回:
        bool: 条件结果
    """
    # 使用正则表达式匹配比较操作符
    match = re.match(r'(.+?)\s*(==|!=|<=|>=|<|>)\s*(.+)', condition)
    if not match:
        raise ValueError(f"无效的条件表达式: {condition}")
    
    left, operator, right = match.groups()
    
    # 获取操作数
    left_val = _get_operand_value(left, variables)
    right_val = _get_operand_value(right, variables)
    
    # 执行比较操作
    if operator == "==":
        return left_val == right_val
    elif operator == "!=":
        return left_val != right_val
    elif operator == "<":
        return left_val < right_val
    elif operator == "<=":
        return left_val <= right_val
    elif operator == ">":
        return left_val > right_val
    elif operator == ">=":
        return left_val >= right_val
    else:
        raise ValueError(f"未知的操作符: {operator}")

def _get_operand_value(operand, variables):
    """
    获取操作数的值
    
    参数:
        operand (str): 操作数字符串
        variables (dict): 变量字典
        
    返回:
        int/float: 操作数的值
    """
    # 尝试解析为数值
    try:
        return int(operand)
    except ValueError:
        try:
            return float(operand)
        except ValueError:
            pass
    
    # 检查是否是变量
    if operand in variables:
        return variables[operand]
    
    # 尝试解析为骰点表达式 (NdM格式)
    dice_match = re.match(r'(\d+)d(\d+)', operand)
    if dice_match:
        num_dice = int(dice_match.group(1))
        dice_sides = int(dice_match.group(2))
        return sum(random.randint(1, dice_sides) for _ in range(num_dice))
    
    raise ValueError(f"无法识别的操作数: {operand}")

def apply_effect(effect_str, variables):
    """
    应用效果表达式到变量集，支持多个效果表达式用"与"连接
    
    参数:
        effect_str (str): 效果表达式字符串（可能包含多个用"与"连接的表达式）
        variables (dict): 变量字典
        
    返回:
        dict: 更新后的变量字典
    """
    if effect_str == "无":
        return variables
    
    # 分割多个效果表达式（以"与"为分隔符）
    effect_list = re.split(r'\s*与\s*', effect_str)
    
    # 依次处理每个效果表达式
    for effect in effect_list:
        if not effect.strip():
            continue  # 跳过空表达式
            
        # 分割效果表达式
        parts = effect.split('=', 1)
        if len(parts) != 2:
            raise ValueError(f"无效的效果表达式: {effect}")
        
        target_var = parts[0].strip()
        expression = parts[1].strip()
        
        # 计算表达式值
        result = _evaluate_expression(expression, variables)
        
        # 更新变量（要求变量必须已存在）
        if target_var not in variables:
            raise ValueError(f"未定义的变量 '{target_var}' 在表达式中使用: {effect}")
        variables[target_var] = result
    
    return variables

def _evaluate_expression(expr, variables):
    """
    计算表达式的值，严格检查变量是否已定义
    
    参数:
        expr (str): 表达式字符串
        variables (dict): 变量字典
        
    返回:
        int/float: 表达式计算结果
        
    异常:
        ValueError: 如果表达式中使用了未定义的变量
    """
    # 创建安全的评估环境
    safe_env = {
        '__builtins__': None,
        'abs': abs,
        'min': min,
        'max': max,
        'round': round,
        'sum': sum,
        'random': random
    }
    
    # 添加当前变量到安全环境
    safe_env.update(variables)
    
    # 检查表达式中使用的所有变量是否已定义
    var_pattern = r'[a-zA-Z_][a-zA-Z0-9_]*'
    for var_name in set(re.findall(var_pattern, expr)):
        # 排除骰点表达式（如2d6）和数字
        if var_name in ['d', 'D'] or var_name.isdigit():
            continue
            
        # 检查变量是否已定义（包括在安全环境中的内置函数）
        if var_name not in variables and var_name not in safe_env:
            raise ValueError(f"未定义的变量 '{var_name}' 在表达式中使用: {expr}")
    
    # 转换骰点表达式为可执行格式
    expr = re.sub(r'(\d+)d(\d+)', r'sum(random.randint(1, \2) for _ in range(\1))', expr)
    
    # 执行表达式计算
    try:
        return eval(expr, {'__builtins__': None}, safe_env)
    except Exception as e:
        raise ValueError(f"表达式计算错误: {expr} - {str(e)}")

def apply_skill(skill, variables):
    """
    参数:
        skill (dict): 技能字典，包含"初始化"、"条件"和"效果"键
        variables (dict): 变量字典
        
    返回:
        dict: 更新后的变量字典
    """
    # 处理初始化表达式
    init_expr = skill.get("初始化", "无")
    if init_expr != "无":
        # 分割初始化表达式
        parts = init_expr.split('=', 1)
        if len(parts) != 2:
            raise ValueError(f"无效的初始化表达式: {init_expr}")
        
        target_var = parts[0].strip()
        expression = parts[1].strip()
        
        # 只有当变量不存在时才进行初始化
        if target_var not in variables:
            # 计算表达式值
            result = _evaluate_expression(expression, variables)
            # 创建新变量
            variables[target_var] = result
    
    # 检查条件是否满足
    condition = skill.get("条件", "无")
    effect = skill.get("效果", "无")

    print({skill.get("优先级",0)},{skill.get("序号",0)})
    
    if evaluate_condition(condition, variables):
        # 应用效果
        return apply_effect(effect, variables)
    
    # 条件不满足时返回原始变量
    return variables