#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
#

from datetime import time
from typing import List, Optional, Tuple

from services.alinls.speech_process import AliRecognitionResult
import azure.cognitiveservices.speech as speechsdk

from services.audio.faster_whisper_recognition_service import FasterWhisperRecognitionResult
from services.audio.tencent_recognition_service import TencentRecognitionResult
from services.captioning import helper


class Caption(object):
    def __init__(self, language: Optional[str], sequence: int, begin: time, end: time, text: str):
        self.language = language
        self.sequence = sequence
        self.begin = begin
        self.end = end
        self.text = text


def get_captions(language: Optional[str], max_width: int, max_height: int, results: List[dict]) -> List[Caption]:
    caption_helper = CaptionHelper(language, max_width, max_height, results)
    return caption_helper.get_captions()


class CaptionHelper(object):
    def __init__(self, language: Optional[str], max_width: int, max_height: int,
                 results: List[object]):
        self._language = language
        self._max_width = max_width
        self._max_height = max_height
        self._results = results

        self._first_pass_terminators = ["?", "!", ",", ";"]
        self._second_pass_terminators = [" ", "."]

        self._captions: List[Caption] = []

        # consider adapting to use http://unicode.org/reports/tr29/#Sentence_Boundaries
        if self._language is not None:
            iso639 = self._language.split('-')[0]
            if "zh" == iso639.lower():
                self._first_pass_terminators = ["，", "、", "；", "？", "！", "?", "!", ",", ";"]
                self._second_pass_terminators = ["。", " "]
                if helper.DEFAULT_MAX_LINE_LENGTH_SBCS == self._max_width:
                    self._max_width = helper.DEFAULT_MAX_LINE_LENGTH_MBCS

    def get_captions(self) -> List[Caption]:
        self.ensure_captions()
        return self._captions

    def ensure_captions(self) -> None:
        if not self._captions:
            self.add_captions_for_all_results()

    def add_captions_for_all_results(self) -> None:
        for result in self._results:
            if (hasattr(result, 'offset') and result.offset <= 0) or not self.is_final_result(result):
                continue
            text = self.get_text_or_translation(result)
            if not text:
                continue
            self.add_captions_for_final_result(result, text)

    def get_text_or_translation(self, result: object) -> Optional[str]:
        return result.text

    def add_captions_for_final_result(self, result: object, text: str) -> None:
        caption_starts_at = 0
        caption_lines: List[str] = []
        index = 0
        while index < len(text):
            index = self.skip_skippable(text, index)

            line_length = self.get_best_width(text, index)
            caption_lines.append(text[index:index + line_length].strip())
            index += line_length

            is_last_caption = index >= len(text)
            max_caption_lines = len(caption_lines) >= self._max_height

            add_caption = is_last_caption or max_caption_lines

            if add_caption:
                caption_text = '\n'.join(caption_lines)
                caption_lines.clear()

                caption_sequence = len(self._captions) + 1
                is_first_caption = 0 == caption_starts_at

                caption_begin_and_end: Tuple[time, time]
                if is_first_caption and is_last_caption:
                    caption_begin_and_end = self.get_full_caption_result_timing(result)
                else:
                    caption_begin_and_end = self.get_partial_result_caption_timing(result, text, caption_text,
                                                                                   caption_starts_at,
                                                                                   index - caption_starts_at)

                self._captions.append(
                    Caption(self._language, caption_sequence, caption_begin_and_end[0], caption_begin_and_end[1],
                            caption_text))

                caption_starts_at = index

    def get_best_width(self, text: str, start_index: int) -> int:
        # print("get_best_width:",text)
        remaining = len(text) - start_index
        best_width = remaining if remaining < self._max_width else self.find_best_width(self._first_pass_terminators,
                                                                                        text, start_index)
        if best_width < 0:
            best_width = self.find_best_width(self._second_pass_terminators, text, start_index)
        if best_width < 0:
            best_width = self._max_width
        # print("best_width",best_width)
        return best_width

    def find_best_width(self, terminators: List[str], text: str, start_at: int) -> int:
        remaining = len(text) - start_at
        check_chars = min(remaining, self._max_width)
        best_width = -1
        for terminator in terminators:
            index = text.rfind(terminator, start_at, start_at + check_chars)
            width = index - start_at
            if width > best_width:
                best_width = width + len(terminator)
        return best_width

    def skip_skippable(self, text: str, start_index: int) -> int:
        index = start_index
        while len(text) > index and ' ' == text[index]:
            index += 1
        return index

    def get_full_caption_result_timing(self, result: object) -> Tuple[time, time]:
        if isinstance(result, speechsdk.RecognitionResult):
            begin = helper.time_from_ticks(result.offset)
            end = helper.time_from_ticks(result.offset + result.duration)
            return begin, end
        if isinstance(result, AliRecognitionResult) or isinstance(result, TencentRecognitionResult):
            begin = helper.time_from_milliseconds(result.begin_time)
            end = helper.time_from_milliseconds(result.end_time)
            return begin, end
        if isinstance(result, FasterWhisperRecognitionResult):
            begin = helper.time_from_seconds(result.begin_time)
            end = helper.time_from_seconds(result.end_time)
            return begin, end

    def get_partial_result_caption_timing(self, result: object, text: str, caption_text: str,
                                          caption_starts_at: int, caption_length: int) -> Tuple[time, time]:
        (result_begin, result_end) = self.get_full_caption_result_timing(result)
        result_duration = helper.subtract_times(result_end, result_begin)
        text_length = len(text)
        partial_begin = helper.add_time_and_timedelta(result_begin, result_duration * caption_starts_at / text_length)
        partial_end = helper.add_time_and_timedelta(result_begin, result_duration * (
                caption_starts_at + caption_length) / text_length)
        return partial_begin, partial_end

    def is_final_result(self, result: object) -> bool:
        if isinstance(result, speechsdk.RecognitionResult):
            return speechsdk.ResultReason.RecognizedSpeech == result.reason or speechsdk.ResultReason.RecognizedIntent == result.reason or speechsdk.ResultReason.TranslatedSpeech == result.reason
        if isinstance(result, AliRecognitionResult) or isinstance(result, TencentRecognitionResult) or isinstance(result, FasterWhisperRecognitionResult):
            return True

    def lines_from_text(self, text: str) -> List[str]:
        retval: List[str] = []
        index = 0
        while index < len(text):
            index = self.skip_skippable(text, index)
            line_length = self.get_best_width(text, index)
            retval.append(text[index:index + line_length].strip())
            index += line_length
        return retval
