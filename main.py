import logging
import os
from dotenv import load_dotenv
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pynse import *
import json

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)
nse = Nse()


def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Top Gainers')
    itembtn2 = types.KeyboardButton('Top Lossers')
    itembtn3 = types.KeyboardButton('Stock Quote')
    markup.add(itembtn1, itembtn2, itembtn3)
    return markup


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("For cash", callback_data="cash"),
               InlineKeyboardButton("For Futures", callback_data="future"),
               InlineKeyboardButton("For Options", callback_data="option"))
    return markup


def top_gain_or_loss_data(status):
    if status == "gain":
        top_10 = nse.top_gainers(index=IndexSymbol.FnO, length=10)
    elif status == "loss":
        top_10 = nse.top_losers(index=IndexSymbol.FnO, length=10)
    else:
        return
    result = top_10.to_json(orient="split")
    parsed = json.loads(result)
    data = json.dumps(parsed, indent=4)
    finaldata = json.loads(data)
    return finaldata


def message_top_gain_or_loss(finaldata):
    msg = ""
    for i in range(0, 10):
        msg += "Symbol: " + str(finaldata['index'][i])
        msg += "\nSeries: " + str(finaldata['data'][i][1])
        msg += "\nOpen: " + str(finaldata['data'][i][2])
        msg += "\nDay High: " + str(finaldata['data'][i][3])
        msg += "\nDay Low: " + str(finaldata['data'][i][4])
        msg += "\nDay Price: " + str(finaldata['data'][i][5])
        msg += "\nPrevious Close: " + str(finaldata['data'][i][6])
        msg += "\nChange: " + str(finaldata['data'][i][7])
        msg += "\nPercentage Change: " + str(finaldata['data'][i][8]) + "%"
        msg += "\nTotal Traded Volume: " + str(finaldata['data'][i][9])
        msg += "\n\n"
    return msg


def cash_stock_func(query):
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Please Enter a stock code starting with /\n\nExample - /infy")


def future_stock_func(query):
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Please Enter a date in yyyy mm dd format")


def optional_stock_func(query):
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Please enter stock code with strike amount of format (strikeamount)(ce/pe)\n\nExample 1800ce or 1800pe")


@bot.message_handler(commands=['help'])
def send_help(message):
    help_message = "Use /start to get started"
    bot.reply_to(message, help_message)


@bot.message_handler(commands=['start'])
def get_started(message):
    menu = main_menu()
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=menu)


@bot.message_handler(regexp="Top Gainers")
def gain_stats(message):
    gain_message = message_top_gain_or_loss(top_gain_or_loss_data("gain"))
    bot.send_message(message.chat.id, gain_message)


@bot.message_handler(regexp="Top Lossers")
def loss_stats(message):
    loss_message = message_top_gain_or_loss(top_gain_or_loss_data("loss"))
    bot.send_message(message.chat.id, loss_message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cash":
        cash_stock_func(call)
    elif call.data == "future":
        future_stock_func(call)
    elif call.data == "option":
        optional_stock_func(call)


@bot.message_handler(regexp="Stock Quote")
def stock_quote(message):
    bot.send_message(message.chat.id, "Chose an option",
                     reply_markup=gen_markup())


bot.polling()
