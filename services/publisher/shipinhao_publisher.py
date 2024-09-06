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

import re
import sys

import pyperclip
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import streamlit as st

import time

from config.config import shipinhao_site
from tools.file_utils import read_head, read_file_with_extra_enter


def shipinhao_publisher(driver, video_file, text_file):

    # driver.switch_to.window(driver.window_handles[0])

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(shipinhao_site)
    time.sleep(2)  # 等待2秒

    # 设置等待
    wait = WebDriverWait(driver, 10)

    # 上传视频按钮
    file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
    file_input.send_keys(video_file)
    time.sleep(10)  # 等待
    # 等待视频上传完毕

    # 设置标题
    title = driver.find_element(By.XPATH, '//input[@placeholder="概括视频主要内容，字数建议6-16个字符"]')
    title_text = read_head(text_file)
    use_common = st.session_state.get('video_publish_use_common_config')
    if use_common:
        common_title = st.session_state.get('video_publish_title_prefix')
    else:
        common_title = st.session_state.get('video_publish_shipinhao_title_prefix')
    # 替换英文标点符号
    title_text = re.sub(r'[.!?,:;"\'\-\(\)]', '', title_text)
    # 替换中文标点符号
    title_text = re.sub(r'[。！？，：、；“’\-（）]', '', title_text)

    # 标题有20字长度限制
    if len(common_title + title_text) <= 20:
        title.send_keys(common_title + title_text)
    else:
        title.send_keys(title_text)
    time.sleep(2)

    # 设置内容
    content = driver.find_element(By.XPATH, '//div[@class="input-editor"]')
    content.click()
    time.sleep(2)
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    # 将要粘贴的文本内容复制到剪贴板
    content_text = read_file_with_extra_enter(text_file)
    pyperclip.copy(content_text)
    action_chains = webdriver.ActionChains(driver)
    # 模拟实际的粘贴操作
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(2)

    # 设置tags
    if use_common:
        tags = st.session_state.get('video_publish_tags')
    else:
        tags = st.session_state.get('video_publish_shipinhao_tags')
    tags = tags.split()
    for tag in tags:
        content.send_keys(' ')
        content.send_keys(tag)
        content.send_keys(' ')
        time.sleep(1)

    # 设置位置
    location_tag = driver.find_element(By.CLASS_NAME,'location-name')
    actions = ActionChains(driver)
    actions.move_to_element(location_tag).click().perform()
    time.sleep(1)
    location_item = driver.find_element(By.XPATH,'//div[@class="location-item-info"]/div[text()="不显示位置"]')
    actions.move_to_element(location_item).click().perform()
    time.sleep(1)

    # 设置合集
    if use_common:
        collection = st.session_state.get('video_publish_collection_name')
    else:
        collection = st.session_state.get('video_publish_shipinhao_collection_name')
    if collection:
        collection_tag = driver.find_element(By.XPATH, '//div[@class="post-album-display-wrap"]/div[text()="选择合集"]')
        actions = ActionChains(driver)
        actions.move_to_element(collection_tag).click().perform()
        time.sleep(1)
        collection_to_select = driver.find_element(By.XPATH,
                                                   f'//div[@class="post-album-wrap"]//div[text()="{collection}"]')
        actions.move_to_element(collection_to_select).click().perform()
        time.sleep(1)

    is_original = st.session_state.get("video_publish_shipinhao_enable_original")

    if is_original:
        # 原创
        original_tag = driver.find_element(By.XPATH, '//div[@class="declare-original-checkbox"]//input[@type="checkbox"]')
        original_tag.click()
        time.sleep(1)
        # original_tag_click = driver.find_element(By.XPATH, '//div[@class="original-type-form"]//dt[contains(text(),"请选择")]')
        # actions.move_to_element(original_tag_click).click().perform()
        # time.sleep(1)
        # original_tag_item = driver.find_element(By.XPATH,
        #                                          '//div[@class="original-type-form"]//span[text()="知识"]')
        # actions.move_to_element(original_tag_item).click().perform()
        # time.sleep(1)
        agree_button = driver.find_element(By.XPATH, '//div[@class="original-proto-wrapper"]//input[@type="checkbox"]')
        agree_button.click()
        time.sleep(1)
        agree_button_click = driver.find_element(By.XPATH,'//button[@type="button" and text()="声明原创"]')
        agree_button_click.click()
        time.sleep(1)

    # 发布
    publish_button = driver.find_element(By.XPATH, '//button[text()="发表"]')
    auto_publish = st.session_state.get('video_publish_auto_publish')
    if auto_publish:
        print("auto publish")
        publish_button.click()
