import requests
import json
import re
import os
import random

def update_dynv6_A(zone):
    #基础变量，api_token使用全局变量
    base_url = "https://dynv6.com/api/v2/zones"
    domain = zone
    headers = {
       "Authorization": f"Bearer {api_token}",
       "Content-Type": "application/json"
    }
    #获取zoneID
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        all_records = response.json()
        for record in all_records:
            if domain == record['name']:
                zoneID = record['id']
                break
        if not zoneID: raise
    except Exception as e:
        print(f'❌ 获取区域信息失败：{str(e)}')
        return
    #形成url
    url = f"{base_url}/{zoneID}/records"
    sub_name = 11
    while sub_name < 38:
        try:
            current_ip = unique_ips.pop()
            if not current_ip: return
            record_data = {
                "name": str(sub_name),
                "type": "A",
                "data": current_ip,  # 用变量暂存IP，方便后续引用
                "ttl": 3600
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            all_records = response.json()
            record_found = False
            for record in all_records:
                if record["name"] == str(sub_name) and record["type"] == "A":
                    renew_response = requests.patch(f"{url}/{record['id']}", headers=headers, data=json.dumps(record_data))
                    renew_response.raise_for_status()
                    record_found = True  # 标记已找到并更新
                    break  # 找到匹配记录，退出循环，无需继续遍历
            if not record_found:
                create_response = requests.post(url, headers=headers, data=json.dumps(record_data))
                create_response.raise_for_status()
            print(f"✅ 成功：{sub_name}.{domain} → {current_ip}")
            bulid_vless_urls(str(sub_name), domain, '002.ljk', 'LJK_E37_TOKEN')
        except Exception as e:
            print(f"❌ {sub_name}.{domain} 操作失败：{str(e)}")
        finally:
            sub_name += 1
            
def bulid_vless_urls(a, b, c, d):
    global vless_urls
    ports = ['443','2053','2083','2087','2096','8443']
    uuid = os.getenv(d)
    if not uuid: return
    port = random.choice(ports)
    host = f'{c}-clouflare.dns.army'
    if not uuid: return
    vless_url = f"vless://{uuid}@{a}.{b}:{port}?path=%2F%3Fed%3D2560&security=tls&encryption=none&host={host}&type=ws&sni={host}#{c[0:3]}-{b[0]}-{a}"
    vless_urls += f'{vless_url}\n'
            
if __name__ == "__main__":
    vless_urls = ''

    urls = [
        'https://ip.164746.xyz',
        'https://ipdb.api.030101.xyz/?type=bestcf&country=true',
        'https://ip.164746.xyz/ipTop10.html',
        'https://www.wetest.vip/page/cloudflare/total_v4.html',
        'https://api.uouin.com/cloudflare.html',
        'https://addressesapi.090227.xyz/CloudFlareYes',
        'https://vps789.com/openApi/cfIpApi'
    ]
    unique_ips = set()
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    api_token = os.getenv('DYNV6_TOKEN')

    for url in urls:
        try:
            response = requests.get(url, timeout=10).text
            ip_matches = re.findall(ip_pattern, response, re.IGNORECASE)
            unique_ips.update(ip_matches)
        except Exception as e:
            continue

    if unique_ips:
        update_dynv6_A('cf-zxs.v6.rocks')

    if vless_urls:
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(vless_urls)
            print(f'✅ 写入index成功！')
