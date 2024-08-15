from config.config import my_config
from services.sd import webuiapi
from tools.utils import must_have_value


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

    def handle_video_resource(self, query, audio_length, per_page=10, exact_match=False):
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
