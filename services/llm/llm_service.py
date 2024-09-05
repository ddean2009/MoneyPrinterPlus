from abc import ABC, abstractmethod

from langchain_core.prompts import PromptTemplate


class MyLLMService(ABC):
    def __init__(self):
        self.topic_template = "请为以下主题扩展为详细的一篇文章,内容在{length}字以内,\n\n主题: {topic}\n\n返回内容用{language}表示"
        self.topic_prompt_template = PromptTemplate(
            input_variables=["topic", "language", "length"],
            template=self.topic_template
        )

        # self.keyword_template = "请分析下面内容,然后提取出1-5个简短的英文关键词,关键词用英文表示,用逗号分割,不需要序号：\n\n内容: {topic}\n\n"
        self.keyword_template = "Please analyze the following content in english, and then extract 1-5 short English keywords,keywords separated by commas, do not need serial number,return the keyword only：\n\ncontent: {topic}\n\n"
        self.keyword_prompt_template = PromptTemplate(
            input_variables=["topic"],
            template=self.keyword_template
        )

        self.sd_template = """
        任务：将以下句子转换成Stable Diffusion图像生成模型能够理解的prompt。
示例句子：
- "一只坐在草地上的小猫。"
- "未来城市风光，高耸的摩天大楼和飞行汽车。"

转换指南：
1. 确定句子中的主要对象和场景。
2. 提取描述性形容词和环境细节。
3. 考虑图像的构图和视角。
4. 使用逗号或空格分隔不同的元素和特征。
5. 确保prompt简洁明了，避免冗余。
6. 使用英文输出。

期望输出：
- "A fluffy kitten, sitting on the grass in the early morning, the sun shining through the leaves。"
- "Futuristic cityscapes with towering skyscrapers, busy flying cars, flashing neon lights and stars in the night sky。"

请根据上述指南，将以下句子转换成Stable Diffusion的prompt：
{topic}
        """
        self.sd_prompt_template = PromptTemplate(
            input_variables=["topic"],
            template=self.sd_template
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
