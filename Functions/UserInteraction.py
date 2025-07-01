import json
from Functions.StructureCharacter import StructureCharacter
from Functions.CalculateCharacter import apply_character_skills

def interactive_simulation():
    """
    与用户交互的模拟函数
    """
    # 获取角色名
    role_name = input("请输入角色名: ")
    
    # 结构化角色数据
    character_data = StructureCharacter()
    
    # 主循环
    while True:
        print("\n请选择操作:")
        print("1. 查询角色数据")
        print("2. 单次模拟")
        print("3. 多轮模拟")
        print("4. 退出")
        
        choice = input("请输入选项(1-4): ")
        
        if choice == "1":
            # 查询角色数据
            print(json.dumps(character_data, ensure_ascii=False, indent=2))
        
        elif choice == "2":
            # 单次模拟
            try:
                round_num = int(input("请输入回合数: "))
                dice_value = int(input("请输入骰点值: "))
                
                # 初始变量集
                variables = {
                    "回合": round_num,
                    "骰点": dice_value,
                    "加值": 0
                }
                
                # 应用角色技能
                updated_vars = apply_character_skills(character_data, role_name, variables)
                print("\n模拟结果:")
                print(json.dumps(updated_vars, ensure_ascii=False, indent=2))
                
            except ValueError:
                print("错误: 请输入有效的数字")
        
        elif choice == "3":
            # 多轮模拟
            round_num = 1
            variables = {
                "回合": round_num,
                "加值": 0
            }
            
            while True:
                try:
                    # 获取当前骰点值
                    dice_value = int(input(f"\n回合 {round_num} - 请输入骰点值 (输入-1退出): "))
                    
                    if dice_value == -1:
                        break
                    
                    # 更新骰点值
                    variables["骰点"] = dice_value
                    
                    # 应用角色技能
                    updated_vars = apply_character_skills(character_data, role_name, variables)
                    print(f"\n回合 {round_num} 结果:")
                    print(json.dumps(updated_vars, ensure_ascii=False, indent=2))
                    
                    # 更新回合数和变量集
                    round_num += 1
                    variables = updated_vars.copy()
                    variables["回合"] = round_num
                    
                except ValueError:
                    print("错误: 请输入有效的数字")
        
        elif choice == "4":
            # 退出
            print("关注六州喵关注六州谢谢喵")
            break
        
        else:
            print("无效的选项，请重新输入")

def main():
    interactive_simulation()

if __name__ == "__main__":
    main()