from playwright.sync_api import sync_playwright
from time import sleep

with sync_playwright() as p:
    # 启动浏览器（chromium/firefox/webkit）
    browser = p.chromium.launch(headless=False)  # headless=True 为无界面模式
    page = browser.new_page()
    # 访问网页
    page.goto("https://api.uouin.com/cloudflare.html")

    # 模拟刷新或等待自动刷新
    page.reload()
    sleep(2)

    # 提取渲染后的HTML
    refreshed_html = page.content()
    print(refreshed_html)

    browser.close()
