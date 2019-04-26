import os
import sys
import requests
from time import sleep
from sys import executable
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from Items import item

TOKEN = "857441667:AAG7cUed0t0RKMTD3uDhLz3ZWt61un-UJUU"
reply_keyboard = [['/RusEng'],
                  ['/EngRus']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def setup_proxy_and_start(token, proxy=True):
    # Указываем настройки прокси (socks5)
    address = "aws.komarov.ml"
    port = 1080
    username = "yandexlyceum"
    password = "yandex"

    # Создаем объект updater. В случае отсутствия пакета PySocks установим его
    try:

        updater = Updater(token, request_kwargs={'proxy_url': f'socks5://{address}:{port}/',
                                                 'urllib3_proxy_kwargs': {'username': username,
                                                                          'password': password}} if proxy else None)
        print('Proxy - OK!')

        # Запускаем бота
        main(updater)
    except RuntimeError:
        sleep(1)
        print('PySocks не установлен!')
        os.system(f'{executable} -m pip install pysocks --user')  # pip.main() не работает в pip 10.0.1

        print('\nЗавистимости установлены!\nПерезапустите бота!')
        exit(0)


def get_ll_spn(toponym):
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])

    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]

    # левая, нижняя, правая и верхняя границы из координат углов:
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    # Собираем размеры в параметр span
    span = "{dx},{dy}".format(**locals())

    return (ll, span)


def show_keyboard(bot, update):
    update.message.reply_text("Чтобы убрать клавиатуру нипиши /close", reply_markup=markup)


def close_keyboard(bot, update):
    update.message.reply_text("Ok", reply_markup=ReplyKeyboardRemove())


def start(bot, update):
    update.message.reply_text("Привет! Я многофункциональный бот!\n"
                              "Если не знаешь, что я могу, напиши /help")


def stop(dot, update, user_data):
    user_data["work"] = "None"
    update.message.reply_text("Отдохну пока что.", reply_markup=ReplyKeyboardRemove())


def help(bot, update):
    update.message.reply_text("Сейчас я ничего не делаю, но могу:\n"
                              "Быть переводчиком, для этого напиши /translater\n"
                              "Быть геокодером, для этого напиши /geokoder\n"
                              "Быть продавцем, для этого напиши /seller")


def translater_description(bot, update, user_data):
    user_data["lang"], user_data["work"] = "ru-en", "translater"
    update.message.reply_text("Теперь я переводчик.\n"
                              "Я перевожу с русского на английский.\n"
                              "Чтобы поменять - напиши /show\n"
                              "Чтобы отключить функцию переводчика напиши /stop")


def translater(word, lang):
    accompanying_text = "Переведено сервисом «Яндекс.Переводчик» http://translate.yandex.ru/."
    translator_uri = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    response = requests.get(
                            translator_uri,
                            params={
                                    "key": "trnsl.1.1.20190412T105229Z.39209ab058b86687.4e9bbcab1feb75b5fc753770cdda61d8ca257963",
                                    "lang": lang,
                                    "text": word
                                    }
                            )

    answer = ("\n\n".join([response.json()["text"][0]]))
    return answer


def RusEng(bot, update, user_data):
    user_data["lang"] = "ru-en"


def EngRus(dot, update, user_data):
    user_data["lang"] = "en-ru"


def geocoder_description(bot, update, user_data):
    user_data["work"] = "geocoder"
    update.message.reply_text("Теперь я геокодер.\n"
                              "Напиши название города и я покажу его тебе\n"
                              "Чтобы отключить функцию переводчика напиши /stop")


def geocoder(address):
    geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"

    try:
        response = requests.get(geocoder_uri, params={
                                                      "format": "json",
                                                      "geocode": address
                                                     })
        if not response:
            print("Ошибка выполнения запроса")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)

    toponym = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn(toponym)
    static_api_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map&pt={ll},pm2rdm1".format(**locals())

    return static_api_request


def seller_description(bot, update, user_data):
    user_data["work"] = "seller"
    update.message.reply_text("Теперь я продавец.\n"
                              "Чтобы отключить функцию продовца напиши /stop\n"
                              "Но сейчас приступим к торгам. Купи слона!")


def seller(answer, new_item):
    if answer.lower() == "хорошо":
        answer = ("Ну наконец-то! Хочешь еще чего-нибудь продам?\n"
                  "Если нет, то напиши /stop")
    else:
        answer = """"Все говорят "{}", а ты купи {}""".format(answer, new_item)
    return answer


def total(bot, updater, user_data):
    if user_data["work"] == "geocoder":
        address = updater.message.text
        static_api_request = geocoder(address)
        bot.sendPhoto(updater.message.chat.id, static_api_request)
    elif user_data["work"] == "translater":
        lang = user_data["lang"]
        word = updater.message.text
        answer = translater(word, lang)
        updater.message.reply_text(answer)
    elif user_data["work"] == "seller":
        answer, new_item = updater.message.text, item()
        ans = seller(answer, new_item)
        updater.message.reply_text(ans)


def main(updater):
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, total, pass_user_data=True))

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("show", show_keyboard))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("stop", stop, pass_user_data=True))
    dp.add_handler(CommandHandler("RusEng", RusEng, pass_user_data=True))
    dp.add_handler(CommandHandler("EngRus", EngRus, pass_user_data=True))
    dp.add_handler(CommandHandler("seller", seller_description, pass_user_data=True))
    dp.add_handler(CommandHandler("geokoder", geocoder_description, pass_user_data=True))
    dp.add_handler(CommandHandler("translater", translater_description, pass_user_data=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    setup_proxy_and_start(token=TOKEN, proxy=True)
