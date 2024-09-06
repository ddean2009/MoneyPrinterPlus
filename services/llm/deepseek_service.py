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

from langchain.prompts import PromptTemplate
from openai import OpenAI

from config.config import my_config
from services.llm.llm_service import MyLLMService
from tools.utils import must_have_value


class MyDeepSeekService(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性
        self.DEEPSEEK_API_KEY = my_config['llm']['DeepSeek']['api_key']
        self.DEEPSEEK_API_URL = my_config['llm']['DeepSeek']['base_url']
        self.DEEPSEEK_MODEL_NAME = my_config['llm']['DeepSeek']['model_name']  # 替换为 DeepSeek API 的model
        must_have_value(self.DEEPSEEK_API_KEY, "请设置DeepSeek 密钥")
        must_have_value(self.DEEPSEEK_API_URL, "请设置DeepSeek Base Url")
        must_have_value(self.DEEPSEEK_MODEL_NAME, "请设置DeepSeek model")

    def generate_content(self, topic: str, prompt_template: PromptTemplate, language: str = None, length: str = None):
        # 创建 DeepSeek 的 LLM 实例
        llm = OpenAI(
            api_key=self.DEEPSEEK_API_KEY,
            base_url=self.DEEPSEEK_API_URL
        )

        response = llm.chat.completions.create(
            model=self.DEEPSEEK_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt_template.format(topic=topic, language=language, length=length)},
            ],
            stream=False
        )

        # 生成视频内容描述
        description = response.choices[0].message.content

        return description.strip()
