import requests
import json
import re
import os
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
response = requests.get('https://api.uouin.com/api/v1/cloudflare/optimize?type=all', timeout=10).text
ip_matches = re.findall(ip_pattern, response, re.IGNORECASE)
print(ip_matches)

