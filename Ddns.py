import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, JSONDecodeError

def get_cloudflare_ips(line_type="ct"):
    """
    获取最新CloudFlare优选IP（适配新接口）
    :param line_type: 线路类型，可选值：ct(电信)、cu(联通)、cm(移动)、all(多线)
    :return: 成功返回IP列表，失败返回None
    """
    # 新接口URL（核心修改：将optimize改为list，参数type改为line）
    url = f"https://api.uouin.com/api/v1/cloudflare/list?line={line_type}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Referer": "https://api.uouin.com/cloudflare.html",  # 模拟页面来源
        "Accept": "application/json, text/javascript, */*; q=0.01"
    }

    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=3))
    session.mount("http://", HTTPAdapter(max_retries=3))

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 捕获404/500等状态码错误

        data = response.json()
        if data.get("code") == 200:
            ip_list = data.get("data", [])  # 新接口data直接是IP列表（无需再按line_type提取）
            print(f"成功获取{line_type}线路IP，共{len(ip_list)}个")
            # 打印前5个IP详情
            for i, ip_info in enumerate(ip_list[:5], 1):
                print(f"{i}. IP: {ip_info['ip']} | 延迟: {ip_info['delay']}ms | 速度: {ip_info['speed']}mb/s | 时间: {ip_info['time']}")
            return ip_list
        else:
            print(f"接口业务错误：{data.get('msg', '未知错误')}")
            return None

    except RequestException as e:
        print(f"请求失败：{str(e)}")
        if 'response' in locals():
            print(f"错误响应预览：{response.text[:200]}")
    except JSONDecodeError:
        print("JSON解析失败，非标准JSON响应")
        if 'response' in locals():
            print(f"实际返回内容：{response.text[:200]}")
    finally:
        session.close()

# 调用示例：获取联通线路IP
cu_ips = get_cloudflare_ips(line_type="cu")
