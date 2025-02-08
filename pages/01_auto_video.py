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

from config.config import my_config, save_config, languages, audio_languages, transition_types, \
    fade_list, audio_types, load_session_state_from_yaml, save_session_state_to_yaml, app_title, GPT_soVITS_languages, CosyVoice_voice
from main import main_generate_video_content, main_generate_ai_video, main_generate_video_dubbing, \
    main_get_video_resource, main_generate_subtitle, main_try_test_audio, get_audio_voices, main_try_test_local_audio, \
    main_generate_ai_video_from_img
from pages.common import common_ui
from services.sd.sd_service import SDService
from tools.tr_utils import tr

import os

from tools.utils import get_file_map_from_dir

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

default_bg_music_dir = os.path.join(script_dir, "../bgmusic")
default_bg_music_dir = os.path.abspath(default_bg_music_dir)

default_chattts_dir = os.path.join(script_dir, "../chattts")
default_chattts_dir = os.path.abspath(default_chattts_dir)

load_session_state_from_yaml('01_first_visit')


def save_to_config(region, key):
    value = st.session_state.get(key)
    if value:
        if not my_config[region]:
            my_config[region] = {}
        my_config[region][key] = value
        save_config()


common_ui()


def get_video_resource():
    main_get_video_resource()


def generate_subtitle():
    main_generate_subtitle()


def generate_video_content():
    main_generate_video_content()


def generate_video_dubbing():
    main_generate_video_dubbing()


def try_test_audio():
    main_try_test_audio()


def try_test_local_audio():
    main_try_test_local_audio()


def generate_video(video_generator):
    save_session_state_to_yaml()
    resource_provider = my_config['resource']['provider']
    if resource_provider == 'stableDiffusion':
        main_generate_ai_video_from_img(video_generator)
    else:
        main_generate_ai_video(video_generator)


st.markdown(f"<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            {app_title}</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>自动短视频生成器</h2>", unsafe_allow_html=True)

# LLM区域
llm_container = st.container(border=True)
with llm_container:
    st.subheader(tr("LLM Video Subject generator"))
    st.info(tr("Please input video subject, then click the generate button to generate the video content"))
    st.text_input(label=tr("Video Subject"), placeholder=tr("Please input video subject"), key="video_subject")
    llm_columns = st.columns(3)
    video_length_options = {"60": "60字以内", "120": "120字以内", "300": "300字以内", "600": "600字以内"}
    # video_length_options = {"60": "60字以内", "120": "120字以内", "300": "300字以内"}
    with llm_columns[0]:
        st.selectbox(label=tr("Video content language"), options=languages, format_func=lambda x: languages.get(x),
                     key="video_language")
    with llm_columns[1]:
        st.selectbox(label=tr("Video length"), options=video_length_options,
                     format_func=lambda x: video_length_options.get(x), key="video_length")
        # print(st.session_state.get("video_length"))
    with llm_columns[2]:
        st.button(label=tr("Generate Video Content"), type="primary", on_click=generate_video_content)
    # print(st.session_state.get("video_content"))
    st.text_area(label=tr("Video content"), key="video_content", height=200)
    st.text_input(label=tr("Video content keyword"), key="video_keyword")

# 资源区
resource_container = st.container(border=True)
with resource_container:
    st.subheader(tr("Video Source"))
    resource_name = my_config['resource'].get('provider', '')
    st.text(tr("Using Resource:") + resource_name)
    if resource_name == "stableDiffusion":
        sd_service = SDService()
        sd_checkpoints = sd_service.get_checkpoints()
        llm_columns = st.columns(4)
        with llm_columns[0]:
            st.selectbox(label=tr("Check Point"), options=sd_checkpoints,
                         key="sd_checkpoint")
        with llm_columns[1]:
            st.slider(label=tr("Width"), min_value=64, max_value=2048, step=1, value=720, key="sd_width")
        with llm_columns[2]:
            st.slider(label=tr("Height"), min_value=64, max_value=2048, step=1, value=1280, key="sd_height")
        with llm_columns[3]:
            st.text_input(label=tr("Seed"), value=2008, key="sd_seed")
        llm_columns = st.columns(4)
        with llm_columns[0]:
            sd_samplers = sd_service.get_samples()
            st.selectbox(label=tr("Sampler"), options=sd_samplers,  key="sd_sample")
        with llm_columns[1]:
            sd_schedules = sd_service.get_schedulers()
            st.selectbox(label=tr("Schedule"), options=sd_schedules,  key="sd_schedule")
        with llm_columns[2]:
            st.slider(label=tr("Steps"), min_value=1, max_value=150, step=1, value=20, key="sd_step")
        with llm_columns[3]:
            st.slider(label=tr("CFG Scale"), min_value=0.0, max_value=1.0, step=0.1, value=0.7, key="sd_cfg_scale")

# 配音区域
captioning_container = st.container(border=True)
with captioning_container:
    # 配音
    st.subheader(tr("Video Captioning"))

    llm_columns = st.columns(4)
    with llm_columns[0]:
        st.selectbox(label=tr("Choose TTS audio type"), options=audio_types, format_func=lambda x: audio_types.get(x),
                     key="audio_type")

    if st.session_state.get("audio_type") == "remote":
        llm_columns = st.columns(4)
        audio_voice = get_audio_voices()
        with llm_columns[0]:
            st.selectbox(label=tr("Audio language"), options=audio_languages,
                         format_func=lambda x: audio_languages.get(x), key="audio_language")
        with llm_columns[1]:
            st.selectbox(label=tr("Audio voice"),
                         options=audio_voice.get(st.session_state.get("audio_language")),
                         format_func=lambda x: audio_voice.get(st.session_state.get("audio_language")).get(x),
                         key="audio_voice")
        with llm_columns[2]:
            st.selectbox(label=tr("Audio speed"),
                         options=["normal", "fast", "faster", "fastest", "slow", "slower", "slowest"],
                         key="audio_speed")
        with llm_columns[3]:
            st.button(label=tr("Testing Audio"), type="primary", on_click=try_test_audio)
    if st.session_state.get("audio_type") == "local":
        selected_local_audio_tts_provider = my_config['audio'].get('local_tts', {}).get('provider', '')
        if not selected_local_audio_tts_provider:
            selected_local_audio_tts_provider = 'chatTTS'
        if selected_local_audio_tts_provider == 'chatTTS':
            llm_columns = st.columns(5)
            with llm_columns[0]:
                st.checkbox(label=tr("Refine text"), key="refine_text")
                st.text_input(label=tr("Refine text Prompt"), placeholder=tr("[oral_2][laugh_0][break_6]"),
                              key="refine_text_prompt")
            with llm_columns[1]:
                st.slider(label=tr("Text Seed"), min_value=1, value=20, max_value=4294967295, step=1,
                          key="text_seed")
            with llm_columns[2]:
                st.slider(label=tr("Audio Temperature"), min_value=0.01, value=0.3, max_value=1.0, step=0.01,
                          key="audio_temperature")
            with llm_columns[3]:
                st.slider(label=tr("top_P"), min_value=0.1, value=0.7, max_value=0.9, step=0.1,
                          key="audio_top_p")
            with llm_columns[4]:
                st.slider(label=tr("top_K"), min_value=1, value=20, max_value=20, step=1,
                          key="audio_top_k")

            st.checkbox(label=tr("Use random voice"), key="use_random_voice")

            if st.session_state.get("use_random_voice"):
                llm_columns = st.columns(4)
                with llm_columns[0]:
                    st.slider(label=tr("Audio Seed"), min_value=1, value=20, max_value=4294967295, step=1,
                              key="audio_seed")
                with llm_columns[1]:
                    st.selectbox(label=tr("Audio speed"),
                                 options=["normal", "fast", "faster", "fastest", "slow", "slower", "slowest"],
                                 key="audio_speed")
                with llm_columns[2]:
                    st.button(label=tr("Testing Audio"), type="primary", on_click=try_test_local_audio)
            else:
                llm_columns = st.columns(4)
                with llm_columns[0]:
                    st.text_input(label=tr("Local Chattts Dir"), placeholder=tr("Input Local Chattts Dir"),
                                  value=default_chattts_dir,
                                  key="default_chattts_dir")
                with llm_columns[1]:
                    chattts_list = get_file_map_from_dir(st.session_state["default_chattts_dir"], ".pt,.txt")
                    st.selectbox(label=tr("Audio voice"), key="audio_voice",
                                 options=chattts_list, format_func=lambda x: chattts_list[x])
                with llm_columns[2]:
                    st.selectbox(label=tr("Audio speed"),
                                 options=["normal", "fast", "faster", "fastest", "slow", "slower", "slowest"],
                                 key="audio_speed")
                with llm_columns[3]:
                    st.button(label=tr("Testing Audio"), type="primary", on_click=try_test_local_audio)
        if selected_local_audio_tts_provider == 'GPTSoVITS':
            use_reference_audio = st.checkbox(label=tr("Use reference audio"), key="use_reference_audio")
            if use_reference_audio:
                llm_columns = st.columns(4)
                with llm_columns[0]:
                    st.file_uploader(label=tr("Reference Audio"), type=["wav", "mp3"], accept_multiple_files=False,
                                     key="reference_audio")
                with llm_columns[1]:
                    st.text_area(label=tr("Reference Audio Text"), placeholder=tr("Input Reference Audio Text"),
                                 key="reference_audio_text")
                with llm_columns[2]:
                    st.selectbox(label=tr("Reference Audio language"), options=GPT_soVITS_languages,
                                 format_func=lambda x: GPT_soVITS_languages.get(x),
                                 key="reference_audio_language")
            llm_columns = st.columns(6)
            with llm_columns[0]:
                st.slider(label=tr("Audio Temperature"), min_value=0.01, value=0.3, max_value=1.0, step=0.01,
                          key="audio_temperature")
            with llm_columns[1]:
                st.slider(label=tr("top_P"), min_value=0.1, value=0.7, max_value=0.9, step=0.1,
                          key="audio_top_p")
            with llm_columns[2]:
                st.slider(label=tr("top_K"), min_value=1, value=20, max_value=20, step=1,
                          key="audio_top_k")
            with llm_columns[3]:
                st.selectbox(label=tr("Audio speed"),
                             options=["normal", "fast", "faster", "fastest", "slow", "slower", "slowest"],
                             key="audio_speed")
            with llm_columns[4]:
                st.selectbox(label=tr("Inference Audio language"),
                             options=GPT_soVITS_languages, format_func=lambda x: GPT_soVITS_languages.get(x),
                             key="inference_audio_language")
            with llm_columns[5]:
                st.button(label=tr("Testing Audio"), type="primary", on_click=try_test_local_audio)

        if selected_local_audio_tts_provider == 'CosyVoice':
            use_reference_audio = st.checkbox(label=tr("Use reference audio"), key="use_reference_audio")
            if use_reference_audio:
                llm_columns = st.columns(2)
                with llm_columns[0]:
                    # st.file_uploader(label=tr("Reference Audio"), type=["wav", "mp3"], accept_multiple_files=False,
                    #                  key="reference_audio")
                    st.text_input(label=tr("Reference Audio"), placeholder=tr("Input Reference Audio File Path"),
                      key="reference_audio_file_path")
                with llm_columns[1]:
                    st.text_area(label=tr("Reference Audio Text"), placeholder=tr("Input Reference Audio Text"),
                                 key="reference_audio_text")
            else:
                llm_columns = st.columns(1)
                st.selectbox(label=tr("Reference Audio language"), options=CosyVoice_voice,
                            format_func=lambda x: CosyVoice_voice.get(x),
                            key="reference_audio_language")
            llm_columns = st.columns(3)
            with llm_columns[0]:
                st.slider(label=tr("Text Seed"), min_value=1, value=20, max_value=4294967295, step=1,
                          key="text_seed")
            with llm_columns[1]:
                st.selectbox(label=tr("Audio speed"),
                             options=["normal", "fast", "faster", "fastest", "slow", "slower", "slowest"],
                             key="audio_speed")
            with llm_columns[2]:
                st.button(label=tr("Testing Audio"), type="primary", on_click=try_test_local_audio)

recognition_container = st.container(border=True)
with recognition_container:
    # 配音
    st.subheader(tr("Audio recognition"))

    llm_columns = st.columns(4)
    with llm_columns[0]:
        st.selectbox(label=tr("Choose recognition type"), options=audio_types, format_func=lambda x: audio_types.get(x),
                     key="recognition_audio_type")

# 背景音乐
bg_music_container = st.container(border=True)
with bg_music_container:
    # 背景音乐
    st.subheader(tr("Video Background Music"))
    llm_columns = st.columns(2)
    with llm_columns[0]:
        st.text_input(label=tr("Background Music Dir"), placeholder=tr("Input Background Music Dir"),
                      value=default_bg_music_dir,
                      key="background_music_dir")

    with llm_columns[1]:
        nest_columns = st.columns(3)
        with nest_columns[0]:
            st.checkbox(label=tr("Enable background music"), key="enable_background_music", value=True)
        with nest_columns[1]:
            bg_music_list = get_file_map_from_dir(st.session_state["background_music_dir"], ".mp3,.wav")
            st.selectbox(label=tr("Background music"), key="background_music",
                         options=bg_music_list, format_func=lambda x: bg_music_list[x])
        with nest_columns[2]:
            st.slider(label=tr("Background music volume"), min_value=0.0, value=0.3, max_value=1.0, step=0.1,
                      key="background_music_volume")

# 视频配置
video_container = st.container(border=True)

with video_container:
    st.subheader(tr("Video Config"))
    llm_columns = st.columns(3)
    with llm_columns[0]:
        layout_options = {"portrait": "竖屏", "landscape": "横屏", "square": "方形"}
        st.selectbox(label=tr("video layout"), key="video_layout", options=layout_options,
                     format_func=lambda x: layout_options[x])
    with llm_columns[1]:
        st.selectbox(label=tr("video fps"), key="video_fps", options=[20, 25, 30])
    with llm_columns[2]:
        if st.session_state.get("video_layout") == "portrait":
            video_size_options = {"1080x1920": "1080p", "720x1280": "720p", "480x960": "480p", "360x720": "360p",
                                  "240x480": "240p"}
        elif st.session_state.get("video_layout") == "landscape":
            video_size_options = {"1920x1080": "1080p", "1280x720": "720p", "960x480": "480p", "720x360": "360p",
                                  "480x240": "240p"}
        else:
            video_size_options = {"1080x1080": "1080p", "720x720": "720p", "480x480": "480p", "360x360": "360p",
                                  "240x240": "240p"}
        st.selectbox(label=tr("video size"), key="video_size", options=video_size_options,
                     format_func=lambda x: video_size_options[x])
    llm_columns = st.columns(2)
    with llm_columns[0]:
        st.slider(label=tr("video segment min length"), min_value=5, value=5, max_value=10, step=1,
                  key="video_segment_min_length")
    with llm_columns[1]:
        st.slider(label=tr("video segment max length"), min_value=10, value=10, max_value=30, step=1,
                  key="video_segment_max_length")
    # 开启本地目录
    # llm_columns = st.columns(2)
    # with llm_columns[0]:
    #     st.checkbox(label=tr("Enable local video dir"), key="enable_local_video_dir", value=False)
    # with llm_columns[1]:
    #     st.text_input(label=tr("local video dir"), key="local_video_dir")
    llm_columns = st.columns(4)
    with llm_columns[0]:
        st.checkbox(label=tr("Enable video Transition effect"), key="enable_video_transition_effect", value=True)
    with llm_columns[1]:
        st.selectbox(label=tr("video Transition effect"), key="video_transition_effect_type", options=transition_types)
    with llm_columns[2]:
        st.selectbox(label=tr("video Transition effect types"), key="video_transition_effect_value", options=fade_list)
    with llm_columns[3]:
        st.selectbox(label=tr("video Transition effect duration"), key="video_transition_effect_duration",
                     options=["1", "2"])

# 字幕
subtitle_container = st.container(border=True)
with subtitle_container:
    st.subheader(tr("Video Subtitles"))
    llm_columns = st.columns(4)
    with llm_columns[0]:
        st.checkbox(label=tr("Enable subtitles"), key="enable_subtitles", value=True)
    with llm_columns[1]:
        st.selectbox(label=tr("subtitle font"), key="subtitle_font",
                     options=["Songti SC Bold",
                              "Songti SC Black",
                              "Songti SC Light",
                              "STSong",
                              "Songti SC Regular",
                              "PingFang SC Regular",
                              "PingFang SC Medium",
                              "PingFang SC Semibold",
                              "PingFang SC Light",
                              "PingFang SC Thin",
                              "PingFang SC Ultralight"], )
    with llm_columns[2]:
        st.selectbox(label=tr("subtitle font size"), key="subtitle_font_size", index=1,
                     options=[4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
    with llm_columns[3]:
        st.selectbox(label=tr("subtitle lines"), key="captioning_lines", index=1,
                     options=[1, 2])

    llm_columns = st.columns(4)
    with llm_columns[0]:
        subtitle_position_options = {5: "top left",
                                     6: "top center",
                                     7: "top right",
                                     9: "center left",
                                     10: "center",
                                     11: "center right",
                                     1: "bottom left",
                                     2: "bottom center",
                                     3: "bottom right"}
        st.selectbox(label=tr("subtitle position"), key="subtitle_position", index=7,
                     options=subtitle_position_options, format_func=lambda x: subtitle_position_options[x])
    with llm_columns[1]:
        st.color_picker(label=tr("subtitle color"), key="subtitle_color", value="#FFFFFF")
    with llm_columns[2]:
        st.color_picker(label=tr("subtitle border color"), key="subtitle_border_color", value="#000000")
    with llm_columns[3]:
        st.slider(label=tr("subtitle border width"), min_value=0, value=0, max_value=4, step=1,
                  key="subtitle_border_width")

# 生成视频
video_generator = st.container(border=True)
with video_generator:
    st.button(label=tr("Generate Video Button"), type="primary", on_click=generate_video, args=(video_generator,))
result_video_file = st.session_state.get("result_video_file")
if result_video_file:
    st.video(result_video_file)