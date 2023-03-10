import subprocess
from config.settings import BASE_DIR, S_TOKEN
from telegram import Bot


def dumpDataScript():
    working_directory = BASE_DIR

    # command = 'python manage.py dumpdata > data.json'

    command = 'python manage.py dumpdata --exclude admin_interface --exclude contenttypes > fixtures/data.json'

    # Run the command and wait for it to finish
    subprocess.run(command, cwd=working_directory, shell=True)
    subprocess.run(command, shell=True)

    bot = Bot(token=S_TOKEN)
    bot.send_document(chat_id=779890968, document=open('data.json', 'rb'))


if __name__ == '__main__':
    dumpDataScript()
