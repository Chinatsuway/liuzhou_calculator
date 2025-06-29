import json
from Functions.StructureCharacter import StructureCharacter
from Functions.CalculateCharacter import apply_character_skills

def main():

    result = StructureCharacter()
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 初始变量集
    variables = {
        "骰点": 1,
        "回合": 2,
    }

    print(apply_character_skills(result,"燕丹",variables))

if __name__ == "__main__":
    main()