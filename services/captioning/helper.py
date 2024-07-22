#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
#

# Note: abc = abstract base classes
from collections.abc import Mapping
from datetime import date, datetime, time, timedelta
from sys import argv
from typing import Optional
from pathlib import Path
import azure.cognitiveservices.speech as speechsdk  # type: ignore

# 英文
DEFAULT_MAX_LINE_LENGTH_SBCS = 37
# 中文
DEFAULT_MAX_LINE_LENGTH_MBCS = 24


# See speech_recognize_once_compressed_input() in:
# https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_sample.py
class BinaryFileReaderCallback(speechsdk.audio.PullAudioInputStreamCallback):
    def __init__(self, filename: str):
        super().__init__()
        self._file_h = open(filename, "rb")

    def read(self, buffer: memoryview) -> int:
        try:
            size = buffer.nbytes
            frames = self._file_h.read(size)
            buffer[:len(frames)] = frames
            return len(frames)
        except Exception as ex:
            print('Exception in `read`: {}'.format(ex))
            raise

    def close(self) -> None:
        print('closing file')
        try:
            self._file_h.close()
        except Exception as ex:
            print('Exception in `close`: {}'.format(ex))
            raise


class Read_Only_Dict(Mapping):
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)


# See:
# https://stackoverflow.com/a/12448721
# https://stackoverflow.com/a/39651061
def add_time_and_timedelta(t1: time, t2: timedelta) -> time:
    return (datetime.combine(date.min, t1) + t2).time()


def subtract_times(t1: time, t2: time) -> timedelta:
    return datetime.combine(date.min, t1) - datetime.combine(date.min, t2)


# We cannot simply create time with ticks.
def time_from_ticks(ticks) -> time:
    microseconds_1 = ticks / 10
    microseconds_2 = microseconds_1 % 1000000
    seconds_1 = microseconds_1 / 1000000
    seconds_2 = seconds_1 % 60
    minutes_1 = seconds_1 / 60
    minutes_2 = minutes_1 % 60
    hours = minutes_1 / 60
    return time(int(hours), int(minutes_2), int(seconds_2), int(microseconds_2))


def time_from_seconds(seconds) -> time:
    seconds = str.replace(str(seconds), "s", "")
    milliseconds = float(seconds) * 1000
    return time_from_milliseconds(milliseconds)


def time_from_milliseconds(milliseconds) -> time:
    # 假设我们有毫秒数
    # 将毫秒转换为微秒（timedelta 以微秒为单位）
    microseconds = milliseconds * 1000
    microseconds_2 = microseconds % 1000000
    seconds_1 = microseconds / 1000000
    seconds_2 = seconds_1 % 60
    minutes_1 = seconds_1 / 60
    minutes_2 = minutes_1 % 60
    hours = minutes_1 / 60
    return time(int(hours), int(minutes_2), int(seconds_2), int(microseconds_2))


def write_to_console(text: str, user_config: Read_Only_Dict):
    if not user_config["suppress_console_output"]:
        print(text, end="", flush=True)
    return


def write_to_console_or_file(text: str, user_config: Read_Only_Dict):
    write_to_console(text=text, user_config=user_config)
    if user_config["output_file"] is not None:
        file_path = Path(user_config["output_file"])
        with open(file_path, mode="a", newline="", encoding='utf-8') as f:
            f.write(text)
    return
