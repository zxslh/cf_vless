import requests
import json
import re
import os

def update_dynv6_a_via_api(ip, sub_name):
    #base_url = f"https://dynv6.com/api/v2/zones/5074729/records" #cf-zxs.v6.rocks
    #api_token = 'xCsd_Hpo89auyq_kVF19QHGqLeQQ6b'
    #domain = 'cf-zxs.v6.rocks'
    
    base_url = f"https://dynv6.com/api/v2/zones/5071717/records" #cf-zxs.dns.army
    api_token = 'vTTXvP2dGw8dtHjwFRXXjVfWL1rcLU'
    domain = 'cf-zxs.dns.army'
    
    subdomain = str(sub_name)  # 确保子域名为字符串类型
    new_ip = ip
    ttl = 3600

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        all_records = response.json()
        
        record_data = {
            "name": subdomain,
            "type": "A",
            "data": new_ip,
            "ttl": ttl
        }
        
        for record in all_records:
            if record["name"] == subdomain and record["type"] == "A":
                renew_response = requests.patch(f"{base_url}/{record['id']}", headers=headers, data=json.dumps(record_data))
                renew_response.raise_for_status()  # 捕获创建请求的错误     
                print(f"✅ 更新成功：{subdomain}.{domain} → {new_ip}")
                bulid_vless_urls(subdomain, domain)
                return
                
        create_response = requests.post(base_url, headers=headers, data=json.dumps(record_data))
        create_response.raise_for_status()  # 捕获创建请求的错误
        print(f"✅ 创建成功：{subdomain}.{domain} → {new_ip}")
        bulid_vless_urls(subdomain, domain)
        
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ {subdomain}.{domain} 操作失败：{str(e)}"
        if hasattr(e, 'response') and e.response:
            error_msg += f"，响应：{e.response.text}"
        print(error_msg)

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
            update_dynv6_a_via_api(ip, i)
            break
            i += 1
            if i > 40:
                break

def bulid_vless_urls(a, b):
    global vless_urls
    vless_url = f"vless://77146000-d7ce-493d-98ad-b913a79c12cd@f'{a}.{b}':443?path=%2F%3Fed%3D2560&security=tls&encryption=none&host=771.qq-zxs.dns.army&type=ws&sni=771.qq-zxs.dns.army#{a}"
    vless_urls.append(vless_url)

if __name__ == "__main__":
    vless_urls = []
    update_A_cfip()
    try:
        with open('index.html', 'w', encoding='utf-8') as file:
            for vless_url in vless_urls:
                file.write(vless_url)
            print(f'✅ 写入成功！')
    except Exception as e:
        print(f'❌ 写入失败：{str(e)}')

