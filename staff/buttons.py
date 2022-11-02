from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def avansButton():
    buttons = [
        [KeyboardButton('Avans so`rovi'), KeyboardButton('Hisobot')],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def homeButton():
    buttons = [
        [KeyboardButton('🏠Bosh sahifa')],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def acceptButton():
    buttons = [
        [KeyboardButton('✅So`rovni tasdiqlayman')],
        [KeyboardButton('🏠Bosh sahifa')]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def acceptInlineButton(req_id):
    buttons = [
        [InlineKeyboardButton("✅Tasdiqlash", callback_data=f"done_{req_id}")],
        [InlineKeyboardButton("❌Rad etish", callback_data=f"not_{req_id}")]
    ]
    return InlineKeyboardMarkup(buttons)
