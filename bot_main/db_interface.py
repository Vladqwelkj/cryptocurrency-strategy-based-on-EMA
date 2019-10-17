import config
import json
import sqlite3
import logging
from datetime import datetime
from utils import thread_decor

conn, cursor = None, None


def connect_db():
    global conn, cursor
    logging.debug('try connect to db')
    conn = sqlite3.connect(config.DB_NAME) # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    logging.info('db connected')


@thread_decor
def get_last_stop_id():
    global conn, cursor
    logging.debug('request for last stop_id from db')
    cursor.execute("""SELECT stop 
                   FROM    trades
                   WHERE   id = (SELECT MAX(id)  FROM trades);
               """)
    return json.loads(cursor.fetchone()[0])['order_id']


@thread_decor
def new_enter_db(is_long,
                    enter, enter_in_fact,
                    qty,
                    order_id):
    global conn, cursor
    logging.debug('add new enter to db')
    cursor.execute("""INSERT INTO trades (timestamp, is_long, enter, qty)
                  VALUES ({}, {}, {}, {})""".format(datetime.utcnow(),
                                                    1 if is_long else 0,
                                                    json.dumps({'order_id': order_id, 
                                                                'start_price': enter,
                                                                'fact_price': enter_in_fact}),
                                                    qty))
    conn.commit()
    logging.debug('enter added to db')


@thread_decor
def add_takes_db(orders): #[{order_id, is_filled, qty}, ...] 
    global conn, cursor
    logging.debug('add takes to db')
    sql = """
        UPDATE trades 
        SET targets = {}
        WHERE id = (SELECT MAX(id)  FROM trades);
        """
    cursor.execute(sql.format(json.dumps(orders)))
    conn.commit()
    logging.debug('takes added to db')


@thread_decor
def add_stop_db(order): #[{order_id, is_filled, qty}, ...] 
    global conn, cursor
    logging.debug('add stop to db')
    sql = """
        UPDATE trades 
        SET stop = {}
        WHERE id = (SELECT MAX(id)  FROM trades);
        """
    cursor.execute(sql.format(json.dumps(order)))
    conn.commit()
    logging.debug('stop added to db')

