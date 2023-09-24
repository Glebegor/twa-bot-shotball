import telebot 
from telebot import types
import logging
from flask import Flask, request
import os

TOKEN = os.getenv("TELEGRAM_APITOKEN")
# TOKEN = "6578695473:AAGT5x9Cnt6UjzjBZIlBxS1R28ynUQt22nw"

bot = telebot.TeleBot(TOKEN)
bot.set_my_commands([

])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Hello my friend! Do you want to have awesome experience in TON gaming? To start, use command: /play, or use command: /help, to check bots features.")

@bot.message_handler(commands=['play'])
def send_webgame(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    webbApp = types.WebAppInfo(url='https://10.145.4.142:8080/')
    markup.add(types.InlineKeyboardButton(text='Play!', web_app=webbApp))
    bot.send_message(message.chat.id,"Have a great time!", reply_markup=markup)

if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)   
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://tonanabot.herokuapp.com/")
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)