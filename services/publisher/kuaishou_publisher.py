import sys

import pyperclip
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import streamlit as st

import time

from config.config import kuaishou_site
from tools.file_utils import read_file_with_extra_enter


def kuaishou_publisher(driver, video_file, text_file):

    # driver.switch_to.window(driver.window_handles[0])

    # 打开新标签页并切换到新标签页
    driver.switch_to.new_window('tab')

    # 浏览器实例现在可以被重用，进行你的自动化操作
    driver.get(kuaishou_site)
    time.sleep(2)  # 等待2秒

    # 设置等待
    wait = WebDriverWait(driver, 10)

    # 上传视频按钮
    file_input = driver.find_element(By.XPATH,'//input[@type="file"]')
    file_input.send_keys(video_file)
    time.sleep(10)  # 等待
    # 等待视频上传完毕
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@placeholder, "添加合适的话题和描述")]')))

    # 设置标题
    use_common = st.session_state.get('video_publish_use_common_config')
    if use_common:
        common_title = st.session_state.get('video_publish_title_prefix')
    else:
        common_title = st.session_state.get('video_publish_kuaishou_title_prefix')

    # 设置内容
    content = driver.find_element(By.XPATH, '//div[contains(@placeholder, "添加合适的话题和描述")]')
    content.click()
    time.sleep(2)
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    # 将要粘贴的文本内容复制到剪贴板
    content_text = read_file_with_extra_enter(text_file)
    content_text = content_text[:450]
    pyperclip.copy(common_title + content_text)
    action_chains = webdriver.ActionChains(driver)
    # 模拟实际的粘贴操作
    action_chains.key_down(cmd_ctrl).send_keys('v').key_up(cmd_ctrl).perform()
    time.sleep(2)

    # 设置tags
    if use_common:
        tags = st.session_state.get('video_publish_tags')
    else:
        tags = st.session_state.get('video_publish_kuaishou_tags')
    i =0
    tags = tags.split()
    for tag in tags:
        # 快手只接受三个标签
        if i == 3:
            break
        content.send_keys(' ')
        content.send_keys(tag)
        time.sleep(2)
        content.send_keys(Keys.ENTER)
        time.sleep(1)
        content.send_keys(' ')
        time.sleep(2)
        i=i+1

    # 设置合集
    if use_common:
        collection = st.session_state.get('video_publish_collection_name')
    else:
        collection = st.session_state.get('video_publish_kuaishou_collection_name')
    if collection:
        collection_tag = driver.find_element(By.XPATH, '//span[contains(text(),"选择要加入到的合集")]')
        actions = ActionChains(driver)
        actions.move_to_element(collection_tag).click().perform()
        # collection_tag.click()
        time.sleep(1)
        collection_to_select = driver.find_element(By.XPATH, f'//div[@label="{collection}"]')
        collection_to_select.click()
        time.sleep(1)

    # 设置领域
    domain =  st.session_state.get('video_publish_enable_kuaishou_domain')
    if domain:
        print("设置领域")
        domain_tag = driver.find_element(By.XPATH, '//span[contains(text(),"请选择")]')
        actions = ActionChains(driver)
        actions.move_to_element(domain_tag).click().perform()
        # domain_tag.click()
        time.sleep(1)
        domain_level1 = st.session_state.get('video_publish_kuaishou_domain_level1')
        domain_level_1 =driver.find_element(By.XPATH, f'//div[@title="{domain_level1}"]')
        actions = ActionChains(driver)
        actions.move_to_element(domain_level_1).click().perform()
        # domain_level_1.click()
        time.sleep(1)

        domain_level2 = st.session_state.get('video_publish_kuaishou_domain_level2')
        domain_level2_tag = driver.find_element(By.XPATH, '//span[contains(text(),"请选择")]')
        actions = ActionChains(driver)
        actions.move_to_element(domain_level2_tag).click().perform()
        # domain_level2_tag.click()
        time.sleep(1)

        domain_level_2 = driver.find_element(By.XPATH, f'//div[@title="{domain_level2}"]')
        actions = ActionChains(driver)
        actions.move_to_element(domain_level_2).click().perform()
        # domain_level_2.click()
        time.sleep(1)

    # 发布
    publish_button = driver.find_element(By.XPATH, '//button[@type="button"]/span[text()="发布"]')
    auto_publish = st.session_state.get('video_publish_auto_publish')
    if auto_publish:
        print("auto publish")
        publish_button.click()







