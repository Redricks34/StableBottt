import json

from aiogram.types import InputMedia
import sqlite3
from sqlite_func import *
from aiogram.utils.markdown import link

from aiogram import types




async def photo_link_aiograph(photo: types.photo_size.PhotoSize) -> str:
    return 'link'
def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


def replace_prompt_lora(prompt):
    promt_ready = prompt.replace('>_<', '<lora:InequalitySignSmileyExpression:1.0>, (><:1.3)').\
        replace('bnight', '<lora:octans-PYNOISE-LOHA:1.4>').\
        replace("makise kurisu", 'makise kurisu, <lora:makiv1:0.3>').\
        replace('rageold', 'ragemode, wild hair, <lora:rageMode_v1:0.65>').\
        replace('ragenew', 'r1ge, <lora:r1ge - AnimeRage:0.3>').\
        replace('peace', '<lora:Internet Yamero:0.8>, internet yamero').\
        replace('yae miko', 'yaemikodef, yaemikornd, <lora:yaemiko1-000008:1>').\
        replace('mecha girl', 'mechagirl girl, <lora:mechagirl_v1a:1.0>'). \
        replace('crazy face', 'CRAZY FACE'). \
        replace('crazy smile', 'CRAZY SMILE, '). \
        replace('crazy eyes', 'CRAZY EYES'). \
        replace('shocked', 'SHOCKED'). \
        replace('scared', 'HORRIFIED, SCARED').\
        replace('kobeni', '(Kobeni), <lora:Character_Kobeni:1>').\
        replace('shenhe', 'shenhe \(genshin impact\), <lora:shenheLoraCollection_shenheHard:1>').\
        replace('rebecca', '1girl, rebecca \(cyberpunk\), <lora:rebecca_v1:0.8>').\
        replace("fishnet", 'fishnet_bodysuit, <lora:fishnet_bodysuit_v10-10:0.6>').\
        replace("pixel", "pixel, pixel art, <lora:pixel_f2:0.3>").\
        replace("manga", "lineart, monochrome, <lora:animeoutlineV4_16:0.7>"). \
        replace("close up face", "halfface, <lora:halfface:1.5>"). \
        replace("half face", "face close up, <lora:halfface:1.5>"). \
        replace("pop figure", "<lora:popupparade-10:1>"). \
        replace("disgusted", "((looking disgusted)), very angry, disappointed, <lora:LookingDisgusted_V1:0.85>"). \
        replace("3drm", "3DMM, <lora:3DMM_V11:0.8>"). \
        replace("re:rem", "Rem, <lora:RemV1:0.8>"). \
        replace("re:emilia", "Emilia, <lora:EmiliaV2:0.8>"). \
        replace("body horror", "<lora:BodHor-V1:0.95>").\
        replace("invisible", "invisible, no humans, headless, faceless, <lora:invisible-14:1.3>").\
        replace("magazine","magazine cover, <lora:Magazine-10:0.8>").\
        replace("niji", "<lora:nijipretty_20230624235607:0.3>").\
        replace('rem galleu', 'rem, <lora:rem galleu:0.7>').\
        replace('mikasa', "hmmikasa, short hair, black eyes, scarf, emblem, belt, thigh strap, red scarf, white pants, brown jacket, long sleeves, <lora:mikasa_ackerman_v1:0.7>").\
        replace('concept', "(multiple views, full body, upper body, reference sheet:1), <lora:CharacterDesign_Concept-10:0.55>").\
        replace("Modeus","modeus(helltaker), <lora:modeus:1.0>").\
        replace("Neferpitou cat", "neferpitou, short hair, (red eyes:1.5), animal ears, tail, white hair, cat ears, cat tail, curly hair, (small breast:1.2), <lora:neferpitou:1.0>").\
        replace("Neferpitou", "neferpitou, long sleeves, shorts, <lora:neferpitou:1.0>").\
        replace("Marinette Dupain", "ladybug outfit, ladybug costume, red and black mask, <lora:marinette-10:1.0>").\
        replace("emilico","1 girl,solo, (emilico:0.9), smile,open mouth, <lora:EMILICO_V1:1.0>").\
        replace("1990s", '<lora:1990:0.8>').\
        replace("colorful portrait", 'Colorful portraits, <lora:Colorful portraits_20230715165729-000018:0.5>').\
        replace('mecha arms', 'mechanical arms, <lora:MechanicalArms_v01:1>').\
        replace('hysteric', 'open_mouth, <lora:screaming:1.0>').\
        replace('constricted pupils', 'constricted pupils, <lora:constricted_pupils_v0.2a:1.0>').\
        replace('buttjob', 'buttjob, penis, girl on top, <lora:buttjob_v0.2:1.0>').\
        replace('octopus', 'octopus, <lora:octopus_v0.5:1.4>').\
        replace('riding girl', 'ridingsexscene, <lora:ridingsexscene_lora_01-i4:0.7>').\
        replace('deepthroat', 'deepthroat, <lora:pov_deepthroat_v0.1:1.0>').\
        replace('titstouch', 'unaligned breasts, asymmetrical docking, <lora:unalignedDocking-000040:0.4>').\
        replace('head back', 'head back, <lora:head_back_v2:0.8>').\
        replace("drow ranger", 'drow, woman, blue skin, pointy ears, <lora:drow_offset:0.27>').\
        replace("st handjob", "cuddling handjob, <lora:cuddling_handjob_v0.1b:1.0>").\
        replace("light lines", '<lora:nlc_blue:1.35>').\
        replace("yagami light", "1boy, Yagami Light,  <lora:Light_30:0.45>").\
        replace("lawliet", "1boy, lawliet, white shirt, denim pants, <lora:Lawlietv1:0.77>").\
        replace("pastel", "<lora:pastelMixStylizedAnime_pastelMixLoraVersion:1.2>").\
        replace("inosuke", "inosuke, <lora:Inosuke:0.6>").\
        replace("inosukemask", "(inosukemask), inosuke, mask, animal, Boar's head, <lora:Inosuke:1.4>").\
        replace("game icon", "game icon, game icon institute, <lora:game icon institute_卡通表情包:0.8>").\
        replace("poster", "poster,  <lora:mryu_7:1.4>").\
        replace("shapes", "<lora:geometric_shapes:1.0>").\
        replace("catman", "<lora:catman:0.75>, maomi").\
        replace("kira yoshikage", "kira yoshikage, formal,suit,necktie ,<lora:jojo_kira-10:1>").\
        replace("diavolo jojo", "diavolojojo, <lora:diavolo-7:1>").\
        replace("joseph joestar", "joseph joestar, muscular male, brown hair, <lora:jojo_joseph_joestar-10:1>").\
        replace("giorno giovanna", "grno, <lora:Giorno giovanna:1.0>").\
        replace("gzibli-style", "ghibli style, <lora:ghibli_style_offset (1):0.9>").\
        replace("liquid clothes", "liquid clothes,water, <lora:LiquidClothesV2:0.4>").\
        replace("x-x","<lora:hotarueye_comic7_v080:0.9> xx").\
        replace("cute comic", "cute comic, <lora:cute_social_Comic-10:1.2>").\
        replace("liuli2","liuli2, <lora:liuli2:1.3>").\
        replace("BJ_Gundam", "BJ_Gundam, <lora:Gundam_Mecha_v3.5(4440):0.5>").\
        replace("pencilsketch","pencilsketch,  <lora:PencilSketch:0.9>,")

    return promt_ready


def replace_description_model(model):
    model_repl = json.loads(open("model_json/model_info.json", encoding="utf-8").read())[model]
    text_l = link("\u200C", model_repl['image'])
    text_l = f"{text_l}*{model}*\n{model_repl['description']}\n\n"
    # return InputMedia(type="photo", media=model_repl["image"],
    #                   caption=f"<b>🤗 {model}</b>\n\n{model_repl['description']}\n\n",
    #                   parse_mode="html")
    return text_l


def replace_dark_light_real_alpha(model):
    return model.replace("2.25D", "2.25D Alpha").replace("Dark", "Dark Alpha").replace("Light", "Light Alpha")

def replace_description_txt2img(model, resolution, prompt, negative="", seed=-1, style="no_style"):
    text_p = link("дополнить", "https://t.me/alphastabletbot?start=edit_prompt")
    text_m = link("Модификации и дополнения", "https://telegra.ph/Dopolneniya--modifikacii-07-18")

    text = f"*Мы готовы сгенерировать ваш запрос ✍️:*\n" \
           f"\n" \
           f"_💬 Чтобы применить стили, нажми на кнопку -Cтили- под строкой ввода текста_\n" \
           f"\n" \
           f"*🎨Промт:* `{prompt}`\n" \
           f"{text_p}\n" \
           f"\n" \
           f"*Дополнительно:*\n" \
           f"└Модель: *{model}*\n" \
           f"└Разрешение: *{resolution}*\n" \

    if seed != -1:
        text += f"└Сид: *{seed}*\n"
    if negative != "":
        text += f"└Негатив: *{negative}*\n"

    return text



    if negative != "":
        text_new += f"└ㅤНегатив: `{negative}`\n"
    if seed != -1:
        text_new += f"└ㅤСид: `{seed}`\n"
    if style != "no_style":
        text_new += f"-✨Стиль: `{style}`"
    text_new += f"\n"\
                f"// {text_p}"
    return text_new.replace("// [Доступные персонажи из аниме/игр/манг](https://telegra.ph/Podderzhka-personazhej-07-13)", "")


def replace_description_img2img(model, prompt, strength, negative="", seed=-1):
    text_new = f"*Мы готовы перевести ваше фото в аниме🏙️:*\n" \
               f"\n" \
               f"🎨Промт: `{prompt}`\n" \
               f"\n" \
               f"*Дополнительно:*\n" \
               f"└ Модель: *{model}*\n" \
               f"└ Сила: _{strength}_\n"
    if negative != "":
        text_new += f"└ㅤНегатив: `{negative}`\n"
    if seed != -1:
        text_new += f"└ㅤСид: `{seed}`\n"

    return text_new



def replace_get_txt2img(model, resolution, prompt, seed,  negative="", style="no_style", seed_link="-"):
    lk = link(f"{seed}", f"https://t.me/sigma_stable_bot?start={seed_link}")
    text = f"*Ваша генерация на основе промта готова ✍️:*\n" \
           f"\n" \
           f"*🌱HyperSeed:* {lk}\n" \
           f"\n" \
           f"*🎨Промт:* `{prompt}`\n" \
           f"\n" \
           f"*Дополнительно:*\n" \
           f"*└Модель:* `{model}`\n" \
           f"*└Разрешение: {resolution}*\n" \
           f"*└Сид:* `{seed}`\n"
    if negative != "":
        text += f"*└Негатив:* `{negative}`"
    return text


def replace_model_zoom(model):
    if model == "Dark Alpha":
        return "alpha.safetensors [5863be5d07]"
    elif model == "Gamma":
        return "gamma.safetensors [42a50d3380]"
    elif model == "Zeta":
        return "zeta.safetensors [a611cf9c19]"
    elif model == "Lamda":
        return "lamda.safetensors [6965f33b20]"
    elif model == "Omicron":
        return "omicron.safetensors [3d6c130515]"
    elif model == "Omega":
        return "omega.safetensors [cbfba64e66]"
    elif model == "Delta":
        return "delta.safetensors"
    elif model == "Yota":
        return "yota.safetensors [e7aab5067d]"
    elif model == "Sigma":
        return "revAnimated_v122.safetensors [4199bcdd14]"


def replace_get_img2img(model, prompt, seed, strength, negative=""):
    text_new = f"*Ваша генерация на основе изображения готова🏙️:*\n" \
                 f"\n" \
                 f"🎨Промт: `{prompt}`\n"

    if negative != "":
        text_new += f"└ㅤНегатив: `{negative}`\n"
    text_new += f"\n" \
                f"└ㅤМодель: `{model}`\n" \
                f"└ㅤСид: `{seed}`\n" \
                f"└Сила: _{strength}_\n" \
                f"\n" \
                f"*Дополнительно:*\n" \
                f"- 🔁 Повторить(10 токенов)\n" \
                f"- ⬆️ Upscale 2х(5 токенов)\n"

    return text_new


def get_settings_ready_txt2img(text):
    text_split = text.split()
    seed = -1
    negative = ""
    style = "no_style"
    model = text_split[text_split.index("└Модель:") + 1]
    resol = text_split[text_split.index("└Разрешение:") + 1]
    prompt = text[text.find("🎨Промт:") + 8:text.find("\nдополнить")]
    if "└Сид:" in text:
        seed = text_split[text_split.index("└Сид:") + 1]
    if "└Негатив:" in text:
        negative = text[text.find("└Негатив:") + 10:]

    return {"model": replace_dark_light_real_alpha(model),
            "resol": resol,
            "prompt": prompt,
            "negative": negative,
            "seed": seed,
            "style": style
            }


def model_replace_name(model):
    if model == "noosphere_v2.safetensors [a32c345ff3]":
        return "Omicron"
    elif model == "CounterfeitV30_v30.safetensors [cbfba64e66]":
        return "Omega"
    elif model == "ghostmix_v20Bakedvae.safetensors [e3edb8a26f]":
        return "Pi"
    elif model == "darkSushiMixMix_darkerPruned.safetensors [fb44463063]":
        return "Dark alpha"
    elif model == "velaMix_velaMixVersion2.safetensors [42a50d3380]":
        return "Gamma"
    elif model == "mutanted.safetensors [25294d1efa]":
        return "Lamda"
    elif model == "meinapastel_v5AnimeIllustration.safetensors [ff1bb68db1]":
        return "Zeta"
    elif model == "yota":
        return "Yota"


def get_settings_ready_img2img(text):
    text_split = text.split()
    seed = -1
    negative = ""
    style = "no_style"
    model = text_split[text_split.index("└ㅤМодель:") + 1]
    strength = text_split[text_split.index("-💪Сила:") + 1]
    prompt = text[text.find("🎨Промт:") + 8:text.find("\nизменить")]
    if "└ㅤСид:" in text:
        seed = text_split[text_split.index("└ㅤСид:") + 1]
    if "-✨Стиль:" in text:
        style = text_split[text_split.index("-✨Стиль:") + 1]

    if "└ㅤСид:" in text and "❌Негатив:" in text:
        negative = text[text.find("❌Негатив:") + 10:text.find("\n└ㅤСид:")]
    elif "└ㅤСид:" not in text and "❌Негатив:" in text and "-✨Стиль:" in text:
        negative = text[text.find("❌Негатив:") + 10:text.find("\n-✨Стиль:")]
    elif "└ㅤСид:" not in text and "❌Негатив:" in text and "-✨Стиль:" not in text:
        negative = text[text.find("❌Негатив:") + 10:]

    return {"model": replace_dark_light_real_alpha(model),
            "prompt": prompt,
            "negative": negative,
            "seed": seed,
            "style": style,
            "strength": strength
            }


def get_settings_get_txt2img(text):
    text_split = text.split()
    negative = ""
    style = "no_style"
    model = text_split[text_split.index("└Модель:") + 1]
    resol = text_split[text_split.index("└Разрешение:") + 1]
    prompt = text[text.find("🎨Промт:") + 8:text.find("\n\nДополнительно:")]
    seed = text_split[text_split.index("└Сид:") + 1]
    if "└Негатив:" in text:
        negative = text[text.find("└Негатив:") + 10:text.find("\n\n💰 Остаток на балансе - ")]

    return {"model": replace_dark_light_real_alpha(model),
            "resol": resol,
            "prompt": prompt,
            "negative": negative,
            "seed": seed,
            "style": style
            }


def get_settings_get_img2img(text):
    text_split = text.split()
    negative = ""
    style = "no_style"
    model = text_split[text_split.index("└ㅤМодель:") + 1]
    seed = text_split[text_split.index("└ㅤСид:") + 1]
    strength = text_split[text_split.index("💪Сила:") + 1]
    if "✨Стиль:" in text:
        style = text_split[text_split.index("✨Стиль:") + 1]
    if "❌Негатив:" in text:
        prompt = text[text.find("🎨Промт:") + 8:text.find("\n❌Негатив:")]
    elif "❌Негатив:" not in text and "✨Стиль:" in text:
        prompt = text[text.find("🎨Промт:") + 8:text.find("\n✨Стиль:")]
    elif "❌Негатив:" not in text and "✨Стиль:" not in text:
        prompt = text[text.find("🎨Промт:") + 8:text.find("\n\n⭐️Модель:")]
    if "❌Негатив:" in text and "✨Стиль:" in text:
        negative = text[text.find("❌Негатив:") + 10:text.find("\n✨Стиль:")]
    if "❌Негатив:" in text and "✨Стиль:" not in text:
        negative = text[text.find("❌Негатив:") + 10:text.find("\n✨Стиль:")]

    return {"model": replace_dark_light_real_alpha(model),
            "prompt": prompt,
            "negative": negative,
            "seed": seed,
            "style": style,
            "strength": strength
            }


def replace_description_style(style):
    style_repl = json.loads(open("model_json/style.json", encoding="utf-8").read())[style]
    text_l = link("\u200C", style_repl['image'])
    text_i = f"{text_l}*🤗 {style_repl['name']}*\n\n{style_repl['desc']}\n\n_Чтобы не использовать стили, выберите - без стиля_"
    return text_i


def st(call, user_id):
    items = get_items(user_id)
    promt = items[7]
    mod_promt = promt.replace(", magazine,", "").replace(", pop figure,", '').replace(", body horror,", '').replace(
        ', invisible,', ''). \
        replace(', rageold,', '').replace(', pixel,', '').replace(', 3drm,', '').replace('manga,', '').replace('niji,', '').replace(
        ', no_style', '').replace(', concept', '').replace(', 1990s', '').replace(', ragenew','')
    if call == "no_style":
        save_data_in_database("promt", mod_promt, items[0])
    else:
        save_data_in_database("promt", mod_promt, str(user_id))
        modd_promt = mod_promt + ", " + call + ','
        save_data_in_database("promt", modd_promt.replace(", ,", ",").replace(", , ,", ",").replace(",,", ","),
                              str(user_id))
