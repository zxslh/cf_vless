from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# 恢复使用webdriver-manager，指定Chrome版本匹配
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def scrape_refreshed_content():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    )

    # 核心修改：指定Chrome版本，让webdriver-manager下载对应驱动
    service = Service(
        ChromeDriverManager(
            chrome_type=ChromeType.GOOGLE,  # 明确使用官方Chrome（非Chromium）
            version="127.0.6533.88"  # 与安装的Chrome版本完全一致
        ).install()
    )
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        target_url = "https://api.uouin.com/cloudflare.html"
        driver.get(target_url)
        print(f"已访问网页：{target_url}")

        time.sleep(2)
        driver.refresh()
        print("已触发页面刷新")

        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), '电信线路')]"))
        )
        print("页面刷新并渲染完成")

        # 提取并保存IP数据
        ip_tables = driver.find_elements(By.CLASS_NAME, "table")
        result = "Cloudflare优选IP（刷新后数据）\n"
        result += "="*50 + "\n"
        for i, table in enumerate(ip_tables, 1):
            line_title = driver.find_elements(By.TAG_NAME, "h3")[i-1].text
            result += f"\n【{line_title}】\n"
            result += table.text + "\n"

        with open("ips_result.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("结果已保存到 ips_result.txt")

    except Exception as e:
        print(f"爬取失败：{str(e)}")
    finally:
        driver.quit()
        print("浏览器已关闭")

if __name__ == "__main__":
    scrape_refreshed_content()
