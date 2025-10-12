from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def get_installed_chrome_version():
    """从YAML步骤中生成的文件读取安装的Chrome版本（前四位）"""
    with open("chrome_version.txt", "r") as f:
        version_line = f.read().strip()
        # 提取版本号（如"Google Chrome 129.0.6668.89" → "129.0.6668.89"）
        version = version_line.split(" ")[2]
        # 返回前四位主版本（驱动只需匹配前四位）
        return ".".join(version.split(".")[:4])

def scrape_refreshed_content():
    # 1. 获取安装的Chrome版本
    chrome_version = get_installed_chrome_version()
    print(f"已安装Chrome版本：{chrome_version}")

    # 2. 配置Chrome无界面选项
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version.split('.')[0]}.0.0.0 Safari/537.36"
    )

    # 3. 自动下载匹配版本的ChromeDriver
    service = Service(
        ChromeDriverManager(
            chrome_type=ChromeType.GOOGLE,
            version=chrome_version  # 用安装的Chrome版本匹配驱动
        ).install()
    )
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 4. 访问并刷新页面
        target_url = "https://api.uouin.com/cloudflare.html"
        driver.get(target_url)
        print(f"已访问网页：{target_url}")

        time.sleep(2)
        driver.refresh()
        print("已触发页面刷新")

        # 5. 等待JS渲染完成
        wait = WebDriverWait(driver, 15)  # 延长等待时间，确保数据加载
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), '电信线路')]"))
        )
        print("页面刷新并渲染完成")

        # 6. 提取并保存IP数据
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
        # 打印详细错误信息，方便调试
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()
        print("浏览器已关闭")

if __name__ == "__main__":
    scrape_refreshed_content()
