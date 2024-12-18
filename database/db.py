import asyncio
import aiosqlite
import datetime
from os import system

import pytz


path = "database/database.db"# Определяем путь к файлу базы данных

# Асинхронная функция для проверки базы данных
async def check_db():
    system("cls")
    _datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    databaseFile = path
    async with aiosqlite.connect(databaseFile) as db:
        cursor = await db.cursor()
        try:
            await cursor.execute("SELECT * FROM users")
            print("----   Database was found   ----")
        except aiosqlite.OperationalError:
            print("----   Database not found   ----")
        print(f"-----   {_datetime}   -----")

# Функция для получения текущей даты в формате ДД.ММ.ГГГГ
def get_now_date():
    dt = datetime.datetime.now()
    tz = pytz.timezone("Europe/Moscow")
    mess_date = tz.normalize(dt.astimezone(tz))
    format_date = mess_date.strftime("%d.%m.%Y")
    return format_date

def get_now_time():
    dt = datetime.datetime.now()
    tz = pytz.timezone("Europe/Moscow")
    mess_date = tz.normalize(dt.astimezone(tz))
    format_date = mess_date.strftime("%d.%m.%Y %H:%M")
    return format_date

# Асинхронная функция для проверки, существует ли пользователь с заданным ID в базе данных
async def get_user_exists(user_id):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        user = await cursor.fetchone()
        if user is None:
            return False
        else:
            return True

# Асинхронная функция для добавления нового пользователя в базу данных
async def add_user(user_id, name):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"INSERT INTO users (user_id, name, reg_date) VALUES ({user_id}, '{name}', '{get_now_date()}')")
        await db.commit()

# Асинхронная функция для получения данных пользователя по его ID
async def get_user(user_id):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        user = await cursor.fetchone()
        return user

# Асинхронная функция для получения топ-10 пользователей по рейтингу
async def get_top_10():
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM users ORDER BY rating DESC LIMIT 10")
        users = await cursor.fetchall()
        return users

# Асинхронная функция для получения всех дат регистрации пользователей
async def get_all_reg_date():
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT reg_date FROM users")
        dates = await cursor.fetchall()
        return dates

# Асинхронная функция для получения всех user_id из таблицы users
async def get_all_users_id():
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT user_id FROM users")
        users = await cursor.fetchall()
        return users

# Асинхронная функция для проверки, находится ли пользователь в комнате (по id)
async def get_user_in_room(user_id):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM rooms WHERE user_id_1 = {user_id} OR user_id_2 = {user_id}")
        room = await cursor.fetchone()
        if room is None:
            return False
        else:
            return room[0]

# Асинхронная функция для поиска свободной комнаты (user_id_2 = 0)
async def get_free_room():
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM rooms WHERE user_id_2 = 0")
        room = await cursor.fetchone()
        if room is None:
            return False
        else:
            return room[0]

# Асинхронная функция для получения данных комнаты по ее ID
async def get_room(room_id):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM rooms WHERE id = {room_id}")
        room = await cursor.fetchone()
        return room

# Асинхронная функция для получения всех комнат, отсортированных по user_id_2
async def get_all_rooms():
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM rooms ORDER BY user_id_2")
        rooms = await cursor.fetchall()
        return rooms

# Асинхронная функция для получения данных комнаты по user_id
async def get_room_by_user_id(user_id):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"SELECT * FROM rooms WHERE user_id_1 = {user_id} OR user_id_2 = {user_id}")
        room = await cursor.fetchone()
        return room

# Асинхронная функция для создания новой комнаты
async def create_new_room(room_type, user_id, field, m_id, name):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        if room_type == "public":
            await cursor.execute(f"INSERT INTO rooms (user_id_1, field_1, m_id_1, name_1) VALUES ({user_id}, '{field}', {m_id}, '{name}')")
        elif room_type == "private":
            await cursor.execute(f"INSERT INTO rooms (user_id_1, field_1, m_id_1, name_1, user_id_2) VALUES ({user_id}, '{field}', {m_id}, '{name}', 1)")
        await db.commit()
        await cursor.execute(f"SELECT * FROM rooms WHERE user_id_1 = {user_id}")
        room = await cursor.fetchone()
        return room[0]

# Асинхронная функция для добавления пользователя в существующую комнату
async def add_user_to_room(room_id, user_id, field, m_id, name):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"UPDATE rooms SET user_id_2 = {user_id}, field_2 = '{field}', m_id_2 = {m_id}, name_2 = '{name}', last_move_time = '{get_now_time()}' WHERE id = {room_id}")
        await db.commit()
        return room_id

# Асинхронная функция для обновления игрового поля и текущего хода
async def update_field_and_current_move(room_id, field, number_player):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        current_move = 1 if number_player == 2 else 2
        await cursor.execute(f"UPDATE rooms SET field_{current_move} = '{field}', current_move = {current_move}, last_move_time = '{get_now_time()}' WHERE id = {room_id}")
        await db.commit()

# Асинхронная функция для обновления игрового поля без смены текущего хода
async def update_field_without_move(room_id, field, number_player):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        current_move = 1 if number_player == 2 else 2
        await cursor.execute(f"UPDATE rooms SET field_{current_move} = '{field}', last_move_time = '{get_now_time()}' WHERE id = {room_id}")
        await db.commit()

# Асинхронная функция для удаления комнаты из базы данных
async def delete_room(room_id):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"DELETE FROM rooms WHERE id = {room_id}")
        await db.commit()

# Асинхронная функция для обновления рейтинга пользователей
async def update_users_rating(win_user_id, lose_user_id):
    async with aiosqlite.connect(path) as db:
        cursor = await db.cursor()
        await cursor.execute(f"UPDATE users SET rating = rating + 15 WHERE user_id = {win_user_id}")
        await cursor.execute(f"UPDATE users SET rating = rating - 15 WHERE user_id = {lose_user_id}")
        await db.commit()