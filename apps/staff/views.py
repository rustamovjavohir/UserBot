import threading

from apps.staff.utils import *
from apps.staff.models import *


def inform(user_id, active=True):
    worker = getWorker(user_id, active)
    text = f"<strong>F.I.O.:</strong> {worker.full_name}\n"
    text += f"<strong>Bo'lim:</strong> {worker.department.name}\n"
    text += f"<strong>Ish:</strong> {worker.job}\n"
    text += f"<strong>Telefon raqam:</strong> {worker.phone}\n"
    text += f"<strong>Telegram ID:</strong> {worker.telegram_id}\n"
    return text


def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if isWorker(telegram_id=user_id):
        worker = getWorker(user_id)
        if isKitchen(user_id):
            update.message.reply_html(inform(user_id), reply_markup=foodMenuButton())
        elif isCashier(user_id):
            update.message.reply_html(inform(user_id), reply_markup=cashierButton())
        else:
            update.message.reply_html(inform(user_id),
                                      reply_markup=avansButton(has_room_booked=hasPermBookRoom(user_id),
                                                               has_create_task=hasPermCreateTask(user_id)))
        obj, created = Data.objects.get_or_create(telegram_id=user_id)
        obj.telegram_id = user_id
        obj.data = {"step": 0, "name": worker.full_name}
        obj.save()
    else:
        update.message.reply_text(f"ID: {user_id}")


#################################################################################################################
def help_handler(update: Update, context: CallbackContext):
    text = "Bot bo'yicha:\n" \
           "1) Botdan foydalanish uchun /start ni bosing.\n" \
           "2) Botdan foydalanish uchun Radius mobile ishchi bo'lishingiz kerak.\n"
    update.message.reply_text(text)


def order(update: Update, context: CallbackContext):
    """
    step 300: booking room
    step 400: creating task
    """
    user_id = update.message.from_user.id
    if isKitchen(user_id):
        kitchenZone(update, context)
    elif isCashier(user_id):
        cashierZone(update, context)
    elif isWorker(user_id):
        mainZone(update, context)


def mainZone(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    msg = update.message.text
    step = Data.objects.get(telegram_id=user_id).data
    if msg == constants.HOME:
        home(update, context)
    elif step["step"] == 0 and msg == constants.REQUEST_AVANS:
        requestAvans(update, context)
    elif step["step"] == 1:
        setAvans(update, context)
    elif step["step"] == 2 and msg == constants.ACCEPT_REQUEST:
        applyAvans(update, context)
    elif step["step"] == 0 and msg == constants.REPORT:
        report(update, context)
    elif step["step"] == 0 and msg == constants.BOOK_ROOM:
        setEventName(update, context)
    elif step["step"] == 0 and msg == constants.CREATE_TASKS:
        createTask(update, context)
    elif step["step"] == 0 and msg == constants.SHOW_TASKS:
        show_tasks(update, context)
    elif step["step"] == 300:
        bookRooms(update, context)
    elif step["step"] == 400:
        setTaskName(update, context)
    elif step["step"] == 401:
        selectTaskWorker(update, context)
    elif step["step"] == 402:
        setTaskWorker(update, context)
    elif step["step"] == 403:
        pass


def cashierZone(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    msg = update.message.text
    step = Data.objects.get(telegram_id=user_id).data
    if msg == constants.HOME:
        home(update, context, menu_button=cashierButton())
    elif step["step"] == 0:
        if msg == constants.REQUEST_AVANS:
            requestAvans(update, context)
        elif msg == constants.REPORT:
            report(update, context)
        elif msg == constants.WRITE_AVANS:
            createAvans(update, context)
        elif msg == constants.BOOK_ROOM:
            setEventName(update, context)
    elif step["step"] == 1 and msg != constants.HOME:
        setAvans(update, context)
    elif step["step"] == 2 and msg == constants.ACCEPT_REQUEST:
        applyAvans(update, context)
    elif step["step"] == 3:
        selectWorker(user_id, update, context)
    elif step["step"] == 4:
        requestAvans(update, context, step_count=5, is_self=False)
    elif step["step"] == 5 and msg != constants.HOME:
        setAvans(update, context, worker_id=step["other_staff_id"])
    elif step["step"] == 6 and msg == constants.ACCEPT_REQUEST:
        applyAvans(update, context, worker_id=step["other_staff_id"])
    elif step["step"] == 300 and msg != constants.HOME:
        bookRooms(update, context)


def kitchenZone(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    msg = update.message.text
    step = Data.objects.get(telegram_id=user_id).data
    if msg == constants.HOME:
        home(update, context, menu_button=foodMenuButton())
    elif step["step"] == 0:
        if msg == constants.FOOD_MENU:
            step.update({"step": 3})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            update.message.reply_text("Bugungi taomnomani tanlang")
        elif msg == constants.GO_KITCHEN:
            step.update({"step": 4})
            Data.objects.filter(telegram_id=user_id).update(data=step)
            update.message.reply_text("Nechta kishiga joy bor", reply_markup=getFreeSeatsInlineButton())
        elif msg == constants.REQUEST_AVANS:
            requestAvans(update, context)
        elif msg == constants.REPORT:
            report(update, context)
    elif step["step"] == 1 and msg != constants.HOME:
        setAvans(update, context, menu_button=foodMenuButton())
    elif step["step"] == 2 and msg == constants.ACCEPT_REQUEST:
        applyAvans(update, context)
    elif step["step"] == 3 and not msg in [constants.FOOD_MENU, constants.GO_KITCHEN]:
        step.update({"step": 0})
        Data.objects.filter(telegram_id=user_id).update(data=step)
        message = f"Bugun menuda: <strong>{msg}</strong>"
        notification_bot_thread = threading.Thread(target=notificationBot, args=(message,))
        notification_bot_thread.start()
        context.bot.send_message(chat_id=user_id, text="Habar jonatildi", reply_markup=foodMenuButton())
