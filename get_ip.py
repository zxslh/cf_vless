import requests

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
    
for url in urls:
    try:
        response = requests.get(url, timeout=10).text
        ip_matches = re.findall(ip_pattern, response, re.IGNORECASE)
        unique_ips.update(ip_matches)
    except Exception as e:
        print(f'❌ 错误：{str(e)}')
        continue
            
if not unique_ips:
    print('❌ 错误：获取CFIP失败')
else:
    with open('ip.txt', 'w', encoding='utf-8') as file:
        file.write(unique_ips)
        
