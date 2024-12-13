from aiogram import Router, F
from aiogram.filters import ExceptionMessageFilter, Command, CommandObject, state
from aiogram.fsm.context import FSMContext
from aiogram.handlers import ErrorHandler
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, BufferedInputFile
import datetime
from random import randint

from keyboards.user_keyboard import *
import database.db as db
from units.drawer import draw_field
from units.string_matrix import to_string, to_matrix
from units.number_player import get_number_player
from units.check_field import check_field
from fields import fields
from config_data.config import config


router = Router()
@router.message(Command("start"))
async def start(message: Message, command: CommandObject, state: FSMContext):
    if not await get_user_exists(message.from_user.id):
        await add_user(message.from_user.id, message.from_user.first_name)
    if command.args:
        game = command.args
    else:
        game = None
    if game:
        info = game.split("_")
        if info[0].isdigit() and info[1].isdigit():
            room_id = int(info[0])
            user_id_1 = int(info[1])
            room = await get_room(room_id)
            if room[1] == user_id_1 and room[1] != message.chat.id:
                if room[2] == 1 or room[2] == 0:
                    if not await get_user_in_room(message.chat.id):
                        str_field = fields[randint(0, len(fields) - 1)]
                        field = to_matrix(str_field)
                        await state.update_data(field=field, room_id=room_id)
                        img_field = await draw_field(field)
                        img = BufferedInputFile(img_field, filename="img.png")
                        await message.answer_photo(photo=img, caption="Пожалуйста, выберите расстановку",
                                                   reply_markup=await set_field_keyboard("connect"))
                    else:
                        await message.answer("Вы уже находитесь в комнате")
                else:
                    await message.answer("Комната уже заполнена")
            else:
                await message.answer("Вы не можете подключиться к этой комнате")
        else:
            await message.answer("Комната не найдена")
    else:
        await message.answer("Добро пожаловать в бота для игры в морской бой!", reply_markup=await main_keyboard())


@router.message(F.text == "⛵️ Играть")
async def play(message: Message):
    await message.delete()
    await message.answer("Выберите режим игры", reply_markup=await game_mode_keyboard())


@router.message(F.text == "👤 Профиль")
async def profile(message: Message):
    await message.delete()
    user_info = await get_user(message.from_user.id)
    await message.answer(f"""👤 <b>Профиль</b>

🆔 ID: <code>{user_info[0]}</code>
📅 Дата регистрации: <b>{user_info[2]}</b>
🏆 Рейтинг: <b>{user_info[3]} очков</b>""", parse_mode="HTML")


@router.message(Command("profile"))
async def profile(message: Message, command: CommandObject, state: FSMContext):
    user_info = await get_user(message.from_user.id)
    await message.answer(f"""👤 <b>Профиль</b>

🆔 ID: <code>{user_info[0]}</code>
📅 Дата регистрации: <b>{user_info[2]}</b>
🏆 Рейтинг: <b>{user_info[3]} очков</b>""", parse_mode="HTML")


@router.message(Command("help"))
async def help(message: Message, command: CommandObject, state: FSMContext):
    help_text = """
    <b>⁉️Правила игры в Морской бой⁉️</b>

    Морской бой — это игра для двух игроков, цель которой — потопить все корабли противника.👥

1. ⛴️Подготовка🧭:

• Игровое поле🗺️: Каждый игрок использует игровое поле размером 6x6 клеток. 
• Корабли🚢: Каждый игрок получает набор кораблей определенной длины:
  * 1 четырёхъюдочный корабль
  * 2 трёхъюдочный корабль
  * 3 двухъюдочный корабль
  * 4 одноюдочный корабль
• Размещение кораблей🧭: Корабли размещаются на поле до начала игры. Корабли могут располагаться только горизонтально или вертикально, нельзя располагать корабли по диагонали. Между кораблями должны быть хотя бы одна пустая клетка.

2. 🌊Игровой процесс🔥:

Игра проходит по очереди. Игроки по очереди выбирают клетки на поле противника.

• Попадание❌: Если игрок выбирает клетку, где находится часть корабля противника, то объявляется "попадание". Игрок делает еще один ход.
• Промах✖️: Если игрок выбирает пустую клетку или клетки, которая уже была атакована, то объявляется "промах". Ход переходит к противнику.
• Потопление корабля🔥: Когда все клетки корабля противника атакованы, корабль считается потопленным. 
• Конец игры❗: Игра заканчивается, когда все корабли одного из игроков потоплены. Побеждает игрок, потопивший все корабли противника.
    """
    await message.answer(help_text, parse_mode="HTML")


@router.message(F.text == "🏆 Топ")
async def top(message: Message):
    await message.delete()
    top_10 = await get_top_10()
    text = "🏆 <b>Топ 10 игроков</b>\n\n"
    for user in top_10:
        text += f"<b>{user[1]}</b> - <b>{user[3]}</b> очков\n"
    await message.answer(text, parse_mode="HTML")


@router.message(Command("top"))
async def top(message: Message, command: CommandObject, state: FSMContext):
    top_10 = await get_top_10()
    text = "🏆 <b>Топ 10 игроков</b>\n\n"
    for user in top_10:
        text += f"<b>{user[1]}</b> - <b>{user[3]}</b> очков\n"
    await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data.startswith("play_with_bot"))
async def play_with_bot(call: CallbackQuery, state: FSMContext):
    await call.answer()
    str_field = fields[randint(0, len(fields) - 1)]
    field = to_matrix(str_field)
    await state.update_data(field=field, bot_field=create_bot_field())
    img_field = await draw_field(field)
    img = BufferedInputFile(img_field, filename="img.png")
    await call.message.answer_photo(photo=img, caption="Ваша расстановка:",
                                    reply_markup=await set_field_keyboard("bot"))

def create_bot_field():
    return to_matrix(fields[randint(0,len(fields)-1)])

@router.callback_query(F.data.startswith("play_with_player"))
async def play_with_player(call: CallbackQuery):
    info = call.data.split(":")
    page = int(info[1])
    try:
        await call.message.edit_text("Список комнат", reply_markup=await get_rooms_keyboard(page))
    except:
        await call.answer("Список комнат не изменился")


@router.callback_query(F.data.startswith("join_room"))
async def join_room(call: CallbackQuery, state: FSMContext):
    info = call.data.split(":")
    room_id = int(info[1])
    status = info[2]
    if status == "open":
        room = await get_room(room_id)
        if room[2] == 0:
            if not await get_user_in_room(call.message.chat.id):
                str_field = fields[randint(0, len(fields) - 1)]
                field = to_matrix(str_field)
                await state.update_data(field=field, room_id=room_id)
                img_field = await draw_field(field)
                img = BufferedInputFile(img_field, filename="img.png")
                await call.message.answer_photo(photo=img, caption="Пожалуйста, выберите расстановку",
                                                reply_markup=await set_field_keyboard("connect"))
                try:
                    await call.message.delete()
                except:
                    pass
            else:
                await call.answer("Вы уже находитесь в комнате", show_alert=True)
    elif status == "private":
        await call.answer("Вы не можете подключиться в приватную комнату", show_alert=True)
    elif status == "close":
        await call.answer("Комната закрыта", show_alert=True)


@router.callback_query(F.data == "select_create_room")
async def select_create_room(call: CallbackQuery):
    await call.message.edit_text("Выберите тип комнаты", reply_markup=await room_type_keyboard())


@router.callback_query(F.data.startswith("create_room"))
async def create_room(call: CallbackQuery, state: FSMContext):
    info = call.data.split(":")
    room_type = info[1]
    if not await get_user_in_room(call.message.chat.id):
        str_field = fields[randint(0, len(fields) - 1)]
        field = to_matrix(str_field)
        await state.update_data(field=field)
        img_field = await draw_field(field)
        img = BufferedInputFile(img_field, filename="img.png")
        await call.message.answer_photo(photo=img, caption="Пожалуйста, выберите расстановку",
                                        reply_markup=await set_field_keyboard(room_type))
        try:
            await call.message.delete()
        except:
            pass
    else:
        await call.answer("Вы уже находитесь в комнате", show_alert=True)


@router.callback_query(F.data.startswith("random_field"))
async def random_field(call: CallbackQuery, state: FSMContext):
    info = call.data.split(":")
    room_type = info[1]
    str_field = fields[randint(0, len(fields) - 1)]
    field = to_matrix(str_field)
    await state.update_data(field=field)
    img_field = await draw_field(field)
    img = BufferedInputFile(img_field, filename="img.png")
    await call.message.edit_media(media=InputMediaPhoto(media=img), reply_markup=await set_field_keyboard(room_type))
    await call.message.edit_caption(caption="Пожалуйста, выберите расстановку",
                                    reply_markup=await set_field_keyboard(room_type))


@router.callback_query(F.data.startswith("start_game"))
async def start_game(call: CallbackQuery, state: FSMContext):
    try:
        if not await db.is_user_in_any_room(call.message.chat.id):
            info = call.data.split(":")
            room_type = info[1]
            data = await state.get_data()
            field = data['field']
            await state.clear()
            m_id = call.message.message_id
            room_id = None

            if room_type == "public" or room_type == "private":
                room_id = await db.create_new_room(room_type, call.message.chat.id, to_string(field), m_id,
                                                    call.message.chat.first_name)
                data = await state.get_data()
                field = data['field']
                m_id = call.message.message_id
                name = call.message.chat.first_name
                await db.add_user_to_room(room_id, call.message.chat.id,to_string(field), m_id, name) # Добавление пользователя в комнату
                await call.message.edit_caption(caption="Комната создана\n\nОжидаем соперника",
                                                reply_markup=await settings_room_keyboard(room_id, call.message.chat.id))

            elif room_type == "bot":  # Логика игры с ботом
                bot_field = data['bot_field']
                room_id = await db.create_new_room_bot(room_type, call.message.chat.id, to_string(field), m_id,
                                                        call.message.chat.first_name, bot_field)
                await db.add_user_to_room(room_id, call.message.chat.id,to_string(field), m_id, name) # Добавление пользователя в комнату
                await call.message.edit_caption(caption=f"Игра против бота началась!\nВаш ход:",
                                                reply_markup=await field_keyboard(bot_field))

            elif room_type == "connect":
                room_id = data['room_id']
                room = await db.get_room(room_id)
                if room and (room[2] == 0 or room[2] == 1): # Проверка на существование комнаты и наличие свободного места
                    data = await state.get_data()
                    field = data['field']
                    m_id = call.message.message_id
                    name = call.message.chat.first_name
                    await db.add_user_to_room(room_id, call.message.chat.id,to_string(field), m_id, name) # Добавление пользователя в комнату
                    await add_user_to_room(room_id, call.message.chat.id, to_string(field), m_id,
                                           call.message.chat.first_name)
                    await call.message.edit_caption(caption=f"Противник: {room[9]}\n\nОжидаем ход соперника",
                                                    reply_markup=await field_keyboard(room[5]))
                    await call.bot.edit_message_caption(chat_id=room[1], message_id=room[3],
                                                        caption=f"Противник: {call.message.chat.first_name}\n\nВаш ход:",
                                                        reply_markup=await field_keyboard(field))
                else:
                    await call.answer("Комната уже заполнена или не существует", show_alert=True)

            #  В случае успешного создания/подключения к комнате:
            if room_id:
                await call.answer("Игра началась!", show_alert=False)

        else:
            await call.answer("Вы уже находитесь в комнате", show_alert=True)

    except KeyError as e:
        await call.answer(f"Ошибка: Недостающие данные в state: {e}", show_alert=True)
    except Exception as e:
        await call.answer(f"Произошла ошибка: {e}", show_alert=True)
        config.logger.exception(f"Ошибка в коллбеке start_game: {e}")



@router.callback_query(F.data.startswith("fire"))
async def fire(call: CallbackQuery):
    info = call.data.split(":")
    x = int(info[1])
    y = int(info[2])
    status = info[3]
    if status == "bot":
        game = await get_room_bot_by_user_id(call.message.chat.id)
        if game:
            bot_field = to_matrix(game[5])
            player_field = to_matrix(game[2])
            x, y = choice(get_available_moves(bot_field))
            if player_field[x][y] == "0":
              player_field[x][y] = "7"
            else:
              player_field[x][y] = "5"

            await update_player_field(game[0], to_string(player_field))
            img_field = await draw_field(player_field)
            img = BufferedInputFile(img_field, filename="img.png")

            await call.message.edit_media(media=InputMediaPhoto(media=img), reply_markup=await field_keyboard(game[5]))
            await call.message.edit_caption(caption=f"Ход бота.\nВаш ход:")
    if status == "yes":
        game = await get_room_by_user_id(call.message.chat.id)
        if game:
            number_player = get_number_player(call.message.chat.id, game)
            field = to_matrix(game[7 - number_player])
            if number_player == game[7]:
                # Если клетка пустая
                if field[x][y] == "0":
                    field[x][y] = "7"
                    str_field = to_string(field)
                    await update_field_and_current_move(game[0], str_field, number_player)
                    img_field = await draw_field(field)
                    img = BufferedInputFile(img_field, filename="img.png")
                    await call.bot.edit_message_media(chat_id=game[3 - number_player],
                                                      message_id=game[5 - number_player],
                                                      media=InputMediaPhoto(media=img),
                                                      reply_markup=await field_keyboard(game[4 + number_player]))
                    await call.bot.edit_message_caption(chat_id=game[3 - number_player],
                                                        message_id=game[5 - number_player],
                                                        caption=f"Противник: {call.message.chat.first_name}\n\nВаш ход:",
                                                        reply_markup=await field_keyboard(game[4 + number_player]))
                    await call.message.edit_caption(
                        caption=f"Противник: {game[11 - number_player]}\n\nОжидаем ход соперника",
                        reply_markup=await field_keyboard(str_field))
                # Если клетка с кораблем
                else:
                    current = field[x][y]
                    same_cells_count = 0
                    for i in range(6):
                        for j in range(6):
                            if field[i][j] == current:
                                same_cells_count += 1
                    # Если клетка это не последняя клетка корабля
                    if same_cells_count > 1:
                        field[x][y] = "5"
                        str_field = to_string(field)
                        await update_field_without_move(game[0], str_field, number_player)
                        img_field = await draw_field(field)
                        img = BufferedInputFile(img_field, filename="img.png")
                        await call.bot.edit_message_media(chat_id=game[3 - number_player],
                                                          message_id=game[5 - number_player],
                                                          media=InputMediaPhoto(media=img),
                                                          reply_markup=await field_keyboard(game[4 + number_player]))
                        await call.bot.edit_message_caption(chat_id=game[3 - number_player],
                                                            message_id=game[5 - number_player],
                                                            caption=f"Противник: {call.message.chat.first_name}\n\nОжидаем ход соперника",
                                                            reply_markup=await field_keyboard(game[4 + number_player]))
                        await call.message.edit_caption(caption=f"Противник: {game[11 - number_player]}\n\nВаш ход:",
                                                        reply_markup=await field_keyboard(str_field))
                    # Если клетка последняя клетка корабля
                    else:
                        field[x][y] = "6"
                        x_, y_ = x, y
                        same_hit_cells = [[x_, y_]]
                        # Ищем соседние подбитые клетки и помечаем их как уничтоженные
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if 0 <= x_ + i < 6 and 0 <= y_ + j < 6:
                                    if field[x_ + i][y_ + j] == "5":
                                        field[x_ + i][y_ + j] = "6"
                                        x_, y_ = x_ + i, y_ + j
                                        same_hit_cells.append([x_, y_])
                                        for _ in range(int(current) - 1):
                                            if 0 <= x_ + i < 6 and 0 <= y_ + j < 6:
                                                if field[x_ + i][y_ + j] == "5":
                                                    field[x_ + i][y_ + j] = "6"
                                                    x_, y_ = x_ + i, y_ + j
                                                    same_hit_cells.append([x_, y_])
                        # Проверяем, есть ли еще живые корабли
                        if check_field(field):
                            # Если есть, то помечаем клетки вокруг уничтоженного корабля как промахнутые
                            for cell in same_hit_cells:
                                for i in range(-1, 2):
                                    for j in range(-1, 2):
                                        if 0 <= cell[0] + i < 6 and 0 <= cell[1] + j < 6:
                                            if field[cell[0] + i][cell[1] + j] == "0":
                                                field[cell[0] + i][cell[1] + j] = "7"
                            str_field = to_string(field)
                            await update_field_without_move(game[0], str_field, number_player)
                            img_field = await draw_field(field)
                            img = BufferedInputFile(img_field, filename="img.png")
                            await call.bot.edit_message_media(chat_id=game[3 - number_player],
                                                              message_id=game[5 - number_player],
                                                              media=InputMediaPhoto(media=img),
                                                              reply_markup=await field_keyboard(game[
                                                                                                    4 + number_player]))
                            await call.bot.edit_message_caption(chat_id=game[3 - number_player],
                                                                message_id=game[5 - number_player],
                                                                caption=f"Противник: {call.message.chat.first_name}\n\nОжидаем ход соперника",
                                                                reply_markup=await field_keyboard(game[
                                                                                                      4 + number_player]))
                            await call.message.edit_caption(
                                caption=f"Противник: {game[11 - number_player]}\n\nВаш ход:",
                                reply_markup=await field_keyboard(str_field))
                        # Если нет, то игрок победил
                        else:
                            str_field = to_string(field)
                            await update_field_without_move(game[0], str_field, number_player)
                            img_field = await draw_field(field)
                            img = BufferedInputFile(img_field, filename="img.png")
                            await call.bot.edit_message_media(chat_id=game[3 - number_player],
                                                              message_id=game[5 - number_player],
                                                              media=InputMediaPhoto(media=img),
                                                              reply_markup=await field_keyboard(game[
                                                                                                    4 + number_player]))
                            await call.bot.edit_message_caption(chat_id=game[3 - number_player],
                                                                message_id=game[5 - number_player],
                                                                caption=f"Противник: {call.message.chat.first_name}\n\nВы проиграли :(",
                                                                reply_markup=await close_keyboard())
                            await call.message.edit_caption(
                                caption=f"Противник: {game[11 - number_player]}\n\nВы победили!",
                                reply_markup=await close_keyboard())
                            await delete_room(game[0])
                            await update_users_rating(call.from_user.id, game[3 - number_player])
            else:
                await call.answer("Сейчас не ваш ход", show_alert=True)
        else:
            await call.answer("Вы не находитесь в игре", show_alert=True)
    else:
        await call.answer("Данная клетка уже открыта", show_alert=True)

async def get_room_bot_by_user_id(user_id):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM rooms_bot WHERE user_id_1 = {user_id}")
        room = await cursor.fetchone()
        return room
async def update_player_field(room_id, field):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"UPDATE rooms_bot SET field_1 = '{field}' WHERE id = {room_id}")
        await db.commit()

def get_available_moves(field):
    moves = []
    for i in range(6):
        for j in range(6):
            if field[i][j] == '0':
                moves.append((i, j))
    return moves
@router.callback_query(F.data == "stop_game")
async def stop_game(call: CallbackQuery):
    room = await get_room_by_user_id(call.message.chat.id)
    if room:
        number_player = get_number_player(call.message.chat.id, room)
        if number_player == room[7]:
            await call.answer("Вы не можете закончить игру, так как сейчас ваш ход", show_alert=True)
        else:
            if datetime.datetime.strptime(room[8], "%d.%m.%Y %H:%M") + datetime.timedelta(
                    minutes=5) < datetime.datetime.strptime(get_now_time(), "%d.%m.%Y %H:%M"):
                await call.message.edit_caption(caption=f"Противник: {room[11 - number_player]}\n\nВы победили!",
                                                reply_markup=await close_keyboard())
                await call.bot.edit_message_caption(chat_id=room[3 - number_player], message_id=room[5 - number_player],
                                                    caption=f"Противник: {call.message.chat.first_name}\n\nВы были слишком долго афк и проиграли :(",
                                                    reply_markup=await close_keyboard())
                await delete_room(room[0])
                await update_users_rating(call.from_user.id, room[3 - number_player])
            else:
                await call.answer(
                    "Вы не можете закончить игру, так как последний ход противника был совершен менее 5 минут назад",
                    show_alert=True)
    else:
        await call.answer("Вы не находитесь в комнате", show_alert=True)


@router.callback_query(F.data == "give_up")
async def give_up(call: CallbackQuery):
    room = await get_room_by_user_id(call.message.chat.id)
    if room:
        number_player = get_number_player(call.message.chat.id, room)
        await call.message.edit_caption(caption=f"Противник: {room[11 - number_player]}\n\nВы сдались :(",
                                        reply_markup=await close_keyboard())
        await call.bot.edit_message_caption(chat_id=room[3 - number_player], message_id=room[5 - number_player],
                                            caption=f"Противник: {call.message.chat.first_name}\n\nВы победили, противник сдался!",
                                            reply_markup=await close_keyboard())
        await delete_room(room[0])
        await update_users_rating(room[3 - number_player], call.from_user.id)
    else:
        await call.answer("Вы не находитесь в комнате", show_alert=True)


@router.callback_query(F.data == "cancel_room")
async def cancel_room(call: CallbackQuery):
    room_id = await db.get_user_room(call.message.chat.id)
    if room_id:
        await db.delete_room(room_id)  # Удаление комнаты
        await db.remove_user_from_room(call.message.chat.id) # Удаление пользователя из таблицы комнат
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer("Комната удалена")
    else:
        await call.answer("Вы не находитесь в комнате", show_alert=True)


@router.callback_query(F.data == "close")
async def close(call: CallbackQuery):
    await call.message.delete()


# Ловим ошибки
@router.errors(ExceptionMessageFilter(
    "Telegram server says - Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message")
)
class MyHandler(ErrorHandler):
    async def handle(self):
        pass


@router.error()
class MyHandler(ErrorHandler):
    async def handle(self):
        print(self.exception_name)
        print(self.exception_message[self.exception_message.find("exception="):])
        config.logger.error(
            self.exception_name + " | " + self.exception_message[self.exception_message.find("exception="):])