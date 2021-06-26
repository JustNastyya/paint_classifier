import telebot
from config import *
from solution import *
from message_from_list import *

bot = telebot.TeleBot(token)


@bot.message_handler(commands = ['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Отправьте фотографию для распознования')


@bot.message_handler(content_types = ['text'])
def send_text(message):  # if users message is a text
    if message.text.lower() == 'стих':
        bot.send_message(message.chat.id, birthday_poem)
    else:
        bot.send_message(message.chat.id, 'Таких команд я не знаю')


def ask_about_error(message):
    global isRunning, e
    answer = message.text.lower()
    if answer == 'да':
        bot.send_message(message.chat.id, 'Хорошо, высылаю ошибку')
        bot.send_message(message.chat.id, e)
        isRunning = False
    elif answer == 'нет':
        bot.send_message(message.chat.id, 'Хорошо, продолжаем')
        isRunning = False
    else:
        msg = bot.send_message(message.chat.id, 'Прошу ответить "да" или "нет"')
        bot.register_next_step_handler(msg, ask_about_error)


@bot.message_handler(content_types= ["photo"])
def verifyUser(message):
    print ("Получил фото")  # message.photo
    try:
        result = get_prediction(message.photo)
        message_text = message_from_list(result) 
        bot.send_message(message.chat.id, message_text)
    except Exception as e:
        msg = bot.send_message(message.chat.id,
            'Что-то пошло не так.. Хотите посмотреть ошибку? (введите "да" или "нет")')
        bot.register_next_step_handler(msg, ask_about_error)
        isRunning = True


bot.polling(none_stop=True)