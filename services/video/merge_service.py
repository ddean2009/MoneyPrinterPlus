import os
import random

from services.hunjian.hunjian_service import get_session_video_scene_text, get_video_scene_text_list


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
