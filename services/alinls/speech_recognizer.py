# Copyright (c) Alibaba, Inc. and its affiliates.

import logging
import uuid
import json
import threading


from .core import NlsCore
from . import logging
from . import util
from .exception import (StartTimeoutException,
                        StopTimeoutException,
                        NotStartException,
                        InvalidParameter)

__SPEECH_RECOGNIZER_NAMESPACE__ = 'SpeechRecognizer'

__SPEECH_RECOGNIZER_REQUEST_CMD__ = {
    'start': 'StartRecognition',
    'stop': 'StopRecognition'
}

__URL__ = 'wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1'

__all__ = ['NlsSpeechRecognizer']


class NlsSpeechRecognizer:
    """
    Api for short sentence speech recognition
    """    
    def __init__(self,
                 url=__URL__,
                 token=None,
                 appkey=None,
                 on_start=None,
                 on_result_changed=None,
                 on_completed=None,
                 on_error=None, on_close=None,
                 callback_args=[]):
        """
        NlsSpeechRecognizer initialization

        Parameters:
        -----------
        url: str
            websocket url.
        token: str
            access token. if you do not have a token, provide access id and key
            secret from your aliyun account.
        appkey: str
            appkey from aliyun
        on_start: function
            Callback object which is called when recognition started.
            on_start has two arguments.
            The 1st argument is message which is a json format string.
            The 2nd argument is *args which is callback_args.
        on_result_changed: function
            Callback object which is called when partial recognition result
            arrived.
            on_result_changed has two arguments.
            The 1st argument is message which is a json format string.
            The 2nd argument is *args which is callback_args.
        on_completed: function
            Callback object which is called when recognition is completed.
            on_completed has two arguments.
            The 1st argument is message which is a json format string.
            The 2nd argument is *args which is callback_args.
        on_error: function
            Callback object which is called when any error occurs.
            on_error has two arguments.
            The 1st argument is message which is a json format string.
            The 2nd argument is *args which is callback_args.
        on_close: function
            Callback object which is called when connection closed.
            on_close has one arguments.
            The 1st argument is *args which is callback_args.
        callback_args: list
            callback_args will return in callbacks above for *args.
        """
        if not token or not appkey:
            raise InvalidParameter('Must provide token and appkey')
        self.__response_handler__ = {
            'RecognitionStarted': self.__recognition_started,
            'RecognitionResultChanged': self.__recognition_result_changed,
            'RecognitionCompleted': self.__recognition_completed,
            'TaskFailed': self.__task_failed
        }
        self.__callback_args = callback_args
        self.__appkey = appkey
        self.__url = url
        self.__token = token
        self.__start_cond = threading.Condition()
        self.__start_flag = False
        self.__on_start = on_start
        self.__on_result_changed = on_result_changed
        self.__on_completed = on_completed
        self.__on_error = on_error
        self.__on_close = on_close
        self.__allow_aformat = (
            'pcm', 'opus', 'opu', 'wav', 'mp3', 'speex', 'aac', 'amr'
        )

    def __handle_message(self, message):
        print('__handle_message')
        try:
            __result = json.loads(message)
            if __result['header']['name'] in self.__response_handler__:
                __handler = self.__response_handler__[
                    __result['header']['name']]
                __handler(message)
            else:
                logging.error('cannot handle cmd{}'.format(
                    __result['header']['name']))
                return
        except json.JSONDecodeError:
            logging.error('cannot parse message:{}'.format(message))
            return

    def __sr_core_on_open(self):
        print('__sr_core_on_open')

    def __sr_core_on_msg(self, msg, *args):
        print('__sr_core_on_msg:msg={} args={}'.format(msg, args))
        self.__handle_message(msg)

    def __sr_core_on_error(self, msg, *args):
        print('__sr_core_on_error:msg={} args={}'.format(msg, args))

    def __sr_core_on_close(self):
        print('__sr_core_on_close')
        if self.__on_close:
            self.__on_close(*self.__callback_args)
        with self.__start_cond:
            self.__start_flag = False
            self.__start_cond.notify()

    def __recognition_started(self, message):
        print('__recognition_started')
        if self.__on_start:
            self.__on_start(message, *self.__callback_args)
        with self.__start_cond:
            self.__start_flag = True
            self.__start_cond.notify()

    def __recognition_result_changed(self, message):
        print('__recognition_result_changed')
        if self.__on_result_changed:
            self.__on_result_changed(message, *self.__callback_args)

    def __recognition_completed(self, message):
        print('__recognition_completed')
        self.__nls.shutdown()
        print('__recognition_completed shutdown done')
        if self.__on_completed:
            self.__on_completed(message, *self.__callback_args)
        with self.__start_cond:
            self.__start_flag = False
            self.__start_cond.notify()

    def __task_failed(self, message):
        print('__task_failed')
        with self.__start_cond:
            self.__start_flag = False
            self.__start_cond.notify()
        if self.__on_error:
            self.__on_error(message, *self.__callback_args)

    def start(self, aformat='pcm', sample_rate=16000, ch=1,
              enable_intermediate_result=False,
              enable_punctuation_prediction=False,
              enable_inverse_text_normalization=False,
              timeout=10,
              ping_interval=8,
              ping_timeout=None,
              ex:dict=None):
        """
        Recognition start 

        Parameters:
        -----------
        aformat: str
            audio binary format, support: 'pcm', 'opu', 'opus', default is 'pcm'
        sample_rate: int
            audio sample rate, default is 16000
        ch: int
            audio channels, only support mono which is 1
        enable_intermediate_result: bool
            whether enable return intermediate recognition result, default is False
        enable_punctuation_prediction: bool
            whether enable punctuation prediction, default is False
        enable_inverse_text_normalization: bool
            whether enable ITN, default is False
        timeout: int
            wait timeout for connection setup
        ping_interval: int
            send ping interval, 0 for disable ping send, default is 8
        ping_timeout: int
            timeout after send ping and recive pong, set None for disable timeout check and default is None
        ex: dict
            dict which will merge into 'payload' field in request
        """
        self.__nls = NlsCore(
            url=self.__url, 
            token=self.__token,
            on_open=self.__sr_core_on_open,
            on_message=self.__sr_core_on_msg,
            on_close=self.__sr_core_on_close,
            on_error=self.__sr_core_on_error,
            callback_args=[])

        if ch != 1:
            raise InvalidParameter(f'Not support channel {ch}')
        if aformat not in self.__allow_aformat:
            raise InvalidParameter(f'Format {aformat} not support')

        __id4 = uuid.uuid4().hex
        self.__task_id = uuid.uuid4().hex
        __header = {
            'message_id': __id4,
            'task_id': self.__task_id,
            'namespace': __SPEECH_RECOGNIZER_NAMESPACE__,
            'name': __SPEECH_RECOGNIZER_REQUEST_CMD__['start'],
            'appkey': self.__appkey
        }
        __payload = {
            'format': aformat,
            'sample_rate': sample_rate,
            'enable_intermediate_result': enable_intermediate_result,
            'enable_punctuation_prediction': enable_punctuation_prediction,
            'enable_inverse_text_normalization': enable_inverse_text_normalization
        }

        if ex:
            __payload.update(ex)

        __msg = {
            'header': __header,
            'payload': __payload,
            'context': util.GetDefaultContext()
        }
        __jmsg = json.dumps(__msg)
        with self.__start_cond:
            if self.__start_flag:
                print('already start...')
                return
            self.__nls.start(__jmsg, ping_interval, ping_timeout)
            if self.__start_flag == False:
                if self.__start_cond.wait(timeout=timeout):
                    return
                else:
                    raise StartTimeoutException(f'Waiting Start over {timeout}s')

    def stop(self, timeout=10):
        """
        Stop recognition and mark session finished

        Parameters:
        -----------
        timeout: int
            timeout for waiting completed message from cloud
        """
        __id4 = uuid.uuid4().hex
        __header = {
            'message_id': __id4,
            'task_id': self.__task_id,
            'namespace': __SPEECH_RECOGNIZER_NAMESPACE__,
            'name': __SPEECH_RECOGNIZER_REQUEST_CMD__['stop'],
            'appkey': self.__appkey
        }
        __msg = {
            'header': __header,
            'context': util.GetDefaultContext()    
        }
        __jmsg = json.dumps(__msg)
        with self.__start_cond:
            if not self.__start_flag:
                print('not start yet...')
                return
            self.__nls.send(__jmsg, False)
            if self.__start_flag == True:
                print('stop wait..')
                if self.__start_cond.wait(timeout):
                    return
                else:
                    raise StopTimeoutException(f'Waiting stop over {timeout}s')
    def shutdown(self):
        """
        Shutdown connection immediately
        """
        self.__nls.shutdown()

    def send_audio(self, pcm_data):
        """
        Send audio binary, audio size prefer 20ms length 

        Parameters:
        -----------
        pcm_data: bytes
            audio binary which format is 'aformat' in start method 
        """
        if not pcm_data:
            raise InvalidParameter('data empty!')
        __data = pcm_data
        with self.__start_cond:
            if not self.__start_flag:
                raise NotStartException('Need start before send!')
        try:
            self.__nls.send(__data, True)
        except ConnectionResetError as __e:
            logging.error('connection reset')
            self.__start_flag = False
            self.__nls.shutdown()
            raise __e
