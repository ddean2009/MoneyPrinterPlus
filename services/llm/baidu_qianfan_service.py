import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from config.config import my_config
from services.llm.llm_service import MyLLMService
from langchain_community.llms import QianfanLLMEndpoint

from tools.utils import must_have_value


class BaiduQianfanService(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性
        self.QIANFAN_AK = my_config['llm']['Qianfan']['api_key']
        self.QIANFAN_SK = my_config['llm']['Qianfan']['secret_key']
        self.QIANFAN_MODEL_NAME = my_config['llm']['Qianfan']['model_name']
        must_have_value(self.QIANFAN_AK, "请设置qianfan AK")
        must_have_value(self.QIANFAN_SK, "请设置qianfan SK")
        must_have_value(self.QIANFAN_MODEL_NAME, "请设置qianfan model")
        os.environ["QIANFAN_AK"] = self.QIANFAN_AK
        os.environ["QIANFAN_SK"] = self.QIANFAN_SK

    def generate_content(self, topic: str, prompt_template: PromptTemplate, language: str = None, length: str = None):
        # 创建 qianfan 的 LLM 实例
        llm = QianfanLLMEndpoint(
            streaming=True,
            model=self.QIANFAN_MODEL_NAME,
        )

        # 生成视频内容描述
        description = llm.invoke(prompt_template.format(topic=topic, language=language, length=length))

        return description.strip()
