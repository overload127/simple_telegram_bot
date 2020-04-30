#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль настроек проекта
"""
import logging
import game_session


PROXY = {
    'proxy_url': 'https://181.118.167.104:80/'
}

log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger("bot_log")
logger.setLevel(logging.DEBUG)

log_file = logging.FileHandler('bot.log')
log_file.setFormatter(log_format)

log_out = logging.StreamHandler()
log_out.setFormatter(log_format)

logger.addHandler(log_file)
logger.addHandler(log_out)

# Настрока модуля game_session
game_session.LOAD_FROM = game_session.TXT
