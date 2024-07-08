import sys

import pyperclip
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import streamlit as st

import time

from config.config import douyin_site
from tools.file_utils import read_head, read_file_with_extra_enter


def douyin_publisher(driver, video_file, text_file):

    # driver.switch_to.window(driver.window_handles[0])

    # 打开新标签页并切common_config换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(douyin_site)
    time.sleep(2)  # 等待2秒

    # 设置等待
    wait = WebDriverWait(driver, 10)

    # 上传视频按钮
    file_input = driver.find_element(By.NAME,'upload-btn')
    file_input.send_keys(video_file)
    time.sleep(10)  # 等待
    # 等待视频上传完毕
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'semi-input semi-input-default')))

    # 设置标题
    title = driver.find_element(By.XPATH, '//input[@class="semi-input semi-input-default"]')
    title_text = read_head(text_file)
    use_common = st.session_state.get('video_publish_use_common_config')
    if use_common:
        common_title = st.session_state.get('video_publish_title_prefix')
    else:
        common_title = st.session_state.get('video_publish_douyin_title_prefix')

    # 标题有30字长度限制
    if len(common_title + title_text) <= 30:
        title.send_keys(common_title + title_text)
    else:
        title.send_keys(title_text)
    time.sleep(2)

    # 设置内容
    content = driver.find_element(By.XPATH, '//div[@data-placeholder="添加作品简介"]')
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
        tags = st.session_state.get('video_publish_douyin_tags')
    tags = tags.split()
    for tag in tags:
        is_firefox = st.session_state.get("video_publish_driver_type") == 'firefox'
        # firefox没有原创按钮？
        if not is_firefox:
            print("tag:", tag)
            content.send_keys(' ')
            content.send_keys(tag)
            time.sleep(2)
            content.send_keys(Keys.ENTER)
            time.sleep(1)
            content.send_keys(' ')
            time.sleep(2)
        else:
            print("firefox tag:", tag)
            content.send_keys(' ')
            pyperclip.copy(tag)
            action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
            time.sleep(2)
            content.send_keys(' ')
            time.sleep(1)

    # 设置合集
    if use_common:
        collection = st.session_state.get('video_publish_collection_name')
    else:
        collection = st.session_state.get('video_publish_douyin_collection_name')
    if collection:
        collection_tag = driver.find_element(By.XPATH, '//div[contains(text(),"选择合集")]')
        collection_tag.click()
        time.sleep(1)
        collection_to_select = driver.find_element(By.XPATH, f'//div[@class="semi-select-option collection-option"]//span[text()="{collection}"]')
        collection_to_select.click()
        time.sleep(1)

    # 发布
    publish_button = driver.find_element(By.XPATH, '//button[text()="发布"]')
    auto_publish = st.session_state.get('video_publish_auto_publish')
    if auto_publish:
        print("auto publish")
        publish_button.click()







