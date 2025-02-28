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

import os

import requests
from pydub import AudioSegment
from pydub.playback import play

from config.config import my_config
from tools.utils import must_have_value, random_with_system_time
import streamlit as st

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)


# 脚本所在的目录
script_dir = os.path.dirname(script_path)

# 音频输出目录
audio_output_dir = os.path.join(script_dir, "../../work")
audio_output_dir = os.path.abspath(audio_output_dir)


class CosyVoiceAudioService:

    SPEED_MAP = {
        "normal": 1.0,
        "fast": 1.1,
        "slow": 0.9,
        "faster": 1.2,
        "slower": 0.8,
        "fastest": 1.3,
        "slowest": 0.7
    }
        
    def __init__(self):
        super().__init__()
        self.service_location = my_config['audio']['local_tts']['CosyVoice']['server_location']
        must_have_value(self.service_location, "请设置CosyVoice server location")
        self.service_location = self.service_location.rstrip('/')

        self.audio_seed = int(st.session_state.get('audio_seed', 0))
        self.audio_speed = self.get_audio_speed(st.session_state.get("audio_speed"))
        self.refer_wav_path = st.session_state.get("reference_audio_file_path")
        self.reference_audio_language = st.session_state.get("reference_audio_language")


    def get_audio_speed(self, speed_key):
        return self.SPEED_MAP.get(speed_key, 1.0)
    
    def get_remote_audio_templates(self):
        '''获取远程cosyvoice音频文件列表'''
        try:
            response = requests.get(f'{self.service_location}/audio_templates')
            response.raise_for_status()
            response_data = response.json()
            if response_data.get('status') == "success":
                return response_data.get('data', {}).get('audio_files', [])
            else:
                print("Error in response status:", response_data.get('message', 'Unknown error'))
        except requests.RequestException as e:
            print(f"Error fetching audio templates: {e}")
        return []

    def read_with_content(self, content):
        wav_file = os.path.join(audio_output_dir, f"{random_with_system_time()}.wav")
        temp_file = self.chat_with_content(content, wav_file)
        audio = AudioSegment.from_file(temp_file)
        play(audio)

    def chat_with_content(self, content, audio_output_file):
        body = {
            "mode": "zero_shot" if self.refer_wav_path else "sft",
            "tts_text": content,
            "seed": self.audio_seed,
            "speed": self.audio_speed,
            "prompt_voice": 'audio_templates/' + self.refer_wav_path,
            "sft_dropdown": self.reference_audio_language if not self.refer_wav_path else None,
            "prompt_text": st.session_state.get("reference_audio_text") if self.refer_wav_path else None
        }

        try:
            response = requests.post(f'{self.service_location}/text-tts', json=body)
            response.raise_for_status()
            with open(audio_output_file, 'wb') as file:
                file.write(response.content)
            print(f"文件已保存到 {audio_output_file}")
            return audio_output_file
        except requests.RequestException as e:
            print(f"Request Error: {e}")
        return None