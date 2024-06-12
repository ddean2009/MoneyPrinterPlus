import os

import streamlit as st

from config.config import my_config
from services.audio.audio_service import AudioService
from services.captioning.captioning_service import generate_caption, add_subtitles
from services.llm.azure_service import MyAzureService
from services.llm.baichuan_service import MyBaichuanService
from services.llm.baidu_qianfan_service import BaiduQianfanService
from services.llm.kimi_service import MyKimiService
from services.llm.openai_service import MyOpenAIService
from services.llm.tongyi_service import MyTongyiService
from services.resource.pexels_service import PexelsService
from services.video.video_service import get_audio_duration, VideoService
from tools.tr_utils import tr
from tools.utils import random_with_system_time, get_must_session_option

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)
# 音频输出目录
audio_output_dir = os.path.join(script_dir, "./work")
audio_output_dir = os.path.abspath(audio_output_dir)

default_video_keyword = "AI"
default_audio_file = '/Users/wayne/data/git/projects/hunjian/work/1718075778714.mp3'
default_video_file = ["/Users/wayne/data/git/projects/hunjian/work/pexels-9373204-hd_1920_1080_25fps.mp4",
                      "/Users/wayne/data/git/projects/hunjian/work/pexels-18069166-uhd_3840_2160_24fps.mp4",
                      "/Users/wayne/data/git/projects/hunjian/work/pexels-18069232-hd_1920_1080_24fps.mp4",
                      "/Users/wayne/data/git/projects/hunjian/work/pexels-18069235-hd_1920_1080_24fps.mp4",
                      "/Users/wayne/data/git/projects/hunjian/work/pexels-18069403-uhd_3840_2160_24fps.mp4"]
default_subtitle_file = '/Users/wayne/data/git/projects/hunjian/work/1718075849055.srt'

test_mode = my_config["test_mode"]


def get_llm_provider(llm_provider):
    if llm_provider == "Azure":
        return MyAzureService()
    if llm_provider == "OpenAI":
        return MyOpenAIService()
    if llm_provider == "Moonshot":
        return MyKimiService()
    if llm_provider == "Qianfan":
        return BaiduQianfanService()
    if llm_provider == "Baichuan":
        return MyBaichuanService()
    if llm_provider == "Tongyi":
        return MyTongyiService()


def main_generate_video_content():
    print("main_generate_video_content begin")
    topic = get_must_session_option('video_subject', "请输入要生成的主题")
    video_language = st.session_state.get('video_language')
    video_length = st.session_state.get('video_length')

    llm_provider = my_config['llm']['provider']
    print("llm_provider:", llm_provider)
    llm_service = get_llm_provider(llm_provider)
    st.session_state["video_content"] = llm_service.generate_content(topic,
                                                                     llm_service.topic_prompt_template,
                                                                     video_language,
                                                                     video_length)
    st.session_state["video_keyword"] = llm_service.generate_content(st.session_state["video_content"],
                                                                     prompt_template=llm_service.keyword_prompt_template)
    print("keyword:", st.session_state.get("video_keyword"))
    print("main_generate_video_content end")


def main_generate_video_dubbing():
    print("main_generate_video_dubbing begin")
    audio_service = AudioService()
    temp_file_name = random_with_system_time()
    audio_output_file = os.path.join(audio_output_dir, str(temp_file_name) + ".mp3")
    st.session_state["audio_output_file"] = audio_output_file
    audio_speed = st.session_state.get("audio_speed")
    if audio_speed == "normal":
        audio_rate = "0.00"
    if audio_speed == "fast":
        audio_rate = "10.00"
    if audio_speed == "slow":
        audio_rate = "-10.00"
    if audio_speed == "faster":
        audio_rate = "20.00"
    if audio_speed == "slower":
        audio_rate = "-20.00"
    if audio_speed == "fastest":
        audio_rate = "30.00"
    if audio_speed == "slowest":
        audio_rate = "-30.00"

    video_content = get_must_session_option("video_content", "请先设置视频主题")
    audio_voice = get_must_session_option("audio_voice", "请先设置配音语音")
    audio_service.save_with_ssml(video_content,
                                 audio_output_file,
                                 audio_voice,
                                 audio_rate)
    print("main_generate_video_dubbing end")


def main_get_video_resource():
    print("main_get_video_resource begin")
    resource_service = PexelsService()
    if test_mode:
        if not st.session_state.get("video_keyword"):
            print("video_keyword not exist")
            query = default_video_keyword
    else:
        query = get_must_session_option("video_keyword", "请先设置视频关键字")

    if test_mode:
        if not st.session_state.get("audio_output_file"):
            print("no audio file")
            audio_file = default_audio_file
    else:
        audio_file = get_must_session_option("audio_output_file", "请先生成配音文件")
    audio_length = get_audio_duration(audio_file)
    print("audio_length:", audio_length)
    return_videos, total_length = resource_service.handle_video_resource(query, audio_length, 50, False)
    st.session_state["return_videos"] = return_videos
    return return_videos, audio_file


def main_generate_subtitle():
    print("main_generate_subtitle begin:")
    enable_subtitles = st.session_state.get("enable_subtitles")
    if enable_subtitles:
        # 设置输出字幕
        random_name = random_with_system_time()
        captioning_output = os.path.join(audio_output_dir, f"{random_name}.srt")
        st.session_state["captioning_output"] = captioning_output
        if test_mode:
            if not st.session_state.get("audio_output_file"):
                print("no audio file")
                st.session_state["audio_output_file"] = default_audio_file
        else:
            audio_output_file = get_must_session_option("audio_output_file", "请先生成配音文件")
        generate_caption()


def main_generate_ai_video(video_generator):
    print("main_generate_ai_video begin:")
    with video_generator:
        st_area = st.status(tr("Generate Video in process..."), expanded=True)
        with st_area as status:
            if not test_mode:
                st.write(tr("Generate Video Dubbing..."))
                main_generate_video_dubbing()
                st.write(tr("Get Video Resource..."))
                main_get_video_resource()
                st.write(tr("Generate Video subtitles..."))
                main_generate_subtitle()
            st.write(tr("Video normalize..."))
            if test_mode:
                if not st.session_state.get("audio_output_file"):
                    print("no audio file")
                    st.session_state["audio_output_file"] = default_audio_file
                audio_file = st.session_state.get("audio_output_file")
            else:
                audio_file = get_must_session_option("audio_output_file", "请先生成配音文件")

            if test_mode:
                if not st.session_state.get("return_videos"):
                    print("no video file")
                    video_list = default_video_file
                video_list = st.session_state.get("return_videos")
            else:
                video_list = get_must_session_option("return_videos", "请先生成视频资源文件")

            video_service = VideoService(video_list, audio_file)
            print("normalize video")
            video_service.normalize_video()
            st.write(tr("Generate Video..."))
            video_file = video_service.generate_video_with_audio()
            print("final file without subtitle:", video_file)

            enable_subtitles = st.session_state.get("enable_subtitles")
            if enable_subtitles:
                st.write(tr("Add Subtitles..."))
                if test_mode:
                    if not st.session_state.get('captioning_output'):
                        subtitle_file = default_subtitle_file
                else:
                    subtitle_file = get_must_session_option('captioning_output', "请先生成字幕文件")

                font_name = st.session_state.get('subtitle_font')
                font_size = st.session_state.get('subtitle_font_size')
                primary_colour = st.session_state.get('subtitle_color')
                outline_colour = st.session_state.get('subtitle_border_color')
                outline = st.session_state.get('subtitle_border_width')
                alignment = st.session_state.get('subtitle_position')
                add_subtitles(video_file, subtitle_file,
                              font_name=font_name,
                              font_size=font_size,
                              primary_colour=primary_colour,
                              outline_colour=outline_colour,
                              outline=outline,
                              alignment=alignment)
                print("final file with subtitle:", video_file)
            st.session_state["result_video_file"] = video_file
            status.update(label=tr("Generate Video completed!"), state="complete", expanded=False)
