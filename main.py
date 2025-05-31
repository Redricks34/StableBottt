import datetime
import os
import random
import shutil
import sqlite3

import requests
from googletrans import Translator
from requests.auth import HTTPBasicAuth
import PIL
from aiogram.dispatcher.filters import Text
import logging
import re
import segno
from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageFilter
import secrets
import string

from multiprocessing import Process

from PIL import Image, PngImagePlugin
import base64
import io
import emoji
import multiprocessing as mp
import requests as requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, callback_query, InputMedia, ContentType, ChatActions, CallbackQuery, \
    Message, WebAppInfo, InputFile
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.markdown import hlink, link

import asyncio

from webuiapi import webuiapi
from yoomoney import Quickpay
from yoomoney import Client
import openai
import json
import time as t
from utils import *
from sqlite_func import *

from upscale import upscaler
from generate_func import *

API_KEY = ""
openai.api_key = API_KEY

API_TOKEN = ""
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class Form(StatesGroup):
    negative_wait = State()
    seed_state = State()
    amount_pay = State()
    casino = State()
    pose = State()
    text = State()
    qr_image = State()
    qr_text = State()
    zoom_prompt = State()
    clear = State()
    qr_hidden_text = State()
    gift_amount = State()
    add_prompt = State()


print('''                                                                      
 _____ __    _____ _____ _____    _____ _____ _____ _____ __    _____ 
|  _  |  |  |  _  |  |  |  _  |  |   __|_   _|  _  | __  |  |  |   __|
|     |  |__|   __|     |     |  |__   | | | |     | __ -|  |__|   __|
|__|__|_____|__|  |__|__|__|__|  |_____| |_| |__|__|_____|_____|_____|
                                                    POWERED BY R/R''')
CHANNEL_ID = '@stablealpha'
NOTSUB_MESSAGE = "Для использования бота, просьба подписаться на наш канал"


def overlay_images(image1_path, image2_path, output_path):
    # Откройте изображения
    image1 = Image.open(image1_path).convert("RGBA")
    image2 = Image.open(image2_path).convert("RGBA").filter(ImageFilter.GaussianBlur(radius=10))
    # Создайте маску с закругленными углами
    mask = Image.new("L", image1.size, 0)
    corner_radius = 20
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image1.width, image1.height), corner_radius, fill=255)

    # Примените маску к image1
    rounded_image = Image.new("RGBA", image1.size)
    rounded_image.paste(image1, (0, 0), mask)

    # Рассчитайте координаты для наложения image1 на image2 по центру
    x = (image2.width - rounded_image.width) // 2
    y = (image2.height - rounded_image.height) // 2

    # Наложите image1 на image2 по центру
    result = Image.new("RGBA", image2.size)
    result.paste(image2, (0, 0))
    result.paste(rounded_image, (x, y), mask=rounded_image)

    # Добавьте текст на изображение-результат
    text = "AlphaStable"
    font = ImageFont.truetype("arial.ttf", 26)
    text_width, text_height = font.getsize(text)

    # Создайте изображение для рамки и заливки
    text_box_width = text_width + 20  # Добавьте отступы слева и справа
    text_box_height = text_height + 20  # Добавьте отступы сверху и снизу
    text_box = Image.new("RGBA", (text_box_width, text_box_height), (255, 255, 255, 128))

    # Нарисуйте рамку и заливку на text_box
    draw = ImageDraw.Draw(text_box)
    draw.rectangle([(0, 0), (text_box_width, text_box_height)], outline=(255, 255, 255), fill=(255, 255, 255))

    # Рассчитайте координаты для размещения текста внутри text_box
    text_x = (text_box_width - text_width) // 2
    text_y = text_box_height - text_height - 10  # Позиционируйте текст внизу

    # Нарисуйте текст на text_box
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    # Наложите text_box на result

    result.paste(text_box, (round(image2.width / 2) - round(text_box_width / 2), image2.height - text_box_height - 10),
                 mask=text_box)

    # Сохраните результат в формате PNG
    result.save(output_path, "PNG")


def crop_to_square(image_path, output_path):
    # Open the image
    image = Image.open(image_path).convert("RGBA")

    # Determine the size of the square
    size = min(image.size)

    # Calculate the coordinates to crop the image
    left = (image.width - size) // 2
    top = (image.height - size) // 2
    right = left + size
    bottom = top + size

    # Crop the image to the square
    cropped_image = image.crop((left, top, right, bottom))

    # Save the cropped image as PNG
    cropped_image.save(output_path, "PNG")


"""
def inter(promt, user_id):
    img_to_interrgate = Image.open(f'outs/{user_id}/{user_id}raw.jpg')
    res = interrgate(img_to_interrgate, user_id)

    save_data_in_database("promt", res, user_id)

    async def sendd():
        await bot.send_photo(chat_id=user_id, photo=open(f'outs/{user_id}/{user_id}raw.jpg', "rb"),
                             caption=f"**🥳 Теперь ты можешь перевести свое фото в аниме!**\n\n Просто жми кнопку **Сгенерировать**.\n\n🤖 **Auto Промт**: `{res}`",
                             reply_markup=propmt_markup_img, parse_mode='markdown')

    asyncio.run(sendd())
"""
"""
def start_upscale(user_id):
    upscaler(user_id)

    async def send_upscale():
        result1 = Image.open(f'outs/{user_id}/{user_id}-upscaled.png')
        width, height = result1.size
        await bot.send_document(user_id, open(f'outs/{user_id}/{user_id}-upscaled.png', "rb"),
                                caption=f"🔝* Upscaled 2x*\n{(str(width / 2)).replace('.0','')}x{(str(height/ 2)).replace('.0','')} < > {width}x{height}",
                                parse_mode='markdown')

    asyncio.run(send_upscale())
"""


def upscale_start(user_id, file_name):
    generate_upscale(user_id=user_id, file_name=file_name)

    async def send():
        await bot.send_document(user_id, open("outs" + f"\\{user_id}\\{user_id}upscaled" + 'rd.png', "rb"),
                                caption=f"*🔥 SuperUpscaled 2x*\n\nГенерация прошла через Upscale. Разрешение увеличено в два раза.",
                                parse_mode='markdown')
        await bot.delete_message(chat_id=user_id, message_id=get_items(user_id)[26])

    asyncio.run(send())


def zoom_start(prompt, user_id, seed, zoom_scale, zoom_status):
    generate_zoom(prompt=prompt, user_id=user_id, seed=seed, zoom_scale=zoom_scale, zoom_status=zoom_status)

    async def send():
        await bot.send_document(user_id, open("outs" + f"\\{user_id}\\{user_id}zoom" + 'rd.png', "rb"),
                                caption=f"⏺ *ZOOM генерация*\n\nИзображение успешно расширено, вот ваш результат:",
                                parse_mode='markdown')
        await bot.delete_message(chat_id=user_id, message_id=get_items(user_id)[26])

    asyncio.run(send())


def generate(prompt, model, resol, user_id, style, hq=False, seed=-1, negative="", re_bool=False):
    ds = ready_txt2img(model=model, prompt=prompt, resol=resol, user_id=user_id, style=style, hq=hq,
                       seed=seed, negative=negative, re_bool=re_bool)

    async def send():
        db = sqlite3.connect('seeds.db')
        c = db.cursor()

        alphabet = string.ascii_letters + string.digits
        link = ''.join(secrets.choice(alphabet) for i in range(20))

        items = get_items(user_id)
        param = (link, ds['prompt'], items[10], ds['negative'], ds["model"], items[6])
        print(param)
        c.execute(f"INSERT INTO seeds VALUES (?, ?, ?, ?, ?, ?)", param)
        db.commit()
        db.close()

        import shutil
        shutil.copyfile("outs" + f"\\{user_id}\\{user_id}" + 'rd.png',
                        "outs" + f"\\{user_id}\\{user_id}" + f'rd{link}.png')
        # 2nd option

        text = replace_get_txt2img(model=ds['model'], prompt=ds['prompt'], negative=ds['negative'],
                                   resolution=ds['resol'], seed=ds['seed'], style=ds['style'],
                                   seed_link=link) + f"\n\n💰 Остаток на балансе - *{items[2]} т*"

        await bot.send_document(user_id, open("outs" + f"\\{user_id}\\{user_id}" + f'rd{link}.png', "rb"),
                                caption=text, parse_mode='markdown', reply_markup=write_history_to_art_markup)
        await bot.delete_message(chat_id=user_id, message_id=get_items(user_id)[26])


    asyncio.run(send())


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


"""
def imgtoimg(prompt, user_id):

    i2i(prompt, user_id)

    async def send_i2i():
        if str(user_id) in get_all_user_id():
            await bot.send_message("Мы не нашли вас в базе пользователей, пожалуйста, пропишите /start")
        else:

            await bot.send_document(user_id, open("outs" + f"\\{user_id}\\{user_id}res.jpg", "rb"),
                                    caption=f"**Ваша последняя генерация:**\n\nпромт: `{prompt}`\n\n*Мы можем написать историю к вашему арту, для этого нажмите кнопку ниже*\n\n*Генерация создана на основе изображения*",
                                    parse_mode='markdown', reply_markup=write_history_to_art_markup_only)

    asyncio.run(send_i2i())
"""

# --> BUTTON <-- #


propmt_markup = InlineKeyboardMarkup(row_width=2)
guide_button = InlineKeyboardButton(text="📚 Гайд", url="https://telegra.ph/AlphaStable---polnoe-rukovodstvo-07-30")
stay_promt_previous = InlineKeyboardButton(text='💬 GPT edit', callback_data='stay_promt')
choose_model_button = InlineKeyboardButton(text='⚙️ Модель', callback_data="choose_model")
choose_resolution_button = InlineKeyboardButton(text="⬜️ Разрешение", callback_data="resolution")
choose_style_button = InlineKeyboardButton(text="✨ Cтиль", callback_data='style')
choose_seed_button = InlineKeyboardButton(text="🌱 Сид", callback_data='seed')
choose_pose_button = InlineKeyboardButton(text="🕺 Референс", callback_data='ref_mode')
choose_negative_button = InlineKeyboardButton(text="❌ Негатив", callback_data='negative')
choose_streight_button = InlineKeyboardButton(text="💪 Сила", callback_data='streight')
start_gen_button = InlineKeyboardButton(text="💫 Сгенерировать ( 10т )", callback_data="start_gen")
start_gen_img = InlineKeyboardButton(text="🖼 Сгенерировать", callback_data="start_gen_img")

propmt_markup.row(guide_button).row(choose_model_button, choose_resolution_button).row(choose_seed_button,
                                                                                       choose_negative_button,
                                                                                       choose_pose_button).row(
    start_gen_button)

propmt_markup_img = InlineKeyboardMarkup(row_width=1).row(choose_seed_button, choose_negative_button).add(
    choose_streight_button, start_gen_img)

change_style_markup = InlineKeyboardMarkup(row_width=3)
prev_style = InlineKeyboardButton('⬅️', callback_data='prev_style')
back_style = InlineKeyboardButton('Назад', callback_data='go_back')
next_style = InlineKeyboardButton('➡️️', callback_data='next_style')
change_style_markup.add(prev_style, back_style, next_style)

choose_streight_markup = InlineKeyboardMarkup(row_width=1)
very_low_str = InlineKeyboardButton("Минимальная", callback_data='1')
low_str = InlineKeyboardButton("Низкая", callback_data='2')
classic_str = InlineKeyboardButton("Стандартная", callback_data='3')
high_str = InlineKeyboardButton("Высокая", callback_data='4')
very_high_str = InlineKeyboardButton("Максимальная", callback_data='5')
save_button_str = InlineKeyboardButton(text='Сохранить выбор', callback_data="save_str")
choose_streight_markup.row(very_low_str, low_str).row(classic_str).row(high_str, very_high_str).row(save_button_str)

choose_model_markup = InlineKeyboardMarkup(row_width=2)
alpha_button = InlineKeyboardButton(text='Alpha', callback_data="Alpha")
beta_button = InlineKeyboardButton(text='Beta', callback_data='Beta')
gamma_button = InlineKeyboardButton(text='Gamma', callback_data='Gamma')
zeta_button = InlineKeyboardButton(text='Zeta', callback_data='Zeta')
lamda_button = InlineKeyboardButton(text='Lamda', callback_data='Lamda')
pi_button = InlineKeyboardButton(text='Pi', callback_data='Pi')
yota_button = InlineKeyboardButton(text="Yota", callback_data='Yota')
omega_button = InlineKeyboardButton(text='Omega', callback_data='Omega')
omicron_button = InlineKeyboardButton(text="Omicron", callback_data='Omicron')
delta_button = InlineKeyboardButton(text='Delta', callback_data='Delta')
sigma_button = InlineKeyboardButton(text="Sigma", callback_data="Sigma")
epsilon_button = InlineKeyboardButton(text="Epsilon", callback_data='Epsilon')
universe_button = InlineKeyboardButton(text="Universe", callback_data="Universe")
sdxl_button = InlineKeyboardButton(text="Omega XL", callback_data="omegaxl")
save_model_button = InlineKeyboardButton(text='Сохранить выбор', callback_data='save_model_button')
choose_model_markup.row(alpha_button, gamma_button, beta_button).row(omega_button, pi_button).row(yota_button).row(
    omicron_button, universe_button).row(save_model_button)

choose_model_alpha_markup = InlineKeyboardMarkup(row_width=3)
dark_alpha_button = InlineKeyboardButton(text='Dark Alpha', callback_data="Dark Alpha")
alpha225d_button = InlineKeyboardButton(text='3D Alpha', callback_data="3DAlpha")
light_alpha_button = InlineKeyboardButton(text='Light Alpha', callback_data="Light Alpha")
back_button = InlineKeyboardButton(text='<< Назад', callback_data="back_button")
choose_model_alpha_markup.row(alpha225d_button, dark_alpha_button).row(
    save_model_button).row(back_button)

choose_resolution_markup = InlineKeyboardMarkup(row_width=2)
one_to_one_button = InlineKeyboardButton(text="1:1", callback_data="1:1")

s_to_n_button = InlineKeyboardButton(text="3:2", callback_data="3:2")
n_to_s_button = InlineKeyboardButton(text="2:3", callback_data="2:3")
res_16_button = InlineKeyboardButton(text="16:9", callback_data="16:9")
res_9_button = InlineKeyboardButton(text="9:16", callback_data="9:16")
t_to_o_button = InlineKeyboardButton(text="2:1", callback_data="2:1")
resol_button = InlineKeyboardButton(text='Сохранить выбор', callback_data='save_resol_button')
choose_resolution_markup.row(one_to_one_button).row(s_to_n_button, n_to_s_button).row(res_16_button, res_9_button).row(
    t_to_o_button).row(resol_button)

get_generation_markup = InlineKeyboardMarkup(row_width=1)
get_generation_button = InlineKeyboardButton(text="Получить генерацию", callback_data="get_get")
get_generation_markup.add(get_generation_button)

styles_markup = InlineKeyboardMarkup(row_width=5)
magazine_style = InlineKeyboardButton(text="Журнал", callback_data="magazine")
popfigure_style = InlineKeyboardButton(text="Фигурка", callback_data="pop figure")
bodyhorror_style = InlineKeyboardButton(text="Хоррор", callback_data="body horror")
invisivle_style = InlineKeyboardButton(text="No body", callback_data="invisible")
ragemode_style = InlineKeyboardButton(text="Ярость", callback_data="ragemode_chooser")
pixel_style = InlineKeyboardButton(text="Пиксель", callback_data="pixel")
tdrm_style = InlineKeyboardButton(text="3D рендер", callback_data="3drm")
manga_style = InlineKeyboardButton(text="Манга", callback_data="manga")
Niji_style = InlineKeyboardButton(text="Niji", callback_data="niji")
pastel_style = InlineKeyboardButton(text="Pastel", callback_data="pastel")
concept_style = InlineKeyboardButton(text='Concept', callback_data="concept")
nn_style = InlineKeyboardButton(text='1990', callback_data='1990s')

rage_markup = InlineKeyboardMarkup(row_width=2)
rage_old = InlineKeyboardButton(text="Rage old", callback_data="rageold")
rage_new = InlineKeyboardButton(text="Rage new", callback_data="ragenew")
save_button = InlineKeyboardButton(text="Сохранить", callback_data="save_style")
rage_markup.add(rage_old, rage_new)
no_style = InlineKeyboardButton(text="Без стиля", callback_data="no_style")

styles_markup.row(magazine_style, popfigure_style, bodyhorror_style).row(invisivle_style, ragemode_style, pixel_style,
                                                                         nn_style).row(tdrm_style, manga_style,
                                                                                       Niji_style, concept_style).row(
    pastel_style).row(no_style).row(save_button)

alphashare_contin_markup = InlineKeyboardMarkup(row_width=1)
alphashare_contin_markup_2 = InlineKeyboardMarkup(row_width=1)
like_button = InlineKeyboardButton(text="❤️ (+3 автору)", callback_data='like')
cont_button = InlineKeyboardButton(text="Далее", callback_data="cont_button")
alphashare_contin_markup.add(like_button, cont_button)
alphashare_contin_markup_2.add(cont_button)

write_history_to_art_markup = InlineKeyboardMarkup(row_width=2)
write_history_to_art_markup_2 = InlineKeyboardMarkup(row_width=2)
write_history_to_art_markup_3 = InlineKeyboardMarkup(row_width=2)
write_history_to_art_markup_4 = InlineKeyboardMarkup(row_width=2)

write_history_to_art_btn = InlineKeyboardButton(text="📖 Написать историю к арту", callback_data="write_history")
restart_gen_button = InlineKeyboardButton(text="🔁 Повторить (10т)", callback_data="restart_gen")
hq_and_su_button = InlineKeyboardButton(text="🔥 Улучшить", callback_data="make_better")
upscaleee_gen_button = InlineKeyboardButton(text="🔥️ SuperUpscale ( 20т )", callback_data="upscale")
zoom_button = InlineKeyboardButton(text="⏺ Zoom (20т)", callback_data='zoom')
upscale_gen_button = InlineKeyboardButton(text="🔝️ HQuality ( 15т )", callback_data="hquality")
edit_gen_button = InlineKeyboardButton(text="⚙️ Изменить", callback_data="edit_res")
alphashare_button = InlineKeyboardButton(text="🔖 Выложить", callback_data="ashare")

hq_and_su_markup = InlineKeyboardMarkup(row_width=2)
back_hq_and_su_button = InlineKeyboardButton(text="<< Отмена", callback_data="back_hqandsu")
hq_and_su_markup.add(upscaleee_gen_button, upscale_gen_button).row(zoom_button).row(back_hq_and_su_button)

write_history_to_art_markup.row(hq_and_su_button).row(edit_gen_button, restart_gen_button).row(alphashare_button)
write_history_to_art_markup_2.row(hq_and_su_button).row(edit_gen_button, restart_gen_button)

write_history_to_art_markup_3.row(restart_gen_button, edit_gen_button).row(alphashare_button)
write_history_to_art_markup_4.row(restart_gen_button, edit_gen_button).row(restart_gen_button)
write_history_to_art_markup_only = InlineKeyboardMarkup(row_width=1)

write_history_to_art_btn = InlineKeyboardButton(text="📖 Написать историю к арту", callback_data="write_history")
write_history_to_art_markup_only.add(write_history_to_art_btn)

cancel_markup = InlineKeyboardMarkup(row_width=1)
cancel_button = InlineKeyboardButton(text="Вернуться назад", callback_data="go_back")
cancel_markup.add(cancel_button)

keyboard_ashare = InlineKeyboardMarkup(row_width=1)
button_1 = InlineKeyboardButton(text="Проверить генерацию", callback_data="check_gen")
keyboard_ashare.add(button_1)

keyboard_ashare2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
ashare_button = types.KeyboardButton(text="AlphaShare")
persons_button = KeyboardButton(text="Персонажи", web_app=WebAppInfo(url='https://innoky.github.io/Персонажи.html'))
keyboard_ashare2.add(ashare_button, persons_button)
choose_amount_markup = InlineKeyboardMarkup(row_width=2)
tf_button = InlineKeyboardButton(text="50т - 25₽", callback_data='tf_button')
f_button = InlineKeyboardButton(text="100т - 49₽", callback_data='f_button')
nf_button = InlineKeyboardButton(text="🔥 200т - 90₽", callback_data='nf_button')
ohf_button = InlineKeyboardButton(text="300т - 149₽", callback_data='ohf_button')
choose_amount_pers = InlineKeyboardButton(text="Другое", callback_data='set_amount')
choose_amount_markup.add(tf_button, f_button, nf_button, ohf_button).row(choose_amount_pers)

back_balance_button = InlineKeyboardButton(text="<< Назад", callback_data="back_balance_button")

casino_markup = InlineKeyboardMarkup(row_width=1)
play_button = InlineKeyboardButton(text="Сыграть", callback_data="play_casino")
back_casino = InlineKeyboardButton(text="<< Назад", callback_data="back_casino")

casino_markup.add(play_button, back_casino)

channel_sub_markup = InlineKeyboardMarkup(row_width=1)
channel_sub_button = InlineKeyboardButton(text="Канал AlphaStable", url="https://t.me/stablealpha")
channel_sub_markup.add(channel_sub_button)


# --> END BUTTON <-- #


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if "alphagift" in message.text:
        db = sqlite3.connect('userbase.db')
        c = db.cursor()
        c.execute("SELECT * FROM users")
        items = c.fetchall()
        existence = bool

        for i in range(len(items)):
            if str(items[i][0]) == str(message.from_user.id):
                existence = True
                break
        if existence == False:
            await bot.send_message(message.chat.id,
                                   "Мы не нашли вас в базе пользователей, пожалуйста, пропишите /start")
        else:
            if items[i][9] == 1:
                await bot.send_message(message.chat.id,
                                       "🥰 Вы уже активировали промокод)"
                                       " Скоро добавим новый, следите в нашем канале!",
                                       reply_markup=keyboard_ashare2)
            else:
                await bot.send_message(message.chat.id,
                                       "🥰 Поздравляем, промокод успешно"
                                       " активирован! Мы безумно рады"
                                       " что вы пользуетесь ботом. Желаем"
                                       " удачных генераций!\n\n<code>Начисление: +40 токенов</code>",
                                       parse_mode="html", reply_markup=keyboard_ashare2)
                save_data_in_database("gift_status", "1", message.from_user.id)
                save_data_in_database("balance", items[i][2] + 40, message.from_user.id)
    if "edit_prompt" in message.text:
        print("test")
        worker_msg = message.text.replace("/start ", "")
        items = get_items(message.from_user.id)
        cancel_neg_markdown = InlineKeyboardMarkup(row_width=1)
        cancel_neg_button = InlineKeyboardButton(text="<< Назад", callback_data="cancel_neg")
        cancel_neg_markdown.add(cancel_neg_button)
        mss = await bot.send_message(message.chat.id,
                                     f"🎨 *Введите промт в дополнении к старому*\nОн добавится к концу старого ввода.\n\nСтарый ввод: `{items[7]}`",
                                     parse_mode="markdown", reply_markup=cancel_neg_markdown)

        async with state.proxy() as data:
            data["edit_id"] = mss.message_id
        await Form.add_prompt.set()
    if "rd" in message.text:

        db = sqlite3.connect('userbase.db')
        c = db.cursor()
        c.execute(f"SELECT id FROM users")
        db.commit()
        items = c.fetchall()
        db.close()
        exist = 0
        for i in range(len(items)):
            if str(items[i]).replace("('", "").replace("',)", "") == str(message.from_user.id):
                exist = 1
        if exist == 0:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="*Мы не нашли вас в базе пользователей.*\n\nПропишите /start",
                                   parse_mode="markdown")
        else:
            worker_text = message.text.replace("/start ", "")
            id = worker_text.split("rd")[0]

            db = sqlite3.connect('gift.db')
            c = db.cursor()
            c.execute(f"SELECT * FROM gift")
            db.commit()
            itemss = c.fetchall()
            db.close()
            status_of_gift = 0
            for i in range(len(itemss)):
                if itemss[i][0].replace("('", "").replace("',)", "") == id:
                    amount = itemss[i][1]
                    gifter = itemss[i][3]
                    getter = itemss[i][4]
                    break

            if itemss[i][2] == 1:
                status_of_gift = 1

            if status_of_gift == 0:
                if str(gifter) == str(message.from_user.id):
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=f"😢 Похоже это ваш подарок. Вы его активировать не можете.",
                                           parse_mode="markdown")
                else:
                    if message.from_user.username != getter and getter != "empty":
                        await bot.send_message(chat_id=message.from_user.id,
                                               text=f"😢 Похоже этот подарок не для вас",
                                               parse_mode="markdown")
                    else:
                        item = get_items(message.from_user.id)
                        balance = item[2]
                        save_data_in_database("balance", balance + int(amount), message.from_user.id)

                        db = sqlite3.connect("gift.db")
                        cur = db.cursor()
                        sql_update_query = f'''UPDATE gift SET status = ? WHERE gift_link = ?'''
                        data_b = (1, id)
                        cur.execute(sql_update_query, data_b)
                        db.commit()
                        db.close()

                        itemsz = get_items(gifter)
                        save_data_in_database("balance", int(itemsz[2]) - int(amount), int(gifter))
                        await bot.send_message(chat_id=message.from_user.id,
                                               text=f"🎁 *Поздравляем! Вам подарили {amount} токен(ов)*",
                                               parse_mode="markdown")
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"😢 *Этот подарок уже использован*", parse_mode="markdown")

    if len(message.text.replace("/start ", "")) == 20:
        db = sqlite3.connect('seeds.db')
        c = db.cursor()
        c.execute(f"SELECT * FROM seeds")
        db.commit()
        items = c.fetchall()
        db.close()
        print(message.text)
        for i in range(len(items)):
            print(items[i][0])
            if str(items[i][0]) == message.text.replace('/start ', ''):
                data = items[i]
                break

        save_data_in_database('pose_status', 0, message.from_user.id)
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        items = get_items(message.from_user.id)

        cur_model = data[4]
        cur_resol = data[5]

        save_data_in_database("raw_promt", data[1], message.from_user.id)
        save_data_in_database("promt", data[1], message.from_user.id)

        text = link('подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
        # await bot.send_photo(message.chat.id, photo="https://i.ibb.co/KVv7rvH/914029246rd-659.png",
        #                      caption=f"""☺️*Мы готовы сгенерировать ваш запрос:*\n\n`{message.text}`\n\n- {text}\n\n*Советуем использовать GPT edit для лучшего результата*\n\nТекущая модель: **{cur_model}**\nРазрешение: **{cur_resol}**""",
        #                      reply_to_message_id=message.message_id,
        #                      parse_mode='markdown', reply_markup=propmt_markup)
        items = get_items(message.from_user.id)
        rp2 = ReplyKeyboardMarkup(resize_keyboard=True)
        rp2_button = KeyboardButton(text="Стили", web_app=WebAppInfo(url='https://innoky.github.io/#'))
        button_1 = types.KeyboardButton(text="AlphaShare")
        rp2.add(button_1, rp2_button)

        await bot.send_message(message.from_user.id, f"*⚙️ Промт:* `{items[7]}`",
                               disable_web_page_preview=True, reply_markup=rp2, parse_mode='markdown')
        await bot.send_message(message.chat.id, text=replace_description_txt2img(model=cur_model,
                                                                                 prompt=data[1],
                                                                                 resolution=cur_resol,
                                                                                 negative=data[3],
                                                                                 seed=data[2], ),
                               reply_to_message_id=message.message_id, parse_mode='markdown',
                               reply_markup=propmt_markup, disable_web_page_preview=True)

    elif message.text == '/start' or (" " in message.text and message.text.split()[1].isdigit()):
        try:

            db = sqlite3.connect('userbase.db')
            c = db.cursor()
            if (" " in message.text and message.text.split()[1].isdigit()):
                referrer_candidate = message.text.split()[1]
                referrer_candidate = int(referrer_candidate)
                print("Реферал найден")
            # Идем далее
            c.execute("SELECT * FROM users")
            items = c.fetchall()
            existence = False
            db.close()
            try:
                for i in range(len(items)):
                    if str(items[i][0]) == str(referrer_candidate):
                        existence = True
                        break
            except:
                print("// user sign in whith out reffer")

            for j in range(len(items)):
                if str(items[j][0]) == message.from_user.id:
                    break
            db = sqlite3.connect('userbase.db')
            c = db.cursor()
            c.execute("SELECT id FROM users")
            items = c.fetchall()
            existence = False
            for el in items:
                if str(el[0]) == str(user_id):
                    existence = True
            if existence == False:
                param = (
                    message.from_user.id, message.from_user.username, 25, 0, 0, "Dark Alpha", "1:1", "text", "null",
                    "null", "..", "..", 'null', 'null', 'null', '0', 1, '2', "0", "no_style", "", 10, 0, 0, 128, 1,
                    "empty", "empty")
                c.execute(
                    f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    param)

                print(f"// User succesfuly added to db. \nid -> {user_id}, name -> {message.from_user.username}\n")
                os.mkdir('outs\\' + str(message.from_user.id))

                await message.answer(
                    f"<b>🖐 Здравствуй, {message.from_user.username}. Вы успешно добавлены в список пользователей.</b> \nРады видеть вас в нашем боте.",
                    parse_mode='html')

                db.commit()
                db.close()
                try:
                    referrer_candidate = message.text.split()[1]
                    referrer_candidate = int(referrer_candidate)
                    await bot.send_message(chat_id=int(referrer_candidate),
                                           text="🔥 Кто-то перешел по вашей реферальной ссылке. Вам начисленно 25 токенов!")
                    items = get_items(referrer_candidate)
                    save_data_in_database('balance', items[2] + 25, referrer_candidate)
                except:
                    print("Пользователь зашел не через рефералку")
            else:

                print(
                    f"// User already exists in data base.  \nid -> {user_id}, name -> {message.from_user.username}\n")
            db.close()

            if len(message.text.replace("/start ", "")) != 20:
                save_data_in_database("pose_status", 0, message.from_user.id)
                text = hlink('🆕 - подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
                i_link = link("\u200C", "https://telegra.ph/file/2d6cde020cef67aec21e4.png")
                ch_link = link("наш канал", "https://t.me/stablealpha")
                await bot.send_message(
                    message.chat.id,
                    text=f'''{i_link}👋 *Здравствуй, {message.from_user.username}!*\n\nХочешь создать свой аниме арт? Просто отправь мне описание желаемого результата на русском, а потом жми *Cгенерировать*.\nЕсли ты профи, можешь составить промт сам.\n\n__Наш бот имеет множество класнных функций, подробнее о них можешь прочитать в нашем канале!__\n\nРекомендуем подписаться на {ch_link}, там мы публикуем новости по обновлениям, а также выкладываем арты наших подписчиков\n\n✨ Желаем вам удачных генераций!''',
                    reply_markup=keyboard_ashare2,
                    reply_to_message_id=message.message_id, parse_mode="markdown", )
        except Exception as e:
            print(e)
            text = hlink('🆕 - подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
            i_link = link("\u200C", "https://telegra.ph/file/2d6cde020cef67aec21e4.png")
            ch_link = link("наш канал", "https://t.me/stablealpha")
            await bot.send_message(
                message.chat.id,
                text=f'''{i_link}👋 *Здравствуй, {message.from_user.username}!*\n\nХочешь создать свой аниме арт? Просто отправь мне описание желаемого результата на русском, а потом жми *Cгенерировать*.\nЕсли ты профи, можешь составить промт сам.\n\n__Наш бот имеет множество класнных функций, подробнее о них можешь прочитать в нашем канале!__\n\nРекомендуем подписаться на {ch_link}, там мы публикуем новости по обновлениям, а также выкладываем арты наших подписчиков\n\n✨ Желаем вам удачных генераций!''',
                reply_markup=keyboard_ashare2,
                reply_to_message_id=message.message_id, parse_mode="markdown", )


@dp.message_handler()
async def get_gen(message: types.Message, state: FSMContext):
    itemms = get_items(message.from_user.id)
    if not (itemms[1] == message.from_user.username):
        save_data_in_database("username", message.from_user.username, message.from_user.id)
    if str(message.from_user.id) not in get_all_user_id():
        await bot.send_message(message.chat.id, "Мы не нашли вас в базе пользователей, пожалуйста, пропишите /start")
    else:
        if "/a" in message.text and (not ("https" in message.text)):
            await bot.send_message(914029246, message.text.replace("/a", "") + "\n\nid, username :" + str(
                message.from_user.id) + " " + str(message.from_user.username))
            await bot.send_message(message.chat.id,
                                   "<b>Мы получили ваше сообщение, администрация вам ответит так скоро, как сможет, спасибо!</b>",
                                   parse_mode="html")
        elif "https://" in message.text:
            await bot.send_message(message.chat.id,
                                   "<b>Можете оставить эту ссылку тут) А вы не боитесь что ее кто-то украдет?)</b>",
                                   parse_mode="html")
        elif message.text == "AlphaShare":

            if len(os.listdir('ashare')) == 0:
                await message.answer(text="Похоже AlphaShare пуст, подождите пока кто-то выложит генерацию")
            else:
                db = sqlite3.connect('userbase.db')
                c = db.cursor()
                c.execute(f"SELECT * FROM users")
                db.commit()
                items = c.fetchall()
                db.close()
                for i in range(len(items)):
                    if str(items[i][0]) == str(message.from_user.id):
                        break
                msg = await bot.send_message(message.from_user.id, "Ищем арты, подождите пару секунд...")
                rch = random.choice(os.listdir("ashare"))
                i = 0
                while rch.split('rd')[0] == str(message.from_user.id) or rch == items[i][18]:
                    rch = random.choice(os.listdir("ashare"))
                    i += 1
                    if i > 10:
                        break
                        await call.answer(text="Похоже AlphaShare пуст, подождите пока кто-то выложит генерацию",
                                          show_alert=True)
                save_data_in_database("cur_alink", rch, message.from_user.id)
                gen_link = rch.split("rd")[1]
                ready_link = hlink("Сид к генерации", f"https://t.me/alphastabletbot?start={gen_link}")
                await bot.send_document(message.from_user.id, open("ashare\\" + rch, "rb"),
                                        caption=f"<b>✨ Случайная генерация</b>\n\n🌱 <b>{ready_link}</b>\n\n<i>Вы можете лайкнуть генерацию или продолжить просмотр нажав кнопку далее</i>",
                                        reply_markup=alphashare_contin_markup, parse_mode="html")
                await msg.delete()

        elif message.text == "/invite":
            await bot.send_message(message.chat.id,
                                   "🙋‍♂️ <b>Пригласи друга</b> \n\nЗа каждого приглашенного друга ты будешь получать 25 токенов. Используй ссылку ниже \n\n<code>https://t.me/alphastabletbot?start=" + str(
                                       message.from_user.id) + "</code>",
                                   parse_mode='html')

        elif message.text == "/persons":
            await bot.send_message(message.chat.id,
                                   "<b>Мы собрали галарею промтов по разным персонажам, можете попробовать кого-нибудь создать</b>\n\nhttps://telegra.ph/Alpha-Stable-personazhi-05-14",
                                   parse_mode="html")

        elif message.text == '/casino':
            items = get_items(message.from_user.id)
            if items[2] < 10:
                await bot.send_message(message.from_user.id, "*Похоже у вас слишком мало токенов, чтобы начать игру*",
                                       parse_mode='markdown')
            else:
                cancel_neg_markdown = InlineKeyboardMarkup(row_width=1)
                cancel_neg_button = InlineKeyboardButton(text="<< Назад", callback_data="cancel_neg")
                cancel_neg_markdown.add(cancel_neg_button)
                await bot.send_message(message.from_user.id,
                                       "💰 <b>Казино токенами</b>\n*<i>Вы можете преумножить свои токены! Но будьте осторожны)</i>\n\nМинимальная ставка - 10 токенов\n\n❌ Проигрыш - 80 процентов\n\n✅ Умножение в 1.4х - 19 процентов\n\n💰 Умножение в 4х - 1 процент\n\n<i>Следующим сообщением укажите сумму, на которую вы хотите сыграть:</i>",
                                       parse_mode='html', reply_markup=cancel_neg_markdown)
                await Form.casino.set()
        elif message.text == "/qr":
            t_link = link("Как правильно создать красивый QR код?", "https://telegra.ph/QR---kody-07-16")
            await bot.send_message(message.from_user.id,
                                   f"🔳 *Отправь мне арт из которого ты хочешь сделать QR-код*\n\nЕсли хочешь отменить создание QR-кода, просто отправь мне любой текст",
                                   parse_mode='markdown', disable_web_page_preview=True)
            await Form.qr_image.set()
        elif message.text == "/balance":

            items = get_items(message.from_user.id)

            token = "4100118356657505.657B2F10480AE81531DF02D685E4349F8F58546CA3D48B6F9A52F4BD6B83F1D6BBCC61CDB109199CF9C8A35D864E6D853779F65D2D06EA2541B8C10B2BA1056C988C81BC0EFEE9B4B7CD63B7D4C635361AC77889036745C9269176DFB970040859009F3F8E328A153417E521C1D3DF5F0D1147F77886DAC050D7F6BCF56C4E4C"

            client = Client(token)
            history = client.operation_history()
            for operation in history.operations:
                if str(operation.label) == str(message.from_user.id) + "::" + str(items[8]):
                    save_data_in_database("balance", int(items[2] + int(items[8].split('spl')[1])),
                                          message.from_user.id)
                    save_data_in_database("pay_token", 'empty', message.from_user.id)
                    break

            await bot.send_message(message.chat.id, "💲 <b>Ваш текущий баланс: </b>"
                                   + str(items[
                                             2]) + "\n\n1 генерация = 10 токенов\n\nЕсли ваш баланс меньше 15 токенов, то он автоматически пополнится до этой суммы через день.\n\n<i>Просьба"
                                                   " оплачивать по кнопке последнего сообщения в чате."
                                                   " После пополнения, обязательно пропишите /balance еще раз."
                                                   " В случае если вы купили токены,"
                                                   " но баланс не пополнился в течении 5 минут,"
                                                   " пропишите: \n\n<code>/a [Ваше обращение к"
                                                   " администрации]</code>\n\nУкажите ваш телеграмм ник в"
                                                   " обращении.</i>",
                                   parse_mode="html", reply_markup=choose_amount_markup)

            client = Client(token)
            history = client.operation_history(label=(str(message.from_user.id) + "::" + str(items[8])))
            for operation in history.operations:
                if str(operation.label) == str(message.from_user.id) + "::" + str(items[8]):
                    save_data_in_database("balance", items[2] + int(items[8].split('spl')[1]), message.from_user.id)

        elif message.text == "/send_users_uvd":
            print("test")
            db = sqlite3.connect('userbase.db')
            c = db.cursor()
            c.execute(f"SELECT id FROM users")
            db.commit()
            items_gen = c.fetchall()
            db.close()
            ch_link = link("канал AlphaStable", "https://t.me/stablealpha")
            i_link = link("\u200C", "https://t.me/stablealpha/815")

            for i in range(len(items_gen)):
                print(items_gen[i])

                try:
                    await bot.send_message(chat_id=int(str(items_gen[i]).replace("('", '').replace("',)", "")),
                                           text=f"{i_link}*Началась золотая лихорадка!*\n\nШансы на победу в /casino повышены. Гранд-выигрышь - 100x от поставленной суммы токенах!",
                                           parse_mode="markdown")
                except BotBlocked:
                    print("blocker by user")
        elif message.text == "supptest":
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"[\u200C](https://i.ibb.co/VmH9DpG/Frame-1-34.png)*Привет, {message.from_user.username}! Я - Alpha Audio*\n\nЯ могу скачать аудио файл с YouTube/YouTube Shorts по ссылке или по текстовому запросу.\nТакже, я могу найти текст песни по ее названию. \n\nБольше информации по использованию бота, вы сможете [найти тут](https://telegra.ph/Alpha-Audio-rukovodstvo-09-16) и в [нашем канале](https://t.me/alpha_audio), а для быстрого поиска трека, просто пропиши /search и название трека",
                                   parse_mode='markdown')
        elif message.text == "/gift":
            create_gift_markup = InlineKeyboardMarkup(row_width=2)
            back_gift_button = InlineKeyboardButton(text="Отмена", callback_data="CANCEL_GIFT")
            create_gift_button = InlineKeyboardButton(text="Создать подарок", callback_data="CREATE_GIFT")
            create_gift_markup.add(back_gift_button, create_gift_button)

            await bot.send_message(message.chat.id,
                                   "🎁* Вы можете создать ссылку с подарком с токенами. *\n\nЕсли ее откроет пользователь бота, то ему будут начислены токены которые вы ему отправили!\n\n",
                                   parse_mode="markdown", reply_markup=create_gift_markup)

        else:
            if len(message.text) > 600:
                await bot.send_message(message.chat.id,
                                       "Слишком длинный ввод. Максимальная длина ввода - 500 символов",
                                       parse_mode="markdown")
            else:
                await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
                db = sqlite3.connect('prompts.db')
                c = db.cursor()

                negative_t = message.text

                # messages = [
                #     {"role": "system",
                #      "content": "you will be provided with image descriptions. translate each query into danbooru tags. answer with danbooru tags. be verbose. if describing several people with different appearances, put each one on a separate line. Don't use special signs and symbols like _ * and -. Always be sure to answer in English! In English only. example of answer: 1girl, solo, beatiful, red hairs. Example for several people: 2people, hug\n\n1girl\n\n1boy"}]
                # messages.append({"role": "user",
                #                  "content":
                #                      message.text})
                # completion = openai.ChatCompletion.create(
                #     model="gpt-3.5-turbo-instruct-0914",
                #     messages=messages,
                #     temperature=0.6
                # )
                # chat_response = completion.choices[0].message.content
                # prompt = chat_response

                prompt = negative_t
                '''def check_mat_en(text):
                    with open("en_profane_words.txt", "r") as file:
                        a = [line[:-1] for line in file]
                        for i in range(len(a)):
                            if a[i] in text:
                                status = False
                                return False
                                break
                            else:
                                status = True

                    return True
                print(prompt)
                if has_cyrillic(message.text) and check_mat_en(prompt.lower()):
                    messages = [
                        {"role": "system",
                         "content": "you will be provided with image descriptions. translate each query into danbooru tags. answer with danbooru tags. be verbose. if describing several people with different appearances, put each one on a separate line. Don't use special signs and symbols like _ * and -. Always be sure to answer in English! In English only. example of answer: 1girl, solo, beatiful, red hairs. Example for several people: 2people, hug\n\n1girl\n\n1boy"}]
                    messages.append({"role": "user",
                                     "content":
                                         prompt})
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-0613",
                        messages=messages,
                        temperature=0.6
                    )
                    chat_response = completion.choices[0].message.content
                    prompt = chat_response'''

                # time = datetime.time()
#
                # param = (str(prompt), str(time))
                # c.execute(f"INSERT INTO prompts VALUES (?, ?)", param)
                # db.commit()
                # print(prompt)
                # db.close()
                save_data_in_database('pose_status', 0, message.from_user.id)
                await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
                items = get_items(message.from_user.id)

                cur_model = items[5]
                cur_resol = items[6]

                save_data_in_database("raw_promt", prompt, message.from_user.id)
                save_data_in_database("promt", prompt, message.from_user.id)
                rp2 = ReplyKeyboardMarkup(resize_keyboard=True)
                rp2_button = KeyboardButton(text="Стили", web_app=WebAppInfo(url='https://innoky.github.io/#'))
                button_1 = types.KeyboardButton(text="AlphaShare")
                rp2.add(button_1, rp2_button)

                text = link('подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
                # await bot.send_photo(message.chat.id, photo="https://i.ibb.co/KVv7rvH/914029246rd-659.png",
                #                      caption=f"""☺️*Мы готовы сгенерировать ваш запрос:*\n\n`{message.text}`\n\n- {text}\n\n*Советуем использовать GPT edit для лучшего результата*\n\nТекущая модель: **{cur_model}**\nРазрешение: **{cur_resol}**""",
                #                      reply_to_message_id=message.message_id,
                #                      parse_mode='markdown', reply_markup=propmt_markup)
                ms = await bot.send_message(chat_id=message.from_user.id, text=f"✏️ *Вы ввели:* `{message.text}`",
                                            reply_markup=rp2, parse_mode='markdown')
                txt = replace_description_txt2img(model=cur_model,
                                                  prompt=prompt,
                                                  resolution=cur_resol)
                mss = await bot.send_message(message.chat.id, text=txt,
                                             reply_to_message_id=message.message_id, parse_mode='markdown',
                                             reply_markup=propmt_markup, disable_web_page_preview=True)
                save_data_in_database("last_msg_id", mss.message_id, message.from_user.id)
                save_data_in_database("cur_settings", txt, message.from_user.id)


@dp.callback_query_handler()
async def func1(call: types.CallbackQuery, state: FSMContext):
    model = json.loads(open("model_json/model_info.json", encoding="utf-8").read())
    resolution = json.loads(open("model_json/resolution_info.json", encoding="utf-8").read())
    # style = json.loads(open("model_json/style.json", encoding="utf-8").read())
    # strength = json.loads(open("model_json/strength.json", encoding="utf-8").read())
    if str(call.from_user.id) not in get_all_user_id():
        await bot.send_message(call.message.chat.id,
                               "Мы не нашли вас в базе пользователей, пожалуйста, пропишите /start")
    else:
        if call.data in model.keys():
            save_data_in_database("cur_model", call.data, call.from_user.id)
            input_file = replace_description_model(call.data)
            if call.data in ("Dark Alpha", "Light Alpha", "3DAlpha"):
                await call.message.edit_text(input_file, reply_markup=choose_model_alpha_markup, parse_mode="markdown")
            else:
                await call.message.edit_text(input_file, reply_markup=choose_model_markup, parse_mode="markdown")
        elif call.data == "Alpha":

            i_link = link("\u200C", "https://telegra.ph/file/a6df906b22412c27718b5.png")
            text_alpha = f"{i_link}*Alpha (2/2)*\n\n_Вы можете выбрать одну из двух моделей Alpha. Каждая из них по особенному красива и имеет свою изюминку._"
            await call.message.edit_text(text=text_alpha, reply_markup=choose_model_alpha_markup, parse_mode="markdown")
        elif call.data in resolution.keys():
            save_data_in_database("resol", call.data, call.from_user.id)
            input_file = InputMedia(type="photo", media=resolution[call.data]["image"],
                                    caption=f"<b>{call.data}</b>", parse_mode="html")
            i_link = link("\u200C", resolution[call.data]["image"])
            text_resol = f"{i_link}*{call.data}*"
            await call.message.edit_text(text_resol, reply_markup=choose_resolution_markup, parse_mode="markdown")
        elif call.data in ("choose_model", "back_button"):
            if call.data == "choose_model":
                text_m = call.message.text
                save_data_in_database("cur_settings", text_m, call.from_user.id)
            items = get_items(call.from_user.id)
            await call.message.edit_text(replace_description_model(items[5]), reply_markup=choose_model_markup,
                                         parse_mode="markdown")
        elif call.data in ("save_resol_button", "save_model_button", "save_style"):
            items = get_items(call.from_user.id)
            settings_dict = get_settings_ready_txt2img(items[20])
            resol_m = settings_dict["resol"]
            model_m = settings_dict["model"]
            style_m = settings_dict["style"]
            prompt_m = settings_dict["prompt"]
            if call.data == "save_resol_button":
                resol_m = items[6]
            elif call.data == "save_model_button":
                model_m = items[5]
            elif call.data == "save_style":
                style_m = items[19]
                prompt_m = items[7]
            text_commit = replace_description_txt2img(model=model_m, resolution=resol_m, seed=settings_dict["seed"],
                                                      prompt=prompt_m,
                                                      negative=settings_dict["negative"], style=style_m)
            await call.message.edit_text(text=text_commit, reply_markup=propmt_markup, parse_mode="markdown",
                                         disable_web_page_preview=True)
        elif call.data == "CANCEL_GIFT":
            await call.message.delete()
        elif call.data == "CREATE_GIFT":
            cancel_neg_markdown = InlineKeyboardMarkup(row_width=1)
            cancel_neg_button = InlineKeyboardButton(text="Отмена", callback_data="cancel_neg")
            cancel_neg_markdown.add(cancel_neg_button)
            await call.message.edit_text(
                text="💰 *Введите сумму для подарка*\n\nУказанная сумма начислится тому, кому вы отправите подарок. Активировать самому этот подарок не выйдет.",
                parse_mode="markdown", reply_markup=cancel_neg_markdown)
            await Form.gift_amount.set()
        elif call.data == "resolution":
            text_m = call.message.text
            save_data_in_database("cur_settings", text_m, call.from_user.id)
            file_resol = InputMedia(type="photo",
                                    media="https://i.ibb.co/DM3L2Yd/Frame-2-2023-05-09-T155404-006.png",
                                    caption="<b>Доступно три варианта: Квадрат, портрет, альбом</b>",
                                    parse_mode="html")
            i_link = link("\u200C", "https://i.ibb.co/DM3L2Yd/Frame-2-2023-05-09-T155404-006.png")
            text_resol = f"{i_link}*Доступно три варианта: Квадрат, портрет, альбом*"
            await call.message.edit_text(text_resol, reply_markup=choose_resolution_markup, parse_mode="markdown")
        elif call.data == 'style':
            text_m = call.message.text
            save_data_in_database("cur_settings", text_m, call.from_user.id)
            file_styles = InputMedia(type="photo", media="https://i.ibb.co/BCqL6g3/Frame-1-87.png",
                                     caption="🎉 *Теперь вы можете выбрать стиль прямо в меню, а не вводить его в промте*\n\nПросто нажми на нужный тебе стиль и нажми *Сохранить*",
                                     parse_mode='markdown')
            link_i = link("\u200C", "https://i.ibb.co/BCqL6g3/Frame-1-87.png")
            text_i = f"{link_i}🎉 *Теперь вы можете выбрать стиль прямо в меню, а не вводить его в промте*\n\nПросто нажми на нужный тебе стиль и нажми *Сохранить*"
            await call.message.edit_text(text_i, reply_markup=styles_markup, parse_mode="markdown")
        elif call.data == "ragemode_chooser":
            await call.message.edit_reply_markup(rage_markup)
        elif call.data in style.keys():
            st(call.data, call.from_user.id)
            save_data_in_database("style", call.data, call.from_user.id)
            await call.message.edit_text(replace_description_style(call.data), reply_markup=styles_markup,
                                         parse_mode="markdown")
        elif call.data in strength.keys():
            save_data_in_database("streight", int(call.data), call.from_user.id)
            file_streight = InputMedia(type="photo",
                                       media=open(f'outs/{call.from_user.id}/{call.from_user.id}raw.jpg', 'rb'),
                                       caption=f"*Доступно пять вариантов сил*\n\nВыбрано:"
                                               f" {strength[call.data]['desc']}")
            await call.message.edit_media(file_streight, reply_markup=choose_streight_markup)
        elif call.data == "upscale":
            await call.message.delete()
            itemsss = get_items(call.from_user.id)
            if int(itemsss[2]) > 20 and str(itemsss[3]) == "0":
                async with state.proxy() as data:
                    msg_id = data['msg_id_hqsu']
                    file_name = msg_id.document.file_name
                db = sqlite3.connect('userbase.db')
                c = db.cursor()
                c.execute(f"SELECT * FROM users")
                db.commit()
                items_gen = c.fetchall()
                db.close()
                sum_time = 1
                for i in range(len(items_gen)):
                    sum_time = sum_time + int(items_gen[i][3])
                sum_time = str((sum_time * 15) - 15 + 35)
                items = get_items(call.from_user.id)
                save_data_in_database('status', 1, call.from_user.id)
                if not (str(items[0]) in ("1430025958", "415356744")):
                    save_data_in_database('balance', items[2] - 20, call.from_user.id)
                ms = await bot.send_message(chat_id=call.from_user.id,
                                            text=f'<b>Генерация началась.</b> \n\n<i>Время ожидания ~{sum_time} секунд(ы). Иногда это может занимать больше времени из-за структуры серверов. Бот самостоятельно отправит вам результат. Также заходите в наш чат, там мы делимся генерациями и просто приятно общаемся</i>',
                                            reply_markup=keyboard_ashare,
                                            parse_mode="html")
                save_data_in_database("edit_last", ms.message_id, call.from_user.id)

                p2 = Process(target=upscale_start, args=(call.from_user.id, file_name))
                p2.start()
            else:
                if str(itemsss[3]) != "0":
                    await call.answer(
                        "Вы уже генерируете что-то, попробуйте позже.",
                        show_alert=True)
                else:
                    await bot.send_message(chat_id=call.from_user.id,
                                           text="*К сожалению у вас недостаточно токенов*\nПропишите /balance для большей информации",
                                           parse_mode="markdown")

        elif call.data == 'write_history':
            await call.message.answer(text="✍ *Начали писать историю...*",
                                      parse_mode='markdown')
            items = get_items(call.from_user.id)
            print(items[7])
            messages = [
                {"role": "system",
                 "content": "You need to write a story based on the tags given to you. Let the story not exceed 5 sentences. Be creative and come up with an interesting story. Write the entire text in Russian. "}]

            messages.append({"role": "user",
                             "content": items[7]})

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            result = completion.choices[0].message.content
            await call.message.answer(text="*✍ Мы написали историю к арту, вот она:*\n\n" + result,
                                      parse_mode='markdown')
        elif call.data == 'play_casino':
            items = get_items(call.from_user.id)
            amount = items[21]
            roll_num = random.randint(0, 100)
            if roll_num <= 5:
                await call.message.edit_text(
                    text="❌ *К сожалению вы проиграли.* \n\nПопробуйте еще раз, у вас есть шанс отыграться\n\n/casino",
                    parse_mode='markdown')
                save_data_in_database("balance", int(items[2]) - int(amount), call.from_user.id)

            elif roll_num > 6:
                await call.message.edit_text(
                    text=f"✅ *Да вы везунчик, вы выиграли {int(round(amount * 10))} токенов!* \n\nВы похоже вышли на победную дорожку!\n\n/casino",
                    parse_mode='markdown')
                save_data_in_database("balance", items[2] + int(round(amount * 10)), call.from_user.id)
            print(roll_num)
        elif call.data == 'save_str':
            items = get_items(call.from_user.id)
            file_streight_commit = InputMedia(type="photo",
                                              media=open(f'outs/{call.from_user.id}/{call.from_user.id}raw.jpg',
                                                         'rb'),
                                              caption=f"**🥳 Теперь ты можешь перевести свое фото в аниме!**\n\n"
                                                      f" Просто жми кнопку **Сгенерировать**.\n\n"
                                                      f"🤖 **Auto Промт**: `{items[7]}`\n\n"
                                                      f"*Сила:* {strength[str(items[17])]['name']}",
                                              parse_mode='markdown')
            await call.message.edit_media(file_streight_commit,
                                          reply_markup=propmt_markup_img)
        elif call.data == "streight":
            textl = hlink("*подробнее тут", 'https://telegra.ph/Primery-sil-Img2Img-06-18')
            await call.message.edit_caption(f"Выберите силу действия эффекта: \n\n{textl}", parse_mode="html",
                                            reply_markup=choose_streight_markup)
        elif call.data == "tf_button":
            items = get_items(call.from_user.id)
            current_time = str(t.time()) + "spl" + "50"
            save_data_in_database("pay_token", current_time, call.from_user.id)

            quickpay = Quickpay(
                receiver="4100118356657505",
                quickpay_form="shop",
                targets="Alpha tokens",
                paymentType="SB",
                sum=25,
                label=str(call.from_user.id) + '::' + str(current_time)
            )
            pay_link = quickpay.redirected_url

            pay_link_markup = InlineKeyboardMarkup()
            pay_link_button = InlineKeyboardButton(text='Оплатить', url=pay_link)
            pay_link_markup.row(pay_link_button).row(back_balance_button)
            await call.message.edit_text(
                text="*Преобрести 50 токенов за 25 рублей*\n\nДля совершения оплаты, нажмите кнопку ниже",
                parse_mode='markdown', reply_markup=pay_link_markup)
        elif call.data == "f_button":
            items = get_items(call.from_user.id)
            current_time = str(t.time()) + "spl" + "100"
            save_data_in_database("pay_token", current_time, call.from_user.id)

            quickpay = Quickpay(
                receiver="4100118356657505",
                quickpay_form="shop",
                targets="Alpha tokens",
                paymentType="SB",
                sum=49,
                label=str(call.from_user.id) + '::' + str(current_time)
            )

            pay_link = quickpay.redirected_url

            pay_link_markup = InlineKeyboardMarkup()
            pay_link_button = InlineKeyboardButton(text='Оплатить', url=pay_link)
            pay_link_markup.row(pay_link_button).row(back_balance_button)
            await call.message.edit_text(
                text="*Преобрести 100 токенов за 49 рублей*\n\nДля совершения оплаты, нажмите кнопку ниже",
                parse_mode='markdown', reply_markup=pay_link_markup)
        elif call.data == "nf_button":
            items = get_items(call.from_user.id)
            current_time = str(t.time()) + "spl" + "200"
            save_data_in_database("pay_token", current_time, call.from_user.id)

            quickpay = Quickpay(
                receiver="4100118356657505",
                quickpay_form="shop",
                targets="Alpha tokens",
                paymentType="SB",
                sum=90,
                label=str(call.from_user.id) + '::' + str(current_time)
            )
            pay_link = quickpay.redirected_url

            pay_link_markup = InlineKeyboardMarkup()
            pay_link_button = InlineKeyboardButton(text='Оплатить', url=pay_link)
            pay_link_markup.row(pay_link_button).row(back_balance_button)
            await call.message.edit_text(
                text="*Преобрести 200 токенов за 90 рублей*\n\nДля совершения оплаты, нажмите кнопку ниже",
                parse_mode='markdown', reply_markup=pay_link_markup)
        elif call.data == "ohf_button":
            items = get_items(call.from_user.id)
            current_time = str(t.time()) + "spl" + "300"
            save_data_in_database("pay_token", current_time, call.from_user.id)

            quickpay = Quickpay(
                receiver="4100118356657505",
                quickpay_form="shop",
                targets="Alpha tokens",
                paymentType="SB",
                sum=149,
                label=str(call.from_user.id) + '::' + str(current_time)
            )

            pay_link = quickpay.redirected_url

            pay_link_markup = InlineKeyboardMarkup()
            pay_link_button = InlineKeyboardButton(text='Оплатить', url=pay_link)
            pay_link_markup.row(pay_link_button).row(back_balance_button)
            await call.message.edit_text(
                text="*Преобрести 300 токенов за 149 рублей*\n\nДля совершения оплаты, нажмите кнопку ниже",
                parse_mode='markdown', reply_markup=pay_link_markup)
        elif call.data == 'back_balance_button':
            items = get_items(call.from_user.id)
            await call.message.edit_text("💲 <b>Ваш текущий баланс: </b>"
                                         + str(items[2]) + "\n\n1 генерация = 10 токенов\n\n<i>Просьба"
                                                           " оплачивать по кнопке последнего сообщения в чате."
                                                           " После пополнения, обязательно пропишите /balance еще раз."
                                                           " В случае если вы купили токены,"
                                                           " но баланс не пополнился в течении 5 минут,"
                                                           " пропишите: \n\n<code>/a [Ваше обращение к"
                                                           " администрации]</code>\n\nУкажите ваш телеграмм ник в"
                                                           " обращении.</i>",
                                         parse_mode="html", reply_markup=choose_amount_markup)

        elif call.data == 'stay_promt':
            text_m = call.message.text
            s = get_settings_ready_txt2img(text_m)
            items = get_items(call.from_user.id)
            messages = [
                {"role": "system",
                 "content": "you will be provided with image descriptions. translate each query into danbooru tags. be verbose. if describing several people with different appearances, put each one on a separate line. Always be sure to answer in English! In English only."}]
            messages.append({"role": "user",
                             "content":
                                 s["prompt"]})
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                temperature=0.9
            )
            chat_response = completion.choices[0].message.content
            promt_global = chat_response
            save_data_in_database("promt", promt_global, str(call.from_user.id))
            file = InputMedia(type='photo', media="https://i.ibb.co/KVv7rvH/914029246rd-659.png",
                              caption=f"""☺️*Мы готовы сгенерировать ваш запрос:*\nПромт: `{promt_global}` \n\nТекущая модель: **{items[5]}\nРазрешение: {items[6]}**""",
                              parse_mode='markdown', reply_markup=propmt_markup)
            text_i = replace_description_txt2img(model=s["model"], prompt=promt_global, seed=s["seed"],
                                                 resolution=s["resol"], style=s["style"], negative=s["negative"])
            await call.message.edit_text(text_i, reply_markup=propmt_markup, parse_mode="markdown",
                                         disable_web_page_preview=True)
        elif call.data == 'zoom':
            items = get_items(call.from_user.id)
            if int(items[2]) < 25:

                await bot.send_message(chat_id=call.from_user.id,
                                       text="*К сожалению у вас недостаточно токенов*\nПропишите /balance для большей информации",
                                       parse_mode="markdown")
            else:
                zoom_choose_markup = InlineKeyboardMarkup(row_width=2)
                horizontal_button_zoom = InlineKeyboardButton(text="Горизонтально", callback_data="horizontal_zoom")
                vertical_button_zoom = InlineKeyboardButton(text="Вертикально", callback_data="vertical_zoom")
                all_button_zoom = InlineKeyboardButton("Во все стороны", callback_data="all_zoom")
                zoom_choose_markup.add(horizontal_button_zoom, vertical_button_zoom, all_button_zoom)
                await bot.send_message(chat_id=call.from_user.id,
                                       text="*Выберите стороны в которые хотите расширить кадр*\n\nПри выборе расширения кадра во все стороны, могут возникать артефакты из-за сложности подбора нужного промта.",
                                       parse_mode="markdown", reply_markup=zoom_choose_markup)
        elif call.data == "make_better":
            link_su = link("🔥 SuperUpscale", "https://t.me/stablealpha/335")
            link_hq = link("⬆️ Hquality", "https://t.me/stablealpha/145")
            async with state.proxy() as data:
                data['msg_id_hqsu'] = call.message
            await bot.send_message(chat_id=call.from_user.id,
                                   text=f"{link_su} - функция позволяющая увеличить разрешение и качество полученного арта. Замыленные места станут четче, улучшится прорисовка лиц.\n\n{link_hq} - функция позволяет сделать новую генерацию с заметно четкими контурами, огромным количеством деталей и большим разрешением.\n\n*1 SuperUpscale - 20 токенов*\n*1 Hquality - 15 токенов*",
                                   parse_mode="markdown", reply_to_message_id=call.message.message_id,
                                   reply_markup=hq_and_su_markup, disable_web_page_preview=True)
        elif call.data == "back_hqandsu":
            await call.message.delete()
        elif call.data in ("horizontal_zoom", "vertical_zoom", "all_zoom"):
            if call.data == "horizontal_zoom":
                save_data_in_database('zoom_status', 1, call.from_user.id)
            elif call.data == "vertical_zoom":
                save_data_in_database('zoom_status', 2, call.from_user.id)
            elif call.data == "all_zoom":
                save_data_in_database('zoom_status', 0, call.from_user.id)

            zoom_scale_markup = InlineKeyboardMarkup(row_width=3)
            ohte_zoom = InlineKeyboardButton(text="64 px", callback_data="64px")
            thfs_zoom = InlineKeyboardButton(text="128 px", callback_data="128px")
            fht_zoom = InlineKeyboardButton(text="256 px", callback_data="256px")
            zoom_scale_markup.add(ohte_zoom, thfs_zoom, fht_zoom)
            await call.message.edit_text(
                text="*Выберите на сколько вы хотите расширить изображение*\n\nПри выборе большого значения, результат может быть хуже, чем при меньшем значении.",
                reply_markup=zoom_scale_markup, parse_mode="markdown")
        elif call.data in ("64px", "128px", "256px"):
            if call.data == "64px":
                save_data_in_database('zoom_scale', 64, call.from_user.id)
            elif call.data == "128px":
                save_data_in_database('zoom_scale', 128, call.from_user.id)
            elif call.data == "256px":
                save_data_in_database('zoom_scale', 256, call.from_user.id)
            link_text = link("эту статью", 'https://telegra.ph/ZOOM-07-20-4')
            await call.message.edit_text(
                text=f"*Введите промт*\n\nУкажите в нем то, что вы хотели бы увидеть в новом кадре.\n\nТе кто пользуется фунцией впервые, убедительная просьба прочитать {link_text}. От промта зависит 50% результата.",
                parse_mode='markdown', disable_web_page_preview=True)
            await Form.zoom_prompt.set()
        elif call.data in ("start_gen", "restart_gen", "hquality"):
            items = get_items(call.from_user.id)
            if items[3] == 1:
                await call.answer(
                    "Вы уже генерируете что-то, попробуйте позже.",
                    show_alert=True)
            else:
                tokens = 10
                if call.data == "hquality":
                    tokens = 15
                settings = dict()
                if call.data == "start_gen":
                    settings = get_settings_ready_txt2img(call.message.text)
                elif call.data in ("restart_gen", "hquality"):
                    if call.data == "hquality":
                        async with state.proxy() as data:
                            msg_id = data['msg_id_hqsu']
                            settings = get_settings_get_txt2img(msg_id.caption)
                    else:
                        settings = get_settings_get_txt2img(call.message.caption)
                if items[2] < tokens:
                    await call.message.answer(
                        "*К сожалению у вас кончились токены*\n\nВы можете преобрести их у нас в меню, либо пригласить друга в бота по реферальной ссылке, её тоже можно найти в меню",
                        parse_mode='markdown')
                else:
                    if call.data == "start_gen":
                        await call.message.delete()
                    db = sqlite3.connect('userbase.db')
                    c = db.cursor()
                    c.execute(f"SELECT * FROM users")
                    db.commit()
                    items_gen = c.fetchall()
                    db.close()
                    sum_time = 1
                    if call.data in ("start_gen", "restart_gen"):
                        for i in range(len(items_gen)):
                            sum_time = sum_time + int(items_gen[i][3])
                        sum_time = str(sum_time * 15)
                    elif call.data == "hquality":
                        for j in range(len(items_gen)):
                            sum_time = sum_time + int(items_gen[j][3])
                        sum_time = str(sum_time * 10 - 10 + 28)

                    if call.data == "restart_gen":
                        h_l = hlink("наш чат", "")
                        ms = await call.message.answer(
                            f'<b>Перегенерация началась.</b> \n\n<i>Время ожидания ~{sum_time} секунд(ы). Бот самостоятельно отправит вам результат. Иногда это может занимать больше времени из-за структуры серверов. Также заходите в наш чат, там мы делимся генерациями и просто приятно общаемся</i>',
                            reply_markup=keyboard_ashare,
                            parse_mode="html")
                        save_data_in_database("edit_last", ms.message_id, call.from_user.id)
                    elif call.data == "hquality":
                        await call.message.delete()
                        ms = await bot.send_message(chat_id=call.from_user.id,
                                                    text=f'⬆️ *Детализация началась.*\n\nВремя ожидания ~{sum_time} секунд(ы). Иногда это может занимать больше времени из-за структуры серверов. Бот самостоятельно отправит вам результат.',
                                                    reply_markup=keyboard_ashare, parse_mode="markdown")
                        save_data_in_database("edit_last", ms.message_id, call.from_user.id)
                    else:
                        ms = await call.message.answer(
                            f'<b>Генерация началась.</b> \n\n<i>Время ожидания ~{sum_time} секунд(ы). Иногда это может занимать больше времени из-за структуры серверов. Бот самостоятельно отправит вам результат. Также заходите в наш чат, там мы делимся генерациями и просто приятно общаемся</i>',
                            reply_markup=keyboard_ashare,
                            parse_mode="html")
                        save_data_in_database("edit_last", ms.message_id, call.from_user.id)
                    save_data_in_database("status", 1, call.from_user.id)
                    if call.data == "hquality":
                        if not (str(items[0]) in ("1430025958", "415356744")):
                            save_data_in_database("balance", items[2] - 15, call.from_user.id)

                    else:
                        if not (str(items[0]) in ("1430025958", "415356744")):
                            if (str(items[0]) in ("943447764")) and items[5] in ("Omega"):
                                print("Unlimited")
                            elif (str(items[0]) in ("6134392324", "914029246")) and items[5] in (
                            "Omicron", "3DAlpha", "Omega"):
                                print("ULIMITED")
                            else:
                                save_data_in_database("balance", items[2] - 10, call.from_user.id)
                    model_m = settings["model"]
                    resol_m = settings["resol"]
                    seed_m = settings["seed"]
                    style_m = settings["style"]
                    negative_m = settings["negative"]
                    prompt_m = settings["prompt"]
                    hq = call.data == "hquality"
                    p = Process(target=generate, args=(prompt_m, model_m, resol_m, call.from_user.id, style_m, hq,
                                                       seed_m, negative_m, call.data == "restart_gen"))
                    print(call.from_user.username)
                    p.start()

                    # prompt, model, resol, user_id, style, hq=False, seed=-1, negative=""
        #elif call.data == "check_gen":
#
        #    api_key = "8FDMB6CCISMARJK4C6LP24GPCGI59MUAS1UEPXIF"
        #    items = get_items(call.from_user.id)
        #    job_id = items[27]
#
        #    res = requests.post(url=f'https://api.runpod.ai/v2/r9puknkh1poi7d/status/{job_id}',
        #                        auth=BearerAuth(f'{api_key}'))
        #    if job_id == "empty":
        #        await call.answer(
        #            text="✅ Начинаем генерацию...",
        #            show_alert=True)
        #    elif job_id == "error":
        #        save_data_in_database("status", 0, call.from_user.id)
        #        save_data_in_database("hquality", 0, call.from_user.id)
        #        itemss = get_items(call.from_user.id)
        #        save_data_in_database("balance", int(itemss[2]) + 20, call.from_user.id)
        #        print("request does not exist")
        #        await call.answer(
        #            text="❌ Похоже во время генерации произошел сбой. \nМы вернули вам возможность заново начать генерацию, а также начислили токенов в качестве компенсации.",
        #            show_alert=True)
        #        await call.message.delete()
        #    else:
        #        if "request does not exist" in res.text:
        #            save_data_in_database("status", 0, call.from_user.id)
        #            save_data_in_database("hquality", 0, call.from_user.id)
        #            itemss = get_items(call.from_user.id)
        #            save_data_in_database("balance", int(itemss[2]) + 20, call.from_user.id)
        #            print("request does not exist")
        #            await call.answer(
        #                text="❌ Похоже во время генерации произошел сбой. \nМы вернули вам возможность заново начать генерацию, а также начислили токенов в качестве компенсации.",
        #                show_alert=True)
        #            await call.message.delete()
        #        elif "IN_PROGRESS" in res.text:
        #            print("IN_PROGRESS")
        #            await call.answer(
        #                text="🔥 С вашим артом все хорошо. \nОн находится в очереди на генерацию либо уже генерируется. Если результат не прийдет через несколько минут, нажмите на эту кнопку еще раз.",
        #                show_alert=True)
        #        else:
        #            save_data_in_database("status", 0, call.from_user.id)
        #            save_data_in_database("hquality", 0, call.from_user.id)
        #            itemss = get_items(call.from_user.id)
        #            save_data_in_database("balance", int(itemss[2]) + 20, call.from_user.id)
        #            print("request does not exist")
        #            await call.answer(
        #                text="❌ Похоже во время генерации произошел сбой. \nМы вернули вам возможность заново начать генерацию, а также начислили токенов в качестве компенсации.",
        #                show_alert=True)
        #            await call.message.delete()

        elif call.data == "negative":
            text_m = call.message.text
            save_data_in_database("cur_settings", text_m, call.from_user.id)
            cancel_neg_markdown = InlineKeyboardMarkup(row_width=1)
            cancel_neg_button = InlineKeyboardButton(text="<< Назад", callback_data="cancel_neg")
            cancel_neg_markdown.add(cancel_neg_button)
            await call.message.edit_text(
                text="🙅‍ *Негатив* позволят убрать с генерации нежелательные вещи, которые вы не хотите видеть на результате.\n\n*Просьба учитывать*, что мы по стандарту оптимизировали негатив. Не нужно вводить вещи по типу (bad hands, worst hands), мы это сделали сами!)\n\n// Будьте конкретны в своем вводе. Текст также можно вводить на русском языке.\n\n❌ *Введите негативный промт следующим сообщением:*",
                parse_mode="markdown", reply_markup=cancel_neg_markdown)

            async with state.proxy() as data:
                data['msg_id_neg'] = call.message
            await Form.negative_wait.set()



        elif call.data == "seed":
            text_m = call.message.text
            save_data_in_database("cur_settings", text_m, call.from_user.id)
            cancel_neg_markdown = InlineKeyboardMarkup(row_width=1)
            cancel_neg_button = InlineKeyboardButton(text="<< Назад", callback_data="cancel_neg")
            cancel_neg_markdown.add(cancel_neg_button)
            await call.message.edit_text(
                "🌱 *Сид - это целое число, которое задает ( основу для генерации )* \n\nВведя сюда сид из другой генерации и использовав близкий по смыслу промт, вы сможете получить очень схожий результат, правда это относится только к одинаковым моделям.\n\n*Введите сид следующим сообщением:*",
                parse_mode="markdown", reply_markup=cancel_neg_markdown)
            async with state.proxy() as data:
                data['seed_id'] = call.message.message_id
            await Form.seed_state.set()
        elif call.data == "ref_mode":

            choose_ref_mode = InlineKeyboardMarkup(row_width=1)
            reference = InlineKeyboardButton(text="Референс", callback_data="pose")
            masked_text = InlineKeyboardButton(text="Скрытый референс", callback_data="hidden_text")
            qr_code = InlineKeyboardButton(text="QR код", callback_data="qr_hidden")
            cancel_neg_button = InlineKeyboardButton(text="<< Назад", callback_data="back_ref")
            choose_ref_mode.row(qr_code, masked_text).row(cancel_neg_button)
            f_link = link("Референс", "https://telegra.ph/Generaciya-po-referensu-07-13")
            h_link = link("Скрытый референс", "https://telegra.ph/Skrytyj-tekst--referens-07-26")
            await call.message.edit_text(
                text=f"*Выберите один из предложеных вариантов.* \n\n{f_link} позволяет создать генерацию, в которой будет частично взята поза, расположение интерьера и цвета из отправленого изображения.\n\n{h_link} позволяет вписать текст в изображение. При первом взгляде его можно и не заметить, но стоит зажмурить глазки, как произойдет магия!",
                disable_web_page_preview=True,
                parse_mode='markdown', reply_markup=choose_ref_mode)
        elif call.data == "qr_hidden":
            cancel_neg_markdown = InlineKeyboardMarkup(row_width=1)
            cancel_neg_button = InlineKeyboardButton(text="<< Назад", callback_data="cancel_neg")
            cancel_neg_markdown.add(cancel_neg_button)

            msg = await call.message.edit_text(
                text="🔲 *Отправьте текст для зашифровки в QR-код*",
                disable_web_page_preview=True,
                parse_mode='markdown', reply_markup=cancel_neg_markdown)
            async with state.proxy() as data:
                data['qr_text_id'] = msg.message_id
            await Form.qr_hidden_text.set()
        elif call.data == "back_ref":
            items = get_items(call.from_user.id)

            cur_model = items[5]
            cur_resol = items[6]

            text = link('подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
            # await bot.send_photo(message.chat.id, photo="https://i.ibb.co/KVv7rvH/914029246rd-659.png",
            #                      caption=f"""☺️*Мы готовы сгенерировать ваш запрос:*\n\n`{message.text}`\n\n- {text}\n\n*Советуем использовать GPT edit для лучшего результата*\n\nТекущая модель: **{cur_model}**\nРазрешение: **{cur_resol}**""",
            #                      reply_to_message_id=message.message_id,
            #                      parse_mode='markdown', reply_markup=propmt_markup)
            await call.message.edit_text(text=replace_description_txt2img(model=cur_model,
                                                                          prompt=items[7],
                                                                          resolution=cur_resol),
                                         parse_mode='markdown',
                                         reply_markup=propmt_markup, disable_web_page_preview=True)
        elif call.data == "hidden_text":
            cancel_neg_markdown = InlineKeyboardMarkup(row_width=1)
            cancel_neg_button = InlineKeyboardButton(text="<< Назад", callback_data="cancel_neg")
            cancel_neg_markdown.add(cancel_neg_button)
            lk = link("\u200C", "https://telegra.ph/file/47633aace2b91b102cb11.png")
            ht = link("❓ Как воспользоваться этим черным фоном?", "https://telegra.ph/Skrytyj-referens-08-01")
            msg = await call.message.edit_text(
                text=f"🔠{lk} *Отправьте изображение с тектом или ч/б рисунком.* \n\nУбедитесь что на изображении хорошо виден текст, также убедитесь что фон - черного цвета, а желаемый референс - белого\n\n{ht}",
                disable_web_page_preview=False,
                parse_mode='markdown', reply_markup=cancel_neg_markdown, )
            async with state.proxy() as data:
                data['text_id'] = msg.message_id
            await Form.text.set()
        elif call.data == "pose":
            cancel_neg_markdown = InlineKeyboardMarkup(row_width=1)
            cancel_neg_button = InlineKeyboardButton(text="<< Назад", callback_data="cancel_neg")
            cancel_neg_markdown.add(cancel_neg_button)
            msg = await call.message.edit_text(
                text="🕺 *Отправьте референс-изображение.* \n\nУбедитесь что на изображении хорошо видны конечности, также убедитесь что ваш промт подчеркивает референс, дает исчерпывающую информацию о желаемой позе, обстановке, интерьере",
                parse_mode='markdown', reply_markup=cancel_neg_markdown)
            async with state.proxy() as data:
                data['pose_id'] = msg.message_id
            await Form.pose.set()
        elif call.data == "like":
            await call.message.edit_reply_markup(alphashare_contin_markup_2)
            doc_id = call.message.document.file_name
            id_u = doc_id.split("rd")[0]
            items = get_items(int(id_u))
            if int(id_u) == call.from_user.id:
                await call.answer(text="Упсс... Кажется это ваш пост", show_alert=True)
            else:
                save_data_in_database("balance", items[2] + 3, id_u)
                os.remove(f"ashare/{doc_id}")
                await bot.send_message(id_u,
                                       "❤️ *Кто-то оценил ваш арт.*\n\nВы получили 3 токенов! Генерация удалена из AlphaShare",
                                       parse_mode="markdown")
        elif call.data == "set_amount":
            back_markup_mr = InlineKeyboardMarkup(row_width=1)
            back_markup_mr.add(back_balance_button)
            cancel_neg_markdown = InlineKeyboardMarkup(row_width=1)
            cancel_neg_button = InlineKeyboardButton(text="<< Назад", callback_data="cancel_neg")
            cancel_neg_markdown.add(cancel_neg_button)
            await call.message.edit_text(
                text="💸 *Укажите количество токенов которое вы хотите преобрести, а мы сами расчитаем их стоимость.*\n\nМинимальная покупка - 10 токенов\nМаксимальная покупка - 5000 токенов\n\n",
                parse_mode="markdown", reply_markup=cancel_neg_markdown)
            await Form.amount_pay.set()
        elif call.data == "back_casino":
            items = get_items(call.from_user.id)
            if items[2] < 20:
                await call.message.edit_text(text="*Похоже у вас слишком мало токенов, чтобы начать игру*",
                                             parse_mode='markdown')
            else:
                await call.message.edit_text(text=
                                             "🎰 *Вы запустили казино*\n\nВы можете увеличить свои токены! Но будьте осторожны)\n\nМинимальная ставка - 10 токенов\n\n❌ *Проигрыш - 80 процентов\n\n✅ Умножение в 1,3х - 19 процентов\n\n💰 Умножение в 4х - 1 процент*\n\n*Введите сумму которую вы хотите поставить:*",
                                             parse_mode='markdown')
                await Form.casino.set()
        elif call.data == 'edit_res':
            save_data_in_database("pose_status", 0, call.from_user.id)
            dict_get = get_settings_get_txt2img(call.message.caption)
            items = get_items(call.from_user.id)
            rp2 = ReplyKeyboardMarkup(resize_keyboard=True)
            rp2_button = KeyboardButton(text="Стили", web_app=WebAppInfo(url='https://innoky.github.io/#'))
            button_1 = types.KeyboardButton(text="AlphaShare")
            rp2.add(button_1, rp2_button)
            await bot.send_message(call.from_user.id, f"*⚙️ Промт:* `{items[7]}`",
                                   disable_web_page_preview=True, reply_markup=rp2, parse_mode='markdown')

            await bot.send_message(call.from_user.id,
                                   replace_description_txt2img(model=dict_get['model'], resolution=dict_get['resol'],
                                                               prompt=dict_get['prompt'], negative=dict_get['negative'],
                                                               seed=dict_get['seed'], style=dict_get['style']),
                                   disable_web_page_preview=True, reply_markup=propmt_markup, parse_mode='markdown')
        elif call.data == 'cont_button':
            db = sqlite3.connect('userbase.db')
            c = db.cursor()
            c.execute(f"SELECT * FROM users")
            db.commit()
            items = c.fetchall()
            db.close()
            for i in range(len(items)):
                if str(items[i][0]) == str(call.from_user.id):
                    break
            msg = await call.message.edit_caption(caption="Ищем арты, подождите пять секунд...")
            rch = random.choice(os.listdir("ashare"))
            i = 0
            while rch.split('rd')[0] == str(call.from_user.id) or rch == items[i][18]:
                rch = random.choice(os.listdir("ashare"))
                i += 1
                if i > 10:
                    break
                    await call.answer(text="Похоже AlphaShare пуст, подождите пока кто-то выложит генерацию",
                                      show_alert=True)
            save_data_in_database("cur_alink", rch, call.from_user.id)
            gen_link = rch.split("rd")[1]
            ready_link = hlink("Сид к генерации", f"https://t.me/alphastabletbot?start={gen_link}")
            await bot.send_document(chat_id=call.from_user.id, document=open("ashare\\" + rch, "rb"),
                                    caption=f"<b>✨ Случайная генерация</b>\n\n🌱 <b>{ready_link}</b>\n\n<i>Вы можете лайкнуть генерацию или продолжить просмотр нажав кнопку далее</i>",
                                    reply_markup=alphashare_contin_markup, parse_mode="html")
            await msg.delete()
        elif call.data == 'ashare':
            document_id = call.message.document.file_name
            src = "outs" + f"\\{call.from_user.id}\\{document_id}"
            print(document_id)

            dst = f"ashare" + f"\\{document_id.replace('.png', '')}rd{random.randint(0, 9999999)}" + '.png'
            shutil.copyfile(src, dst)
            await call.answer(text="📤 Генерация отправлена в AlphaShare!", show_alert=True)
            await call.message.edit_reply_markup(reply_markup=write_history_to_art_markup_2)


@dp.message_handler(content_types=["photo"])
async def get_photo2img(message: types.Message):
    await message.photo[-1].download(destination_file=f'outs/{message.from_user.id}/{message.from_user.id}img2img.png')
    prompt = message.caption
    input_photo = InputFile(f"outs/{message.from_user.id}/{message.from_user.id}img2img.png")
    items = get_items(message.from_user.id)
    cur_model = items[5]
    cur_resol = f"{message.photo[-1].width}:{message.photo[-1].height}"
    if prompt is None:
        text = replace_description_img2img(model=cur_model, prompt="Prompt отсутствует, если хотите задать prompt,"
                                                                   " отправьте картинку с описанием",
                                           strength="ХЗ",)
        await bot.send_photo(photo=input_photo, caption=text,
                             chat_id=message.chat.id, parse_mode="markdown")


@dp.message_handler(state=Form.qr_hidden_text)
async def amount_get(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        delete_msg = a['qr_text_id']

    if len(message.text) > 300:
        await message.answer(text="Вы указали слишком большой текст", parse_mode='markdown')
    else:
        try:
            os.remove(f"outs/{message.from_user.id}/qr_hd_text_nr.jpg")
        except:
            print("Файл с qr отсутсвутет")
        import qrcode
        # пример данных
        data = message.text
        # имя конечного файла
        filename = f"outs/{message.from_user.id}/qr_hd_text_nr.jpg"
        # генерируем qr-код
        img = qrcode.make(data)
        # сохраняем img в файл
        img.save(filename)
        #################
        image_path = f"outs/{message.from_user.id}/qr_hd_text_nr.jpg"

        img = Image.open(image_path)
        # изменяем размер
        new_image = img.resize((1000, 1000))

        # сохранение картинки
        new_image.save(f"outs/{message.from_user.id}/qr_hd_text.jpg")

        await bot.delete_message(chat_id=message.from_user.id, message_id=delete_msg)
        items = get_items(message.from_user.id)

        cur_model = items[5]
        cur_resol = items[6]

        await bot.send_message(chat_id=message.chat.id, text=replace_description_txt2img(model=cur_model,
                                                                                         prompt=items[7],
                                                                                         resolution=cur_resol),
                               parse_mode='markdown',
                               reply_markup=propmt_markup, disable_web_page_preview=True)

        await message.answer(text="✅ *Вы успешно установили QR код!*\n\nМожете начать генерацию!",
                             parse_mode="markdown")
        save_data_in_database("pose_status", 3, message.from_user.id)
        await state.finish()


@dp.callback_query_handler(text_startswith='cancel_neg', state='*')
async def back_func(call: CallbackQuery, state: FSMContext):
    await state.finish()
    items = get_items(call.from_user.id)

    cur_model = items[5]
    cur_resol = items[6]

    text = link('подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
    # await bot.send_photo(message.chat.id, photo="https://i.ibb.co/KVv7rvH/914029246rd-659.png",
    #                      caption=f"""☺️*Мы готовы сгенерировать ваш запрос:*\n\n`{message.text}`\n\n- {text}\n\n*Советуем использовать GPT edit для лучшего результата*\n\nТекущая модель: **{cur_model}**\nРазрешение: **{cur_resol}**""",
    #                      reply_to_message_id=message.message_id,
    #                      parse_mode='markdown', reply_markup=propmt_markup)
    await call.message.edit_text(text=replace_description_txt2img(model=cur_model,
                                                                  prompt=items[7],
                                                                  resolution=cur_resol),
                                 parse_mode='markdown',
                                 reply_markup=propmt_markup, disable_web_page_preview=True)


@dp.message_handler(state=Form.add_prompt)
async def amount_get(message: types.Message, state: FSMContext):
    new_prompt = message.text
    items = get_items(message.from_user.id)
    async with state.proxy() as data:
        id = data["edit_id"]
    if len(items[7]) + len(message.text) > 500:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"*Вы ввели слишком большой промт*\n\n Доступное количество символов: *{500 - (len(items[7]))}*",
                               parse_mode="markdown")
    else:

        items = get_items(message.from_user.id)

        cur_model = items[5]
        cur_resol = items[6]

        save_data_in_database("raw_promt", items[7] + ", " + new_prompt, message.from_user.id)
        save_data_in_database("promt", items[7] + ", " + new_prompt, message.from_user.id)
        rp2 = ReplyKeyboardMarkup(resize_keyboard=True)
        rp2_button = KeyboardButton(text="Стили", web_app=WebAppInfo(url='https://innoky.github.io/#'))
        button_1 = types.KeyboardButton(text="AlphaShare")
        rp2.add(button_1, rp2_button)

        text = link('подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
        # await bot.send_photo(message.chat.id, photo="https://i.ibb.co/KVv7rvH/914029246rd-659.png",
        #                      caption=f"""☺️*Мы готовы сгенерировать ваш запрос:*\n\n`{message.text}`\n\n- {text}\n\n*Советуем использовать GPT edit для лучшего результата*\n\nТекущая модель: **{cur_model}**\nРазрешение: **{cur_resol}**""",
        #                      reply_to_message_id=message.message_id,
        #                      parse_mode='markdown', reply_markup=propmt_markup)

        txt = replace_description_txt2img(model=cur_model,
                                          prompt=items[7] + ", " + message.text,
                                          resolution=cur_resol)
        mss = await bot.edit_message_text(chat_id=message.chat.id, message_id=id, text=txt, parse_mode='markdown',
                                          reply_markup=propmt_markup, disable_web_page_preview=True)
        save_data_in_database("last_msg_id", mss.message_id, message.from_user.id)
        save_data_in_database("cur_settings", txt, message.from_user.id)

        await state.finish()


@dp.message_handler(state=Form.gift_amount)
async def amount_get(message: types.Message, state: FSMContext):
    items = get_items(message.from_user.id)
    if message.text.isdigit():
        if int(message.text) < 500 and int(message.text) >= 1:
            if int(message.text) <= items[2] and int(message.text) > 25:
                db = sqlite3.connect('gift.db')
                c = db.cursor()

                alphabet = string.ascii_letters + string.digits
                link = ''.join(secrets.choice(alphabet) for i in range(20))
                param = (link, message.text, 0, message.from_user.id, "empty")
                print(param)
                c.execute(f"INSERT INTO gift VALUES (?, ?, ?, ?, ?)", param)
                db.commit()
                db.close()

                gift_link = f"https://t.me/sigma_stable_bot?start={link}rd{message.text}"

                send_gift_markup = InlineKeyboardMarkup(row_width=1)
                send_gift_button = InlineKeyboardButton(text="🎁 Активировать подарок", url=gift_link)
                send_gift_markup.add(send_gift_button)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"🎁 *Нажмите на кнопку ниже, чтобы открыть подарок!*\n\nПодарок на сумму в *{message.text}* токен(ов)",
                                       parse_mode="markdown", reply_markup=send_gift_markup)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"<i>*Просто перешлите сообщение выше тому, кому хотите подарить токены</i>",
                                       parse_mode="html")

                await state.finish()
            else:
                await message.answer("Недостаточно токенов или указано меньше ")
        else:
            await message.answer("Вы указали слишком маленькую или слишком большую сумму")
    else:
        await message.answer("Похоже вы ввели текст. Введите нужное количество токенов для подарка.")


@dp.message_handler(state=Form.zoom_prompt)
async def zoom_set(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['zoom_prompt'] = message.text
    zprompt = a['zoom_prompt']
    if len(zprompt) > 300:
        await message.answer(text="Вы указали слишком большой текст", parse_mode='markdown')
    else:
        msg = await bot.send_message(chat_id=message.from_user.id, text="Обрабатываем промт...")
        items = get_items(message.from_user.id)

        # translator = Translator(service_urls=['translate.googleapis.com'])
#
        # chat_response = (translator.translate(message.text, dest='en'))
        result_promt = message.text
        db = sqlite3.connect('userbase.db')
        c = db.cursor()
        c.execute(f"SELECT * FROM users")
        db.commit()
        items_gen = c.fetchall()
        db.close()
        sum_time = 1
        for i in range(len(items_gen)):
            sum_time = sum_time + int(items_gen[i][3])
        sum_time = str((sum_time * 15) - 15 + 35)

        ms = await bot.edit_message_text(chat_id=message.from_user.id, message_id=msg.message_id,
                                         text=f'<b>Генерация началась.</b> \n\n<i>Время ожидания ~{sum_time} секунд(ы). Бот самостоятельно отправит вам результат. Также заходите в наш чат, там мы делимся генерациями и просто приятно общаемся</i>',
                                         parse_mode="html")
        save_data_in_database("edit_last", ms.message_id, message.from_user.id)
        print(result_promt)
        save_data_in_database('status', 1, message.from_user.id)
        if not (str(items[0]) in ("1430025958", "415356744")):
            save_data_in_database("balance", items[2] - 25, message.from_user.id)
        p1 = Process(target=zoom_start, args=(result_promt, message.from_user.id, items[10], items[24], items[23]))
        p1.start()
        await state.finish()


@dp.message_handler(state=Form.qr_text)
async def amount_get(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['qr_text'] = message.text
    qrt = a['qr_text']
    if len(qrt) > 300:
        await message.answer(text="Вы указали слишком большой текст", parse_mode='markdown')
    else:
        import segno

        crop_to_square(f"outs/{message.from_user.id}/qr_input.jpg", f"outs/{message.from_user.id}/qr_inputsq.png")
        piet = segno.make(qrt, error='h', )
        piet.to_artistic(background=f"outs/{message.from_user.id}/qr_inputsq.png",
                         target=f"outs/{message.from_user.id}/qr_outputsq.png", scale=16)

        overlay_images(f"outs/{message.from_user.id}/qr_outputsq.png", f"outs/{message.from_user.id}/qr_input.jpg",
                       f"outs/{message.from_user.id}/qr_output.png")
        await bot.send_document(chat_id=message.from_user.id,
                                document=open(f'outs/{message.from_user.id}/qr_output.png', 'rb'),
                                caption=f"🔲 *Ваш QR-код готов!*\n\nТеперь вы можете его отсканировать и вы получите введеный вами текст!",
                                parse_mode='markdown')
        await state.finish()


@dp.message_handler(state=Form.qr_image, content_types=['photo', 'text'])
async def get_img_qr(message: types.Message, state=FSMContext):
    if message.content_type == 'photo':
        user_id = message.from_user.id
        await message.photo[-1].download(destination_file=f'outs/{user_id}/qr_input.jpg')
        await message.delete()
        await message.answer(text="✅ *Вы успешно установили изображение!*\n\nВведите текст для записи его в QR-код:",
                             parse_mode="markdown")
        save_data_in_database('pose_status', 1, message.from_user.id)
        await state.finish()
        await Form.qr_text.set()

    else:
        await message.answer(text="*Вы отменили создание QR-кода*", parse_mode='markdown')
        await state.finish()


@dp.message_handler(state=Form.text, content_types=['photo', 'text'])
async def get_pose(message: types.Message, state=FSMContext):
    if message.content_type == 'photo':
        user_id = message.from_user.id
        await message.photo[-1].download(destination_file=f'outs/{user_id}/text.jpg')
        await message.delete()
        async with state.proxy() as data:
            delete_id = data['text_id']
        await bot.delete_message(chat_id=message.from_user.id, message_id=delete_id)
        items = get_items(message.from_user.id)

        cur_model = items[5]
        cur_resol = items[6]

        text = link('подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
        # await bot.send_photo(message.chat.id, photo="https://i.ibb.co/KVv7rvH/914029246rd-659.png",
        #                      caption=f"""☺️*Мы готовы сгенерировать ваш запрос:*\n\n`{message.text}`\n\n- {text}\n\n*Советуем использовать GPT edit для лучшего результата*\n\nТекущая модель: **{cur_model}**\nРазрешение: **{cur_resol}**""",
        #                      reply_to_message_id=message.message_id,
        #                      parse_mode='markdown', reply_markup=propmt_markup)
        await bot.send_message(chat_id=message.chat.id, text=replace_description_txt2img(model=cur_model,
                                                                                         prompt=items[7],
                                                                                         resolution=cur_resol),
                               parse_mode='markdown',
                               reply_markup=propmt_markup, disable_web_page_preview=True)

        await message.answer(text="✅ *Вы успешно установили текст для маскировки!*\n\nМожете начать генерацию!",
                             parse_mode="markdown")
        save_data_in_database('pose_status', 2, message.from_user.id)
        await state.finish()


    else:
        await message.answer(text="*Пожалуйста, отправьте фото с нужным референсом*", parse_mode='markdown')


@dp.message_handler(state=Form.pose, content_types=['photo', 'text'])
async def get_pose(message: types.Message, state=FSMContext):
    if message.content_type == 'photo':
        user_id = message.from_user.id
        await message.photo[-1].download(destination_file=f'outs/{user_id}/pose.jpg')
        await message.delete()
        async with state.proxy() as data:
            delete_id = data['pose_id']
        await bot.delete_message(chat_id=message.from_user.id, message_id=delete_id)
        items = get_items(message.from_user.id)

        cur_model = items[5]
        cur_resol = items[6]

        text = link('подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
        # await bot.send_photo(message.chat.id, photo="https://i.ibb.co/KVv7rvH/914029246rd-659.png",
        #                      caption=f"""☺️*Мы готовы сгенерировать ваш запрос:*\n\n`{message.text}`\n\n- {text}\n\n*Советуем использовать GPT edit для лучшего результата*\n\nТекущая модель: **{cur_model}**\nРазрешение: **{cur_resol}**""",
        #                      reply_to_message_id=message.message_id,
        #                      parse_mode='markdown', reply_markup=propmt_markup)
        await bot.send_message(chat_id=message.chat.id, text=replace_description_txt2img(model=cur_model,
                                                                                         prompt=items[7],
                                                                                         resolution=cur_resol),
                               parse_mode='markdown',
                               reply_markup=propmt_markup, disable_web_page_preview=True)

        await message.answer(text="✅ *Вы успешно установили референс!*\n\nМожете начать генерацию!",
                             parse_mode="markdown")
        save_data_in_database('pose_status', 1, message.from_user.id)
        await state.finish()


    else:
        await message.answer(text="*Пожалуйста, отправьте фото с нужным референсом*", parse_mode='markdown')


@dp.message_handler(state=Form.casino)
async def amount_get(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['casino'] = message.text
    amount = a['casino'].replace(" ", "")
    if amount.isdigit():
        items = get_items(message.from_user.id)
        if int(amount) > 15 and int(amount) < int(items[2]):
            await message.answer(
                text=f"*💰 Ваша ставка: {amount} токенов*\n\nИграем?\n\n*Если вы не хотите играть, просто введите любую другую команду или промт*",
                parse_mode='markdown', reply_markup=casino_markup)
            save_data_in_database("casino", int(amount), message.from_user.id)
            await state.finish()

        else:
            await message.answer(
                text=f"Кажется вы поставили слишком большую ставку, либо указали слишком маленькую ставку")
    else:
        await message.answer(text="Укажите сумму цифрами без пробелов и других знаков.")


@dp.message_handler(state=Form.amount_pay)
async def amount_get(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['amount_pay'] = message.text
    amount = a['amount_pay'].replace(" ", "")
    if amount.isdigit():
        if int(amount) > 9 and int(amount) < 5001:

            current_time = str(t.time()) + "spl" + str(round(int(amount) / 2))
            current_time_tobase = str(t.time()) + "spl" + str(round(int(amount)))
            save_data_in_database("pay_token", current_time_tobase, message.from_user.id)

            quickpay = Quickpay(
                receiver="4100118356657505",
                quickpay_form="shop",
                targets="Alpha tokens",
                paymentType="SB",
                sum=(round(int(amount) / 2)),
                label=str(message.from_user.id) + '::' + str(current_time_tobase)
            )
            pay_link = quickpay.redirected_url

            pay_link_markup = InlineKeyboardMarkup()
            pay_link_button = InlineKeyboardButton(text='Оплатить', url=pay_link)
            pay_link_markup.row(pay_link_button).row(back_balance_button)

            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"*Преобрести {str(amount)} токенов за {str(round(int(amount) / 2))} рублей*\n\nДля совершения оплаты, нажмите кнопку ниже",
                                   parse_mode='markdown', reply_markup=pay_link_markup)
            await state.finish()

        else:
            await message.answer(text="Похоже вы указали слишком большую или слишком маленькую сумму.")

    else:
        await message.answer(text="Укажите сумму цифрами без пробелов и других знаков.")


@dp.message_handler(state=Form.negative_wait)
async def negative_get(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['negative_wait'] = message.text
    async with state.proxy() as data:
        neg_id = data['msg_id_neg']

    items = get_items(message.from_user.id)
    negative = a['negative_wait']
    if negative.lower() == "нет":
        negative_m = ""
    else:
        translator = Translator(service_urls=['translate.googleapis.com'])

        chat_response = (translator.translate(negative, dest='en'))
        negative_m = chat_response.text

    s = get_settings_ready_txt2img(items[20])

    text_new = replace_description_txt2img(model=s["model"], prompt=s["prompt"], resolution=s["resol"],
                                           seed=s["seed"], style=s["style"], negative=negative_m)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=neg_id.message_id, text=text_new,
                                parse_mode='markdown', reply_markup=propmt_markup,
                                disable_web_page_preview=True)
    text_m = text_new
    save_data_in_database("cur_settings", text_m, message.from_user.id)
    await state.finish()


@dp.message_handler(state=Form.seed_state)
async def seed_get(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['seed_wait'] = message.text
    items = get_items(message.from_user.id)
    seed = a['seed_wait']
    async with state.proxy() as data:
        seed_id = data['seed_id']

    if not seed.isdigit() and seed != "-1":
        await bot.send_message(message.chat.id,
                               text="Данный ввод не является числом, отправьте сообщение с целым числом")
    else:
        s = get_settings_ready_txt2img(items[20])
        text_new = replace_description_txt2img(model=s["model"], prompt=s["prompt"], resolution=s["resol"],
                                               seed=int(seed), style=s["style"], negative=s["negative"])

        await bot.edit_message_text(chat_id=message.chat.id, message_id=seed_id, text=text_new, parse_mode='markdown',
                                    reply_markup=propmt_markup,
                                    disable_web_page_preview=True)
        text_m = text_new
        save_data_in_database("cur_settings", text_m, message.from_user.id)
        await state.finish()


@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_recieve(message: Message, state: FSMContext):
    style = json.loads(open("model_json/style.json", encoding="utf-8").read())
    print(message.web_app_data.data)

    data_key = "1"
    if (message.web_app_data.data).isdigit():
        if message.web_app_data.data == "1":
            data_key = "1990s"
        elif message.web_app_data.data == "2":
            data_key = "magazine"
        elif message.web_app_data.data == "3":
            data_key = "pop figure"
        elif message.web_app_data.data == "4":
            data_key = "invisible"
        elif message.web_app_data.data == "5":
            data_key = "ragenew"
        elif message.web_app_data.data == "6":
            data_key = "body horror"
        elif message.web_app_data.data == "7":
            data_key = "pixel"
        elif message.web_app_data.data == "8":
            data_key = "3drm"
        elif message.web_app_data.data == "9":
            data_key = "manga"
        elif message.web_app_data.data == "10":
            data_key = "niji"
        elif message.web_app_data.data == "11":
            data_key = "concept"
        elif message.web_app_data.data == "12":
            data_key = "pastel"
        elif message.web_app_data.data == "13":
            data_key = "poster"
        elif message.web_app_data.data == "14":
            data_key = "shapes"

        items = get_items(message.from_user.id)
        settings_dict = get_settings_ready_txt2img(items[20])
        resol_m = settings_dict["resol"]
        model_m = settings_dict["model"]
        style_m = settings_dict["style"]
        prompt_m = settings_dict["prompt"]
        try:
            negative_m = settings_dict["negative"]
        except:
            print("пустой негатив")
        try:
            seed_m = settings_dict['seed']
        except:
            print("Пустой сид")

        if data_key in style.keys():
            items = get_items(message.from_user.id)
            save_data_in_database("promt", items[7] + f", {data_key} ", message.from_user.id)
            items = get_items(message.from_user.id)

            await bot.edit_message_text(chat_id=message.from_user.id, message_id=items[25],
                                        text=replace_description_txt2img(items[5], items[6], items[7], negative_m,
                                                                         seed_m, style_m),
                                        disable_web_page_preview=True, reply_markup=propmt_markup,
                                        parse_mode='markdown')
    else:
        save_data_in_database('pose_status', 0, message.from_user.id)
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        items = get_items(message.from_user.id)

        cur_model = items[5]
        cur_resol = items[6]

        save_data_in_database("raw_promt", message.web_app_data.data, message.from_user.id)
        save_data_in_database("promt", message.web_app_data.data, message.from_user.id)
        rp2 = ReplyKeyboardMarkup(resize_keyboard=True)
        rp2_button = KeyboardButton(text="Стили", web_app=WebAppInfo(url='https://innoky.github.io/#'))
        button_1 = types.KeyboardButton(text="AlphaShare")
        rp2.add(button_1, rp2_button)

        text = link('подсказки', 'https://telegra.ph/AlphaStable-Tutorial-06-10')
        # await bot.send_photo(message.chat.id, photo="https://i.ibb.co/KVv7rvH/914029246rd-659.png",
        #                      caption=f"""☺️*Мы готовы сгенерировать ваш запрос:*\n\n`{message.text}`\n\n- {text}\n\n*Советуем использовать GPT edit для лучшего результата*\n\nТекущая модель: **{cur_model}**\nРазрешение: **{cur_resol}**""",
        #                      reply_to_message_id=message.message_id,
        #                      parse_mode='markdown', reply_markup=propmt_markup)
        ms = await bot.send_message(chat_id=message.from_user.id, text=f"✏️ *Вы ввели:* `{message.web_app_data.data}`",
                                    reply_markup=rp2, parse_mode='markdown')
        txt = replace_description_txt2img(model=cur_model,
                                          prompt=message.web_app_data.data,
                                          resolution=cur_resol)
        mss = await bot.send_message(message.chat.id, text=txt,
                                     reply_to_message_id=message.message_id, parse_mode='markdown',
                                     reply_markup=propmt_markup, disable_web_page_preview=True)
        save_data_in_database("last_msg_id", mss.message_id, message.from_user.id)
        save_data_in_database("cur_settings", txt, message.from_user.id)


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    print(query.query)
    if len(query.query.split(" ")) == 2:
        db = sqlite3.connect('userbase.db')
        c = db.cursor()
        c.execute("SELECT username FROM users")
        items = c.fetchall()
        existence = bool
        getter = "empty"
        for i in range(len(items)):
            if str(items[i]).replace("('", "").replace("',)", "") == query.query.split(" ")[1]:
                getter = items[i]
                break

        if getter != "empty":
            items = get_items(query.from_user.id)

            if int(query.query.split(" ")[0]) < items[2] and int(query.query.split(" ")[0]) <= 500 and int(
                    query.query.split(" ")[0]) >= 25:
                db = sqlite3.connect('gift.db')
                c = db.cursor()

                alphabet = string.ascii_letters + string.digits
                link = ''.join(secrets.choice(alphabet) for i in range(20))
                param = (link, query.query.split(' ')[0], 0, query.from_user.id,
                         str(getter).replace("('", "").replace("',)", ""))
                print(param)
                c.execute(f"INSERT INTO gift VALUES (?, ?, ?, ?, ?)", param)
                db.commit()
                db.close()

                gift_link = f"https://t.me/alphastabletbot?start={link}rd{query.query.split(' ')[0]}"

                send_gift_markup = InlineKeyboardMarkup(row_width=1)
                send_gift_button = InlineKeyboardButton(text="🎁 Активировать подарок", url=gift_link)
                send_gift_markup.add(send_gift_button)
                getter2 = str(getter).replace("('", "").replace("',)", "")
                articles = [types.InlineQueryResultArticle(
                    id=random.randint(1, 1000),
                    title=f"🎁 Подарок на сумму в {query.query.split(' ')[0]} токен(ов) для @{getter2}",
                    reply_markup=send_gift_markup,
                    thumb_url="https://creazilla-store.fra1.digitaloceanspaces.com/emojis/46882/wrapped-gift-emoji-clipart-md.png",
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"🎁 Подарок на сумму в {query.query.split(' ')[0]} токен(ов) для @{getter2}"))]

                await query.answer(articles, cache_time=1, is_personal=True)

        # if query.query.split(" ")[2]
    elif query.query.isdigit():
        items = get_items(query.from_user.id)

        if int(query.query) < items[2] and int(query.query) <= 500 and int(query.query) >= 25:
            db = sqlite3.connect('gift.db')
            c = db.cursor()

            alphabet = string.ascii_letters + string.digits
            link = ''.join(secrets.choice(alphabet) for i in range(20))
            param = (link, query.query, 0, query.from_user.id, "empty")
            print(param)
            c.execute(f"INSERT INTO gift VALUES (?, ?, ?, ?, ?)", param)
            db.commit()
            db.close()

            gift_link = f"https://t.me/alphastabletbot?start={link}rd{query.query}"

            send_gift_markup = InlineKeyboardMarkup(row_width=1)
            send_gift_button = InlineKeyboardButton(text="🎁 Активировать подарок", url=gift_link)
            send_gift_markup.add(send_gift_button)

            articles = [types.InlineQueryResultArticle(
                id=random.randint(1, 1000),
                title=f"🎁 Подарок на сумму в {query.query} токен(ов)",
                reply_markup=send_gift_markup,
                thumb_url="https://creazilla-store.fra1.digitaloceanspaces.com/emojis/46882/wrapped-gift-emoji-clipart-md.png",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"🎁 Подарок на сумму в {query.query} токен(ов)"))]

            await query.answer(articles, cache_time=1, is_personal=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
