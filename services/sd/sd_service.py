from config.config import my_config
from services.llm.llm_provider import get_llm_provider
from services.sd import webuiapi
from tools.file_utils import split_text
from tools.utils import must_have_value
import streamlit as st

text_min_length = 10


class SDService:
    def __init__(self):
        self.base_url = my_config['resource'].get('stableDiffusion', {}).get("server_address", "")
        must_have_value(self.base_url, "请设置Stable diffusion的地址")
        self.user_name = my_config['resource'].get('stableDiffusion', {}).get("user_name", "")
        self.password = my_config['resource'].get('stableDiffusion', {}).get("password", "")
        if self.user_name is not None and self.password is not None and self.user_name != "" and self.password != "":
            self.api = webuiapi.WebUIApi(baseurl=self.base_url, username=self.user_name, password=self.password)
        else:
            self.api = webuiapi.WebUIApi(baseurl=self.base_url)

    def sd_get_video_list(self, video_content):
        text_list = split_text(video_content)
        video_language = st.session_state.get('video_language')
        video_length = st.session_state.get('video_length')

        llm_provider = my_config['llm']['provider']
        print("llm_provider:", llm_provider)
        neg_prompt = ""
        width = st.session_state.get("sd_width")
        height = st.session_state.get("sd_height")
        sampler_name = st.session_state.get("sd_sample")
        steps = st.session_state.get("sd_step")
        scheduler = st.session_state.get("sd_schedule")
        cfg_scale = st.session_state.get("sd_cfg_scale")
        seed = st.session_state.get("sd_seed")
        llm_service = get_llm_provider(llm_provider)
        for topic in text_list:
            sd_prompt = llm_service.generate_content(topic, llm_service.sd_prompt_template)
            sd_service = SDService()
            webuiapi_result = sd_service.text_2_img(sd_prompt, neg_prompt, int(width), int(height), steps=int(steps),
                                                    sampler_name=sampler_name,
                                                    scheduler=scheduler, cfg_scale=float(cfg_scale), seed=int(seed))
            if webuiapi_result.images is not None:
                image_file = webuiapi_result.images[0]
                print(image_file)


        pass

    def set_checkpoint(self, checkpoint_name):
        self.api.util_set_model(checkpoint_name)

    def get_checkpoints(self):
        try:
            checkpoints = self.api.util_get_model_names()
        except Exception as e:
            print(f"SD发生了一个错误: {e}")
            checkpoints = []
        return checkpoints

    def get_samples(self):
        try:
            samples = self.api.util_get_sampler_names()
        except Exception as e:
            print(f"SD发生了一个错误: {e}")
            samples = []

        return samples

    def get_schedulers(self):
        try:
            schedulers = self.api.util_get_scheduler_names()
        except Exception as e:
            print(f"SD发生了一个错误: {e}")
            schedulers = []
        return schedulers

    def text_2_img(self, prompt, negative_prompt, width, height, steps, sampler_name, scheduler, cfg_scale, seed):
        return self.api.txt2img(prompt=prompt, negative_prompt=negative_prompt,
                                width=width, height=height,
                                sampler_name=sampler_name,
                                scheduler=scheduler,
                                steps=steps, cfg_scale=cfg_scale, seed=seed)
