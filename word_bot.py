#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главный модуль
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# В этом модули находится ключ в переменной YOUR_TOKEN
# YOUR_TOKEN = "строка-токен"
from security import YOUR_TOKEN
# Модуль с настройками
import config
import game_session

# {user_id:{used_word:set(many words)}}
game_session_for_user = dict()


def connect_user(bot, update):
    """Функция регистрации вновь подключённых юзеров к боту

    Параметры:

    **bot** — Вся инфа о боте.
    **update** — Вся инфа о чате с юзером.
    """
    config.logger.debug('Вызван /start')
    user_id = update.message.chat_id

    msg_text = 'Привет друг! Можешь начинать играть.'

    game_session_for_user[user_id] = game_session.GameSession()
    invite_text = game_session_for_user[user_id].chat_start()

    msg_text = f"{msg_text}\n{invite_text}"
    config.logger.debug(msg_text)
    update.message.reply_text(msg_text)


def game_word_dialog(bot, update):
    """Функция передаёт сообщения от пользователя в игру и обратно

    Параметры:

    **bot** — Вся инфа о боте.
    **update** — Вся инфа о чате с юзером.
    """
    config.logger.debug('Вызван game_word_dialog')
    user_id = update.message.chat_id
    answer = update.message.text

    # используем конструкцию try ... except
    # для отлоова выхода из генератора.
    try:
        msg_text = game_session_for_user[user_id].chat(answer)
    except StopIteration as err:
        game_session_for_user[user_id] = None
        msg_text = err.value

        # Создаём игру заново и выводим результат прошлой
        # и приглашение в новую
        game_session_for_user[user_id] = game_session.GameSession()
        invite_text = game_session_for_user[user_id].chat_start()
        msg_text = f"{msg_text}\nДавай сыграем ещё раз." \
            f"{invite_text}"

    config.logger.debug(msg_text)
    update.message.reply_text(msg_text)


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
    config.logger.info('Бот запускается')
    # Загрузка названий городов в бота
    game_session.GameSession.load_words()
    mybot = Updater(YOUR_TOKEN,
                    request_kwargs=config.PROXY, use_context=False)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", connect_user))
    dp.add_handler(MessageHandler(Filters.text, game_word_dialog))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
else:
    print("Данный модуль должен быть главным.")
