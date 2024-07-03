import os

import streamlit as st

from config.config import transition_types, fade_list, languages, audio_languages
from main import main_generate_ai_video_for_mix, main_try_test_audio, get_audio_voices
from pages.common import common_ui
from tools.tr_utils import tr
from tools.utils import get_file_map_from_dir

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

default_bg_music_dir = os.path.join(script_dir, "../bgmusic")
default_bg_music_dir = os.path.abspath(default_bg_music_dir)


def try_test_audio():
    main_try_test_audio()


def delete_scene_for_mix(video_scene_container):
    if 'scene_number' not in st.session_state or st.session_state['scene_number'] < 1:
        return
    st.session_state['scene_number'] = st.session_state['scene_number'] - 1
    # with video_scene_container:
    #     for k in range(st.session_state['scene_number']):
    #         st.subheader(tr("Mix Video Scene") + str(k + 2))
    #         st.text_input(label=tr("Video Scene Resource"),
    #                       placeholder=tr("Please input video scene resource folder path"),
    #                       key="video_scene_folder_" + str(k + 2))
    #         st.text_input(label=tr("Video Scene Text"), placeholder=tr("Please input video scene text path"),
    #                       key="video_scene_text_" + str(k + 2))


def add_more_scene_for_mix(video_scene_container):
    if 'scene_number' in st.session_state:
        # 最多5个场景
        if st.session_state['scene_number'] < 4:
            st.session_state['scene_number'] = st.session_state['scene_number'] + 1
        else:
            st.toast(tr("Maximum number of scenes reached"), icon="⚠️")
    else:
        st.session_state['scene_number'] = 1
    # add_more_scene_fragment(video_scene_container)
    # with video_scene_container:
    #     for k in range(st.session_state['scene_number']):
    #         st.subheader(tr("Mix Video Scene") + str(k + 2))
    #         st.text_input(label=tr("Video Scene Resource"),
    #                       placeholder=tr("Please input video scene resource folder path"),
    #                       key="video_scene_folder_" + str(k + 2))
    #         st.text_input(label=tr("Video Scene Text"), placeholder=tr("Please input video scene text path"),
    #                       key="video_scene_text_" + str(k + 2))

def more_scene_fragment(video_scene_container):
    with video_scene_container:
        if 'scene_number' in st.session_state:
            for k in range(st.session_state['scene_number']):
                st.subheader(tr("Mix Video Scene") + str(k + 2))
                st.text_input(label=tr("Video Scene Resource"),
                              placeholder=tr("Please input video scene resource folder path"),
                              key="video_scene_folder_" + str(k + 2))
                st.text_input(label=tr("Video Scene Text"), placeholder=tr("Please input video scene text path"),
                              key="video_scene_text_" + str(k + 2))

def generate_video_for_mix(video_generator):
    videos_count = st.session_state.get('videos_count')
    if videos_count is not None:
        for i in range(int(videos_count)):
            print(i)
            main_generate_ai_video_for_mix(video_generator)


common_ui()

st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            AI搞钱工具</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>视频批量混剪工具</h2>", unsafe_allow_html=True)

# 场景设置
mix_video_container = st.container(border=True)
with mix_video_container:
    st.subheader(tr("Mix Video"))
    video_scene_container = st.container(border=True)
    with video_scene_container:
        st.subheader(tr("Mix Video Scene") + str(1))
        st.text_input(label=tr("Video Scene Resource"), placeholder=tr("Please input video scene resource folder path"),
                      key="video_scene_folder_" + str(1))
        st.text_input(label=tr("Video Scene Text"), placeholder=tr("Please input video scene text path"),
                      help=tr("One Line Text For One Scene,UTF-8 encoding"),
                      key="video_scene_text_" + str(1))
    more_scene_fragment(video_scene_container)
    st_columns = st.columns(2)
    with st_columns[0]:
        st.button(label=tr("Add More Scene"), type="primary", on_click=add_more_scene_for_mix,
                  args=(video_scene_container,))
    with st_columns[1]:
        st.button(label=tr("Delete Extra Scene"), type="primary", on_click=delete_scene_for_mix,
                  args=(video_scene_container,))

# 配音区域
captioning_container = st.container(border=True)
with captioning_container:
    # 配音
    st.subheader(tr("Video Captioning"))
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
        st.slider(label=tr("video segment min length"), min_value=5.0, value=5.0, max_value=10.0, step=1.0,
                  key="video_segment_min_length")
    with llm_columns[1]:
        st.slider(label=tr("video segment max length"), min_value=5.0, value=10.0, max_value=30.0, step=1.0,
                  key="video_segment_max_length")
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
        st.slider(label=tr("subtitle border width"), min_value=0.0, value=0.0, max_value=4.0, step=1.0,
                  key="subtitle_border_width")

# 生成视频
video_generator = st.container(border=True)
with video_generator:
    st.slider(label=tr("how many videos do you want"), min_value=1.0, value=1.0, max_value=100.0, step=1.0,
              key="videos_count")
    st.button(label=tr("Generate Video Button"), type="primary", on_click=generate_video_for_mix,
              args=(video_generator,))
result_video_file = st.session_state.get("result_video_file")
if result_video_file:
    st.video(result_video_file)
