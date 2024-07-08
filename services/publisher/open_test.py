import time

import selenium
from selenium import webdriver

from services.publisher.publisher_common import init_driver
from tools.utils import get_must_session_option


def start_page(site_url, driver):
    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')
    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(site_url)
    time.sleep(1)


def start_all_pages():
    driver = init_driver()
    start_page('http://www.flydean.com', driver)
    # 在需要的时候关闭浏览器，不要关闭浏览器进程
    driver.quit()


if __name__ == '__main__':
    start_all_pages()
