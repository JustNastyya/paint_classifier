import telebot
from config import *

bot = telebot.TeleBot(token)

keyboard = telebot.types.ReplyKeyboardMarkup(True)  # main keyboard with 4 buttons
keyboard.row('Список художников', 'Список стилей', 'Стих')


def send_info(msg, message):
    bot.send_message(message.chat.id, info[msg][1], reply_markup=keyboard)
    photo = open(f'images/{info[msg][0]}', 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands = ['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я могу рассказать о некоторых интересных художниках и стилях!', reply_markup=keyboard)


@bot.message_handler(content_types = ['text'])
def send_text(message):
    msg = message.text.lower()
    if msg == 'стих':
        bot.send_message(message.chat.id, birthday_poem, reply_markup=keyboard)
    elif msg == 'список художников':
        bot.send_message(message.chat.id, painter_list, reply_markup=keyboard)
    elif msg == 'список стилей':
        bot.send_message(message.chat.id, style_list, reply_markup=keyboard)
    elif msg in info.keys():
        send_info(msg, message)
    else:
        bot.send_message(message.chat.id, 'Таких команд я не знаю', reply_markup=keyboard)


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