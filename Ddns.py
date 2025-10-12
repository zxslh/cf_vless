import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, JSONDecodeError

def get_cloudflare_ips(line_type="all"):
    """
    获取CloudFlare优选IP
    :param line_type: 线路类型，可选值：ct(电信)、cu(联通)、cm(移动)、all(全部)
    :return: 成功返回IP列表，失败返回None
    """
    # 1. 核心配置（模拟浏览器请求+重试机制）
    url = f"https://api.uouin.com/api/v1/cloudflare/optimize?type={line_type}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Referer": "https://api.uouin.com/cloudflare.html",  # 模拟从页面跳转过来的请求
        "Accept": "application/json, text/javascript, */*; q=0.01"  # 声明接收JSON格式
    }
    # 创建会话，设置3次重试+10秒超时
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=3))
    session.mount("http://", HTTPAdapter(max_retries=3))

    try:
        # 2. 发送请求
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 若状态码非200（如403/500），直接抛出异常

        # 3. 解析JSON数据
        data = response.json()
        if data.get("code") == 200:  # 接口业务逻辑成功
            ip_list = data.get("data", {}).get(line_type, [])
            print(f"成功获取{line_type}线路IP，共{len(ip_list)}个")
            # 格式化输出前5个IP示例
            for i, ip_info in enumerate(ip_list[:5], 1):
                print(f"{i}. IP: {ip_info['ip']} | 延迟: {ip_info['delay']}ms | 速度: {ip_info['speed']}mb/s | 更新时间: {ip_info['time']}")
            return ip_list
        else:
            print(f"接口返回错误：{data.get('msg', '未知错误')}")
            return None

    # 4. 捕获所有可能的异常
    except RequestException as e:
        print(f"请求失败：{str(e)}")
        # 打印错误响应内容（辅助排查问题）
        if 'response' in locals():
            print(f"错误响应内容：{response.text[:200]}")  # 只打印前200字符，避免过长
    except JSONDecodeError:
        print("JSON解析失败，接口返回非JSON格式")
        if 'response' in locals():
            print(f"实际返回内容：{response.text[:200]}")
    except Exception as e:
        print(f"其他未知错误：{str(e)}")
    finally:
        session.close()  # 关闭会话，释放资源

# ------------------- 调用示例 -------------------
# 获取电信线路IP（如需其他线路，改参数为cu/cm/all）
ct_ips = get_cloudflare_ips(line_type="ct")
