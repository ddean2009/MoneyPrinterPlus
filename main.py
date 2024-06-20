import os

import streamlit as st

from config.config import my_config
from services.audio.alitts_service import AliAudioService
from services.audio.azure_service import AzureAudioService
from services.audio.tencent_tts_service import TencentAudioService
from services.captioning.captioning_service import generate_caption, add_subtitles
from services.llm.azure_service import MyAzureService
from services.llm.baichuan_service import MyBaichuanService
from services.llm.baidu_qianfan_service import BaiduQianfanService
from services.llm.deepseek_service import MyDeepSeekService
from services.llm.kimi_service import MyKimiService
from services.llm.openai_service import MyOpenAIService
from services.llm.tongyi_service import MyTongyiService
from services.resource.pexels_service import PexelsService
from services.resource.pixabay_service import PixabayService
from services.video.video_service import get_audio_duration, VideoService
from tools.tr_utils import tr
from tools.utils import random_with_system_time, get_must_session_option, extent_audio

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)
# 音频输出目录
audio_output_dir = os.path.join(script_dir, "./work")
audio_output_dir = os.path.abspath(audio_output_dir)


def get_resource_provider():
    resource_provider = my_config['resource']['provider']
    print("resource_provider:", resource_provider)
    if resource_provider == "pexels":
        return PexelsService()
    if resource_provider == "pixabay":
        return PixabayService()


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
    if llm_provider == "DeepSeek":
        return MyDeepSeekService()


def get_audio_service():
    selected_audio_provider = my_config['audio']['provider']
    if selected_audio_provider == "Azure":
        return AzureAudioService()
    if selected_audio_provider == "Ali":
        return AliAudioService()
    if selected_audio_provider == "Tencent":
        return TencentAudioService()


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


def main_try_test_audio():
    print("main_try_test_audio begin")
    audio_service = get_audio_service()
    audio_rate = get_audio_rate()
    audio_language = st.session_state.get("audio_language")
    if audio_language == "en-US":
        video_content = "hello,this is flydean"
    else:
        video_content = "你好，我是程序那些事"
    audio_voice = get_must_session_option("audio_voice", "请先设置配音语音")
    audio_service.read_with_ssml(video_content,
                                 audio_voice,
                                 audio_rate)


def main_generate_video_dubbing():
    print("main_generate_video_dubbing begin")
    audio_service = get_audio_service()
    temp_file_name = random_with_system_time()
    audio_output_file = os.path.join(audio_output_dir, str(temp_file_name) + ".wav")
    st.session_state["audio_output_file"] = audio_output_file
    audio_rate = get_audio_rate()

    video_content = get_must_session_option("video_content", "请先设置视频主题")
    audio_voice = get_must_session_option("audio_voice", "请先设置配音语音")
    audio_service.save_with_ssml(video_content,
                                 audio_output_file,
                                 audio_voice,
                                 audio_rate)
    # 语音扩展2秒钟,防止突然结束很突兀
    extent_audio(audio_output_file, 2)
    print("main_generate_video_dubbing end")


def get_audio_rate():
    audio_provider = my_config['audio']['provider']
    if audio_provider == "Azure":
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
        return audio_rate
    if audio_provider == "Ali":
        audio_speed = st.session_state.get("audio_speed")
        if audio_speed == "normal":
            audio_rate = "0"
        if audio_speed == "fast":
            audio_rate = "150"
        if audio_speed == "slow":
            audio_rate = "-150"
        if audio_speed == "faster":
            audio_rate = "250"
        if audio_speed == "slower":
            audio_rate = "-250"
        if audio_speed == "fastest":
            audio_rate = "400"
        if audio_speed == "slowest":
            audio_rate = "-400"
        return audio_rate
    if audio_provider == "Tencent":
        audio_speed = st.session_state.get("audio_speed")
        if audio_speed == "normal":
            audio_rate = "0"
        if audio_speed == "fast":
            audio_rate = "1"
        if audio_speed == "slow":
            audio_rate = "-1"
        if audio_speed == "faster":
            audio_rate = "1.5"
        if audio_speed == "slower":
            audio_rate = "-1.5"
        if audio_speed == "fastest":
            audio_rate = "2"
        if audio_speed == "slowest":
            audio_rate = "-2"
        return audio_rate


def main_get_video_resource():
    print("main_get_video_resource begin")
    resource_service = get_resource_provider()
    query = get_must_session_option("video_keyword", "请先设置视频关键字")
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
        audio_output_file = get_must_session_option("audio_output_file", "请先生成配音文件")
        generate_caption()


def main_generate_ai_video(video_generator):
    print("main_generate_ai_video begin:")
    with video_generator:
        st_area = st.status(tr("Generate Video in process..."), expanded=True)
        with st_area as status:
            st.write(tr("Generate Video Dubbing..."))
            main_generate_video_dubbing()
            st.write(tr("Generate Video subtitles..."))
            main_generate_subtitle()
            st.write(tr("Get Video Resource..."))
            main_get_video_resource()
            st.write(tr("Video normalize..."))
            audio_file = get_must_session_option("audio_output_file", "请先生成配音文件")
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
