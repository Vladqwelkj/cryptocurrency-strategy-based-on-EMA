
import json
import sqlite3
 
conn = sqlite3.connect("bot.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 


def get_last_stop_id():
    cursor.execute("""SELECT stop 
                   FROM    trades
                   WHERE   id = (SELECT MAX(id)  FROM trades);
               """)
    return json.loads(cursor.fetchall())['order_id']

def get_last_side():
    cursor.execute("""SELECT is_long 
                   FROM    trades
                   WHERE   id = (SELECT MAX(id)  FROM trades);
               """)
    return cursor.fetchall()

#json massive {order_id, is_filled, qty} -stop
#json massive [{order_id, is_filled, qty}, ...] -targets
#json massive [{order_id, start_price, in_fact, qty},...] -enter
