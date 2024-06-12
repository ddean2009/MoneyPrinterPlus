from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI

from config.config import my_config
from services.llm.llm_service import MyLLMService
from tools.utils import must_have_value

# 设置 Azure OpenAI API 密钥和服务区域
AZURE_OPENAI_API_KEY = my_config['llm']['Azure']['api_key']  # 替换为您的 Azure OpenAI API 密钥
AZURE_OPENAI_API_BASE = my_config['llm']['Azure']['base_url']  # 替换为您的 Azure OpenAI API 基础 URL
AZURE_OPENAI_MODEL_NAME = my_config['llm']['Azure']['model_name']  # 替换为您的 Azure OpenAI 部署名称

must_have_value(AZURE_OPENAI_API_KEY, "请设置Azure OpenAI API 密钥")
must_have_value(AZURE_OPENAI_API_BASE, "请设置Azure OpenAI API base URL")
must_have_value(AZURE_OPENAI_MODEL_NAME, "请设置Azure OpenAI API deploy name")


class MyAzureService(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性
        print("")

    def generate_content(self, topic: str, prompt_template: PromptTemplate, language: str = None, length: str = None):
        # 创建 Azure OpenAI 的 LLM 实例
        llm = AzureChatOpenAI(
            openai_api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_API_BASE,
            openai_api_version="2023-05-15",
            deployment_name=AZURE_OPENAI_MODEL_NAME
        )

        # 创建 LLMChain
        chain = prompt_template | llm | StrOutputParser()

        # 生成视频内容描述
        description = chain.invoke({"topic": topic, "language": language, "length": length})

        return description.strip()


def main():
    topic = "AI"
    # 创建 AzureService 实例
    service = MyAzureService()
    description = service.generate_content(topic, service.topic_prompt_template)
    print(f"\n生成的视频内容描述:\n{description}")


if __name__ == "__main__":
    main()
