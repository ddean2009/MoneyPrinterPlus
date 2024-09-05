from services.llm.azure_service import MyAzureService
from services.llm.baichuan_service import MyBaichuanService
from services.llm.baidu_qianfan_service import BaiduQianfanService
from services.llm.deepseek_service import MyDeepSeekService
from services.llm.kimi_service import MyKimiService
from services.llm.ollama_service import OllamaService
from services.llm.openai_service import MyOpenAIService
from services.llm.tongyi_service import MyTongyiService


def get_llm_provider(llm_provider):
    if llm_provider == "Azure":
        return MyAzureService()
    if llm_provider == "OpenAI":
        return MyOpenAIService()
    if llm_provider == "Moonshot":
        return MyKimiService()
    if llm_provider == "Qianfan":
        return BaiduQianfanService()
    if llm_provider == "Baichuan":
        return MyBaichuanService()
    if llm_provider == "Tongyi":
        return MyTongyiService()
    if llm_provider == "DeepSeek":
        return MyDeepSeekService()
    if llm_provider == "Ollama":
        return OllamaService()
