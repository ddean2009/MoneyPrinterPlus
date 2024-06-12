import os
import shutil

from tools.file_utils import read_yaml, save_yaml

languages = {'zh-CN': "简体中文", 'en': "english", 'zh-TW': "繁體中文"}
audio_languages = {'zh-CN': "中文", 'en-US': "english"}
audio_voices = {
    "zh-CN": {
        "zh-CN-XiaoxiaoNeural": "晓晓(女)",
        "zh-CN-YunxiNeural": "云希(男)",
    },
    "en-US": {
        "en-US-AvaMultilingualNeural": "Ava(female)",
    }
}

transition_types = ['xfade']
fade_list = ['fade', 'smoothleft', 'smoothright', 'smoothup', 'smoothdown', 'circlecrop', 'rectcrop', 'circleclose',
             'circleopen', 'horzclose', 'horzopen', 'vertclose',
             'vertopen', 'diagbl', 'diagbr', 'diagtl', 'diagtr', 'hlslice', 'hrslice', 'vuslice', 'vdslice', 'dissolve',
             'pixelize', 'radial', 'hblur',
             'wipetl', 'wipetr', 'wipebl', 'wipebr', 'zoomin', 'hlwind', 'hrwind', 'vuwind', 'vdwind', 'coverleft',
             'coverright', 'covertop', 'coverbottom', 'revealleft', 'revealright', 'revealup', 'revealdown']

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

config_example_file_name = "config.example.yml"
config_file_name = "config.yml"

config_example_file = os.path.join(script_dir, config_example_file_name)
config_file = os.path.join(script_dir, config_file_name)


def load_config():
    # 加载配置文件
    if not os.path.exists(config_file):
        shutil.copy(config_example_file, config_file)
    if os.path.exists(config_file):
        return read_yaml(config_file)


def save_config():
    # 保存配置文件
    if os.path.exists(config_file):
        save_yaml(config_file, my_config)


my_config = load_config()
