import requests
import json
import os
import random

def build_file():
    uuid = os.getenv('LJK_E37_TOKEN')
    if not uuid: return
 #   port = random.choice(ports)
    port = 443
    host = '002.ljk-clouflare.dns.army'
        
    try:
        response = requests.get('https://vps789.com/openApi/cfIpTop20', timeout=10)
        response.raise_for_status()
        all_records = response.json()['data']['good']
    except Exception as e:
        print(f"❌ 失败：{str(e)}")
        return
        
    vless_urls = ''
    i = 1
    for record in all_records:
        ip = record['ip']
        vless_url = f"vless://{uuid}@{ip}:{port}?path=%2F%3Fed%3D2560&security=tls&encryption=none&host={host}&type=ws&sni={host}#TOP{i:02d}"
        vless_urls += f'{vless_url}\n'
        print(f"✅ 成功：{ip} → TOP{i:02d}")
        i += 1
        
    if vless_urls:
        with open('top20', 'w', encoding='utf-8') as file:
            file.write(vless_urls)
            
    try:
        response = requests.get('https://vps789.com/openApi/cfIpApi', timeout=10)
        response.raise_for_status()
        all_records_CT = response.json()['data']['CT']
        all_records_CU = response.json()['data']['CU']
        all_records_CM = response.json()['data']['CM']
    except Exception as e:
        print(f"❌ 失败：{str(e)}")
        return
        
    vless_urls = ''
    i = 1
    for record in all_records_CT:
        ip = record['ip']
        vless_url = f"vless://{uuid}@{ip}:{port}?path=%2F%3Fed%3D2560&security=tls&encryption=none&host={host}&type=ws&sni={host}#CT_{i:02d}"
        vless_urls += f'{vless_url}\n'
        print(f"✅ 成功：{ip} → CT_{i:02d}")
        i += 1
    i = 1
    for record in all_records_CU:
        ip = record['ip']
        vless_url = f"vless://{uuid}@{ip}:{port}?path=%2F%3Fed%3D2560&security=tls&encryption=none&host={host}&type=ws&sni={host}#CU_{i:02d}"
        vless_urls += f'{vless_url}\n'
        print(f"✅ 成功：{ip} → CU_{i:02d}")
        i += 1    
    i = 1
    for record in all_records_CM:
        ip = record['ip']
        vless_url = f"vless://{uuid}@{ip}:{port}?path=%2F%3Fed%3D2560&security=tls&encryption=none&host={host}&type=ws&sni={host}#CM_{i:02d}"
        vless_urls += f'{vless_url}\n'
        print(f"✅ 成功：{ip} → CM_{i:02d}")
        i += 1
        
    if vless_urls:
        with open('tum', 'w', encoding='utf-8') as file:
            file.write(vless_urls)

build_file()


