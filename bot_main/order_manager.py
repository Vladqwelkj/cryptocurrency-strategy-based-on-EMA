import bitmex
import websocket
import json
from datetime import datetime
from dateutil import parser
import time
import logging
from utils import thread_decor
import utils
import db_interface
import config
from logic import OHLC


CLIENT = bitmex.bitmex(
	test=False,
	api_key=config.API_KEY,
	api_secret=config.API_SECRET)


AMOUNT_FOR_TRADING = None
def update_amount_for_trading():
	global AMOUNT_FOR_TRADING, CLIENT
	AMOUNT_FOR_TRADING = (
		utils.usd_balance(CLIENT, OHLC['close'][-1])
		* (config.PERCENT_CAPITAL_FOR_TRADING/100))
	AMOUNT_FOR_TRADING -= AMOUNT_FOR_TRADING % sum(config.PARTS_EXIT.values())
		 



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
	global AMOUNT_FOR_TRADING, CLIENT
	logging.info('make long')
	update_amount_for_trading()

	position_qty_now = utils.get_position_qty(CLIENT)
	order_qty = 0 if position_qty_now > 0 else position_qty_now # чтобы перекрыть прошлую позицию, если есть
	order_qty += AMOUNT_FOR_TRADING

	original_price = logic.OHLC['close'][-1]
	while True:
		price_now = utils.get_bid_ask_price()['bid']
		enter_order_id = utils.limit_order( # Первоначальное создание входа
			client=CLIENT,
			side='Buy',
			orderQty=order_qty,
			price=price_now)['orderID']
		logging.debug('enter is made')
		time.sleep(0.5)
		if utils.status_by_id(CLIENT, [enter_order_id])[enter_order_id] != 'Canceled':
			break # если ордер нормально выставился, выйти из цикла
		time.sleep(1)

	WSS = 'wss://www.bitmex.com/realtime?subscribe=trade'
	def on_message(ws, message):
		nonlocal price_now
		msg = json.loads(message)['data'][0]
		#print(msg)
		try:
			if msg['symbol']=='XBTUSD':

				tmp_price_memory = price_now
				if msg['side']=='Buy':
					price_now = msg['price'] - 0.5
				if msg['side']=='Sell':
					price_now = msg['price']
			if price_now < tmp_price_memory or price_now > tmp_price_memory:
				if utils.status_by_id(CLIENT, [enter_order_id])[enter_order_id]=='Filled':
					logging.debug('enter is filled')
					ws.close()
					return
			if price_now > tmp_price_memory:
				logging.debug('price changed. edit order')
				edit_order_price(CLIENT, enter_order_id, price_now)

		except Exception as er:
			logging.error('ws enter err:', er)
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp(WSS, on_message = on_message)
	ws.run_forever()




@thread_decor
def short():
	logging.info('make short')
	update_amount_for_trading()


@thread_decor
def make_takes(is_long):
	global AMOUNT_FOR_TRADING, CLIENT
	logging.info('make takes')
	close = logic.OHLC['close'][-1]
	one_part = AMOUNT_FOR_TRADING / sum(config.PARTS_EXIT.values())
	if is_long:
		for procent_take_and_key in config.PARTS_EXIT.keys():
			utils.limit_order(CLIENT,
							  side='Sell',
							  orderQty=one_part*config.PARTS_EXIT[procent_take_and_key],
							  price=close*(1+procent_take_and_key/100),
							  execInst='ReduceOnly')
	if 


@thread_decor
def make_stop(is_long):
	logging.info('make stop')

