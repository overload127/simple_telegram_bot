#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# В этом модули находится ключ в переменной YOUR_TOKEN
# YOUR_TOKEN = "строка-токен"
from security import YOUR_TOKEN
# Модуль с настройками
import config


def connect_user(bot, update):
    """Функция регистрации вновь подключённых юзеров к боту

    Параметры:

    **bot** — Вся инфа о боте.
    **update** — Вся инфа о чате с юзером.
    """
    config.logger.debug('Вызван /start')
    text = 'Привет друг!'
    config.logger.debug(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    """Эхо функция - отвечает на полученное сообщение тем же
    самым сообщением. Действует как заглушка.

    Параметры:

    **bot** — Вся инфа о боте.
    **update** — Вся инфа о чате с юзером.
    """
    config.logger.debug('Вызван talk_to_me')
    user_text = update.message.text
    config.logger.debug(user_text)
    update.message.reply_text(user_text)


def main():
    """Основная функция бота"""
    # game_session.GameSession.load_words()
    config.logger.info('Бот запускается')
    mybot = Updater(YOUR_TOKEN,
                    request_kwargs=config.PROXY, use_context=False)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", connect_user))
    # dp.add_handler(CommandHandler("game_in_words", game_in_words_start))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
else:
    print("Данный модуль должен быть главным.")
