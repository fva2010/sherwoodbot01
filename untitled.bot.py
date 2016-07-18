import telebot
import constants
from flask import Flask, request # Сервер для получения данных
import os
bot = telebot.TeleBot(constants.token)

server = Flask(__name__)  # Создаём сервер


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat_id, "Список возможностей: /list")


@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat_id, "Бот кофейни 'Sherwood' \r Список возможностей: /list")


@bot.message_handler(commands=['list'])
def handle_text(message):
    bot.send_message(message.chat_id, "1 - menu, 2 - something else")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == '1':
        bot.send_message(message.chat_id, "this is menu")
    elif message.text == '2':
        bot.send_message(message.chat_id, "this is something else")
    else:
        bot.send_message(message.chat_id, "I don't know this command")


@server.route("/bot", methods=['POST'])
def getmessage():
    # Чтение данных от серверов telegram
    bot.process_new_messages(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8")).message])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    # Если вы будете использовать хостинг или сервис без https
    # то вам необходимо создать сертификат и
    # добавить параметр certificate=open('ваш сертификат.pem')
    bot.set_webhook(url="https://sherwoodbot01.herokuapp.com/")
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))



