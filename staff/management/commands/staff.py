from django.core.management import BaseCommand

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config.settings import S_TOKEN
from jobs.updater import startUpdater
from staff.views import order, start
from staff.callback import inline


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        updater = Updater(S_TOKEN)
        updater.dispatcher.add_handler(
            CommandHandler(command='start', filters=Filters.chat_type.private, callback=start))
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.all & Filters.chat_type.private, callback=order))
        updater.dispatcher.add_handler(CallbackQueryHandler(inline))
        startUpdater()
        updater.start_polling()
        updater.idle()
