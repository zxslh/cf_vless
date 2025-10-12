from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# 核心修复：ChromeType 从 core.enums 导入（而非 core.utils）
from webdriver_manager.core.enums import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def get_installed_chrome_version():
    """读取YAML步骤中保存的Chrome版本号"""
    with open("chrome_version.txt", "r") as f:
        version_line = f.read().strip()
        version = version_line.split(" ")[2]  # 提取版本号（如"129.0.6668.89"）
        return ".".join(version.split(".")[:4])  # 返回前四位主版本

def scrape_refreshed_content():
    chrome_version = get_installed_chrome_version()
    print(f"已安装Chrome版本：{chrome_version}")

    # 配置Chrome无界面选项
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version.split('.')[0]}.0.0.0 Safari/537.36"
    )

    # 自动下载匹配版本的ChromeDriver
    service = Service(
        ChromeDriverManager(
            chrome_type=ChromeType.GOOGLE,  # 明确使用官方Chrome驱动
            version=chrome_version  # 匹配安装的Chrome版本
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

        # 等待数据渲染（最长15秒）
        wait = WebDriverWait(driver, 15)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), '电信线路')]"))
        )
        print("页面刷新并渲染完成")

        # 提取IP数据并保存
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
        import traceback
        traceback.print_exc()  # 打印详细错误栈
    finally:
        driver.quit()
        print("浏览器已关闭")

if __name__ == "__main__":
    scrape_refreshed_content()
