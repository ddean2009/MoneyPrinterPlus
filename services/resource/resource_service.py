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

from abc import ABC, abstractmethod
import streamlit as st

from const.video_const import Orientation


class ResourceService(ABC):
    def __init__(self):
        # self.exact_match = exact_match
        self.orientation = Orientation(st.session_state.get("video_layout"))
        self.width, self.height = st.session_state.get("video_size").split('x')
        self.width = int(self.width)
        self.height = int(self.height)
        self.fps = st.session_state.get("video_fps")
        self.video_segment_min_length = st.session_state.get("video_segment_min_length")
        self.video_segment_max_length = st.session_state.get("video_segment_max_length")

        # 是否开启转场特效
        self.enable_video_transition_effect = st.session_state.get("enable_video_transition_effect")
        self.video_transition_effect_duration = st.session_state.get("video_transition_effect_duration")

    @abstractmethod
    def handle_video_resource(self, query, audio_length, per_page=10, exact_match=False):
        raise NotImplementedError

