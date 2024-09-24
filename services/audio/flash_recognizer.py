# -*- coding: utf-8 -*-

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

import requests
import hmac
import hashlib
import base64
import time
import random
import os
import json

#录音识别极速版使用
class FlashRecognitionRequest:
    def __init__(self, engine_type):
        self.engine_type = engine_type
        self.speaker_diarization = 0
        self.hotword_id = ""
        self.customization_id = ""
        self.filter_dirty = 0
        self.filter_modal = 0
        self.filter_punc = 0
        self.convert_num_mode = 1
        self.word_info = 0
        self.voice_format = ""
        self.first_channel_only = 1
        self.reinforce_hotword = 0
        self.sentence_max_length = 0

    def set_first_channel_only(self, first_channel_only):
        self.first_channel_only = first_channel_only

    def set_speaker_diarization(self, speaker_diarization):
        self.speaker_diarization = speaker_diarization

    def set_filter_dirty(self, filter_dirty):
        self.filter_dirty = filter_dirty

    def set_filter_modal(self, filter_modal):
        self.filter_modal = filter_modal

    def set_filter_punc(self, filter_punc):
        self.filter_punc = filter_punc

    def set_convert_num_mode(self, convert_num_mode):
        self.convert_num_mode = convert_num_mode

    def set_word_info(self, word_info):
        self.word_info = word_info

    def set_hotword_id(self, hotword_id):
        self.hotword_id = hotword_id

    def set_customization_id(self, customization_id):
        self.customization_id = customization_id

    def set_voice_format(self, voice_format):
        self.voice_format = voice_format

    def set_sentence_max_length(self, sentence_max_length):
        self.sentence_max_length = sentence_max_length

    def set_reinforce_hotword(self, reinforce_hotword):
        self.reinforce_hotword = reinforce_hotword



class FlashRecognizer:
    '''
    reponse:
    字段名            类型
    request_id        string
    status            Integer
    message           String
    audio_duration    Integer
    flash_result      Result Array

    Result的结构体格式为:
    text              String
    channel_id        Integer
    sentence_list     Sentence Array

    Sentence的结构体格式为:
    text              String
    start_time        Integer
    end_time          Integer
    speaker_id        Integer
    word_list         Word Array

    Word的类型为:
    word              String
    start_time        Integer
    end_time          Integer
    stable_flag：     Integer
    '''

    def __init__(self, appid, credential):
        self.credential = credential
        self.appid = appid

    def _format_sign_string(self, param):
        signstr = "POSTasr.cloud.tencent.com/asr/flash/v1/"
        for t in param:
            if 'appid' in t:
                signstr += str(t[1])
                break
        signstr += "?"
        for x in param:
            tmp = x
            if 'appid' in x:
                continue
            for t in tmp:
                signstr += str(t)
                signstr += "="
            signstr = signstr[:-1]
            signstr += "&"
        signstr = signstr[:-1]
        return signstr

    def _build_header(self):
        header = dict()
        header["Host"] = "asr.cloud.tencent.com"
        return header

    def _sign(self, signstr, secret_key):
        hmacstr = hmac.new(secret_key.encode('utf-8'),
                           signstr.encode('utf-8'), hashlib.sha1).digest()
        s = base64.b64encode(hmacstr)
        s = s.decode('utf-8')
        return s

    def _build_req_with_signature(self, secret_key, params, header):
        query = sorted(params.items(), key=lambda d: d[0])
        signstr = self._format_sign_string(query)
        signature = self._sign(signstr, secret_key)
        header["Authorization"] = signature
        requrl = "https://"
        requrl += signstr[4::]
        return requrl

    def _create_query_arr(self, req):
        query_arr = dict()
        query_arr['appid'] = self.appid
        query_arr['secretid'] = self.credential.secret_id
        query_arr['timestamp'] = str(int(time.time()))
        query_arr['engine_type'] = req.engine_type
        query_arr['voice_format'] = req.voice_format
        query_arr['speaker_diarization'] = req.speaker_diarization
        query_arr['hotword_id'] = req.hotword_id
        query_arr['customization_id'] = req.customization_id
        query_arr['filter_dirty'] = req.filter_dirty
        query_arr['filter_modal'] = req.filter_modal
        query_arr['filter_punc'] = req.filter_punc
        query_arr['convert_num_mode'] = req.convert_num_mode
        query_arr['word_info'] = req.word_info
        query_arr['first_channel_only'] = req.first_channel_only
        query_arr['reinforce_hotword'] = req.reinforce_hotword
        query_arr['sentence_max_length'] = req.sentence_max_length
        return query_arr

    def recognize(self, req, data):
        header = self._build_header()
        query_arr = self._create_query_arr(req)
        req_url = self._build_req_with_signature(self.credential.secret_key, query_arr, header)
        r = requests.post(req_url, headers=header, data=data)
        return r.text