# base 模式的返回结果
base_result = {
    "status": "1",  # 接口调用结果状态，1 表示成功
    "count": "1",  # 返回结果数量，这里是 1 条
    "info": "OK",  # 简要描述接口调用结果，OK 表示成功
    "infocode": "10000",  # 调用结果代码，10000 表示正常请求
    "lives": [  # 实时天气信息数组
        {
            "province": "北京",  # 省份名称
            "city": "朝阳区",  # 城市/区名称
            "adcode": "110105",  # 行政区划代码
            "weather": "晴",  # 天气情况
            "temperature": "5",  # 当前气温（摄氏度）
            "winddirection": "西北",  # 风向
            "windpower": "≤3",  # 风力等级（小于等于 3 级）
            "humidity": "17",  # 当前湿度（百分比）
            "reporttime": "2025-01-16 11:02:37",  # 数据发布时间
            "temperature_float": "5.0",  # 气温的浮点数表示形式
            "humidity_float": "17.0"  # 湿度的浮点数表示形式
        }
    ]
}

# all 模式的返回结果
all_result = {
    "status": "1",  # 接口调用结果状态，1 表示成功
    "count": "1",  # 返回结果数量，这里是 1 条
    "info": "OK",  # 简要描述接口调用结果，OK 表示成功
    "infocode": "10000",  # 调用结果代码，10000 表示正常请求
    "forecasts": [  # 天气预报数组
        {
            "city": "朝阳区",  # 城市/区名称
            "adcode": "110105",  # 行政区划代码
            "province": "北京",  # 省份名称
            "reporttime": "2025-01-16 11:02:37",  # 数据发布时间
            "casts": [  # 未来 4 天的天气预报数组（当天、明天、后天、大后天）
                {
                    "date": "2025-01-16",  # 日期
                    "week": "4",  # 星期几（4 表示周四）
                    "dayweather": "晴",  # 白天天气情况
                    "nightweather": "晴",  # 夜晚天气情况
                    "daytemp": "8",  # 白天最高气温（摄氏度）
                    "nighttemp": "-5",  # 夜晚最低气温（摄氏度）
                    "daywind": "北",  # 白天风向
                    "nightwind": "北",  # 夜晚风向
                    "daypower": "1-3",  # 白天风力等级（1 到 3 级）
                    "nightpower": "1-3",  # 夜晚风力等级（1 到 3 级）
                    "daytemp_float": "8.0",  # 白天气温的浮点数表示形式
                    "nighttemp_float": "-5.0"  # 夜晚气温的浮点数表示形式
                },
                {
                    "date": "2025-01-17",  # 日期
                    "week": "5",  # 星期几（5 表示周五）
                    "dayweather": "晴",  # 白天天气情况
                    "nightweather": "晴",  # 夜晚天气情况
                    "daytemp": "8",  # 白天最高气温（摄氏度）
                    "nighttemp": "-4",  # 夜晚最低气温（摄氏度）
                    "daywind": "南",  # 白天风向
                    "nightwind": "南",  # 夜晚风向
                    "daypower": "1-3",  # 白天风力等级（1 到 3 级）
                    "nightpower": "1-3",  # 夜晚风力等级（1 到 3 级）
                    "daytemp_float": "8.0",  # 白天气温的浮点数表示形式
                    "nighttemp_float": "-4.0"  # 夜晚气温的浮点数表示形式
                },
                {
                    "date": "2025-01-18",  # 日期
                    "week": "6",  # 星期几（6 表示周六）
                    "dayweather": "晴",  # 白天天气情况
                    "nightweather": "晴",  # 夜晚天气情况
                    "daytemp": "8",  # 白天最高气温（摄氏度）
                    "nighttemp": "-4",  # 夜晚最低气温（摄氏度）
                    "daywind": "西南",  # 白天风向
                    "nightwind": "西南",  # 夜晚风向
                    "daypower": "1-3",  # 白天风力等级（1 到 3 级）
                    "nightpower": "1-3",  # 夜晚风力等级（1 到 3 级）
                    "daytemp_float": "8.0",  # 白天气温的浮点数表示形式
                    "nighttemp_float": "-4.0"  # 夜晚气温的浮点数表示形式
                },
                {
                    "date": "2025-01-19",  # 日期
                    "week": "7",  # 星期几（7 表示周日）
                    "dayweather": "晴",  # 白天天气情况
                    "nightweather": "晴",  # 夜晚天气情况
                    "daytemp": "6",  # 白天最高气温（摄氏度）
                    "nighttemp": "-4",  # 夜晚最低气温（摄氏度）
                    "daywind": "北",  # 白天风向
                    "nightwind": "北",  # 夜晚风向
                    "daypower": "1-3",  # 白天风力等级（1 到 3 级）
                    "nightpower": "1-3",  # 夜晚风力等级（1 到 3 级）
                    "daytemp_float": "6.0",  # 白天气温的浮点数表示形式
                    "nighttemp_float": "-4.0"  # 夜晚气温的浮点数表示形式
                }
            ]
        }
    ]
}
