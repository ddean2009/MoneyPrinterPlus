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

import json

import PIL
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional, Union, Literal


class Upscaler(str, Enum):
    none = "None"
    Lanczos = "Lanczos"
    Nearest = "Nearest"
    LDSR = "LDSR"
    BSRGAN = "BSRGAN"
    ESRGAN_4x = "R-ESRGAN 4x+"
    R_ESRGAN_General_4xV3 = "R-ESRGAN General 4xV3"
    ScuNET_GAN = "ScuNET GAN"
    ScuNET_PSNR = "ScuNET PSNR"
    SwinIR_4x = "SwinIR 4x"


class HiResUpscaler(str, Enum):
    none = "None"
    Latent = "Latent"
    LatentAntialiased = "Latent (antialiased)"
    LatentBicubic = "Latent (bicubic)"
    LatentBicubicAntialiased = "Latent (bicubic antialiased)"
    LatentNearest = "Latent (nearest)"
    LatentNearestExact = "Latent (nearest-exact)"
    Lanczos = "Lanczos"
    Nearest = "Nearest"
    ESRGAN_4x = "R-ESRGAN 4x+"
    LDSR = "LDSR"
    ScuNET_GAN = "ScuNET GAN"
    ScuNET_PSNR = "ScuNET PSNR"
    SwinIR_4x = "SwinIR 4x"


@dataclass
class WebUIApiResult:
    images: list
    parameters: dict
    info: dict
    json: dict

    @property
    def image(self):
        return self.images[0]


class ControlNetUnit:
    def __init__(
            self,
            image: Image = None,
            mask: Image = None,
            module: str = "none",
            model: str = "None",
            weight: float = 1.0,
            resize_mode: str = "Resize and Fill",
            low_vram: bool = False,
            processor_res: int = 512,
            threshold_a: float = 64,
            threshold_b: float = 64,
            guidance_start: float = 0.0,
            guidance_end: float = 1.0,
            control_mode: int = 0,
            pixel_perfect: bool = False,
            guessmode: int = None,  # deprecated: use control_mode
            hr_option: str = "Both",  # Both, Low res only, High res only
            enabled: bool = True,
    ):
        self.image = image
        self.mask = mask
        self.module = module
        self.model = model
        self.weight = weight
        self.resize_mode = resize_mode
        self.low_vram = low_vram
        self.processor_res = processor_res
        self.threshold_a = threshold_a
        self.threshold_b = threshold_b
        self.guidance_start = guidance_start
        self.guidance_end = guidance_end
        self.enabled = enabled
        if guessmode:
            print(
                "ControlNetUnit guessmode is deprecated. Please use control_mode instead."
            )
            control_mode = guessmode

        if control_mode == 0:
            self.control_mode = 'Balanced'
        elif control_mode == 1:
            self.control_mode = 'My prompt is more important'
        elif control_mode == 2:
            self.control_mode = 'ControlNet is more important'
        else:
            self.control_mode = control_mode

        self.pixel_perfect = pixel_perfect
        self.hr_option = hr_option

    def to_dict(self):
        return {
            "image": raw_b64_img(self.image) if self.image else "",
            "mask": raw_b64_img(self.mask) if self.mask is not None else None,
            "module": self.module,
            "model": self.model,
            "weight": self.weight,
            "resize_mode": self.resize_mode,
            "low_vram": self.low_vram,
            "processor_res": self.processor_res,
            "threshold_a": self.threshold_a,
            "threshold_b": self.threshold_b,
            "guidance_start": self.guidance_start,
            "guidance_end": self.guidance_end,
            "control_mode": self.control_mode,
            "pixel_perfect": self.pixel_perfect,
            "hr_option": self.hr_option,
            "enabled": self.enabled,
        }


class ADetailer:
    def __init__(self,
                 ad_model: str = "None",
                 ad_prompt: str = "",
                 ad_negative_prompt: str = "",
                 ad_confidence: float = 0.3,
                 ad_mask_k_largest: float = 0.0,
                 ad_mask_min_ratio: float = 0.0,
                 ad_mask_max_ratio: float = 1.0,
                 ad_dilate_erode: int = 4,
                 ad_x_offset: int = 0,
                 ad_y_offset: int = 0,
                 ad_mask_merge_invert: Literal["None", "Merge", "Merge and Invert"] = "None",
                 ad_mask_blur: int = 4,
                 ad_denoising_strength: int = 0.4,
                 ad_inpaint_only_masked: bool = True,
                 ad_inpaint_only_masked_padding: int = 32,
                 ad_use_inpaint_width_height: bool = False,
                 ad_inpaint_width: int = 512,
                 ad_inpaint_height: int = 512,
                 ad_use_steps: bool = False,
                 ad_steps: int = 28,
                 ad_use_cfg_scale: bool = False,
                 ad_cfg_scale: float = 7.0,
                 # ad_use_sampler: bool = False,
                 # ad_sampler: str = "None",
                 ad_use_noise_multiplier: bool = False,
                 ad_noise_multiplier=1.0,
                 ad_use_clip_skip: bool = False,
                 ad_clip_skip: int = 1,
                 ad_restore_face: bool = False,
                 ad_controlnet_model: str = "None",
                 ad_controlnet_module: str = "None",
                 ad_controlnet_weight: float = 1.0,
                 ad_controlnet_guidance_start: float = 0.0,
                 ad_controlnet_guidance_end: float = 1.0,
                 ):
        self.ad_model = ad_model
        self.ad_prompt = ad_prompt
        self.ad_negative_prompt = ad_negative_prompt
        self.ad_confidence = ad_confidence
        self.ad_mask_k_largest = ad_mask_k_largest
        self.ad_mask_min_ratio = ad_mask_min_ratio
        self.ad_mask_max_ratio = ad_mask_max_ratio
        self.ad_dilate_erode = ad_dilate_erode
        self.ad_x_offset = ad_x_offset
        self.ad_y_offset = ad_y_offset
        self.ad_mask_merge_invert = ad_mask_merge_invert
        self.ad_mask_blur = ad_mask_blur
        self.ad_denoising_strength = ad_denoising_strength
        self.ad_inpaint_only_masked = ad_inpaint_only_masked
        self.ad_inpaint_only_masked_padding = ad_inpaint_only_masked_padding
        self.ad_use_inpaint_width_height = ad_use_inpaint_width_height
        self.ad_inpaint_width = ad_inpaint_width
        self.ad_inpaint_height = ad_inpaint_height
        self.ad_use_steps = ad_use_steps
        self.ad_steps = ad_steps
        self.ad_use_cfg_scale = ad_use_cfg_scale
        self.ad_cfg_scale = ad_cfg_scale
        self.ad_use_noise_multiplier = ad_use_noise_multiplier
        self.ad_noise_multiplier = ad_noise_multiplier
        self.ad_use_clip_skip = ad_use_clip_skip
        self.ad_clip_skip = ad_clip_skip
        self.ad_restore_face = ad_restore_face
        self.ad_controlnet_model = ad_controlnet_model
        self.ad_controlnet_module = ad_controlnet_module
        self.ad_controlnet_weight = ad_controlnet_weight
        self.ad_controlnet_guidance_start = ad_controlnet_guidance_start
        self.ad_controlnet_guidance_end = ad_controlnet_guidance_end

    def to_dict(self):
        return {
            "ad_model": self.ad_model,
            "ad_prompt": self.ad_prompt,
            "ad_negative_prompt": self.ad_negative_prompt,
            "ad_confidence": self.ad_confidence,
            "ad_mask_k_largest": self.ad_mask_k_largest,
            "ad_mask_min_ratio": self.ad_mask_min_ratio,
            "ad_mask_max_ratio": self.ad_mask_max_ratio,
            "ad_dilate_erode": self.ad_dilate_erode,
            "ad_x_offset": self.ad_x_offset,
            "ad_y_offset": self.ad_y_offset,
            "ad_mask_merge_invert": self.ad_mask_merge_invert,
            "ad_mask_blur": self.ad_mask_blur,
            "ad_denoising_strength": self.ad_denoising_strength,
            "ad_inpaint_only_masked": self.ad_inpaint_only_masked,
            "ad_inpaint_only_masked_padding": self.ad_inpaint_only_masked_padding,
            "ad_use_inpaint_width_height": self.ad_use_inpaint_width_height,
            "ad_inpaint_width": self.ad_inpaint_width,
            "ad_inpaint_height": self.ad_inpaint_height,
            "ad_use_steps": self.ad_use_steps,
            "ad_steps": self.ad_steps,
            "ad_use_cfg_scale": self.ad_use_cfg_scale,
            "ad_cfg_scale": self.ad_cfg_scale,
            "ad_use_noise_multiplier": self.ad_use_noise_multiplier,
            "ad_noise_multiplier": self.ad_noise_multiplier,
            "ad_use_clip_skip": self.ad_use_clip_skip,
            "ad_clip_skip": self.ad_clip_skip,
            "ad_restore_face": self.ad_restore_face,
            "ad_controlnet_model": self.ad_controlnet_model,
            "ad_controlnet_module": self.ad_controlnet_module,
            "ad_controlnet_weight": self.ad_controlnet_weight,
            "ad_controlnet_guidance_start": self.ad_controlnet_guidance_start,
            "ad_controlnet_guidance_end": self.ad_controlnet_guidance_end,
        }


class AnimateDiff:
    def __init__(self,
                 model="mm_sd15_v3.safetensors",
                 enable=True,
                 video_length=0,
                 fps=8,
                 loop_number=0,  # Display loop number
                 closed_loop='R-P',  # Closed loop, 'N' | 'R-P' | 'R+P' | 'A'
                 batch_size=16,
                 stride=1,
                 overlap=-1,
                 format=['GIF'],  # 'GIF' | 'MP4' | 'PNG' | 'WEBP' | 'WEBM' | 'TXT' | 'Frame'
                 interp='Off',  # Frame interpolation, 'Off' | 'FILM'
                 interp_x=10,  # Interp X
                 video_source=None,
                 video_path='',
                 mask_path='',
                 freeinit_enable=False,
                 freeinit_filter="butterworth",
                 freeinit_ds=0.25,
                 freeinit_dt=0.25,
                 freeinit_iters=3,
                 latent_power=1,
                 latent_scale=32,
                 last_frame=None,
                 latent_power_last=1,
                 latent_scale_last=32,
                 request_id='',
                 ):
        self.model = model
        self.enable = enable
        self.video_length = video_length
        self.fps = fps
        self.loop_number = loop_number
        self.closed_loop = closed_loop
        self.batch_size = batch_size
        self.stride = stride
        self.overlap = overlap
        self.format = format
        self.interp = interp
        self.interp_x = interp_x
        self.video_source = video_source
        self.video_path = video_path
        self.mask_path = mask_path
        self.freeinit_enable = freeinit_enable
        self.freeinit_filter = freeinit_filter
        self.freeinit_ds = freeinit_ds
        self.freeinit_dt = freeinit_dt
        self.freeinit_iters = freeinit_iters
        self.latent_power = latent_power
        self.latent_scale = latent_scale
        self.last_frame = last_frame
        self.latent_power_last = latent_power_last
        self.latent_scale_last = latent_scale_last
        self.request_id = request_id

    def to_dict(self, is_img2img=False):
        infotext = {
            "model": self.model,
            "enable": self.enable,
            "video_length": self.video_length,
            "format": self.format,
            "fps": self.fps,
            "loop_number": self.loop_number,
            "closed_loop": self.closed_loop,
            "batch_size": self.batch_size,
            "stride": self.stride,
            "overlap": self.overlap,
            "interp": self.interp,
            "interp_x": self.interp_x,
            "freeinit_enable": self.freeinit_enable,
            "freeinit_filter": self.freeinit_filter,
            "freeinit_ds": self.freeinit_ds,
            "freeinit_dt": self.freeinit_dt,
            "freeinit_iters": self.freeinit_iters,
        }
        if self.request_id:
            infotext['request_id'] = self.request_id
        if self.last_frame:
            infotext['last_frame'] = self.last_frame
        if len(self.video_path) > 0:
            infotext['video_path'] = self.video_path
        if len(self.mask_path) > 0:
            infotext['mask_path'] = self.mask_path

        if is_img2img:
            infotext.update({
                "latent_power": self.latent_power,
                "latent_scale": self.latent_scale,
                "latent_power_last": self.latent_power_last,
                "latent_scale_last": self.latent_scale_last,
            })

        return infotext


class Roop:
    def __init__(self, img: PIL.Image,
                 enable: bool = True,
                 faces_index: str = "0",
                 model: str = None,
                 face_restorer_name: str = "GFPGAN",
                 face_restorer_visibility: float = 1,
                 upscaler_name: str = "R-ESRGAN 4x+",
                 upscaler_scale: float = 1,
                 upscaler_visibility: float = 1,
                 swap_in_source: bool = False,
                 swap_in_generated: bool = True):
        self.img = b64_img(img)
        self.enable = enable
        self.faces_index = faces_index
        self.model = model
        self.face_restorer_name = face_restorer_name
        self.face_restorer_visibility = face_restorer_visibility
        self.upscaler_name = upscaler_name
        self.upscaler_scale = upscaler_scale
        self.upscaler_visibility = upscaler_visibility
        self.swap_in_source = swap_in_source
        self.swap_in_generated = swap_in_generated

    def to_dict(self):
        return [
            self.img,
            self.enable,
            self.faces_index,
            self.model,
            self.face_restorer_name,
            self.face_restorer_visibility,
            self.upscaler_name,
            self.upscaler_scale,
            self.upscaler_visibility,
            self.swap_in_source,
            self.swap_in_generated]


class ReActor:
    def __init__(self,
                 img: PIL.Image,  # 0
                 enable: bool = True,  # 1 Enable ReActor
                 source_faces_index: str = "0",  # 2 Comma separated face number(s) from swap-source image
                 faces_index: str = "0",  # 3 Comma separated face number(s) for target image (result)
                 model: str = 'inswapper_128.onnx',  # None, #4 model path
                 face_restorer_name: str = "CodeFormer",  # 4 Restore Face: None; CodeFormer; GFPGAN
                 face_restorer_visibility: float = 1,  # 5 Restore visibility value
                 restore_first: bool = True,  # 7 Restore face -> Upscale
                 upscaler_name: str = "R-ESRGAN 4x+",
                 # None, # "R-ESRGAN 4x+", #8 Upscaler (type 'None' if doesn't need), see full list here: http://127.0.0.1:7860/sdapi/v1/script-info -> reactor -> sec.8
                 upscaler_scale: int = 2,  # 9 Upscaler scale value
                 upscaler_visibility: float = 1,
                 swap_in_source: bool = False,
                 swap_in_generated: bool = True,
                 console_logging_level: int = 1,  # 13 Console Log Level (0 - min, 1 - med or 2 - max)
                 gender_source: int = 0,  # 14 Gender Detection (Source) (0 - No, 1 - Female Only, 2 - Male Only)
                 gender_target: int = 0,  # 14 Gender Detection (Target) (0 - No, 1 - Female Only, 2 - Male Only)
                 save_original: bool = False,
                 codeFormer_weight: float = 0.5,
                 source_hash_check: bool = True,
                 target_hash_check: bool = False,
                 device: str = "CUDA",  # or CPU
                 mask_face: bool = True,
                 select_source: int = 0,  # IMPORTANT. MUST BE 0 or faceswap won't work
                 face_model: str = None,
                 ):
        self.img = b64_img(img)
        self.enable = enable
        self.source_faces_index = source_faces_index
        self.faces_index = faces_index
        self.model = model
        self.face_restorer_name = face_restorer_name
        self.face_restorer_visibility = face_restorer_visibility
        self.restore_first = restore_first
        self.upscaler_name = upscaler_name
        self.upscaler_scale = upscaler_scale
        self.upscaler_visibility = upscaler_visibility
        self.swap_in_source = swap_in_source
        self.swap_in_generated = swap_in_generated
        self.console_logging_level = console_logging_level
        self.gender_source = gender_source
        self.gender_target = gender_target
        self.save_original = save_original
        self.codeFormer_weight = codeFormer_weight
        self.source_hash_check = source_hash_check
        self.target_hash_check = target_hash_check
        self.device = device
        self.mask_face = mask_face
        self.select_source = select_source
        self.face_model = face_model

    def to_dict(self):
        return [
            self.img,
            self.enable,
            self.source_faces_index,
            self.faces_index,
            self.model,
            self.face_restorer_name,
            self.face_restorer_visibility,
            self.restore_first,
            self.upscaler_name,
            self.upscaler_scale,
            self.upscaler_visibility,
            self.swap_in_source,
            self.swap_in_generated,
            self.console_logging_level,
            self.gender_source,
            self.gender_target,
            self.save_original,
            self.codeFormer_weight,
            self.source_hash_check,
            self.target_hash_check,
            self.device,
            self.mask_face,
            self.select_source,
            self.face_model,
        ]


class Sag:
    def __init__(self,
                 enable: bool = True,  # 1 Enable Sag
                 scale: float = 0.75,
                 mask_threshold: float = 1.00
                 ):
        self.enable = enable
        self.scale = scale
        self.mask_threshold = mask_threshold

    def to_dict(self):
        return [
            self.enable,
            self.scale,
            self.mask_threshold,
        ]


def b64_img(image: Image) -> str:
    return "data:image/png;base64," + raw_b64_img(image)


def raw_b64_img(image: Image) -> str:
    # XXX controlnet only accepts RAW base64 without headers
    with io.BytesIO() as output_bytes:
        metadata = None
        for key, value in image.info.items():
            if isinstance(key, str) and isinstance(value, str):
                if metadata is None:
                    metadata = PngImagePlugin.PngInfo()
                metadata.add_text(key, value)
        image.save(output_bytes, format="PNG", pnginfo=metadata)

        bytes_data = output_bytes.getvalue()

    return str(base64.b64encode(bytes_data), "utf-8")


class WebUIApi:
    has_controlnet = False
    has_adetailer = False
    has_animatediff = False

    def __init__(
            self,
            host="127.0.0.1",
            port=7860,
            baseurl=None,
            sampler="Euler a",
            scheduler="automatic",
            steps=20,
            use_https=False,
            username=None,
            password=None,
    ):
        if baseurl is None:
            if use_https:
                baseurl = f"https://{host}:{port}/sdapi/v1"
            else:
                baseurl = f"http://{host}:{port}/sdapi/v1"

        self.baseurl = baseurl
        self.default_sampler = sampler
        self.default_scheduler = scheduler
        self.default_steps = steps

        self.session = requests.Session()

        if username and password:
            self.set_auth(username, password)
        else:
            self.check_extensions()

    def check_extensions(self):
        try:
            scripts = self.get_scripts()
            self.has_controlnet = "controlnet m2m" in scripts["txt2img"]
            self.has_adetailer = "adetailer" in scripts["txt2img"]
            self.has_animatediff = "animatediff" in scripts["txt2img"]

        except:
            pass

    def set_auth(self, username, password):
        self.session.auth = (username, password)
        self.check_extensions()

    def _to_api_result(self, response):
        if response.status_code != 200:
            raise RuntimeError(response.status_code, response.text)

        r = response.json()
        images = []
        if "images" in r.keys():
            images = [Image.open(io.BytesIO(base64.b64decode(i))) for i in r["images"]]
        elif "image" in r.keys():
            images = [Image.open(io.BytesIO(base64.b64decode(r["image"])))]

        info = ""
        if "info" in r.keys():
            try:
                info = json.loads(r["info"])
            except:
                info = r["info"]
        elif "html_info" in r.keys():
            info = r["html_info"]
        elif "caption" in r.keys():
            info = r["caption"]

        parameters = ""
        if "parameters" in r.keys():
            parameters = r["parameters"]

        return WebUIApiResult(images, parameters, info, r)

    async def _to_api_result_async(self, response):
        if response.status != 200:
            raise RuntimeError(response.status, await response.text())

        r = await response.json()
        images = []
        if "images" in r.keys():
            images = [Image.open(io.BytesIO(base64.b64decode(i))) for i in r["images"]]
        elif "image" in r.keys():
            images = [Image.open(io.BytesIO(base64.b64decode(r["image"])))]

        info = ""
        if "info" in r.keys():
            try:
                info = json.loads(r["info"])
            except:
                info = r["info"]
        elif "html_info" in r.keys():
            info = r["html_info"]
        elif "caption" in r.keys():
            info = r["caption"]

        parameters = ""
        if "parameters" in r.keys():
            parameters = r["parameters"]

        return WebUIApiResult(images, parameters, info, r)

    def txt2img(
            self,
            enable_hr=False,
            denoising_strength=0.7,
            firstphase_width=0,
            firstphase_height=0,
            hr_scale=2,
            hr_upscaler=HiResUpscaler.Latent,
            hr_second_pass_steps=0,
            hr_resize_x=0,
            hr_resize_y=0,
            prompt="",
            styles=[],
            seed=-1,
            subseed=-1,
            subseed_strength=0.0,
            seed_resize_from_h=0,
            seed_resize_from_w=0,
            sampler_name=None,  # use this instead of sampler_index
            scheduler=None,
            batch_size=1,
            n_iter=1,
            steps=None,
            cfg_scale=7.0,
            width=512,
            height=512,
            restore_faces=False,
            tiling=False,
            do_not_save_samples=False,
            do_not_save_grid=False,
            negative_prompt="",
            eta=1.0,
            s_churn=0,
            s_tmax=0,
            s_tmin=0,
            s_noise=1,
            override_settings={},
            override_settings_restore_afterwards=True,
            script_args=None,  # List of arguments for the script "script_name"
            script_name=None,
            send_images=True,
            save_images=False,
            alwayson_scripts={},
            controlnet_units: List[ControlNetUnit] = [],
            adetailer: List[ADetailer] = [],
            animatediff: AnimateDiff = None,
            roop: Roop = None,
            reactor: ReActor = None,
            sag: Sag = None,
            sampler_index=None,  # deprecated: use sampler_name
            use_deprecated_controlnet=False,
            use_async=False,
    ):
        if sampler_index is None:
            sampler_index = self.default_sampler
        if sampler_name is None:
            sampler_name = self.default_sampler

        if scheduler is None:
            scheduler = self.default_scheduler

        if steps is None:
            steps = self.default_steps
        if script_args is None:
            script_args = []
        payload = {
            "enable_hr": enable_hr,
            "hr_scale": hr_scale,
            "hr_upscaler": hr_upscaler,
            "hr_second_pass_steps": hr_second_pass_steps,
            "hr_resize_x": hr_resize_x,
            "hr_resize_y": hr_resize_y,
            "denoising_strength": denoising_strength,
            "firstphase_width": firstphase_width,
            "firstphase_height": firstphase_height,
            "prompt": prompt,
            "styles": styles,
            "seed": seed,
            "subseed": subseed,
            "subseed_strength": subseed_strength,
            "seed_resize_from_h": seed_resize_from_h,
            "seed_resize_from_w": seed_resize_from_w,
            "batch_size": batch_size,
            "n_iter": n_iter,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": width,
            "height": height,
            "restore_faces": restore_faces,
            "tiling": tiling,
            "do_not_save_samples": do_not_save_samples,
            "do_not_save_grid": do_not_save_grid,
            "negative_prompt": negative_prompt,
            "eta": eta,
            "s_churn": s_churn,
            "s_tmax": s_tmax,
            "s_tmin": s_tmin,
            "s_noise": s_noise,
            "override_settings": override_settings,
            "override_settings_restore_afterwards": override_settings_restore_afterwards,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
            "sampler_index": sampler_index,
            "script_name": script_name,
            "script_args": script_args,
            "send_images": send_images,
            "save_images": save_images,
            "alwayson_scripts": alwayson_scripts,
        }

        if use_deprecated_controlnet and controlnet_units and len(controlnet_units) > 0:
            payload["controlnet_units"] = [x.to_dict() for x in controlnet_units]
            return self.custom_post(
                "controlnet/txt2img", payload=payload, use_async=use_async
            )

        if adetailer and len(adetailer) > 0:
            ads = [True]
            for x in adetailer:
                ads.append(x.to_dict())
            payload["alwayson_scripts"]["ADetailer"] = {
                "args": ads
            }
        elif self.has_adetailer:
            payload["alwayson_scripts"]["ADetailer"] = {
                "args": [False]
            }

        if animatediff:
            payload["alwayson_scripts"]["animatediff"] = {
                "args": [animatediff.to_dict(False)]
            }
        elif self.has_animatediff:
            payload["alwayson_scripts"]["animatediff"] = {
                "args": [False],
            }

        if roop:
            payload["alwayson_scripts"]["roop"] = {
                "args": roop.to_dict()
            }

        if reactor:
            payload["alwayson_scripts"]["reactor"] = {
                "args": reactor.to_dict()
            }

        if sag:
            payload["alwayson_scripts"]["Self Attention Guidance"] = {
                "args": sag.to_dict()
            }

        if controlnet_units and len(controlnet_units) > 0:
            payload["alwayson_scripts"]["ControlNet"] = {
                "args": [x.to_dict() for x in controlnet_units]
            }
        elif self.has_controlnet:
            # workaround : if not passed, webui will use previous args!
            payload["alwayson_scripts"]["ControlNet"] = {"args": []}

        return self.post_and_get_api_result(
            f"{self.baseurl}/txt2img", payload, use_async
        )

    def post_and_get_api_result(self, url, json, use_async):
        if use_async:
            import asyncio

            return asyncio.ensure_future(self.async_post(url=url, json=json))
        else:
            response = self.session.post(url=url, json=json)
            return self._to_api_result(response)

    async def async_post(self, url, json):
        import aiohttp

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout()) as session:
            infinite_timeout = aiohttp.ClientTimeout(total=None)
            auth = aiohttp.BasicAuth(self.session.auth[0], self.session.auth[1]) if self.session.auth else None
            async with session.post(url, json=json, auth=auth,
                                    timeout=infinite_timeout) as response:  # infinite_timeout timeout here for timeout fix
                return await self._to_api_result_async(response)

    def img2img(
            self,
            images=[],  # list of PIL Image
            resize_mode=0,
            denoising_strength=0.75,
            image_cfg_scale=1.5,
            mask_image=None,  # PIL Image mask
            mask_blur=4,
            inpainting_fill=0,
            inpaint_full_res=True,
            inpaint_full_res_padding=0,
            inpainting_mask_invert=0,
            initial_noise_multiplier=1,
            prompt="",
            styles=[],
            seed=-1,
            subseed=-1,
            subseed_strength=0,
            seed_resize_from_h=0,
            seed_resize_from_w=0,
            sampler_name=None,  # use this instead of sampler_index
            scheduler=None,
            batch_size=1,
            n_iter=1,
            steps=None,
            cfg_scale=7.0,
            width=512,
            height=512,
            restore_faces=False,
            tiling=False,
            do_not_save_samples=False,
            do_not_save_grid=False,
            negative_prompt="",
            eta=1.0,
            s_churn=0,
            s_tmax=0,
            s_tmin=0,
            s_noise=1,
            override_settings={},
            override_settings_restore_afterwards=True,
            script_args=None,  # List of arguments for the script "script_name"
            sampler_index=None,  # deprecated: use sampler_name
            include_init_images=False,
            script_name=None,
            send_images=True,
            save_images=False,
            alwayson_scripts={},
            controlnet_units: List[ControlNetUnit] = [],
            adetailer: List[ADetailer] = [],
            animatediff: AnimateDiff = None,
            roop: Roop = None,
            reactor: ReActor = None,
            sag: Sag = None,
            use_deprecated_controlnet=False,
            use_async=False,
    ):
        if sampler_name is None:
            sampler_name = self.default_sampler
        if sampler_index is None:
            sampler_index = self.default_sampler
        if scheduler is None:
            scheduler = self.default_scheduler
        if steps is None:
            steps = self.default_steps
        if script_args is None:
            script_args = []

        payload = {
            "init_images": [b64_img(x) for x in images],
            "resize_mode": resize_mode,
            "denoising_strength": denoising_strength,
            "mask_blur": mask_blur,
            "inpainting_fill": inpainting_fill,
            "inpaint_full_res": inpaint_full_res,
            "inpaint_full_res_padding": inpaint_full_res_padding,
            "inpainting_mask_invert": inpainting_mask_invert,
            "initial_noise_multiplier": initial_noise_multiplier,
            "prompt": prompt,
            "styles": styles,
            "seed": seed,
            "subseed": subseed,
            "subseed_strength": subseed_strength,
            "seed_resize_from_h": seed_resize_from_h,
            "seed_resize_from_w": seed_resize_from_w,
            "batch_size": batch_size,
            "n_iter": n_iter,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "image_cfg_scale": image_cfg_scale,
            "width": width,
            "height": height,
            "restore_faces": restore_faces,
            "tiling": tiling,
            "do_not_save_samples": do_not_save_samples,
            "do_not_save_grid": do_not_save_grid,
            "negative_prompt": negative_prompt,
            "eta": eta,
            "s_churn": s_churn,
            "s_tmax": s_tmax,
            "s_tmin": s_tmin,
            "s_noise": s_noise,
            "override_settings": override_settings,
            "override_settings_restore_afterwards": override_settings_restore_afterwards,
            "sampler_name": sampler_name,
            "scheduler": scheduler,
            "sampler_index": sampler_index,
            "include_init_images": include_init_images,
            "script_name": script_name,
            "script_args": script_args,
            "send_images": send_images,
            "save_images": save_images,
            "alwayson_scripts": alwayson_scripts,
        }
        if mask_image is not None:
            payload["mask"] = b64_img(mask_image)

        if use_deprecated_controlnet and controlnet_units and len(controlnet_units) > 0:
            payload["controlnet_units"] = [x.to_dict() for x in controlnet_units]
            return self.custom_post(
                "controlnet/img2img", payload=payload, use_async=use_async
            )

        if adetailer and len(adetailer) > 0:
            ads = [True]
            for x in adetailer:
                ads.append(x.to_dict())
            payload["alwayson_scripts"]["ADetailer"] = {
                "args": ads
            }
        elif self.has_adetailer:
            payload["alwayson_scripts"]["ADetailer"] = {
                "args": [False]
            }

        if animatediff:
            payload["alwayson_scripts"]["animatediff"] = {
                "args": [animatediff.to_dict(True)]
            }
        elif self.has_animatediff:
            payload["alwayson_scripts"]["animatediff"] = {
                "args": [False],
            }

        if roop:
            payload["alwayson_scripts"]["roop"] = {
                "args": roop.to_dict()
            }

        if reactor:
            payload["alwayson_scripts"]["reactor"] = {
                "args": reactor.to_dict()
            }

        if sag:
            payload["alwayson_scripts"]["Self Attention Guidance"] = {
                "args": sag.to_dict()
            }

        if controlnet_units and len(controlnet_units) > 0:
            payload["alwayson_scripts"]["ControlNet"] = {
                "args": [x.to_dict() for x in controlnet_units]
            }
        elif self.has_controlnet:
            payload["alwayson_scripts"]["ControlNet"] = {"args": []}

        return self.post_and_get_api_result(
            f"{self.baseurl}/img2img", payload, use_async
        )

    def extra_single_image(
            self,
            image,  # PIL Image
            resize_mode=0,
            show_extras_results=True,
            gfpgan_visibility=0,
            codeformer_visibility=0,
            codeformer_weight=0,
            upscaling_resize=2,
            upscaling_resize_w=512,
            upscaling_resize_h=512,
            upscaling_crop=True,
            upscaler_1="None",
            upscaler_2="None",
            extras_upscaler_2_visibility=0,
            upscale_first=False,
            use_async=False,
    ):
        payload = {
            "resize_mode": resize_mode,
            "show_extras_results": show_extras_results,
            "gfpgan_visibility": gfpgan_visibility,
            "codeformer_visibility": codeformer_visibility,
            "codeformer_weight": codeformer_weight,
            "upscaling_resize": upscaling_resize,
            "upscaling_resize_w": upscaling_resize_w,
            "upscaling_resize_h": upscaling_resize_h,
            "upscaling_crop": upscaling_crop,
            "upscaler_1": upscaler_1,
            "upscaler_2": upscaler_2,
            "extras_upscaler_2_visibility": extras_upscaler_2_visibility,
            "upscale_first": upscale_first,
            "image": b64_img(image),
        }

        return self.post_and_get_api_result(
            f"{self.baseurl}/extra-single-image", payload, use_async
        )

    def extra_batch_images(
            self,
            images,  # list of PIL images
            name_list=None,  # list of image names
            resize_mode=0,
            show_extras_results=True,
            gfpgan_visibility=0,
            codeformer_visibility=0,
            codeformer_weight=0,
            upscaling_resize=2,
            upscaling_resize_w=512,
            upscaling_resize_h=512,
            upscaling_crop=True,
            upscaler_1="None",
            upscaler_2="None",
            extras_upscaler_2_visibility=0,
            upscale_first=False,
            use_async=False,
    ):
        if name_list is not None:
            if len(name_list) != len(images):
                raise RuntimeError("len(images) != len(name_list)")
        else:
            name_list = [f"image{i + 1:05}" for i in range(len(images))]
        images = [b64_img(x) for x in images]

        image_list = []
        for name, image in zip(name_list, images):
            image_list.append({"data": image, "name": name})

        payload = {
            "resize_mode": resize_mode,
            "show_extras_results": show_extras_results,
            "gfpgan_visibility": gfpgan_visibility,
            "codeformer_visibility": codeformer_visibility,
            "codeformer_weight": codeformer_weight,
            "upscaling_resize": upscaling_resize,
            "upscaling_resize_w": upscaling_resize_w,
            "upscaling_resize_h": upscaling_resize_h,
            "upscaling_crop": upscaling_crop,
            "upscaler_1": upscaler_1,
            "upscaler_2": upscaler_2,
            "extras_upscaler_2_visibility": extras_upscaler_2_visibility,
            "upscale_first": upscale_first,
            "imageList": image_list,
        }

        return self.post_and_get_api_result(
            f"{self.baseurl}/extra-batch-images", payload, use_async
        )

    # XXX 500 error (2022/12/26)
    def png_info(self, image):
        payload = {
            "image": b64_img(image),
        }

        response = self.session.post(url=f"{self.baseurl}/png-info", json=payload)
        return self._to_api_result(response)

    """
    :param image pass base64 encoded image or PIL Image
    :param model "clip" or "deepdanbooru"
    """

    def interrogate(self, image, model="clip"):
        payload = {
            "image": b64_img(image) if isinstance(image, Image.Image) else image,
            "model": model,
        }

        response = self.session.post(url=f"{self.baseurl}/interrogate", json=payload)
        return self._to_api_result(response)

    def list_prompt_gen_models(self):
        r = self.custom_get("promptgen/list_models")
        return r['available_models']

    def prompt_gen(self,
                   model_name: str = "AUTOMATIC/promptgen-lexart",
                   batch_count: int = 1,
                   batch_size: int = 10,
                   text: str = "",
                   min_length: int = 20,
                   max_length: int = 150,
                   num_beams: int = 1,
                   temperature: float = 1,
                   repetition_penalty: float = 1,
                   length_preference: float = 1,
                   sampling_mode: str = "Top K",
                   top_k: float = 12,
                   top_p: float = 0.15,
                   ):
        payload = {
            "model_name": model_name,
            "batch_count": batch_count,
            "batch_size": batch_size,
            "text": text,
            "min_length": min_length,
            "max_length": max_length,
            "num_beams": num_beams,
            "temperature": temperature,
            "repetition_penalty": repetition_penalty,
            "length_preference": length_preference,
            "sampling_mode": sampling_mode,
            "top_k": top_k,
            "top_p": top_p
        }

        r = self.custom_post("promptgen/generate", payload=payload)
        return r.json['prompts']

    def interrupt(self):
        response = self.session.post(url=f"{self.baseurl}/interrupt")
        return response.json()

    def skip(self):
        response = self.session.post(url=f"{self.baseurl}/skip")
        return response.json()

    def get_options(self):
        response = self.session.get(url=f"{self.baseurl}/options")
        return response.json()

    def set_options(self, options):
        response = self.session.post(url=f"{self.baseurl}/options", json=options)
        return response.json()

    def get_cmd_flags(self):
        response = self.session.get(url=f"{self.baseurl}/cmd-flags")
        return response.json()

    def get_progress(self):
        response = self.session.get(url=f"{self.baseurl}/progress")
        return response.json()

    def get_cmd_flags(self):
        response = self.session.get(url=f"{self.baseurl}/cmd-flags")
        return response.json()

    def get_samplers(self):
        response = self.session.get(url=f"{self.baseurl}/samplers")
        return response.json()

    def get_sd_vae(self):
        response = self.session.get(url=f"{self.baseurl}/sd-vae")
        return response.json()

    def get_upscalers(self):
        response = self.session.get(url=f"{self.baseurl}/upscalers")
        return response.json()

    def get_latent_upscale_modes(self):
        response = self.session.get(url=f"{self.baseurl}/latent-upscale-modes")
        return response.json()

    def get_loras(self):
        response = self.session.get(url=f"{self.baseurl}/loras")
        return response.json()

    def get_sd_models(self):
        response = self.session.get(url=f"{self.baseurl}/sd-models")
        return response.json()

    def get_hypernetworks(self):
        response = self.session.get(url=f"{self.baseurl}/hypernetworks")
        return response.json()

    def get_face_restorers(self):
        response = self.session.get(url=f"{self.baseurl}/face-restorers")
        return response.json()

    def get_realesrgan_models(self):
        response = self.session.get(url=f"{self.baseurl}/realesrgan-models")
        return response.json()

    def get_prompt_styles(self):
        response = self.session.get(url=f"{self.baseurl}/prompt-styles")
        return response.json()

    def get_artist_categories(self):  # deprecated ?
        response = self.session.get(url=f"{self.baseurl}/artist-categories")
        return response.json()

    def get_artists(self):  # deprecated ?
        response = self.session.get(url=f"{self.baseurl}/artists")
        return response.json()

    def refresh_checkpoints(self):
        response = self.session.post(url=f"{self.baseurl}/refresh-checkpoints")
        return response.json()

    def get_scripts(self):
        response = self.session.get(url=f"{self.baseurl}/scripts")
        return response.json()

    def get_embeddings(self):
        response = self.session.get(url=f"{self.baseurl}/embeddings")
        return response.json()

    def get_memory(self):
        response = self.session.get(url=f"{self.baseurl}/memory")
        return response.json()

    def get_schedulers(self):
        response = self.session.get(url=f"{self.baseurl}/schedulers")
        return response.json()

    def get_endpoint(self, endpoint, baseurl):
        if baseurl:
            return f"{self.baseurl}/{endpoint}"
        else:
            from urllib.parse import urlparse, urlunparse

            parsed_url = urlparse(self.baseurl)
            basehost = parsed_url.netloc
            parsed_url2 = (parsed_url[0], basehost, endpoint, "", "", "")
            return urlunparse(parsed_url2)

    def custom_get(self, endpoint, baseurl=False):
        url = self.get_endpoint(endpoint, baseurl)
        response = self.session.get(url=url)
        return response.json()

    def custom_post(self, endpoint, payload={}, baseurl=False, use_async=False):
        url = self.get_endpoint(endpoint, baseurl)
        if use_async:
            import asyncio

            return asyncio.ensure_future(self.async_post(url=url, json=payload))
        else:
            response = self.session.post(url=url, json=payload)
            return self._to_api_result(response)

    def controlnet_version(self):
        r = self.custom_get("controlnet/version")
        return r["version"]

    def controlnet_model_list(self):
        r = self.custom_get("controlnet/model_list")
        return r["model_list"]

    def controlnet_module_list(self):
        r = self.custom_get("controlnet/module_list")
        return r["module_list"]

    def controlnet_detect(
            self, images, module="none", processor_res=512, threshold_a=64, threshold_b=64
    ):
        images = [b64_img(x) for x in images]
        payload = {
            "controlnet_module": module,
            "controlnet_images": images,
            "controlnet_processor_res": processor_res,
            "controlnet_threshold_a": threshold_a,
            "controlnet_threshold_b": threshold_b,
        }
        r = self.custom_post("controlnet/detect", payload=payload)
        return r

    def util_get_model_names(self):
        return sorted([x["title"] for x in self.get_sd_models()])

    def util_get_sampler_names(self):
        return sorted([s['name'] for s in self.get_samplers()])

    def util_get_scheduler_names(self):
        return sorted([s['name'] for s in self.get_schedulers()])

    def util_set_model(self, name, find_closest=True):
        if find_closest:
            name = name.lower()
        models = self.util_get_model_names()
        found_model = None
        if name in models:
            found_model = name
        elif find_closest:
            import difflib

            def str_simularity(a, b):
                return difflib.SequenceMatcher(None, a, b).ratio()

            max_sim = 0.0
            max_model = models[0]
            for model in models:
                sim = str_simularity(name, model)
                if sim >= max_sim:
                    max_sim = sim
                    max_model = model
            found_model = max_model
        if found_model:
            print(f"loading {found_model}")
            options = {}
            options["sd_model_checkpoint"] = found_model
            self.set_options(options)
            print(f"model changed to {found_model}")
        else:
            print("model not found")

    def util_get_current_model(self):
        options = self.get_options()
        if ("sd_model_checkpoint" in options):
            return options["sd_model_checkpoint"]
        else:
            sd_models = self.get_sd_models()
            sd_model = [model for model in sd_models if model["sha256"] == options["sd_checkpoint_hash"]]
            return sd_model[0]["title"]

    def util_wait_for_ready(self, check_interval=5.0):
        import time

        while True:
            result = self.get_progress()
            progress = result["progress"]
            job_count = result["state"]["job_count"]
            if progress == 0.0 and job_count == 0:
                break
            else:
                print(f"[WAIT]: progress = {progress:.4f}, job_count = {job_count}")
                time.sleep(check_interval)


## Interface for extensions

@dataclass
class ModelKeywordResult:
    keywords: list
    model: str
    oldhash: str
    match_source: str


class ModelKeywordInterface:
    def __init__(self, webuiapi):
        self.api = webuiapi

    def get_keywords(self):
        result = self.api.custom_get("model_keyword/get_keywords")
        keywords = result["keywords"]
        model = result["model"]
        oldhash = result["hash"]
        match_source = result["match_source"]
        return ModelKeywordResult(keywords, model, oldhash, match_source)


# https://github.com/Klace/stable-diffusion-webui-instruct-pix2pix
class InstructPix2PixInterface:
    def __init__(self, webuiapi):
        self.api = webuiapi

    def img2img(
            self,
            images=[],
            prompt: str = "",
            negative_prompt: str = "",
            output_batches: int = 1,
            sampler: str = "Euler a",
            steps: int = 20,
            seed: int = 0,
            randomize_seed: bool = True,
            text_cfg: float = 7.5,
            image_cfg: float = 1.5,
            randomize_cfg: bool = False,
            output_image_width: int = 512,
    ):
        init_images = [b64_img(x) for x in images]
        payload = {
            "init_images": init_images,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "output_batches": output_batches,
            "sampler": sampler,
            "steps": steps,
            "seed": seed,
            "randomize_seed": randomize_seed,
            "text_cfg": text_cfg,
            "image_cfg": image_cfg,
            "randomize_cfg": randomize_cfg,
            "output_image_width": output_image_width,
        }
        return self.api.custom_post("instruct-pix2pix/img2img", payload=payload)


# https://github.com/AUTOMATIC1111/stable-diffusion-webui-rembg
class RemBGInterface:
    def __init__(self, webuiapi):
        self.api = webuiapi

    def rembg(
            self,
            input_image: str = "",  # image string (?)
            model: str = 'u2net',
            # [None, 'u2net', 'u2netp', 'u2net_human_seg', 'u2net_cloth_seg','silueta','isnet-general-use','isnet-anime']
            return_mask: bool = False,
            alpha_matting: bool = False,
            alpha_matting_foreground_threshold: int = 240,
            alpha_matting_background_threshold: int = 10,
            alpha_matting_erode_size: int = 10
    ):
        payload = {
            "input_image": b64_img(input_image),
            "model": model,
            "return_mask": return_mask,
            "alpha_matting": alpha_matting,
            "alpha_matting_foreground_threshold": alpha_matting_foreground_threshold,
            "alpha_matting_background_threshold": alpha_matting_background_threshold,
            "alpha_matting_erode_size": alpha_matting_erode_size
        }
        return self.api.custom_post("rembg", payload=payload)


# https://github.com/Mikubill/sd-webui-controlnet
class ControlNetInterface:
    def __init__(self, webuiapi, show_deprecation_warning=True):
        self.api = webuiapi
        self.show_deprecation_warning = show_deprecation_warning

    def print_deprecation_warning(self):
        print(
            "ControlNetInterface txt2img/img2img is deprecated. Please use normal txt2img/img2img with controlnet_units param"
        )

    def txt2img(
            self,
            prompt: str = "",
            negative_prompt: str = "",
            controlnet_image: [] = [],
            controlnet_mask: [] = [],
            controlnet_module: str = "",
            controlnet_model: str = "",
            controlnet_weight: float = 0.5,
            controlnet_resize_mode: str = "Scale to Fit (Inner Fit)",
            controlnet_low_vram: bool = False,
            controlnet_processor_res: int = 512,
            controlnet_threshold_a: int = 64,
            controlnet_threshold_b: int = 64,
            controlnet_guidance: float = 1.0,
            enable_hr: bool = False,  # hiresfix
            denoising_strength: float = 0.5,
            hr_scale: float = 1.5,
            hr_upscale: str = "Latent",
            guess_mode: bool = True,
            seed: int = -1,
            subseed: int = -1,
            subseed_strength: int = -1,
            sampler_index: str = "Euler a",
            batch_size: int = 1,
            n_iter: int = 1,  # Iteration
            steps: int = 20,
            cfg_scale: float = 7,
            width: int = 512,
            height: int = 512,
            restore_faces: bool = False,
            override_settings: Dict[str, Any] = None,
            override_settings_restore_afterwards: bool = True,
    ):
        if self.show_deprecation_warning:
            self.print_deprecation_warning()

        controlnet_image_b64 = [raw_b64_img(x) for x in controlnet_image]
        controlnet_mask_b64 = [raw_b64_img(x) for x in controlnet_mask]

        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "controlnet_image": controlnet_image_b64,
            "controlnet_mask": controlnet_mask_b64,
            "controlnet_module": controlnet_module,
            "controlnet_model": controlnet_model,
            "controlnet_weight": controlnet_weight,
            "controlnet_resize_mode": controlnet_resize_mode,
            "controlnet_low_vram": controlnet_low_vram,
            "controlnet_processor_res": controlnet_processor_res,
            "controlnet_threshold_a": controlnet_threshold_a,
            "controlnet_threshold_b": controlnet_threshold_b,
            "enable_hr": enable_hr,
            "denoising_strength": denoising_strength,
            "hr_scale": hr_scale,
            "hr_upscale": hr_upscale,
            "guess_mode": guess_mode,
            "seed": seed,
            "subseed": subseed,
            "subseed_strength": subseed_strength,
            "sampler_index": sampler_index,
            "batch_size": batch_size,
            "n_iter": n_iter,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": width,
            "height": height,
            "restore_faces": restore_faces,
            "override_settings": override_settings,
            "override_settings_restore_afterwards": override_settings_restore_afterwards,
        }
        return self.api.custom_post("controlnet/txt2img", payload=payload)

    def img2img(
            self,
            init_images: [] = [],
            mask: str = None,
            mask_blur: int = 30,
            inpainting_fill: int = 0,
            inpaint_full_res: bool = True,
            inpaint_full_res_padding: int = 1,
            inpainting_mask_invert: int = 1,
            resize_mode: int = 0,
            denoising_strength: float = 0.7,
            prompt: str = "",
            negative_prompt: str = "",
            controlnet_image: [] = [],
            controlnet_mask: [] = [],
            controlnet_module: str = "",
            controlnet_model: str = "",
            controlnet_weight: float = 1.0,
            controlnet_resize_mode: str = "Scale to Fit (Inner Fit)",
            controlnet_low_vram: bool = False,
            controlnet_processor_res: int = 512,
            controlnet_threshold_a: int = 64,
            controlnet_threshold_b: int = 64,
            guess_mode: bool = True,
            seed: int = -1,
            subseed: int = -1,
            subseed_strength: int = -1,
            sampler_index: str = "",
            batch_size: int = 1,
            n_iter: int = 1,  # Iteration
            steps: int = 20,
            cfg_scale: float = 7,
            width: int = 512,
            height: int = 512,
            restore_faces: bool = False,
            include_init_images: bool = True,
            override_settings: Dict[str, Any] = None,
            override_settings_restore_afterwards: bool = True,
    ):
        if self.show_deprecation_warning:
            self.print_deprecation_warning()

        init_images_b64 = [raw_b64_img(x) for x in init_images]
        controlnet_image_b64 = [raw_b64_img(x) for x in controlnet_image]
        controlnet_mask_b64 = [raw_b64_img(x) for x in controlnet_mask]

        payload = {
            "init_images": init_images_b64,
            "mask": raw_b64_img(mask) if mask else None,
            "mask_blur": mask_blur,
            "inpainting_fill": inpainting_fill,
            "inpaint_full_res": inpaint_full_res,
            "inpaint_full_res_padding": inpaint_full_res_padding,
            "inpainting_mask_invert": inpainting_mask_invert,
            "resize_mode": resize_mode,
            "denoising_strength": denoising_strength,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "controlnet_image": controlnet_image_b64,
            "controlnet_mask": controlnet_mask_b64,
            "controlnet_module": controlnet_module,
            "controlnet_model": controlnet_model,
            "controlnet_weight": controlnet_weight,
            "controlnet_resize_mode": controlnet_resize_mode,
            "controlnet_low_vram": controlnet_low_vram,
            "controlnet_processor_res": controlnet_processor_res,
            "controlnet_threshold_a": controlnet_threshold_a,
            "controlnet_threshold_b": controlnet_threshold_b,
            "guess_mode": guess_mode,
            "seed": seed,
            "subseed": subseed,
            "subseed_strength": subseed_strength,
            "sampler_index": sampler_index,
            "batch_size": batch_size,
            "n_iter": n_iter,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": width,
            "height": height,
            "restore_faces": restore_faces,
            "include_init_images": include_init_images,
            "override_settings": override_settings,
            "override_settings_restore_afterwards": override_settings_restore_afterwards,
        }
        return self.api.custom_post("controlnet/img2img", payload=payload)

    def model_list(self):
        r = self.api.custom_get("controlnet/model_list")
        return r["model_list"]


# https://github.com/continue-revolution/sd-webui-segment-anything
@dataclass
class SegmentAnythingSamResult:
    message: Optional[str]
    blended_images: List[Image.Image]
    masks: List[Image.Image]
    masked_images: List[Image.Image]


@dataclass
class SegmentAnythingGinoResult:
    message: str
    image_with_box: Image.Image


@dataclass
class SegmentAnythingDilationResult:
    blended_image: Image.Image
    mask: Image.Image
    masked_image: Image.Image


@dataclass
class SegmentAnythingControlNetSegNotRandomResult:
    message: str
    sem_presam: Image.Image
    sem_postsam: Image.Image
    blended_presam: Image.Image
    blended_postsam: Image.Image


@dataclass
class SegmentAnythingControlNetSegRandomResult:
    message: str
    blended_image: Image.Image
    random_seg: Image.Image
    edit_anything_control: Image.Image


@dataclass
class SegmentAnythingSemanticSegWithCatIdResult:
    message: str
    blended_image: Image.Image
    mask: Image.Image
    masked_image: Image.Image
    resized_input: Image.Image


class SegmentAnythingInterface:
    def __init__(self, webuiapi: WebUIApi):
        self.api = webuiapi

    def heartbeat(self) -> Dict[str, str]:
        """Check if this extension is working."""
        return self.api.custom_get("sam/heartbeat")

    def get_sam_models(self) -> List[str]:
        """Get available SAM models"""
        return self.api.custom_get("sam/sam-model")

    def sam_predict(
            self,
            image: Image,
            sam_model_name: str = "sam_vit_h_4b8939.pth",
            sam_positive_points: Optional[List[List[float]]] = None,
            sam_negative_points: Optional[List[List[float]]] = None,
            dino_enabled: bool = False,
            dino_model_name: Optional[str] = "GroundingDINO_SwinT_OGC (694MB)",
            dino_text_prompt: Optional[str] = None,
            dino_box_threshold: Optional[float] = 0.3,
            dino_preview_checkbox: bool = False,
            dino_preview_boxes_selection: Optional[List[int]] = None
    ) -> SegmentAnythingSamResult:
        """
        Get masks from SAM

        :param image: Input image.
        :param sam_model_name: SAM model name. You should manually download models before using them.
        :param sam_positive_points: Positive point prompts in N * 2 python list.
        :param sam_negative_points: Negative point prompts in N * 2 python list.
        :param dino_enabled: Whether to use GroundingDINO to generate bounding boxes
            from text to guide SAM to generate masks.
        :param dino_model_name: Choose one of "GroundingDINO_SwinT_OGC (694MB)" and "GroundingDINO_SwinB (938MB)"
            as your desired GroundingDINO model.
        :param dino_text_prompt: Text prompt for GroundingDINO to generate bounding boxes.
            Separate different categories with .
        :param dino_box_threshold: Threshold for selecting bounding boxes. Do not use a very high value,
            otherwise you may get no box.
        :param dino_preview_checkbox: Whether to preview checkbox.
            You can enable preview to select boxes you want if you have accessed API dino-predict
        :param dino_preview_boxes_selection: Choose the boxes you want. Index start from 0.
        """
        payload = {
            "input_image": raw_b64_img(image),
            "sam_model_name": sam_model_name,
            "sam_positive_points": sam_positive_points or [],
            "sam_negative_points": sam_negative_points or [],
            "dino_enabled": dino_enabled,
            "dino_model_name": dino_model_name,
            "dino_text_prompt": dino_text_prompt,
            "dino_box_threshold": dino_box_threshold,
            "dino_preview_checkbox": dino_preview_checkbox,
            "dino_preview_boxes_selection": dino_preview_boxes_selection
        }

        url = self.api.get_endpoint("sam/sam-predict", baseurl=False)
        r = self.api.session.post(url=url, json=payload).json()

        return SegmentAnythingSamResult(
            message=r.get("msg"),
            blended_images=[Image.open(io.BytesIO(base64.b64decode(i))) for i in r["blended_images"]],
            masks=[Image.open(io.BytesIO(base64.b64decode(i))) for i in r["masks"]],
            masked_images=[Image.open(io.BytesIO(base64.b64decode(i))) for i in r["masked_images"]]
        )

    def dino_predict(
            self,
            image: Image,
            text_prompt: str,
            dino_model_name: str = "GroundingDINO_SwinT_OGC (694MB)",
            box_threshold: float = 0.3
    ) -> SegmentAnythingGinoResult:
        """
        Get bounding boxes from GroundingDINO

        :param image: Input image.
        :param text_prompt: Text prompt for GroundingDINO to generate bounding boxes.
            Separate different categories with .
        :param dino_model_name: Choose one of "GroundingDINO_SwinT_OGC (694MB)" and "GroundingDINO_SwinB (938MB)"
            as your desired GroundingDINO model.
        :param box_threshold: Threshold for selecting bounding boxes. Do not use a very high value,
            otherwise you may get no box.
        """
        payload = {
            "input_image": raw_b64_img(image),
            "text_prompt": text_prompt,
            "dino_model_name": dino_model_name,
            "box_threshold": box_threshold
        }

        url = self.api.get_endpoint("sam/dino-predict", baseurl=False)
        r = self.api.session.post(url=url, json=payload).json()

        return SegmentAnythingGinoResult(
            message=r.get("msg"),
            image_with_box=Image.open(io.BytesIO(base64.b64decode(r["image_with_box"])))
        )

    def dilate_mask(
            self,
            image: Image,
            mask: Image,
            dilate_amount: int = 10
    ) -> SegmentAnythingDilationResult:
        """
        Expand mask

        :param image: Input image.
        :param mask: Input mask.
        :param dilate_amount: Mask expansion amount from 0 to 100.
        """
        payload = {
            "input_image": raw_b64_img(image),
            "mask": raw_b64_img(mask),
            "dilate_amount": dilate_amount
        }

        url = self.api.get_endpoint("sam/dilate-mask", baseurl=False)
        r = self.api.session.post(url=url, json=payload).json()

        return SegmentAnythingDilationResult(
            blended_image=Image.open(io.BytesIO(base64.b64decode(r["blended_image"]))),
            mask=Image.open(io.BytesIO(base64.b64decode(r["mask"]))),
            masked_image=Image.open(io.BytesIO(base64.b64decode(r["masked_image"])))
        )

    def generate_semantic_segmentation(
            self,
            image: Image,
            sam_model_name: str = "sam_vit_h_4b8939.pth",
            processor: str = "seg_ofade20k",
            processor_res: int = 512,
            pixel_perfect: bool = False,
            resize_mode: Optional[int] = 1,
            target_width: Optional[int] = None,
            target_height: Optional[int] = None,
            points_per_side: Optional[int] = 32,
            points_per_batch: int = 64,
            pred_iou_thresh: float = 0.88,
            stability_score_thresh: float = 0.95,
            stability_score_offset: float = 1.0,
            box_nms_thresh: float = 0.7,
            crop_n_layers: int = 0,
            crop_nms_thresh: float = 0.7,
            crop_overlap_ratio: float = 512 / 1500,
            crop_n_points_downscale_factor: int = 1,
            min_mask_region_area: int = 0
    ) -> Union[SegmentAnythingControlNetSegNotRandomResult, SegmentAnythingControlNetSegRandomResult]:
        """
        Generate semantic segmentation enhanced by SAM.

        :param image: Input image.
        :param sam_model_name: SAM model name.
        :param processor: Preprocessor for semantic segmentation, choose from one of "seg_ufade20k"
            (uniformer trained on ade20k, performance really bad, can be greatly enhanced by SAM),
            "seg_ofade20k" (oneformer trained on ade20k, performance far better than uniformer, can
            be slightly improved by SAM), "seg_ofcoco" (oneformer trained on coco, similar to seg_ofade20k),
            "random" (for EditAnything)
        :param processor_res: Preprocessor resolution, range in (64, 2048].
        :param pixel_perfect: Whether to enable pixel perfect. If enabled, target_W and target_H will be required,
        and the processor resolution will be overridden by the optimal value.
        :param resize_mode: Resize mode from the original shape to target shape,
        only effective when pixel_perfect is enabled. 0: just resize, 1: crop and resize, 2: resize and fill
        :param target_width: [Required if pixel_perfect is True] Target width if the segmentation will be used
        to generate a new image.
        :param target_height: [Required if pixel_perfect is True] Target height if the segmentation will be used
        to generate a new image.
        :param points_per_side: The number of points to be sampled
            along one side of the image. The total number of points is
            points_per_side**2. If None, 'point_grids' must provide explicit
            point sampling.
        :param points_per_batch: Sets the number of points run simultaneously
            by the model. Higher numbers may be faster but use more GPU memory.
        :param pred_iou_thresh: A filtering threshold in [0,1], using the
            model's predicted mask quality.
        :param stability_score_thresh: A filtering threshold in [0,1], using
            the stability of the mask under changes to the cutoff used to binarize
            the model's mask predictions.
        :param stability_score_offset: The amount to shift the cutoff when
            calculated the stability score.
        :param box_nms_thresh: The box IoU cutoff used by non-maximal
            suppression to filter duplicate masks.
        :param crop_n_layers: If >0, mask prediction will be run again on
            crops of the image. Sets the number of layers to run, where each
            layer has 2**i_layer number of image crops.
        :param crop_nms_thresh: The box IoU cutoff used by non-maximal
            suppression to filter duplicate masks between different crops.
        :param crop_overlap_ratio: Sets the degree to which crops overlap.
            In the first crop layer, crops will overlap by this fraction of
            the image length. Later layers with more crops scale down this overlap.
        :param crop_n_points_downscale_factor: The number of points-per-side
            sampled in layer n is scaled down by crop_n_points_downscale_factor**n.
        :param min_mask_region_area: If >0, postprocessing will be applied
            to remove disconnected regions and holes in masks with area smaller
            than min_mask_region_area. Requires opencv.
        """
        payload = {
            "input_image": raw_b64_img(image),
            "sam_model_name": sam_model_name,
            "processor": processor,
            "processor_res": processor_res,
            "pixel_perfect": pixel_perfect,
            "resize_mode": resize_mode,
            "target_W": target_width,
            "target_H": target_height
        }

        autosam_conf = {
            "points_per_side": points_per_side,
            "points_per_batch": points_per_batch,
            "pred_iou_thresh": pred_iou_thresh,
            "stability_score_thresh": stability_score_thresh,
            "stability_score_offset": stability_score_offset,
            "box_nms_thresh": box_nms_thresh,
            "crop_n_layers": crop_n_layers,
            "crop_nms_thresh": crop_nms_thresh,
            "crop_overlap_ratio": crop_overlap_ratio,
            "crop_n_points_downscale_factor": crop_n_points_downscale_factor,
            "min_mask_region_area": min_mask_region_area
        }

        url = self.api.get_endpoint("sam/controlnet-seg", baseurl=False)
        r = self.api.session.post(url=url, json={"payload": payload, "autosam_conf": autosam_conf}).json()

        if r.get("random_seg"):
            return SegmentAnythingControlNetSegRandomResult(
                message=r.get("msg"),
                blended_image=Image.open(io.BytesIO(base64.b64decode(r["blended_image"]))),
                random_seg=Image.open(io.BytesIO(base64.b64decode(r["random_seg"]))),
                edit_anything_control=Image.open(io.BytesIO(base64.b64decode(r["edit_anything_control"])))
            )
        else:
            return SegmentAnythingControlNetSegNotRandomResult(
                message=r.get("msg"),
                sem_presam=Image.open(io.BytesIO(base64.b64decode(r["sem_presam"]))),
                sem_postsam=Image.open(io.BytesIO(base64.b64decode(r["sem_postsam"]))),
                blended_presam=Image.open(io.BytesIO(base64.b64decode(r["blended_presam"]))),
                blended_postsam=Image.open(io.BytesIO(base64.b64decode(r["blended_postsam"])))
            )

    def sam_and_semantic_seg_with_cat_id(
            self,
            image: Image,
            category: str,
            sam_model_name: str = "sam_vit_h_4b8939.pth",
            processor: str = "seg_ofade20k",
            processor_res: int = 512,
            pixel_perfect: bool = False,
            resize_mode: Optional[int] = 1,
            target_width: Optional[int] = None,
            target_height: Optional[int] = None,
            points_per_side: Optional[int] = 32,
            points_per_batch: int = 64,
            pred_iou_thresh: float = 0.88,
            stability_score_thresh: float = 0.95,
            stability_score_offset: float = 1.0,
            box_nms_thresh: float = 0.7,
            crop_n_layers: int = 0,
            crop_nms_thresh: float = 0.7,
            crop_overlap_ratio: float = 512 / 1500,
            crop_n_points_downscale_factor: int = 1,
            min_mask_region_area: int = 0
    ) -> SegmentAnythingSemanticSegWithCatIdResult:
        """
        Get masks generated by SAM + Semantic segmentation with category IDs.

        :param image: Input image.
        :param category: Category IDs separated by +.
        :param sam_model_name: SAM model name.
        :param processor: Preprocessor for semantic segmentation.
        :param processor_res: Preprocessor resolution.
        :param pixel_perfect: Whether to enable pixel perfect.
        :param resize_mode: Resize mode from the original shape to target shape.
        :param target_width: Target width if the segmentation will be used to generate a new image.
        :param target_height: Target height if the segmentation will be used to generate a new image.
        :param points_per_side: The number of points to be sampled
            along one side of the image. The total number of points is
            points_per_side**2. If None, 'point_grids' must provide explicit
            point sampling.
        :param points_per_batch: Sets the number of points run simultaneously
            by the model. Higher numbers may be faster but use more GPU memory.
        :param pred_iou_thresh: A filtering threshold in [0,1], using the
            model's predicted mask quality.
        :param stability_score_thresh: A filtering threshold in [0,1], using
            the stability of the mask under changes to the cutoff used to binarize
            the model's mask predictions.
        :param stability_score_offset: The amount to shift the cutoff when
            calculated the stability score.
        :param box_nms_thresh: The box IoU cutoff used by non-maximal
            suppression to filter duplicate masks.
        :param crop_n_layers: If >0, mask prediction will be run again on
            crops of the image. Sets the number of layers to run, where each
            layer has 2**i_layer number of image crops.
        :param crop_nms_thresh: The box IoU cutoff used by non-maximal
            suppression to filter duplicate masks between different crops.
        :param crop_overlap_ratio: Sets the degree to which crops overlap.
            In the first crop layer, crops will overlap by this fraction of
            the image length. Later layers with more crops scale down this overlap.
        :param crop_n_points_downscale_factor: The number of points-per-side
            sampled in layer n is scaled down by crop_n_points_downscale_factor**n.
        :param min_mask_region_area: If >0, postprocessing will be applied
            to remove disconnected regions and holes in masks with area smaller
            than min_mask_region_area. Requires opencv.
        """
        payload = {
            "input_image": raw_b64_img(image),
            "category": category,
            "sam_model_name": sam_model_name,
            "processor": processor,
            "processor_res": processor_res,
            "pixel_perfect": pixel_perfect,
            "resize_mode": resize_mode,
            "target_W": target_width,
            "target_H": target_height,
        }

        autosam_conf = {
            "points_per_side": points_per_side,
            "points_per_batch": points_per_batch,
            "pred_iou_thresh": pred_iou_thresh,
            "stability_score_thresh": stability_score_thresh,
            "stability_score_offset": stability_score_offset,
            "box_nms_thresh": box_nms_thresh,
            "crop_n_layers": crop_n_layers,
            "crop_nms_thresh": crop_nms_thresh,
            "crop_overlap_ratio": crop_overlap_ratio,
            "crop_n_points_downscale_factor": crop_n_points_downscale_factor,
            "min_mask_region_area": min_mask_region_area
        }

        url = self.api.get_endpoint("sam/category-mask", baseurl=False)
        r = self.api.session.post(url=url, json={"payload": payload, "autosam_conf": autosam_conf}).json()

        return SegmentAnythingSemanticSegWithCatIdResult(
            message=r.get("msg"),
            blended_image=Image.open(io.BytesIO(base64.b64decode(r["blended_image"]))),
            mask=Image.open(io.BytesIO(base64.b64decode(r["mask"]))),
            masked_image=Image.open(io.BytesIO(base64.b64decode(r["masked_image"]))),
            resized_input=Image.open(io.BytesIO(base64.b64decode(r["resized_input"])))
        )