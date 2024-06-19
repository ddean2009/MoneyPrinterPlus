import os
import shutil

from tools.file_utils import read_yaml, save_yaml

languages = {'zh-CN': "简体中文", 'en': "english", 'zh-TW': "繁體中文"}
audio_languages = {'zh-CN': "中文", 'en-US': "english"}
audio_voices_tencent = {
    "zh-CN": {
        "1001": "智瑜(女)",
        "1002": "智聆(女)",
        "1003": "智美(女)",
        "1004": "智云(男)",
        "1005": "智莉(女)",
        "1007": "智娜(女)",
        "1008": "智琪(女)",
        "1009": "智芸(女)",
        "1010": "智华(男)",
        "1017": "智蓉(女)",
        "1018": "智靖(男)",
        "100510000": "智逍遥(男)",
        "101001": "智瑜(女)",
        "101002": "智聆(女)",
        "101003": "智美(女)",
        "101004": "智云(男)",
        "101005": "智莉(女)",
        "101006": "智言(女)",
        "101007": "智娜(女)",
        "101008": "智琪(女)",
        "101009": "智芸(女)",
        "1010010": "智华(男)",
        "1010011": "智燕(女)",
        "1010012": "智丹(女)",
        "1010013": "智辉(男)",
        "1010014": "智宁(男)",
        "1010015": "智萌(男童)",
        "1010016": "智甜(女童)",
        "1010017": "智蓉(女)",
        "1010018": "智靖(男)",
        "1010019": "智彤(粤语)",
        "1010020": "智刚(男)",
        "1010021": "智瑞(男)",
        "1010022": "智虹(女)",
        "1010023": "智萱(女)",
        "1010024": "智皓(男)",
        "1010025": "智薇(女)",
        "1010026": "智希(女)",
        "1010027": "智梅(女)",
        "1010028": "智洁(女)",
        "1010029": "智凯(男)",
        "1010030": "智柯(男)"
    },
    "en-US": {
        "1050": "WeJack(男)",
        "1051": "WeRose(女)",
        "101050": "WeJack(男)精品",
        "101051": "WeRose(女)精品"
    }
}

audio_voices_azure = {
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


audio_voices_ali = {
    "zh-CN": {
        "zhixiaobai": "知小白(普通话女声)",
        "zhixiaoxia": "知小夏(普通话女声)",
        "zhixiaomei": "知小妹(普通话女声)",
        "zhigui": "知柜(普通话女声)",
        "zhishuo": "知硕(普通话男声)",
        "aixia": "艾夏(普通话女声)",
        "xiaoyun": "小云(标准女声)",
        "xiaogang": "小刚(标准男声)",
        "ruoxi": "若兮(温柔女声)",
        "siqi": "思琪(温柔女声)",
        "sijia": "思佳(标准女声)",
        "sicheng": "思诚(标准男声)",
        "aiqi": "艾琪(温柔女声)",
        "aijia": "艾佳(标准女声)",
        "aicheng": "艾诚(标准男声)",
        "aida": "艾达(标准男声)",
        "ninger": "宁儿(标准女声)",
        "ruilin": "瑞琳(标准女声)",
        "siyue": "思悦(温柔女声)",
        "aiya": "艾雅(严厉女声)",
        "aimei": "艾美(甜美女声)",
        "aiyu": "艾雨(自然女声)",
        "aiyue": "艾悦(温柔女声)",
        "aijing": "艾静(严厉女声)",
        "xiaomei": "小美(甜美女声)",
        "aina": "艾娜(浙普女声)",
        "yina": "依娜(浙普女声)",
        "sijing": "思婧(严厉女声)",
        "sitong": "思彤(儿童音)",
        "xiaobei": "小北(萝莉女声)",
        "aitong": "艾彤(儿童音)",
        "aiwei": "艾薇(萝莉女声)",
        "aibao": "艾宝(萝莉女声)"


    },
    "en-US": {
        "zhixiaobai": "知小白(普通话女声)",
        "zhixiaoxia": "知小夏(普通话女声)",
        "zhixiaomei": "知小妹(普通话女声)",
        "zhigui": "知柜(普通话女声)",
        "zhishuo": "知硕(普通话男声)",
        "aixia": "艾夏(普通话女声)",
        "cally": "Cally(美式英文女声)",
        "xiaoyun": "小云(标准女声)",
        "xiaogang": "小刚(标准男声)",
        "ruoxi": "若兮(温柔女声)",
        "siqi": "思琪(温柔女声)",
        "sijia": "思佳(标准女声)",
        "sicheng": "思诚(标准男声)",
        "aiqi": "艾琪(温柔女声)",
        "aijia": "艾佳(标准女声)",
        "aicheng": "艾诚(标准男声)",
        "aida": "艾达(标准男声)",
        "siyue": "思悦(温柔女声)",
        "aiya": "艾雅(严厉女声)",
        "aimei": "艾美(甜美女声)",
        "aiyu": "艾雨(自然女声)",
        "aiyue": "艾悦(温柔女声)",
        "aijing": "艾静(严厉女声)",
        "xiaomei": "小美(甜美女声)",
        "harry": "Harry(英音男声)",
        "abby": "Abby(美音女声)",
        "andy": "Andy(美音男声)",
        "eric": "Eric(英音男声)",
        "emily": "Emily(英音女声)",
        "luna": "Luna(英音女声)",
        "luca": "Luca(英音男声)",
        "wendy": "Wendy(英音女声)",
        "william": "William(英音男声)",
        "olivia": "Olivia(英音女声)"
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
    print("load_config")
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
