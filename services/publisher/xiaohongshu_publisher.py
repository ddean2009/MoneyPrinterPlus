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

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import streamlit as st

import time

from config.config import xiaohongshu_site
from tools.file_utils import read_head, read_file_with_extra_enter


def xiaohongshu_publisher(driver, video_file, text_file):

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(xiaohongshu_site)
    time.sleep(2)  # 等待2秒

    # 设置等待
    wait = WebDriverWait(driver, 10)

    # 上传视频按钮
    file_input = driver.find_element(By.CLASS_NAME, 'upload-input')
    file_input.send_keys(video_file)
    time.sleep(10)  # 等待
    # 等待视频上传完毕
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'c-input_inner')))

    # 设置标题
    title = driver.find_element(By.CLASS_NAME, 'el-input__inner')
    title_text = read_head(text_file)
    use_common = st.session_state.get('video_publish_use_common_config')
    if use_common:
        common_title = st.session_state.get('video_publish_title_prefix')
    else:
        common_title = st.session_state.get('video_publish_xiaohongshu_title_prefix')
    # 标题有20字长度限制
    if len(common_title + title_text) <= 20:
        title.send_keys(common_title + title_text)
    else:
        title.send_keys(title_text)
    time.sleep(2)

    # 设置内容
    content = driver.find_element(By.ID, 'post-textarea')
    content_text = read_file_with_extra_enter(text_file)
    content.send_keys(content_text)
    time.sleep(2)

    # 设置tags
    if use_common:
        tags = st.session_state.get('video_publish_tags')
    else:
        tags = st.session_state.get('video_publish_xiaohongshu_tags')
    tags = tags.split()
    for tag in tags:
        content.send_keys(tag)
        time.sleep(2)
        content.send_keys(Keys.ENTER)
        time.sleep(1)
        content.send_keys(' ')
        time.sleep(2)


    # 发布
    publish_button = driver.find_element(By.XPATH, '//button[contains(@class, "publishBtn")]')
    auto_publish = st.session_state.get('video_publish_auto_publish')
    if auto_publish:
        print("auto publish")
        publish_button.click()







