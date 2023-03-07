import re


def isGroup(message):
    return message.chat.type.__eq__('group')


def findMessageId(message: str):
    message = message.split('MessageId')[-1]
    number_list = [float(x) for x in re.findall(r'-?\d+\.?\d*', message)]
    return int(number_list[0])


def sendMessageToGroup(message, user_info):
    text = f'<strong>user:</strong> {user_info}\n' \
           f'<strong>MessageId:</strong> {message.message_id}\n' \
           f'<strong>Text:</strong> {message.message}'
    return text


def sendMessageWithPhoto(message, user_info):
    pass
