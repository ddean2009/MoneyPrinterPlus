from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from config.config import my_config
from services.llm.llm_service import MyLLMService
from tools.utils import must_have_value


class OllamaService(MyLLMService):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数来初始化父类的属性
        self.OLLAMA_API_BASE = my_config['llm']['Ollama']['base_url']  # 替换为您的 Ollama 基础 URL
        self.OLLAMA_MODEL_NAME = my_config['llm']['Ollama']['model_name']  # 替换为您的 Ollama model name
        must_have_value(self.OLLAMA_API_BASE, "请设置Ollama base URL")
        must_have_value(self.OLLAMA_MODEL_NAME, "请设置Ollama model name")

        print("")

    def generate_content(self, topic: str, prompt_template: PromptTemplate, language: str = None, length: str = None):
        # 创建 Ollama 的 LLM 实例
        llm = ChatOllama(
            base_url=self.OLLAMA_API_BASE,
            model=self.OLLAMA_MODEL_NAME
        )

        # 创建 LLMChain
        chain = prompt_template | llm | StrOutputParser()

        # 生成视频内容描述
        description = chain.invoke({"topic": topic, "language": language, "length": length})

        return description.strip()


def main():
    topic = "AI"
    # 创建 OllamaService 实例
    service = OllamaService()
    description = service.generate_content(topic, service.topic_prompt_template)
    print(f"\n生成的视频内容描述:\n{description}")


if __name__ == "__main__":
    main()
