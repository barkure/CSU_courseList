import requests
import json
import pandas as pd
from datetime import datetime

# 定义目标 URL
url = "http://csujwc.its.csu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb="

# 定义表单数据
data = {
    "iColumns": 14,
    "sColumns": "",
    "iDisplayLength": 15,
    "mDataProp_0": "kch",
    "mDataProp_1": "kcmc",
    "mDataProp_2": "ktmc",
    "mDataProp_3": "xf",
    "mDataProp_4": "skls",
    "mDataProp_5": "sksj",
    "mDataProp_6": "skdd",
    "mDataProp_7": "xkrs",
    "mDataProp_8": "syrs",
    "mDataProp_9": "xxrs",
    "mDataProp_10": "ctsm",
    "mDataProp_11": "szkcflmc",
    "mDataProp_12": "xqmc",
    "mDataProp_13": "czOper"
}

# 定义 Cookie
cookies = {
}

# 创建一个空的 DataFrame 用于存储所有页的数据
all_data = pd.DataFrame()

# 循环获取多页数据
for page in range(1, 20):  # 获取前20页的数据
    data["sEcho"] = page + 14
    data["iDisplayStart"] = page * 15 - 15
    # 发送 POST 请求
    response = requests.post(url, data=data, cookies=cookies)
    print("Status code:", response.status_code)
    if response.status_code == 404:
        print("Resource not found, stopping...")
        break
    print("Response text:", response.text)
    # 解析返回的 JSON 数据
    page_data = json.loads(response.text)
    # 将数据转换为 DataFrame
    df = pd.DataFrame(page_data['aaData'])
    # 删除不需要的列
    columns_to_drop = ['kkapList', 'kxh', 'bjkx', 'bjbkx', 'xbyq', 'ctsm']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
    # 将这一页的数据添加到 all_data 中
    all_data = pd.concat([all_data, df])

# 获取当前的时间
now = datetime.now()
# 将时间格式化为字符串
time_str = now.strftime("%Y%m%d%H%M%S")

# 将所有数据保存到 Excel 文件中
all_data.to_excel(f"courseList_{time_str}.xlsx", index=False)
