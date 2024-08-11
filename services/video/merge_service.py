import itertools
import os
import random
import subprocess
from datetime import timedelta

import streamlit as st

from services.captioning.captioning_service import add_subtitles
from services.hunjian.hunjian_service import get_session_video_scene_text, get_video_scene_text_list
from services.video.texiao_service import gen_filter
from services.video.video_service import DEFAULT_DURATION, get_image_info, get_video_duration, get_video_info, \
    get_video_length_list, add_background_music
from tools.file_utils import generate_temp_filename
from tools.tr_utils import tr
from tools.utils import run_ffmpeg_command, random_with_system_time

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)
# 视频出目录
video_output_dir = os.path.join(script_dir, "../../final")
video_output_dir = os.path.abspath(video_output_dir)

# work目录
work_output_dir = os.path.join(script_dir, "../../work")
work_output_dir = os.path.abspath(work_output_dir)


def merge_generate_subtitle(video_scene_video_list, video_scene_text_list):
    enable_subtitles = st.session_state.get("enable_subtitles")
    if enable_subtitles and video_scene_text_list is not None:
        st.write(tr("Add Subtitles..."))
        for video_file, scene_text in zip(video_scene_video_list, video_scene_text_list):
            if scene_text is not None:
                generate_subtitles(video_file, scene_text)


def generate_subtitles(video_file, scene_text):
    # 获取视频时长
    video_duration = get_video_duration(video_file)
    # 生成字幕文件
    # 设置输出字幕
    random_name = random_with_system_time()
    captioning_output = os.path.join(work_output_dir, f"{random_name}.srt")
    subtitle_file = generate_temp_filename(captioning_output)
    gen_subtitle_file(subtitle_file, scene_text, video_duration)
    # 添加字幕

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
    print("file with subtitle:", video_file)


def format_time(seconds):
    """格式化时间为 SRT 字幕格式"""
    time = str(timedelta(seconds=seconds))
    if '.' in time:
        time, milliseconds = time.split('.')
        milliseconds = int(milliseconds) * 1000
    else:
        milliseconds = 0
    return f"{time},000" if milliseconds == 0 else f"{time},{milliseconds:03d}"


def gen_subtitle_file(subtitle_file, scene_text, video_duration):
    """生成 SRT 字幕文件"""
    start_time = 0
    end_time = video_duration

    with open(subtitle_file, 'w', encoding='utf-8') as file:
        file.write("1\n")
        file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
        file.write(f"{scene_text}\n")
        file.write("\n")


def merge_get_video_list():
    print("merge_get_video_list begin")
    video_dir_list, video_text_list = get_session_video_scene_text()
    video_scene_text_list = get_video_scene_text_list(video_text_list)
    video_scene_video_list = get_video_scene_video_list(video_dir_list)
    return video_scene_video_list, video_scene_text_list


def get_video_scene_video_list(video_dir_list):
    video_scene_video_list = []
    for video_dir in video_dir_list:
        if video_dir is not None:
            video_file = random_video_from_dir(video_dir)
            video_scene_video_list.append(video_file)
    return video_scene_video_list


def random_video_from_dir(video_dir):
    # 获取媒体文件夹中的所有图片和视频文件
    media_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if
                   f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]

    # 随机排序媒体文件
    random.shuffle(media_files)

    # 确保有视频文件在列表中
    video_files = [os.path.join(video_dir, f) for f in media_files if f.lower().endswith(('.mp4', '.mov'))]
    if video_files:
        # 从视频文件中随机选择一个
        random_video = random.choice(video_files)
    else:
        random_video = random.choice(media_files)
    return random_video


class VideoMergeService:
    def __init__(self, video_list):
        self.video_list = video_list
        self.fps = st.session_state["video_fps"]
        self.target_width, self.target_height = st.session_state["video_size"].split('x')
        self.target_width = int(self.target_width)
        self.target_height = int(self.target_height)

        self.enable_background_music = st.session_state["enable_background_music"]
        self.background_music = st.session_state["background_music"]
        self.background_music_volume = st.session_state["background_music_volume"]

        self.enable_video_transition_effect = st.session_state["enable_video_transition_effect"]
        self.video_transition_effect_duration = st.session_state["video_transition_effect_duration"]
        self.video_transition_effect_type = st.session_state["video_transition_effect_type"]
        self.video_transition_effect_value = st.session_state["video_transition_effect_value"]
        self.default_duration = DEFAULT_DURATION

    def normalize_video(self):
        return_video_list = []
        for media_file in self.video_list:
            # 如果当前文件是图片，添加转换为视频的命令
            if media_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                output_name = generate_temp_filename(media_file, ".mp4", work_output_dir)
                # 判断图片的纵横比和
                img_width, img_height = get_image_info(media_file)
                if img_width / img_height > self.target_width / self.target_height:
                    # 转换图片为视频片段 图片的视频帧率必须要跟视频的帧率一样，否则可能在最后的合并过程中导致 合并过后的视频过长
                    ffmpeg_cmd = [
                        'ffmpeg',
                        '-loop', '1',
                        '-i', media_file,
                        '-c:v', 'h264',
                        '-t', str(self.default_duration),
                        '-r', str(self.fps),
                        '-vf',
                        f'scale=-1:{self.target_height}:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2'
                        '-y', output_name]
                else:
                    ffmpeg_cmd = [
                        'ffmpeg',
                        '-loop', '1',
                        '-i', media_file,
                        '-c:v', 'h264',
                        '-t', str(self.default_duration),
                        '-r', str(self.fps),
                        '-vf',
                        f'scale={self.target_width}:-1:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2'
                        '-y', output_name]
                print(" ".join(ffmpeg_cmd))
                subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
                return_video_list.append(output_name)

            else:
                # 当前文件是视频文件
                video_duration = get_video_duration(media_file)
                video_width, video_height = get_video_info(media_file)
                output_name = generate_temp_filename(media_file, new_directory=work_output_dir)
                # 不需要拉伸也不需要裁剪，只需要调整分辨率和fps
                if video_width / video_height > self.target_width / self.target_height:
                    command = [
                        'ffmpeg',
                        '-i', media_file,  # 输入文件
                        '-r', str(self.fps),  # 设置帧率
                        '-vf',
                        f"scale=-1:{self.target_height}:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2",
                        # 设置视频滤镜来调整分辨率
                        # '-vf', f'crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                        '-y',
                        output_name  # 输出文件
                    ]
                else:
                    command = [
                        'ffmpeg',
                        '-i', media_file,  # 输入文件
                        '-r', str(self.fps),  # 设置帧率
                        '-vf',
                        f"scale={self.target_width}:-1:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2",
                        # 设置视频滤镜来调整分辨率
                        # '-vf', f'crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                        '-y',
                        output_name  # 输出文件
                    ]
                # 执行FFmpeg命令
                print(" ".join(command))
                run_ffmpeg_command(command)
                return_video_list.append(output_name)
        self.video_list = return_video_list
        return return_video_list

    def generate_video_with_bg_music(self):
        # 生成视频和音频的代码
        random_name = str(random_with_system_time())
        merge_video = os.path.join(video_output_dir, "final-" + random_name + ".mp4")
        temp_video_filelist_path = os.path.join(video_output_dir, 'generate_video_with_bg_file_list.txt')

        # 创建包含所有视频文件的文本文件
        with open(temp_video_filelist_path, 'w') as f:
            for video_file in self.video_list:
                f.write(f"file '{video_file}'\n")

        # 拼接视频
        ffmpeg_concat_cmd = ['ffmpeg',
                             '-f', 'concat',
                             '-safe', '0',
                             '-i', temp_video_filelist_path,
                             '-c', 'copy',
                             '-fflags',
                             '+genpts',
                             '-y',
                             merge_video]

        # 是否需要转场特效
        if self.enable_video_transition_effect and len(self.video_list) > 1:
            video_length_list = get_video_length_list(self.video_list)
            print("启动转场特效")
            zhuanchang_txt = gen_filter(video_length_list, None, None,
                                        self.video_transition_effect_type,
                                        self.video_transition_effect_value,
                                        self.video_transition_effect_duration,
                                        True)

            # File inputs from the list
            files_input = [['-i', f] for f in self.video_list]
            ffmpeg_concat_cmd = ['ffmpeg', *itertools.chain(*files_input),
                                 '-filter_complex', zhuanchang_txt,
                                 '-map', '[video]',
                                 '-map', '[audio]',
                                 '-y',
                                 merge_video]

        subprocess.run(ffmpeg_concat_cmd)
        # 删除临时文件
        os.remove(temp_video_filelist_path)

        # 添加背景音乐
        if self.enable_background_music:
            add_background_music(merge_video, self.background_music, self.background_music_volume)
        return merge_video
