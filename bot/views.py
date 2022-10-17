from django.shortcuts import render
from django.conf import settings
from telegram import Update, Bot
from telegram.ext import CallbackContext
from bot.models import Message, User, Group
from bot.utils import isGroup, findMessageId, sendMessageToGroup


def start(update: Update, context: CallbackContext):
    try:
        user_id = update.message.from_user.id
        if not User.objects.filter(user_telegram_id=user_id).exists():
            full_name = update.message.from_user.full_name
            username = "@" + update.message.from_user.username
            user = User.objects.create(user_telegram_id=user_id, full_name=full_name, username=username)
        user = User.objects.get(user_telegram_id=user_id)
        update.message.reply_text("Assalomu Aleykum")
    except Exception as ex:
        print(ex)


def main_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user = User.objects.filter(user_telegram_id=user_id).first()
    tg_message = update.message
    if not isGroup(update.message):
        group_id = Group.objects.first().group_id
        user_info = user.full_name
        if user.username:
            user_info = user.username
        if tg_message.photo:
            image = tg_message.photo[-1].file_id
            message = Message.objects.create(message_id=tg_message.message_id,
                                             message=tg_message.caption, user=user, image=image)
            text = sendMessageToGroup(message, user_info)
            context.bot.sendPhoto(chat_id=group_id, photo=image, caption=text, parse_mode="HTML")
        elif update.message.voice:
            voice = update.message.voice.file_id
            message = Message.objects.create(message_id=tg_message.message_id,
                                             message="Voice", user=user, voice=voice)
            text = sendMessageToGroup(message, user_info)
            context.bot.sendVoice(chat_id=group_id, voice=voice, caption=text, parse_mode="HTML")
        else:
            message = Message.objects.create(message_id=tg_message.message_id,
                                             message=tg_message.text, user=user)
            text = sendMessageToGroup(message, user_info)
            context.bot.sendMessage(chat_id=group_id, text=text, parse_mode="HTML")
    else:
        try:
            if len(tg_message.reply_to_message.photo) > 0 or tg_message.reply_to_message.voice:
                message_id = findMessageId(tg_message.reply_to_message.caption)
            else:
                message_id = findMessageId(tg_message.reply_to_message.text)
            client = Message.objects.filter(message_id=message_id).first().user
            if tg_message.photo:
                image = tg_message.photo[-1].file_id
                context.bot.sendPhoto(chat_id=client.user_telegram_id, photo=image, reply_to_message_id=message_id)
            elif tg_message.voice:
                voice = update.message.voice.file_id
                context.bot.sendVoice(chat_id=client.user_telegram_id, voice=voice, reply_to_message_id=message_id)
            else:
                answer = tg_message.text
                context.bot.sendMessage(chat_id=client.user_telegram_id, reply_to_message_id=message_id, text=answer)

        except Exception as ex:
            print(ex)
