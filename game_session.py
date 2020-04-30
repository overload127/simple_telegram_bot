#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль сесии игры.
Сесия выполнена в виде объекта класса.
Загружает данные из текстового файла.
"""
from collections import defaultdict
import xlrd


# **LOAD_FROM** - настройка. Определяет функцию загрузки городов.
# TXT - загрузка из текстового файла
# XLS - загрузка из таблицы
TXT = 'txt'
XLS = 'xls'
# Определена в конце и если это главный модуль
# LOAD_FROM = XLS


class GameSession:
    """
    Класс описывает объект - сесию.

    Параметры класса:

    **EXIT** — список кнопок. Используется как слово выхода.
    **__words** - множество содержащие города
    """

    __words = set()
    EXIT = ("Quit", "Exit", "Clouse", "Выход", "Закончить", "Конец")

    def __init__(self, string_to_start="от а до я"):
        """
        Параметры:

        **string_to_start** - приветственная строка для ввода.
        """
        # Словарь использованных слов
        self.__usedword = defaultdict(lambda: True)
        self.__char_start = string_to_start
        # Создаём генератор сессии и привязываем к объекту.
        self.__chat = self.__class__.__gen_chat(self)

    @property
    def char_start(self):
        """Метод возвращает одноимённую переменную"""
        return self.__char_start

    @classmethod
    def __gen_chat(cls, self):
        """Главная функцияигры в слова.

        Выполнены в виде единого генератора.

        Парметр yield:
        **1** - строка содержащая название города.
        **2** - строка содержащая название города.
        Возвращает yield:
        **1** - строку - ответ.
        **2** - строку - ответ.
        Возвращает return:
        строку прощания
        """
        # 1 yield
        answer = yield "Пусть игра начнётся! Введите первый " \
            f"город на букву [{self.char_start}]: "
        answer = answer.strip().title()
        # бесконечный цикл. Завершение по вводу одного из слов
        # (переменная EXIT)
        while answer not in cls.EXIT:
            back_text = ""

            check = self.check_and_block(answer)
            if check is None:
                back_text = "Такого наазвания нет. Попробуй другое название.\n"
            elif check:
                words = self.find_next_word()
                word = self.check_and_block_from_many(words)
                if word:
                    # word - соддержит строку (город)
                    back_text = f"Теперь я на букву [{word[0]}] - [{word}].\n"
                    # Проверка, есть ли ещё города на букву.
                    if not self.find_next_word():
                        back_text = (
                            f"{back_text}"
                            "Кажется я победил. В моём словере нет больше "
                            f"неиспользованных городов на букву {word[-1]}"
                        )
                        break
                else:
                    # word - None
                    back_text = (
                        "Ты победил. Я незнаю больше городов на букву "
                        f"[{answer[-1]}]"
                    )
                    break
            else:
                back_text = "Такое наазвание уже использовано.\n"

            back_text = f"{back_text}Введите название города на "\
                f"букву [{self.char_start}]: "
            # 2 yield
            answer = yield back_text
            answer = answer.strip().title()
        else:
            back_text = "Уже уходишь(: Я буду тут если ты вдруг захочешь " \
                "ещё раз поиграть."

        return back_text

    def chat(self, answer: str):
        """скрывает под методом обращение к генератору

        Параметры:

        **answer** - название города (от игрока)

        return - транслирует сообщение из генератора
        """
        return self.__chat.send(answer)

    def chat_start(self):
        """скрывает под методом инициализацию генератора

        return - транслирует сообщение из генератора
        """
        return next(self.__chat)

    @classmethod
    def __check_word(cls, key: str) -> bool:
        """метод проверяет возможность использования названия города

         Параметры:

        **key** - название города (от игрока)

        return - true | False в зависимости от наличия всловаре
        """
        return key in cls._GameSession__words

    @classmethod
    def load_words_from_xls(cls, filename: str = "city.xls") -> bool:
        """Загрузка слов из файла xls

         Параметры:

        **filename** - строка с названием файла

        return - true | False в зависимости от наличия всловаре
        """
        try:
            # открываем файл
            book_city = xlrd.open_workbook(filename)

            # выбираем активный лист
            sheet_city = book_city.sheet_by_index(0)

            # Загружаем столбец с названиями городов в множество (без шапки)
            cls.__words = {sheet_city.row_values(
                rownum)[1] for rownum in range(
                1, sheet_city.nrows)}

            return True
        except Exception as err:
            print("ERROR")
            print(err)
            return False

    @classmethod
    def load_words_from_txt(cls, filename: str = "city.txt") -> bool:
        """Загрузка слов из файла txt

         Параметры:

        **filename** - строка с названием файла

        return - true | False в зависимости от наличия всловаре
        """
        try:
            text_file = None
            with open(filename, 'r', encoding='utf-8') as file:
                text_file = file.read()

            if text_file:
                list_city = text_file.split()

                cls.__words = set(list_city)

            return True
        except IOError as err:
            print(f"I/O error({err.errno}): {err.strerror}")
            return False

    @classmethod
    def load_words(cls) -> bool:
        """Метод выбирает свпособ загрузки файлов"""
        if LOAD_FROM == TXT:
            res = cls.load_words_from_txt("city.txt")
        elif LOAD_FROM == XLS:
            res = cls.load_words_from_xls("city.xls")
        else:
            # Что-то пошло не так.
            # Сооьщаем, что не удалось загрузить слова
            res = False

        return res

    def check_and_block(self, key: str):
        """Метод проверяет, использовалось ли введённое слово.

        Возвращает:
            False - Использовалось ранее
            True - Не использовалось. И блокирует его.
            None - Такого словав словаре нет
        """
        if self.__class__.__check_word(key):
            if self.__usedword[key]:
                self.__char_start = key[-1].upper()
                self.__usedword[key] = False
                return True
            else:
                return False
        else:
            return None

    def find_next_word(self):
        """Создаёт список не заблокированных слов на определлённую букву"""
        return [word for word in self.__words if (
            word.startswith(self.__char_start))]

    def check_and_block_from_many(self, words):
        """Комп выбирает сово из найденых им. Проверяет его на блок.
        И если оно свободно - блокирует и возвращает его.

        Возвращает:
            word - найденное слово
            "" - пустую строку, если все заблокированны
        """

        for word in words:
            if self.check_and_block(word):
                self.__char_start = word[-1].upper()
                self.__usedword[word] = False
                return word

        return ""


if __name__ == "__main__":
    """Демонстрация использования даного модуля."""

    LOAD_FROM = TXT

    def main():
        all_game_setion = dict()

        if not GameSession.load_words():
            print("Проблема с загрузкой слов из файла.")
            print("Завершение программы.")
            return
        id = 123455678
        all_game_setion[id] = GameSession()
        print(all_game_setion[id].chat_start())
        while True:
            answer = input()
            try:
                print(all_game_setion[id].chat(answer))
            except StopIteration as err:
                all_game_setion[id] = None
                print(err)
                break

    main()
