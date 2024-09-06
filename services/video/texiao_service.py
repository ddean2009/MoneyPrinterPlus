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

import streamlit as st

def gen_filter(segments, target_width, target_height,transition_type, transition_value, transition_duration ,with_audio=False):
    video_fades = ""
    audio_fades = ""
    settb = ""
    last_fade_output = "0v"
    last_audio_output = "0:a"

    video_length = 0
    file_lengths = [0] * len(segments)

    if target_width:
        for i in range(len(segments)):
            # 视频归一化
            # settb += "[%d:v]settb=AVTB,fps=30,scale=w=%d:h=%d:force_original_aspect_ratio=1,pad=%d:%d:(ow-iw)/2:(oh-ih)/2[%dv];" % (i, target_width, target_height, target_width, target_height, i)
            settb += "[%d:v]settb=AVTB,scale=w=%d:h=%d:force_original_aspect_ratio=1,pad=%d:%d:(ow-iw)/2:(oh-ih)/2[%dv];" % (
            i, target_width, target_height, target_width, target_height, i)

    str_list = [str(f) for f in segments]
    print("转场视频长度：" + " ".join(str_list))
    for i in range(len(segments) - 1):
        file_lengths[i] = segments[i]

        video_length += float(file_lengths[i])
        next_fade_output = "v%d%d" % (i, i + 1)
        video_fades += f"[%s][%dv]{transition_type}=transition=%s:duration=%f:offset=%f%s%s" % \
                       (last_fade_output, i + 1, transition_value, float(transition_duration), video_length - float(transition_duration) * (i + 1),
                        '[' + next_fade_output + '];' if (i) < len(segments) - 2 else "",
                        "" if i < len(segments) - 2 else ",format=yuv420p[video];")
        last_fade_output = next_fade_output

        if with_audio:
            next_audio_output = "a%d%d" % (i, i + 1)
            # audio_fades += "[%s][%d:a]acrossfade=d=%f%s" % \
            # 第二段音频不需要淡入效果
            audio_fades += "[%s][%d:a]acrossfade=d=%f:c2=nofade%s" % \
                           (last_audio_output, i + 1, float(transition_duration),
                            '[' + next_audio_output + '];' if (i) < len(segments) - 2 else "[audio]")
            # 直接concat 不做效果处理
            # audio_fades += "[%s][%d:a]concat=n=2:v=0:a=1%s" % \
            #                (last_audio_output, i + 1,
            #                 '[' + next_audio_output + '];' if (i) < len(segments) - 2 else "[audio]")
            last_audio_output = next_audio_output

    if with_audio:
        return settb + video_fades + audio_fades
    return settb + video_fades
