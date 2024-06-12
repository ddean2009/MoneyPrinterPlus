# 原始文件名
input_filename = 'tangshi.txt'
# 新文件名，或者覆盖原始文件
output_filename = 'tangshi_linux.txt'

# 读取原始文件的内容
with open(input_filename, 'r', encoding='utf-8') as file:
    content = file.read()

# 将Windows换行符\r\n替换为Linux换行符\n
content = content.replace('\r\n', '\n')

# 写入到新文件或覆盖原始文件
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(content)