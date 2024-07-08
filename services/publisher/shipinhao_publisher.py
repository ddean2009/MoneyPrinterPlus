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

    is_firefox = st.session_state.get("video_publish_driver_type") == 'firefox'
    # firefox没有原创按钮？
    # if not is_firefox:
    # 原创
    original_tag = driver.find_element(By.XPATH, '//div[@class="declare-original-checkbox"]//input[@type="checkbox"]')
    original_tag.click()
    time.sleep(1)
    original_tag_click = driver.find_element(By.XPATH, '//div[@class="original-type-form"]//dt[contains(text(),"请选择")]')
    actions.move_to_element(original_tag_click).click().perform()
    time.sleep(1)
    original_tag_item = driver.find_element(By.XPATH,
                                             '//div[@class="original-type-form"]//span[text()="知识"]')
    actions.move_to_element(original_tag_item).click().perform()
    time.sleep(1)
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
