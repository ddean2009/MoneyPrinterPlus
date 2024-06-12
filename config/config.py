import os
import shutil

from tools.file_utils import read_yaml, save_yaml

languages = {'zh-CN': "简体中文", 'en': "english", 'zh-TW': "繁體中文"}
audio_languages = {'zh-CN': "中文", 'en-US': "english"}
audio_voices = {
    "zh-CN": {
        "zh-CN-XiaoxiaoNeural": "晓晓(女)",
        "zh-CN-YunxiNeural": "云希(男)",
        "zh-CN-YunjianNeural": "云健(男)",
        "zh-CN-XiaoyiNeural": "晓伊(女)",
        "zh-CN-YunyangNeural": "云扬(男)",
        "zh-CN-XiaochenNeural": "晓晨(女)",
        "zh-CN-XiaohanNeural": "晓涵(女)",
        "zh-CN-XiaomengNeural": "晓萌(女)",
        "zh-CN-XiaomoNeural": "晓墨(女)",
        "zh-CN-XiaoqiuNeural": "晓秋(女)",
        "zh-CN-XiaoruiNeural": "晓睿(女)",
        "zh-CN-XiaoshuangNeural": "晓双(女,儿童)",
        "zh-CN-XiaoyanNeural": "晓颜(女)",
        "zh-CN-XiaoyouNeural": "晓悠(女,儿童)",
        "zh-CN-XiaozhenNeura": "晓珍(女)",
        "zh-CN-YunfengNeural": "云峰(男)",
        "zh-CN-YunhaoNeural": "云浩(男)",
        "zh-CN-YunxiaNeural": "云夏(男)",
        "zh-CN-YunyeNeural": "云野(男)",
        "zh-CN-YunzeNeural": "云泽(男)",
        "zh-CN-XiaochenMultilingualNeural": "晓晨(女),多语言",
        "zh-CN-XiaorouNeural": "晓蓉(女)",
        "zh-CN-XiaoxiaoDialectsNeural": "晓晓(女),方言",
        "zh-CN-XiaoxiaoMultilingualNeural": "晓晓(女),多语言",
        "zh-CN-XiaoyuMultilingualNeural": "晓雨(女),多语言",
        "zh-CN-YunjieNeural": "云杰(男)",
        "zh-CN-YunyiMultilingualNeural": "云逸(男),多语言"
    },
    "en-US": {
        "en-US-AvaMultilingualNeural": "Ava(female)",
        "en-US-AndrewNeural": "Andrew(male)",
        "en-US-EmmaNeural": "Emma(female)",
        "en-US-BrianNeural": "Brian(male)",
        "en-US-JennyNeural": "Jenny(female)",
        "en-US-GuyNeural": "Guy(male)",
        "en-US-AriaNeural": "Aria(female)",
        "en-US-DavisNeural": "Davis(male)",
        "en-US-JaneNeural": "Jane(female)",
        "en-US-JasonNeural": "Jason(male)",
        "en-US-SaraNeural": "Sara(female)",
        "en-US-TonyNeural": "Tony(male)",
        "en-US-NancyNeural": "Nancy(female)",
        "en-US-AmberNeural": "Amber(female)",
        "en-US-AnaNeural": "Ana(female),child",
        "en-US-AshleyNeural": "Ashley(female)",
        "en-US-BrandonNeural": "Brandon(male)",
        "en-US-ChristopherNeural": "Christopher(male)",
        "en-US-CoraNeural": "Cora(female)",
        "en-US-ElizabethNeural": "Elizabeth(female)",
        "en-US-EricNeural": "Eric(male)",
        "en-US-JacobNeural": "Jacob(male)",
        "en-US-JennyMultilingualNeural": "Jenny(female),multilingual",
        "en-US-MichelleNeural": "Michelle(female)",
        "en-US-MonicaNeural": "Monica(female)",
        "en-US-RogerNeural": "Roger(male)",
        "en-US-RyanMultilingualNeural": "Ryan(male),multilingual",
        "en-US-SteffanNeural": "Steffan(male)",
        "en-US-AndrewMultilingualNeura": "Andrew(male),multilingual",
        "en-US-BlueNeural": "Blue(neural)",
        "en-US-BrianMultilingualNeural": "Brian(male),multilingual",
        "en-US-EmmaMultilingualNeural": "Emma(female),multilingual",
        "en-US-AlloyMultilingualNeural": "Alloy(male),multilingual",
        "en-US-EchoMultilingualNeural": "Echo(male),multilingual",
        "en-US-FableMultilingualNeural": "Fable(neural),multilingual",
        "en-US-OnyxMultilingualNeural": "Onyx(male),multilingual",
        "en-US-NovaMultilingualNeural": "Nova(female),multilingual",
        "en-US-ShimmerMultilingualNeural": "Shimmer(female),multilingual",
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
