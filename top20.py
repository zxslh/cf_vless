import requests
import json
import os

def build_file():
    vless_urls = ''
    uuid = os.getenv('LIVE_CFV_TOKEN')
    port = '443'
    host = 'cfv.live-zxs.dns.army'
    if not uuid: return
    try:
        response = requests.get('https://vps789.com/openApi/cfIpTop20')
        response.raise_for_status()
        all_records = response.json()['data']['good']
    except Exception as e:
        print(f"❌ 失败：{str(e)}")
        return
    i = 1
    for record in all_records:
        ip = record['ip']
        vless_url = f"vless://{uuid}@ip:{port}?path=%2F%3Fed%3D2560&security=tls&encryption=none&host={host}&type=ws&sni={host}#TOP{i:02d}"
        vless_urls += f'{vless_url}\n'
        print(f"✅ 成功：{ip} → TOP{i:02d}")
        i += 1
    if vless_urls:
        with open('top20', 'w', encoding='utf-8') as file:
            file.write(vless_urls)

build_file()


