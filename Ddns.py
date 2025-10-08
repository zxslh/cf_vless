import requests
import re

update_list = [
    {'domain': 'cf-zxs.dynv6.net', 'url': 'https://ip.164746.xyz', 'token': 'yDmZaZ13RqSEpjZzr5yoihdT_g3hp6'},
    {'domain': 'cf-zxs.v6.army', 'url': 'https://ipdb.api.030101.xyz/?type=bestcf&country=true', 'token': 'c4qv9NXXa6WEv5RyR2LpK-tnoZso92'},
    {'domain': 'cf-zxs.dns.army', 'url': 'https://ip.164746.xyz/ipTop10.html', 'token': 'vTTXvP2dGw8dtHjwFRXXjVfWL1rcLU'},
    {'domain': 'cf-zxs.dns.navy', 'url': 'https://www.wetest.vip/page/cloudflare/total_v4.html', 'token': 'w-2rwUkVh_6XfEuUgYddGz89T3qTCg'},
    {'domain': 'cf-zxs.v6.navy', 'url': 'https://api.uouin.com/cloudflare.html', 'token': 'qAprRPsvN9xZJ3_Mr9_A87aRaxHWsY'},
    {'domain': 'ljk-clouflare.dns.army', 'url': 'https://addressesapi.090227.xyz/CloudFlareYes', 'token': 'a-TseGU4AzYLSo57__-xj6Sxn7zxhz'},
    {'domain': 'live-zxs.dns.army', 'url': 'https://vps789.com/openApi/cfIpApi', 'token': 'QizA-xcwLjvtKc3nPJwwg7PykPRxZr'}
]

ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

for list in update_list:
    try:
        response = requests.get(list['url'], timeout=10).text
        ip_matches = re.findall(ip_pattern, response, re.IGNORECASE)
        if ip_matches:
            ipv4 = ip_matches[0]
            update_url = f"http://dynv6.com/api/update?token={list['token']}&hostname={list['domain']}&ipv4={ipv4}"
            response = requests.get(update_url, timeout=10).text.strip()
            print(f"{ipv4}@{response}@{list['domain']}")
        else:
            print(f"{list['url']}未返回IP@{list['domain']}")
    except Exception as e:
        print(f"失败: {e}")
        continue
