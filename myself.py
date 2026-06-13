import requests
import json
import re
import os
import random
import socket
import time

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
    sub_name = 1
    for ip in list_ips:
        if sub_name > 50: break
        try:
            current_ip = ip
            if not current_ip: return
            record_data = {
                "name": f'{sub_name:02d}',
                "type": "A",
                "data": current_ip,  # 用变量暂存IP，方便后续引用
                "ttl": 3600
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            all_records = response.json()
            record_found = False
            for record in all_records:
                if record["name"] == f'{sub_name:02d}' and record["type"] == "A":
                    renew_response = requests.patch(f"{url}/{record['id']}", headers=headers, data=json.dumps(record_data))
                    renew_response.raise_for_status()
                    record_found = True  # 标记已找到并更新
                    break  # 找到匹配记录，退出循环，无需继续遍历
            if not record_found:
                create_response = requests.post(url, headers=headers, data=json.dumps(record_data))
                create_response.raise_for_status()
            print(f"✅ 成功：{sub_name:02d}.{domain} → {current_ip}")
            bulid_vless_urls(f'{sub_name:02d}', domain)
        except Exception as e:
            print(f"❌ {sub_name:02d}.{domain} 操作失败：{str(e)}")
        finally:
            sub_name += 1
            
def bulid_vless_urls(a, b):
    global vless_urls
    ports = ['443','2053','2083','2087','2096','8443']
    uuid = os.getenv('LJK_E37_TOKEN')
    if not uuid: return
    port = random.choice(ports)
    port = 443
    host = '002.ljk-clouflare.dns.army'
    vless_url = f"vless://{uuid}@{a}.{b}:{port}?path=%2F%3Fed%3D2560&security=tls&encryption=none&host={host}&type=ws&sni={host}#{host[0:3]}-{b[0]}-{a}"
    vless_urls += f'{vless_url}\n'
    
def test_ip_connection(ip, port=443, timeout=2):
    """测试IP+端口的TCP连接，返回(连接结果, 状态描述, 耗时ms)"""
    try:
        if '.' in ip:  # IPv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_addr = (ip, int(port))
        elif ':' in ip:  # IPv6（预留逻辑，当前未实际使用）
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            addr_info = socket.getaddrinfo(ip, int(port), socket.AF_INET6, socket.SOCK_STREAM)
            target_addr = addr_info[0][4]
        else:
            return False, f"IP格式错误：{ip} 非法", -1
        sock.settimeout(timeout)
        start_time = time.time()
        sock.connect(target_addr)
        sock.close()
        cost_time = int(round(time.time() - start_time, 3)*1000)
        try:
            geo_api_co = f"https://api.ipinfo.io/lite/{ip}?token=ac0234fdb1a7c7"
            #geo_api_ci = f"https://api.ipgeolocation.io/v2/ipgeo?apiKey=2f98161b8f61480889286e1f9a91d937&ip={ip}&fields=location.city"
            country = requests.get(geo_api_co, timeout=timeout).json()['country']
            #city = requests.get(geo_api_ci, timeout=timeout).json()['location']['city']
        except Exception as e:
            country = '未知'
            pass
        return True, f"连接成功 耗时：{cost_time}", cost_time, f"{country}"
    except socket.timeout:
        return False, f"连接超时（{timeout}秒）", -1, '未知'
    except ConnectionRefusedError:
        return False, "端口拒绝连接（端口关闭）", -1, '未知'
    except Exception as e:
        return False, f"连接失败：{str(e)[:50]}...", -1, '未知'
        
def sort_out_cfips_json(test_us_num=0, test_other_num=0):
    unique_ip_list = []
    unique_ip_dict = {}
    unique_group_dict = {}
    cfips_path = 'abcd.json'
    ips_data = {}
    try:
        with open(cfips_path, 'r', encoding="utf-8-sig") as f:
            ips_data = json.load(f)
        # 按group分组，每组最多保留前5个
        for item in ips_data['ipv4']:
            key = item.get('group', '未分组')
            if len(unique_group_dict.setdefault(key, [])) < 5:
                unique_group_dict[key].append(item)
                unique_ip_list.append(item)
        # 过滤重复IP
        unique_ip_dict = {item['ip']: item for item in unique_ip_list}
    except Exception as e:
        print(str(e))
        pass

    getips_urls = [
        'https://ip.164746.xyz',
        'https://ipdb.api.030101.xyz/?type=bestcf&country=true',
        'https://www.wetest.vip/page/cloudflare/total_v4.html',
        'https://vps789.com/openApi/cfIpApi',
        'https://cf.090227.xyz/CloudFlareYes',
        'https://www.wetest.vip/page/cloudflare/address_v4.html',
        'https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/Cf-ipv4.json',
    ]
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'  # 仅匹配IPv4的正则
    print(f"  📥 开始爬取新IP（共{len(getips_urls)}个源）：")
    all_new_ip_num = 0
    for url in getips_urls:
        new_ip_num = 0
        try:
            response = requests.get(url, timeout=10).text
            ipv4s = re.findall(ip_pattern, response, re.IGNORECASE)
            for ip in ipv4s:
                new_ip_info = {}
                if ip not in unique_ip_dict:
                    new_ip_num += 1
                    all_new_ip_num += 1
                    new_ip_info['ip'] = ip
                    new_ip_info['port'] = 443
                    new_ip_info['group'] = ".".join(ip.split(".")[:3])
                    new_ip_info['name'] = '未知'
                    new_ip_info['cost_time'] = -1
                    unique_ip_dict[ip] = new_ip_info
            print(f"    🆕 {url.split('//')[1][:13]}... 爬{len(ipv4s)}个，获取{new_ip_num}个")
        except Exception as e:
            print(f"    ❌ {url.split('//')[1][:13]}... 失败: {str(e)[:20]}...")
            continue
    print('  📥 爬取完成！')
    print('  🔄 更新IP信息')
    unique_ip_list = list(unique_ip_dict.values())
    good_cost_time = [item for item in unique_ip_list if item['cost_time'] != -1]
    bad_cost_time = [item for item in unique_ip_list if item['cost_time'] == -1]
    if bad_cost_time:
        print(f'    🔄 新增IP（{all_new_ip_num}），连接超时（{len(bad_cost_time)-all_new_ip_num}）个')
        for index, ip_info in enumerate(bad_cost_time, 1):
            is_valid, test_msg, cost_time, location = test_ip_connection(ip_info['ip'], ip_info['port'])
            if is_valid and (cost_time < 300 or location != 'United States'):
                ip_info['cost_time'] = cost_time
                if ip_info['name'] == '未知': ip_info['name'] = location
                good_cost_time.append(ip_info)
                print(f"✅ Index: {str(index).ljust(5)} | {ip_info['ip'].ljust(21)} | {test_msg} | {location.ljust(58)}")
            else:
                print(f"🗑️ Index: {str(index).ljust(5)} | {ip_info['ip'].ljust(21)} | {test_msg.ljust(58)}")
        print('')
    unknown = [item for item in good_cost_time if item['name'] == '未知']
    known = [item for item in good_cost_time if item['name'] != '未知']
    us = [item for item in known if item['name'] == 'United States']
    other = [item for item in known if item['name'] != 'United States']
    test_ipv4s_data = unknown + us[:test_us_num] + other[:test_other_num]
    if test_ipv4s_data:
        print(f'    🔄 更新IP连接耗时：未知 （{len(unknown)}）个，United States（{min(test_us_num,len(us))}）个, Other（{min(test_other_num,len(other))}）个')
        for index, ip_info in enumerate(test_ipv4s_data, 1):
            is_valid, test_msg, cost_time, location = test_ip_connection(ip_info['ip'], ip_info['port'])
            ip_info['cost_time'] = cost_time
            if ip_info['name'] == '未知': ip_info['name'] = location
            if is_valid:
                print(f"✅ Index: {str(index).ljust(5)} | {ip_info['ip'].ljust(21)} | {test_msg} | {location.ljust(58)}")
            else:
                print(f"⚠️ Index: {str(index).ljust(5)} | {ip_info['ip'].ljust(21)} | {test_msg.ljust(58)}")
        print('')
    print(f"  🔄 更新完成！")
    unique_ip_list = us[test_us_num:] + other[test_other_num:] + test_ipv4s_data
    unique_ip_list.sort(key=lambda x: x['cost_time'])

    ips_data['ipv4'] = unique_ip_list
    with open(cfips_path, 'w', encoding="utf-8-sig") as f:
        json.dump(ips_data, f, indent=2, ensure_ascii=False)
    print(f"  🌟 写入IP总数：{len(ips_data['ipv4'])}个；原group数量：{len(unique_group_dict)}")
           
if __name__ == "__main__":
    vless_urls = ''
    list_ips = []
    sort_out_cfips_json()
    try:
        with open('abcd.json', 'r', encoding='utf-8-sig') as file:
            json_data = json.load(file)
            if not json_data['ipv4']: raise Exception('没有json数据')
            for index, item in enumerate(json_data['ipv4']):
                if index > 51: break
                list_ips.append(item['ip'])
    except Exception as e:
        print(f"❌ 读取失败: {str(e)}")
    api_token = os.getenv('DYNV6_TOKEN')

    if list_ips:
        update_dynv6_A(os.getenv('CF_VLESS_ADDR'))

    if vless_urls:
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(vless_urls)
            print(f'✅ 写入index成功！')
