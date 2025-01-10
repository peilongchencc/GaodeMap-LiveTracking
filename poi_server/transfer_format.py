from collections import defaultdict

def transform_poi_data(data):
    """
    将 POI 数据格式化为 {type: [name, ...]} 的字典。

    Args:
        data (dict): 包含 "pois" 数据的字典。

    Returns:
        dict: 格式化后的结果字典。
    """
    result = defaultdict(list)  # 创建一个默认值为列表的 defaultdict 对象

    for poi in data.get("pois", []):
        # 获取 type 的最后一个类别
        poi_type = poi["type"].split(";")[-1]
        # 获取 name 字段
        name = poi["name"]
        # 将 name 添加到对应类型的列表中
        result[poi_type].append(name)

    return dict(result)
if __name__ == '__main__':
    # 示例数据
    data = {
        "pois": [
            {
                "type": "餐饮服务;中餐厅;中餐厅",
                "name": "望京一号(博雅店)"
            },
            {
                "type": "餐饮服务;中餐厅;中餐厅",
                "name": "黄记煌三汁焖锅(望京万象汇店)"
            },
            {
                "type": "购物服务;商场;普通商场",
                "name": "北京望京万象汇"
            }
        ]
    }

    # 调用函数并输出结果
    result = transform_poi_data(data)
    print(result)