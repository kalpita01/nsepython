import logging
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pynse import *
import json

logging.basicConfig(level=logging.DEBUG)

#initialize your bots API KEY over here
API_KEY = "xxxxxxxxxxxxxxxxxxxxxx"

bot = telebot.TeleBot(API_KEY)
nse = Nse()


stock_code_global = ""
future_stock_global = False
cash_stock_global = False
option_chain_week_global = False
option_chain_month_global = False


def value_stock_code_global(value):
    global stock_code_global
    stock_code_global = value


def value_option_chain_week_global(value):
    global option_chain_week_global
    option_chain_week_global = value


def value_option_chain_month_global(value):
    global option_chain_month_global
    option_chain_month_global = value


def future_stock_code_global(value):
    global future_stock_global
    future_stock_global = value


def cash_stock_code_global(value):
    global cash_stock_global
    cash_stock_global = value


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


def nifty_50(para):
    if para == "nifty":
        nifty_50 = nse.get_indices(IndexSymbol.Nifty50)
    else:
        nifty_50 = nse.get_indices(IndexSymbol.NiftyBank)
    result = nifty_50.to_json(orient="split")
    parsed = json.loads(result)
    data = json.dumps(parsed, indent=4)
    finaldata = json.loads(data)
    return finaldata


def option_chain_func(para, amount, stock_name_small):
    stock_name = stock_name_small.upper()
    if para == "week":
        data = nse.option_chain(stock_name, expiry=dt.date(2021, 5, 27))
    if para == "month":
        data = nse.option_chain(stock_name, expiry=dt.date(2021, 5, 27))
    finaldata = data.loc[data["strikePrice"] == int(amount)]
    if finaldata.empty:
        return 0
    else:
        result = finaldata.to_json(orient="split")
        parsed = json.loads(result)
        value = json.dumps(parsed, indent=4)
        final_data = json.loads(value)
        return final_data


def print_option_chain_func(finaldata):
    msg = str(finaldata['data'][0][4])
    msg += "\n\nStrike Price: " + str(finaldata['data'][0][0])
    msg += "\nCE Open Interest: " + str(finaldata['data'][0][6])
    msg += "\nPE Open Interest: " + str(finaldata['data'][0][25])
    msg += "\nCE Implied Volatility: " + str(finaldata['data'][0][10])
    msg += "\nPE Implied Volatility: " + str(finaldata['data'][0][29])
    msg += "\nCE Last Price: " + str(finaldata['data'][0][11])
    msg += "\nPE Last Price: " + str(finaldata['data'][0][30])
    msg += "\nCE Percent Change: " + str(round(finaldata['data'][0][13])) + "%"
    msg += "\nPE Percent Change: " + str(round(finaldata['data'][0][32])) + "%"
    msg += "\n\n"
    return msg


def print_option_chain(finaldata):
    msg = ""
    msg += "Symbol: " + str(finaldata['index'][0])
    msg += "\nOpen: " + str(finaldata['data'][0][2])
    msg += "\nDay High: " + str(finaldata['data'][0][3])
    msg += "\nDay Low: " + str(finaldata['data'][0][4])
    msg += "\nDay Price: " + str(finaldata['data'][0][5])
    msg += "\nChange: " + str(finaldata['data'][0][7])
    msg += "\nPrevious Close: " + str(finaldata['data'][0][6])
    msg += "\nPercentage Change: " + str(round(finaldata['data'][0][8])) + "%"
    msg += "\nTotal Traded Volume: " + str(finaldata['data'][0][9])
    msg += "\n\n"
    return msg


def print_nifty_50(finaldata):
    msg = str(finaldata['data'][0][1])
    msg += "\n\nOpen: " + str(finaldata['data'][0][5])
    msg += "\nHigh: " + str(finaldata['data'][0][6])
    msg += "\nLow: " + str(finaldata['data'][0][7])
    msg += "\nUnchanged: " + str(finaldata['data'][0][15])
    msg += "\nPrevious Close: " + str(finaldata['data'][0][8])
    msg += "\nPercentage Change: " + str(round(finaldata['data'][0][4])) + "%"
    msg += "\n\n"
    return msg


def print_opt_stock_details(option_data, stock_name):
    opt_msg = ""
    opt_msg = "Symbol: " + str(stock_name).upper()
    opt_msg += "\nStrike Price: " + str(option_data["strikePrice"])
    opt_msg += "\nOpen Price: " + str(option_data["openPrice"])
    opt_msg += "\nHigh Price: " + str(option_data["highPrice"])
    opt_msg += "\nLow Price: " + str(option_data["lowPrice"])
    opt_msg += "\nPrevious Close: " + str(option_data["prevClose"])
    opt_msg += "\nLast Price: " + str(option_data["lastPrice"])
    opt_msg += "\nClose Price: " + str(option_data["closePrice"])
    opt_msg += "\nOpen Interest: " + str(option_data["openInterest"])
    opt_msg += "\nPercentage Change: " + \
        str(round(option_data["pChange"])) + "%"
    opt_msg += "\nTraded Volume: " + str(option_data["tradedVolume"])
    opt_msg += "\nImplied Volatility: " + str(option_data["impliedVolatility"])
    opt_msg += "\nTime: " + str(option_data["timestamp"])
    opt_msg += "\n\n"
    return opt_msg


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


def get_stock_details(stockname):
    try:
        stock = nse.get_quote(stockname)
        return stock
    except:
        return 0


def print_fut_stock_details(future_stock, stock_name):
    value = ""
    value += "Symbol: " + str(stock_name).upper()
    value += "\nOpen Price: " + str(future_stock['openPrice'])
    value += "\nHigh Price: " + str(future_stock['highPrice'])
    value += "\nLow Price: " + str(future_stock['lowPrice'])
    value += "\nClose Price: " + str(future_stock['closePrice'])
    value += "\nLast Price: " + str(future_stock['lastPrice'])
    value += "\nOpen Interest: " + str(future_stock["openInterest"])
    value += "\nPrevious Close Price: " + str(future_stock['prevClose'])
    value += "\nPrevious Change: " + str(round(future_stock['pChange'])) + "%"
    value += "\nstrikePrice: " + str(future_stock['strikePrice'])
    value += "\ntradedVolume: " + str(future_stock['tradedVolume'])
    value += "\ntimestamp: " + str(future_stock['timestamp'])
    value += "\n\n"
    return value


def get_fut_stock_details(stock_name_lower):
    stock_name = stock_name_lower.upper()
    try:
        future_stock = nse.get_quote(
            stock_name, segment=Segment.FUT, expiry=dt.date(2021, 5, 27))
        return future_stock
    except:
        return 0


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
        msg += "\nPercentage Change: " + \
            str(round(finaldata['data'][i][8])) + "%"
        msg += "\nTotal Traded Volume: " + str(finaldata['data'][i][9])
        msg += "\n\n"
    return msg


def print_stock_details(stock):
    value = ""
    value += "Symbol: " + str(stock['symbol'])
    value += "\nSeries: " + str(stock['series'])
    value += "\nOpen: " + str(stock['open'])
    value += "\nClose: " + str(stock['close'])
    value += "\nDay High: " + str(stock['high'])
    value += "\nDay Low: " + str(stock['low'])
    value += "\nPercentage Change: " + str(round(stock['pChange'])) + "%"
    value += "\nPrevious Close: " + str(stock['previousClose'])
    value += "\nQuantity Traded: " + str(stock['quantityTraded'])
    value += "\nTime: " + str(stock['timestamp'])
    value += "\n\n"
    return value


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Cash", callback_data="cash"),
               InlineKeyboardButton("Future", callback_data="future"),
               InlineKeyboardButton("Options", callback_data="option"),
               InlineKeyboardButton("Analysis of options", callback_data="analysis"))
    return markup


def week_or_month():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton(
            "Current Week", callback_data="week_option_chain"),
        InlineKeyboardButton(
            "Current Month", callback_data="month_option_chain"),
    )
    return markup


def cash_stock_func(query):
    cash_stock_code_global(True)
    future_stock_code_global(False)
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id,
                     "Please Enter a stock code starting with /\n\nExample - /infy")


def week_option_chain(query):
    bot.answer_callback_query(query.id)
    value_option_chain_week_global(True)
    value_option_chain_month_global(False)
    bot.send_message(query.message.chat.id,
                     "Enter the stock code and strike amount like /(code) (amount)\n\nExample - /infy 1000")


def month_option_chain(query):
    bot.answer_callback_query(query.id)
    value_option_chain_week_global(False)
    value_option_chain_month_global(True)
    bot.send_message(query.message.chat.id,
                     "Enter the stock code and strike amount like /(code) (amount)\n\nExample - /infy 1000")


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
    msg = print_nifty_50(nifty_50("nifty"))
    bot.send_message(message.chat.id, msg)


@bot.message_handler(regexp="Bank NIFTY")
def bank_nifty_stock_quote(message):
    msg = print_nifty_50(nifty_50("banknifty"))
    bot.send_message(message.chat.id, msg)


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
    elif call.data == "week_option_chain":
        week_option_chain(call)
    elif call.data == "month_option_chain":
        month_option_chain(call)


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


@bot.message_handler(regexp=r"^\/[a-zA-Z]+\s[0-9]+")
def option_chain(message):
    amount = message.text
    data = amount[1:]
    try:
        stock_name = data.split(' ', 1)[0]
        amount = data.split(" ")[1:][0]
        if option_chain_week_global == True and option_chain_month_global == False:
            data = option_chain_func("week", amount, stock_name)
            if data == 0:
                bot.send_message(
                    message.chat.id, "No such strike amount")
            else:
                msg = print_option_chain_func(
                    option_chain_func("month", amount, stock_name))
                bot.send_message(
                    message.chat.id, msg)
        elif option_chain_week_global == False and option_chain_month_global == True:
            data = option_chain_func("month", amount, stock_name)
            if data == 0:
                bot.send_message(
                    message.chat.id, "No such strike amount")
            else:
                msg = print_option_chain_func(
                    option_chain_func("month", amount, stock_name))
                bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, "Error! try again")
            value_option_chain_week_global(False)
            value_option_chain_month_global(False)
    except:
        bot.send_message(message.chat.id, "Please enter proper details")

bot.polling()

