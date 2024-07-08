import os
import random
import subprocess
import time
import streamlit as st
from typing import Optional

from tools.file_utils import generate_temp_filename


def generate_operator():
    operators = ['+', '-']
    return random.choice(operators)

def random_with_system_time():
    system_time = int(time.time() * 1000)
    random_seed = (system_time + random.randint(0, 10000))
    return random_seed


def get_images_with_prefix(img_dir, img_file_prefix):
    # 确保提供的是绝对路径
    img_dir = os.path.abspath(img_dir)

    # 持有所有匹配前缀的图片文件的列表
    images_with_prefix = []

    # 遍历img_dir中的文件
    for filename in os.listdir(img_dir):
        # print('filename:', filename)
        # print('img_file_prefix:',img_file_prefix)
        # print(filename.startswith(img_file_prefix))
        # 检查文件名是否以img_file_prefix开头 并且后缀是.jpg
        if filename.startswith(img_file_prefix) and (filename.endswith('.png') or filename.endswith('.jpg')):
            # 构建完整的文件路径
            file_path = os.path.join(img_dir, filename)
            # 确保这是一个文件而不是目录
            if os.path.isfile(file_path):
                images_with_prefix.append(file_path)

    return images_with_prefix


def get_file_from_dir(file_dir, extension):
    extension_list = [ext.strip() for ext in extension.split(',')]
    # 确保提供的是绝对路径
    file_dir = os.path.abspath(file_dir)

    # 所有文件的列表
    file_list = []

    # 遍历file_dir中的文件
    for filename in os.listdir(file_dir):
        # print('filename:', filename)
        file_extension = os.path.splitext(filename)[1]
        # 检查文件名是否以img_file_prefix开头 并且后缀是.txt
        if file_extension in extension_list:
            # 构建完整的文件路径
            file_path = os.path.join(file_dir, filename)
            # 确保这是一个文件而不是目录
            if os.path.isfile(file_path):
                file_list.append(file_path)

    return file_list


def get_file_map_from_dir(file_dir, extension):
    extension_list = [ext.strip() for ext in extension.split(',')]
    # 确保提供的是绝对路径
    file_dir = os.path.abspath(file_dir)
    # 所有文件的列表
    file_map = {}

    # 遍历file_dir中的文件
    for filename in os.listdir(file_dir):
        # print('filename:', filename)
        file_extension = os.path.splitext(filename)[1]
        # 检查文件名是否以img_file_prefix开头 并且后缀是.txt
        if file_extension in extension_list:
            # 构建完整的文件路径
            file_path = os.path.join(file_dir, filename)
            # 确保这是一个文件而不是目录
            if os.path.isfile(file_path):
                file_map[file_path] = os.path.split(file_path)[1]

    return file_map


def get_text_from_dir(text_dir):
    return get_file_from_dir(text_dir, ".txt")


def get_mp4_from_dir(video_dir):
    return get_file_from_dir(video_dir, ".mp4")


def get_session_option(option: str) -> Optional[str]:
    return st.session_state.get(option)


def get_must_session_option(option: str, msg: str) -> Optional[str]:
    result = st.session_state.get(option)
    if not result:
        st.toast(msg, icon="⚠️")
        st.stop()
    return result


def must_have_value(option: str, msg: str) -> Optional[str]:
    if not option:
        st.toast(msg, icon="⚠️")
        st.stop()
    return option


def run_ffmpeg_command(command):
    try:
        result = subprocess.run(command, capture_output=True, check=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg returned an error: {result.stderr}")
        else:
            print("Command executed successfully.")
    except Exception as e:
        print(f"An error occurred while execute ffmpeg command {e}")


def extent_audio(audio_file, pad_dur=2):
    temp_file = generate_temp_filename(audio_file)
    # 构造ffmpeg命令
    command = [
        'ffmpeg',
        '-i', audio_file,
        '-af', f'apad=pad_dur={pad_dur}',
        temp_file
    ]
    # 执行命令
    subprocess.run(command, capture_output=True, check=True)
    # 重命名最终的文件
    if os.path.exists(temp_file):
        os.remove(audio_file)
        os.renames(temp_file, audio_file)

