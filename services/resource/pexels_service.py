from typing import List, Tuple, Any

import requests
import os

from config.config import my_config
from const.video_const import Orientation
from services.resource.resource_service import ResourceService
from tools.utils import must_have_value

# Pexels API密钥
API_KEY = my_config['resource']['pexels']['api_key']

must_have_value(API_KEY, "请设置pexels密钥")

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

# workdir
workdir = os.path.join(script_dir, "../../work")
workdir = os.path.abspath(workdir)

# 设置请求头
headers = {
    'Authorization': API_KEY
}


def download_video(video_url, save_path):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video downloaded successfully: {save_path}")
    else:
        print(f"Failed to download video: {response.status_code}")


def search_videos(query, orientation: Orientation, per_page=10):
    url = f'https://api.pexels.com/videos/search?query={query}&orientation={orientation.value}&per_page={per_page}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


class PexelsService(ResourceService):
    def __init__(self):
        super().__init__()

    def match_videos(self, video_data, audio_length,
                     exact_match=False) -> tuple[list[Any], int | Any]:
        matching_videos = []
        total_length = 0
        if video_data and 'videos' in video_data:
            i = 0
            for video in video_data['videos']:

                video_duration = video['duration']
                # 排除短的视频
                if video_duration < self.video_segment_min_length:
                    continue
                if video_duration > self.video_segment_max_length:
                    video_duration = self.video_segment_max_length

                print("total length:", total_length, "audio length:", audio_length)
                if total_length < audio_length:
                    video_files = video["video_files"]
                    for video_file in video_files:
                        # fps转换
                        # video_fps = video_file["fps"]
                        # video_duration = video_duration * video_fps / self.fps
                        # if video_duration > self.video_segment_max_length:
                        #     video_duration = self.video_segment_max_length
                        if exact_match:
                            if video_file["width"] == self.width and video_file["height"] == self.height:
                                video_url = video_file['link']
                                print("match:", video_file)
                                # total_length = total_length + video_duration
                                if self.enable_video_transition_effect:
                                    if i == 0:
                                        total_length = total_length + video_duration
                                    else:
                                        total_length = total_length + video_duration - float(self.video_transition_effect_duration)
                                matching_videos.append(video_url)
                                i = i + 1
                                break
                        else:
                            if video_file["width"] >= self.width and video_file["height"] >= self.height:
                                video_url = video_file['link']
                                print("match:", video_file)
                                # total_length = total_length + video_duration
                                if self.enable_video_transition_effect:
                                    if i == 0:
                                        total_length = total_length + video_duration
                                    else:
                                        total_length = total_length + video_duration - float(self.video_transition_effect_duration)
                                matching_videos.append(video_url)
                                i = i + 1
                                break
                else:
                    break
        return matching_videos, total_length

    def handle_video_resource(self, query, audio_length, per_page=10, exact_match=False):
        video_data = search_videos(query, self.orientation, per_page)
        # print(video_data)

        matching_videos, total_length = self.match_videos(video_data, audio_length, exact_match)
        return_videos = []
        if matching_videos:
            for video_url in matching_videos:
                video_name = video_url.split('/')[-1]
                save_name = os.path.join(workdir, f"pexels-{video_name}")
                # if not os.path.exists(save_name):
                print("download video")
                download_video(video_url, save_name)
                return_videos.append(save_name)
        else:
            print("No videos found.")
        return return_videos, total_length


def main():
    query = input("Enter search keyword: ")
    resource_service = PexelsService()
    resource_service.handle_video_resource(query, 100,  1080, False)


if __name__ == "__main__":
    main()
