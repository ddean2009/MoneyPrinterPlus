import os

from langchain.prompts import PromptTemplate
from langchain_community.llms.moonshot import Moonshot

from config.config import my_config
from services.llm.llm_service import MyLLMService
from tools.utils import must_have_value


class MyKimiService(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性
        self.KIMI_API_KEY = my_config['llm']['Moonshot']['api_key']  # 替换为您的 Kimi API 密钥
        self.KIMI_MODEL_NAME = my_config['llm']['Moonshot']['model_name']  # 替换为 Kimi API 的model
        must_have_value(self.KIMI_API_KEY, "请设置Kimi API 密钥")
        must_have_value(self.KIMI_MODEL_NAME, "请设置Kimi API model")

        os.environ["MOONSHOT_API_KEY"] = self.KIMI_API_KEY

    def generate_content(self, topic: str, prompt_template: PromptTemplate, language: str = None, length: str = None):
        # 创建 Kimi 的 LLM 实例
        llm = Moonshot(model=self.KIMI_MODEL_NAME)

        # 创建 LLMChain
        # chain = prompt_template | llm | StrOutputParser()

        description = llm.invoke(prompt_template.format(topic=topic, language=language, length=length))

        # 生成视频内容描述
        # description = chain.invoke({"topic": topic, "language": language, "length": length})

        return description.strip()


def main():
    kimi_service = MyKimiService()
    topic = "AI"
    description = kimi_service.generate_content(topic, kimi_service.topic_prompt_template)
    print(f"\n生成的视频内容描述:\n{description}")


if __name__ == "__main__":
    main()
