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
from typing import List

from config.config import my_config
from tools.utils import must_have_value
from faster_whisper import WhisperModel

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)
# module输出目录
module_output_dir = os.path.join(script_dir, "../../fasterwhisper")
module_output_dir = os.path.abspath(module_output_dir)


def convert_module_to_path(module_name):
    return_path = os.path.join(module_output_dir, module_name)
    print(return_path, os.path.isdir(return_path))
    return return_path


class FasterWhisperRecognitionResult:
    def __init__(self, text, begin_time, end_time):
        self.text = text
        self.begin_time = begin_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.text} {self.begin_time} {self.end_time}"


class FasterWhisperRecognitionService:
    def __init__(self):
        super().__init__()
        self.model_name = my_config['audio'].get('local_recognition', {}).get('fasterwhisper', {}).get('model_name')
        must_have_value(self.model_name, "请设置语音识别model_name")
        self.device_type = my_config['audio'].get('local_recognition', {}).get('fasterwhisper', {}).get('device_type')
        self.compute_type = my_config['audio'].get('local_recognition', {}).get('fasterwhisper', {}).get('compute_type')
        must_have_value(self.device_type, "请设置语音识别device_type")
        must_have_value(self.compute_type, "请设置语音识别compute_type")

    def process(self, audioFile, language) -> List[FasterWhisperRecognitionResult]:
        result_list = []

        # Run on GPU with FP16
        model = WhisperModel(convert_module_to_path(self.model_name), device=self.device_type, compute_type=self.compute_type,
                             local_files_only=True)

        # or run on GPU with INT8
        # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
        # or run on CPU with INT8
        # model = WhisperModel(model_size, device="cpu", compute_type="int8")

        segments, info = model.transcribe(audioFile, beam_size=5)

        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            result_list.append(
                FasterWhisperRecognitionResult(segment.text, segment.start,
                                               segment.end))

        return result_list
