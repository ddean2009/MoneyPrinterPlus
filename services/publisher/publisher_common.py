#  Copyright © [2024] 程序那些事
#
#  All rights reserved. This software and associated documentation files (the "Software") are provided for personal and educational use only. Commercial use of the Software is strictly prohibited unless explicit permission is obtained from the author.
#
#  Permission is hereby granted to any person to use, copy, and modify the Software for non-commercial purposes, provided that the following conditions are met:
#
#  1. The original copyright notice and this permission notice must be included in all copies or substantial portions of the Software.
#  2. Modifications, if any, must retain the original copyright information and must not imply that the modified version is an official version of the Software.
#  3. Any distribution of the Software or its modifications must retain the original copyright notice and include this permission notice.
#
#  For commercial use, including but not limited to selling, distributing, or using the Software as part of any commercial product or service, you must obtain explicit authorization from the author.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Author: 程序那些事
#  email: flydean@163.com
#  Website: [www.flydean.com](http://www.flydean.com)
#  GitHub: [https://github.com/ddean2009/MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus)
#
#  All rights reserved.
#
#

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
        driver.implicitly_wait(10)  # 设置隐式等待时间为15秒
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
        driver.implicitly_wait(10)  # 设置隐式等待时间为15秒
        return driver
