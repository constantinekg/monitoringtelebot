#!/usr/bin/env python3

import config
import telebot
import portcheck
import logging
from datetime import datetime
import time
import os
import urllib.request
import socket
import sys
from threading import Thread
import signal
import requests


# Disable python's BIN cache
sys.dont_write_bytecode = True

bot = telebot.TeleBot(config.token)


# Simple help
@bot.message_handler(commands=['start','help'])
def handle_start_help(message):
	bot.send_message(message.chat.id, 'В чате введите символ / и выберите одну из доступных комманд.')


# Return id of user
@bot.message_handler(commands=['myid'])
def handle_start_help(message):
	bot.send_message(message.chat.id, 'Ваш id: '+str(message.chat.id))

# Show current date and time
@bot.message_handler(commands=['clock'])
def handle_start_help(message):
	if str(message.chat.id) == config.constchatid:
		bot.send_message(message.chat.id, socket.gethostname()+': '+str(datetime.now()))


# Check servers status
#@bot.message_handler(commands=['checkservers'])
def checkservers():
    while True:
        res = portcheck.portchecker()
        for i in res[0]:
            bot.send_message(config.constchatid, i)
        if res[1] == 'bad':
            photo = open(os.path.dirname(sys.argv[0])+'/bad.png', 'rb')
            bot.send_photo(config.constchatid, photo)
        else:
            pass
        time.sleep(60)


# Check sites for RETCODE 200
def checksites():
    while True:
        for i in config.sites4check:
            try:
                r = requests.get(i)
                if r.status_code != 200:
                    bot.send_message(config.constchatid, i+' bad http status code - '+str(r.status_code))
                    photo = open(os.path.dirname(sys.argv[0]) + '/bad.png', 'rb')
                    bot.send_photo(config.constchatid, photo)
                else:
                    pass
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print (str(e))
                bot.send_message(config.constchatid, 'can not make connection to '+i+' error: '+str(e))
        time.sleep(60)


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    raise OSError("Couldn't open device!")


def botpool():
    while True:
        try:
            bot.polling(none_stop=True)
            signal.signal(signal.SIGINT, handler)
        except Exception as e:
            logging.error(e)
            signal.signal(signal.SIGINT, handler)
            time.sleep(15)

if __name__ == '__main__':
    try:
        t2 = Thread(target=checkservers).start() # distrowatch thread start
        t3 = Thread(target=checksites).start() # distrowatch thread start
        t1 = Thread(target=botpool).start() # main bot pool thread start
    except KeyboardInterrupt:
        pass
