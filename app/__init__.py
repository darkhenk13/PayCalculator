from prometheus_client import start_wsgi_server, make_wsgi_app
import os
import requests
import json
from datetime import datetime
from calendar import monthrange
import logging
import telebot


logging.getLogger().setLevel(level=os.environ.get('LOGLEVEL', 'INFO').upper())
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")


logging.info('Application initialization')


#start_http_server(8000)

app = make_wsgi_app(disable_compression=True)

start_wsgi_server(8000)

from app.telegramBot import telegramBot


