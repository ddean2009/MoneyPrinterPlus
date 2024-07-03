import os

from langchain.prompts import PromptTemplate
from langchain_community.llms.baichuan import BaichuanLLM

from config.config import my_config
from services.llm.llm_service import MyLLMService
from tools.utils import must_have_value


class MyBaichuanService(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性
        # 设置 baichuan API 的基础 URL 和 API 密钥
        self.BAICHUAN_API_KEY = my_config['llm']['Baichuan']['api_key']  # 替换为您的 Baichuan API 密钥
        self.BAICHUAN_MODEL_NAME = my_config['llm']['Baichuan']['model_name']  # 替换为 Baichuan API 的model
        must_have_value(self.BAICHUAN_API_KEY, "请设置Baichuan API 密钥")
        must_have_value(self.BAICHUAN_MODEL_NAME, "请设置Baichuan API model")
        os.environ["BAICHUAN_API_KEY"] = self.BAICHUAN_API_KEY

    def generate_content(self, topic: str, prompt_template: PromptTemplate, language: str = None, length: str = None):
        # 创建 baichuan 的 LLM 实例
        llm = BaichuanLLM(model=self.BAICHUAN_MODEL_NAME)

        description = llm.invoke(prompt_template.format(topic=topic, language=language, length=length))

        return description.strip()
