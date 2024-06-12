import os
import re
import string

import yaml
from PIL.Image import Image


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


def generate_temp_filename(original_filepath, new_ext=""):
    # 获取文件的目录、文件名和扩展名
    directory, filename_with_ext = os.path.split(original_filepath)
    filename, ext = os.path.splitext(filename_with_ext)

    # 在文件名后添加.temp，但不改变扩展名
    if new_ext:
        new_filename = filename + '.temp' + new_ext
    else:
        new_filename = filename + '.temp' + ext

    # 如果你需要完整的路径，可以使用os.path.join
    new_filepath = os.path.join(directory, new_filename)

    return new_filepath


def get_file_extension(filename):
    _, ext = os.path.splitext(filename)
    # return ext[1:]  # 去掉前面的点（.）
    return ext
