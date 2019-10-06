import bitmex
import websocket
import json
from datetime import datetime
from dateutil import parser
import logging
from utils import thread_decor
import db_interface
import config

CLIENT = bitmex.bitmex(
	test=False,
	api_key=config.API_KEY,
	api_secret=config.API_SECRET)

@thread_decor
def update_stop():
	logging.info('update stop')
	order_id = db_interface.get_last_stop_id()


@thread_decor
def check_last_takes():
	logging.info('check_last_takes')

@thread_decor
def check_last_stop():
	logging.info('check_last_stop')

@thread_decor
def long():
	logging.info('make long')


@thread_decor
def short():
	logging.info('make short')

@thread_decor
def make_takes():
	logging.info('make takes')

@thread_decor
def make_stop():
	logging.info('make stop')


@thread_decor
def Getting_new_ohlc(func_to_start):
	WSS = 'wss://www.bitmex.com/realtime?subscribe=trade'
	def on_message(ws, message):
		msg = json.loads(message)
		#print(msg)
		try:
			if msg['data'][0]['symbol']=='XBTUSD':
				if func_to_start:
					func_to_start(data=msg)
		except Exception as er:
			print('err:', er)
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp(WSS, on_message = on_message)
	ws.run_forever()

Getting_new_ohlc(func_to_start=lambda data: print(data['data'][0]))