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

stock_code_global = ""
future_stock_global = False
cash_stock_global = False

# Changing the value of the stock_code global variable


def value_stock_code_global(value):
    global stock_code_global
    stock_code_global = value


def future_stock_code_global(value):
    global future_stock_global
    future_stock_global = value


def cash_stock_code_global(value):
    global cash_stock_global
    cash_stock_global = value

# Startup menu


def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Top Gainers')
    itembtn2 = types.KeyboardButton('Top Lossers')
    itembtn3 = types.KeyboardButton('Real Time Index')
    itembtn4 = types.KeyboardButton('Option Chain')
    itembtn5 = types.KeyboardButton('Stock Quote')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    return markup


def real_time_markup():
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Nifty50')
    itembtn2 = types.KeyboardButton('Bank NIFTY')
    markup.add(itembtn1, itembtn2)
    return markup


# Getting the value of Optional stocks
def get_opt_stock_details(stock_name, amount, type):
    stockname = stock_name.upper()
    if type.lower() == "pe":
        try:
            option_data = nse.get_quote(
                stockname, segment=Segment.OPT, optionType=OptionType.PE, strike=int(amount))
            return option_data
        except:
            return 0
    elif type.lower() == "ce":
        try:
            option_data = nse.get_quote(
                stockname, segment=Segment.OPT, optionType=OptionType.CE, strike=int(amount))
            return option_data
        except:
            return 0
    else:
        return 0

# Printing optional stock details


def print_opt_stock_details(option_data, stock_name):
    opt_msg = ""
    opt_msg = "Symbol: " + str(stock_name).upper()
    opt_msg += "\nStrike Price: " + str(option_data["strikePrice"])
    opt_msg += "\nOpen Price: " + str(option_data["openPrice"])
    opt_msg += "\nHigh Price: " + str(option_data["highPrice"])
    opt_msg += "\nLow Price: " + str(option_data["lowPrice"])
    opt_msg += "\nPrevious Close: " + str(option_data["prevClose"])
    opt_msg += "\nLast Price: " + str(option_data["lastPrice"])
    opt_msg += "\nPercentage Change: " + str(option_data["pChange"]) + "%"
    opt_msg += "\nClose Price: " + str(option_data["closePrice"])
    opt_msg += "\nTraded Volume: " + str(option_data["tradedVolume"])
    opt_msg += "\nImplied Volatility: " + str(option_data["impliedVolatility"])
    opt_msg += "\nTime: " + str(option_data["timestamp"])
    opt_msg += "\n\n"
    return opt_msg

# Printing the analysis part


def print_analysis(option_pe_data, option_ce_data, stock_name):
    opt_msg = ""
    last_price = float(option_pe_data["lastPrice"]) + \
        float(option_ce_data["lastPrice"])
    opt_msg += "Symbol: " + str(stock_name).upper()
    opt_msg += "\nLast Price: " + str(last_price)
    opt_msg += "\nCE Open Interest: " + str(option_ce_data["openInterest"])
    opt_msg += "\nPE Open Interest: " + str(option_pe_data["openInterest"])
    opt_msg += "\nImplied Volatility PE: " + \
        str(option_pe_data["impliedVolatility"])
    opt_msg += "\nImplied Volatility CE: " + \
        str(option_ce_data["impliedVolatility"])
    opt_msg += "\nTiming of CE: " + str(option_ce_data["timestamp"])
    opt_msg += "\nTiming of PE: " + str(option_pe_data["timestamp"])
    opt_msg += "\n\n"
    return opt_msg


# gain or loss data
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

# Getting the Cash stock details of a stock


def get_stock_details(stockname):
    try:
        stock = nse.get_quote(stockname)
        return stock
    except:
        return 0

# Printing the future stock details


def print_fut_stock_details(future_stock, stock_name):
    value = ""
    value += "Symbol: " + str(stock_name).upper()
    value += "\nOpen Price: " + str(future_stock['openPrice'])
    value += "\nHigh Price: " + str(future_stock['highPrice'])
    value += "\nLow Price: " + str(future_stock['lowPrice'])
    value += "\nClose Price: " + str(future_stock['closePrice'])
    value += "\nPrevious Close Price: " + str(future_stock['prevClose'])
    value += "\nLast Price: " + str(future_stock['lastPrice'])
    value += "\nPrevious Change: " + str(future_stock['pChange']) + "%"
    value += "\nstrikePrice: " + str(future_stock['strikePrice'])
    value += "\ntradedVolume: " + str(future_stock['tradedVolume'])
    value += "\ntimestamp: " + str(future_stock['timestamp'])
    value += "\n\n"
    return value

# Getting the value of the future stocks


def get_fut_stock_details(stock_name_lower):
    stock_name = stock_name_lower.upper()
    try:
        future_stock = nse.get_quote(
            stock_name, segment=Segment.FUT, expiry=dt.date(2021, 5, 27))
        return future_stock
    except:
        return 0

# printing of gain or loss


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

# Printing the stock details


def print_stock_details(stock):
    value = ""
    value += "Symbol: " + str(stock['symbol'])
    value += "\nSeries: " + str(stock['series'])
    value += "\nOpen: " + str(stock['open'])
    value += "\nClose: " + str(stock['close'])
    value += "\nDay High: " + str(stock['high'])
    value += "\nDay Low: " + str(stock['low'])
    value += "\nPercentage Change: " + str(stock['pChange']) + "%"
    value += "\nPrevious Close: " + str(stock['previousClose'])
    value += "\nQuantity Traded: " + str(stock['quantityTraded'])
    value += "\nTime: " + str(stock['timestamp'])
    value += "\n\n"
    return value


# Stocks menu
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("For cash", callback_data="cash"),
               InlineKeyboardButton("For Future", callback_data="future"),
               InlineKeyboardButton("For Options", callback_data="option"),
               InlineKeyboardButton("Analysis of options", callback_data="analysis"))
    return markup


def week_or_month():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Current", callback_data="current_option_chain"),
               InlineKeyboardButton(
                   "This Week", callback_data="week_option_chain"),
               InlineKeyboardButton(
                   "This Month", callback_data="month_option_chain"),
               )
    return markup


def cash_stock_func(query):
    cash_stock_code_global(True)
    future_stock_code_global(False)
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Please Enter a stock code starting with /\n\nExample - /infy")


def current_option_chain(query):
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Current option chain")


def week_option_chain(query):
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Week option chain")


def month_option_chain(query):
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "month option chain")


def future_stock_func(query):
    cash_stock_code_global(False)
    future_stock_code_global(True)
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Please Enter a stock code starting with /\n\nExample - /infy")


def optional_stock_func(query):
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Please enter stock code with strike amount of format/(stockcode) (strikeamount)(ce/pe)\n\nExample /infy 1800ce or /infy 1800pe")


def analysis_stock_func(query):
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Please enter stock code with strike amount of format/(stockcode) s (strikeamount)\n\nExample /infy s 1800 ")


@bot.message_handler(commands=['help'])
def send_help(message):
    help_message = "Use /start to get started"
    bot.reply_to(message, help_message)


@bot.message_handler(commands=['start'])
def get_started(message):
    menu = main_menu()
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=menu)


@bot.message_handler(commands=['gain'])
@bot.message_handler(regexp="Top Gainers")
def gain_stats(message):
    gain_message = message_top_gain_or_loss(top_gain_or_loss_data("gain"))
    bot.send_message(message.chat.id, gain_message)


@bot.message_handler(commands=['gain'])
@bot.message_handler(regexp="Top Lossers")
def loss_stats(message):
    loss_message = message_top_gain_or_loss(top_gain_or_loss_data("loss"))
    bot.send_message(message.chat.id, loss_message)


@bot.message_handler(regexp="Stock Quote")
def stock_quote(message):
    bot.send_message(message.chat.id, "Chose an option",
                     reply_markup=gen_markup())


@bot.message_handler(regexp="Real Time Index")
def real_time_index_stock_quote(message):
    bot.send_message(message.chat.id, "Chose an option",
                     reply_markup=real_time_markup())


@bot.message_handler(regexp="Nifty50")
def nifty50_stock_quote(message):
    bot.send_message(message.chat.id, "Nifty50 chosen")


@bot.message_handler(regexp="Bank NIFTY")
def bank_nifty_stock_quote(message):
    bot.send_message(message.chat.id, "bank NIFTYchosen")


@bot.message_handler(regexp="Option Chain")
def bank_nifty_stock_quote(message):
    bot.send_message(message.chat.id, "Choose and option",
                     reply_markup=week_or_month())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cash":
        cash_stock_func(call)
    elif call.data == "option":
        optional_stock_func(call)
    elif call.data == "future":
        future_stock_func(call)
    elif call.data == "analysis":
        analysis_stock_func(call)
    elif call.data == "current_option_chain":
        current_option_chain(call)
    elif call.data == "week_option_chain":
        week_option_chain(call)
    elif call.data == "month_option_chain":
        month_option_chain(call)

# to check stock details


@bot.message_handler(regexp=r"^\/[a-zA-Z]+$")
def cash_stock_details(message):
    temp = message.text
    data = temp[1:]
    stock_name = data
    if future_stock_global == True and cash_stock_global == False:
        stock_details = get_fut_stock_details(stock_name)
        if stock_details == 0:
            bot.send_message(
                message.chat.id, "Please enter a valid expiry date")
        else:
            fut_msg = print_fut_stock_details(stock_details, stock_name)
            bot.send_message(message.chat.id, fut_msg)
    elif cash_stock_global == True and future_stock_global == False:
        stock_details = get_stock_details(data)
        if stock_details == 0:
            bot.send_message(
                message.chat.id, "Please enter a valid stock code")
        else:
            cash_msg = print_stock_details(stock_details)
            bot.send_message(message.chat.id, cash_msg)
    else:
        bot.send_message(message.chat.id, "Error, please try again")
        future_stock_code_global(False)
        cash_stock_code_global(False)


@bot.message_handler(regexp=r"^\/[a-zA-Z]+\s[s]\s[0-9]+$")
def analysis_details(message):
    temp = message.text
    data = temp[1:]
    try:
        stock_name = data.split(' ', 1)[0]
        amount = data.split(" ")[1:][1]
        ce_data = get_opt_stock_details(stock_name, amount, "ce")
        pe_data = get_opt_stock_details(stock_name, amount, "pe")
        if ce_data == 0 or pe_data == 0:
            bot.send_message(message.chat.id, "Please enter valid parameter")
        else:
            msg = print_analysis(ce_data, pe_data, stock_name)
            bot.send_message(message.chat.id, msg)
    except:
        bot.send_message(message.chat.id, "Please enter valid parameter")

# to check optional stock details


@bot.message_handler(regexp=r"^\/[a-zA-Z]+\s[0-9]+[cp]{1}[eE]{1}$")
def opt_stock_details(message):
    temp = message.text
    data = temp[1:]
    try:
        stock_name = data.split(' ', 1)[0]
        code = data.split(" ")[1:][0]
        type = code[-2:]
        amount = code[:-2]
        stock_details = get_opt_stock_details(stock_name, amount, type)
        if stock_details == 0:
            bot.send_message(
                message.chat.id, "Please enter a valid stock code")
        else:
            msg = print_opt_stock_details(stock_details, code)
            bot.send_message(message.chat.id, msg)
    except:
        bot.send_message(message.chat.id, "Please enter a valid parameters")


bot.polling()
