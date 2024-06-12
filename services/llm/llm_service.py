from abc import ABC, abstractmethod

from langchain_core.prompts import PromptTemplate


class MyLLMService(ABC):
    def __init__(self):
        self.topic_template = "请为以下视频主题生成一个详细的适合生成视频字幕的视频内容文案,内容在{length}字以内：\n\n视频主题: {topic}\n\n返回内容用{language}表示"
        self.topic_prompt_template = PromptTemplate(
            input_variables=["topic", "language", "length"],
            template=self.topic_template
        )

        self.keyword_template = "请分析下面内容,然后提取出1-5个简短的关键词,关键词用英文表示,用逗号分割：\n\n内容: {topic}\n\n英文关键词:"
        self.keyword_prompt_template = PromptTemplate(
            input_variables=["topic"],
            template=self.keyword_template
        )

    @abstractmethod
    def generate_content(self, topic: str, language: str, length: str, prompt_template: PromptTemplate) -> str:
        """
        Generate a video description for the given topic.
        :param length:
        :param language:
        :param prompt_template:
        :param topic: The topic for which to generate a video description.
        :return: A string containing the video description.
        """
        raise NotImplementedError
