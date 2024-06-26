import os
import random
import re
import string

import yaml
from PIL.Image import Image


def random_line(afile):
    lines = afile.readlines()
    return random.choice(lines)


def read_yaml(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data


def save_yaml(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)


def is_chinese(char):
    if '\u4e00' <= char <= '\u9fff':
        return True
    else:
        return False


def split_at_first_chinese_char(s):
    for i, char in enumerate(s):
        # 检查字符是否是中文字符
        if '\u4e00' <= char <= '\u9fff':  # Unicode范围大致对应于常用中文字符
            return s[:i], s[i:]
    return s, ""  # 如果没有找到中文字符，返回原字符串和一个空字符串


def add_next_line_at_first_chinese_char(s):
    for i, char in enumerate(s):
        # 检查字符是否是中文字符
        if '\u4e00' <= char <= '\u9fff':  # Unicode范围大致对应于常用中文字符
            return s[:i] + "\n" + s[i:], max(len(s[:i]), len(s[i:]))
    return s, len(s)


def insert_newline(text):
    # 创建一个正则表达式，匹配任何标点符号
    punctuations = '[' + re.escape(string.punctuation) + ']'
    # 正则表达式匹配长度为30的字符串，后面紧跟空格或标点符号
    pattern = r'(.{30})(?=' + punctuations + r'|\s)'
    # 使用 re.sub 替换匹配的部分，在匹配到的字符串后添加换行符
    return re.sub(pattern, r'\1\n', text)


def generate_temp_filename(original_filepath, new_ext="", new_directory=None):
    # 获取文件的目录、文件名和扩展名
    directory, filename_with_ext = os.path.split(original_filepath)
    filename, ext = os.path.splitext(filename_with_ext)

    # 在文件名后添加.temp，但不改变扩展名
    if new_ext:
        new_filename = filename + '.temp' + new_ext
    else:
        new_filename = filename + '.temp' + ext

    # 如果你需要完整的路径，可以使用os.path.join
    if new_directory:
        new_filepath = os.path.join(new_directory, new_filename)
    else:
        new_filepath = os.path.join(directory, new_filename)

    return new_filepath


def get_file_extension(filename):
    _, ext = os.path.splitext(filename)
    # return ext[1:]  # 去掉前面的点（.）
    return ext


import requests


def download_file_from_url(url, output_path):
    """
    从给定的URL下载文件并保存到指定的输出路径。

    参数:
    url (str): 要下载的文件的URL。
    output_path (str): 保存文件的本地路径。

    返回:
    None
    """
    try:
        # 发送GET请求到URL
        response = requests.get(url, stream=True)

        # 检查请求是否成功
        if response.status_code == 200:
            # 打开一个文件以二进制写模式
            with open(output_path, 'wb') as file:
                # 使用chunk迭代数据
                for chunk in response.iter_content(chunk_size=8192):
                    # 写入文件
                    file.write(chunk)
            print(f"文件已成功下载到 {output_path}")
        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"发生了一个错误: {e}")


def random_line_from_text_file(text_file):
    # 从文本文件中随机读取文本
    with open(text_file, 'r', encoding='utf-8') as file:
        line = random_line(file)
        return line.strip()
