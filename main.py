import telebot
import bs4
import requests


bot_api = "5970872432:AAEX3BNMjENYli94J6212S0Hs18aEgZrQak"
url = 'http://www.hmn.ru/index.php?index=45'

bot = telebot.TeleBot(bot_api)
page = requests.get(url)


def coldest(URL):
    r = requests.get(URL)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    coldest_city = soup.select('div > a')
    temperature = soup.select('div > b')
    place = [c.text for c in coldest_city]
    temp = [c.text for c in temperature]
    ans = [place[1], temp[1]]
    return ans


cold = coldest(url)


def hottest(URL):
    idx = 0
    r = requests.get(URL)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    hottest_city = soup.select('div > a')
    temperature = soup.select('div > b')
    ans = [0, 0]
    temp = [c.text for c in temperature]
    for i in temp:
        if i[0] == '+':
            ans[1] = i
            idx = temp.index(i)
            break
    place = [c.text for c in hottest_city]
    ans[0] = place[idx]
    return ans


hot = hottest(url)


def wettest(URL):
    idx = 0
    r = requests.get(URL)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    wettest_city = soup.select('div > a')
    temperature = soup.select('div > b')
    ans = [0, 0]
    temp = [c.text for c in temperature]
    for i in temp:
        if i[2] == '%':
            ans[1] = i
            idx = temp.index(i)
            break
    place = [c.text for c in wettest_city]
    trans = len(place) - len(temp) + 10
    ans[0] = place[idx + trans]
    return ans


wet = wettest(url)


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nЕсли хочешь узнать, что я умею, то пиши /help')


@bot.message_handler(commands=["help"])
def command_help(message):
    bot.send_message(message.chat.id, 'Чтобы узнать самое холодное место - /coldest\n'
                                      'Чтобы узнать самое теплое место - /hottest\n'
                                      'Чтобы узнать самое влажное место - /wettest\n')


@bot.message_handler(commands=["coldest"])
def coldest(message):
    bot.send_message(message.chat.id, 'Город: ' + str(cold[0]) + '\n' + 'Температура: ' + str(cold[1]) + '🥶')


@bot.message_handler(commands=["hottest"])
def hottest(message):
    bot.send_message(message.chat.id, 'Город: ' + str(hot[0]) + '\n' + 'Температура: ' + str(hot[1]) + '🥵')


@bot.message_handler(commands=["wettest"])
def wettest(message):
    bot.send_message(message.chat.id, 'Город: ' + str(wet[0]) + '\n' + 'Влажность: ' + str(wet[1][:3:]) + '💦\n' + 'Температура: ' + str(wet[1][-3::]))


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, message.text)


bot.polling()
