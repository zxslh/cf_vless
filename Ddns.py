import requests
import json
import re
import os
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
response = requests.get('http://cf.090227.xyz/', timeout=10).json()
print(response)
#ip_matches = re.findall(ip_pattern, response, re.IGNORECASE)()
#print(ip_matches)

