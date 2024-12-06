import os
from datetime import datetime
from PIL import Image
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import base64
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CanvasScraper:
    def __init__(self):
        # Initialize Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def scrape_canvas_image(self, url):
        self.driver.get(url)

        # 等待画布元素加载并确保其尺寸足够
        try:
            canvas = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "canvas"))
            )
            time.sleep(10)  # 额外等待画布内容加载完成
            WebDriverWait(self.driver, 20).until(
                lambda d: d.execute_script("return arguments[0].width", canvas) > 100
            )
        except TimeoutException:
            print("等待画布加载超时，没有找到canvas元素。")
            return None

        # 提取画布图像数据为 base64
        canvas_base64 = self.driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);", canvas
        )

        # 解码 base64 数据并创建图像
        canvas_png = base64.b64decode(canvas_base64)
        image = Image.open(BytesIO(canvas_png))
        return image

    def save_canvas_image(self, url, filename='canvas_image.png', timestamp=None):
        # 直接调用scrape_canvas_image
        image = self.scrape_canvas_image(url)

        if image is None:
            print(f"未能从 {url} 获取画布图像，跳过此链接。")
            return

        # 设置默认时间戳
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y%m%d')

        # 创建 'image/{timestamp}' 文件夹
        output_folder = os.path.join('image', timestamp)
        os.makedirs(output_folder, exist_ok=True)

        # 设置图像的完整路径
        output_path = os.path.join(output_folder, filename)

        # 保存图像
        image.save(output_path)
        print(f"画布图像保存到 {output_path}")


# 使用示例
if __name__ == '__main__':
    scraper = CanvasScraper()

    urls = [
        "https://ai.s.weibo.com/web/other/ai/content?ua=OPPO-PFZM10__weibo__14.3.2__android__android14&from=10E3295010&query=%E9%BA%A6%E7%90%B3%20%E6%9D%8E%E8%A1%8C%E4%BA%AE&from=3004",
        # 你可以在这里添加其他 URL
    ]

    timestamp = datetime.now().strftime('%Y%m%d')
    output_image_name = 'output_canvas_image.png'

    # 遍历 URL 列表，抓取并保存画布图像
    for url in urls:
        scraper.save_canvas_image(url, output_image_name, timestamp)
