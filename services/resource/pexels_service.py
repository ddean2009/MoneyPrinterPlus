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

from typing import List, Tuple, Any

import requests
import os

from config.config import my_config
from const.video_const import Orientation
from services.resource.resource_service import ResourceService
from tools.utils import must_have_value

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

# workdir
workdir = os.path.join(script_dir, "../../resource")
workdir = os.path.abspath(workdir)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
}


def download_video(video_url, save_path):
    response = requests.get(video_url, headers=HEADERS, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video downloaded successfully: {save_path}")
    else:
        print(f"Failed to download video: {response.status_code}")


class PexelsService(ResourceService):
    def __init__(self):
        super().__init__()
        self.API_KEY = my_config['resource']['pexels']['api_key']
        must_have_value(self.API_KEY, "请设置pexels密钥")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            'Authorization': self.API_KEY
        }

    def match_videos(self, video_data, audio_length,
                     exact_match=False) -> tuple[list[Any], int | Any]:
        # print(video_data)
        matching_videos = []
        total_length = 0
        if video_data and 'videos' in video_data:
            i = 0
            for video in video_data['videos']:

                video_duration = video['duration']
                print('video_duration:', video_duration)
                # 排除短的视频
                if video_duration < self.video_segment_min_length:
                    continue
                if video_duration > self.video_segment_max_length:
                    video_duration = self.video_segment_max_length

                print("total length:", total_length, "audio length:", audio_length)
                if total_length < audio_length:
                    video_files = video["video_files"]
                    for video_file in video_files:
                        if exact_match:
                            if video_file["width"] == self.width and video_file["height"] == self.height:
                                video_url = video_file['link']
                                print("exact match:", video_file)
                                # total_length = total_length + video_duration
                                if self.enable_video_transition_effect:
                                    if i == 0:
                                        total_length = total_length + video_duration
                                    else:
                                        total_length = total_length + video_duration - float(
                                            self.video_transition_effect_duration)
                                else:
                                    total_length = total_length + video_duration
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
                                        total_length = total_length + video_duration - float(
                                            self.video_transition_effect_duration)
                                else:
                                    total_length = total_length + video_duration
                                matching_videos.append(video_url)
                                i = i + 1
                                break
                else:
                    break
        return matching_videos, total_length

    def search_videos(self, query, orientation: Orientation, per_page=10):
        url = f'https://api.pexels.com/videos/search?query={query}&orientation={orientation.value}&per_page={per_page}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def handle_video_resource(self, query, audio_length, per_page=10, exact_match=False):
        video_data = self.search_videos(query, self.orientation, per_page)
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
    resource_service.handle_video_resource(query, 100, 1080, False)


if __name__ == "__main__":
    main()
