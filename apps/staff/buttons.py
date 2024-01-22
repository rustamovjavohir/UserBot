from datetime import date, datetime

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from apps.staff import constants
from apps.tasks.models import Tasks


def baseMenuButton():
    buttons = [
        [KeyboardButton(constants.REQUEST_AVANS), KeyboardButton(constants.REPORT)],
    ]
    return buttons


def avansButton(has_room_booked: bool = False, has_create_task: bool = False):
    buttons = baseMenuButton()
    if has_create_task:
        buttons.append([
            KeyboardButton(constants.CREATE_TASKS),
            KeyboardButton(constants.SHOW_TASKS),
        ])
    if has_room_booked:
        buttons.append([KeyboardButton(constants.BOOK_ROOM)])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def homeButton():
    buttons = [
        [KeyboardButton(constants.HOME)]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def acceptButton():
    buttons = [
        [KeyboardButton(constants.ACCEPT_REQUEST)],
        [KeyboardButton(constants.HOME)]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def acceptInlineButton(req_id):
    buttons = [
        [InlineKeyboardButton(constants.ACCEPT, callback_data=f"done_{req_id}")],
        [InlineKeyboardButton(constants.REJECT, callback_data=f"not_{req_id}")]
    ]
    return InlineKeyboardMarkup(buttons)


def acceptInlineButton2(req_id):
    buttons = [
        [InlineKeyboardButton(constants.ACCEPT, callback_data=f"sendBoss_{req_id}")],
        [InlineKeyboardButton(constants.REJECT, callback_data=f"not_{req_id}")]
    ]
    return InlineKeyboardMarkup(buttons)


def foodMenuButton():
    button = baseMenuButton()
    button.append([
        KeyboardButton(constants.FOOD_MENU),
        KeyboardButton(constants.GO_KITCHEN),
    ])

    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


def cashierButton():
    button = baseMenuButton()
    button.append([
        KeyboardButton(constants.WRITE_AVANS),
        KeyboardButton(constants.BOOK_ROOM),
    ])
    button.append([KeyboardButton(constants.CREATE_TASKS)])

    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


def workersListButton(workers):
    button = []
    for worker in workers:
        button.append([KeyboardButton(f"{worker.full_name}")])
    button.append([KeyboardButton(constants.HOME)])
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
        InlineKeyboardButton(constants.HOME, callback_data=f"room_{room.id}_home"),
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
    button.append([InlineKeyboardButton(constants.HOME, callback_data=f"room_{room.id}_home")])
    return InlineKeyboardMarkup(button)


def dayInlineButton(today: date = datetime.now().date(), prev_date: date = None, next_date: date = None):
    button = []
    inner_button = []
    prefix = 'task'
    if prev_date:
        inner_button.append(
            InlineKeyboardButton("⬅️", callback_data=f"{prefix}_day_{str(prev_date)}_prev")
        )
    inner_button.append(
        InlineKeyboardButton(f"{today}", callback_data=f"{prefix}_day_{today}_select")
    )
    if next_date:
        inner_button.append(
            InlineKeyboardButton("➡️", callback_data=f"{prefix}_day_{str(next_date)}_next")
        )
    button.append(inner_button)
    button.append([InlineKeyboardButton(constants.HOME, callback_data=f"{prefix}_day_close")])

    return InlineKeyboardMarkup(button)


def hourInlineButton(hour: int = 8):
    prefix = 'task'
    button = []
    delta = 24 - hour
    start_hour = 24 - delta + 1
    if delta % 2 == 0:
        for i in range(start_hour, 24, 2):
            button.append([
                InlineKeyboardButton(f"{i}:00", callback_data=f"{prefix}_hour_{i}"),
                InlineKeyboardButton(f"{i + 1}:00", callback_data=f"{prefix}_hour_{i + 1}")
            ])
    else:
        for i in range(start_hour, 23, 2):
            button.append([
                InlineKeyboardButton(f"{i}:00", callback_data=f"{prefix}_hour_{i}"),
                InlineKeyboardButton(f"{i + 1}:00", callback_data=f"{prefix}_hour_{i + 1}")
            ])
        button.append([InlineKeyboardButton(f"{24}:00", callback_data=f"{prefix}_hour_{24}")])
    button.append([InlineKeyboardButton(constants.HOME, callback_data=f"{prefix}_time_close")])
    return InlineKeyboardMarkup(button)


def taskButton(task: Tasks):
    button = [
        InlineKeyboardButton(f"{constants.ACCEPT_TASK}", callback_data=f"task_{task.id}_accept"),
    ]

    return InlineKeyboardMarkup([button])


def completeTaskButton(task: Tasks):
    button = [
        InlineKeyboardButton(f"{constants.COMPLETE_TASK}", callback_data=f"task_{task.id}_complete"),
    ]

    return InlineKeyboardMarkup([button])


def cancelTaskButton(task: Tasks):
    button = [
        InlineKeyboardButton(f"{constants.CANCEL_TASK}", callback_data=f"task_{task.id}_cancel"),
    ]

    return InlineKeyboardMarkup([button])


def confirmCancelTaskButton(task: Tasks):
    button = [
        InlineKeyboardButton(f"{constants.ACCEPT}", callback_data=f"task_{task.id}_yes_cancel"),
        InlineKeyboardButton(f"{constants.REJECT}", callback_data=f"task_{task.id}_no_cancel"),
    ]

    return InlineKeyboardMarkup([button])
