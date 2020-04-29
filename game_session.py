#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль сесии игры.
Сесия выполнена в виде объекта класса.
Загружает данные из текстового файла.
"""

from collections import defaultdict
import xlrd


class GameSession:
    """
    Класс описывает объект - сесию.

    Параметры класса:

    **EXIT** — список кнопок. Используется как слово выхода.
    **__words** - множество содержащие города
    **LOAD_FROM** - настройка. Определяет функцию загрузки городов.
        TXT - загрузка из текстового файла
        XLS - загрузка из таблицы
    """

    __words = set()
    EXIT = ("Quit", "Exit", "Clouse", "Выход", "Закончить", "Конец")
    TXT = 'txt'
    XLS = 'xls'
    LOAD_FROM = TXT

    def __init__(self, char_to_start="от а до я"):
        self.__usedword = defaultdict(lambda: True)
        self.__char_start = char_to_start
        self.__chat = self.__class__.__gen_chat(self)

    @property
    def char_start(self):
        return self.__char_start

    @classmethod
    def __gen_chat(cls, self):
        answer = yield f"Пусть игра начнётся! Введите первый город на букву [{self.char_start}]: "
        answer = answer.strip().title()
        while answer not in cls.EXIT:
            back_text = ""

            check = self.check_and_block(answer)
            if check is None:
                back_text = "Такого наазвания нет. Попробуй другое название.\n"
            elif check:
                words = self.find_next_word()
                word = self.check_and_block_from_many(words)
                if word:
                    back_text = f"Теперь я на букву [{word[0]}] - [{word}].\n"
                    if not self.find_next_word():
                        back_text = (
                            f"{back_text}"
                            "Кажется я победил. В моём словере нет больше "
                            f"неиспользованных городов на букву {word[-1]}"
                        )
                        break
                else:
                    back_text = (
                        "Ты победил. Я незнаю больше городов на букву "
                        f"[{answer[-1]}]"
                    )
                    break
            else:
                back_text = "Такое наазвание уже использовано.\n"

            back_text = f"{back_text}Введите название города на букву [{self.char_start}]: "
            answer = yield back_text
            answer = answer.strip().title()
        else:
            back_text = "Уже уходишь(: Я буду тут если ты вдруг захочешь ещё раз поиграть."

        return back_text

    def chat(self, answer: str):
        return self.__chat.send(answer)

    def chat_start(self):
        return next(self.__chat)

    @classmethod
    def __check_word(cls, key: str) -> bool:
        return key in cls._GameSession__words

    @classmethod
    def load_words_from_xls(cls, filename: str = "city.xls") -> bool:
        # открываем файл
        book_city = xlrd.open_workbook(filename)

        # выбираем активный лист
        sheet_city = book_city.sheet_by_index(0)

        # Загружаем столбец с названиями городов в множество (без шапки)
        cls.__words = {sheet_city.row_values(rownum)[1] for rownum in range(
            1, sheet_city.nrows)}

    @classmethod
    def load_words_from_txt(cls, filename: str = "city.txt") -> bool:

        text_file = None
        with open(filename, 'r', encoding='utf-8') as file:
            text_file = file.read()

        if text_file:
            list_city = text_file.split()

            cls.__words = set(list_city)

    @classmethod
    def load_words(cls) -> bool:
        if cls.LOAD_FROM == cls.TXT:
            cls.load_words_from_txt("city.txt")
        elif cls.LOAD_FROM == cls.XLS:
            cls.load_words_from_xls("city.xls")
        else:
            pass

    def check_and_block(self, key: str):
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
        return [word for word in self.__words if (
            word.startswith(self.__char_start))]

    def check_and_block_from_many(self, words):

        for word in words:
            if self.check_and_block(word):
                self.__char_start = word[-1].upper()
                self.__usedword[word] = False
                return word

        return ""


def __main2():
    all_game_setion = dict()

    GameSession.load_words()
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


if __name__ == "__main__":
    __main2()
