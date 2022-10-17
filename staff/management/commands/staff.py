from django.core.management import BaseCommand

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config.settings import S_TOKEN
from jobs.updater import start
from staff.views import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        updater = Updater(S_TOKEN)
        updater.dispatcher.add_handler(
            CommandHandler(command='start', filters=Filters.chat_type.private, callback=start))
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.all & Filters.chat_type.private, callback=order))
        updater.dispatcher.add_handler(CallbackQueryHandler(inline))
        start()
        updater.start_polling()
        updater.idle()
