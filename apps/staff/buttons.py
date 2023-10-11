from datetime import date

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def avansButton(has_room_booked: bool = False):
    buttons = [
        [KeyboardButton('Avans so`rovi'), KeyboardButton('Hisobot')],
    ]
    if has_room_booked:
        buttons.append([KeyboardButton('Xonani band qilish')])
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


def acceptInlineButton2(req_id):
    buttons = [
        [InlineKeyboardButton("✅Tasdiqlash", callback_data=f"sendBoss_{req_id}")],
        [InlineKeyboardButton("❌Rad etish", callback_data=f"not_{req_id}")]
    ]
    return InlineKeyboardMarkup(buttons)


def foodMenuButton():
    button = [
        [
            KeyboardButton("Taomnoma"),
            KeyboardButton("Obetga 🗣")
        ],
        [
            KeyboardButton('Avans so`rovi'),
            KeyboardButton('Hisobot')
        ],
    ]

    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


def cashierButton():
    button = [
        [
            KeyboardButton("Avans yozish"),
            KeyboardButton('Avans so`rovi')
        ],
        [
            KeyboardButton('Xonani band qilish'),
            KeyboardButton('Hisobot')
        ],
    ]

    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


def workersListButton(workers):
    button = []
    for worker in workers:
        button.append([KeyboardButton(f"{worker.full_name}")])

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
            InlineKeyboardButton("0👤", callback_data="0_seat"),
            InlineKeyboardButton("1👤", callback_data="1_seat"),
            InlineKeyboardButton("2👤", callback_data="2_seat"),
            InlineKeyboardButton("3👤", callback_data="3_seat"),

        ],
        [
            InlineKeyboardButton("4👤", callback_data="4_seat"),
            InlineKeyboardButton("5👤", callback_data="5_seat"),
            InlineKeyboardButton("6👤", callback_data="6_seat"),
            InlineKeyboardButton("7👤", callback_data="7_seat"),
        ],
    ]

    return InlineKeyboardMarkup(free_seats_button)


def roomListInlineButton(rooms):
    button = []
    if len(rooms) % 2 == 0:
        for i in range(0, len(rooms), 2):
            button.append([
                InlineKeyboardButton(f"{rooms[i].name}", callback_data=f"room_{rooms[i].id}"),
                InlineKeyboardButton(f"{rooms[i + 1].name}", callback_data=f"room_{rooms[i + 1].id}")
            ])
    else:
        for i in range(0, len(rooms) - 1, 2):
            button.append([
                InlineKeyboardButton(f"{rooms[i].name}", callback_data=f"room_{rooms[i].id}"),
                InlineKeyboardButton(f"{rooms[i + 1].name}", callback_data=f"room_{rooms[i + 1].id}")
            ])
        button.append([InlineKeyboardButton(f"{rooms[-1].name}", callback_data=f"room_{rooms[-1].id}")])
    return InlineKeyboardMarkup(button)


def roomMenuButton(room, date: date = None, prev_date: date = None, next_date: date = None):
    button = []
    inner_button = []
    if prev_date:
        inner_button.append(
            InlineKeyboardButton("⬅️", callback_data=f"room_{room.id}_{str(prev_date)}_prev")
        )
    inner_button.append(
        InlineKeyboardButton("📅Bron qilish", callback_data=f"room_{room.id}_{str(date)}_book")
    )
    if next_date:
        inner_button.append(
            InlineKeyboardButton("➡️", callback_data=f"room_{room.id}_{str(next_date)}_next")
        )
    button.append(inner_button)
    button.append([
        InlineKeyboardButton("🏠Bosh sahifa", callback_data=f"room_{room.id}_home"),
    ])

    return InlineKeyboardMarkup(button)


def freeRoomHoursInlineButton(room, hours, command: str = "start"):
    button = []
    if len(hours) > 0:
        if len(hours) % 2 == 0:
            for i in range(0, len(hours), 2):
                button.append([
                    InlineKeyboardButton(f"{hours[i]}:00", callback_data=f"room_{room.id}_{hours[i]}_{command}"),
                    InlineKeyboardButton(f"{hours[i + 1]}:00", callback_data=f"room_{room.id}_{hours[i + 1]}_{command}")
                ])
        else:
            for i in range(0, len(hours) - 1, 2):
                button.append([
                    InlineKeyboardButton(f"{hours[i]}:00", callback_data=f"room_{room.id}_{hours[i]}_{command}"),
                    InlineKeyboardButton(f"{hours[i + 1]}:00", callback_data=f"room_{room.id}_{hours[i + 1]}_{command}")
                ])
            button.append(
                [InlineKeyboardButton(f"{hours[-1]}:00", callback_data=f"room_{room.id}_{hours[-1]}_{command}")])
    button.append([InlineKeyboardButton("🏠Bosh sahifa", callback_data=f"room_{room.id}_home")])
    return InlineKeyboardMarkup(button)
