import os
from typing import List, Optional, Any

import requests
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms.moonshot import Moonshot
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import LLMResult

from config.config import my_config
from services.llm.llm_service import MyLLMService
from tools.utils import must_have_value

# 设置 Kimi API 的基础 URL 和 API 密钥
KIMI_API_KEY = my_config['llm']['Moonshot']['api_key']  # 替换为您的 Kimi API 密钥
KIMI_API_BASE_URL = my_config['llm']['Moonshot']['base_url']  # 替换为 Kimi API 的基础 URL

must_have_value(KIMI_API_KEY, "请设置Kimi API 密钥")
# must_have_value(KIMI_API_BASE_URL, "请设置Kimi API base URL")


class MyKimiService(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性
        os.environ["MOONSHOT_API_KEY"] = KIMI_API_KEY

    def generate_content(self, topic: str, language: str, length: str, prompt_template: PromptTemplate):
        # 创建 Kimi 的 LLM 实例
        llm = Moonshot(model="moonshot-v1-8k")

        # 创建 LLMChain
        chain = prompt_template | llm | StrOutputParser()

        # 生成视频内容描述
        description = chain.invoke({"topic": topic, "language": language, "length": length})

        return description.strip()


def main():
    kimi_service = MyKimiService()
    topic = "AI"
    description = kimi_service.generate_content(topic, kimi_service.topic_prompt_template)
    print(f"\n生成的视频内容描述:\n{description}")


if __name__ == "__main__":
    main()
