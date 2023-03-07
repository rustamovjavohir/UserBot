from django.conf import settings
from django.core.management import BaseCommand
from telegram.ext import (Updater, Dispatcher, CommandHandler, MessageHandler, Filters)
from apps.bot.views import start, main_handler


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = Updater(settings.TELEGRAM_TOKEN)
        dispatcher: Dispatcher = updater.dispatcher
        updater.dispatcher.add_handler(CommandHandler(command='start', callback=start))
        dispatcher.add_handler(MessageHandler(Filters.all, callback=main_handler))
        # dispatcher.add_handler(MessageHandler(Filters.location, location))
        # updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_callback))
        updater.start_polling()
        updater.idle()
