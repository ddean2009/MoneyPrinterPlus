import streamlit as st

from config.config import my_config, save_config, languages, audio_languages, audio_voices, transition_types, \
    fade_list
from main import main_generate_video_content, main_generate_ai_video, main_generate_video_dubbing, \
    main_get_video_resource, main_generate_subtitle
from pages.common import common_ui
from tools.tr_utils import tr

# import tkinter as tk
# from tkinter import filedialog

# import wx
import os

from tools.utils import get_file_from_dir, get_file_map_from_dir

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

default_bg_music_dir = os.path.join(script_dir, "../bgmusic")
default_bg_music_dir = os.path.abspath(default_bg_music_dir)


# def select_folder():
#    root = tk.Tk()
#    root.withdraw()
#    folder_path = filedialog.askdirectory(master=root)
#    root.destroy()
#    return folder_path

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


def generate_video(video_generator):
    main_generate_ai_video(video_generator)


test_mode = my_config["test_mode"]

st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            AI搞钱工具</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>自动短视频生成器</h2>", unsafe_allow_html=True)

# LLM区域
llm_container = st.container(border=True)
with llm_container:
    st.subheader(tr("LLM Video Subject generator"))
    st.info(tr("Please input video subject, then click the generate button to generate the video content"))
    st.text_input(label=tr("Video Subject"), placeholder=tr("Please input video subject"), key="video_subject")
    llm_columns = st.columns(3)
    video_length_options = {"60": "60字以内", "120": "120字以内", "300": "300字以内", "600": "600字以内"}
    with llm_columns[0]:
        st.selectbox(label=tr("Video content language"), options=languages, format_func=lambda x: languages.get(x),
                     key="video_language")
    with llm_columns[1]:
        st.selectbox(label=tr("Video length"), options=video_length_options,
                     format_func=lambda x: video_length_options.get(x), key="video_length")
        # print(st.session_state.get("video_length"))
    with llm_columns[2]:
        st.button(label=tr("Generate Video Content"),type="primary", on_click=generate_video_content)
    # print(st.session_state.get("video_content"))
    st.text_area(label=tr("Video content"), key="video_content", height=200)
    st.text_input(label=tr("Video content keyword"), key="video_keyword")

# 配音区域
captioning_container = st.container(border=True)
with captioning_container:
    # 配音
    st.subheader(tr("Video Captioning"))
    llm_columns = st.columns(3)
    with llm_columns[0]:
        st.selectbox(label=tr("Audio language"), options=audio_languages,
                     format_func=lambda x: audio_languages.get(x), key="audio_language")
    with llm_columns[1]:
        # with st.container(st.session_state.get("captioning_language")):
        st.selectbox(label=tr("Audio voice"),
                     options=audio_voices.get(st.session_state.get("audio_language")),
                     format_func=lambda x: audio_voices.get(st.session_state.get("audio_language")).get(x),
                     key="audio_voice")
        # print(st.session_state.get("captioning_voice"))
    with llm_columns[2]:
        st.selectbox(label=tr("Audio speed"),
                     options=["normal", "fast", "faster", "fastest", "slow", "slower", "slowest"],
                     key="audio_speed")
    if test_mode:
        st.button(label=tr("Generate Video dubbing"), on_click=generate_video_dubbing)

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

        # selected_folder_path = st.session_state.get("folder_path", None)
        # folder_select_button = st.button("Select Folder")
        # if folder_select_button:
        #     selected_folder_path = select_folder()
        #     st.session_state.folder_path = selected_folder_path

        # if st.button("Browse"):
        #     app = wx.App()
        #     dialog = wx.DirDialog(None, "Select a folder:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        #     if dialog.ShowModal() == wx.ID_OK:
        #         folder_path = dialog.GetPath()  # folder_path will contain the path of the folder you have selected as string
        #     app.MainLoop()
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
        st.slider(label=tr("video segment max length"), min_value=10.0, value=10.0, max_value=30.0, step=1.0,
                  key="video_segment_max_length")
    # 开启本地目录
    llm_columns = st.columns(2)
    with llm_columns[0]:
        st.checkbox(label=tr("Enable local video dir"), key="enable_local_video_dir", value=False)
    with llm_columns[1]:
        st.text_input(label=tr("local video dir"), key="local_video_dir")
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
    if test_mode:
        st.button(label=tr("Get Video Resource"), on_click=get_video_resource)

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
                              "Songti SC Regular"], )
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
        st.color_picker(label=tr("subtitle color"), key="subtitle_color",value="#FFFFFF" )
    with llm_columns[2]:
        st.color_picker(label=tr("subtitle border color"), key="subtitle_border_color", value="#000000")
    with llm_columns[3]:
        st.slider(label=tr("subtitle border width"), min_value=0.0, value=0.0, max_value=4.0, step=1.0,
                  key="subtitle_border_width")
    if test_mode:
        st.button(label=tr("Generate subtitle"), on_click=generate_subtitle)

# 生成视频
video_generator = st.container(border=True)
with video_generator:
    # st_status = st.status(tr("Generate Video in process..."), expanded=True)
    st.button(label=tr("Generate Video Button"), type="primary", on_click=generate_video, args=(video_generator, ))
result_video_file = st.session_state.get("result_video_file")
if result_video_file:
    st.video(result_video_file)
