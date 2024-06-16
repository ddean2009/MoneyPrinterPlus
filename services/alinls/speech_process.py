import http.client
import json
from typing import List

from config.config import my_config
from services.alinls.token import getToken
from tools.utils import must_have_value


class AliRecognitionResult:
    def __init__(self, text, begin_time, end_time):
        self.text = text
        self.begin_time = begin_time
        self.end_time = end_time


class AliRecognitionService:
    def __init__(self):
        self.ALI_ACCESS_AKID = my_config['audio']['Ali']['access_key_id']
        self.ALI_ACCESS_AKKEY = my_config['audio']['Ali']['access_key_secret']
        self.ALI_APP_KEY = my_config['audio']['Ali']['app_key']
        must_have_value(self.ALI_ACCESS_AKID, "请设置Ali access key id")
        must_have_value(self.ALI_ACCESS_AKKEY, "请设置Ali access key secret")
        must_have_value(self.ALI_APP_KEY, "请设置Ali app key")
        self.token = getToken(self.ALI_ACCESS_AKID, self.ALI_ACCESS_AKKEY)
        self.format = "wav"
        self.sampleRate = 16000
        self.url = 'https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/FlashRecognizer'

    def process(self, audioFile) -> List[AliRecognitionResult]:
        result_list = []
        # 设置RESTful请求参数
        request = self.url + '?appkey=' + self.ALI_APP_KEY
        request = request + '&token=' + self.token
        request = request + '&format=' + self.format
        request = request + '&sample_rate=' + str(self.sampleRate)

        # 读取音频文件
        with open(audioFile, mode='rb') as f:
            audioContent = f.read()
        host = 'nls-gateway-cn-shanghai.aliyuncs.com'
        # 设置HTTP请求头部
        httpHeaders = {
            'Content-Length': len(audioContent)
        }
        # Python 3.x使用http.client
        conn = http.client.HTTPSConnection(host)

        conn.request(method='POST', url=request, body=audioContent, headers=httpHeaders)
        response = conn.getresponse()
        print('Response status and response reason:')
        print(response.status, response.reason)
        body = response.read()
        try:
            print('Recognize response is:')
            body = json.loads(body)
            print(body)
            status = body['status']
            if status == 20000000:
                result = body['flash_result']
                # print(result)
                # result = json.loads(result)
                if 'sentences' in result:
                    for sentence in result['sentences']:
                        result_list.append(
                            AliRecognitionResult(sentence['text'], sentence['begin_time'], sentence['end_time']))
            else:
                print('Recognizer failed!')
        except ValueError:
            print('The response is not json format string')
        conn.close()
        return result_list
