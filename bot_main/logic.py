import config
import ta_indicators
import order_manager
from utils import thread_decor

import threading
import websocket
import json
from datetime import datetime
from dateutil import parser
import logging


OHLC = None


@thread_decor
def getting_new_ohlc_in_15min():
	logging.debug('ws getting new ohlc start')
	WSS = 'wss://www.bitmex.com/realtime?subscribe=tradeBin1m,tradeBin5m'
	tmp_price_for_convert = {}
	counter_of_5min = 0 # Раз в 8 часов нужно переподключаться
	def on_message(ws, message):
		msg = json.loads(message)
		#print(msg)
		try:
			if msg['data'][0]['symbol']=='XBTUSD' and msg['table']=='tradeBin5m':
				for name in ['open', 'high', 'low', 'close']:
					tmp_price_for_convert[name].append(data['data'][0][name])
				counter_of_5min += 1
				logging.debug('5min')

				if parser.parse(data['data'][0]['timestamp']).minute % 15 == 0:
					if len(tmp_price_for_convert['close']) < 3: #при первом запуске, можем не успеть получить 15мин свечку.
						return
					tmp_price_for_convert = {}
					order_manager.update_stop()
					add_new_price(tmp_price_for_convert)
					

					signal = is_signal()
					if signal['is_long']:
						order_manager.long()
					if signal['is_short']:
						order_manager.short()


					if counter_of_5min > 90: #есло прошло больше 450 минут, переподключиться
						logging.debug('reconnect getting_new_ohlc_in_15min')
						ws.close()
						getting_new_ohlc_in_15min()
					
		except Exception as er:
			if str(er)=="'data'":
				return
			debug.error(str(er))
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp(WSS, on_message = on_message)
	ws.run_forever()


def get_OHLC(test, symbol):
	global OHLC
	logging.debug('get prepare ohlc')
	client = bitmex.bitmex(test=test)
	OHLC = {'open':[],
				'high':[],
				'low':[],
				'close':[]}
	prices = client.Trade.Trade_getBucketed(
		binSize = '5m',
		symbol = symbol,
		count = 300,
		reverse = True
	).result()[0]

	factor = 3 #15 min / 5min = 3
	OHLC = {'open':[],
				'high':[],
				'low':[],
				'close':[]}
	for n in range(factor, len(prices), factor):
		open_price = prices[n-factor : n][0]['open']
		close_price = prices[n-factor : n][-1]['close']
		low_tmp = []
		high_tmp = []
		for val in prices[n-factor : n]:
			high_tmp.append(val['high'])
			low_tmp.append(val['low'])
		OHLC['open'].append(openPrice)
		OHLC['high'].append(max(high_tmp))
		OHLC['low'].append(min(low_tmp))
		OHLC['close'].append(close_price)
	logging.debug('getted prepare ohlc')


def add_new_price(data):
	global OHLC
	OHLC['open'].append(data[0]['open'])
	OHLC['high'].append(max([c['high'] for c in data]))
	OHLC['low'].append(min([c['low'] for c in data]))
	OHLC['close'].append(data[-1]['close'])
	for name in ['open', 'high', 'low', 'close']:
		del OHLC[name][0]
	logging.debug('added new candle')


def is_signal():
	global OHLC
	ema_source = OHLC['close']
	enter_source = OHLC['close']
	ema = ta_indicators.EMA(ema_source, config.EMA_PERIOD)

	is_long = True
	is_short = True
	for n in range(0, config.CONFIRM_N):
		if enter_source[-1-n] > ema[-1-n]:
			is_short = False
		if enter_source[-1-n] < ema[-1-n]:
			is_long = False
	if is_long or is_short:
		out = {'is_long': is_long, 'is_short': is_short}
		logging.debug('signal '+str(out))
		return 
	else:
		logging.debug('no signal')
		return False

