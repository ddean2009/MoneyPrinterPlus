#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
#

from datetime import timedelta
from enum import Enum
from os import linesep, environ
from sys import argv
from typing import List, Optional
import azure.cognitiveservices.speech as speechsdk  # type: ignore
from config.config import my_config
import streamlit as st

from services.captioning import helper
from tools.utils import get_session_option, must_have_value

key = my_config['audio']['Azure']['speech_key']
region = my_config['audio']['Azure']['service_region']

# must_have_value(key, "请设置Azure speech_key")
# must_have_value(region, "请设置Azure service_region")


class CaptioningMode(Enum):
    OFFLINE = 1
    REALTIME = 2


def get_language() -> str:
    retval = "zh-CN"
    language = get_session_option("audio_language")
    if language is not None:
        retval = language
    return retval


def get_phrases() -> List[str]:
    retval: List[str] = []
    phrases = get_session_option("captioning_phrases")
    if phrases is not None:
        retval = list(map(lambda phrase: phrase.strip(), phrases.split(';')))
    return retval


def get_compressed_audio_format() -> speechsdk.AudioStreamContainerFormat:
    value = get_session_option("captioning_format")
    if value is None:
        return speechsdk.AudioStreamContainerFormat.ANY
    else:
        value = value.lower()
        if "alaw" == value:
            return speechsdk.AudioStreamContainerFormat.ALAW
        elif "flac" == value:
            return speechsdk.AudioStreamContainerFormat.FLAC
        elif "mp3" == value:
            return speechsdk.AudioStreamContainerFormat.MP3
        elif "mulaw" == value:
            return speechsdk.AudioStreamContainerFormat.MULAW
        elif "ogg_opus" == value:
            return speechsdk.AudioStreamContainerFormat.OGG_OPUS
        else:
            return speechsdk.AudioStreamContainerFormat.ANY


def get_profanity_option() -> speechsdk.ProfanityOption:
    value = get_session_option("captioning_profanity")
    if value is None:
        return speechsdk.ProfanityOption.Masked
    else:
        value = value.lower()
        if "raw" == value:
            return speechsdk.ProfanityOption.Raw
        elif "remove" == value:
            return speechsdk.ProfanityOption.Removed
        else:
            return speechsdk.ProfanityOption.Masked


def user_config_from_args() -> helper.Read_Only_Dict:
    if get_session_option("captioning_mode") == "realtime":
        captioning_mode = CaptioningMode.REALTIME
    else:
        captioning_mode = CaptioningMode.OFFLINE

    td_remain_time = timedelta(milliseconds=1000)
    s_remain_time = get_session_option("captioning_remainTime")
    if s_remain_time is not None:
        int_remain_time = float(s_remain_time)
        if int_remain_time < 0:
            int_remain_time = 1000
        td_remain_time = timedelta(milliseconds=int_remain_time)

    td_delay = timedelta(milliseconds=1000)
    s_delay = get_session_option("captioning_delay")
    if s_delay is not None:
        int_delay = float(s_delay)
        if int_delay < 0:
            int_delay = 1000
        td_delay = timedelta(milliseconds=int_delay)

    int_max_line_length = helper.DEFAULT_MAX_LINE_LENGTH_SBCS
    s_max_line_length = get_session_option("captioning_maxLineLength")
    if s_max_line_length is not None:
        int_max_line_length = int(s_max_line_length)
        if int_max_line_length < 20:
            int_max_line_length = 20

    int_lines = 2
    s_lines = get_session_option("captioning_lines")
    if s_lines is not None:
        int_lines = int(s_lines)
        if int_lines < 1:
            int_lines = 2

    return helper.Read_Only_Dict({
        "use_compressed_audio": get_session_option("captioning_format"),
        "compressed_audio_format": get_compressed_audio_format(),
        "profanity_option": get_profanity_option(),
        "language": get_language(),
        "input_file": get_session_option("audio_output_file"),
        "output_file": get_session_option("captioning_output"),
        "phrases": get_phrases(),
        "suppress_console_output": get_session_option("captioning_quiet"),
        "captioning_mode": captioning_mode,
        "remain_time": td_remain_time,
        "delay": td_delay,
        "use_sub_rip_text_caption_format": True,
        "max_line_length": int_max_line_length,
        "lines": int_lines,
        "stable_partial_result_threshold": get_session_option("captioning_threshold"),
        "subscription_key": key,
        "region": region,
    })
