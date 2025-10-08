import requests
import json
import re
import os

def update_dynv6_a_via_api(ip, sub_name):
    subdomain = str(sub_name)  # 确保子域名为字符串类型
    new_ip = ip
    ttl = 3600
    record_data = {
        "nodeName": subdomain,
        "recordType": "A",
        "ipv4Address": new_ip,
        "ttl": ttl,
        "state": True,
        "group": ""
    }
    api_token = 'bXV3VU6f2bagfYdVdYTU62U5Ud363366'
    domain = 'as-zxs.ddnsfree.com'
    
    headers = {
        "accept": "application/json",
        "API-Key": api_token
    }

    try:
        base_url = f'https://api.dynu.com/v2/dns/getroot/{domain}'
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        id = response.json()['id']
        base_url = f"https://api.dynu.com/v2/dns/{id}/record"
        
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        all_records = response.json()['dnsRecords']
        
        for record in all_records:
            if record["nodeName"] == subdomain and record["recordType"] == "A":
                base_url = f"{base_url}/{record['id']}"                
                break
                
        create_response = requests.post(base_url, headers=headers, data=json.dumps(record_data))
        create_response.raise_for_status()  # 捕获创建请求的错误
        print(f"✅ 成功：{subdomain}.{domain} → {new_ip}")
        bulid_vless_urls(subdomain, domain)
        
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ {subdomain}.{domain} 操作失败：{str(e)}"
        if hasattr(e, 'response') and e.response:
            error_msg += f"，响应：{e.response.text}"
        print(error_msg)
        raise Exception

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
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    i = 11  # 子域名起始编号（如10、11、12...）
    
    for url in urls:
        response = requests.get(url, timeout=10).text
        ip_matches = re.findall(ip_pattern, response, re.IGNORECASE)
        unique_ips.update(ip_matches)
            
    if unique_ips:
        for ip in unique_ips:
            try:
                update_dynv6_a_via_api(ip, i)
            except Exception as e:
                break
            i += 1                
            if i > 40:
                break

def bulid_vless_urls(a, b):
    global vless_urls
    vless_url = f"vless://e3713ba4-a8fc-44ec-b401-3b736e67718d@{a}.{b}:443?path=%2F%3Fed%3D2560&security=tls&encryption=none&host=cfv.live-zxs.dns.army&type=ws&sni=cfv.live-zxs.dns.army#{a}"
    vless_urls.append(vless_url)

if __name__ == "__main__":
    vless_urls = []
    update_A_cfip()
    try:
        with open('dynu.txt', 'w', encoding='utf-8') as file:
            for vless_url in vless_urls:
                file.write(f'{vless_url}\n')
            print(f'✅ 写入成功！')
    except Exception as e:
        print(f'❌ 写入失败：{str(e)}')
