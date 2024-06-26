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
