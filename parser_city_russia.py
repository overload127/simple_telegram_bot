#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль содержит функцию парсинга страницы с городами из интернета

get_city_russian_wikipedia - получить города с сайта

save_to_txt - сохранить словарь в текстовый файл

save_to_xlsx - сохранить словарь в текстовый таблицу
"""

from datetime import datetime
from collections import defaultdict

from bs4 import BeautifulSoup
import requests
import xlwt

headers = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9;'
                   ' rv:44.0) Gecko/20100101 Firefox/44.0')
      }

# параметр определяет формат сохранения
# txt | xlsx
TXT = 'txt'
XLSX = 'xlsx'
SAVE_TO = TXT


class DownloadError(Exception):
    """Исключение сигнализирующее о том что при загрузке файла произошла ошибка"""
    def __init__(self, text):
        self.txt = text


def main():
    """Пример использования"""
    all_city_list = defaultdict(int)

    get_city_russian_wikipedia(all_city_list)

    if SAVE_TO == TXT:
        save_to_txt(all_city_list)
    elif SAVE_TO == XLSX:
        save_to_xlsx(all_city_list)
    else:
        pass


def get_city_russian_wikipedia(all_city_list: dict) -> None:
    """
    Хранит ссылку на страницу и вызываетпоследовательно
    функции скачки и парсинга

    Параметры:

    **all_city_list** — Пустой словарь для сохранения городов.
    """
    url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8'
    full_html = download_url(url)
    parse_html_city_russian_wikipedia(full_html, all_city_list)


def download_url(url: str) -> str:
    """
    Функция скачки страницы с сайта

    Параметры:

    **url** — Ссылка на страницу сайта которую нужно скачать.

    Возвращяет:
        страницу в тестовой строке
    """
    print("Download page")
    try:
        response = requests.get(url, timeout=30.0, headers=headers)

        response.raise_for_status()
    except requests.HTTPError as http_err:
        raise DownloadError(f'HTTP error occurred: {http_err}')
    except requests.RequestException as err:
        raise DownloadError(('Other RequestException '
                             f'error occurred: {err}'))
    except Exception as err:
        raise DownloadError(f'Other error occurred: {err}')
    else:
        print('Download page Success!')

    return response.text


def parse_html_city_russian_wikipedia(full_html: str, all_city_list: dict) -> None:
    """
    функция парсинга страницы википедии с городами.

    Параметры:

    **str** — Скаченная страница сайта википедии.
    **all_city_list** — Пустой словарь для сохранения городов.

    Возвращяет:
        страницу в тестовой строке
    """
    print("Parse site [wikipedia]")
    soup = BeautifulSoup(full_html, 'lxml')
    table = soup.find('table', class_='standard sortable')
    city_all = table.select("table>tbody>tr>td:nth-of-type(3)")

    count_city = 0
    for line in city_all:

        cur_city = line.text.strip()
        all_city_list[cur_city] += 1
        count_city += 1

    print(f'Parse site [wikipedia] Success! Add [{count_city}] city(s)')


def save_to_xlsx(all_city_list: dict) -> None:
    """
    функция сохранения словаря с городами в файл xlsx (таблица)

    Параметры:

    **all_city_list** — Пустой словарь для сохранения городов.
    """
    print('Save city to excel')
    HEAD = ("№", "Город", "Сколько раз встречается")
    NUMBER, CITY, COUNT = 0, 1, 2
    wb = xlwt.Workbook()
    ws = wb.add_sheet('all_proxy')

    count = 0
    ws.write(count, NUMBER, HEAD[NUMBER])
    ws.write(count, CITY, HEAD[CITY])
    ws.write(count, COUNT, HEAD[COUNT])
    count += 1
    for key in all_city_list:
        ws.write(count, NUMBER, count+1)
        ws.write(count, CITY, key)
        ws.write(count, COUNT, all_city_list[key])
        count += 1

    wb.save('city_{0}.xls'.format(
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))

    print('Save city to excel Success!')


def save_to_txt(all_city_list: dict) -> None:
    """
    функция сохранения словаря с городами в файл txt (текстовый файл)

    Параметры:

    **all_city_list** — Пустой словарь для сохранения городов.
    """
    print('Save city to txt')

    filename = 'city_{0}.txt'.format(
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    with open(filename, 'w', encoding='utf-8') as file:
        for key in all_city_list:
            file.writelines(f'{key}\n')

    print('Save city to txt Success!')


if __name__ == "__main__":
    main()
