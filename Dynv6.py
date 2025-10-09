import requests
import json
import re
import os

def update_dynv6_a_via_api(ip, sub_name, domain, zoneID):

    url = f"{base_url}/{zoneID}/records"
    record_data = {
        "name": str(sub_name),
        "type": "A",
        "data": ip,
        "ttl": 3600
    }
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        all_records = response.json()
        
        for record in all_records:
            if record["name"] == str(sub_name) and record["type"] == "A":
                renew_response = requests.patch(f"{url}/{record['id']}", headers=headers, data=json.dumps(record_data))
                renew_response.raise_for_status()  # 捕获创建请求的错误     
                print(f"✅ 更新成功：{sub_name}.{domain} → {ip}")
                return
                
        create_response = requests.post(url, headers=headers, data=json.dumps(record_data))
        create_response.raise_for_status()  # 捕获创建请求的错误
        print(f"✅ 创建成功：{sub_name}.{domain} → {ip}")
    except Exception as e:
        print(f"❌ {sub_name}.{domain} 操作失败：{str(e)}")
        raise

def update_A_cfip():
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
    all_ip = []
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    i = 11  # 子域名起始编号（如10、11、12...）
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10).text
            ip_matches = re.findall(ip_pattern, response, re.IGNORECASE)
            unique_ips.update(ip_matches)
            all_ips.append(f'{url}：{len(ip_matches)}\n{ip_matches}\n')
            
        except Exception as e:
            print(f'❌ 错误：{str(e)}')
            continue
    if not unique_ips:
        print('❌ 错误：获取CFIP失败')
        return
        
    with open('ip.txt', 'w', encoding='utf-8') as file:
        file.write(all_ips)
        return
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
        
    for ip in unique_ips:
        try:
            update_dynv6_a_via_api(ip, str(i), domain, zoneID)
        except Exception as e:
            break
        bulid_vless_urls(str(i), domain)
        i += 1
        if i > 40: break

def bulid_vless_urls(a, b):
    global vless_urls
    uuid = os.getenv('QQ_771_TOKEN')
    port = '443'
    host = '771.qq-zxs.dns.army'
    if not uuid:
        print('❌ 需要UUID')
        return
    vless_url = f"vless://{uuid}@{a}.{b}:{port}?path=%2F%3Fed%3D2560&security=tls&encryption=none&host={host}&type=ws&sni={host}#{a}{b[0]}"
    vless_urls.append(vless_url)

if __name__ == "__main__":
    vless_urls = []
    api_token = os.getenv('DYNV6_TOKEN')
    domain = 'cf-zxs.dns.army'
    base_url = "https://dynv6.com/api/v2/zones"
    if not api_token:
        print('❌ 需要TOKEN')
    else:
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        update_A_cfip()
        with open('index.html', 'w', encoding='utf-8') as file:
            for vless_url in vless_urls:
                file.write(f'{vless_url}\n')
            print(f'✅ 写入成功！')


