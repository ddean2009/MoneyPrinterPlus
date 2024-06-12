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

