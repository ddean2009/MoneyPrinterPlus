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
