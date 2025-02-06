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

import streamlit as st
from config.config import my_config, save_config, languages, test_config, local_audio_tts_providers, \
    local_audio_recognition_providers, local_audio_recognition_fasterwhisper_module_names, \
    local_audio_recognition_fasterwhisper_device_types, local_audio_recognition_fasterwhisper_compute_types, \
    delete_first_visit_session_state, app_title
from pages.common import common_ui
from tools.tr_utils import tr

delete_first_visit_session_state("all_first_visit")

common_ui()

st.markdown(f"<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            {app_title}</h1>", unsafe_allow_html=True)
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


def save_stable_diffusion_api_user_name():
    test_config(my_config, "resource", 'stableDiffusion')
    my_config['resource']['stableDiffusion']['user_name'] = st.session_state['stableDiffusion_api_user_name']
    save_config()


def save_stable_diffusion_api_password():
    test_config(my_config, "resource", 'stableDiffusion')
    my_config['resource']['stableDiffusion']['password'] = st.session_state['stableDiffusion_api_password']
    save_config()


def save_stable_diffusion_api_server_address():
    test_config(my_config, "resource", 'stableDiffusion')
    my_config['resource']['stableDiffusion']['server_address'] = st.session_state['stableDiffusion_api_server_address']
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


def set_local_audio_tts_provider():
    test_config(my_config, "audio", "local_tts", 'provider')
    my_config['audio']['local_tts']['provider'] = st.session_state['local_audio_tts_provider']
    save_config()


def set_local_audio_recognition_provider():
    test_config(my_config, "audio", "local_recognition", 'provider')
    my_config['audio']['local_recognition']['provider'] = st.session_state['local_audio_recognition_provider']
    save_config()


def get_recognition_value(key):
    recognition_provider = st.session_state['local_audio_recognition_provider']
    return my_config['audio'].get('local_recognition', {}).get(recognition_provider, {}).get(key, '')


def set_recognition_value(key, session_key):
    recognition_provider = st.session_state['local_audio_recognition_provider']
    test_config(my_config, "audio", "local_recognition", recognition_provider, key)
    my_config['audio']['local_recognition'][recognition_provider][key] = st.session_state[session_key]
    save_config()


def get_chatTTS_server_location():
    return my_config['audio'].get('local_tts', {}).get('chatTTS', {}).get('server_location', '')


def set_chatTTS_server_location():
    test_config(my_config, "audio", "local_tts", 'chatTTS', 'server_location')
    my_config['audio']['local_tts']['chatTTS']['server_location'] = st.session_state['chatTTS_server_location']
    save_config()


def get_GPTSoVITS_server_location():
    return my_config['audio'].get('local_tts', {}).get('GPTSoVITS', {}).get('server_location', '')


def set_GPTSoVITS_server_location():
    test_config(my_config, "audio", "local_tts", 'GPTSoVITS', 'server_location')
    my_config['audio']['local_tts']['GPTSoVITS']['server_location'] = st.session_state['GPTSoVITS_server_location']
    save_config()


def get_CosyVoice_server_location():
    return my_config['audio'].get('local_tts', {}).get('CosyVoice', {}).get('server_location', '')


def set_CosyVoice_server_location():
    test_config(my_config, "audio", "local_tts", 'CosyVoice', 'server_location')
    my_config['audio']['local_tts']['CosyVoice']['server_location'] = st.session_state['CosyVoice_server_location']
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
    resource_providers = ['pexels', 'pixabay', 'stableDiffusion', 'comfyUI']
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
    key_panels = st.columns(3)
    if selected_resource_provider == 'pexels':
        with key_panels[0]:
            pexels_api_key = my_config['resource']['pexels']['api_key']
            pexels_api_key = st.text_input(tr("Pexels API Key"), value=pexels_api_key, type="password",
                                           key='pexels_api_key',
                                           on_change=save_pexels_api_key)
    if selected_resource_provider == 'pixabay':
        with key_panels[0]:
            pixabay_api_key = my_config['resource']['pixabay']['api_key']
            pixabay_api_key = st.text_input(tr("Pixabay API Key"), value=pixabay_api_key, type="password",
                                            key='pixabay_api_key', on_change=save_pixabay_api_key)
    if selected_resource_provider == 'stableDiffusion':
        with key_panels[0]:
            sd_api_user_name = my_config['resource'].get('stableDiffusion', {}).get('user_name', '')
            st.text_input(tr("Stable Diffusion API User Name"), value=sd_api_user_name,
                          key='stableDiffusion_api_user_name', on_change=save_stable_diffusion_api_user_name)
        with key_panels[1]:
            sd_api_password = my_config['resource'].get('stableDiffusion', {}).get('password', '')
            st.text_input(tr("Stable Diffusion API Password"), type="password", value=sd_api_password,
                          key='stableDiffusion_api_password', on_change=save_stable_diffusion_api_password)
        with key_panels[2]:
            sd_api_address = my_config['resource'].get('stableDiffusion', {}).get('server_address', '')
            st.text_input(tr("Stable Diffusion API Server Address"), value=sd_api_address,
                          key='stableDiffusion_api_server_address', on_change=save_stable_diffusion_api_server_address)

# 设置语音
audio_container = st.container(border=True)
with audio_container:
    st.info(tr("Audio Provider Info"))

    # local TTS config
    local_tts_container = st.container(border=True)
    with local_tts_container:
        selected_local_audio_tts_provider = my_config['audio'].get('local_tts', {}).get('provider', '')
        if not selected_local_audio_tts_provider:
            selected_local_audio_tts_provider = 'chatTTS'
            st.session_state['local_audio_tts_provider'] = selected_local_audio_tts_provider
            set_local_audio_tts_provider()
        selected_local_audio_tts_provider_index = 0
        for i, provider in enumerate(local_audio_tts_providers):
            if provider == selected_local_audio_tts_provider:
                selected_local_audio_tts_provider_index = i
                break

        local_audio_tts_provider = st.selectbox(tr("Local Audio TTS Provider"), options=local_audio_tts_providers,
                                                index=selected_local_audio_tts_provider_index,
                                                key='local_audio_tts_provider', on_change=set_local_audio_tts_provider)
        if local_audio_tts_provider == 'chatTTS':
            st.text_input(label=tr("ChatTTS http server location"), placeholder=tr("Input chatTTS http server address"),
                          value=get_chatTTS_server_location(),
                          key="chatTTS_server_location", on_change=set_chatTTS_server_location)
        if local_audio_tts_provider == 'GPTSoVITS':
            st.text_input(label=tr("GPT-SoVITS http server location"),
                          placeholder=tr("Input GPT-SoVITS http server address"),
                          value=get_GPTSoVITS_server_location(),
                          key="GPTSoVITS_server_location", on_change=set_GPTSoVITS_server_location)
        if local_audio_tts_provider == 'CosyVoice':
            st.text_input(label=tr("CosyVoice http server location"),
                          placeholder=tr("Input CosyVoice http server address"),
                          value=get_CosyVoice_server_location(),
                          key="CosyVoice_server_location", on_change=set_CosyVoice_server_location,
                          help=tr("Download the cosyvoice-api from https://github.com/diudiu62/CosyVoice-api.git"))
    # local recognition config
    local_recognition_container = st.container(border=True)
    with local_recognition_container:
        selected_local_audio_recognition_provider = my_config['audio'].get('local_recognition', {}).get('provider', '')
        if not selected_local_audio_recognition_provider:
            selected_local_audio_recognition_provider = 'fasterwhisper'
            st.session_state['local_audio_recognition_provider'] = selected_local_audio_recognition_provider
            set_local_audio_recognition_provider()
        selected_local_audio_recognition_provider_index = 0
        for i, provider in enumerate(local_audio_recognition_providers):
            if provider == selected_local_audio_recognition_provider:
                selected_local_audio_recognition_provider_index = i
                break

        local_audio_recognition_provider = st.selectbox(tr("Local Audio recognition Provider"),
                                                        options=local_audio_recognition_providers,
                                                        index=selected_local_audio_recognition_provider_index,
                                                        key='local_audio_recognition_provider',
                                                        on_change=set_local_audio_recognition_provider)
        if selected_local_audio_recognition_provider == 'sensevoice':
            st.info(tr("⚠️参考项目sensevoice文件夹中的README.md，下载sherpa-onnx-sense-voice相关模型"))  # 添加帮助信息

        if selected_local_audio_recognition_provider == 'fasterwhisper':                                    
            recognition_columns = st.columns(3)
            with recognition_columns[0]:
                selected_local_audio_recognition_module = my_config['audio'].get('local_recognition', {}).get(
                    st.session_state['local_audio_recognition_provider'],
                    {}).get('model_name',
                            '')
                if not selected_local_audio_recognition_module:
                    selected_local_audio_recognition_module = 'tiny'
                    st.session_state['recognition_model_name'] = selected_local_audio_recognition_module
                    set_recognition_value('model_name', 'recognition_model_name')
                selected_local_audio_recognition_module_index = 0
                for i, module_name in enumerate(local_audio_recognition_fasterwhisper_module_names):
                    if module_name == selected_local_audio_recognition_module:
                        selected_local_audio_recognition_module_index = i
                        break
                st.selectbox(tr("model name"),
                            options=local_audio_recognition_fasterwhisper_module_names,
                            index=selected_local_audio_recognition_module_index,
                            key='recognition_model_name',
                            on_change=set_recognition_value, args=('model_name', 'recognition_model_name',))
            with recognition_columns[1]:
                selected_local_audio_recognition_device = my_config['audio'].get('local_recognition', {}).get(
                    st.session_state['local_audio_recognition_provider'],
                    '').get('device_type', '')
                if not selected_local_audio_recognition_device:
                    selected_local_audio_recognition_device = 'cpu'
                    st.session_state['recognition_device_type'] = selected_local_audio_recognition_device
                    set_recognition_value('device_type', 'recognition_device_type')
                selected_local_audio_recognition_device_index = 0
                for i, module_name in enumerate(local_audio_recognition_fasterwhisper_device_types):
                    if module_name == selected_local_audio_recognition_device:
                        selected_local_audio_recognition_device_index = i
                        break
                st.selectbox(tr("device type"),
                            options=local_audio_recognition_fasterwhisper_device_types,
                            index=selected_local_audio_recognition_device_index,
                            key='recognition_device_type',
                            on_change=set_recognition_value, args=('device_type', 'recognition_device_type',))
            with recognition_columns[2]:
                selected_local_audio_recognition_compute = my_config['audio'].get('local_recognition', {}).get(
                    st.session_state['local_audio_recognition_provider'],
                    '').get('compute_type', '')
                if not selected_local_audio_recognition_compute:
                    selected_local_audio_recognition_compute = 'int8'
                    st.session_state['recognition_compute_type'] = selected_local_audio_recognition_compute
                    set_recognition_value('compute_type', 'recognition_compute_type')
                selected_local_audio_recognition_compute_index = 0
                for i, module_name in enumerate(local_audio_recognition_fasterwhisper_compute_types):
                    if module_name == selected_local_audio_recognition_compute:
                        selected_local_audio_recognition_compute_index = i
                        break
                st.selectbox(tr("compute type"),
                            options=local_audio_recognition_fasterwhisper_compute_types,
                            index=selected_local_audio_recognition_compute_index,
                            key='recognition_compute_type',
                            on_change=set_recognition_value, args=('compute_type', 'recognition_compute_type',))            

    # remote Audio config
    audio_providers = ['Azure', 'Ali', 'Tencent']
    selected_audio_provider = my_config['audio']['provider']
    selected_audio_provider_index = 0
    for i, provider in enumerate(audio_providers):
        if provider == selected_audio_provider:
            selected_audio_provider_index = i
            break

    audio_provider = st.selectbox(tr("Remote Audio Provider"), options=audio_providers,
                                  index=selected_audio_provider_index,
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
        if audio_provider == 'Tencent':
            st.info(tr("Audio Tencent config"))
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
                st.text_input(label=tr("App ID"), type="password",
                              value=my_config['audio'].get(audio_provider, {}).get('app_key', ''),
                              on_change=set_audio_app_key, key=audio_provider + "_app_key",
                              args=(audio_provider, audio_provider + '_app_key'))

# 设置默认的LLM
llm_container = st.container(border=True)
with (llm_container):
    llm_providers = ['OpenAI', 'Moonshot', 'Azure', 'Qianfan', 'Baichuan', 'Tongyi', 'DeepSeek', 'Ollama']
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
        if llm_provider != 'Ollama':
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
            if llm_provider == 'Azure' or llm_provider == 'DeepSeek' or llm_provider == 'Ollama':
                st_llm_base_url = st.text_input(tr("Base Url"),
                                                value=my_config['llm'].get(llm_provider, {}).get('base_url', ''),
                                                type="password", key=llm_provider + '_base_url',
                                                on_change=set_llm_base_url,
                                                args=(llm_provider, llm_provider + '_base_url'))

        st_llm_model_name = st.text_input(tr("Model Name"),
                                          value=my_config['llm'].get(llm_provider, {}).get('model_name', ''),
                                          key=llm_provider + '_model_name', on_change=set_llm_model_name,
                                          args=(llm_provider, llm_provider + '_model_name'))
