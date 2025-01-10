"""
Description: 
Requirements: pip install json5
Notes: 
将json文件添加// 或 /* ... */ 这类注释写入jsonl文件，不能使用标准 JSON 解析器的库，会提示`JSONDecodeError`。

需要使用例如json5、commentjson，或其他类似库来处理带注释的 JSON。
"""
import json5

file_path = 'regeo_ex_note.jsonl'

with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()
    loaded_json = json5.loads(data)  # 可以解析含注释的JSON
    print(loaded_json, type(loaded_json))   # <class 'dict'>
    print(f"更容易理解的地址：{loaded_json["regeocode"]["formatted_address"]}")
    """
    例如 "北京市朝阳区阜通东大街6号"(具体的门牌号信息) 其实就是 "北京市朝阳区望京街道方恒购物中心方恒国际"(更容易理解的地址)。
    """
