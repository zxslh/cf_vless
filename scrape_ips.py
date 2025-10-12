from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_refreshed_content():
    # 1. 配置Chrome无界面模式（适配GitHub Actions Linux环境）
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 最新Headless模式（更稳定）
    chrome_options.add_argument("--no-sandbox")     # 禁用沙箱（Linux必需）
    chrome_options.add_argument("--disable-dev-shm-usage")  # 解决内存限制
    chrome_options.add_argument("--disable-gpu")    # 禁用GPU加速（无界面无需）
    # 配置浏览器用户代理（模拟正常访问，防反爬）
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    )

    # 2. 初始化WebDriver（用webdriver-manager自动匹配ChromeDriver版本）
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 3. 访问目标网页
        target_url = "https://api.uouin.com/cloudflare.html"
        driver.get(target_url)
        print(f"已访问网页：{target_url}")

        # 4. 模拟刷新（或等待自动刷新，这里手动触发更可控）
        time.sleep(2)  # 等待页面初始加载
        driver.refresh()
        print("已触发页面刷新")

        # 5. 等待刷新后JS渲染完成（关键：等待表格数据加载，通过“电信线路”标题定位）
        wait = WebDriverWait(driver, 10)  # 最长等待10秒
        # 等待“电信线路”表格标题出现（说明数据已渲染）
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), '电信线路')]"))
        )
        print("页面刷新并渲染完成")

        # 6. 提取刷新后的内容（这里以提取所有IP表格文本为例，可按需解析）
        refreshed_html = driver.page_source
        # 或直接提取表格内容（更简洁）
        ip_tables = driver.find_elements(By.CLASS_NAME, "table")  # 页面中所有表格
        result = "Cloudflare优选IP（刷新后数据）\n"
        result += "="*50 + "\n"
        for i, table in enumerate(ip_tables, 1):
            line_title = driver.find_elements(By.TAG_NAME, "h3")[i-1].text  # 线路标题（电信/联通等）
            result += f"\n【{line_title}】\n"
            result += table.text + "\n"

        # 7. 保存结果到文件（供GitHub Actions上传）
        with open("ips_result.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("结果已保存到 ips_result.txt")
        print("前100字符预览：", result[:100])

    except Exception as e:
        print(f"爬取失败：{str(e)}")
    finally:
        # 8. 关闭浏览器（必需，避免资源泄漏）
        driver.quit()
        print("浏览器已关闭")

if __name__ == "__main__":
    scrape_refreshed_content()
