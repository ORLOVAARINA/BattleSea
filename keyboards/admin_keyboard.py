from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)


#Клавиатура admin панели
def admin_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data=f"statistic"),
        ],
        [
            InlineKeyboardButton(text="📨 Рассылка", callback_data=f"send_mailing"),
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

#Клавиатура рассылки
def mailing_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="📨 Отправить", callback_data=f"count_send_mailing"),
            InlineKeyboardButton(text="🔄 Заново", callback_data=f"send_mailing")
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

#Клавиатура подтверждения рассылки
def ask_mailing_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="📨 Отправить", callback_data=f"start_send_mailing")
        ],
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

#Кнопка отмены
def admin_cancel_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="❌", callback_data=f"cancel")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard