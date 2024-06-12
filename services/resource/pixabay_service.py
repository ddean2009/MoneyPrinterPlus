import requests
import os

from config.config import my_config
from tools.utils import must_have_value

# Pixabay API密钥
API_KEY = my_config['resource']['pixabay']['api_key']

must_have_value(API_KEY, "请设置pixabay密钥")

def search_videos(query, per_page=1):
    url = f'https://pixabay.com/api/videos/?key={API_KEY}&q={query}&per_page={per_page}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def download_video(video_url, save_path):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video downloaded successfully: {save_path}")
    else:
        print(f"Failed to download video: {response.status_code}")

def main():
    query = input("Enter search keyword: ")
    video_data = search_videos(query, per_page=1)

    if video_data and 'hits' in video_data and len(video_data['hits']) > 0:
        video = video_data['hits'][0]  # 下载第一个视频
        video_url = video['videos']['medium']['url']
        video_id = video['id']

        save_path = os.path.join(os.getcwd(), f"video_{video_id}.mp4")
        download_video(video_url, save_path)
    else:
        print("No videos found.")

if __name__ == "__main__":
    main()
