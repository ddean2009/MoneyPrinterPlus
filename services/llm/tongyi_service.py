# 设置 tongyi API 的基础 URL 和 API 密钥
import os

from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

from config.config import my_config
from services.llm.llm_service import MyLLMService
from tools.utils import must_have_value


class MyTongyiService(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性
        # DASHSCOPE_API_KEY = getpass()
        self.TONGYI_API_KEY = my_config['llm']['Tongyi']['api_key']  # 替换为您的 tongyi API 密钥
        self.TONGYI_MODEL_NAME = my_config['llm']['Tongyi']['model_name']  # 替换为 tongyi API 的model
        must_have_value(self.TONGYI_API_KEY, "请设置tongyi API 密钥")
        must_have_value(self.TONGYI_MODEL_NAME, "请设置tongyi API model")
        os.environ["DASHSCOPE_API_KEY"] = self.TONGYI_API_KEY

    def generate_content(self, topic: str, prompt_template: PromptTemplate, language: str = None, length: str = None):
        # 创建 Kimi 的 LLM 实例
        llm = Tongyi(model=self.TONGYI_MODEL_NAME)

        description = llm.invoke(prompt_template.format(topic=topic, language=language, length=length))

        return description.strip()
