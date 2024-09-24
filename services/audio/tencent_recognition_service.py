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
from typing import List

from tencentcloud.common import credential

from config.config import my_config
from services.audio import flash_recognizer
from tools.utils import must_have_value
import streamlit as st


class TencentRecognitionResult:
    def __init__(self, text, begin_time, end_time):
        self.text = text
        self.begin_time = begin_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.text} {self.begin_time} {self.end_time}"


class TencentRecognitionService:
    def __init__(self):
        super().__init__()
        self.TENCENT_ACCESS_AKID = my_config['audio'].get('Tencent', {}).get('access_key_id')
        self.TENCENT_ACCESS_AKKEY = my_config['audio'].get('Tencent', {}).get('access_key_secret')
        self.TENCENT_APP_ID = my_config['audio'].get('Tencent', {}).get('app_key')
        must_have_value(self.TENCENT_ACCESS_AKID, "请设置Tencent access key id")
        must_have_value(self.TENCENT_ACCESS_AKKEY, "请设置Tencent access key secret")
        must_have_value(self.TENCENT_APP_ID, "请设置Tencent app ID")
        self.endpoint = "tts.tencentcloudapi.com"

    def process(self, audioFile, language) -> List[TencentRecognitionResult]:
        result_list = []
        credential_var = credential.Credential(self.TENCENT_ACCESS_AKID, self.TENCENT_ACCESS_AKKEY)
        # 新建FlashRecognizer，一个recognizer可以执行N次识别请求
        recognizer = flash_recognizer.FlashRecognizer(self.TENCENT_APP_ID, credential_var)
        ENGINE_TYPE = "16k_zh"
        if language == 'zh-CN':
            ENGINE_TYPE = "16k_zh"
        elif language == 'en-US':
            ENGINE_TYPE = "16k_en"
        # 新建识别请求
        req = flash_recognizer.FlashRecognitionRequest(ENGINE_TYPE)
        req.set_filter_modal(0)
        req.set_filter_punc(0)
        req.set_filter_dirty(0)
        req.set_voice_format("wav")
        req.set_word_info(0)
        req.set_convert_num_mode(1)

        # 音频路径
        with open(audioFile, 'rb') as f:
            # 读取音频数据
            data = f.read()
            # 执行识别
            resultData = recognizer.recognize(req, data)
            resp = json.loads(resultData)
            request_id = resp["request_id"]
            code = resp["code"]
            if code != 0:
                print("recognize failed! request_id: ", request_id, " code: ", code, ", message: ", resp["message"])
                st.toast("腾讯云语音识别失败", icon="⚠️")
                return None

            print("request_id: ", request_id)
            # 一个channl_result对应一个声道的识别结果
            # 大多数音频是单声道，对应一个channl_result
            for channl_result in resp["flash_result"]:
                # print("channel_id: ", channl_result["channel_id"])
                # print(channl_result)
                for sentence in channl_result['sentence_list']:
                    print(sentence)
                    result_list.append(
                        TencentRecognitionResult(sentence['text'], sentence['start_time'],
                                                 sentence['end_time']))
            return result_list
