#  Copyright © [2024] 程序那些事
#
#  All rights reserved. This software and associated documentation files (the "Software") are provided for personal and educational use only. Commercial use of the Software is strictly prohibited unless explicit permission is obtained from the author.
#
#  Permission is hereby granted to any person to use, copy, and modify the Software for non-commercial purposes, provided that the following conditions are met:
#
#  1. The original copyright notice and this permission notice must be included in all copies or substantial portions of the Software.
#  2. Modifications, if any, must retain the original copyright information and must not imply that the modified version is an official version of the Software.
#  3. Any distribution of the Software or its modifications must retain the original copyright notice and include this permission notice.
#
#  For commercial use, including but not limited to selling, distributing, or using the Software as part of any commercial product or service, you must obtain explicit authorization from the author.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Author: 程序那些事
#  email: flydean@163.com
#  Website: [www.flydean.com](http://www.flydean.com)
#  GitHub: [https://github.com/ddean2009/MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus)
#
#  All rights reserved.
#
#

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
