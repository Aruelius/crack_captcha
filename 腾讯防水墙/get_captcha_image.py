import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


Driver = webdriver.Chrome
Ele = webdriver.remote.webelement.WebElement

class GetTcaptchaImage(object):
    def __init__(self):
        self.count = 100

    def creat_driver(self) -> Driver:
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1270,720")
        options.add_argument("no-sandbox")
        driver = webdriver.Chrome(options=options)
        return driver

    def webdriverwait_click(self, driver: Driver, element: Ele) -> None:
        WebDriverWait(driver, 10, 5).until(lambda driver: element).click()

    def save_image(self, url: str) -> None:
        os.makedirs('./image/', exist_ok=True)
        r = requests.get(url)
        file_name = f'./image/bgBlock_{int(time.time() * 1000)}.jpg'
        with open(file_name, "wb") as f:
            f.write(r.content)
            f.close()
        print("下载成功", file_name)

    def get_image(self, driver: Driver):
        for _ in range(self.count):
            bg_block = driver.find_element_by_xpath('//img[@id="slideBg"]')  # 大图
            bg_block_src = bg_block.get_attribute('src')
            self.save_image(bg_block_src)
            print("刷新图片")
            reload_btn = driver.find_elements_by_id("reload")[0]
            self.webdriverwait_click(driver, reload_btn)
            time.sleep(0.5)

    def main(self):
        driver = self.creat_driver()
        driver.get("https://007.qq.com/online.html")
        self.webdriverwait_click(driver, driver.find_elements_by_id("code")[0])
        timeout = WebDriverWait(driver, 5)
        timeout.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "tcaptcha_iframe")))
        self.get_image(driver)

tdc = GetTcaptchaImage()
tdc.main()
