'''
mport bitmex
import config
CLIENT = bitmex.bitmex(
    test=False,
    api_key=config.API_KEY,
    api_secret=config.API_SECRET)
print(dir(CLIENT.Order))

#fc2768ff-1e7d-06ad-5b58-89e7cda0cb68

def edit_order_price(client, orderID, new_price):
    client.Order.Order_amend(orderID=orderID,
                             price=new_price).result()[0]
edit_order_price(CLIENT, 'fc2768ff-1e7d-06ad-5b58-89e7cda0cb68', 1050)


import sqlite3

from datetime import datetime
conn = sqlite3.connect(config.DB_NAME) # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

cursor.execute("""INSERT INTO trades (is_long)
                  VALUES (1)"""
               )
 
# Сохраняем изменения
conn.commit()




class C():
	t = 1
	def __init__(self):
		self.t = 2




from bitmex_websocket import BitMEXWebsocket
import logging
from time import sleep


# Basic use of websocket.
def run():
    logger = setup_logger()

    # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.
    ws = BitMEXWebsocket(endpoint="wss://www.bitmex.com/realtime", symbol="XBTUSD",
                         api_key=None, api_secret=None)

    logger.info("Instrument data: %s" % ws.get_instrument())
  #  ws.exit()
    # Run forever
    while(ws.ws.sock.connected):
       # logger.info("Ticker: %s" % ws.get_ticker())

        #logger.info("Market Depth: %s" % ws.market_depth())
        logger.info("Recent Trades: %s\n\n" % ws.recent_trades())
        sleep(1)


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    run()'''

import websocket
import json
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