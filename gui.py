import time

import streamlit as st
import tkinter as tk
from config.config import my_config, save_config, languages
from pages.common import common_ui
from tools.tr_utils import tr

common_ui()

st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            AI搞钱工具</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>基本配置信息</h2>", unsafe_allow_html=True)

if 'ui_language' not in st.session_state:
    st.session_state['ui_language'] = 'zh-CN - 简体中文'


def set_ui_language():
    print('set_ui_language:', st.session_state['ui_language'])
    my_config['ui']['language'] = st.session_state['ui_language'].split(" - ")[0].strip()
    print('set ui language:', my_config['ui']['language'])
    save_config()


def save_pexels_api_key():
    my_config['resource']['pexels']['api_key'] = st.session_state['pexels_api_key']
    save_config()


def save_pixabay_api_key():
    my_config['resource']['pixabay']['api_key'] = st.session_state['pixabay_api_key']
    save_config()


def set_llm_provider():
    my_config['llm']['provider'] = st.session_state['llm_provider']
    save_config()


def set_resource_provider():
    my_config['resource']['provider'] = st.session_state['resource_provider']
    save_config()


def set_audio_provider():
    my_config['audio']['provider'] = st.session_state['audio_provider']
    save_config()


def set_audio_key(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['speech_key'] = st.session_state[key]
    save_config()


def set_audio_access_key_id(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['access_key_id'] = st.session_state[key]
    save_config()


def set_audio_access_key_secret(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['access_key_secret'] = st.session_state[key]
    save_config()


def set_audio_app_key(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['app_key'] = st.session_state[key]
    save_config()


def set_audio_region(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['service_region'] = st.session_state[key]
    save_config()


def set_llm_sk(provider, key):
    my_config['llm'][provider]['secret_key'] = st.session_state[key]
    save_config()


def set_llm_key(provider, key):
    my_config['llm'][provider]['api_key'] = st.session_state[key]
    save_config()


def set_llm_base_url(provider, key):
    my_config['llm'][provider]['base_url'] = st.session_state[key]
    save_config()


def set_llm_model_name(provider, key):
    if provider not in my_config['llm']:
        my_config['llm'][provider] = {}
    my_config['llm'][provider]['model_name'] = st.session_state[key]
    save_config()


# 设置language
display_languages = []
selected_index = 0
for i, code in enumerate(languages.keys()):
    display_languages.append(f"{code} - {languages[code]}")
    if f"{code} - {languages[code]}" == st.session_state['ui_language']:
        selected_index = i
# print("selected_index:", selected_index)
selected_language = st.selectbox(tr("Language"), options=display_languages,
                                 index=selected_index, key='ui_language', on_change=set_ui_language)
# 设置资源
resource_container = st.container(border=True)
with resource_container:
    resource_providers = ['pexels', 'pixabay']
    selected_resource_provider = my_config['resource']['provider']
    selected_resource_provider_index = 0
    for i, provider in enumerate(resource_providers):
        if provider == selected_resource_provider:
            selected_resource_provider_index = i
            break

    llm_provider = st.selectbox(tr("Resource Provider"), options=resource_providers,
                                index=selected_resource_provider_index,
                                key='resource_provider', on_change=set_resource_provider)

    # 设置资源key
    key_panels = st.columns(2)
    with key_panels[0]:
        pexels_api_key = my_config['resource']['pexels']['api_key']
        pexels_api_key = st.text_input(tr("Pexels API Key"), value=pexels_api_key, type="password",
                                       key='pexels_api_key',
                                       on_change=save_pexels_api_key)
    with key_panels[1]:
        pixabay_api_key = my_config['resource']['pixabay']['api_key']
        pixabay_api_key = st.text_input(tr("Pixabay API Key"), value=pixabay_api_key, type="password",
                                        key='pixabay_api_key', on_change=save_pixabay_api_key)

# 设置语音
audio_container = st.container(border=True)
with audio_container:
    st.info(tr("Audio Provider Info"))
    audio_providers = ['Azure', 'Ali']
    # audio_providers = ['Azure']
    selected_audio_provider = my_config['audio']['provider']
    selected_audio_provider_index = 0
    for i, provider in enumerate(audio_providers):
        if provider == selected_audio_provider:
            selected_audio_provider_index = i
            break

    audio_provider = st.selectbox(tr("Audio Provider"), options=audio_providers, index=selected_audio_provider_index,
                                  key='audio_provider', on_change=set_audio_provider)
    with st.expander(audio_provider, expanded=True):
        if audio_provider == 'Azure':
            st.info(tr("Audio Azure config"))
            audio_columns = st.columns(2)
            with audio_columns[0]:
                st.text_input(label=tr("Speech Key"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('speech_key', ''),
                              on_change=set_audio_key, key=audio_provider + "_speech_key",
                              args=(audio_provider, audio_provider + '_speech_key'))
            with audio_columns[1]:
                st.text_input(label=tr("Service Region"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('service_region', ''),
                              on_change=set_audio_region,
                              key=audio_provider + "_service_region",
                              args=(audio_provider, audio_provider + '_service_region'))
        if audio_provider == 'Ali':
            st.info(tr("Audio Ali config"))
            audio_columns = st.columns(3)
            with audio_columns[0]:
                st.text_input(label=tr("Access Key ID"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('access_key_id', ''),
                              on_change=set_audio_access_key_id, key=audio_provider + "_access_key_id",
                              args=(audio_provider, audio_provider + '_access_key_id'))
            with audio_columns[1]:
                st.text_input(label=tr("Access Key Secret"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('access_key_secret', ''),
                              on_change=set_audio_access_key_secret, key=audio_provider + "_access_key_secret",
                              args=(audio_provider, audio_provider + '_access_key_secret'))
            with audio_columns[2]:
                st.text_input(label=tr("App Key"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('app_key', ''),
                              on_change=set_audio_app_key, key=audio_provider + "_app_key",
                              args=(audio_provider, audio_provider + '_app_key'))

# 设置默认的LLM
llm_container = st.container(border=True)
with (llm_container):
    llm_providers = ['OpenAI', 'Moonshot', 'Azure', 'Qianfan', 'Baichuan', 'Tongyi', 'DeepSeek']
    saved_llm_provider = my_config['llm']['provider']
    saved_llm_provider_index = 0
    for i, provider in enumerate(llm_providers):
        if provider == saved_llm_provider:
            saved_llm_provider_index = i
            break

    llm_provider = st.selectbox(tr("LLM Provider"), options=llm_providers, index=saved_llm_provider_index,
                                key='llm_provider', on_change=set_llm_provider)
    print(llm_provider)

    # 设置llm的值：
    with st.expander(llm_provider, expanded=True):
        tips = f"""
               ##### {llm_provider} 配置信息
               """
        st.info(tips)
        st_llm_api_key = st.text_input(tr("API Key"),
                                       value=my_config['llm'].get(llm_provider, {}).get('api_key', ''),
                                       type="password", key=llm_provider + '_api_key', on_change=set_llm_key,
                                       args=(llm_provider, llm_provider + '_api_key'))

        if llm_provider == 'Qianfan':
            st_llm_base_url = st.text_input(tr("Secret Key"),
                                            value=my_config['llm'].get(llm_provider, {}).get('secret_key', ''),
                                            type="password", key=llm_provider + '_secret_key', on_change=set_llm_sk,
                                            args=(llm_provider, llm_provider + '_secret_key'))
        else:
            if llm_provider == 'Azure' or llm_provider == 'DeepSeek':
                st_llm_base_url = st.text_input(tr("Base Url"),
                                                value=my_config['llm'].get(llm_provider, {}).get('base_url', ''),
                                                type="password", key=llm_provider + '_base_url',
                                                on_change=set_llm_base_url,
                                                args=(llm_provider, llm_provider + '_base_url'))

        st_llm_model_name = st.text_input(tr("Model Name"),
                                          value=my_config['llm'].get(llm_provider, {}).get('model_name', ''),
                                          key=llm_provider + '_model_name', on_change=set_llm_model_name,
                                          args=(llm_provider, llm_provider + '_model_name'))
