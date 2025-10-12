import requests
import json

# 核心AJAX接口，type=all表示获取所有线路
url = "https://api.uouin.com/api/v1/cloudflare/optimize?type=all"

# 发送GET请求（该接口无需headers和cookies，直接请求即可）
response = requests.get(url)
# 解析JSON响应
data = response.json()

# 提取并打印电信线路（ct）的IP数据（其他线路替换为cu/cm/all即可）
if data["code"] == 200:  # 接口返回成功
    ct_ips = data["data"]["ct"]  # 电信线路数据列表
    print("电信线路优选IP：")
    for ip_info in ct_ips:
        ip = ip_info["ip"]  # IP地址
        delay = ip_info["delay"]  # 延迟（ms）
        speed = ip_info["speed"]  # 速度（mb/s）
        print(f"IP: {ip}, 延迟: {delay}ms, 速度: {speed}mb/s")
else:
    print("请求失败：", data["msg"])


