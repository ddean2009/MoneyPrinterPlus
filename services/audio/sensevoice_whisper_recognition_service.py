
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
import subprocess
import numpy as np
from typing import List
import sherpa_onnx

from config.config import my_config
from tools.utils import must_have_value

class SenseVoiceRecognitionResult:
    def __init__(self, text, begin_time, end_time):
        self.text = text
        self.begin_time = begin_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.text} {self.begin_time} {self.end_time}"


class SenseVoiceRecognitionService:
    def __init__(self):
        super().__init__()
        self.model_path = "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/model.onnx"
        self.tokens_path = "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/tokens.txt"
        must_have_value(self.model_path, "请设置 SenseVoice 模型路径")
        must_have_value(self.tokens_path, "请设置 SenseVoice tokens 路径")

    def process(self, audioFile, language) -> List[SenseVoiceRecognitionResult]:
        result_list = []

        # 创建 SenseVoice 识别器
        recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
            model=self.model_path,
            tokens=self.tokens_path,
            num_threads=2,  # 可以根据需要调整线程数
            use_itn=True,
            debug=False,
        )

        # 使用 ffmpeg 将音频文件转换为 16kHz 16bit 单声道 PCM 格式
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", audioFile,
            "-f", "s16le",
            "-acodec", "pcm_s16le",
            "-ac", "1",
            "-ar", "16000",
            "-",
        ]

        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        data = process.stdout.read()

        # 将音频数据转换为 float32 格式
        samples = np.frombuffer(data, dtype=np.int16)
        samples = samples.astype(np.float32) / 32768

        # 创建识别流并处理音频数据
        stream = recognizer.create_stream()
        stream.accept_waveform(16000, samples)
        recognizer.decode_stream(stream)

        # 获取识别结果
        result = stream.result.text

        # 假设整个音频的起止时间为 0 到音频长度
        result_list.append(SenseVoiceRecognitionResult(result, 0, len(samples) / 16000))

        return result_list