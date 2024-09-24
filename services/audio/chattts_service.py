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

import datetime
import lzma
import os
import zipfile
from io import BytesIO

import numpy as np
import requests
import torch
from pydub import AudioSegment
from pydub.playback import play

from config.config import my_config
from tools.file_utils import read_file, convert_mp3_to_wav
from tools.utils import must_have_value, random_with_system_time
import streamlit as st
import pybase16384 as b14

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

# 音频输出目录
audio_output_dir = os.path.join(script_dir, "../../work")
audio_output_dir = os.path.abspath(audio_output_dir)


def encode_spk_emb(spk_emb: torch.Tensor) -> str:
    arr: np.ndarray = spk_emb.to(dtype=torch.float16, device="cpu").detach().numpy()
    s = b14.encode_to_string(
        lzma.compress(
            arr.tobytes(),
            format=lzma.FORMAT_RAW,
            filters=[{"id": lzma.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME}],
        ),
    )
    del arr
    return s

class ChatTTSAudioService:
    def __init__(self):
        super().__init__()
        self.service_location = my_config['audio']['local_tts']['chatTTS']['server_location']
        must_have_value(self.service_location, "请设置ChatTTS server location")
        self.service_location = self.service_location + '/generate_voice'
        if st.session_state.get('refine_text'):
            self.skip_refine_text = False
        else:
            self.skip_refine_text = True

        if st.session_state.get('refine_text_prompt'):
            self.refine_text_prompt = st.session_state.get('refine_text_prompt')
        else:
            self.refine_text_prompt = ""

        self.text_seed = st.session_state.get('text_seed')
        self.audio_temperature = st.session_state.get('audio_temperature')
        self.audio_top_p = st.session_state.get('audio_top_p')
        self.audio_top_k = st.session_state.get('audio_top_k')

        if st.session_state.get('use_random_voice'):
            self.audio_seed = st.session_state.get('audio_seed')
        else:
            self.audio_seed = None
            if os.path.exists(st.session_state.get('audio_voice')):
                if st.session_state.get('audio_voice').endswith('.pt'):
                    self.audio_content = encode_spk_emb(torch.load(st.session_state.get('audio_voice'), map_location=torch.device('cpu')))
                if st.session_state.get('audio_voice').endswith('.txt'):
                    self.audio_content = read_file(st.session_state.get('audio_voice'))

        audio_speed = st.session_state.get("audio_speed")
        if audio_speed == "normal":
            self.audio_speed = "[speed_5]"
        if audio_speed == "fast":
            self.audio_speed = "[speed_6]"
        if audio_speed == "slow":
            self.audio_speed = "[speed_4]"
        if audio_speed == "faster":
            self.audio_speed = "[speed_7]"
        if audio_speed == "slower":
            self.audio_speed = "[speed_3]"
        if audio_speed == "fastest":
            self.audio_speed = "[speed_8]"
        if audio_speed == "slowest":
            self.audio_speed = "[speed_2]"


        self.chats_url = f"{self.service_location}/generate_voice"

    def read_with_content(self, content):
        wav_file = os.path.join(audio_output_dir, str(random_with_system_time()) + ".wav")
        temp_file = self.chat_with_content(content, wav_file)
        # 读取音频文件
        audio = AudioSegment.from_file(temp_file)
        play(audio)

    def chat_with_content(self, content, audio_output_file):
        # main infer params
        body = {
            "text": [content],
            "stream": False,
            "lang": None,
            "skip_refine_text": self.skip_refine_text,
            "refine_text_only": False,
            "use_decoder": True,
            "audio_seed": int(self.audio_seed) if self.audio_seed else 0,
            "text_seed": int(self.text_seed),
            "do_text_normalization": True,
            "do_homophone_replacement": False,
        }

        # refine text params
        params_refine_text = {
            "prompt": self.refine_text_prompt,
            "top_P": float(self.audio_top_p),
            "top_K": int(self.audio_top_k),
            "temperature": float(self.audio_temperature),
            "repetition_penalty": 1,
            "max_new_token": 384,
            "min_new_token": 0,
            "show_tqdm": True,
            "ensure_non_empty": True,
            "stream_batch": 24,
        }
        body["params_refine_text"] = params_refine_text

        # infer code params
        params_infer_code = {
            "prompt": self.audio_speed,
            "top_P": float(self.audio_top_p),
            "top_K": int(self.audio_top_k),
            "temperature": float(self.audio_temperature),
            "repetition_penalty": 1.05,
            "max_new_token": 2048,
            "min_new_token": 0,
            "show_tqdm": True,
            "ensure_non_empty": True,
            "stream_batch": True,
            "spk_emb": self.audio_content if not self.audio_seed else None,
        }
        body["params_infer_code"] = params_infer_code

        print(body)

        try:
            response = requests.post(self.service_location, json=body)
            response.raise_for_status()
            with zipfile.ZipFile(BytesIO(response.content), "r") as zip_ref:
                zip_ref.extractall(audio_output_dir)
                file_names = zip_ref.namelist()
                output_file = os.path.join(audio_output_dir, file_names[0])

                convert_mp3_to_wav(output_file, audio_output_file)
                print("Extracted files into", audio_output_file)
                return audio_output_file

        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
