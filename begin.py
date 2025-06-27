import json
from Functions.StructureCharacter import StructureCharacter

def main():
    """
    主函数：调用StructureCharacter函数并打印结果
    """
    result = StructureCharacter()
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()