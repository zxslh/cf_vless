import requests
import json
import re
import os

def update_dynv6_A(zone):
    #基础变量
    api_token = os.getenv('DYNV6_TOKEN')
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
    while sub_name < 40:
        try:
            current_ip = unique_ips.pop()
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
                    # 找到匹配记录，执行更新
                    renew_response = requests.patch(f"{url}/{record['id']}", headers=headers, data=json.dumps(record_data))
                    renew_response.raise_for_status()
                    print(f"✅ 更新成功：{sub_name}.{domain} → {current_ip}")
                    bulid_vless_urls(str(sub_name), domain, '771.qq', 'QQ_771_TOKEN')
                    sub_name += 1
                    record_found = True  # 标记已找到并更新
                    break  # 找到匹配记录，退出循环，无需继续遍历
            if not record_found:
                create_response = requests.post(url, headers=headers, data=json.dumps(record_data))
                create_response.raise_for_status()
                print(f"✅ 创建成功：{sub_name}.{domain} → {current_ip}")
                bulid_vless_urls(str(sub_name), domain, '771.qq', 'QQ_771_TOKEN')
                sub_name += 1  # 创建成功后，sub_name递增
        except Exception as e:
            print(f"❌ {sub_name}.{domain} 操作失败：{str(e)}")
            return  # 抛出异常，终止程序（若需继续执行，可替换为continue，但需注意IP已被pop）

def update_dynu_A():
    #DYNU免费用户限制4个domain，每个domain限制4个A记录
    api_token = os.getenv('DYNU_TOKEN')
    api_token = 'f4YXU34YYba3WW33gX43bgUfX2gTZdf6'
    base_url = f"https://api.dynu.com/v2/dns"
    headers = {
        "accept": "application/json",
        "API-Key": api_token
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        all_domains = response.json()['domains']
    except Exception as e:
        print(f'❌ 获取区域信息失败：{str(e)}')
        return

    for domain_data in all_domains:
        sub_name = 11
        domain = domain_data['name']
        url = f"{base_url}/{domain_data['id']}/record"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            all_records = response.json()['dnsRecords']
        except Exception as e:
            print(f"❌ {domain} 操作失败：{str(e)}")
            return
        while sub_name < 15:
            current_ip = unique_ips.pop()
            record_data = {
                "nodeName": str(sub_name),
                "recordType": "A",
                "ipv4Address": current_ip,
                "ttl": 3600,
                "state": True,
                "group": ""
            }
            try: 
                for record in all_records:
                    if record["nodeName"] == str(sub_name) and record["recordType"] == "A":
                        act_url = f"{url}/{record['id']}"                
                        break                       
                update_response = requests.post(act_url, headers=headers, data=json.dumps(record_data))
                update_response.raise_for_status()  # 捕获创建请求的错误
                bulid_vless_urls(str(sub_name), domain, 'cfv.live', 'LIVE_CFV_TOKEN')
                print(f"✅ 成功：{sub_name}.{domain} → {current_ip}")
            except Exception as e:
                print(f"❌ {sub_name}.{domain} 操作失败：{str(e)}")
            finally:
                sub_name += 1

def bulid_vless_urls(a, b, c, d):
    global vless_urls
    uuid = os.getenv(d)
    port = '443'
    host = f'{c}-zxs.dns.army'
    if not uuid: return
    vless_url = f"vless://{uuid}@{a}.{b}:{port}?path=%2F%3Fed%3D2560&security=tls&encryption=none&host={host}&type=ws&sni={host}#{a}{b[0]}"
    vless_urls.append(vless_url)

if __name__ == "__main__":
    vless_urls = []
    update_list = [
        {'domain': 'cf-zxs.dynv6.net', 'url': 'https://ip.164746.xyz'},
        {'domain': 'cf-zxs.v6.army', 'url': 'https://ipdb.api.030101.xyz/?type=bestcf&country=true'},
        {'domain': 'cf-zxs.dns.army', 'url': 'https://ip.164746.xyz/ipTop10.html'},
        {'domain': 'cf-zxs.dns.navy', 'url': 'https://www.wetest.vip/page/cloudflare/total_v4.html'},
        {'domain': 'cf-zxs.v6.navy', 'url': 'https://api.uouin.com/cloudflare.html'},
        {'domain': 'ljk-clouflare.dns.army', 'url': 'https://addressesapi.090227.xyz/CloudFlareYes'},
        {'domain': 'live-zxs.dns.army', 'url': 'https://vps789.com/openApi/cfIpApi'}
    ]
    unique_ips = set()
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    api_token = os.getenv('DYNV6_TOKEN')

    for list in update_list:
        try:
            response = requests.get(list['url'], timeout=10).text
            ip_matches = re.findall(ip_pattern, response, re.IGNORECASE)
            if ip_matches:
                unique_ips.update(ip_matches[1:])
                ipv4 = ip_matches[0]
                update_url = f"http://dynv6.com/api/update?token={api_token}&hostname={list['domain']}&ipv4={ipv4}"
                response = requests.get(update_url, timeout=10).text.strip()
                print(f"{ipv4}@{response}@{list['domain']}")
                bulid_vless_urls(list['domain'].split(".", 1)[0], list['domain'].split(".", 1)[1], '771.qq', 'QQ_771_TOKEN')
            else:
                print(f"❌ {list['url']}未返回IP")
        except Exception as e:
            print(f"❌ 失败: {e}")
            continue

    if unique_ips:
        update_dynv6_A('cf-zxs.dns.army')
        update_dynu_A()

    if vless_urls:
        with open('index.html', 'w', encoding='utf-8') as file:
            for vless_url in vless_urls:
                file.write(f'{vless_url}\n')
            print(f'✅ 写入成功！')


