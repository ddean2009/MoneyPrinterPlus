import os
import platform
from typing import Optional

from config.config import my_config
from services.alinls.speech_process import AliRecognitionService
from services.captioning.azure_captioning_service import run_captioning, Captioning
import subprocess

from tools.file_utils import generate_temp_filename
import streamlit as st

from tools.utils import get_session_option

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

font_dir = os.path.join(script_dir, '../../fonts')
font_dir = os.path.abspath(font_dir)

# windows路径需要特殊处理
if platform.system() == "Windows":
    font_dir = font_dir.replace("\\", "\\\\\\\\")
    font_dir = font_dir.replace(":", "\\\\:")


# 生成字幕
def generate_caption():
    captioning = Captioning()
    captioning.initialize()
    speech_recognizer_data = captioning.speech_recognizer_from_user_config()
    # print(speech_recognizer_data)
    selected_audio_provider = my_config['audio']['provider']
    if selected_audio_provider == 'Azure':
        captioning.recognize_continuous(speech_recognizer=speech_recognizer_data["speech_recognizer"],
                                        format=speech_recognizer_data["audio_stream_format"],
                                        callback=speech_recognizer_data["pull_input_audio_stream_callback"],
                                        stream=speech_recognizer_data["pull_input_audio_stream"])
    if selected_audio_provider == 'Ali':
        ali_service = AliRecognitionService()
        result_list = ali_service.process(get_session_option("audio_output_file"))
        # print("result_list:", result_list)
        captioning._offline_results = result_list
    captioning.finish()


# 添加字幕
def add_subtitles(video_file, subtitle_file, font_name='Songti TC Bold', font_size=12, primary_colour='#FFFFFF',
                  outline_colour='#FFFFFF', margin_v=16, margin_l=4, margin_r=4, border_style=1, outline=0, alignment=2,
                  shadow=0, spacing=2):
    output_file = generate_temp_filename(video_file)
    primary_colour = f"&H{primary_colour[1:]}&"
    outline_colour = f"&H{outline_colour[1:]}&"
    # windows路径需要特殊处理
    if platform.system() == "Windows":
        subtitle_file = subtitle_file.replace("\\", "\\\\\\\\")
        subtitle_file = subtitle_file.replace(":", "\\\\:")
    vf_text = f"subtitles={subtitle_file}:fontsdir={font_dir}:force_style='Fontname={font_name},Fontsize={font_size},Alignment={alignment},MarginV={margin_v},MarginL={margin_l},MarginR={margin_r},BorderStyle={border_style},Outline={outline},Shadow={shadow},PrimaryColour={primary_colour},OutlineColour={outline_colour},Spacing={spacing}'"
    # 构建FFmpeg命令
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_file,  # 输入视频文件
        '-vf', vf_text,  # 输入字幕文件
        '-y',
        output_file  # 输出文件
    ]
    print(" ".join(ffmpeg_cmd))
    # 调用ffmpeg
    subprocess.run(ffmpeg_cmd, check=True)
    # 重命名最终的文件
    if os.path.exists(output_file):
        os.remove(video_file)
        os.renames(output_file, video_file)
