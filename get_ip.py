import requests
import re
import json

urls = [
        'https://ip.164746.xyz',
        'https://ipdb.api.030101.xyz/?type=bestcf&country=true',
        'https://ip.164746.xyz/ipTop10.html',
        'https://www.wetest.vip/page/cloudflare/total_v4.html',
        'https://addressesapi.090227.xyz/CloudFlareYes',
        'https://vps789.com/openApi/cfIpApi',
        'https://vps789.com/openApi/cfIpTop20',
        'https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/Cf-ipv4.json',
]
    
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
badips = ['172.64.88.85','104.18.39.252','104.18.42.183','104.19.44.225']
ips = {}
uips = set()
for url in urls:
    try:
        response = requests.get(url, timeout=10).text
        ip_matches = re.findall(ip_pattern, response, re.IGNORECASE)
        for badip in badips:
            if badip in ip_matches:
                print(f'{url} {badip}')
        ips = {'url': url, 'ip': ip_matches}
        uips.update(ip_matches)
    except Exception as e:
        print(f'❌ 错误：{str(e)}')
        continue
with open('badips', 'r', encoding='utf-8') as file:
        for ip in file:
            uips.remove(ip)
for badip in badips:
    if badip in uips:
        print('bad')
    else:
        print('good')

if not ips:
    print('❌ 错误：获取CFIP失败')
else:
    with open('ip.txt', 'w', encoding='utf-8') as file:
        json.dump(ips, file, ensure_ascii=False, indent=2)

        
