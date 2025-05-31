import random
from datetime import time

import requests as req

from PIL import Image, PngImagePlugin
import base64
import io
import json
import string
import secrets
from sqlite_func import *
from utils import *
from webuiapi import webuiapi
from utils import replace_prompt_lora
# import runpod

# runpod.api_key = "8FDMB6CCISMARJK4C6LP24GPCGI59MUAS1UEPXIF"

url = "http://127.0.0.1:7860"


def runpod_endpoing(model):
    return model


def generate_upscale(user_id, file_name):
    import base64
    with open(f"outs" + f"\\{user_id}\\{file_name}", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        base = encoded_string.decode('utf-8')
    items = get_items(user_id)
    md = replace_model_zoom(items[5])
    # endpoint = runpod.Endpoint("r9puknkh1poi7d")
    payload = {
        'init_images': [base],
        "override_settings": {
            "sd_model_checkpoint": f"{md}"},
        'prompt': "raw, hdr, 8k textures, extreme detail, hight detailed skin texture, epic details, high sharpness",
        'script_name': 'SD upscale', 'sampler_index': "DPM++ 2S a Karras",
        'script_args': [None, 64, "R-ESRGAN 4x+ Anime6B", 1.5], 'steps': 15, 'denoising_strength': 0.2,
        'negative_prompt': " watermark, signature, mutation, negative_hand, (deformed, distorted, disfigured:1.3),"
                           " poorly drawn, bad anatomy, worng anatomy, extra limbs, missing limbs, floating limbs,"
                           " (mutated hands and fingers:1.4), mutations, mutated, ugly, blury, amputation "}

    response = req.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    data = response.json()
    img_data = (str(data["images"]).replace("['", "").replace("']", ""))

    with open("outs" + f"\\{user_id}\\{user_id}upscaled" + '.png', "wb") as fh:
        fh.write(base64.b64decode(img_data))

    image = Image.open("outs" + f"\\{user_id}\\{user_id}upscaled" + '.png')

    # next 3 lines strip exif
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)

    image_without_exif.save("outs" + f"\\{user_id}\\{user_id}upscaled" + 'rd.png')
    # as a good practice, close the file handler after saving the image.
    image_without_exif.close()

    save_data_in_database("status", 0, user_id)
    save_data_in_database("hquality", 0, user_id)
    save_data_in_database("job_id", "empty", user_id)


def generate_zoom(prompt, user_id, seed, zoom_scale, zoom_status):
    import base64
    if zoom_status == 0:
        sides = ['down', 'left', 'right', 'up']
    elif zoom_status == 1:
        sides = ['left', 'right']
    elif zoom_status == 2:
        sides = ['up', 'down']
    endp = "r9puknkh1poi7d"
    with open(f"outs" + f"\\{user_id}\\{user_id}" + 'rd.png', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        input_image = encoded_string.decode('utf-8')
    items = get_items(user_id)
    md = replace_model_zoom(items[5])
    # endpoint = runpod.Endpoint("r9puknkh1poi7d")
    payload ={
            'init_images': [input_image],
            'cfg_scale': 4,
            "override_settings": {
                "sd_model_checkpoint": f"{md}"},
            'prompt': "background, " + prompt,
            'script_name': 'Outpainting mk2',
            'sampler_index': "Euler a",
            'script_args': [None, zoom_scale, 43, sides, 1, 0.03],
            'steps': 20,
            'denoising_strength': 0.9,
            "seed": int(seed),
            'negative_prompt': " watermark, signature, mutation, negative_hand, (deformed, distorted, disfigured:1.3),"
                               " poorly drawn, bad anatomy, worng anatomy, extra limbs, missing limbs, floating limbs,"
                               " (mutated hands and fingers:1.4), mutations, mutated, ugly, blury, amputation "}

    # Check the status of the endpoint run request

    # Get the output of the endpoint run request, blocking until the endpoint run is complete.

    response = req.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    data = response.json()
    print(data)
    img_data = (str(data["images"]).replace("['", "").replace("']", ""))

    import base64
    with open("outs" + f"\\{user_id}\\{user_id}zoom" + '.png', "wb") as fh:
        fh.write(base64.b64decode(img_data))

    image = Image.open("outs" + f"\\{user_id}\\{user_id}zoom" + '.png')

    # next 3 lines strip exif
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)

    image_without_exif.save("outs" + f"\\{user_id}\\{user_id}zoom" + 'rd.png')
    # as a good practice, close the file handler after saving the image.
    image_without_exif.close()

    save_data_in_database("status", 0, user_id)
    save_data_in_database("hquality", 0, user_id)
    save_data_in_database("seed", seed, user_id)


def generate_txt2img(prompt, model, negative, seed, resol, steps, up_scale, hr, d_strength, user_id):
    import base64
    endp = "r9puknkh1poi7d"
    cfg = 8

    upload_model = runpod_endpoing(model)
    items = get_items(user_id)
    print(up_scale)
    print(upload_model)
    if items[22] == 1:
        ds = 0.7
        sampler = "UniPC"
        steps = 24
        if upload_model == "omega.safetensors [cbfba64e66]":
            ds = 0.46
            up_scale = "R-ESRGAN 4x+"
            sampler = "DPM++ SDE Karras"
            steps = 26
        elif upload_model == "alpha.safetensors [5863be5d07]":
            sampler = "Euler a"
            steps = 24
            up_scale = "ESRGAN_4x"

        with open(f"outs/{user_id}/pose.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            input_image = encoded_string.decode('utf-8')
        json_payload = {
            "override_settings": {
                "sd_model_checkpoint": f"{upload_model}"
            },
            "prompt": prompt,
            "width": resol[0],
            "height": resol[1],
            "seed": seed,
            "negative_prompt": negative,
            "steps": 15, "enable_hr": True,
            "denoising_strength": ds,
            'hr_scale': hr,
            'cfg_scale': cfg,
            'clip_skip': 2,
            "hr_second_pass_steps": 15,
            'sampler_index': sampler,
            'hr_upscaler': up_scale,
            "alwayson_scripts": {"controlnet": {"args": [
                {"module": "canny", "weight": 0.9, "model": "t2iadapter_canny-fp16 [f2e7f7cd]",
                 "input_image": f"{str(input_image)}"}]}}}
    elif items[22] == 3:
        with open(f"outs/{user_id}/qr_hd_text.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            input_image = encoded_string.decode('utf-8')
        json_payload = {
            "override_settings": {
                "sd_model_checkpoint": f"{upload_model}"
            },
            "prompt": prompt,
            "width": resol[0],
            "height": resol[1],
            "seed": seed,
            "negative_prompt": negative,
            "steps": 15, "enable_hr": True,
            "denoising_strength": 0.6,
            'hr_scale': 2,
            'cfg_scale': 10,
            'clip_skip': 2,
            "hr_second_pass_steps": 15,
            'sampler_index': "DPM++ 2S a Karras",
            'hr_upscaler': "Latent",
            "alwayson_scripts": {"controlnet": {"args": [
                {"weight": 2.0,
                 "model": "control_v1p_sd15_qrcode_monster [a6e58995]",
                 "input_image": f"{str(input_image)}"}], "pixel perfect": True}}}
        print("qr_setup")
    elif items[22] == 2:
        with open(f"outs/{user_id}/text.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            input_image = encoded_string.decode('utf-8')
        json_payload = {
            "override_settings": {
                "sd_model_checkpoint": f"{upload_model}"
            },
            "prompt": prompt,
            "width": int(resol[0]),
            "height": int(resol[1]),
            "seed": seed,
            "negative_prompt": negative,
            "steps": 15, "enable_hr": True,
            "denoising_strength": 0.65,
            'hr_scale': 2.5,
            'cfg_scale': 11,
            'clip_skip': 2,
            "hr_second_pass_steps": 15,
            'sampler_index': "UniPC",
            'hr_upscaler': "R-ESRGAN 4x+ Anime6B",
            "alwayson_scripts": {"controlnet": {"args": [
                {"pixel perfect": "True", "weight": 0.9,
                 "model": "control_v1p_sd15_qrcode_monster [a6e58995]",
                 "input_image": f"{str(input_image)}"}]}}}
    else:

        cfg = 10
        ds = 0.7
        sampler = "UniPC"
        steps = 35
        hr = 2.5
        hr_steps = 15
        en_hr = True

        if upload_model == "omega.safetensors [cbfba64e66]":
            ds = 0.55
            up_scale = "4x-UniScaleV2_Moderate"
            sampler = "DPM++ SDE Karras"
            steps = 30
            cfg = 7
        elif upload_model == "yota.safetensors [372dd2ad6a]":
            up_scale = "lollypop"
            ds = 0.5
            steps = 30
            sampler = "Euler a"
            cfg = 7

        elif upload_model == "pastelMixStylizedAnime_pastelMixFull.safetensors [fa818fcf2c]":
            ds = 0.6
            up_scale = "Latent"
            sampler = "DPM++ SDE Karras"
            steps = 25
            hr = 2
            cfg = 10
            hr_steps = 20
            negative = negative.replace("easynegative", "(easynegative:1.2)")
        elif upload_model == "alpha.safetensors [5863be5d07]":
            ds = 0.56
            up_scale = "Latent"
            sampler = "DPM++ 2M Karras"
            steps = 30
            cfg = 8

            negative = 'EasyNegativeV2, ' + negative.replace("easynegative", '')
        elif upload_model == "cetusMix_Coda2.safetensors [68c0a27380]":
            cfg = 10
            ds = 0.5
            steps = 30
            sampler = "UniPC"
            up_scale = "4x-AnimeSharp"
        elif upload_model == "darkSushi25D25D_v40.safetensors [bb32ad727a]":
            cfg = 8
            ds = 0.56
            sampler = "DPM++ 2M Karras"
            up_scale = "Latent"
            steps = 20
            print("3D alpha")
        elif upload_model == "delta.safetensors":
            cfg = 10
            ds = 0.6
            up_scale = "4x-UltraSharp"
            steps = 20
            sampler = "Euler a"
        elif upload_model == "omicron.safetensors [3d6c130515]":
            up_scale = "4x-UniScaleV2_Moderate"
            ds = 0.5
            sampler = "DPM++ 2M Karras"
            steps = 28
            hr = 2.5
            cfg = 10
        elif upload_model == "gamma.safetensors [42a50d3380]":
            ds = 0.56
            up_scale = "4x-UniScaleV2_Moderate"
            sampler = "DPM++ SDE Karras"
            steps = 26
            cfg = 10
        elif upload_model == "delta.safetensors":
            ds = 0.8
            sampler == "UniPC"
        elif upload_model == "beta.safetensors [aeb953ac1a]":
            sampler = "Euler a"
            up_scale = "Latent"
            ds = 0.55
            cfg = 7
            steps = 20
        elif model == "revAnimated_v122.safetensors [4199bcdd14]":
            sampler = "DPM++ SDE Karras"
            steps = 30
            cfg = 10
            up_scale = "Latent"
        elif upload_model == "universe.safetensors [879db523c3]":
            sampler = "DPM++ 2S a Karras"
            up_scale = "R-ESRGAN 4x+"
            steps = 30
            ds = 0.6
            cfg = 10
            prompt = prompt.replace("masterpiece, best quality, (sharpness) ", "")
        elif "pastel" in prompt:
            steps = 30
            sampler = "DPM++ 2S a Karras"
            up_scale = "Latent"
            ds = 0.6
            prompt = prompt + ", (soft), ((watercolor))"

        json_payload = {
            "override_settings": {
                "sd_model_checkpoint": f"{upload_model}"
            },
            "prompt": prompt,
            "width": resol[0],
            "height": resol[1],
            "seed": seed,
            "negative_prompt": negative,
            "steps": steps, "enable_hr": en_hr,
            "denoising_strength": ds,
            'hr_scale': hr,
            'cfg_scale': cfg,
            'clip_skip': 2,
            "hr_second_pass_steps": hr_steps,
            'sampler_index': sampler,
            'hr_upscaler': up_scale,

        }
    # try:
    #     endpoint = runpod.Endpoint(endp)
    #     run_request = endpoint.run(json_payload)
    #     save_data_in_database("job_id", str(run_request.job_id), user_id)
    # except:
    #     save_data_in_database("job_id", "error", user_id)

    # print(run_request.job_id + " <== JOB ID ")

    # Check the status of the endpoint run request

    # Get the output of the endpoint run request, blocking until the endpoint run is complete.

    response = req.post(url=f'{url}/sdapi/v1/txt2img', json=json_payload)
    data = response.json()

    img_data = (str(data["images"]).replace("['", "").replace("']", ""))

    import base64
    with open("outs" + f"\\{user_id}\\{user_id}" + '.png', "wb") as fh:
        fh.write(base64.b64decode(img_data))

    image = Image.open("outs" + f"\\{user_id}\\{user_id}" + '.png')

    # next 3 lines strip exif
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)

    image_without_exif.save("outs" + f"\\{user_id}\\{user_id}" + 'rd.png')

    # as a good practice, close the file handler after saving the image.
    image_without_exif.close()

    save_data_in_database("status", 0, user_id)
    save_data_in_database("hquality", 0, user_id)
    save_data_in_database("seed", seed, user_id)
    save_data_in_database("job_id", "empty", user_id)


def ready_txt2img(prompt, model, resol, user_id, style="no_style", re_bool=False, hq=False, seed=-1, negative=""):
    print(style)
    model_sd = json.loads(open("model_json/model_info.json", encoding="utf-8").read())[model]["model_sd"]
    resolution_sd = json.loads(open("model_json/resolution_info.json", encoding="utf-8").read())[resol]["resol"]
    prompt_sd = "(masterpiece, best quality, detailed, variable, colored), " + prompt
    negative_sd = "(verybadimagenegative_v1.3, easynegative), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, blurry, deformed face, deformed hands, deformed fingers, ugly, bad anatomy, extra fingers, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face" + negative
    seed_sd = random.randint(0, 100000000)
    steps = 20
    d_strength = 0.7
    up_scale = "R-ESRGAN 4x+ Anime6B"
    hr = 2.5
    if model == "Pi":
        up_scale = "Latent"
        steps = 30
        d_strength = 0.6

    elif model == "Omega":
        steps = 25

    if seed != -1 and not re_bool:
        seed_sd = seed

    if hq:
        prompt_sd += ", <lora:add_detail:1.3>"
        hr = 2.5

    if resol == "2:1" and hq == 1:
        hr = 2

    try:
        cl_prompt = prompt_sd.split("-c:")[1]
    except:
        print("Корректор одежды не введен")
    if "-c:" in prompt_sd and prompt.split("-c:")[1].isdigit() and 0 <= int(prompt_sd.split("-c:")[1]) <= 100:
        low = 0
        high = 100

        low_2 = -1
        high_2 = 1

        relative_value = (float(cl_prompt) - low) / (high - low)

        scaled_value = round(low_2 + (high_2 - low_2) * relative_value, 2) * (-1)

        prompt_sd = (prompt_sd + f", <lora:ClothingAdjuster2:{str(scaled_value)}>")
        print(scaled_value)
        print(cl_prompt)
        prompt_sd = prompt_sd.replace(f"-c:{str(cl_prompt)}", "")

    if "CRAZY FACE" in replace_prompt_lora(prompt) or "CRAZY SMILE" in replace_prompt_lora(
            prompt) or "CRAZY EYES" in replace_prompt_lora(prompt) or "SHOCKED" in replace_prompt_lora(
        prompt) or "SCARED" in replace_prompt_lora(prompt):
        prompt_sd += ", <lora:Crazy_ExpressionsV2:0.8>"
    if "kiss" in prompt or "tongue kiss" in prompt or "kissing" in prompt:
        prompt_sd += ",  <lora:AnimeKiss:0.6>"
    if "clothes tug" in prompt or "skirt tug" in prompt or "dress tug" in prompt or "shirt tug" in prompt or "sweater tug" in prompt or "wind" in prompt or "wind lift" in prompt:
        prompt_sd = prompt_sd + ", <lora:skirt_tug_v0.1:1.2>"
    if "Asuna Yuuki" in prompt:
        prompt_sd = prompt_sd + ", <lora:asunayuukitest:1.0>"
    if "hmjy1" in prompt:
        prompt_sd = prompt_sd + ", <lora:jabami yumeko_v10:0.7>"
    if "kitagawa marin" in prompt:
        prompt_sd = prompt_sd + ",  <lora:kitagawa_marin_v1-1:1.0>"
    if "rengoku kyojuro" in prompt:
        prompt_sd = prompt_sd + ", <lyco:demonslayer_rengoku-10:1.0>"
    if "sophie hatter" in prompt:
        prompt_sd = prompt_sd.replace("sophie hatter",
                                      "") + "1girl, sophie_hatter,  brown eyes, <lora:sophie_hatter:0.85>"
    if "howl jenkins" in prompt:
        prompt_sd = prompt_sd.replace("howl jenkins",
                                      "") + "howl_jenkins, blue eyes, necklace, earrings, jewelry, white shirt, black pants, <lora:howl_jenkins:0.9>"
    if "tape gag" in prompt and "tape bondage" in prompt:
        prompt_sd = prompt_sd + ", tape gag, tape bondage, <lora:TapeGagV7:1>"
    if "tape gag" in prompt:
        prompt_sd = prompt_sd + ", tape gag, <lora:TapeGagV7:1>"
    if "Oversized shirt" in prompt and "oversized clothes" in prompt:
        prompt_sd = prompt_sd + ", oversized clothes, <lora:oversized_shirt:1>"
    if "Oversized shirt" in prompt:
        prompt_sd = prompt_sd + ", Oversized shirt, <lora:oversized_shirt:1>"

    image_sd = generate_txt2img(prompt=replace_prompt_lora(prompt_sd), model=model_sd, resol=resolution_sd,
                                negative=negative_sd,
                                seed=seed_sd, steps=steps, hr=hr, up_scale=up_scale, d_strength=d_strength,
                                user_id=user_id)

    if hq:
        return {
            "prompt": prompt,
            "model": model,
            "negative": negative,
            "seed": str(seed_sd) + " ✨Hqualited",
            "style": style,
            "resol": resol
        }
    else:
        return {
            "prompt": prompt,
            "model": model,
            "negative": negative,
            "seed": str(seed_sd),
            "style": style,
            "resol": resol
        }


# Временно недоступно

'''
def generate_img2img(images, width, height, prompt, strength, negative, seed, user_id):
    api = webuiapi.WebUIApi(sampler='DPM++ SDE Karras', steps=25)
    result2 = api.img2img(images=[images], width=width * 1, height=height * 1, resize_mode=1,
                          prompt=prompt,
                          seed=seed, cfg_scale=7,
                          negative_prompt=negative, denoising_strength=strength)
    result2.image.save(f'outs/{user_id}/{user_id}res.jpg')


def ready_img2img(prompt, strength, user_id, negative="", seed=-1):
    result1 = Image.open(f'outs/{user_id}/{user_id}raw.jpg')
    width, height = result1.size
    negative_sd = 'easynegative, negative_hand-neg, verybadimagenegative_v1.3, ng_deepnegative_v1_75t,' \
                  ' (mutated hands:1.9), mutation, bad anatomy, bad proportions, extra limbs, cloned face' + negative

    seed_sd = random.randint(0, 100000000)
    if seed != -1:
        seed_sd = seed
    strength_sd = json.loads(open("model_json/strength.json", encoding="utf-8").read())[strength]["strength_sd"]

    generate_img2img(images=result1, width=width, height=height, prompt=prompt, negative=negative_sd, seed=seed_sd,
                     user_id=user_id, strength=strength_sd)

    save_data_in_database("status", 0, user_id)
    save_data_in_database("seed", seed_sd, user_id)



def upscaler(user_id):
    api = webuiapi.WebUIApi(steps=25)
    result1 = Image.open(f'outs/{user_id}/{user_id}rd.png')
    result2 = api.extra_single_image(upscaling_resize=2, image=result1, upscaler_1='R-ESRGAN 4x+ Anime6B',
                                     upscaler_2='R-ESRGAN 4x+ Anime6B')
    result2.image.save(f'outs/{user_id}/{user_id}-upscaled.png')
    save_data_in_database("status", 0, user_id)

def ready_upscale(user_id):
    upscaler(user_id)
'''
