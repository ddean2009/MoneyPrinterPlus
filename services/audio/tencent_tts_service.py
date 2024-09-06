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

import base64
import json
import os
import time
import types

from pydub import AudioSegment
from pydub.playback import play
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tts.v20190823 import tts_client, models

from config.config import my_config
from services.audio.audio_service import AudioService
from tools.file_utils import download_file_from_url
from tools.utils import must_have_value, random_with_system_time

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)
# 音频输出目录
audio_output_dir = os.path.join(script_dir, "../../work")
audio_output_dir = os.path.abspath(audio_output_dir)


class TencentAudioService(AudioService):
    def __init__(self):
        super().__init__()
        self.TENCENT_ACCESS_AKID = my_config['audio'].get('Tencent', {}).get('access_key_id')
        self.TENCENT_ACCESS_AKKEY = my_config['audio'].get('Tencent', {}).get('access_key_secret')
        must_have_value(self.TENCENT_ACCESS_AKID, "请设置Tencent access key id")
        must_have_value(self.TENCENT_ACCESS_AKKEY, "请设置Tencent access key secret")
        self.endpoint = "tts.tencentcloudapi.com"

    def save_with_ssml(self, text, file_name, voice, rate="0.00"):
        cred = credential.Credential(self.TENCENT_ACCESS_AKID, self.TENCENT_ACCESS_AKKEY)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = self.endpoint

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = tts_client.TtsClient(cred, "ap-beijing", clientProfile)

        # 返回的resp是一个TextToVoiceResponse的实例，与请求对象对应
        if len(text) < 150:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.TextToVoiceRequest()
            params = {
                "Text": text,
                "SessionId": str(random_with_system_time()),
                "Codec": "wav",
                "VoiceType": int(voice),
                "Speed": float(rate)

            }
            req.from_json_string(json.dumps(params))
            resp = client.TextToVoice(req)
            # 输出json格式的字符串回包
            # print(resp.to_json_string())
            # 使用base64库解码字符串
            decoded_audio_data = base64.b64decode(resp.Audio)
            # 写入WAV文件
            print("腾讯语音合成任务成功")
            with open(file_name, 'wb') as wav_file:
                wav_file.write(decoded_audio_data)
        else:
            # 使用腾讯长文本语音合成
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.CreateTtsTaskRequest()
            params = {
                "Text": text,
                "SessionId": str(random_with_system_time()),
                "Codec": "wav",
                "VoiceType": int(voice),
                "Speed": float(rate)
            }
            req.from_json_string(json.dumps(params))
            # 返回的resp是一个CreateTtsTaskResponse的实例，与请求对象对应
            resp = client.CreateTtsTask(req)
            # 输出json格式的字符串回包
            print(resp.to_json_string())
            long_tts_request_id = resp.RequestId
            long_tts_request_task = resp.Data.TaskId
            time.sleep(2)
            # 查询结果
            while True:
                # 实例化一个请求对象,每个接口都会对应一个request对象
                req = models.DescribeTtsTaskStatusRequest()
                params = {
                    "TaskId": long_tts_request_task
                }
                req.from_json_string(json.dumps(params))
                # 返回的resp是一个DescribeTtsTaskStatusResponse的实例，与请求对象对应
                resp = client.DescribeTtsTaskStatus(req)
                # 输出json格式的字符串回包
                # print(resp.to_json_string())
                # Status: 任务状态码，0：任务等待，1：任务执行中，2：任务成功，3：任务失败。
                if resp.Data.Status == 0:
                    print("腾讯语音合成任务等待中...")
                    time.sleep(2)
                    continue
                elif resp.Data.Status == 1:
                    print("腾讯语音合成任务执行中...")
                    time.sleep(2)
                    continue
                elif resp.Data.Status == 2:
                    print("腾讯语音合成任务成功")
                    result_url = resp.Data.ResultUrl
                    if result_url:
                        download_file_from_url(result_url, file_name)
                    break
                elif resp.Data.Status == 3:
                    print("腾讯语音合成任务失败")
                    break

    def read_with_ssml(self, text, voice, rate="0.00"):
        temp_file = os.path.join(audio_output_dir, "temp.wav")
        self.save_with_ssml(text, temp_file, voice, rate)
        # 读取音频文件
        audio = AudioSegment.from_file(temp_file)
        # 剪辑音频（例如，剪辑前5秒）
        # audio_snippet = audio[:5000]
        # 播放剪辑后的音频
        play(audio)


if __name__ == '__main__':
    service = TencentAudioService()
    service.save_with_ssml("你好", "/tmp/temp.wav", 1001)
