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

import json
import os
import platform
from typing import Optional

from config.config import my_config
from services.alinls.speech_process import AliRecognitionService
from services.audio.faster_whisper_recognition_service import FasterWhisperRecognitionService
from services.audio.tencent_recognition_service import TencentRecognitionService
from services.captioning.common_captioning_service import Captioning
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
    recognition_type = st.session_state.get('recognition_audio_type')
    if recognition_type == "remote":
        selected_audio_provider = my_config['audio']['provider']
        if selected_audio_provider == 'Azure':
            print("selected_audio_provider: Azure")
            captioning.recognize_continuous(speech_recognizer=speech_recognizer_data["speech_recognizer"],
                                            format=speech_recognizer_data["audio_stream_format"],
                                            callback=speech_recognizer_data["pull_input_audio_stream_callback"],
                                            stream=speech_recognizer_data["pull_input_audio_stream"])
        if selected_audio_provider == 'Ali':
            print("selected_audio_provider: Ali")
            ali_service = AliRecognitionService()
            result_list = ali_service.process(get_session_option("audio_output_file"))
            captioning._offline_results = result_list
        if selected_audio_provider == 'Tencent':
            print("selected_audio_provider: Tencent")
            tencent_service = TencentRecognitionService()
            result_list = tencent_service.process(get_session_option("audio_output_file"),
                                                  get_session_option("audio_language"))
            if result_list is None:
                return
            captioning._offline_results = result_list
    if recognition_type == "local":
        selected_audio_provider = my_config['audio'].get('local_recognition',{}).get('provider','fasterwhisper')
        if selected_audio_provider =='fasterwhisper':
            print("selected_audio_provider: fasterwhisper")
            fasterwhisper_service = FasterWhisperRecognitionService()
            result_list = fasterwhisper_service.process(get_session_option("audio_output_file"),
                                                  get_session_option("audio_language"))
            print(result_list)
            if result_list is None:
                return
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
