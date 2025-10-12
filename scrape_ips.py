import page_parser

# 1、指定网页
url = "https://api.uouin.com/cloudflare.html"

# 2、解析网页
items = page_parser.parse(url)

# 3、输出数据
for item in items: print(item)
# {'title': '百度一下，你就知道'}
