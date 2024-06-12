# 加载JSON翻译文件
import json
import os

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

LANG = 'zh-CN'

default_file_path = os.path.join(script_dir, "../locales", 'zh-CN.json')


# 加载翻译文件
def load_translations(lang):
    file_path = os.path.join(script_dir, "../locales", f'{lang}.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        with open(default_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


# 获取翻译
def tr(key, lang=LANG):
    translations = load_translations(lang)
    return translations.get(key, key)  # 如果找不到翻译，就返回原字符串

def main():
    print(tr('test'))


if __name__ == "__main__":
    main()