from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hlink, link
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State
import json
import sqlite3
from sqlite_func_2 import *

api = "6448499765:AAH1TWiHnhNdwWknqswnD7KWGIcIMaRMsBw"

bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
admins_list = ("869834155", "914029246")


class Form(StatesGroup):
    update_gift_status = State()
    change_tokens = State()
    find_username_token = State()
    find_id_token = State()
    find_username_status = State()
    find_id_status = State()
    find_username = State()
    find_id = State()
    change_status = State()


# button start

user_button = InlineKeyboardMarkup()
id_button_user = InlineKeyboardButton(text="ID", callback_data="id_user_stats")
username_button_user = InlineKeyboardButton(text="USERNAME", callback_data="username_user_stats")
user_button.row(id_button_user, username_button_user)

tokens_button = InlineKeyboardMarkup()
id_tokens_button_user = InlineKeyboardButton(text="ID", callback_data="id_user_tokens")
username_tokens_button_user = InlineKeyboardButton(text="USERNAME", callback_data="username_user_tokens")
tokens_button.row(id_tokens_button_user, username_tokens_button_user)

status_button = InlineKeyboardMarkup()
id_status_button_user = InlineKeyboardButton(text="ID", callback_data="id_user_status")
username_status_button_user = InlineKeyboardButton(text="USERNAME", callback_data="username_user_status")
status_button.row(id_status_button_user, username_status_button_user)

tokens_change_markup = InlineKeyboardMarkup(row_width=1)
tokens_change_button = InlineKeyboardButton(text="Изменить💷", callback_data="change_tokens")
tokens_change_markup.add(tokens_change_button)

status_change_markup = InlineKeyboardMarkup(row_width=1)
status_change_button = InlineKeyboardButton(text="Изменить обычный статус", callback_data="change_simple_status")
status_hq_change_button = InlineKeyboardButton(text="Изменить hquality статус", callback_data="change_hq_status")
status_zoom_change_button = InlineKeyboardButton(text="Изменить zoom статус", callback_data="change_zoom_status")
status_change_markup.add(status_change_button, status_hq_change_button, status_zoom_change_button)

# button end


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.text == "/start":
        link_chanel = hlink("AlphaStable", "https://t.me/stablealpha")
        link_bot = hlink("AlphaStable", "https://t.me/alphastabletbot")
        await bot.send_message(message.from_user.id,
                               text=f"🖐️Приветствую.\n"
                                    f"Я бот для работы с базой данных телеграм бота <b>{link_bot}</b>.\n"
                                    f"Бот доступен лишь админам канала <i>{link_chanel}</i>.\n"
                                    f"Для информации об моих умениях, пропишите <i>/info</i>.", parse_mode="html",
                               disable_web_page_preview=True)


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    link_group = hlink("телеграм чат", "https://t.me/+F5tR-Odqr_djZWEy")
    if str(message.from_user.id) not in admins_list:
        await bot.send_message(message.from_user.id, text="🛑 Вы не являетесь админом канала.")
    else:
        await message.delete()
        await bot.send_message(message.from_user.id, text="Мои умения📝\n"
                                                          "1. Информация об пользователе/пользователях 👤:\n"
                                                          "└Баланс токенов\n"
                                                          "└Текущие настройки генерации\n"
                                                          "└Общее кол-во генераций и кол-во за этот день(обнуление в 00:00) \n"
                                                          "└Генерирует ли сейчас пользователь\n"
                                                          "└Последняя дата покупки и размер\n"
                                                          "└Гифт статус\n"
                                                          "└Какие модели использовал за всё время пользователь\n"
                                                          "└Дата и время начала счёта статистики\n"
                                                          "2. Управление балансом отдельного пользователя 💷\n"
                                                          "3. Обновление гифт статуса всех пользователей 🎁\n"
                                                          "4. Обнуление статуса генерации определённого пользователя ⚙️\n"
                                                          "5. Общая статистика генераций:\n"
                                                          "└Общее кол-во генераций за всё время\n"
                                                          "└Кол-во генераций за день\n"
                                                          "└Топ использования моделей исходя из общего количества генераций за всё время\n"
                                                          f"🔔Также доступен <b>{link_group}</b>, <i>созданный только для админов</i>, куда бот будет присылать уведомления, хотите узнать, какие уведомления, пропишите <i>/notif</i>.\n"
                                                          "Для большего понимания, команды есть в выпадающем меню, а также появится сообщением, если прописать <i>/help</i>.",
                               disable_web_page_preview=True, parse_mode="html")


@dp.message_handler(commands=['notif'])
async def notif(message: types.Message):
    link_bot = hlink("ботом", "https://t.me/alphastabletbot")
    link_group = hlink("специальном чате", "https://t.me/+F5tR-Odqr_djZWEy")
    if str(message.from_user.id) not in admins_list:
        await bot.send_message(message.chat.id, text="🛑 Вы не являетесь админом канала")
    else:
        await bot.send_message(message.chat.id, text=f"🔔Уведомления присылаемые {link_bot} в <b>{link_group}</b>\n"
                                                     "└Уведомление об новом участнике\n"
                                                     "└Уведомление об реферальном участнике(и кто привёл)\n"
                                                     "└Уведомление об покупке токенов\n"
                                                     "└Уведомление об создании ссылки подарка, и об получении(и кто получил)\n", parse_mode="html", disable_web_page_preview=True)


@dp.message_handler(commands=['help'])
async def help_(message: types.Message):
    if str(message.from_user.id) not in admins_list:
        await bot.send_message(message.chat.id, text="🛑 Вы не являетесь админом канала")
    else:
        await bot.send_message(message.chat.id, text="Команды:\n"
                                                     "<i>/user</i> выводит статистику об пользователе\n"
                                                     "<i>/tokens</i> выводит баланс пользователя, и позволяет его изменить, также можно отредактировать баланс и в статистике об пользователе\n"
                                                     "<i>/gift</i> обнуляет гифт статус всех пользователей\n"
                                                     "<i>/status</i> обнуляет статус генераии одного пользователя и возвращает ему\n"
                                                     "<i>/all</i> выводит общую статистику(если нужно что-то добавить, ты знаешь куда писать)\n"
                                                     "<i>/day</i> выводит статистику генераций за день\n"
                                                     "<i>/model</i> выводит топ моделей", parse_mode="html")


@dp.message_handler()
async def commands_func(message: types.Message):
    if message.text == "/user":
        await bot.send_message(message.chat.id, text="Сделайте выбор:\n Найти пользователя по\n<i>ID</i> или"
                                                     " <i>USERNAME</i>", parse_mode="html", reply_markup=user_button)
    elif message.text == "/tokens":
        await bot.send_message(message.chat.id, text="Сделайте выбор:\n Найти пользователя по\n<i>ID</i> или"
                                                     " <i>USERNAME</i>", parse_mode="html", reply_markup=tokens_button)
    elif message.text == "/status":
        await bot.send_message(message.chat.id, text="Сделайте выбор:\n Найти пользователя по\n<i>ID</i> или"
                                                     " <i>USERNAME</i>", parse_mode="html", reply_markup=status_button)

    elif message.text == "/gift":
        await bot.send_message(message.chat.id, text="Хотите обнулить гифт статус?\nДля подтверждения отправьте <b>Да</b>."
                                                     "\nЛюбой другой ввод будет являться отказом.", parse_mode="html")
        await Form.update_gift_status.set()

    elif message.text == "/all":
        db_user = sqlite3.connect("userbase.db")
        # db_stats = sqlite3.connect("stats_user.db")
        cur_user = db_user.cursor()
        # cur_stats = db_stats.cursor()
        # cur_stats.execute("SELECT SUM(gen_all) FROM user_stats")
        # gen_all = cur_stats.fetchone()[0]
        # cur_stats.execute("SELECT SUM(gen_day) FROM user_stats")
        # gen_day = cur_stats.fetchone()[0]
        cur_user.execute("SELECT SUM(status) FROM users")
        gen_cur = cur_user.fetchone()[0]
        cur_user.execute("SELECT COUNT(*) FROM users")
        count_users = cur_user.fetchone()[0]
        cur_user.execute("SELECT SUM(gift_status) FROM users")
        gift_status_count = cur_user.fetchone()[0]
        db_user.close()
        # db_stats.close()
        await bot.send_message(message.chat.id, text=f"<b>Общая статистика 📊</b>\n"
                                                     f"Количество генераций: <code>{'в разработке'}</code>\n"
                                                     f"Количество генераций за день: <code>{'в разработке'}</code>\n"
                                                     f"Людей генерирующих в данный момент: <code>{gen_cur}/"
                                                     f"{count_users}</code>\n"
                                                     f"Людей активировавших промокод:"
                                                     f" <code>{int(gift_status_count)}/{count_users}</code>", parse_mode="html")
    elif message.text == "/day":
        await bot.send_message(message.chat.id, text="В разработке.")
    elif message.text == "/model":
        await bot.send_message(message.chat.id, text="В разработке.")
    elif message.text == "/gen_day":
        # db_user = sqlite3.connect("stats_user.db")
        # cur_user = db_user.cursor()
        # cur_user.execute("UPDATE user_stats SET gen_day=0")
        # db_user.commit()
        # db_user.close()
        await bot.send_message(message.chat.id, text="В разработке.")


@dp.callback_query_handler()
async def callback_command(call: types.CallbackQuery, state: FSMContext):
    if call.data == "username_user_tokens":
        await call.message.delete()
        await bot.send_message(call.message.chat.id, text="Отправьте <i>username</i> пользователя, баланс которого"
                                                          " хотите посмотреть.", parse_mode="html")
        await Form.find_username_token.set()
    elif call.data == "id_user_tokens":
        await call.message.delete()
        await bot.send_message(call.message.chat.id, text="Отправьте <i>id</i> пользователя, баланс которого"
                                                          " хотите посмотреть.", parse_mode="html")
        await Form.find_id_token.set()
    elif call.data == "username_user_status":
        await call.message.delete()
        await bot.send_message(call.message.chat.id, text="Отправьте <i>username</i> пользователя, статус генерации которого"
                                                          " хотите посмотреть.", parse_mode="html")
        await Form.find_username_status.set()
    elif call.data == "id_user_status":
        await call.message.delete()
        await bot.send_message(call.message.chat.id, text="Отправьте <i>id</i> пользователя, статус генерации которого"
                                                          " хотите посмотреть.", parse_mode="html")
        await Form.find_id_status.set()
    elif call.data == "change_tokens":
        text = call.message.text.split()
        cur_tokens = text[text.index("Токены:") + 1]
        cur_id = text[text.index("ID:") + 1]
        cur_username = text[text.index("USERNAME:") + 1]
        await call.message.delete()
        await bot.send_message(call.message.chat.id, text=f"Введите новое значение токенов\n"
                                                          f"Прошлое значение: {cur_tokens}")
        async with state.proxy() as a:
            a['cur_tokens'] = cur_tokens
            a['cur_id'] = cur_id
            a['cur_username'] = cur_username
        await Form.change_tokens.set()

    elif call.data in ("change_zoom_status", "change_simple_status", "change_hq_status"):
        data = {
            "change_simple_status": "simple",
            "change_zoom_status": "zoom",
            "change_hq_status": "hq"
        }
        cur_id = call.message.text.split()[call.message.text.split().index("ID:") + 1]
        async with state.proxy() as a:
            a['where_update'] = data[call.data]
            a["id_status_f"] = cur_id
        await call.message.delete()
        await bot.send_message(call.message.chat.id, text="Хотите обнулить cтатус"
                                                          " генерации?\nДля подтверждения отправьте <b>Да</b>."
                                                          "\nЛюбой другой ввод будет являться отказом.",
                               parse_mode="html")
        await Form.change_status.set()
    elif call.data in ("username_user_stats", "id_user_stats"):
        if call.data == "username_user_stats":
            pass
        else:
            pass


@dp.message_handler(state=Form.find_username_token)
async def username_tokens(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['username_tokens'] = message.text
    answer = a["username_tokens"]
    bool_ = get_items_2("userbase", answer)
    if bool_[0]:
        items = bool_[1]
        tokens = items[2]
        id_user = items[0]
        await bot.send_message(message.chat.id, text="<b>Пользователь найден!</b>\n"
                                                     f"<b>ID:</b> <code>{id_user}</code>\n"
                                                     f"<b>USERNAME:</b> @{answer}\n"
                                                     f"Токены: <code>{tokens}</code>\n"
                                                     f"Чтобы изменить количество, нажмите кнопку внизу.",
                               parse_mode="html", reply_markup=tokens_change_markup)
    else:
        await bot.send_message(message.chat.id, text=f"<b>Пользователь @{answer} не найден.</b>", parse_mode="html")
    await state.finish()


@dp.message_handler(state=Form.find_id_token)
async def id_tokens(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['id_tokens'] = message.text
    answer = a["id_tokens"]
    if answer.isdigit():
        bool_ = get_items_2("userbase", answer, id_user=True)
        if bool_[0]:
            items = bool_[1]
            tokens = items[2]
            username_user = items[1]
            await bot.send_message(message.chat.id, text="<b>Пользователь найден!</b>\n"
                                                         f"<b>ID:</b> <code>{answer}</code>\n"
                                                         f"<b>USERNAME:</b> @{username_user}\n"
                                                         f"Токены: <code>{tokens}</code>\n"
                                                         f"Чтобы изменить количество, нажмите кнопку внизу.",
                                   parse_mode="html", reply_markup=tokens_change_markup)
        else:
            await bot.send_message(message.chat.id, text=f"<b>Пользователь <code>{answer}</code> не найден.</b>",
                                   parse_mode="html")
    else:
        await bot.send_message(message.chat.id, text="<b>Вы ввели не id.</b>", parse_mode="html")
    await state.finish()


@dp.message_handler(state=Form.find_username_status)
async def username_status(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['username_status'] = message.text
    answer = a["username_status"]
    bool_ = get_items_2("userbase", answer)
    if bool_[0]:
        items = bool_[1]
        status_code = items[3]
        status = "Не генерирует"
        if int(status_code):
            status = "Генерирует"
        id_user = items[0]
        await bot.send_message(message.chat.id, text="<b>Пользователь найден!</b>\n"
                                                     f"<b>ID:</b> <code>{id_user}</code>\n"
                                                     f"<b>USERNAME:</b> @{answer}\n"
                                                     f"Статус генерации: <code>{status}</code>\n"
                                                     f"Чтобы изменить статус генерации, нажмите кнопку внизу.",
                               parse_mode="html", reply_markup=status_change_markup)
    else:
        await bot.send_message(message.chat.id, text=f"<b>Пользователь @{answer} не найден.</b>", parse_mode="html")
    await state.finish()


@dp.message_handler(state=Form.find_id_status)
async def id_status(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['id_status'] = message.text
    answer = a["id_status"]
    if answer.isdigit():
        bool_ = get_items_2("userbase", answer, id_user=True)
        if bool_[0]:
            items = bool_[1]
            status_code = items[3]
            status = "Не генерирует"
            if int(status_code):
                status = "Генерирует"
            username_user = items[1]
            await bot.send_message(message.chat.id, text="<b>Пользователь найден!</b>\n"
                                                         f"<b>ID:</b> <code>{answer}</code>\n"
                                                         f"<b>USERNAME:</b> @{username_user}\n"
                                                         f"Статус генерации: <code>{status}</code>\n"
                                                         f"Чтобы изменить статус генерации, нажмите кнопку внизу.",
                                   parse_mode="html", reply_markup=status_change_markup)
        else:
            await bot.send_message(message.chat.id, text=f"<b>Пользователь <code>{answer}</code> не найден.</b>",
                                   parse_mode="html")
    else:
        await bot.send_message(message.chat.id, text="<b>Вы ввели не id.</b>", parse_mode="html")
    await state.finish()


@dp.message_handler(state=Form.update_gift_status)
async def gift_status_update(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['update_gift'] = message.text
    answer = a["update_gift"]
    if answer == "Да":
        db_user = sqlite3.connect("userbase.db")
        cur_user = db_user.cursor()
        cur_user.execute("UPDATE users SET gift_status=0")
        db_user.commit()
        db_user.close()
        await bot.send_message(message.chat.id, text="<b>Гифт статус успешно обновлён!</b>", parse_mode="html")
    else:
        await bot.send_message(message.chat.id, text="<b>Отмена операции</b>", parse_mode="html")
    await state.finish()


@dp.message_handler(state=Form.change_tokens)
async def tokens_change(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['new_tokens'] = message.text
    last_tokens = a["cur_tokens"]
    cur_id = a["cur_id"]
    cur_username = a["cur_username"]
    new_tokens = a['new_tokens']
    if new_tokens.isdigit():
        save_data_in_database_2("userbase", "balance", new_tokens, cur_id, True)
        await bot.send_message(message.chat.id, text=f"<b>Баланс пользователя обновлён!</b>\n"
                                                     f"<b>ID:</b> <code>{cur_id}</code>\n"
                                                     f"<b>USERNAME:</b> {cur_username}\n"
                                                     f"Токены: <code>{last_tokens}</code> -> <code>{new_tokens}</code>\n",
                               parse_mode="html")
    else:
        await bot.send_message(message.chat.id, text="<b>Ввод не является числом.\nОперация отменена.</b>",
                               parse_mode="html")
    await state.finish()


@dp.message_handler(state=Form.change_status)
async def status_change(message: types.Message, state: FSMContext):
    async with state.proxy() as a:
        a['update_status'] = message.text
    where_update = a["where_update"]
    answer = a["update_status"]
    cur_id = a["id_status_f"]
    if answer == "Да":
        if where_update == "simple":
            items = get_items_2("userbase", cur_id, True)[1]
            tokens = int(items[2]) + 10
            if str(items[3]) == "1":
                status = 0
                username = items[1]
                save_data_in_database_2("userbase", "balance", tokens, cur_id, True)
                save_data_in_database_2("userbase", "status", status, cur_id, True)
                await bot.send_message(message.chat.id, text=f"<b>Статус обновлён!</b>\n"
                                                             f"<b>ID:</b> <code>{cur_id}</code>\n"
                                                             f"<b>USERNAME:</b> @{username}\n"
                                                             f"Новый статус генерации: Не генерирует\n"
                                                             f"Новый баланс: <code>{items[2]}</code>-><code>{tokens}</code>"
                                       , parse_mode="html")
            else:
                await bot.send_message(message.chat.id, "Пользователь не генерирует, обнуление не нужно.")
        elif where_update == "zoom":
            items = get_items_2("userbase", cur_id, True)[1]
            tokens = int(items[2]) + 20
            if str(items[3]) == "1" and str(items[23]) == "1":
                status = 0
                username = items[1]
                save_data_in_database_2("userbase", "balance", tokens, cur_id, True)
                save_data_in_database_2("userbase", "status", status, cur_id, True)
                save_data_in_database_2("userbase", "zoom_status", status, cur_id, True)
                await bot.send_message(message.chat.id, text=f"<b>Статус обновлён!</b>\n"
                                                             f"<b>ID:</b> <code>{cur_id}</code>\n"
                                                             f"<b>USERNAME:</b> @{username}\n"
                                                             f"Новый статус генерации: Не генерирует\n"
                                                             f"Новый баланс: <code>{items[2]}</code>-><code>{tokens}</code>"
                                       , parse_mode="html")
            else:
                await bot.send_message(message.chat.id, "Пользователь не использует зум, обнуление не нужно.")
        elif where_update == "hq":
            items = get_items_2("userbase", cur_id, True)[1]
            tokens = int(items[2]) + 15
            if str(items[3]) == "1":
                status = 0
                username = items[1]
                save_data_in_database_2("userbase", "balance", tokens, cur_id, True)
                save_data_in_database_2("userbase", "status", status, cur_id, True)
                await bot.send_message(message.chat.id, text=f"<b>Статус обновлён!</b>\n"
                                                             f"<b>ID:</b> <code>{cur_id}</code>\n"
                                                             f"<b>USERNAME:</b> @{username}\n"
                                                             f"Новый статус генерации: Не генерирует\n"
                                                             f"Новый баланс: <code>{items[2]}</code>-><code>{tokens}</code>"
                                       , parse_mode="html")
            else:
                await bot.send_message(message.chat.id, "Пользователь не генерирует, обнуление не нужно.")
    else:
        await bot.send_message(message.chat.id, text="<b>Отмена операции</b>", parse_mode="html")
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
