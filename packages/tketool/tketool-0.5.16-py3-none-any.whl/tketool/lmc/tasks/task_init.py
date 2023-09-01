from tketool.JConfig import get_config_instance
from tketool.lmc.models import *
from langchain.llms import OpenAI
import os


def get_init_llm():
    llm_type = get_config_instance().get_config("llm_type", "chatgpt")

    if llm_type == "chatgpt":
        model_name = get_config_instance().get_config("model_name", "gpt-4")
        proxys = get_config_instance().get_config("openai_proxy", "not_set")
        api_token = get_config_instance().get_config("openai_token", "not_set")
        temperature = get_config_instance().get_config("openai_temperature", "0.8")

        os.environ["OPENAI_API_KEY"] = api_token
        os.environ['OPENAI_API_PROXY'] = proxys

        return OpenAI(temperature=float(temperature), model_name=model_name)

    if llm_type == "glm":
        model_url = get_config_instance().get_config("glm_url", "not_set")
        return ChatGLM(model_url)
