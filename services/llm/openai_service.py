import openai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from config.config import my_config
from services.llm.llm_service import MyLLMService
from tools.utils import must_have_value

# 设置OpenAI API密钥
OPENAI_API_KEY = my_config['llm']['OpenAI']['api_key']

must_have_value(OPENAI_API_KEY, "请设置openAI 密钥")


class MyOpenAIService(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性

    def generate_content(self, topic: str, language: str, length: str, prompt_template: PromptTemplate):
        # 创建 OpenAI 的 LLM 实例
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
        )

        # 创建 LLMChain
        chain = prompt_template | llm | StrOutputParser()

        # 生成视频内容描述
        description = chain.invoke({"topic": topic, "language": language, "length": length})

        return description.strip()


def main():
    topic = "AI"
    openai_service = MyOpenAIService()
    description = openai_service.generate_content(topic, openai_service.topic_prompt_template)
    print(f"\n生成的视频内容描述:\n{description}")


if __name__ == "__main__":
    main()
