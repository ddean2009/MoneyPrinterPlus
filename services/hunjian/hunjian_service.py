import os
import subprocess

import streamlit as st

from tools.file_utils import random_line_from_text_file
from tools.utils import get_must_session_option, random_with_system_time, extent_audio, run_ffmpeg_command

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)
# 音频输出目录
audio_output_dir = os.path.join(script_dir, "../../work")
audio_output_dir = os.path.abspath(audio_output_dir)


def get_session_video_scene_text():
    video_dir_list = []
    video_text_list = []
    if 'scene_number' not in st.session_state:
        st.session_state['scene_number'] = 0
    for i in range(int(st.session_state.get('scene_number'))+1):
        print("select video scene " + str(i + 1))
        if "video_scene_folder_" + str(i + 1) in st.session_state and st.session_state["video_scene_folder_" + str(i + 1)] is not None:
            video_dir_list.append(st.session_state["video_scene_folder_" + str(i + 1)])
            video_text_list.append(st.session_state["video_scene_text_" + str(i + 1)])
    return video_dir_list, video_text_list


def get_video_scene_text_list(video_text_list):
    video_scene_text_list = []
    for video_text in video_text_list:
        if video_text is not None and video_text != "":
            video_line = random_line_from_text_file(video_text)
            video_scene_text_list.append(video_line)
        else:
            video_scene_text_list.append("")
    return video_scene_text_list


def get_video_text_from_list(video_scene_text_list):
    return " ".join(video_scene_text_list)


def get_audio_and_video_list(audio_service, audio_rate):
    audio_output_file_list = []
    video_dir_list, video_text_list = get_session_video_scene_text()
    video_scene_text_list = get_video_scene_text_list(video_text_list)
    audio_voice = get_must_session_option("audio_voice", "请先设置配音语音")
    i = 0
    for video_scene_text in video_scene_text_list:
        if video_scene_text is not None and video_scene_text != "":
            temp_file_name = str(random_with_system_time()) + str(i)
            i = i + 1
            audio_output_file = os.path.join(audio_output_dir, str(temp_file_name) + ".wav")
            audio_service.save_with_ssml(video_scene_text,
                                         audio_output_file,
                                         audio_voice,
                                         audio_rate)
            extent_audio(audio_output_file, 1)
            audio_output_file_list.append(audio_output_file)
        else:
            st.toast("配音文字不能为空", icon="⚠️")
            st.stop()

    return audio_output_file_list, video_dir_list


def get_audio_and_video_list_local(audio_service):
    audio_output_file_list = []
    video_dir_list, video_text_list = get_session_video_scene_text()
    video_scene_text_list = get_video_scene_text_list(video_text_list)
    i = 0
    for video_scene_text in video_scene_text_list:
        temp_file_name = str(random_with_system_time()) + str(i)
        i = i + 1
        audio_output_file = os.path.join(audio_output_dir, str(temp_file_name) + ".wav")
        audio_service.chat_with_content(video_scene_text, audio_output_file)
        extent_audio(audio_output_file, 1)
        audio_output_file_list.append(audio_output_file)
    return audio_output_file_list, video_dir_list


def get_video_text():
    video_dir_list, video_text_list = get_session_video_scene_text()
    video_scene_text_list = get_video_scene_text_list(video_text_list)
    return get_video_text_from_list(video_scene_text_list)


def concat_audio_list(audio_output_file_list):
    temp_output_file_name = os.path.join(audio_output_dir, str(random_with_system_time()) + ".wav")
    concat_audio_file = os.path.join(audio_output_dir, "concat_audio_file.txt")
    with open(concat_audio_file, 'w', encoding='utf-8') as f:
        for audio_file in audio_output_file_list:
            f.write("file '{}'\n".format(os.path.abspath(audio_file)))
    # 调用ffmpeg来合并音频
    # 注意：这里假设ffmpeg在你的PATH中，否则你需要提供ffmpeg的完整路径
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_audio_file,
        '-c', 'copy',  # 如果可能，直接复制流而不是重新编码
        temp_output_file_name
    ]
    run_ffmpeg_command(command)
    # 完成后，删除临时文件（如果你不再需要它）
    os.remove(concat_audio_file)
    print(f"Audio files have been merged into {temp_output_file_name}")
    return temp_output_file_name
