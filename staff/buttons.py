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


def foodMenuButton():
    button = [
        [
            KeyboardButton("Taomnoma"),
            KeyboardButton("Obetga 🗣")
        ]
    ]

    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


def getMenuListInlineButton():
    menu_button = [
        [
            InlineKeyboardButton("Makaron", callback_data="Makaron_food"),
            InlineKeyboardButton("Say", callback_data="Say_food")
        ],
        [
            InlineKeyboardButton("Tovuq", callback_data="Tovuq_food"),
            InlineKeyboardButton("Osh", callback_data="Osh_food")
        ],
        [
            InlineKeyboardButton("Bishteks", callback_data="Bishteks_food")
        ]

    ]

    return InlineKeyboardMarkup(menu_button)


def getFreeSeatsInlineButton():
    free_seats_button = [
        [
            InlineKeyboardButton("1👤", callback_data="1_seat"),
            InlineKeyboardButton("2👤", callback_data="2_seat"),
            InlineKeyboardButton("3👤", callback_data="3_seat"),
            InlineKeyboardButton("4👤", callback_data="4_seat")
        ],
        [
            InlineKeyboardButton("5👤", callback_data="5_seat"),
            InlineKeyboardButton("6👤", callback_data="6_seat"),
            InlineKeyboardButton("7👤", callback_data="7_seat"),
            InlineKeyboardButton("8👤", callback_data="8_seat")
        ],
    ]

    return InlineKeyboardMarkup(free_seats_button)
