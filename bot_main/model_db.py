
import sqlite3
 
conn = sqlite3.connect("bot.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
# Создание таблицы
cursor.execute("""CREATE TABLE trades
                  (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  timestamp datetime,
                  is_long boolean,
                  enter text, 
                  targets text, 
                  stop text,
                  qty INTEGER)
               """)
#json massive {order_id, is_filled} -stop
#json massive [{order_id, is_filled, qty}, ...] -targets
#json massive {order_id, start_price, fact_price} -enter