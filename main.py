import configure
import data
import datetime
import parsing
import telebot
import time
import schedule


class ConverterClass:
    def __init__(self):
        self.reduction = list()
        self.index1 = list()
        self.index2 = list()
        self.code = list()
        self.LastUpdateDate = datetime.date
        self.update_class()
        self.update_db()

    def update_class(self):
        self.update_db()
        a = parsing.get_rates()
        self.reduction = list()
        self.index1 = list()
        self.index2 = list()
        self.code = list()
        self.LastUpdateDate = datetime.date
        for i in range(len(a) // 5):
            self.code.append(a[i * 5])
            self.reduction.append(a[i * 5 + 1])
            self.index1.append(a[i * 5 + 2])
            self.index2.append(a[i * 5 + 4])

    def update_db(self):
        data.init_db(force=True)
        for i in range(len(self.reduction)):
            data.add_pole(self.reduction[i], self.index2[i])


bot = telebot.TeleBot(configure.TOKEN)
currency = ConverterClass()


def is_not_number(num):
    try:
        float(num)
        return False
    except ValueError:
        return True


@bot.message_handler(commands=['get_info', 'info'])
def print_info(message):
    bot.send_message(message.chat.id, 'This bot has several commands.\n '
                                      '/rate(/get_rate) <reduction> gives you the exchange of this currency and compare '
                                      'it with yesterdays exchange\n'
                                      '/convert <reduction1> <amount> <reduction2> convert <amount> of currency1 into'
                                      ' currency2 ')


@bot.message_handler(commands=['print_rate', 'rate'])
def print_rate(message):
    if currency.reduction.count(message.text.split()[1]) == 0:
        bot.send_message(message.chat.id, "Unknown reduction")
    else:
        i = currency.reduction.index(message.text.split()[1])
        rate = currency.index2[i]
        bot.send_message(message.chat.id, (str(currency.index1[i]) + message.text.split()[1] + ' = ' + rate +
                                           data.compare(rate, message.text.split()[1]) + "RUB"))


@bot.message_handler(commands=['convert'])
def converter(message):
    if not len(message.text.split()) == 4:
        bot.send_message(message.chat.id, "Wrong format")
    else:
        red1 = message.text.split()[1]
        num = (message.text.split()[2])
        red2 = message.text.split()[3]
        if currency.reduction.count(red1) == 0 or currency.reduction.count(red2) == 0 or is_not_number(num):
            bot.send_message(message.chat.id, "Unknown reductions or format")
        else:
            num = float(num)
            pl1 = currency.reduction.index(red1)
            pl2 = currency.reduction.index(red2)
            res = float(float(currency.index2[pl1]) / float(currency.index1[pl1])) / float(
                float(currency.index2[pl2]) / float(currency.index1[pl2]))
            bot.send_message(message.chat.id, str(num) + red1 + " = " + str(res) + red2)


schedule.every().day.at("03:00").do(currency.update_class)


def main_loop():
    while True:
        bot.polling()
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main_loop()

bot.polling(none_stop=True, interval=0)
