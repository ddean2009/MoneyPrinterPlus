import time

import selenium
from selenium import webdriver

from tools.utils import get_must_session_option


def init_driver():
    driver_type = get_must_session_option('video_publish_driver_type', "请设置驱动类型")
    driver_location = get_must_session_option('video_publish_driver_location', "请设置驱动位置")
    debugger_address = get_must_session_option('video_publish_debugger_address', "请设置debugger地址")
    if driver_type == 'chrome':
        # 启动浏览器驱动服务
        service = selenium.webdriver.chrome.service.Service(driver_location)
        # Chrome 的调试地址
        debugger_address = debugger_address
        # 创建Chrome选项，重用现有的浏览器实例
        options = selenium.webdriver.chrome.options.Options()
        options.page_load_strategy = 'normal'  # 设置页面加载策略为'normal' 默认值, 等待所有资源下载,
        options.add_experimental_option('debuggerAddress', debugger_address)
        # 使用服务和选项初始化WebDriver
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    elif driver_type == 'firefox':
        # 启动浏览器驱动服务
        service = selenium.webdriver.firefox.service.Service(driver_location,
                                                             service_args=['--marionette-port', '2828',
                                                                           '--connect-existing'])
        # 创建firefox选项，重用现有的浏览器实例
        options = selenium.webdriver.firefox.options.Options()
        options.page_load_strategy = 'normal'  # 设置页面加载策略为'normal' 默认值, 等待所有资源下载,
        driver = webdriver.Firefox(service=service, options=options)
        return driver




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
