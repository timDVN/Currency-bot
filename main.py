import configure
import data
import log
import parsing
import schedule
import telebot
import time


class ConverterClass:
    def __init__(self):
        self.reduction = list()  # list of reductions of currencies example "USD","RUB"...
        self.index1 = list()  # list of first indexes in exchange rate example : <index1> <reduction> = <index2> RUB
        self.index2 = list()
        self.update_class()
        self.update_db()

    def update_class(self):
        self.update_db()
        parsing_res = parsing.get_rates()
        # parsing gives list objects like
        # ['036', 'AUD', '1', 'Австралийский доллар', '57.8082', '944', 'AZN', '1','Азербайджанский манат','44.0622'...]
        # <code>(never used in bot)   <reduction> <index1> <name>(never used in bot)  <index2>
        self.reduction = list()
        self.index1 = list()
        self.index2 = list()
        for i in range(len(parsing_res) // 5):  # because every currency has 5 boxes
            self.reduction.append(parsing_res[i * 5 + 1])
            self.index1.append(parsing_res[i * 5 + 2])
            self.index2.append(parsing_res[i * 5 + 4])
        self.reduction.append('RUB')  # addition of Russian ruble
        self.index1.append('1')  #
        self.index2.append('1')  #
        log.logger.debug(f"Update class new amount of currencies in ConvertClass is {len(self.reduction)}")
        if not len(data.currencies_in_db()) == len(self.reduction):
            log.logger.warning(
                f"different number of currencies in ConvertClass and in db {self.reduction}\n "
                f"{data.currencies_in_db()}")

    def update_db(self):
        data.init_db(force=True)  # clearing the database
        for i in range(len(self.reduction)):  # writing new meaning
            data.add_currency(self.reduction[i], self.index2[i])
        log.logger.debug(f"Update db new amount of currencies in db is {len(data.currencies_in_db())}")
        if not len(data.currencies_in_db()) == len(self.reduction):
            log.logger.critical(f"data loss during transfer\n {self.reduction} \n{data.currencies_in_db()}")


bot = telebot.TeleBot(configure.TOKEN)
currency = ConverterClass()


def is_not_number(num):  # is used in converter for checking the correctness of the input
    log.logger.debug(f"Function: is_not_number({num})")
    try:
        float(num)
        return False
    except ValueError:
        return True


@bot.message_handler(commands=['get_info', 'info', 'start'])
def print_info(message):
    log.logger.debug("Function: print_info")
    bot.send_message(message.chat.id, 'This bot has several commands.\n '
                                      '/rate(/get_rate) <reduction> : gives you the exchange of this currency and '
                                      'compare '
                                      'it with yesterdays exchange\n'
                                      '/convert <reduction1> <amount> <reduction2> : convert amount of currency1 into'
                                      ' currency2 \n'
                                      '/ListOfCurrencies : gives you list of currencies which you can use\n'
                                      '/StartMailing <reduction> : you will receive messages with rate of entered '
                                      'currency every day\n'
                                      '/EndMailing <reduction>: you stop receiving everyday messages with entered '
                                      'currency rate\n'
                                      '/MyMailing : gives you list of currencies rates of which you receive in '
                                      'everyday message')


@bot.message_handler(commands=['print_rate', 'rate'])
def print_rate(message):
    log.logger.debug(f"Function: print_rate. message.text = {message.text}")
    give_rate(message.text, message.chat.id)


@bot.message_handler(commands=['convert'])
def converter(message):
    log.logger.debug(f"Function: converter. message.text = {message.text}")
    if not len(message.text.split()) == 4:  # checking the correctness of the input
        bot.send_message(message.chat.id, "Wrong format")
    else:
        currency1 = message.text.split()[1]
        amount = (message.text.split()[2])
        currency2 = message.text.split()[3]
        if currency.reduction.count(currency2) == 0 or currency.reduction.count(currency1) == 0 or is_not_number(
                amount):  # checking the correctness of the input
            bot.send_message(message.chat.id, "Unknown reductions or format")
        else:
            amount = float(amount)
            place1 = currency.reduction.index(currency1)  # the number of values corresponding to this currency1
            # in ConverterClass lists
            place2 = currency.reduction.index(currency2)  # -//-
            res = amount * float(float(currency.index2[place1]) / float(currency.index1[place1])) / float(
                float(currency.index2[place2]) / float(currency.index1[place2]))
            res = round(res, 4)  # rounding to 4 decimal places
            bot.send_message(message.chat.id,
                             str(amount) + " " + currency1 + " = " + str(res) + " " + currency2)  # output


@bot.message_handler(commands=['ListOfCurrencies'])
def send_currencies(message):  # gives you list of currencies which you can use
    log.logger.debug("Function: send_currencies")
    answer = str()
    for reduction in currency.reduction:
        answer = answer + reduction + '\n'
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['StartMailing'])
def start_mailing(message):
    log.logger.debug(f"Function: start_mailing. message.text = {message.text}")
    if checking_format1(message.text):  # checking the correctness of the input
        bot.send_message(message.chat.id, "Unknown reductions or format")
    else:
        data.add_recipient(str(message.chat.id), message.text.split()[1])
        bot.send_message(message.chat.id, 'Start mailing' + message.text.split()[1])


@bot.message_handler(commands=['EndMailing'])
def end_mailing(message):
    log.logger.debug(f"Function: end_mailing. message.text = {message.text}")
    if checking_format1(message.text):  # checking the correctness of the input
        bot.send_message(message.chat.id, "Unknown reductions or format")
    else:
        data.remove_recipient(str(message.chat.id), message.text.split()[1])
        bot.send_message(message.chat.id, 'End of mailing' + message.text.split()[1])


@bot.message_handler(commands=['MyMailing'])
def my_mailing(message):
    log.logger.debug(f"Function: MyMailing. message.text = {message.text}")
    answer = str()
    for reduction in data.list_of_currencies(str(message.chat.id)):
        answer = answer + reduction[0] + '\n'
    bot.send_message(message.chat.id, answer)
    if len(answer) == 0:
        bot.send_message(message.chat.id, "You haven't any mailing")


def give_rate(message, chat_id):
    log.logger.debug(f"Function: give_rate. message = {message}")
    if checking_format1(message):  # checking the correctness of the input
        bot.send_message(chat_id, "Unknown reductions or format")
    else:
        reduction = message.split()[1]
        place = currency.reduction.index(reduction)  # the number of values corresponding to this currency
        # in ConverterClass lists
        rate = currency.index2[place]
        bot.send_message(chat_id, str(currency.index1[place]) + " " + reduction + ' = ' + rate +
                         data.compare(rate, reduction) + "RUB")  # output


def mailing():
    log.logger.debug("Function: mailing")
    recipients = set(data.list_of_recipients())
    for recipient in recipients:
        currencies = data.list_of_currencies(recipient[0])
        for reduction in currencies:
            give_rate(". " + reduction[0], int(recipient[0]))


def checking_format1(message):
    if len(message.split()) < 2:
        log.logger.debug(f"Function: checking_format1. message = {message}. Answer: not correct")
        return True
    elif currency.reduction.count(
            message.split()[1]) == 0:  # checking the correctness of the input
        log.logger.debug(f"Function: checking_format1. message = {message}. Answer: not correct")
        return True
    else:
        log.logger.debug(f"Function: checking_format1. message = {message}. Answer: correct")
        return False


schedule.every().day.at("03:00").do(currency.update_class)  # time to update the currencies rate
schedule.every().day.at("08:00").do(mailing)  # sand mails to people that give consent


def main_loop():
    while True:
        bot.polling()
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    mailing()
    main_loop()
